# Working Notes

## Date
- 2026-02-18

## Goal
- Make SDK onboarding one command with browser OAuth login.
- Auto-register app in DB, issue API key, and ingest logs under app ownership.
- Default alert email recipients to registered app owner/team source in DB.

## Implemented
- Backend device flow endpoints:
  - `POST /sdk/device/start`
  - `GET /sdk/device/poll`
  - `POST /sdk/device/complete`
- Backend schema validation endpoint:
  - `GET /sdk/schema/validate`
- Backend startup schema gate:
  - env `SDK_SCHEMA_STRICT_STARTUP=true` fails startup if schema invalid.
- SDK CLI:
  - `sentry-logger init`
  - `sentry-logger login` (alias)
  - `sentry-logger status`
- SDK local credential persistence:
  - `~/.sentry_logger/config.json`
- SDK runtime init fallback:
  - `init()` now loads local config if `api_key` not explicitly passed.
- Frontend link completion page:
  - `/sdk/link` completes device session after OAuth login.
- Alert recipient default logic:
  - if `EMAIL_ALERT_TO` unset, backend resolves app owner email from `users.email`, fallback `profiles.email`.

## Files Added/Changed
- `sentry/backend/app/main.py`
- `sentry/backend/app/core/api_key.py`
- `supabase/migrations/20260218000000_add_sdk_device_sessions.sql`
- `sdk/python/sentry_logger/cli.py`
- `sdk/python/sentry_logger/local_config.py`
- `sdk/python/sentry_logger/__init__.py`
- `sdk/python/pyproject.toml`
- `sdk/python/README.md`
- `frontend/app/sdk/link/page.tsx`
- `SETUP-SDK.md`

## Required Migrations
- `supabase/migrations/20250218000000_add_api_key_to_apps.sql`
- `supabase/migrations/20260218000000_add_sdk_device_sessions.sql`

## Required Env (backend)
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SDK_VERIFICATION_BASE_URL` (example: `http://localhost:3000`)
- `SDK_DEFAULT_DSN` (example: `http://localhost:8001`)
- `SDK_SCHEMA_STRICT_STARTUP` (`true` in prod)
- SMTP/email vars for alerts:
  - `EMAIL_ALERT_FROM`
  - `SMTP_HOST`
  - `SMTP_PORT`
  - `SMTP_USERNAME`
  - `SMTP_PASSWORD`
  - `SMTP_USE_TLS`

## Current Flow
1. `pip install -e ./sdk/python`
2. `sentry-logger init --app-name "myApp" --dsn "http://localhost:8001"`
3. CLI opens browser login URL.
4. User signs in on frontend.
5. Frontend `/sdk/link` calls backend `/sdk/device/complete`.
6. Backend creates app + `api_key` and approves device session.
7. CLI polls `/sdk/device/poll`, receives credentials, saves local config.
8. App code uses:
   - `from sentry_logger import init`
   - `init()`
9. SDK sends logs to `/ingest` with API key; backend resolves app ownership.

## Validation
- Startup: schema validation runs automatically.
- Manual: `GET /sdk/schema/validate` should return `ok: true`.

## Next Steps
1. Run migrations in Supabase.
2. Set env vars and start backend/frontend.
3. Test full onboarding and ingest end-to-end.
4. (Optional) Add team-member recipient table for multi-user alerts.
