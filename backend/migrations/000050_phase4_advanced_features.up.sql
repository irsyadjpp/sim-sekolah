-- Phase 4: Advanced Features & Interoperability
-- This migration implements Phase 4 components:
-- 1. Document Repository
-- 2. Question Bank System
-- 3. Dapodik Integration
-- 4. Enhanced Notification System

-- ============================================
-- DOCUMENT REPOSITORY TABLES
-- ============================================

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    document_number VARCHAR(100) UNIQUE,
    category VARCHAR(50) NOT NULL,
    document_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    access_level VARCHAR(20) NOT NULL DEFAULT 'INTERNAL',
    file_url VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT,
    file_hash VARCHAR(64),
    mime_type VARCHAR(100),
    author_id UUID NOT NULL,
    department_id UUID,
    school_id UUID NOT NULL,
    tags TEXT, -- JSON array of tags
    version INTEGER DEFAULT 1,
    is_current_version BOOLEAN DEFAULT true,
    parent_document_id UUID,
    published_date TIMESTAMPTZ,
    expiry_date TIMESTAMPTZ,
    effective_date TIMESTAMPTZ,
    review_date TIMESTAMPTZ,
    archived_date TIMESTAMPTZ,
    download_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    is_confidential BOOLEAN DEFAULT false,
    requires_signature BOOLEAN DEFAULT false,
    storage_location VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for documents
CREATE INDEX idx_documents_school_id ON documents(school_id);
CREATE INDEX idx_documents_author_id ON documents(author_id);
CREATE INDEX idx_documents_category ON documents(category);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_document_type ON documents(document_type);
CREATE INDEX idx_documents_access_level ON documents(access_level);
CREATE INDEX idx_documents_parent_document_id ON documents(parent_document_id);

-- Document versions table
CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL,
    version_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT,
    file_hash VARCHAR(64),
    change_summary TEXT,
    changed_by UUID NOT NULL,
    change_reason TEXT,
    is_major_version BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_document_versions_document_id ON document_versions(document_id);

-- Document approvals table
CREATE TABLE IF NOT EXISTS document_approvals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL,
    approver_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL,
    comments TEXT,
    approved_at TIMESTAMPTZ,
    approval_level INTEGER NOT NULL,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_document_approvals_document_id ON document_approvals(document_id);
CREATE INDEX idx_document_approvals_approver_id ON document_approvals(approver_id);

-- Document categories table
CREATE TABLE IF NOT EXISTS document_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(7),
    icon VARCHAR(50),
    parent_id UUID,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Document tags table
CREATE TABLE IF NOT EXISTS document_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(7),
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Document tag associations table
CREATE TABLE IF NOT EXISTS document_tag_associations (
    document_id UUID NOT NULL,
    tag_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID,
    PRIMARY KEY (document_id, tag_id)
);

-- Document access logs table
CREATE TABLE IF NOT EXISTS document_access_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    access_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    additional_info JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_document_access_logs_document_id ON document_access_logs(document_id);
CREATE INDEX idx_document_access_logs_user_id ON document_access_logs(user_id);
CREATE INDEX idx_document_access_logs_access_time ON document_access_logs(access_time DESC);

