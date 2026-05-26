-- Rollback for Phase 5: Security Enhancements
-- This removes RLS policies, security functions, and monitoring

-- ============================================
-- DISABLE ROW LEVEL SECURITY
-- ============================================

ALTER TABLE students DISABLE ROW LEVEL SECURITY;
ALTER TABLE teachers DISABLE ROW LEVEL SECURITY;
ALTER TABLE trx_student_assessment_result DISABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs DISABLE ROW LEVEL SECURITY;

-- ============================================
-- DROP RLS POLICIES
-- ============================================

-- Students Table Policies
DROP POLICY IF EXISTS students_school_isolation_policy ON students;
DROP POLICY IF EXISTS students_read_policy ON students;
DROP POLICY IF EXISTS students_update_policy ON students;

-- Teachers Table Policies
DROP POLICY IF EXISTS teachers_school_isolation_policy ON teachers;
DROP POLICY IF EXISTS teachers_read_policy ON teachers;

-- Assessment Results Policies
DROP POLICY IF EXISTS trx_student_assessment_result_school_policy ON trx_student_assessment_result;

-- Audit Logs Policies
DROP POLICY IF EXISTS audit_logs_admin_policy ON audit_logs;
DROP POLICY IF EXISTS audit_logs_read_policy ON audit_logs;

-- ============================================
-- DROP SECURITY FUNCTIONS
-- ============================================

DROP FUNCTION IF EXISTS set_school_context;
DROP FUNCTION IF EXISTS log_security_event;
DROP FUNCTION IF EXISTS check_data_access_permission;
DROP FUNCTION IF EXISTS mask_sensitive_data;
DROP FUNCTION IF EXISTS encrypt_sensitive_column;
DROP FUNCTION IF EXISTS decrypt_sensitive_column;
DROP FUNCTION IF EXISTS log_sensitive_data_access;
DROP FUNCTION IF EXISTS check_security_event_frequency;

-- ============================================
-- DROP SECURITY TRIGGERS
-- ============================================

DROP TRIGGER IF EXISTS tr_audit_log_security ON audit_logs;
DROP TRIGGER IF EXISTS tr_students_security ON students;
DROP TRIGGER IF EXISTS tr_teachers_security ON teachers;
DROP TRIGGER IF EXISTS tr_assessment_results_security ON trx_student_assessment_result;

-- ============================================
-- DROP SECURITY MONITORING VIEWS
-- ============================================

DROP VIEW IF EXISTS v_security_events;
DROP VIEW IF EXISTS v_security_alerts;
DROP VIEW IF EXISTS v_data_access_log;
DROP VIEW IF EXISTS v_security_metrics;

-- ============================================
-- DROP SECURITY CONFIGURATION TABLES
-- ============================================

DROP TABLE IF EXISTS security_configuration;
DROP TABLE IF EXISTS data_retention_policies;