-- Down migration: Remove ILP tables and triggers
DROP TRIGGER IF EXISTS trigger_update_ilp_template_updated_at ON master_ilp_template;
DROP TRIGGER IF EXISTS trigger_update_milestone_updated_at ON trx_ilp_milestone;
DROP TRIGGER IF EXISTS trigger_update_ilp_updated_at ON trx_individual_learning_plan;
DROP FUNCTION IF EXISTS update_ilp_updated_at();
DROP TABLE IF EXISTS trx_ilp_milestone CASCADE;
DROP TABLE IF EXISTS trx_individual_learning_plan CASCADE;
DROP TABLE IF EXISTS master_ilp_template CASCADE;