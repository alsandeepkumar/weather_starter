from dataclasses import dataclass
from typing import List, Dict

import httpx


class WeatherProviderError(Exception):
    pass


@dataclass
class SingaporeWeatherClient:
    base_url: str = "https://api-open.data.gov.sg"
    two_hour_path: str = "/v2/real-time/api/two-hr-forecast"
    timeout_seconds: float = 8.0
    user_agent: str = "weather-starter/0.1 (educational project)"
    api_key: str | None = None

    def fetch_latest_forecast_payload(self) -> dict:
        headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key

        with httpx.Client(timeout=self.timeout_seconds, headers=headers) as client:
            return self._fetch_json(client, f"{self.base_url}{self.two_hour_path}")

    def get_two_hour_forecast(self) -> List[Dict[str, str]]:
        """Fetch and return the two-hour area forecasts.

        Returns a list of dicts with keys: `area`, `forecast`, and `timestamp`.
        Raises `WeatherProviderError` on any failure to fetch or parse data.
        """
        try:
            payload = self.fetch_latest_forecast_payload()
        except WeatherProviderError:
            raise

        data = payload if isinstance(payload, dict) else {}
        items = data.get("items") or []
        if not items:
            raise WeatherProviderError("Forecast response contains no items")

        latest = items[0]
        forecasts = latest.get("forecasts") or []
        timestamp = latest.get("update_timestamp") or latest.get("timestamp") or ""
        valid_period_text = latest.get("valid_period", {}).get("text")

        result: List[Dict[str, str]] = []
        for entry in forecasts:
            area = entry.get("area")
            forecast = entry.get("forecast")
            if not area or forecast is None:
                continue
            result.append({
                "area": area,
                "forecast": forecast,
                "timestamp": timestamp,
                "valid_period_text": valid_period_text,
            })

        if not result:
            raise WeatherProviderError("No valid area forecasts found in response")

        return result

    def get_current_weather(self, latitude: float, longitude: float) -> dict:
        payload = self.fetch_latest_forecast_payload()
        return self.snapshot_from_payload(payload, latitude, longitude)

    def snapshot_from_payload(
        self, payload: dict, latitude: float, longitude: float
    ) -> dict:
        if isinstance(payload, dict) and payload.get("code") not in (None, 0):
            message = payload.get("errorMsg") or "Weather provider returned an error"
            raise WeatherProviderError(message)

        data = payload.get("data") if isinstance(payload, dict) else None
        root = data if isinstance(data, dict) else payload

        area_metadata = root.get("area_metadata", [])
        items = root.get("items", [])
        if not items:
            raise WeatherProviderError("Forecast response has no items")

        latest_item = items[0]
        forecasts = latest_item.get("forecasts", [])
        if not forecasts:
            raise WeatherProviderError("Forecast item has no area forecasts")

        forecast_by_area = {
            entry.get("area"): entry.get("forecast")
            for entry in forecasts
            if entry.get("area") and entry.get("forecast")
        }

        nearest_area = self._nearest_area_name(area_metadata, latitude, longitude)
        if nearest_area and nearest_area in forecast_by_area:
            area = nearest_area
            condition = forecast_by_area[nearest_area]
        else:
            fallback = forecasts[0]
            area = fallback.get("area")
            condition = fallback.get("forecast") or "Unknown"

        return {
            "condition": condition,
            "observed_at": latest_item.get("update_timestamp")
            or latest_item.get("timestamp")
            or "",
            "source": "api-open.data.gov.sg",
            "area": area,
            "valid_period_text": latest_item.get("valid_period", {}).get("text"),
        }

    @staticmethod
    def _fetch_json(client: httpx.Client, url: str) -> dict:
        try:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            if status_code == 429:
                raise WeatherProviderError(
                    "Weather provider rate limit reached (HTTP 429)"
                ) from exc
            if status_code in (401, 403):
                raise WeatherProviderError(
                    "Weather provider rejected request (check API key)"
                ) from exc
            raise WeatherProviderError(f"Weather provider returned HTTP {status_code}") from exc
        except httpx.HTTPError as exc:
            raise WeatherProviderError("Unable to reach weather provider") from exc

    @staticmethod
    def _nearest_area_name(
        area_metadata: list[dict], latitude: float, longitude: float
    ) -> str | None:
        nearest_name: str | None = None
        nearest_distance: float | None = None

        for area in area_metadata:
            label = area.get("label_location", {})
            lat = label.get("latitude")
            lon = label.get("longitude")
            name = area.get("name")
            if lat is None or lon is None or not name:
                continue

            delta = (float(lat) - latitude) ** 2 + (float(lon) - longitude) ** 2
            if nearest_distance is None or delta < nearest_distance:
                nearest_distance = delta
                nearest_name = name

        return nearest_name


def get_aqi_for_locations(locations: List[str]) -> Dict[str, int]:
    # Placeholder implementation: map each location to None.
    # Real implementation should call an AQI provider or database.
    result: Dict[str, int] = {}
    for loc in locations:
        result[loc] = None
    return result


def get_rain_forecast_for_locations(locations: List[str]) -> Dict[str, float]:
    # Placeholder: return None for each location. Real implementation should
    # parse forecast payloads to compute expected max rainfall rate (mm/hr).
    result: Dict[str, float] = {}
    for loc in locations:
        result[loc] = None
    return result
