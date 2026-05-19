DROP INDEX IF EXISTS idx_audit_logs_impersonator;
ALTER TABLE audit_logs DROP COLUMN IF EXISTS impersonator_id;
