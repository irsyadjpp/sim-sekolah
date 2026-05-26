-- Down migration: Remove reading literacy assessment tables
DROP TABLE IF EXISTS trx_reading_literacy_assessment CASCADE;
DROP TABLE IF EXISTS master_reading_level CASCADE;