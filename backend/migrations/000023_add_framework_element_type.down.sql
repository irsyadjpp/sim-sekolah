-- Down migration: Remove framework_element_type column and restore original data
ALTER TABLE dl_design_element DROP COLUMN IF EXISTS framework_element_type;

-- Remove the index
DROP INDEX IF EXISTS idx_dl_design_element_framework_type;