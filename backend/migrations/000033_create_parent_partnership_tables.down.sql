-- Down migration: Remove parent partnership tables
DROP TABLE IF EXISTS trx_parent_contribution CASCADE;
DROP TABLE IF EXISTS master_parent_partnership CASCADE;