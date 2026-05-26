-- Phase 5: Database Optimization & Future-Proofing
-- This migration implements performance optimizations for the database
-- Focus: Indexing optimization, security enhancements, and monitoring setup

-- ============================================
-- PERFORMANCE INDEXING OPTIMIZATION
-- ============================================

-- Assessment Results Indexing (High-traffic table)
CREATE INDEX IF NOT EXISTS idx_trx_student_assessment_result_student_date 
ON trx_student_assessment_result(student_id, assessment_date DESC);

CREATE INDEX IF NOT EXISTS idx_trx_student_assessment_result_subject_class 
ON trx_student_assessment_result(subject_id, classroom_id, assessment_date DESC);

CREATE INDEX IF NOT EXISTS idx_trx_student_assessment_result_type_status 
ON trx_student_assessment_result(assessment_type, status);

-- Audit Logs Indexing (High-volume table)
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_timestamp 
ON audit_logs(actor, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_logs_action_timestamp 
ON audit_logs(action, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_logs_school_timestamp 
ON audit_logs(school_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_logs_date_range 
ON audit_logs(created_at DESC) 
WHERE created_at >= CURRENT_DATE - INTERVAL '90 days';

-- Student Attendance Indexing
CREATE INDEX IF NOT EXISTS idx_trx_daily_attendance_student_date 
ON trx_daily_attendance(student_id, attendance_date DESC);

CREATE INDEX IF NOT EXISTS idx_trx_daily_attendance_class_date 
ON trx_daily_attendance(classroom_id, attendance_date DESC);

CREATE INDEX IF NOT EXISTS idx_trx_daily_attendance_status_date 
ON trx_daily_attendance(status, attendance_date DESC);

-- Teaching Assignment Indexing
CREATE Index IF NOT EXISTS idx_teaching_assignment_teacher_academic_year 
ON trx_teaching_assignment(teacher_id, academic_year_id);

CREATE INDEX IF NOT EXISTS idx_teaching_assignment_subject_class 
ON trx_teaching_assignment(subject_id, classroom_id);

-- Numeracy Assessment Indexing
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_student_date 
ON numeracy_assessments(student_id, assessment_date DESC);

CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_indicator 
ON numeracy_assessments(indicator_id);

-- Portfolio Artifacts Indexing
CREATE INDEX IF NOT EXISTS idx_portfolio_artifacts_student_type 
ON portfolio_artifacts(student_id, artifact_type);

CREATE INDEX IF NOT EXISTS idx_portfolio_artifacts_date 
ON portfolio_artifacts(created_at DESC);

-- Communication Indexing
CREATE INDEX IF NOT EXISTS idx_messages_recipient_date 
ON messages(recipient_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_messages_sender_date 
ON messages(sender_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_notifications_recipient_read 
ON notifications(recipient_id, is_read);

-- Offline Sync State Indexing
CREATE INDEX IF NOT EXISTS idx_sync_state_entity_status 
ON sync_state(entity_type, sync_status);

CREATE INDEX IF NOT EXISTS idx_sync_state_last_sync 
ON sync_state(last_sync_at);

-- ============================================
-- PARTIAL INDEXES FOR OPTIMIZATION
-- ============================================

-- Partial index for active records only (commonly queried)
CREATE INDEX IF NOT EXISTS idx_students_active 
ON students(status) 
WHERE status = 'ACTIVE';

CREATE INDEX IF NOT EXISTS idx_teachers_active 
ON teachers(status) 
WHERE status = 'ACTIVE';

CREATE INDEX IF NOT EXISTS idx_supervision_cycles_active 
ON supervision_cycles(status) 
WHERE status = 'ACTIVE';

CREATE INDEX IF NOT EXISTS idx_student_interventions_active 
ON student_intervention_assignments(status) 
WHERE status = 'ACTIVE';

-- Partial index for recent data (most commonly accessed)
CREATE INDEX IF NOT EXISTS idx_trx_student_assessment_result_recent 
ON trx_student_assessment_result(created_at DESC) 
WHERE created_at >= CURRENT_DATE - INTERVAL '6 months';

CREATE INDEX IF NOT EXISTS idx_audit_logs_recent 
ON audit_logs(created_at DESC) 
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';

-- ============================================
-- COMPOSITE INDEXES FOR COMPLEX QUERIES
-- ============================================

-- For student performance queries
CREATE INDEX IF NOT EXISTS idx_trx_student_assessment_result_student_subject_date 
ON trx_student_assessment_result(student_id, subject_id, assessment_date DESC);

-- For teacher workload analytics
CREATE INDEX IF NOT EXISTS idx_trx_teaching_assignment_teacher_date 
ON trx_teaching_assignment(teacher_id, created_at DESC);

-- For attendance analytics
CREATE INDEX IF NOT EXISTS idx_trx_daily_attendance_student_status_date 
ON trx_daily_attendance(student_id, status, attendance_date DESC);

-- For character intervention tracking
CREATE INDEX IF NOT EXISTS idx_student_character_interventions_teacher_status 
ON trx_student_character_intervention(teacher_id, current_status, assignment_date DESC);

-- For supervision analytics
CREATE INDEX IF NOT EXISTS idx_teacher_observations_observer_status 
ON teacher_observations(observer_id, status, observation_date DESC);

-- For learning analytics
CREATE INDEX IF NOT EXISTS idx_teaching_reflections_teacher_date 
ON teaching_reflections(teacher_id, reflection_date DESC);

-- ============================================
-- SECURITY ENHANCEMENTS
-- ============================================

-- Enable pgcrypto extension if not already enabled
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create function for data encryption
CREATE OR REPLACE FUNCTION encrypt_data(data text, secret_key text)
RETURNS bytea AS $$
BEGIN
    RETURN pgp_sym_encrypt(data::bytea, secret_key::bytea);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function for data decryption
CREATE OR REPLACE FUNCTION decrypt_data(data bytea, secret_key text)
RETURNS text AS $$
BEGIN
    RETURN pgp_sym_decrypt(data, secret_key::bytea)::text;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- ANALYTICS AND MONITORING VIEWS
-- ============================================

-- View for database size monitoring
CREATE OR REPLACE VIEW v_database_size AS
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname::text||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname::text||'.'||tablename) DESC;

-- View for index usage statistics
CREATE OR REPLACE VIEW v_index_usage AS
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC, idx_tup_read DESC;

-- View for table statistics
CREATE OR REPLACE VIEW v_table_statistics AS
SELECT 
    schemaname,
    tablename,
    n_live_tup as live_tuples,
    n_dead_tup as dead_tuples,
    last_vacuum,
    last_autovacuum,
    vacuum_count,
    autovacuum_count
FROM pg_stat_user_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY n_live_tup DESC;

-- View for slow queries monitoring (requires pg_stat_statements)
CREATE OR REPLACE VIEW v_slow_queries AS
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- ============================================
-- PARTITIONING STRATEGY (PREPARATION)
-- ============================================

-- Create partitioning function (for future use)
CREATE OR REPLACE FUNCTION create_partitioned_table()
RETURNS void AS $$
BEGIN
    -- This function is a placeholder for future partitioning implementation
    -- Partitioning will be implemented when tables grow significantly
    -- Target tables for partitioning:
    -- - trx_student_assessment_result (by academic_year)
    -- - audit_logs (by date)
    -- - trx_daily_attendance (by academic_year)
    -- - trx_teaching_assignment (by academic_year)
    
    RAISE NOTICE 'Partitioning strategy ready for implementation when needed';
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- MONITORING FUNCTIONS
-- ============================================

-- Function to check table bloat
CREATE OR REPLACE FUNCTION check_table_bloat()
RETURNS TABLE(
    schemaname text,
    tablename text,
    table_size bigint,
    table_bloat bigint,
    percentage float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        schemaname,
        tablename,
        pg_total_relation_size(schemaname::text||'.'||tablename) as table_size,
        pg_relation_size(schemaname::text||'.'||tablename) - pg_total_relation_size(schemaname::text||'.'||tablename) as table_bloat,
        CASE 
            WHEN pg_total_relation_size(schemaname::text||'.'||tablename) = 0 THEN 0
            ELSE ROUND(((pg_relation_size(schemaname::text||'.'||tablename) - pg_total_relation_size(schemaname::text||'.'||tablename))::numeric / pg_total_relation_size(schemaname::text||'.'||tablename)::numeric * 100, 2)
        END as percentage
    FROM pg_tables 
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY percentage DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to get index recommendations
CREATE OR REPLACE FUNCTION get_index_recommendations()
RETURNS TABLE(
    tablename text,
    indexname text,
    recommendation text,
    priority text
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        schemaname||'.'||tablename as tablename,
        indexname,
        CASE 
            WHEN idx_scan = 0 THEN 'Index never used - consider dropping'
            WHEN idx_tup_read < 1000 THEN 'Low usage index - evaluate necessity'
            WHEN pg_size_pretty(pg_relation_size(indexrelid))::text LIKE '%MB%' THEN 'Large index - consider optimization'
            ELSE 'Index appears healthy'
        END as recommendation,
        CASE 
            WHEN idx_scan = 0 THEN 'HIGH'
            WHEN idx_tup_read < 1000 THEN 'MEDIUM'
            ELSE 'LOW'
        END as priority
    FROM pg_stat_user_indexes
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY idx_scan ASC, idx_tup_read ASC;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- PERFORMANCE ANALYTICS FUNCTIONS
-- ============================================

-- Function to analyze query performance
CREATE OR REPLACE FUNCTION analyze_query_performance()
RETURNS TABLE(
    metric_name text,
    metric_value bigint,
    metric_description text
) AS $$
BEGIN
    -- Total database size
    INSERT INTO analyze_query_performance(metric_name, metric_value, metric_description)
    SELECT 
        'total_db_size', 
        pg_database_size(current_database()), 
        'Total database size in bytes';
    
    -- Total number of tables
    INSERT INTO analyze_query_performance(metric_name, metric_value, metric_description)
    SELECT 
        'total_tables', 
        COUNT(*), 
        'Total number of user tables'
    FROM pg_tables 
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
    
    -- Total number of indexes
    INSERT INTO analyze_query_performance(metric_name, metric_value, metric_description)
    SELECT 
        'total_indexes', 
        COUNT(*), 
        'Total number of user indexes'
    FROM pg_indexes 
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
    
    -- Total number of sequences
    INSERT INTO analyze_query_performance(metric_name, metric_value, metric_description)
    SELECT 
        'total_sequences', 
        COUNT(*), 
        'Total number of sequences'
    FROM pg_sequences;
    
    RETURN QUERY SELECT * FROM analyze_query_performance;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- ROW LEVEL SECURITY PREPARATION
-- ============================================

-- Enable RLS on sensitive tables (for future implementation)
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE trx_student_assessment_result ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (placeholder - to be customized based on requirements)
-- Example policy for students table (school isolation)
-- CREATE POLICY students_school_isolation_policy ON students
--     USING (school_id = current_setting('app.current_school_id')::uuid);

-- ============================================
-- BACKUP AND MAINTENANCE FUNCTIONS
-- ============================================

-- Function to get table statistics for maintenance planning
CREATE OR REPLACE FUNCTION get_maintenance_recommendations()
RETURNS TABLE(
    tablename text,
    action_required text,
    priority text,
    reason text
) AS $$
BEGIN
    RETURN QUERY
    WITH table_stats AS (
        SELECT 
            schemaname||'.'||tablename as tablename,
            n_live_tup,
            n_dead_tup,
            last_vacuum,
            last_autovacuum,
            vacuum_count,
            autovacuum_count
        FROM pg_stat_user_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    )
    SELECT 
        tablename,
        'VACUUM' as action_required,
        CASE 
            WHEN n_dead_tup > n_live_tup * 0.1 THEN 'HIGH'
            WHEN n_dead_tup > n_live_tup * 0.05 THEN 'MEDIUM'
            ELSE 'LOW'
        END as priority,
        'High table bloat: ' || n_dead_tup || ' dead tuples out of ' || n_live_tup || ' live tuples' as reason
    FROM table_stats
    WHERE n_dead_tup > n_live_tup * 0.05
    
    UNION ALL
    
    SELECT 
        tablename,
        'ANALYZE' as action_required,
        CASE 
            WHEN last_autovacuum < CURRENT_DATE - INTERVAL '7 days' THEN 'HIGH'
            WHEN last_autovacuum < CURRENT_DATE - INTERVAL '30 days' THEN 'MEDIUM'
            ELSE 'LOW'
        END as priority,
        'Statistics not updated since: ' || last_autovacuum as reason
    FROM table_stats
    WHERE last_autovacuum < CURRENT_DATE - INTERVAL '7 days';
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- COMMENTS AND DOCUMENTATION
-- ============================================

COMMENT ON SCHEMA public IS 'Main schema for SIM Sekolah database';

COMMENT ON FUNCTION encrypt_data IS 'Encrypts data using pgcrypto for sensitive information';
COMMENT ON FUNCTION decrypt_data IS 'Decrypts data encrypted with encrypt_data function';
COMMENT ON FUNCTION check_table_bloat IS 'Analyzes table bloat and returns recommendations';
COMMENT ON FUNCTION get_index_recommendations IS 'Analyzes index usage and provides optimization recommendations';
COMMENT ON FUNCTION analyze_query_performance IS 'Provides database performance metrics and statistics';
COMMENT ON FUNCTION get_maintenance_recommendations IS 'Suggests maintenance actions based on table statistics';

COMMENT ON VIEW v_database_size IS 'Monitor database and table sizes for storage planning';
COMMENT ON VIEW v_index_usage IS 'Track index usage statistics for optimization';
COMMENT ON VIEW v_table_statistics IS 'Monitor table statistics for maintenance planning';
COMMENT ON VIEW v_slow_queries IS 'Identify slow queries for performance tuning';

-- ============================================
-- STATISTICS UPDATE
-- ============================================

-- Update statistics for better query planning
ANALYZE students;
ANALYZE teachers;
ANALYZE trx_student_assessment_result;
ANALYZE audit_logs;
ANALYZE trx_daily_attendance;
ANALYZE trx_teaching_assignment;
ANALYZE supervision_cycles;
ANALYZE teacher_observations;
ANALYZE teaching_reflections;

-- ============================================
-- PERFORMANCE NOTES
-- ============================================

-- This migration includes:
-- 1. Strategic indexes for high-traffic tables (trx_student_assessment_result, audit_logs, attendance)
-- 2. Partial indexes for commonly filtered data (active records, recent data)
-- 3. Composite indexes for complex query patterns
-- 4. Security enhancements (encryption functions, RLS preparation)
-- 5. Monitoring views and functions for database health
-- 6. Maintenance functions for ongoing optimization

-- Partitioning strategy is prepared but not implemented yet
-- (will be implemented when tables grow significantly)

-- RLS policies are enabled but not configured
-- (will be customized based on multi-tenancy requirements)

-- Encryption functions are ready for sensitive data protection
-- (implementation requires secret key management)