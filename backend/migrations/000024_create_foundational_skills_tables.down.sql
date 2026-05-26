-- Down migration: Remove foundational skills assessment tables
DROP TABLE IF EXISTS trx_foundational_skill_assessment CASCADE;
DROP TABLE IF EXISTS master_foundational_skill_standard CASCADE;