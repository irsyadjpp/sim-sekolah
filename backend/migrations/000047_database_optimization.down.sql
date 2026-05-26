-- Rollback for Phase 5: Database Optimization & Future-Proofing
-- This removes the performance indexes, security functions, and monitoring views

-- ============================================
-- DROP MONITORING VIEWS
-- ============================================

DROP VIEW IF EXISTS v_database_size;
DROP VIEW IF EXISTS v_index_usage;
DROP VIEW IF EXISTS v_table_statistics;
DROP VIEW IF EXISTS v_slow_queries;

-- ============================================
-- DROP MONITORING FUNCTIONS
-- ============================================

DROP FUNCTION IF EXISTS check_table_bloat;
DROP FUNCTION IF EXISTS check_index_bloat;
DROP FUNCTION IF EXISTS get_table_stats;
DROP FUNCTION IF EXISTS analyze_query_performance;
DROP FUNCTION IF EXISTS create_partitioned_table;

-- ============================================
-- DROP SECURITY FUNCTIONS
-- ============================================

DROP FUNCTION IF EXISTS encrypt_data;
DROP FUNCTION IF EXISTS decrypt_data;

-- ============================================
-- DROP INDEXES (Performance optimization)
-- ============================================

-- Assessment Results Indexes
DROP INDEX IF EXISTS idx_trx_student_assessment_result_student_date;
DROP INDEX IF EXISTS idx_trx_student_assessment_result_subject_class;
DROP INDEX IF EXISTS idx_trx_student_assessment_result_type_status;

-- Audit Logs Indexes
DROP INDEX IF EXISTS idx_audit_logs_actor_timestamp;
DROP INDEX IF EXISTS idx_audit_logs_action_timestamp;
DROP INDEX IF EXISTS idx_audit_logs_school_timestamp;
DROP INDEX IF EXISTS idx_audit_logs_date_range;

-- Student Attendance Indexes
DROP INDEX IF EXISTS idx_trx_daily_attendance_student_date;
DROP INDEX IF EXISTS idx_trx_daily_attendance_class_date;
DROP INDEX IF EXISTS idx_trx_daily_attendance_status_date;

-- Teaching Assignment Indexes
DROP INDEX IF EXISTS idx_trx_teaching_assignment_teacher_academic_year;
DROP INDEX IF EXISTS idx_trx_teaching_assignment_subject_class;

-- Numeracy Assessment Indexes
DROP INDEX IF EXISTS idx_numeracy_assessments_student_date;
DROP INDEX IF EXISTS idx_numeracy_assessments_indicator;

-- Portfolio Artifacts Indexes
DROP INDEX IF EXISTS idx_portfolio_artifacts_student_type;
DROP INDEX IF EXISTS idx_portfolio_artifacts_date;

-- Communication Indexes
DROP INDEX IF EXISTS idx_messages_recipient_date;
DROP INDEX IF EXISTS idx_messages_sender_date;
DROP INDEX IF EXISTS idx_notifications_recipient_read;

-- Offline Sync State Indexes
DROP INDEX IF EXISTS idx_sync_state_entity_status;
DROP INDEX IF EXISTS idx_sync_state_last_sync;

-- Partial Indexes
DROP INDEX IF EXISTS idx_students_active;
DROP INDEX IF EXISTS idx_teachers_active;
DROP INDEX IF EXISTS idx_supervision_cycles_active;
DROP INDEX IF EXISTS idx_student_intervention_assignments_active;
DROP INDEX IF EXISTS idx_trx_student_assessment_result_recent;
DROP INDEX IF EXISTS idx_audit_logs_recent;

-- Composite Indexes
DROP INDEX IF EXISTS idx_trx_student_assessment_result_student_subject_date;
DROP INDEX IF EXISTS idx_trx_teaching_assignments_teacher_date;
DROP INDEX IF EXISTS idx_trx_daily_attendance_student_status_date;
DROP INDEX IF EXISTS idx_trx_student_character_interventions_teacher_status;
DROP INDEX IF EXISTS idx_teacher_observations_observer_status;
DROP INDEX IF EXISTS idx_teaching_reflections_teacher_date;

-- ============================================
-- DROP EXTENSION (if no longer needed)
-- ============================================

-- Note: pgcrypto might be used by other features, so we don't drop it here
-- DROP EXTENSION IF EXISTS pgcrypto;