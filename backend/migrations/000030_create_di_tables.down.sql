-- Down migration: Remove Differentiated Instruction tables
DROP TRIGGER IF EXISTS trigger_update_di_strategy_updated_at ON master_di_strategy;
DROP FUNCTION IF EXISTS update_di_updated_at();
DROP TABLE IF EXISTS trx_module_differentiation CASCADE;
DROP TABLE IF EXISTS master_di_strategy CASCADE;