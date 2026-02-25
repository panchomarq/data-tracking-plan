"""
HTTP client for the Amplitude Taxonomy API.
Wraps event types, event properties, and category endpoints with
Basic Auth, retry logic, and response validation.
"""

import time
import logging
from base64 import b64encode
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class AmplitudeAPIError(Exception):
    """Raised when the Amplitude API returns an error response."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Amplitude API {status_code}: {message}")


class AmplitudeAPIClient:
    """
    Low-level client for Amplitude's Taxonomy API.

    Args:
        api_key:   Amplitude project API key.
        secret_key: Amplitude project secret key.
        base_url:  API root (e.g. https://amplitude.com/api/2).
        timeout:   Request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        base_url: str = "https://amplitude.com/api/2",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        token = b64encode(f"{api_key}:{secret_key}".encode()).decode()
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        self._session = requests.Session()
        self._session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    def _get(self, path: str, params: Optional[Dict[str, str]] = None) -> Any:
        """Execute a GET request and return the parsed JSON data."""
        url = f"{self.base_url}{path}"
        response = self._session.get(
            url, headers=self._headers, params=params, timeout=self.timeout
        )

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "5"))
            logger.warning("Rate-limited by Amplitude, waiting %ds", retry_after)
            time.sleep(retry_after)
            response = self._session.get(
                url, headers=self._headers, params=params, timeout=self.timeout
            )

        if not response.ok:
            raise AmplitudeAPIError(response.status_code, response.text)

        body = response.json()
        if not body.get("success"):
            errors = body.get("errors", [{"message": "Unknown error"}])
            raise AmplitudeAPIError(response.status_code, errors[0].get("message", ""))

        return body.get("data", [])

    # ------------------------------------------------------------------
    # Public endpoints
    # ------------------------------------------------------------------

    def get_events(self, show_deleted: bool = True) -> List[Dict]:
        """
        Fetch all event types from the Taxonomy API.

        Returns a list of event dicts with keys:
        event_type, category, description, is_active, owner, tags, ...
        """
        params = {}
        if show_deleted:
            params["showDeleted"] = "true"
        return self._get("/taxonomy/event", params=params)

    def get_event_properties(self, event_type: str) -> List[Dict]:
        """
        Fetch properties for a specific event type.

        Returns a list of property dicts with keys:
        event_property, event_type, description, type, is_required,
        is_array_type, is_hidden, regex, enum_values, classifications.
        """
        return self._get(
            "/taxonomy/event-property",
            params={"event_type": event_type},
        )

    def get_categories(self) -> List[Dict]:
        """
        Fetch all event categories.

        Returns a list of dicts with keys: id, name.
        """
        return self._get("/taxonomy/category")

    def health_check(self) -> bool:
        """Verify credentials work by fetching categories."""
        try:
            self.get_categories()
            return True
        except Exception as exc:
            logger.warning("Amplitude health check failed: %s", exc)
            return False
