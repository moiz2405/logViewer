-- Device-code flow sessions for SDK CLI onboarding.
-- Used by backend endpoints:
--   POST /sdk/device/start
--   GET  /sdk/device/poll
--   POST /sdk/device/complete

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

CREATE INDEX IF NOT EXISTS idx_sdk_device_sessions_device_code
  ON sdk_device_sessions(device_code);

CREATE INDEX IF NOT EXISTS idx_sdk_device_sessions_status_expires
  ON sdk_device_sessions(status, expires_at);
