from datetime import datetime, timezone
from typing import Dict, List

from .weather_api import get_aqi_for_locations, get_rain_forecast_for_locations
from app.config import settings


# In-memory cache for last computed alert state
_last_state: Dict = {"active": False, "count": 0, "areas": [], "checked_at": None}


def evaluate_area_alert(area: str, aqi_value: int, rain_rate: float) -> Dict:
    reasons = []
    if aqi_value is not None and aqi_value >= settings.AQI_THRESHOLD:
        reasons.append("aqi")
    if rain_rate is not None and rain_rate > settings.RAIN_RATE_THRESHOLD:
        reasons.append("heavy_rain")
    return {"area": area, "aqi": aqi_value, "rain_rate": rain_rate, "reasons": reasons}


def aggregate_alerts(area_results: List[Dict], min_areas: int = None) -> Dict:
    if min_areas is None:
        min_areas = settings.ALERT_MIN_AREAS
    affected = [r for r in area_results if r["reasons"]]
    active = len(affected) >= min_areas
    return {"active": active, "count": len(affected), "areas": affected, "checked_at": datetime.now(timezone.utc).isoformat()}


def evaluate_all(monitored_areas: List[str]) -> Dict:
    aqi_map = get_aqi_for_locations(monitored_areas)
    rain_map = get_rain_forecast_for_locations(monitored_areas)

    results = []
    for area in monitored_areas:
        aqi = aqi_map.get(area)
        rain = rain_map.get(area)
        results.append(evaluate_area_alert(area, aqi, rain))

    state = aggregate_alerts(results)
    global _last_state
    _last_state = state
    return state


def get_cached_state() -> Dict:
    return _last_state


def is_event_active() -> bool:
    """Placeholder for event-activity check.

    Replace this with a real integration that consults the events DB or
    external scheduling system. For now it returns True so alerts are
    evaluated during development.
    """
    return True


def is_event_active() -> bool:
    """Placeholder for event-activity check.

    Replace this with a real integration that consults the events DB or
    external scheduling system. For now it returns True so alerts are
    evaluated during development.
    """
    return True
