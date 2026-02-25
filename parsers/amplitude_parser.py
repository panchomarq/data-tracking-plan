"""
Dual-mode parser for Amplitude event taxonomy data.

Supports two source modes:
  - "api"  : live data from the Amplitude Taxonomy API via AmplitudeAPIClient.
  - "csv"  : static CSV export file (original behaviour, used as fallback).

Both modes expose identical public method signatures so that routes,
templates, and API endpoints require zero changes.
"""

import logging
import time
from collections import Counter, defaultdict
from typing import TYPE_CHECKING, Dict, List, Optional

import pandas as pd

if TYPE_CHECKING:
    from services.amplitude_client import AmplitudeAPIClient

logger = logging.getLogger(__name__)


class AmplitudeParser:
    """
    Parser for Amplitude event/property taxonomy data.

    Instantiate with *either* a CSV file path (legacy) or an API client
    instance (live). The ``cache_ttl`` parameter controls how long API
    responses are reused before refetching (seconds, default 900).
    """

    def __init__(
        self,
        file_path: Optional[str] = None,
        api_client: Optional["AmplitudeAPIClient"] = None,
        cache_ttl: int = 900,
    ):
        if api_client is not None:
            self._mode = "api"
            self._client = api_client
            self._cache_ttl = cache_ttl
            self._cache: Dict[str, Dict] = {}
            self._fetch_api_data()
        elif file_path is not None:
            self._mode = "csv"
            self.file_path = file_path
            self.data: Optional[pd.DataFrame] = None
            self._load_csv()
        else:
            raise ValueError("Provide either file_path or api_client")

    # ------------------------------------------------------------------
    # Internal: CSV loading (legacy)
    # ------------------------------------------------------------------

    def _load_csv(self) -> None:
        """Load the CSV export into a pandas DataFrame."""
        try:
            self.data = pd.read_csv(self.file_path, dtype=str, on_bad_lines="skip")
            self.data = self.data.fillna("")
            self.data.columns = self.data.columns.str.strip()
            if "Object Type" in self.data.columns:
                self.data["Object Type"] = self.data["Object Type"].str.strip()
        except Exception as exc:
            raise Exception(f"Error loading Amplitude CSV data: {exc}") from exc

    # ------------------------------------------------------------------
    # Internal: API fetching + caching
    # ------------------------------------------------------------------

    def _is_cache_valid(self) -> bool:
        ts = self._cache.get("_timestamp", 0)
        return (time.time() - ts) < self._cache_ttl

    def _fetch_api_data(self) -> None:
        """Pull events, categories, and per-event properties from the API."""
        if self._is_cache_valid():
            return

        raw_events = self._client.get_events(show_deleted=True)

        categories_list = self._client.get_categories()
        categories_by_id: Dict[int, str] = {
            c["id"]: c["name"] for c in categories_list
        }

        props_by_event: Dict[str, list] = {}
        for ev in raw_events:
            event_name = ev.get("event_type", "")
            if not event_name:
                continue
            try:
                props_by_event[event_name] = self._client.get_event_properties(
                    event_name
                )
            except Exception:
                props_by_event[event_name] = []

        self._cache = {
            "_timestamp": time.time(),
            "events": raw_events,
            "categories": categories_by_id,
            "properties_by_event": props_by_event,
        }
        logger.info(
            "Amplitude API data cached: %d events, %d categories",
            len(raw_events),
            len(categories_by_id),
        )

    def _ensure_api_data(self) -> None:
        """Refresh cache if stale."""
        if not self._is_cache_valid():
            self._fetch_api_data()

    # ------------------------------------------------------------------
    # Helpers to normalise API data into the same shape as CSV data
    # ------------------------------------------------------------------

    def _api_events_list(self) -> List[Dict]:
        """Convert raw API events into the standard event dict list."""
        self._ensure_api_data()
        events = []
        for ev in self._cache.get("events", []):
            cat = ev.get("category") or {}
            cat_name = cat.get("name", "") if isinstance(cat, dict) else str(cat)
            events.append(
                {
                    "name": ev.get("event_type", ""),
                    "display_name": ev.get("display_name", ""),
                    "category": cat_name,
                    "owner": ev.get("owner") or "",
                    "description": ev.get("description") or "",
                    "activity": "ACTIVE" if ev.get("is_active") else "DELETED",
                    "schema_status": "",
                    "volume_180_days": 0,
                    "queries_180_days": 0,
                    "first_seen": "",
                    "last_seen": "",
                }
            )
        return events

    def _api_properties_by_event(self) -> Dict[str, List[Dict]]:
        """Convert raw API properties into the standard shape."""
        self._ensure_api_data()
        result: Dict[str, List[Dict]] = {}
        for event_name, props in self._cache.get("properties_by_event", {}).items():
            result[event_name] = [
                {
                    "name": p.get("event_property", ""),
                    "description": p.get("description") or "",
                    "type": p.get("type") or "",
                    "required": p.get("is_required", False),
                    "is_array": p.get("is_array_type", False),
                    "schema_status": "",
                    "first_seen": "",
                    "last_seen": "",
                }
                for p in props
            ]
        return result

    # ------------------------------------------------------------------
    # Public interface (identical signatures for both modes)
    # ------------------------------------------------------------------

    def get_events_summary(self) -> Dict:
        """
        Comprehensive summary: counts, activity status, categories, schema status, owners.

        Returns:
            Dict with total_events, activity_status, categories, schema_status,
            top_owners, unique_event_names.
        """
        if self._mode == "api":
            events = self._api_events_list()
            activity = Counter(e["activity"] for e in events)
            categories = Counter(e["category"] for e in events if e["category"])
            schema = Counter(e["schema_status"] for e in events if e["schema_status"])
            owners = Counter(e["owner"] for e in events if e["owner"])
            top_owners = dict(owners.most_common(10))
            return {
                "total_events": len(events),
                "activity_status": dict(activity),
                "categories": dict(categories),
                "schema_status": dict(schema),
                "top_owners": top_owners,
                "unique_event_names": len({e["name"] for e in events}),
            }

        events_df = self.data[
            (self.data["Object Type"] == "Event")
            & (self.data["Object Name"].notna())
            & (self.data["Object Name"] != "")
        ]
        return {
            "total_events": len(events_df),
            "activity_status": events_df["Event Activity"].value_counts().to_dict(),
            "categories": events_df["Event Category"].value_counts().to_dict(),
            "schema_status": events_df["Event Schema Status"].value_counts().to_dict(),
            "top_owners": events_df["Object Owner"].value_counts().head(10).to_dict(),
            "unique_event_names": events_df["Object Name"].nunique(),
        }

    def get_properties_summary(self) -> Dict:
        """
        Summary of event properties: counts, types, required breakdown, arrays.

        Returns:
            Dict with total_properties, unique_properties, value_types,
            required_breakdown, schema_status, array_properties_count.
        """
        if self._mode == "api":
            all_props = []
            for props in self._api_properties_by_event().values():
                all_props.extend(props)

            types = Counter(p["type"] for p in all_props if p["type"])
            required = Counter(
                "true" if p["required"] else "false" for p in all_props
            )
            schema = Counter(
                p["schema_status"] for p in all_props if p["schema_status"]
            )
            arrays = sum(1 for p in all_props if p["is_array"])
            unique_names = {p["name"] for p in all_props}
            return {
                "total_properties": len(all_props),
                "unique_properties": len(unique_names),
                "value_types": dict(types),
                "required_breakdown": dict(required),
                "schema_status": dict(schema),
                "array_properties_count": arrays,
            }

        properties_df = self.data[
            (self.data["Event Property Name"].notna())
            & (self.data["Event Property Name"] != "")
        ]
        return {
            "total_properties": len(properties_df),
            "unique_properties": properties_df["Event Property Name"].nunique(),
            "value_types": properties_df["Property Value Type"]
            .value_counts()
            .to_dict(),
            "required_breakdown": properties_df["Property Required"]
            .value_counts()
            .to_dict(),
            "schema_status": properties_df["Property Schema Status"]
            .value_counts()
            .to_dict(),
            "array_properties_count": len(
                properties_df[properties_df["Property Is Array"] == True]  # noqa: E712
            ),
        }

    def get_events_list(self) -> List[Dict]:
        """
        Detailed list of all events with metadata.

        Returns:
            List[Dict] — each dict has name, display_name, category, owner,
            description, activity, schema_status, volume_180_days,
            queries_180_days, first_seen, last_seen.
        """
        if self._mode == "api":
            return self._api_events_list()

        events_df = self.data[
            (self.data["Object Type"] == "Event")
            & (self.data["Object Name"].notna())
            & (self.data["Object Name"] != "")
        ]
        events_list = []
        for _, row in events_df.iterrows():
            vol = str(row.get("Event 180 Day Volume", "0")).strip()
            qry = str(row.get("Event 180 Day Queries", "0")).strip()
            events_list.append(
                {
                    "name": row["Object Name"],
                    "display_name": row.get("Event Display Name", ""),
                    "category": row.get("Event Category", ""),
                    "owner": row.get("Object Owner", ""),
                    "description": row.get("Object Description", ""),
                    "activity": row.get("Event Activity", ""),
                    "schema_status": row.get("Event Schema Status", ""),
                    "volume_180_days": int(vol) if vol else 0,
                    "queries_180_days": int(qry) if qry else 0,
                    "first_seen": row.get("Event First Seen", ""),
                    "last_seen": row.get("Event Last Seen", ""),
                }
            )
        return events_list

    def get_properties_by_event(self) -> Dict[str, List[Dict]]:
        """
        Properties grouped by their parent event name.

        Returns:
            Dict[str, List[Dict]] — event name -> list of property dicts.
        """
        if self._mode == "api":
            return self._api_properties_by_event()

        properties_df = self.data[
            (self.data["Event Property Name"].notna())
            & (self.data["Event Property Name"] != "")
            & (self.data["Object Name"].notna())
            & (self.data["Object Name"] != "")
        ]
        events_properties: Dict[str, List[Dict]] = defaultdict(list)
        for _, row in properties_df.iterrows():
            events_properties[row["Object Name"]].append(
                {
                    "name": row["Event Property Name"],
                    "description": row.get("Property Description", ""),
                    "type": row.get("Property Value Type", ""),
                    "required": row.get("Property Required", False),
                    "is_array": row.get("Property Is Array", False),
                    "schema_status": row.get("Property Schema Status", ""),
                    "first_seen": row.get("Property First Seen", ""),
                    "last_seen": row.get("Property Last Seen", ""),
                }
            )
        return dict(events_properties)

    def get_unique_properties_list(self) -> List[Dict]:
        """
        Deduplicated properties across all events, sorted by usage count desc.

        Returns:
            List[Dict] — each dict has name, description, type, is_array,
            schema_status, first_seen, last_seen, event_count.
        """
        if self._mode == "api":
            props_by_event = self._api_properties_by_event()
            unique: Dict[str, Dict] = {}
            for event_name, props in props_by_event.items():
                for p in props:
                    pname = p["name"]
                    if pname not in unique:
                        unique[pname] = {
                            "name": pname,
                            "description": p["description"],
                            "type": p["type"],
                            "is_array": p["is_array"],
                            "schema_status": p["schema_status"],
                            "first_seen": "",
                            "last_seen": "",
                            "event_count": 0,
                        }
                    if not unique[pname]["description"] and p["description"]:
                        unique[pname]["description"] = p["description"]
                    if not unique[pname]["type"] and p["type"]:
                        unique[pname]["type"] = p["type"]
                    unique[pname]["event_count"] += 1
            return sorted(
                unique.values(), key=lambda x: x["event_count"], reverse=True
            )

        properties_df = self.data[
            (self.data["Event Property Name"].notna())
            & (self.data["Event Property Name"] != "")
        ]
        unique_props: Dict[str, Dict] = {}
        for _, row in properties_df.iterrows():
            prop_name = row["Event Property Name"]
            if prop_name not in unique_props:
                unique_props[prop_name] = {
                    "name": prop_name,
                    "description": row.get("Property Description", ""),
                    "type": row.get("Property Value Type", ""),
                    "is_array": row.get("Property Is Array", False),
                    "schema_status": row.get("Property Schema Status", ""),
                    "first_seen": row.get("Property First Seen", ""),
                    "last_seen": row.get("Property Last Seen", ""),
                    "event_count": 0,
                }
            if not unique_props[prop_name]["description"] and row.get(
                "Property Description"
            ):
                unique_props[prop_name]["description"] = row.get(
                    "Property Description"
                )
            if not unique_props[prop_name]["type"] and row.get("Property Value Type"):
                unique_props[prop_name]["type"] = row.get("Property Value Type")

            if row.get("Object Name") and row.get("Object Name").strip():
                unique_props[prop_name]["event_count"] += 1

        return sorted(
            unique_props.values(), key=lambda x: x["event_count"], reverse=True
        )

    def get_platform_overview(self) -> Dict:
        """
        High-level overview metrics for the dashboard card.

        Returns:
            Dict with platform, total_events, total_properties,
            unique_properties, active_events, deleted_events,
            categories_count, last_updated.
        """
        events_summary = self.get_events_summary()
        properties_summary = self.get_properties_summary()
        return {
            "platform": "Amplitude",
            "total_events": events_summary["total_events"],
            "total_properties": properties_summary["total_properties"],
            "unique_properties": properties_summary["unique_properties"],
            "active_events": events_summary["activity_status"].get("ACTIVE", 0),
            "deleted_events": events_summary["activity_status"].get("DELETED", 0),
            "categories_count": len(events_summary["categories"]),
            "last_updated": "Live"
            if self._mode == "api"
            else "CSV snapshot",
        }
