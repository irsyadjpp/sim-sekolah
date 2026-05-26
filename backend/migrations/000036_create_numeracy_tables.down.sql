-- Down migration: Remove numeracy assessment tables
DROP TABLE IF EXISTS numeracy_assessments CASCADE;
DROP TABLE IF EXISTS numeracy_indicators CASCADE;