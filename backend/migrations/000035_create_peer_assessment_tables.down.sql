-- Down migration: Remove peer assessment tables
DROP TABLE IF EXISTS trx_peer_assessment CASCADE;
DROP TABLE IF EXISTS master_peer_assessment_rubric CASCADE;