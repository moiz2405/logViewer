"""Configuration for Sentry Logger SDK."""
import os
from dataclasses import dataclass


@dataclass
class SentryLoggerConfig:
    api_key: str
    dsn: str | None = None
    batch_size: int = 50
    flush_interval_seconds: float = 5.0

    def __post_init__(self):
        if not self.dsn:
            self.dsn = os.environ.get("SENTRY_INGEST_URL", "http://localhost:8001")
        self.dsn = self.dsn.rstrip("/")
        self.ingest_url = f"{self.dsn}/ingest"
