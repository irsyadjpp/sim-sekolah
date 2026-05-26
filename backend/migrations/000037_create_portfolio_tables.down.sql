-- Down migration: Remove portfolio tables
DROP TABLE IF EXISTS portfolio_artifacts CASCADE;
DROP TABLE IF EXISTS portfolios CASCADE;