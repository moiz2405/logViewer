"""
Logging handler that buffers log records and sends them in batches to the Sentry ingest API.
"""
import atexit
import json
import logging
import threading
import time
import urllib.request

from .config import SentryLoggerConfig


class SentryLogHandler(logging.Handler):
    """
    Buffers log records and POSTs them in batches to the Sentry ingest endpoint.
    Uses a background thread for non-blocking sends.
    """

    def __init__(self, config: SentryLoggerConfig):
        super().__init__()
        self.config = config
        self._buffer: list[str] = []
        self._lock = threading.Lock()
        self._shutdown = False
        self._last_flush = time.monotonic()
        self.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s")
        )
        atexit.register(self.flush)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            with self._lock:
                self._buffer.append(msg)
                now = time.monotonic()
                if (
                    len(self._buffer) >= self.config.batch_size
                    or (now - self._last_flush) >= self.config.flush_interval_seconds
                ):
                    self._flush_locked()
        except Exception:
            self.handleError(record)

    def _flush_locked(self) -> None:
        if not self._buffer:
            return
        logs = self._buffer[:]
        self._buffer = []
        self._last_flush = time.monotonic()
        threading.Thread(target=self._send, args=(logs,), daemon=True).start()

    def _send(self, logs: list[str]) -> None:
        try:
            body = json.dumps({"logs": logs}).encode("utf-8")
            req = urllib.request.Request(
                self.config.ingest_url,
                data=body,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config.api_key}",
                    "X-API-Key": self.config.api_key,
                },
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass  # Fail silently to avoid disrupting the app

    def flush(self) -> None:
        with self._lock:
            self._flush_locked()
