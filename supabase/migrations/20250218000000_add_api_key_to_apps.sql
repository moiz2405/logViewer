-- Add api_key column to apps table for SDK-based log ingestion
-- Format: sk_<32 random chars>, unique per app
-- Run this in Supabase SQL editor if migrations are not used.

ALTER TABLE apps ADD COLUMN IF NOT EXISTS api_key TEXT UNIQUE;

CREATE INDEX IF NOT EXISTS idx_apps_api_key ON apps(api_key) WHERE api_key IS NOT NULL;

-- Make url optional (no longer required for ingestion)
ALTER TABLE apps ALTER COLUMN url DROP NOT NULL;
