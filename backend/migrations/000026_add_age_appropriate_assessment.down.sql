-- Down migration: Remove age-appropriate assessment features
-- This migration adds columns and tables, reverse them
DROP TABLE IF EXISTS master_sd_assessment_criteria CASCADE;
ALTER TABLE trx_assessment DROP COLUMN IF EXISTS age_appropriate_type;