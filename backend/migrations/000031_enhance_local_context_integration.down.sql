-- Down migration: Remove local context integration enhancements
DROP TABLE IF EXISTS trx_local_context_utilization CASCADE;
ALTER TABLE trx_teaching_module DROP COLUMN IF EXISTS local_context_ids;
ALTER TABLE master_subject DROP COLUMN IF EXISTS local_context_ids;