# Sentry Logger SDK (Python)

Push logs from your FastAPI/Python app to the Sentry dashboard.

## Installation

```bash
pip install ./sdk/python
```

## One-command setup (CLI + browser OAuth)

```bash
sentry-logger init --app-name "my-service" --dsn "http://localhost:8001"
```

What happens:
- CLI requests a device session from backend
- Browser opens your sign-in page
- After login, app is registered in DB and API key is created
- CLI polls and stores credentials in `~/.sentry_logger/config.json`

Check current linked app:

```bash
sentry-logger status
```

## SDK Usage

```python
from sentry_logger import init

# Uses API key from ~/.sentry_logger/config.json
init()

# All logs from the root logger will be sent to your dashboard
import logging
logging.info("Hello from my app")
logging.error("Something went wrong")
```

## FastAPI Example

```python
import logging
import os
from fastapi import FastAPI
from sentry_logger import init

app = FastAPI()

@app.on_event("startup")
def setup_logging() -> None:
    init()
    logging.getLogger(__name__).info("Sentry SDK initialized")
```

## Configuration

- `api_key` (optional): If omitted, loaded from local CLI config
- `dsn` (optional): Ingest URL base. Defaults to `SENTRY_INGEST_URL` env or `http://localhost:8001`
- `batch_size` (optional): Send logs when buffer reaches this size (default: 50)
- `flush_interval_seconds` (optional): Flush buffer after this many seconds (default: 5.0)
