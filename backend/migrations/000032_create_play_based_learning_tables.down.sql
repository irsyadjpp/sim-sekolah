-- Down migration: Remove play-based learning tables
DROP TRIGGER IF EXISTS trigger_update_play_activity_updated_at ON trx_play_based_activity;
DROP TRIGGER IF EXISTS trigger_update_play_type_updated_at ON master_play_activity_type;
DROP FUNCTION IF EXISTS update_play_updated_at();
DROP TABLE IF EXISTS trx_play_based_activity CASCADE;
DROP TABLE IF EXISTS master_play_activity_type CASCADE;