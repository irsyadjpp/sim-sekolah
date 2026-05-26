-- Down migration: Remove learning experience tables
DROP TABLE IF EXISTS trx_student_experience_progression CASCADE;
DROP TABLE IF EXISTS trx_activity_experience_mapping CASCADE;
DROP TABLE IF EXISTS master_learning_experience CASCADE;