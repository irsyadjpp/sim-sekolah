-- Down migration: Remove offline sync tables
DROP TABLE IF EXISTS sync_state CASCADE;