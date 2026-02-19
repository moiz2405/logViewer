"""CLI for one-command SDK onboarding."""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

from .local_config import get_default_config_path, load_local_config, save_local_config


def _http_json(method: str, url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        method=method,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read().decode("utf-8")
        return json.loads(body) if body else {}


def cmd_init(args: argparse.Namespace) -> int:
    dsn = args.dsn.rstrip("/")
    try:
        start = _http_json(
            "POST",
            f"{dsn}/sdk/device/start",
            {
                "app_name": args.app_name,
                "description": args.description,
                "ttl_seconds": args.ttl_seconds,
            },
        )
    except urllib.error.HTTPError as exc:
        print(f"Failed to start login flow: HTTP {exc.code}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Failed to start login flow: {type(exc).__name__}", file=sys.stderr)
        return 1

    verification_uri_complete = start["verification_uri_complete"]
    user_code = start["user_code"]
    device_code = start["device_code"]
    interval = int(start.get("interval", 3))

    print("Open this URL to login and link your app:")
    print(verification_uri_complete)
    print(f"If prompted, enter code: {user_code}")

    if not args.no_browser:
        webbrowser.open(verification_uri_complete)

    started = time.monotonic()
    while True:
        if (time.monotonic() - started) > args.timeout_seconds:
            print("Timed out waiting for approval.", file=sys.stderr)
            return 2

        try:
            poll_url = f"{dsn}/sdk/device/poll?{urllib.parse.urlencode({'device_code': device_code})}"
            poll = _http_json("GET", poll_url)
        except urllib.error.HTTPError as exc:
            if exc.code == 400:
                print("Device code expired. Run init again.", file=sys.stderr)
                return 2
            time.sleep(interval)
            continue
        except Exception:
            time.sleep(interval)
            continue

        if poll.get("status") == "approved":
            payload = {
                "app_id": poll["app_id"],
                "app_name": poll.get("app_name", args.app_name),
                "api_key": poll["api_key"],
                "dsn": poll.get("dsn", dsn),
            }
            saved = save_local_config(payload, path=args.config_path)
            print("")
            print(f"Linked app '{payload['app_name']}' ({payload['app_id']}).")
            print(f"Credentials saved to {saved}.")
            print("Use in code:")
            print("  from sentry_logger import init")
            print("  init()  # reads local config")
            return 0

        time.sleep(interval)


def cmd_status(args: argparse.Namespace) -> int:
    cfg = load_local_config(path=args.config_path)
    if not cfg:
        print(f"No config found at {args.config_path or get_default_config_path()}")
        return 1
    print(f"App: {cfg.get('app_name')}")
    print(f"App ID: {cfg.get('app_id')}")
    print(f"DSN: {cfg.get('dsn')}")
    print(f"API key present: {'yes' if cfg.get('api_key') else 'no'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentry-logger", description="Sentry Logger SDK CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Login in browser and provision app credentials")
    init_parser.add_argument("--app-name", required=True, help="Name for the app to register")
    init_parser.add_argument("--description", default="", help="Optional app description")
    init_parser.add_argument("--dsn", default="http://localhost:8001", help="Backend base URL")
    init_parser.add_argument("--ttl-seconds", type=int, default=600, help="Login session TTL")
    init_parser.add_argument("--timeout-seconds", type=int, default=300, help="Polling timeout")
    init_parser.add_argument("--no-browser", action="store_true", help="Do not auto-open browser")
    init_parser.add_argument("--config-path", default=None, help="Override config file path")
    init_parser.set_defaults(func=cmd_init)

    login_parser = sub.add_parser("login", help="Alias for init")
    login_parser.add_argument("--app-name", required=True, help="Name for the app to register")
    login_parser.add_argument("--description", default="", help="Optional app description")
    login_parser.add_argument("--dsn", default="http://localhost:8001", help="Backend base URL")
    login_parser.add_argument("--ttl-seconds", type=int, default=600, help="Login session TTL")
    login_parser.add_argument("--timeout-seconds", type=int, default=300, help="Polling timeout")
    login_parser.add_argument("--no-browser", action="store_true", help="Do not auto-open browser")
    login_parser.add_argument("--config-path", default=None, help="Override config file path")
    login_parser.set_defaults(func=cmd_init)

    status_parser = sub.add_parser("status", help="Show current local SDK config")
    status_parser.add_argument("--config-path", default=None, help="Override config file path")
    status_parser.set_defaults(func=cmd_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
