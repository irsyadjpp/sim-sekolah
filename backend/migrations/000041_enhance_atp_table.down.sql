-- Down migration: Remove ATP table enhancements
ALTER TABLE cur_atp DROP COLUMN IF EXISTS differentiation_strategy;
ALTER TABLE cur_atp DROP COLUMN IF EXISTS assessment_mode;