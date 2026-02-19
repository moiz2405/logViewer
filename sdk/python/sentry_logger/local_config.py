"""Local CLI config persistence for SDK credentials."""
import json
import os
from pathlib import Path
from typing import Any


def get_default_config_path() -> Path:
    home = Path.home()
    return home / ".sentry_logger" / "config.json"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_local_config(path: str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path else get_default_config_path()
    if not config_path.exists():
        return {}
    try:
        with config_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def save_local_config(payload: dict[str, Any], path: str | None = None) -> Path:
    config_path = Path(path) if path else get_default_config_path()
    ensure_parent(config_path)
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return config_path


def resolve_dsn(explicit_dsn: str | None = None) -> str:
    if explicit_dsn:
        return explicit_dsn.rstrip("/")
    env_dsn = os.environ.get("SENTRY_INGEST_URL")
    if env_dsn:
        return env_dsn.rstrip("/")
    cfg = load_local_config()
    if cfg.get("dsn"):
        return str(cfg["dsn"]).rstrip("/")
    return "http://localhost:8001"
