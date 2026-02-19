# SDK Setup Guide

## 1. Run Database Migration

In Supabase SQL Editor, run the migration:

```sql
-- From supabase/migrations/20250218000000_add_api_key_to_apps.sql
ALTER TABLE apps ADD COLUMN IF NOT EXISTS api_key TEXT UNIQUE;
CREATE INDEX IF NOT EXISTS idx_apps_api_key ON apps(api_key) WHERE api_key IS NOT NULL;
ALTER TABLE apps ALTER COLUMN url DROP NOT NULL;

-- From supabase/migrations/20260218000000_add_sdk_device_sessions.sql
CREATE TABLE IF NOT EXISTS sdk_device_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_code TEXT NOT NULL UNIQUE,
  user_code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  app_name TEXT NOT NULL,
  description TEXT,
  user_id UUID,
  app_id UUID,
  api_key TEXT,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  approved_at TIMESTAMPTZ
);
```

## 2. Configure Sentry Backend

Copy `sentry/.env.example` to `sentry/.env.local` and set:

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key (for API key validation)
- `SDK_VERIFICATION_BASE_URL` - Frontend base URL (e.g. `http://localhost:3000`)
- `SDK_DEFAULT_DSN` - Ingest/backend URL returned to CLI (e.g. `http://localhost:8001`)
- `SDK_SCHEMA_STRICT_STARTUP` - Set `true` in prod to fail fast on schema mismatch
- `EMAIL_ALERT_FROM`, `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD` - for email alerts

## 3. Install SDK in Your App

```bash
pip install -e ./sdk/python
# Or from sdk/python: pip install .
```

## 4. Use the SDK

```python
from sentry_logger import init

init()  # reads credentials from local CLI config
# Logs will be sent to your dashboard automatically
```

## 5. One-command app linking (CLI + OAuth)

```bash
sentry-logger init --app-name "myApp" --dsn "http://localhost:8001"
```

This opens browser login (`/auth/sign-in`), links your user, creates an app row in `apps`, then stores `api_key` locally.

## 6. Run myApp Demo

```bash
cd myApp
pip install -e ../sdk/python
export SENTRY_INGEST_URL=http://localhost:8001
python main.py
```

## 7. Validate DB schema mapping

```bash
curl http://localhost:8001/sdk/schema/validate
```

Check:
- `ok: true`
- `email_source` is either `users.email` or `profiles.email`
- if not, follow `guidance` from the response

## Services

- **Sentry backend** (port 8001): Receives logs via `/ingest`, SDK auth at `/sdk/device/*`, serves summaries at `/summary/{app_id}`
- **Frontend** (port 3000): Dashboard, app registration, polling for summaries
- **myApp** (port 8000): Demo backend with SDK - sends logs to Sentry
