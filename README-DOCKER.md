# Docker & Compose Setup

This project uses two containers:
- `sentry` (port 8001)
- `myApp` (port 8000)

## Build & Run

```bash
docker compose up --build
```

## Stopping
```bash
docker compose down
```

## Notes
- Make sure your EC2 instance has Docker & Docker Compose installed.
- Both containers use Python 3.11 and run their respective scripts.
- You can access the services on ports 8000 and 8001.
