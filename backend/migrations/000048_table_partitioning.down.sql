-- Rollback for Phase 5: Table Partitioning Strategy (PREPARATION ONLY)
-- This removes the partitioning helper functions and monitoring views

-- ============================================
-- DROP PARTITIONING MONITORING VIEWS
-- ============================================

DROP VIEW IF EXISTS v_partition_sizes;

-- ============================================
-- DROP PARTITIONING HELPER FUNCTIONS
-- ============================================

DROP FUNCTION IF EXISTS create_audit_log_partition;
DROP FUNCTION IF EXISTS create_attendance_partition;
DROP FUNCTION IF EXISTS create_assessment_partition;
DROP FUNCTION IF EXISTS drop_old_partition;