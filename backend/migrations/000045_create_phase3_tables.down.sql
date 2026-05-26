-- Down migration: Remove Phase 3 tables
DROP TABLE IF EXISTS teaching_reflections CASCADE;
DROP TABLE IF EXISTS teacher_observations CASCADE;
DROP TABLE IF EXISTS supervision_feedback CASCADE;
DROP TABLE IF EXISTS supervision_cycles CASCADE;