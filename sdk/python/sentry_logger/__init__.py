"""
Sentry Logger SDK - Push logs from your FastAPI/Python app to the Sentry dashboard.
"""
from .handler import SentryLogHandler
from .config import SentryLoggerConfig
from .local_config import load_local_config

__all__ = ["SentryLogHandler", "SentryLoggerConfig", "init"]


def init(
    api_key: str,
    batch_size: int = 50,
    flush_interval_seconds: float = 5.0,
) -> SentryLogHandler:
    """
    Initialize Sentry Logger and add handler to root logger.
    
    Args:
        api_key: Your LogSentry API key from the dashboard
        batch_size: Number of logs to batch before sending (default: 50)
        flush_interval_seconds: Seconds between automatic flushes (default: 5.0)
    
    Returns:
        SentryLogHandler instance for advanced usage
    
    Example:
        >>> import sentry_logger as sentry
        >>> sentry.init(api_key="sk_...")
        >>> 
        >>> import logging
        >>> logging.info("Hello from my app!")
    
    Note:
        The LogSentry backend URL is configured via the LOGSENTRY_URL 
        environment variable. Default: https://api.logsentry.io
    """
    import logging

    if not api_key:
        raise ValueError("api_key is required. Get it from your LogSentry dashboard.")

    config = SentryLoggerConfig(
        api_key=api_key,
        batch_size=batch_size,
        flush_interval_seconds=flush_interval_seconds,
    )
    handler = SentryLogHandler(config)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    return handler
