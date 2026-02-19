"""
Sentry Logger SDK - Push logs from your FastAPI/Python app to the Sentry dashboard.
"""
from .handler import SentryLogHandler
from .config import SentryLoggerConfig
from .local_config import load_local_config

__all__ = ["SentryLogHandler", "SentryLoggerConfig", "init"]


def init(
    api_key: str | None = None,
    dsn: str | None = None,
    batch_size: int = 50,
    flush_interval_seconds: float = 5.0,
) -> SentryLogHandler:
    """
    Initialize Sentry Logger and add handler to root logger.
    Returns the handler instance for advanced usage.
    """
    import logging

    resolved_api_key = api_key
    if not resolved_api_key:
        cfg = load_local_config()
        resolved_api_key = cfg.get("api_key")
        if not dsn and cfg.get("dsn"):
            dsn = str(cfg["dsn"])

    if not resolved_api_key:
        raise ValueError("api_key is required. Run `sentry-logger init` or pass api_key explicitly.")

    config = SentryLoggerConfig(
        api_key=resolved_api_key,
        dsn=dsn,
        batch_size=batch_size,
        flush_interval_seconds=flush_interval_seconds,
    )
    handler = SentryLogHandler(config)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    return handler
