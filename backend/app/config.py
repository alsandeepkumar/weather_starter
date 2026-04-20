from dataclasses import dataclass
import os


@dataclass
class Settings:
    AQI_THRESHOLD: int = int(os.getenv("AQI_THRESHOLD", "151"))
    RAIN_RATE_THRESHOLD: float = float(os.getenv("RAIN_RATE_THRESHOLD", "10"))
    ALERT_MIN_AREAS: int = int(os.getenv("ALERT_MIN_AREAS", "2"))
    ALERT_CHECK_INTERVAL_MIN: int = int(os.getenv("ALERT_CHECK_INTERVAL_MIN", "15"))
    MONITORED_AREAS: str = os.getenv("MONITORED_AREAS", "Central,North,East,West,South")


settings = Settings()
