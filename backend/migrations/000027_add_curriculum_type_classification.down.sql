-- Down migration: Remove curriculum type classification
DROP TABLE IF EXISTS trx_ekstrakurikuler_activity CASCADE;
DROP TABLE IF EXISTS trx_kokurikuler_activity CASCADE;
ALTER TABLE trx_curriculum_document DROP COLUMN IF EXISTS curriculum_type;