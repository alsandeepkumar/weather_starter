from fastapi import APIRouter
from typing import List

from ..services import alerts
from app.config import settings

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/")
def get_alerts() -> dict:
    monitored: List[str] = [s.strip() for s in settings.MONITORED_AREAS.split(",") if s.strip()]
    # If an event is not active, return cached state marked inactive
    if not alerts.is_event_active():
        state = alerts.get_cached_state()
        state["note"] = "No active events"
        return state

    state = alerts.evaluate_all(monitored)
    return state
