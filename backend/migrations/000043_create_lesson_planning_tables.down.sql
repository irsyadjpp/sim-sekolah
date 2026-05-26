-- Down migration: Remove lesson planning tables
DROP TABLE IF EXISTS lesson_resources CASCADE;
DROP TABLE IF EXISTS lesson_plans CASCADE;