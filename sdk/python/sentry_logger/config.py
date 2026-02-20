"""Configuration for Sentry Logger SDK."""
import os
from dataclasses import dataclass


@dataclass
class SentryLoggerConfig:
    api_key: str
    batch_size: int = 50
    flush_interval_seconds: float = 5.0
    
    # Internal - URL is set via environment variable
    _backend_url: str | None = None

    def __post_init__(self):
        # Get backend URL from environment, default to production
        if not self._backend_url:
            self._backend_url = os.environ.get(
                "LOGSENTRY_URL", 
                "https://api.logsentry.io"
            )
        self._backend_url = self._backend_url.rstrip("/")
        self.ingest_url = f"{self._backend_url}/ingest"
