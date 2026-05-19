ALTER TABLE audit_logs ADD COLUMN impersonator_id UUID REFERENCES auth_user(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_audit_logs_impersonator ON audit_logs(impersonator_id);