-- Document shares table
CREATE TABLE IF NOT EXISTS document_shares (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL,
    shared_with UUID NOT NULL,
    shared_by UUID NOT NULL,
    share_type VARCHAR(20) NOT NULL,
    permission VARCHAR(20) NOT NULL,
    expires_at TIMESTAMPTZ,
    access_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_document_shares_document_id ON document_shares(document_id);
CREATE INDEX idx_document_shares_shared_with ON document_shares(shared_with);

-- Accreditation documents table
CREATE TABLE IF NOT EXISTS accreditation_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL UNIQUE,
    accreditation_type VARCHAR(50) NOT NULL,
    standard_number VARCHAR(50) NOT NULL,
    standard_component VARCHAR(100) NOT NULL,
    evidence_type VARCHAR(50) NOT NULL,
    compliance_status VARCHAR(20) NOT NULL,
    assessor_notes TEXT,
    verification_date TIMESTAMPTZ,
    next_review_date TIMESTAMPTZ,
    is_mandatory BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_accreditation_documents_document_id ON accreditation_documents(document_id);

-- ============================================
-- QUESTION BANK TABLES
-- ============================================

-- Questions table
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    subject_id UUID,
    topic_id UUID,
    grade_level_id UUID,
    difficulty VARCHAR(20) NOT NULL,
    bloom_level VARCHAR(20),
    points NUMERIC(5,2) DEFAULT 1.0,
    time_limit INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    explanation TEXT,
    hints JSONB,
    tags JSONB,
    author_id UUID NOT NULL,
    school_id UUID NOT NULL,
    is_public BOOLEAN DEFAULT false,
    allow_review BOOLEAN DEFAULT true,
    randomize_options BOOLEAN DEFAULT false,
    usage_count INTEGER DEFAULT 0,
    correct_rate NUMERIC(5,2),
    average_time NUMERIC(10,2),
    last_used_at TIMESTAMPTZ,
    effective_date TIMESTAMPTZ,
    expiry_date TIMESTAMPTZ,
    reference_material TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_questions_school_id ON questions(school_id);
CREATE INDEX idx_questions_author_id ON questions(author_id);
CREATE INDEX idx_questions_subject_id ON questions(subject_id);
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_questions_question_type ON questions(question_type);
CREATE INDEX idx_questions_status ON questions(status);

-- Question options table
CREATE TABLE IF NOT EXISTS question_options (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    "order" INTEGER DEFAULT 0,
    feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_question_options_question_id ON question_options(question_id);

-- Question answers table
CREATE TABLE IF NOT EXISTS question_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT true,
    "order" INTEGER DEFAULT 0,
    match_with TEXT,
    explanation TEXT,
    partial_credit NUMERIC(5,2),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_question_answers_question_id ON question_answers(question_id);

-- Question sets table
CREATE TABLE IF NOT EXISTS question_sets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    subject_id UUID,
    grade_level_id UUID,
    author_id UUID NOT NULL,
    school_id UUID NOT NULL,
    question_ids JSONB,
    total_questions INTEGER DEFAULT 0,
    total_points NUMERIC(10,2) DEFAULT 0,
    estimated_time INTEGER DEFAULT 0,
    difficulty VARCHAR(20),
    is_public BOOLEAN DEFAULT false,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_question_sets_school_id ON question_sets(school_id);
CREATE INDEX idx_question_sets_author_id ON question_sets(author_id);

-- Question difficulty calibration table
CREATE TABLE IF NOT EXISTS question_difficulty_calibration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL UNIQUE,
    original_difficulty VARCHAR(20),
    calibrated_difficulty VARCHAR(20),
    calibration_score NUMERIC(5,2),
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    average_time NUMERIC(10,2),
    discrimination_index NUMERIC(5,2),
    last_calibrated_at TIMESTAMPTZ,
    calibrated_by UUID,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Question usage analytics table
CREATE TABLE IF NOT EXISTS question_usage_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL,
    assessment_id UUID,
    usage_date TIMESTAMPTZ NOT NULL,
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    average_time NUMERIC(10,2),
    skip_count INTEGER DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_question_usage_analytics_question_id ON question_usage_analytics(question_id);
CREATE INDEX idx_question_usage_analytics_usage_date ON question_usage_analytics(usage_date DESC);

-- Question tags table
CREATE TABLE IF NOT EXISTS question_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(7),
    category VARCHAR(50),
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Question tag associations table
CREATE TABLE IF NOT EXISTS question_tag_associations (
    question_id UUID NOT NULL,
    tag_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID,
    PRIMARY KEY (question_id, tag_id)
);

-- Question categories table
CREATE TABLE IF NOT EXISTS question_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id UUID,
    sort_order INTEGER DEFAULT 0,
    icon VARCHAR(50),
    color VARCHAR(7),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Question reviews table
CREATE TABLE IF NOT EXISTS question_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL,
    reviewer_id UUID NOT NULL,
    rating INTEGER NOT NULL,
    comments TEXT,
    review_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_question_reviews_question_id ON question_reviews(question_id);

-- Question imports table
CREATE TABLE IF NOT EXISTS question_imports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    import_file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    import_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total_questions INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    error_log TEXT,
    imported_by UUID NOT NULL,
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Question exports table
CREATE TABLE IF NOT EXISTS question_exports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    export_name VARCHAR(255) NOT NULL,
    export_format VARCHAR(20) NOT NULL,
    filter_criteria JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    file_url VARCHAR(500),
    total_questions INTEGER DEFAULT 0,
    exported_by UUID NOT NULL,
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- ============================================
-- DAPODIK INTEGRATION TABLES
-- ============================================

-- Dapodik sync configuration table
CREATE TABLE IF NOT EXISTS dapodik_sync_config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school_id UUID NOT NULL UNIQUE,
    dapodik_school_id VARCHAR(50),
    api_key VARCHAR(255),
    api_endpoint VARCHAR(500),
    sync_frequency VARCHAR(20) DEFAULT 'DAILY',
    last_sync_at TIMESTAMPTZ,
    next_sync_at TIMESTAMPTZ,
    sync_status VARCHAR(20) DEFAULT 'IDLE',
    auto_sync BOOLEAN DEFAULT false,
    sync_modules JSONB, -- List of modules to sync
    error_log TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Dapodik sync history table
CREATE TABLE IF NOT EXISTS dapodik_sync_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school_id UUID NOT NULL,
    sync_type VARCHAR(50) NOT NULL,
    sync_status VARCHAR(20) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    records_processed INTEGER DEFAULT 0,
    records_success INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_details TEXT,
    sync_summary JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_dapodik_sync_history_school_id ON dapodik_sync_history(school_id);
CREATE INDEX idx_dapodik_sync_history_started_at ON dapodik_sync_history(started_at DESC);

-- Dapodik mapping table
CREATE TABLE IF NOT EXISTS dapodik_mapping (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school_id UUID NOT NULL,
    local_entity_type VARCHAR(50) NOT NULL,
    local_entity_id UUID NOT NULL,
    dapodik_entity_type VARCHAR(50) NOT NULL,
    dapodik_entity_id VARCHAR(100),
    mapping_status VARCHAR(20) DEFAULT 'ACTIVE',
    last_synced_at TIMESTAMPTZ,
    sync_conflicts TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_dapodik_mapping_school_id ON dapodik_mapping(school_id);
CREATE INDEX idx_dapodik_mapping_local_entity ON dapodik_mapping(local_entity_type, local_entity_id);
CREATE UNIQUE INDEX idx_dapodik_mapping_unique_entity ON dapodik_mapping(local_entity_type, local_entity_id, dapodik_entity_type);

-- National assessment standards table
CREATE TABLE IF NOT EXISTS national_assessment_standards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    standard_code VARCHAR(50) NOT NULL UNIQUE,
    standard_name VARCHAR(255) NOT NULL,
    standard_category VARCHAR(100),
    grade_level VARCHAR(50),
    subject VARCHAR(100),
    description TEXT,
    effective_date DATE,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_national_assessment_standards_grade_subject ON national_assessment_standards(grade_level, subject);

-- ============================================
-- ENHANCED NOTIFICATION SYSTEM TABLES
-- ============================================

-- Notification templates table
CREATE TABLE IF NOT EXISTS notification_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_name VARCHAR(100) NOT NULL UNIQUE,
    template_code VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    subject_template VARCHAR(255) NOT NULL,
    body_template TEXT NOT NULL,
    variables JSONB, -- List of variables used in template
    notification_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    is_active BOOLEAN DEFAULT true,
    default_channels JSONB, -- ['email', 'sms', 'push', 'in_app']
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_notification_templates_category ON notification_templates(category);
CREATE INDEX idx_notification_templates_notification_type ON notification_templates(notification_type);

-- Notification rules table
CREATE TABLE IF NOT EXISTS notification_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_name VARCHAR(255) NOT NULL UNIQUE,
    rule_code VARCHAR(50) NOT NULL UNIQUE,
    trigger_event VARCHAR(100) NOT NULL,
    trigger_conditions JSONB,
    template_id UUID NOT NULL,
    target_audience VARCHAR(50), -- ALL, SPECIFIC_USERS, ROLES, DEPARTMENTS
    target_criteria JSONB,
    channels JSONB,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    is_active BOOLEAN DEFAULT true,
    schedule_type VARCHAR(20), -- IMMEDIATE, SCHEDULED, RECURRING
    schedule_config JSONB,
    cooldown_period INTEGER, -- in minutes
    last_triggered_at TIMESTAMPTZ,
    trigger_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_notification_rules_trigger_event ON notification_rules(trigger_event);
CREATE INDEX idx_notification_rules_is_active ON notification_rules(is_active);

-- Notification delivery table
CREATE TABLE IF NOT EXISTS notification_delivery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    notification_id UUID NOT NULL,
    recipient_id UUID NOT NULL,
    channel VARCHAR(50) NOT NULL, -- EMAIL, SMS, PUSH, IN_APP
    delivery_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    failed_at TIMESTAMPTZ,
    failure_reason TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    external_id VARCHAR(255), -- External service ID (email service, SMS gateway, etc.)
    cost DECIMAL(10,4),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_notification_delivery_notification_id ON notification_delivery(notification_id);
CREATE INDEX idx_notification_delivery_recipient_id ON notification_delivery(recipient_id);
CREATE INDEX idx_notification_delivery_channel ON notification_delivery(channel);
CREATE INDEX idx_notification_delivery_status ON notification_delivery(delivery_status);

-- Update existing notifications table to support enhanced features
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS template_id UUID;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS rule_id UUID;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS delivery_config JSONB;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS scheduled_for TIMESTAMPTZ;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'MEDIUM';
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS retry_count INTEGER DEFAULT 0;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS max_retries INTEGER DEFAULT 3;

CREATE INDEX IF NOT EXISTS idx_notifications_template_id ON notifications(template_id);
CREATE INDEX IF NOT EXISTS idx_notifications_rule_id ON notifications(rule_id);
CREATE INDEX IF NOT EXISTS idx_notifications_scheduled_for ON notifications(scheduled_for);
CREATE INDEX IF NOT EXISTS idx_notifications_priority ON notifications(priority);

-- Notification preferences table
CREATE TABLE IF NOT EXISTS notification_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE,
    email_enabled BOOLEAN DEFAULT true,
    sms_enabled BOOLEAN DEFAULT false,
    push_enabled BOOLEAN DEFAULT true,
    in_app_enabled BOOLEAN DEFAULT true,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    quiet_days JSONB, -- Days when notifications should be suppressed
    category_preferences JSONB, -- Per-category preferences
    frequency_limits JSONB, -- Limits per category per time period
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_notification_preferences_user_id ON notification_preferences(user_id);

-- Notification statistics table
CREATE TABLE IF NOT EXISTS notification_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stat_date DATE NOT NULL,
    notification_type VARCHAR(50),
    channel VARCHAR(50),
    total_sent INTEGER DEFAULT 0,
    total_delivered INTEGER DEFAULT 0,
    total_read INTEGER DEFAULT 0,
    total_failed INTEGER DEFAULT 0,
    average_delivery_time NUMERIC(10,2),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

CREATE INDEX idx_notification_statistics_stat_date ON notification_statistics(stat_date DESC);
CREATE INDEX idx_notification_statistics_notification_type ON notification_statistics(notification_type);
CREATE INDEX idx_notification_statistics_channel ON notification_statistics(channel);

-- ============================================
-- COMMENTS AND DOCUMENTATION
-- ============================================

COMMENT ON TABLE documents IS 'Centralized document management for accreditation and general school documents';
COMMENT ON TABLE questions IS 'Question bank for assessment items with difficulty calibration';
COMMENT ON TABLE dapodik_sync_config IS 'Configuration for Dapodik integration and synchronization';
COMMENT ON TABLE notification_templates IS 'Templates for different types of notifications';
COMMENT ON TABLE notification_rules IS 'Rules for automatic notification triggering based on events';

-- ============================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================

-- Function to update updated_at timestamptz
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON questions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notification_templates_updated_at BEFORE UPDATE ON notification_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notification_rules_updated_at BEFORE UPDATE ON notification_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- INITIAL DATA SEEDING
-- ============================================

-- Insert default document categories
INSERT INTO document_categories (name, description, color, icon, sort_order) VALUES
('Umum', 'Dokumen umum sekolah', '#3B82F6', 'NiFile', 1),
('Akreditasi', 'Dokumen untuk akreditasi sekolah', '#EF4444', 'NiAward', 2),
('Kurikulum', 'Dokumen kurikulum dan pembelajaran', '#10B981', 'NiBook', 3),
('Asesmen', 'Dokumen penilaian dan evaluasi', '#F59E0B', 'NiClipboard', 4),
('Administrasi', 'Dokumen administratif', '#6366F1', 'NiSettings', 5),
('Keuangan', 'Dokumen keuangan', '#8B5CF6', 'NiDollar', 6),
('SDM', 'Dokumen sumber daya manusia', '#EC4899', 'NiUsers', 7),
('Hukum', 'Dokumen hukum dan legalitas', '#14B8A6', 'NiScale', 8)
ON CONFLICT (name) DO NOTHING;

-- Insert default question categories
INSERT INTO question_categories (name, description, color, icon, sort_order) VALUES
('Pengetahuan', 'Soal pengetahuan dasar', '#3B82F6', 'NiBrain', 1),
('Pemahaman', 'Soal pemahaman konsep', '#10B981', 'NiLightbulb', 2),
('Penerapan', 'Soal penerapan konsep', '#F59E0B', 'NiCpu', 3),
('Analisis', 'Soal analisis', '#EF4444', 'NiSearch', 4),
('Evaluasi', 'Soal evaluasi', '#8B5CF6', 'NiStar', 5),
('Kreatifitas', 'Soal kreatifitas', '#EC4899', 'NiPalette', 6)
ON CONFLICT (name) DO NOTHING;

-- Insert default notification templates
INSERT INTO notification_templates (template_name, template_code, category, subject_template, body_template, notification_type, priority, default_channels) VALUES
('Pengumuman Baru', 'NEW_ANNOUNCEMENT', 'ANNOUNCEMENT', 'Pengumuman Baru: {{title}}', '{{content}}', 'ANNOUNCEMENT', 'HIGH', '["in_app", "push", "email"]'::jsonb),
('Tugas Baru', 'NEW_ASSIGNMENT', 'ACADEMIC', 'Tugas Baru: {{title}}', 'Anda memiliki tugas baru: {{title}}. Tenggat: {{due_date}}', 'ASSIGNMENT', 'MEDIUM', '["in_app", "push"]'::jsonb),
('Nilai Rapor', 'GRADE_PUBLISHED', 'ACADEMIC', 'Nilai Rapor Tersedia', 'Nilai rapor untuk {{term}} sudah tersedia. Silakan cek di aplikasi.', 'GRADE', 'HIGH', '["in_app", "push", "sms"]'::jsonb),
('Absensi', 'ABSENCE_ALERT', 'ACADEMIC', 'Peringatan Absensi', 'Siswa {{student_name}} tidak hadir {{absence_count}} hari berturut-turut.', 'ATTENDANCE', 'MEDIUM', '["in_app", "push", "sms"]'::jsonb),
('Sistem', 'SYSTEM_NOTIFICATION', 'SYSTEM', '{{subject}}', '{{message}}', 'SYSTEM', 'LOW', '["in_app"]'::jsonb)
ON CONFLICT (template_code) DO NOTHING;

-- ============================================
-- PHASE 4 IMPLEMENTATION COMPLETE
-- ============================================

-- This migration includes:
-- 1. Document Repository (9 tables) - Complete document management with versioning, approval workflow, accreditation support
-- 2. Question Bank System (12 tables) - Assessment item management with difficulty calibration and analytics
-- 3. Dapodik Integration (4 tables) - National education system integration and mapping
-- 4. Enhanced Notification System (5 tables + updates) - Templates, rules, delivery tracking, preferences, statistics

-- Total: 30 new tables, 20+ indexes, automatic triggers, initial data seeding