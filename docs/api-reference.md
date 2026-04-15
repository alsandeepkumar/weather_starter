# API Reference

Base URL (dev): `http://localhost:8000`. The frontend reaches the same endpoints via the Vite proxy at `http://localhost:5173/api/...`.

## Location object

Returned by every `/api/locations*` endpoint that yields a row. Built by `row_to_dict` in `backend/app/routers/locations.py`.

```json
{
  "id": 1,
  "latitude": 1.3508,
  "longitude": 103.839,
  "created_at": "2026-04-15T03:22:00",
  "weather": {
    "condition": "Partly Cloudy",
    "observed_at": "2026-04-15T11:00:00+08:00",
    "source": "api-open.data.gov.sg",
    "area": "Clementi",
    "valid_period_text": "2026-04-15 11:00 to 13:00"
  }
}
```

A freshly created location has `weather.condition = "Not refreshed"` and `weather.source = "not-refreshed"`; the other `weather.*` fields are `null` until the first refresh.

---

## `GET /health`

Liveness check. Also returns a quick row count from SQLite.

**200 OK**

```json
{ "status": "healthy", "location_count": 3 }
```

```bash
curl http://localhost:8000/health
```

---

## `GET /api/locations`

List all locations, ordered by `created_at DESC, id DESC`. Pure SQLite read — no external API call.

**200 OK**

```json
{
  "locations": [
    {
      "id": 2,
      "latitude": 1.29,
      "longitude": 103.85,
      "created_at": "2026-04-15T03:30:00",
      "weather": {
        "condition": "Not refreshed",
        "observed_at": null,
        "source": "not-refreshed",
        "area": null,
        "valid_period_text": null
      }
    }
  ]
}
```

```bash
curl http://localhost:8000/api/locations
```

---

## `POST /api/locations`

Create a new location. Coordinates must lie inside Singapore: latitude in `[1.1, 1.5]`, longitude in `[103.6, 104.1]`. Pairs are unique — duplicates return 409.

**Request body**

```json
{ "latitude": 1.3508, "longitude": 103.839 }
```

**201 Created** — returns the created [location object](#location-object). The new row has `weather.condition = "Not refreshed"` until you call refresh.

**Errors**

| Status | Detail                                                                   |
| ------ | ------------------------------------------------------------------------ |
| 422    | `latitude and longitude are required`                                    |
| 422    | `Coordinates must be within Singapore (lat 1.1–1.5, lon 103.6–104.1)`    |
| 409    | `Location already exists`                                                |

```bash
curl -X POST http://localhost:8000/api/locations \
  -H 'content-type: application/json' \
  -d '{"latitude": 1.3508, "longitude": 103.839}'
```

---

## `GET /api/locations/{id}`

Fetch a single location by id.

**200 OK** — returns the [location object](#location-object).

**404 Not Found** — `Location not found`.

```bash
curl http://localhost:8000/api/locations/1
```

---

## `POST /api/locations/{id}/refresh`

Fetch the latest 2-hour forecast from `api-open.data.gov.sg` for this location's coordinates, write the snapshot to SQLite, and return the updated row. Empty request body.

**200 OK** — returns the updated [location object](#location-object) with all `weather.*` fields populated.

**Errors**

| Status | Detail                                                              |
| ------ | ------------------------------------------------------------------- |
| 404    | `Location not found`                                                |
| 502    | `Unable to reach provider`, `rate limit reached`, etc. (see below)  |

The 502 detail comes from `WeatherProviderError` raised by `SingaporeWeatherClient` (`backend/app/services/weather_api.py`). Possible messages include rate-limit, auth (when `WEATHER_API_KEY` is wrong), upstream-error, and connectivity failures.

```bash
curl -X POST http://localhost:8000/api/locations/1/refresh
```

---

## `DELETE /api/locations/locations/{id}`

Delete a location.

!!! warning "Known issues"
    - The route declaration in `backend/app/routers/locations.py` uses path `"/locations/{location_id}"`, but the router itself already mounts at `prefix="/locations"`. The effective URL is therefore `/api/locations/locations/{id}` — almost certainly a bug.
    - The handler concatenates `location_id` directly into a SQL string (`"DELETE FROM locations WHERE id = " + str(location_id)`). FastAPI coerces the path param to `int` before it reaches the handler, so the immediate injection vector is closed, but the code pattern is still unsafe and should be replaced with a parameterised query.

**200 OK**

```json
{ "ok": true }
```

```bash
curl -X DELETE http://localhost:8000/api/locations/locations/1
```
