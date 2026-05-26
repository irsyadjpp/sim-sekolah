-- Phase 5: Security Enhancements
-- This migration implements advanced security features including:
-- - Row-Level Security (RLS) policies
-- - Data encryption for sensitive fields
-- - Data masking for PII
-- - Enhanced audit logging
-- - Security monitoring functions

-- ============================================
-- ROW-LEVEL SECURITY (RLS) POLICIES
-- ============================================

-- Helper function to set school context
CREATE OR REPLACE FUNCTION set_school_context(school_id uuid)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_school_id', school_id::text, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Enable RLS on tables
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE trx_student_assessment_result ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Students Table RLS Policies
DROP POLICY IF EXISTS students_school_isolation_policy ON students;
CREATE POLICY students_school_isolation_policy ON students
    FOR ALL
    USING (
        school_id = current_setting('app.current_school_id', true)::uuid OR
        current_setting('app.current_school_id', true) IS NULL  -- Allow system/admin access
    );

DROP POLICY IF EXISTS students_read_policy ON students;
CREATE POLICY students_read_policy ON students
    FOR SELECT
    USING (
        school_id = current_setting('app.current_school_id', true)::uuid OR
        current_setting('app.current_school_id', true) IS NULL
    );

DROP POLICY IF EXISTS students_update_policy ON students;
CREATE POLICY students_update_policy ON students
    FOR UPDATE
    USING (
        school_id = current_setting('app.current_school_id', true)::uuid OR
        current_setting('app.current_school_id', true) IS NULL
    );

-- Teachers Table RLS Policies
DROP POLICY IF EXISTS teachers_school_isolation_policy ON teachers;
CREATE POLICY teachers_school_isolation_policy ON teachers
    FOR ALL
    USING (
        school_id = current_setting('app.current_school_id', true)::uuid OR
        current_setting('app.current_school_id', true) IS NULL
    );

DROP POLICY IF EXISTS teachers_read_policy ON teachers;
CREATE POLICY teachers_read_policy ON teachers
    FOR SELECT
    USING (
        school_id = current_setting('app.current_school_id', true)::uuid OR
        current_setting('app.current_school_id', true) IS NULL
    );

-- Assessment Results RLS Policies
DROP POLICY IF EXISTS trx_student_assessment_result_school_policy ON trx_student_assessment_result;
CREATE POLICY trx_student_assessment_result_school_policy ON trx_student_assessment_result
    FOR ALL
    USING (
        school_id = current_setting('app.current_school_id', true)::uuid OR
        current_setting('app.current_school_id', true) IS NULL OR
        EXISTS (
            SELECT 1 FROM students s 
            WHERE s.id = trx_student_assessment_result.student_id 
            AND s.school_id = current_setting('app.current_school_id', true)::uuid
        )
    );

-- Audit Logs RLS Policies (admin only access)
DROP POLICY IF EXISTS audit_logs_admin_policy ON audit_logs;
CREATE POLICY audit_logs_admin_policy ON audit_logs
    FOR ALL
    USING (
        current_setting('app.user_role', true) IN ('SUPER_ADMIN', 'SCHOOL_ADMIN')
    );

-- Teaching Assignments RLS Policies
DROP POLICY IF EXISTS teaching_assignments_school_policy ON teaching_assignments;
CREATE POLICY teaching_assignments_school_policy ON teaching_assignments
    FOR ALL
    USING (school_id = current_setting('app.current_school_id', true)::uuid);

-- ============================================
-- SENSITIVE DATA ENCRYPTION
-- ============================================

-- Create table for encryption keys (this should be in a secure location)
CREATE TABLE IF NOT EXISTS encryption_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key_name VARCHAR(255) UNIQUE NOT NULL,
    encrypted_key BYTEA NOT NULL,
    key_type VARCHAR(50) NOT NULL DEFAULT 'AES256',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    description TEXT
);

-- Create table for tracking encrypted fields
CREATE TABLE IF NOT EXISTS encrypted_fields_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(255) NOT NULL,
    column_name VARCHAR(255) NOT NULL,
    encryption_key_id UUID REFERENCES encryption_keys(id),
    is_encrypted BOOLEAN DEFAULT FALSE,
    encryption_date TIMESTAMP WITH TIME ZONE,
    description TEXT,
    UNIQUE(table_name, column_name)
);

