# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app (dev mode)
python app.py
# or
flask --app app run --debug

# Run tests
pytest -q

# Run a single test
pytest tests/test_basic.py::test_homepage -v

# Run the UI auditor standalone
python tools/ui_auditor.py

# Run the property extractor (exports to CSV)
python process_events_properties.py
```

The app runs at `http://localhost:5000`.

## Architecture

This is a **read-only Flask dashboard** for analyzing tracking plan data from three platforms: Amplitude, Insider, and Google Tag Manager (GTM). All data is loaded from local source files — no live API calls.

### Data Flow

```
sources/              →  parsers/              →  services/            →  routes/
amplitude/*.csv           amplitude_parser.py      parser_manager.py      web.py (HTML pages)
insider/*.json            insider_parser.py        (singleton, lazy)      api.py  (/api/* JSON)
gtm/*.json                gtm_parser.py
```

`ParserManager` (`services/parser_manager.py`) is a **singleton** that initializes all four parsers at startup (amplitude, insider, gtm_server, gtm_client). If a source file is missing, that parser is set to `None` and the app continues without it — partial data loading is by design.

### Parser Contract

All three parser classes must implement these methods so routes and templates can call them uniformly:

- `get_platform_overview()` — summary dict for the dashboard overview cards
- `get_events_summary()` — aggregated event statistics
- `get_events_list()` — full list of events (used by both web routes and API endpoints)
- `get_properties_summary()` / `get_parameters_summary()` — property/parameter stats

GTMParser additionally implements: `get_container_info()`, `get_tags_summary()`, `get_variables_summary()`, `get_triggers_summary()`, `get_tags_list()`, `get_destination_analysis()`, `get_data_flow_analysis()`.

### Source File Paths

Configured in `config.py` using `pathlib.Path`:

| Key | Path |
|-----|------|
| `AMPLITUDE_CSV` | `sources/amplitude/amplitude_events.csv` |
| `INSIDER_JSON` | `sources/insider/insider.json` |
| `GTM_SERVER_JSON` | `sources/gtm/GTM-P32K5GT_workspace486.json` |
| `GTM_CLIENT_JSON` | `sources/gtm/GTM-NRGXLJ_workspace1002783.json` |

### Routes

**Web (HTML):** `routes/web.py`
- `/` — dashboard overview (all platforms)
- `/amplitude` — Amplitude detail
- `/insider` — Insider detail
- `/gtm` — GTM both containers overview
- `/gtm/<server|client>` — GTM container detail
- `/audit` — UI/UX audit report viewer

**API (JSON):** `routes/api.py` — prefixed `/api/`
- `/api/amplitude/events`
- `/api/insider/events`
- `/api/gtm/<container_type>/tags`
- `/api/audit/run` (POST) — runs `UIAuditor`, writes `audit_report.json`
- `/api/audit/report` (GET) — reads last `audit_report.json`
- `/api/audit/fix/token` (POST) — replaces a hardcoded hex color with a CSS var
- `/api/audit/fix/inline-style` (POST) — moves an inline style to `dashboard.css`
- `/api/audit/fix/all-tokens` (POST) — bulk fix all design token issues

### Tools

`tools/ui_auditor.py` — scans templates and CSS for hardcoded colors, inline styles, and accessibility issues. Outputs `audit_report.json` and a markdown summary. Uses constants from `tools/constants.py` (CSS_VARS map, regex patterns, project paths).

`tools/ui_fixer_agent.py` — automated fixer that calls the audit API endpoints.

`process_events_properties.py` — standalone script that uses `parser_manager` to extract and combine Amplitude + Insider properties, exporting to CSV for use in spreadsheets.

### Templates

All templates extend `templates/base.html`. Template logic is kept minimal — data processing happens in parsers before being passed to `render_template()`.

## Key Conventions

- Use `pathlib.Path` for all file path operations.
- Route handlers delegate all data logic to parser methods; keep handlers thin.
- API endpoints return `{'error': '...'}` with appropriate HTTP status on failure.
- Parsers are initialized once (singleton); never re-instantiate `ParserManager`.
- Amplitude data uses pandas DataFrames internally; Insider and GTM use raw JSON dicts.
- CSS design tokens (variables) are defined in `static/css/dashboard.css` and mapped in `tools/constants.py` (`CSS_VARS`).
