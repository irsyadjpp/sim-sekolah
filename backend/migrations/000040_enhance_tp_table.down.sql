-- Down migration: Remove TP table enhancements
ALTER TABLE cur_tp DROP COLUMN IF EXISTS local_context_integration;