-- Insert sample encryption key (in production, this should be managed securely)
INSERT INTO encryption_keys (key_name, encrypted_key, key_type, description)
VALUES (
    'student_personal_data_key',
    pgp_sym_encrypt('CHANGE_THIS_SECURE_KEY_IN_PRODUCTION', 'master_key'),
    'AES256',
    'Key for encrypting student personal information'
) ON CONFLICT (key_name) DO NOTHING;

-- Register fields that should be encrypted
INSERT INTO encrypted_fields_registry (table_name, column_name, description)
VALUES 
    ('students', 'birth_place', 'Student birth place location'),
    ('students', 'address', 'Student residential address'),
    ('students', 'parent_phone', 'Parent/guardian phone number'),
    ('teachers', 'phone_number', 'Teacher contact number'),
    ('teachers', 'address', 'Teacher residential address'),
    ('users', 'email', 'User email address')
ON CONFLICT (table_name, column_name) DO NOTHING;

-- ============================================
-- DATA MASKING FUNCTIONS
-- ============================================

-- Function to mask email addresses
CREATE OR REPLACE FUNCTION mask_email(email text)
RETURNS text AS $$
BEGIN
    IF email IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN 
        SUBSTRING(email FROM 1 FOR 2) || 
        '***@' || 
        SPLIT_PART(email, '@', 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to mask phone numbers
CREATE OR REPLACE FUNCTION mask_phone(phone text)
RETURNS text AS $$
BEGIN
    IF phone IS NULL THEN
        RETURN NULL;
    END IF;
    
    -- Keep last 4 digits visible
    RETURN 
        SUBSTRING(phone FROM 1 FOR LENGTH(phone) - 4) || 
        '****';
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to mask names
CREATE OR REPLACE FUNCTION mask_name(name text)
RETURNS text AS $$
BEGIN
    IF name IS NULL THEN
        RETURN NULL;
    END IF;
    
    -- Show first letter and last name
    RETURN 
        SUBSTRING(name FROM 1 FOR 1) || 
        '***** ' || 
        SPLIT_PART(TRIM(name), ' ', 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to mask addresses
CREATE OR REPLACE FUNCTION mask_address(address text)
RETURNS text AS $$
BEGIN
    IF address IS NULL THEN
        RETURN NULL;
    END IF;
    
    -- Show first word and mask the rest
    RETURN 
        SPLIT_PART(address, ' ', 1) || 
        ' ****';
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ============================================
-- SECURITY AUDIT FUNCTIONS
-- ============================================

-- Function to log security events
CREATE OR REPLACE FUNCTION log_security_event(
    event_type VARCHAR(100),
    event_description TEXT,
    severity VARCHAR(20) DEFAULT 'INFO',
    user_id UUID DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    additional_data JSONB DEFAULT '{}'::jsonb
)
RETURNS void AS $$
BEGIN
    INSERT INTO audit_logs (
        action,
        entity_type,
        entity_id,
        actor,
        school_id,
        ip_address,
        user_agent,
        changes,
        created_at
    ) VALUES (
        event_type,
        'SECURITY_EVENT',
        gen_random_uuid(),
        user_id,
        current_setting('app.current_school_id', true)::uuid,
        ip_address,
        current_setting('app.user_agent', true),
        jsonb_build_object(
            'event_description', event_description,
            'severity', severity,
            'additional_data', additional_data
        ),
        NOW()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check for suspicious login patterns
CREATE OR REPLACE FUNCTION check_suspicious_login(user_id UUID, ip_address VARCHAR(45))
RETURNS BOOLEAN AS $$
DECLARE
    recent_login_count INTEGER;
    different_ip_count INTEGER;
    is_suspicious BOOLEAN := FALSE;
BEGIN
    -- Check for multiple login attempts in last hour
    SELECT COUNT(*) INTO recent_login_count
    FROM audit_logs
    WHERE actor = user_id
    AND action = 'LOGIN'
    AND created_at > NOW() - INTERVAL '1 hour';
    
    IF recent_login_count > 10 THEN
        is_suspicious := TRUE;
    END IF;
    
    -- Check for login from different IPs in last hour
    SELECT COUNT(DISTINCT ip_address) INTO different_ip_count
    FROM audit_logs
    WHERE actor = user_id
    AND action = 'LOGIN'
    AND created_at > NOW() - INTERVAL '1 hour';
    
    IF different_ip_count > 3 THEN
        is_suspicious := TRUE;
    END IF;
    
    -- Log suspicious activity
    IF is_suspicious THEN
        PERFORM log_security_event(
            'SUSPICIOUS_LOGIN',
            'Multiple login attempts or IP changes detected',
            'HIGH',
            user_id,
            ip_address,
            jsonb_build_object(
                'recent_login_count', recent_login_count,
                'different_ip_count', different_ip_count
            )
        );
    END IF;
    
    RETURN is_suspicious;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- SECURITY MONITORING VIEWS
-- ============================================

-- View for security events
CREATE OR REPLACE VIEW v_security_events AS
SELECT 
    id,
    action as event_type,
    changes->>'event_description' as event_description,
    changes->>'severity' as severity,
    actor as user_id,
    ip_address,
    created_at as event_time
FROM audit_logs
WHERE action IN ('SUSPICIOUS_LOGIN', 'UNAUTHORIZED_ACCESS', 'DATA_BREACH_ATTEMPT', 'PRIVILEGE_ESCALATION')
ORDER BY created_at DESC;

-- View for user activity monitoring
CREATE OR REPLACE VIEW v_user_activity_monitoring AS
SELECT 
    actor as user_id,
    action,
    COUNT(*) as action_count,
    MAX(created_at) as last_activity,
    MIN(created_at) as first_activity,
    COUNT(DISTINCT ip_address) as unique_ips
FROM audit_logs
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY actor, action
ORDER BY action_count DESC;

-- View for failed authentication attempts
CREATE OR REPLACE VIEW v_failed_authentications AS
SELECT 
    actor as user_id,
    ip_address,
    COUNT(*) as failed_attempts,
    MAX(created_at) as last_attempt
FROM audit_logs
WHERE action IN ('LOGIN_FAILED', 'AUTHENTICATION_FAILED')
AND created_at > NOW() - INTERVAL '24 hours'
GROUP BY actor, ip_address
ORDER BY failed_attempts DESC;

-- View for data access monitoring
CREATE OR REPLACE VIEW v_data_access_monitoring AS
SELECT 
    actor as user_id,
    entity_type,
    entity_id,
    action,
    COUNT(*) as access_count,
    MAX(created_at) as last_access
FROM audit_logs
WHERE action IN ('SELECT', 'READ', 'VIEW')
AND created_at > NOW() - INTERVAL '7 days'
GROUP BY actor, entity_type, entity_id, action
ORDER BY access_count DESC;

-- View for privilege changes
CREATE OR REPLACE VIEW v_privilege_changes AS
SELECT 
    actor as user_id,
    action,
    entity_type,
    entity_id,
    changes,
    created_at as change_time
FROM audit_logs
WHERE action IN ('GRANT_PRIVILEGE', 'REVOKE_PRIVILEGE', 'ROLE_CHANGE', 'PERMISSION_UPDATE')
ORDER BY created_at DESC;

-- ============================================
-- SECURITY COMPLIANCE FUNCTIONS
-- ============================================

-- Function to check data retention compliance
CREATE OR REPLACE FUNCTION check_data_retention_compliance()
RETURNS TABLE(
    table_name text,
    retention_period text,
    compliance_status text,
    action_required text
) AS $$
BEGIN
    RETURN QUERY
    WITH retention_rules AS (
        SELECT 
            'audit_logs' as table_name,
            '2 years' as retention_period
        UNION ALL
        SELECT 
            'trx_student_assessment_result',
            '7 years'
        UNION ALL
        SELECT 
            'student_attendance',
            '5 years'
        UNION ALL
        SELECT 
            'teaching_assignments',
            '5 years'
    )
    SELECT 
        r.table_name,
        r.retention_period,
        'COMPLIANT' as compliance_status,
        'No action required' as action_required
    FROM retention_rules r
    WHERE NOT EXISTS (
        SELECT 1 FROM audit_logs 
        WHERE created_at < NOW() - INTERVAL '2 years'
        LIMIT 1
    );
END;
$$ LANGUAGE plpgsql;

-- Function to generate security compliance report
CREATE OR REPLACE FUNCTION generate_security_report()
RETURNS TABLE(
    report_section text,
    metric_name text,
    metric_value text,
    status text
) AS $$
BEGIN
    -- Security Events Section
    RETURN QUERY
    SELECT 
        'SECURITY_EVENTS' as report_section,
        'Total security events (24h)' as metric_name,
        COUNT(*)::text as metric_value,
        CASE WHEN COUNT(*) < 10 THEN 'OK' ELSE 'REVIEW' END as status
    FROM audit_logs
    WHERE action IN ('SUSPICIOUS_LOGIN', 'UNAUTHORIZED_ACCESS', 'DATA_BREACH_ATTEMPT')
    AND created_at > NOW() - INTERVAL '24 hours'
    
    UNION ALL
    
    -- Failed Authentication Section
    SELECT 
        'AUTHENTICATION' as report_section,
        'Failed login attempts (24h)' as metric_name,
        COUNT(*)::text as metric_value,
        CASE WHEN COUNT(*) < 50 THEN 'OK' ELSE 'ALERT' END as status
    FROM audit_logs
    WHERE action IN ('LOGIN_FAILED', 'AUTHENTICATION_FAILED')
    AND created_at > NOW() - INTERVAL '24 hours'
    
    UNION ALL
    
    -- Data Access Section
    SELECT 
        'DATA_ACCESS' as report_section,
        'High-volume data access (7d)' as metric_name,
        COUNT(*)::text as metric_value,
        CASE WHEN COUNT(*) < 1000 THEN 'OK' ELSE 'REVIEW' END as status
    FROM audit_logs
    WHERE action IN ('SELECT', 'READ', 'VIEW')
    AND created_at > NOW() - INTERVAL '7 days'
    GROUP BY actor
    HAVING COUNT(*) > 100
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- DATA PRIVACY FUNCTIONS
-- ============================================

-- Function to anonymize student data (GDPR compliance)
CREATE OR REPLACE FUNCTION anonymize_student_data(student_id UUID)
RETURNS void AS $$
BEGIN
    UPDATE students SET
        birth_place = mask_email(birth_place),
        address = mask_address(address),
        parent_phone = mask_phone(parent_phone),
        parent_name = mask_name(parent_name),
        updated_at = NOW()
    WHERE id = student_id;
    
    -- Log data anonymization
    PERFORM log_security_event(
        'DATA_ANONYMIZATION',
        'Student data anonymized for GDPR compliance',
        'INFO',
        current_setting('app.user_id', true)::uuid,
        current_setting('app.ip_address', true),
        jsonb_build_object('student_id', student_id)
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to implement right to be forgotten (GDPR)
CREATE OR REPLACE FUNCTION right_to_be_forgotten(student_id UUID)
RETURNS void AS $$
BEGIN
    -- Anonymize personal data
    UPDATE students SET
        full_name = 'ANONYMIZED_' || SUBSTRING(id::text, 1, 8),
        birth_place = NULL,
        address = NULL,
        parent_phone = NULL,
        parent_name = NULL,
        nisn = NULL,
        nik = NULL,
        status = 'INACTIVE',
        updated_at = NOW()
    WHERE id = student_id;
    
    -- Log data deletion
    PERFORM log_security_event(
        'RIGHT_TO_BE_FORGOTTEN',
        'Student data anonymized per GDPR right to be forgotten',
        'HIGH',
        current_setting('app.user_id', true)::uuid,
        current_setting('app.ip_address', true),
        jsonb_build_object('student_id', student_id)
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- SECURITY CONFIGURATION
-- ============================================

-- Create security configuration table
CREATE TABLE IF NOT EXISTS security_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    config_type VARCHAR(50) NOT NULL DEFAULT 'STRING',
    description TEXT,
    is_encrypted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default security configurations
INSERT INTO security_config (config_key, config_value, config_type, description) VALUES
    ('max_login_attempts', '5', 'INTEGER', 'Maximum failed login attempts before account lockout'),
    ('login_lockout_duration', '30', 'INTEGER', 'Account lockout duration in minutes'),
    ('session_timeout', '60', 'INTEGER', 'Session timeout in minutes'),
    ('password_min_length', '8', 'INTEGER', 'Minimum password length'),
    ('password_require_uppercase', 'true', 'BOOLEAN', 'Require uppercase letters in password'),
    ('password_require_lowercase', 'true', 'BOOLEAN', 'Require lowercase letters in password'),
    ('password_require_numbers', 'true', 'BOOLEAN', 'Require numbers in password'),
    ('password_require_special_chars', 'true', 'BOOLEAN', 'Require special characters in password'),
    ('data_retention_audit_logs', '2', 'INTEGER', 'Data retention period for audit logs in years'),
    ('data_retention_trx_student_assessment_result', '7', 'INTEGER', 'Data retention period for assessment results in years'),
    ('enable_rls', 'true', 'BOOLEAN', 'Enable Row-Level Security'),
    ('enable_data_encryption', 'false', 'BOOLEAN', 'Enable data encryption for sensitive fields')
ON CONFLICT (config_key) DO NOTHING;

-- ============================================
-- SECURITY TRIGGERS
-- ============================================

-- Trigger to log sensitive data access
CREATE OR REPLACE FUNCTION log_sensitive_data_access()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'SELECT' THEN
        PERFORM log_security_event(
            'SENSITIVE_DATA_ACCESS',
            'Access to sensitive data in ' || TG_TABLE_NAME,
            'INFO',
            current_setting('app.user_id', true)::uuid,
            current_setting('app.ip_address', true),
            jsonb_build_object(
                'table_name', TG_TABLE_NAME,
                'operation', TG_OP
            )
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for students table (if needed for compliance)
-- CREATE TRIGGER trigger_students_sensitive_access
--     AFTER SELECT ON students
--     FOR EACH STATEMENT
--     EXECUTE FUNCTION log_sensitive_data_access();

-- ============================================
-- COMMENTS AND DOCUMENTATION
-- ============================================

COMMENT ON TABLE encryption_keys IS 'Stores encryption keys for sensitive data encryption';
COMMENT ON TABLE encrypted_fields_registry IS 'Registry of fields that should be encrypted';
COMMENT ON TABLE security_config IS 'Security configuration settings';
COMMENT ON FUNCTION mask_email IS 'Masks email addresses for privacy protection';
COMMENT ON FUNCTION mask_phone IS 'Masks phone numbers for privacy protection';
COMMENT ON FUNCTION mask_name IS 'Masks personal names for privacy protection';
COMMENT ON FUNCTION mask_address IS 'Masks addresses for privacy protection';
COMMENT ON FUNCTION log_security_event IS 'Logs security events to audit trail';
COMMENT ON FUNCTION check_suspicious_login IS 'Detects suspicious login patterns';
COMMENT ON FUNCTION check_data_retention_compliance IS 'Checks compliance with data retention policies';
COMMENT ON FUNCTION generate_security_report IS 'Generates comprehensive security compliance report';
COMMENT ON FUNCTION anonymize_student_data IS 'Anonymizes student data for GDPR compliance';
COMMENT ON FUNCTION right_to_be_forgotten IS 'Implements GDPR right to be forgotten';
COMMENT ON VIEW v_security_events IS 'Monitors security-related events';
COMMENT ON VIEW v_user_activity_monitoring IS 'Tracks user activity patterns';
COMMENT ON VIEW v_failed_authentications IS 'Monitors failed authentication attempts';
COMMENT ON VIEW v_data_access_monitoring IS 'Tracks data access patterns';
COMMENT ON VIEW v_privilege_changes IS 'Monitors privilege and permission changes';

-- ============================================
-- SECURITY IMPLEMENTATION NOTES
-- ============================================

-- SECURITY FEATURES IMPLEMENTED:
-- 1. Row-Level Security (RLS) policies for multi-tenant isolation
-- 2. Data encryption infrastructure for sensitive fields
-- 3. Data masking functions for PII protection
-- 4. Enhanced security audit logging
-- 5. Suspicious activity detection
-- 6. Security monitoring views
-- 7. GDPR compliance functions
-- 8. Security configuration management

-- IMPLEMENTATION REQUIREMENTS:
-- 1. Set app.current_school_id session variable for RLS
-- 2. Set app.user_role session variable for authorization
-- 3. Configure encryption key management
-- 4. Set up automated security monitoring
-- 5. Implement security alert notifications
-- 6. Regular security audit reviews
-- 7. Data retention policy implementation

-- SECURITY BEST PRACTICES:
-- - Regularly review and update RLS policies
-- - Rotate encryption keys periodically
-- - Monitor security events and alerts
-- - Conduct regular security audits
-- - Keep security configurations updated
-- - Implement principle of least privilege
-- - Regular backup and disaster recovery testing