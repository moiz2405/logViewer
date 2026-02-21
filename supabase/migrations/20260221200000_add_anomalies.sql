-- Migration: create anomalies table for detected log anomalies

CREATE TABLE IF NOT EXISTS public.anomalies (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  app_id        UUID        NOT NULL REFERENCES public.apps(id) ON DELETE CASCADE,
  detected_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  type          TEXT        NOT NULL,
  severity      TEXT        NOT NULL,
  title         TEXT        NOT NULL,
  summary       TEXT        NOT NULL,
  services_affected TEXT[]  NOT NULL DEFAULT '{}',
  evidence      JSONB       NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS anomalies_app_id_detected_at_idx
  ON public.anomalies (app_id, detected_at DESC);

ALTER TABLE public.anomalies ENABLE ROW LEVEL SECURITY;
