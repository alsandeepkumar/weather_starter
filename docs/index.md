# Weather Starter

A small Singapore weather dashboard. Add a location by latitude/longitude, then refresh on demand to pull the latest two-hour forecast from [data.gov.sg](https://data.gov.sg) and store the snapshot locally.

## What it does

- Track a list of Singapore locations (`UNIQUE(latitude, longitude)`).
- Fetch the 2-hour forecast from the official `data.gov.sg` real-time API on demand.
- Store the latest weather snapshot per location in SQLite (no history — each refresh overwrites the previous snapshot).
- Serve a React UI that lists locations and lets the user trigger a refresh per card.

## Tech stack

| Layer    | Stack                                                              |
| -------- | ------------------------------------------------------------------ |
| Backend  | Python ≥3.11, FastAPI, Uvicorn, httpx, structlog, SQLite (stdlib)  |
| Frontend | React 18, Vite 7, Tailwind CSS 3                                   |
| Tooling  | `uv` (Python), `npm` (Node), `pytest`, `ruff`, `pyright`, ESLint   |

## Quick start

### Backend (port 8000)

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

The API is then reachable at `http://localhost:8000`. Health check: `GET /health`.

### Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api/*` to the backend automatically — no CORS configuration needed.

## Environment variables

| Variable             | Default                  | Used by  | Purpose                                       |
| -------------------- | ------------------------ | -------- | --------------------------------------------- |
| `DATABASE_PATH`      | `weather.db`             | backend  | SQLite file location                          |
| `WEATHER_API_KEY`    | _(unset)_                | backend  | Optional `x-api-key` header for data.gov.sg   |
| `VITE_BACKEND_PORT`  | `8000`                   | frontend | Backend port the Vite proxy forwards to       |
| `VITE_API_TARGET`    | `http://localhost:8000`  | frontend | Full proxy target (overrides `VITE_BACKEND_PORT`) |

## Building these docs

The `mkdocs-material` and `mkdocs-mermaid2-plugin` packages are declared as dev dependencies of the backend project, so `uv` manages them.

```bash
# Serve locally with live reload
uv --project backend run mkdocs serve

# Build the static site into ./site
uv --project backend run mkdocs build --strict
```

Run from the repository root (where `mkdocs.yml` lives).

## Where to go next

- [API Reference](api-reference.md) — all HTTP endpoints with request/response examples.
- [Architecture](architecture.md) — the snapshot pattern, the Vite proxy, the data.gov.sg integration, and sequence diagrams.
