-- Down migration: Remove character intervention tables
DROP TABLE IF EXISTS trx_student_character_intervention CASCADE;
DROP TABLE IF EXISTS master_character_intervention CASCADE;