-- ============================================================
-- Migration: 001_init_normalized_schema
-- Description: Initialize complete normalized database schema from scratch
--              This migration creates all tables with normalized structure
--              including constraints, indexes, and seed data
-- Author: Database Team
-- Created: 2026-05-28
-- Related Issues: Database normalization initiative
-- Risk Level: LOW (Fresh schema creation)
-- Downtime Required: NO
-- Rollback Procedure: Drop all tables and recreate from backup
-- ============================================================

-- ============================================================
-- SECTION 1: Authentication Domain Tables
-- ============================================================

CREATE TABLE auth_user (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teacher_id UUID,
    student_id UUID,
    full_name TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
    account_non_expired BOOLEAN DEFAULT true,
    account_non_locked BOOLEAN DEFAULT true,
    credentials_non_expired BOOLEAN DEFAULT true,
    is_enabled BOOLEAN DEFAULT true,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    theme_color TEXT DEFAULT 'theme-purple',
    theme_mode TEXT DEFAULT 'system',
    content_type TEXT DEFAULT 'boxed',
    left_menu_type TEXT DEFAULT 'comfort',
    two_factor_enabled BOOLEAN DEFAULT false,
    totp_secret VARCHAR(100),
    email_notifications BOOLEAN DEFAULT true,
    push_notifications BOOLEAN DEFAULT true
);

CREATE TABLE auth_role (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    role_name TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auth_user_role (
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE auth_refresh_token (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id TEXT,
    token TEXT,
    expired_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auth_password_reset_token (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id TEXT,
    token TEXT,
    expired_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auth_user_session (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id UUID NOT NULL,
    user_agent TEXT NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    is_revoked BOOLEAN DEFAULT false,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auth_permission (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    permission_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auth_role_permission (
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    PRIMARY KEY (role_id, permission_id)
);

-- ============================================================
-- SECTION 2: Master Data Domain Tables (Normalized)
-- ============================================================

-- School tables (normalized)
CREATE TABLE master_school (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    npsn VARCHAR(20) UNIQUE,
    school_name VARCHAR(255) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(100),
    status VARCHAR(20),
    operating_hours VARCHAR(255),
    bos_status VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE school_location (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    district VARCHAR(100),
    regency VARCHAR(100),
    province VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Indonesia',
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    full_address TEXT,
    postal_code VARCHAR(10),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE school_statistics (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    total_students BIGINT,
    male_students BIGINT,
    female_students BIGINT,
    total_teachers BIGINT,
    male_teachers BIGINT,
    female_teachers BIGINT,
    total_staff BIGINT,
    rombel_count BIGINT,
    student_ratio VARCHAR(50),
    student_religion VARCHAR(100),
    report_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE school_infrastructure (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    electricity_capacity BIGINT,
    signal_status VARCHAR(50),
    water_source VARCHAR(100),
    internet_access VARCHAR(50),
    classroom_count BIGINT,
    classroom_good_count BIGINT,
    classroom_damaged_count BIGINT,
    library_count BIGINT,
    lab_count BIGINT,
    toilet_student_count BIGINT,
    toilet_teacher_count BIGINT,
    infrastructure_summary TEXT,
    report_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE school_academic (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    curriculum VARCHAR(100),
    accreditation VARCHAR(50),
    education_form VARCHAR(100),
    graduation_data VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE school_administration (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    principal_name VARCHAR(255),
    operator_name VARCHAR(255),
    vision TEXT,
    vision_meaning TEXT,
    mission TEXT,
    goal TEXT,
    sync_system VARCHAR(100),
    sync_compliance VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Academic structure tables
CREATE TABLE master_academic_year (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    year_name VARCHAR(20) NOT NULL,
    semester VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7(),
    CONSTRAINT unique_year_semester UNIQUE (year_name, semester)
);

CREATE TABLE master_phase (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    phase_code TEXT UNIQUE,
    phase_name TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_grade (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    phase_id UUID NOT NULL REFERENCES master_phase(id) ON DELETE CASCADE,
    grade_level SMALLINT NOT NULL,
    grade_name VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_classroom (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES master_academic_year(id) ON DELETE CASCADE,
    grade_id UUID NOT NULL REFERENCES master_grade(id) ON DELETE CASCADE,
    classroom_name VARCHAR(50) NOT NULL,
    homeroom_teacher_id UUID,
    class_characteristics TEXT,
    phase_id UUID NOT NULL REFERENCES master_phase(id) ON DELETE CASCADE,
    max_quota SMALLINT DEFAULT 28,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Teacher tables (normalized)
CREATE TABLE master_teacher (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    gender CHAR(1),
    birth_place VARCHAR(100),
    birth_date DATE,
    nik VARCHAR(20),
    nuptk VARCHAR(20),
    niynigk VARCHAR(30),
    religion VARCHAR(20),
    nationality VARCHAR(50) DEFAULT 'WNI',
    photo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE teacher_contact (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teacher_id UUID NOT NULL REFERENCES master_teacher(id) ON DELETE CASCADE,
    full_address TEXT,
    hamlet VARCHAR(100),
    rtrw VARCHAR(10),
    village VARCHAR(100),
    district VARCHAR(100),
    regency VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(10),
    phone VARCHAR(30),
    email VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE teacher_employment (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teacher_id UUID NOT NULL REFERENCES master_teacher(id) ON DELETE CASCADE,
    nip VARCHAR(30),
    employment_status VARCHAR(20),
    start_teaching_date DATE,
    appointment_decree VARCHAR(100),
    salary_source VARCHAR(50),
    teaching_subject VARCHAR(255),
    additional_position VARCHAR(100),
    teaching_hours SMALLINT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE teacher_education (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teacher_id UUID NOT NULL REFERENCES master_teacher(id) ON DELETE CASCADE,
    last_education VARCHAR(20),
    major VARCHAR(100),
    university_name VARCHAR(255),
    graduation_year SMALLINT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE teacher_certification (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teacher_id UUID NOT NULL REFERENCES master_teacher(id) ON DELETE CASCADE,
    is_certified BOOLEAN DEFAULT false,
    certificate_number VARCHAR(50),
    certification_date DATE,
    certification_level VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE teacher_preference (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teacher_id UUID NOT NULL REFERENCES master_teacher(id) ON DELETE CASCADE,
    teaching_preference TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Student tables (normalized)
CREATE TABLE master_student (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id UUID NOT NULL REFERENCES master_school(id) ON DELETE CASCADE,
    nik VARCHAR(20) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    gender CHAR(1),
    birth_place VARCHAR(100),
    birth_date DATE,
    religion VARCHAR(20),
    nationality VARCHAR(50) DEFAULT 'WNI',
    photo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_family (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    child_order SMALLINT DEFAULT 1,
    siblings SMALLINT DEFAULT 0,
    family_card_number VARCHAR(20),
    birth_certificate VARCHAR(50),
    k_ip_number VARCHAR(30),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_contact (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    full_address TEXT,
    rtrw VARCHAR(10),
    village VARCHAR(100),
    district VARCHAR(100),
    regency VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(10),
    coordinates VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_academic (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    nis VARCHAR(20),
    nisn VARCHAR(20),
    enrollment_year SMALLINT,
    curriculum VARCHAR(50),
    student_status VARCHAR(20) DEFAULT 'Aktif',
    entry_path VARCHAR(50),
    previous_school VARCHAR(255),
    exam_number VARCHAR(30),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_medical (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    blood_type VARCHAR(5),
    height NUMERIC(5,2) DEFAULT 0,
    weight NUMERIC(5,2) DEFAULT 0,
    medical_history TEXT,
    disability VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_documents (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    photo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_student_parent (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    parent_type VARCHAR(10) NOT NULL,
    full_name VARCHAR(255),
    nik VARCHAR(20),
    education VARCHAR(20),
    occupation VARCHAR(100),
    income BIGINT DEFAULT 0,
    phone VARCHAR(30),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Subject tables (normalized)
CREATE TABLE master_subject (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    subject_code VARCHAR(20) NOT NULL,
    subject_name VARCHAR(255) NOT NULL,
    rational TEXT,
    goals TEXT,
    characteristics TEXT,
    is_active BOOLEAN DEFAULT true,
    level TEXT,
    abbreviation TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_subject_characteristic (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    subject_id UUID REFERENCES master_subject(id) ON DELETE CASCADE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_subject_element (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    subject_id UUID REFERENCES master_subject(id) ON DELETE CASCADE,
    point_id UUID,
    sub_code TEXT,
    detail_text TEXT,
    sequence_no BIGINT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_subject_local_context (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    subject_id UUID NOT NULL REFERENCES master_subject(id) ON DELETE CASCADE,
    local_context_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7(),
    CONSTRAINT unique_subject_context UNIQUE (subject_id, local_context_id)
);

-- Local context tables
CREATE TABLE master_local_context (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    school_id TEXT,
    category_id UUID,
    title TEXT,
    description TEXT,
    location TEXT,
    scope_type TEXT,
    context_code VARCHAR(50),
    context_name VARCHAR(100),
    context_category VARCHAR(50),
    examples TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_local_context_category (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    category_code TEXT UNIQUE,
    category_name TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Profile dimension tables
CREATE TABLE master_profile_dimension (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    dimension_code TEXT UNIQUE NOT NULL,
    dimension_name TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 3: Curriculum Domain Tables
-- ============================================================

CREATE TABLE cur_cp_detail (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    learning_outcome_id UUID REFERENCES cur_learning_outcome(id) ON DELETE CASCADE,
    element_id UUID REFERENCES master_subject_element(id) ON DELETE SET NULL,
    sub_code TEXT,
    detail_text TEXT,
    sequence_no BIGINT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE cur_learning_objective (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    learning_outcome_id UUID NOT NULL REFERENCES cur_learning_outcome(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE cur_learning_outcome (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    phase_id UUID REFERENCES master_phase(id) ON DELETE SET NULL,
    subject_id UUID REFERENCES master_subject(id) ON DELETE SET NULL,
    cp_code TEXT,
    outcome_text TEXT,
    year_sk TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE dl_assessment_level (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    level_code TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    pisa_level TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE dl_cognitive_stage (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    stage_order INTEGER UNIQUE NOT NULL,
    stage_name TEXT NOT NULL,
    operational_verbs TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE dl_design_element (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    design_element_name TEXT UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 4: Transaction Domain Tables (Partial - continue in next section)
-- ============================================================

CREATE TABLE trx_assessment (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    teaching_assignment_id UUID NOT NULL,
    assessment_name VARCHAR(100) NOT NULL,
    assessment_type VARCHAR(20) NOT NULL,
    age_appropriate_type VARCHAR(30),
    assessment_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_assessment_score (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    assessment_id UUID NOT NULL REFERENCES trx_assessment(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    score NUMERIC(5,2) DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_rubric (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    name TEXT NOT NULL,
    description TEXT,
    subject_id UUID REFERENCES master_subject(id) ON DELETE SET NULL,
    phase_id UUID REFERENCES master_phase(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_rubric_criteria (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    rubric_id UUID NOT NULL REFERENCES trx_rubric(id) ON DELETE CASCADE,
    criteria_name TEXT NOT NULL,
    description TEXT,
    max_score NUMERIC(5,2) DEFAULT 100,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_rubric_score (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    rubric_criteria_id UUID NOT NULL REFERENCES trx_rubric_criteria(id) ON DELETE CASCADE,
    assessment_score_id UUID NOT NULL REFERENCES trx_assessment_score(id) ON DELETE CASCADE,
    score NUMERIC(5,2) DEFAULT 0,
    feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 5: System Tables
-- ============================================================

CREATE TABLE sys_automation_queue (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    task_type VARCHAR(50) NOT NULL,
    reference_id UUID NOT NULL,
    user_id UUID NOT NULL,
    status VARCHAR(20) DEFAULT 'ANTREAN' NOT NULL,
    error_log TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sys_server_telemetry (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    cpu_usage_percent NUMERIC(5,2) NOT NULL,
    ram_usage_percent NUMERIC(5,2) NOT NULL,
    storage_free_gb NUMERIC(10,2) NOT NULL,
    server_temperature_c NUMERIC(4,1),
    disk_io_read_mb_s NUMERIC(10,2),
    disk_io_write_mb_s NUMERIC(10,2),
    network_in_mbps NUMERIC(10,2),
    network_out_mbps NUMERIC(10,2),
    active_connections BIGINT,
    engine_status VARCHAR(20) DEFAULT 'RUNNING' NOT NULL,
    logged_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100),
    ip_address VARCHAR(45),
    impersonator_id UUID,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id UUID NOT NULL,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    data JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    action_url VARCHAR(500),
    action_text VARCHAR(50),
    template_id UUID,
    rule_id UUID,
    delivery_config JSONB,
    scheduled_for TIMESTAMPTZ,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    sent_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    source_id UUID,
    source_type VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 6: Indexes
-- ============================================================

-- Auth indexes
CREATE INDEX idx_auth_user_teacher ON auth_user(teacher_id);
CREATE INDEX idx_auth_user_student ON auth_user(student_id);
CREATE INDEX idx_auth_user_username ON auth_user(username);
CREATE INDEX idx_auth_user_email ON auth_user(email);
CREATE INDEX idx_user_session_user ON auth_user_session(user_id);
CREATE INDEX idx_user_session_revoked ON auth_user_session(is_revoked);
CREATE INDEX idx_role_permission_role ON auth_role_permission(role_id);
CREATE INDEX idx_role_permission_permission ON auth_role_permission(permission_id);

-- School indexes
CREATE INDEX idx_school_npsn ON master_school(npsn);
CREATE INDEX idx_school_status ON master_school(status);
CREATE INDEX idx_school_location_school_id ON school_location(school_id);
CREATE INDEX idx_school_location_province ON school_location(province);
CREATE INDEX idx_school_statistics_school_id ON school_statistics(school_id);
CREATE INDEX idx_school_infrastructure_school_id ON school_infrastructure(school_id);
CREATE INDEX idx_school_academic_school_id ON school_academic(school_id);
CREATE INDEX idx_school_administration_school_id ON school_administration(school_id);

-- Academic indexes
CREATE INDEX idx_academic_year_active ON master_academic_year(is_active);
CREATE INDEX idx_classroom_school ON master_classroom(school_id);
CREATE INDEX idx_classroom_academic_year ON master_classroom(academic_year_id);
CREATE INDEX idx_classroom_grade ON master_classroom(grade_id);
CREATE INDEX idx_classroom_phase ON master_classroom(phase_id);
CREATE INDEX idx_classroom_teacher ON master_classroom(homeroom_teacher_id);

-- Teacher indexes
CREATE INDEX idx_teacher_school ON master_teacher(school_id);
CREATE INDEX idx_teacher_nuptk ON master_teacher(nuptk);
CREATE INDEX idx_teacher_nik ON master_teacher(nik);
CREATE INDEX idx_teacher_active ON master_teacher(is_active);
CREATE INDEX idx_teacher_contact_teacher_id ON teacher_contact(teacher_id);
CREATE INDEX idx_teacher_employment_teacher_id ON teacher_employment(teacher_id);
CREATE INDEX idx_teacher_education_teacher_id ON teacher_education(teacher_id);
CREATE INDEX idx_teacher_certification_teacher_id ON teacher_certification(teacher_id);
CREATE INDEX idx_teacher_preference_teacher_id ON teacher_preference(teacher_id);

-- Student indexes
CREATE INDEX idx_student_school ON master_student(school_id);
CREATE INDEX idx_student_nik ON master_student(nik);
CREATE INDEX idx_student_nisn ON student_academic(nisn);
CREATE INDEX idx_student_status ON student_academic(student_status);
CREATE INDEX idx_student_family_student_id ON student_family(student_id);
CREATE INDEX idx_student_contact_student_id ON student_contact(student_id);
CREATE INDEX idx_student_academic_student_id ON student_academic(student_id);
CREATE INDEX idx_student_medical_student_id ON student_medical(student_id);
CREATE INDEX idx_student_documents_student_id ON student_documents(student_id);

-- Subject indexes
CREATE INDEX idx_subject_code ON master_subject(subject_code);
CREATE INDEX idx_subject_active ON master_subject(is_active);
CREATE INDEX idx_subject_element_subject ON master_subject_element(subject_id);
CREATE INDEX idx_subject_local_context_subject_id ON master_subject_local_context(subject_id);
CREATE INDEX idx_subject_local_context_context_id ON master_subject_local_context(local_context_id);

-- System indexes
CREATE INDEX idx_sys_automation_queue_status ON sys_automation_queue(status);
CREATE INDEX idx_sys_automation_queue_user ON sys_automation_queue(user_id);
CREATE INDEX idx_sys_automation_queue_task_type ON sys_automation_queue(task_type);
CREATE INDEX idx_sys_automation_queue_created_at ON sys_automation_queue(created_at);
CREATE INDEX idx_sys_server_telemetry_logged_at ON sys_server_telemetry(logged_at);
CREATE INDEX idx_sys_server_telemetry_engine_status ON sys_server_telemetry(engine_status);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity);
CREATE INDEX idx_audit_logs_impersonator ON audit_logs(impersonator_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_priority ON notifications(priority);
CREATE INDEX idx_notifications_scheduled_for ON notifications(scheduled_for);
CREATE INDEX idx_notifications_sent_at ON notifications(sent_at);
CREATE INDEX idx_notifications_source ON notifications(source_type, source_id);
CREATE INDEX idx_notifications_expires_at ON notifications(expires_at);

-- ============================================================
-- SECTION 7: Comments
-- ============================================================

COMMENT ON TABLE master_school IS 'Normalized master school table - basic info only';
COMMENT ON TABLE school_location IS 'School location data (normalized from master_school)';
COMMENT ON TABLE school_statistics IS 'School enrollment statistics (normalized from master_school)';
COMMENT ON TABLE school_infrastructure IS 'School infrastructure data (normalized from master_school)';
COMMENT ON TABLE school_academic IS 'School academic programs (normalized from master_school)';
COMMENT ON TABLE school_administration IS 'School administrative information (normalized from master_school)';

COMMENT ON TABLE master_teacher IS 'Normalized master teacher table - basic info only';
COMMENT ON TABLE teacher_contact IS 'Teacher contact information (normalized from master_teacher)';
COMMENT ON TABLE teacher_employment IS 'Teacher employment details (normalized from master_teacher)';
COMMENT ON TABLE teacher_education IS 'Teacher education history (normalized from master_teacher)';
COMMENT ON TABLE teacher_certification IS 'Teacher certification details (normalized from master_teacher)';
COMMENT ON TABLE teacher_preference IS 'Teacher teaching preferences (normalized from master_teacher)';

COMMENT ON TABLE master_student IS 'Normalized master student table - basic info only';
COMMENT ON TABLE student_family IS 'Student family information (normalized from master_student)';
COMMENT ON TABLE student_contact IS 'Student contact information (normalized from master_student)';
COMMENT ON TABLE student_academic IS 'Student academic enrollment (normalized from master_student)';
COMMENT ON TABLE student_medical IS 'Student medical records (normalized from master_student)';
COMMENT ON TABLE student_documents IS 'Student document tracking (normalized from master_student)';

COMMENT ON TABLE master_subject_local_context IS 'Junction table for subject-local context relationships (normalized from ARRAY)';

-- ============================================================
-- SECTION 8: Additional Transaction Domain Tables
-- ============================================================

CREATE TABLE trx_academic_score (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    question_id UUID NOT NULL,
    assessment_type VARCHAR(20) NOT NULL,
    score NUMERIC(5,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_assessment_p5 (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    project_id UUID NOT NULL,
    dimension_id UUID NOT NULL REFERENCES master_profile_dimension(id) ON DELETE CASCADE,
    capaian VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 9: Phase Feature Tables
-- ============================================================

-- AI Learning Intelligence
CREATE TABLE ai_learning_pattern (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    pattern_type TEXT NOT NULL,
    pattern_data JSONB,
    confidence_score NUMERIC(5,2),
    discovered_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE ai_adaptive_learning (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES master_subject(id) ON DELETE SET NULL,
    adaptation_strategy TEXT,
    performance_metrics JSONB,
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE ai_character_analysis (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    analysis_date DATE NOT NULL,
    character_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE ai_character_analysis_traits (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES ai_character_analysis(id) ON DELETE CASCADE,
    trait_name TEXT NOT NULL,
    trait_value NUMERIC,
    trait_description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE ai_character_analysis_strengths (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES ai_character_analysis(id) ON DELETE CASCADE,
    strength TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE ai_character_analysis_improvements (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES ai_character_analysis(id) ON DELETE CASCADE,
    area TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Portfolio System
CREATE TABLE trx_portfolio (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    portfolio_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    period_start DATE,
    period_end DATE,
    status TEXT DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_portfolio_item (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    portfolio_id UUID NOT NULL REFERENCES trx_portfolio(id) ON DELETE CASCADE,
    item_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    file_path TEXT,
    achievement_date DATE,
    sequence_no BIGINT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Communication System
CREATE TABLE trx_communication (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    sender_id UUID NOT NULL,
    recipient_id UUID NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    message_type TEXT DEFAULT 'MESSAGE',
    status TEXT DEFAULT 'SENT',
    sent_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_communication_attachment (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    communication_id UUID NOT NULL REFERENCES trx_communication(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT,
    mime_type TEXT,
    uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Offline Support
CREATE TABLE sys_offline_queue (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id UUID NOT NULL,
    operation_type TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_id UUID,
    payload JSONB,
    status TEXT DEFAULT 'PENDING',
    retry_count BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ,
    error_message TEXT
);

CREATE TABLE sys_offline_sync_log (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    user_id UUID NOT NULL,
    sync_start TIMESTAMPTZ,
    sync_end TIMESTAMPTZ,
    records_processed BIGINT DEFAULT 0,
    records_failed BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Survey System
CREATE TABLE trx_survey (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    survey_name TEXT NOT NULL,
    survey_type TEXT NOT NULL,
    target_audience TEXT,
    description TEXT,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_survey_question (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    survey_id UUID NOT NULL REFERENCES trx_survey(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    sequence_no BIGINT DEFAULT 1,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_survey_question_options (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    question_id UUID NOT NULL REFERENCES trx_survey_question(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    option_value TEXT,
    option_order SMALLINT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_survey_response (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    survey_id UUID NOT NULL REFERENCES trx_survey(id) ON DELETE CASCADE,
    respondent_id UUID NOT NULL,
    submitted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_survey_answer (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    response_id UUID NOT NULL REFERENCES trx_survey_response(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES trx_survey_question(id) ON DELETE CASCADE,
    answer_text TEXT,
    answer_value JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- FGD System
CREATE TABLE trx_fgd_session (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    session_name TEXT NOT NULL,
    session_date DATE NOT NULL,
    location TEXT,
    facilitator_id UUID,
    participants TEXT,
    objectives TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_fgd_participant (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    session_id UUID NOT NULL REFERENCES trx_fgd_session(id) ON DELETE CASCADE,
    participant_id UUID NOT NULL,
    role TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_fgd_note (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    session_id UUID NOT NULL REFERENCES trx_fgd_session(id) ON DELETE CASCADE,
    note_text TEXT NOT NULL,
    note_type TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Analysis Tools
CREATE TABLE trx_swot_analysis (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    analysis_date DATE NOT NULL,
    analysis_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_swot_strengths (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES trx_swot_analysis(id) ON DELETE CASCADE,
    strength TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_swot_weaknesses (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES trx_swot_analysis(id) ON DELETE CASCADE,
    weakness TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_swot_opportunities (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES trx_swot_analysis(id) ON DELETE CASCADE,
    opportunity TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_swot_threats (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES trx_swot_analysis(id) ON DELETE CASCADE,
    threat TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_root_cause_analysis (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    issue_description TEXT NOT NULL,
    analysis_date DATE NOT NULL,
    root_cause TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_root_cause_factors (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES trx_root_cause_analysis(id) ON DELETE CASCADE,
    factor TEXT NOT NULL,
    factor_category VARCHAR(100),
    severity VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_root_cause_actions (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    analysis_id UUID NOT NULL REFERENCES trx_root_cause_analysis(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    action_priority VARCHAR(50),
    action_owner VARCHAR(255),
    due_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 10: Missing Model Tables
-- ============================================================

-- Assessment Tables
CREATE TABLE master_sd_assessment_criteria (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    assessment_type VARCHAR(50) NOT NULL,
    phase_id UUID REFERENCES master_phase(id) ON DELETE SET NULL,
    criteria_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    rubric_elements JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Differentiated Instruction Tables
CREATE TABLE master_di_strategy (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    strategy_code VARCHAR(20) UNIQUE NOT NULL,
    strategy_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    applicability TEXT,
    examples TEXT,
    target_group VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_module_differentiation (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    module_id UUID NOT NULL,
    strategy_id UUID NOT NULL REFERENCES master_di_strategy(id) ON DELETE CASCADE,
    target_students TEXT,
    modifications TEXT,
    resources TEXT,
    assessment_type VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE trx_student_di_need (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES master_subject(id) ON DELETE SET NULL,
    need_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT,
    assessment_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_di_strategies (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    di_need_id UUID NOT NULL REFERENCES trx_student_di_need(id) ON DELETE CASCADE,
    strategy TEXT NOT NULL,
    strategy_category VARCHAR(100),
    implementation_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Daily Attendance
CREATE TABLE trx_daily_attendance (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    classroom_id UUID NOT NULL REFERENCES master_classroom(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Master Tables
CREATE TABLE master_olah_aspect (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    aspect_code TEXT UNIQUE NOT NULL,
    aspect_name TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_learning_principle (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    principle_code TEXT UNIQUE NOT NULL,
    principle_name TEXT NOT NULL,
    description TEXT,
    key_characteristics TEXT,
    implementation_examples TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_reading_level (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    level_code TEXT UNIQUE NOT NULL,
    level_name TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE master_play_activity_type (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    activity_type_code TEXT UNIQUE NOT NULL,
    activity_type_name TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Local Context Utilization
CREATE TABLE trx_local_context_utilization (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    local_context_id UUID NOT NULL,
    subject_id UUID REFERENCES master_subject(id) ON DELETE SET NULL,
    teaching_module_id UUID,
    utilization_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Document Repository
CREATE TABLE doc_document (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    document_name TEXT NOT NULL,
    document_type TEXT NOT NULL,
    file_path TEXT,
    description TEXT,
    subject_id UUID REFERENCES master_subject(id) ON DELETE SET NULL,
    phase_id UUID REFERENCES master_phase(id) ON DELETE SET NULL,
    uploaded_by UUID NOT NULL,
    uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE doc_document_tags (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    document_id UUID NOT NULL REFERENCES doc_document(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- Teaching Module
CREATE TABLE trx_teaching_module (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    subject_id UUID NOT NULL REFERENCES master_subject(id) ON DELETE CASCADE,
    phase_id UUID NOT NULL REFERENCES master_phase(id) ON DELETE CASCADE,
    module_name TEXT NOT NULL,
    module_code TEXT,
    description TEXT,
    duration_hours NUMERIC(5,2),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE teaching_module_local_context (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    module_id UUID NOT NULL REFERENCES trx_teaching_module(id) ON DELETE CASCADE,
    local_context_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7(),
    CONSTRAINT unique_module_context UNIQUE (module_id, local_context_id)
);

-- Student Profile Extension
CREATE TABLE trx_student_profile_ext (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
    profile_date DATE NOT NULL,
    profile_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

CREATE TABLE student_profile_attributes (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    profile_id UUID NOT NULL REFERENCES trx_student_profile_ext(id) ON DELETE CASCADE,
    attribute_name TEXT NOT NULL,
    attribute_value TEXT,
    attribute_category VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID DEFAULT uuidv7(),
    updated_by UUID DEFAULT uuidv7(),
    deleted_by UUID DEFAULT uuidv7()
);

-- ============================================================
-- SECTION 11: Additional Indexes
-- ============================================================

-- AI indexes
CREATE INDEX idx_ai_learning_pattern_student ON ai_learning_pattern(student_id);
CREATE INDEX idx_ai_learning_pattern_type ON ai_learning_pattern(pattern_type);
CREATE INDEX idx_ai_adaptive_learning_student ON ai_adaptive_learning(student_id);
CREATE INDEX idx_ai_adaptive_learning_subject ON ai_adaptive_learning(subject_id);
CREATE INDEX idx_ai_character_analysis_student ON ai_character_analysis(student_id);
CREATE INDEX idx_ai_character_analysis_traits_analysis_id ON ai_character_analysis_traits(analysis_id);
CREATE INDEX idx_ai_character_analysis_traits_name ON ai_character_analysis_traits(trait_name);
CREATE INDEX idx_ai_character_analysis_strengths_analysis_id ON ai_character_analysis_strengths(analysis_id);
CREATE INDEX idx_ai_character_analysis_improvements_analysis_id ON ai_character_analysis_improvements(analysis_id);

-- Portfolio indexes
CREATE INDEX idx_portfolio_student ON trx_portfolio(student_id);
CREATE INDEX idx_portfolio_status ON trx_portfolio(status);
CREATE INDEX idx_portfolio_item_portfolio ON trx_portfolio_item(portfolio_id);

-- Communication indexes
CREATE INDEX idx_communication_sender ON trx_communication(sender_id);
CREATE INDEX idx_communication_recipient ON trx_communication(recipient_id);
CREATE INDEX idx_communication_status ON trx_communication(status);
CREATE INDEX idx_communication_attachment_communication ON trx_communication_attachment(communication_id);

-- Offline indexes
CREATE INDEX idx_offline_queue_user ON sys_offline_queue(user_id);
CREATE INDEX idx_offline_queue_status ON sys_offline_queue(status);
CREATE INDEX idx_offline_sync_log_user ON sys_offline_sync_log(user_id);

-- Survey indexes
CREATE INDEX idx_survey_active ON trx_survey(is_active);
CREATE INDEX idx_survey_question_survey ON trx_survey_question(survey_id);
CREATE INDEX idx_survey_question_options_question ON trx_survey_question_options(question_id);
CREATE INDEX idx_survey_response_survey ON trx_survey_response(survey_id);
CREATE INDEX idx_survey_response_respondent ON trx_survey_response(respondent_id);
CREATE INDEX idx_survey_answer_response ON trx_survey_answer(response_id);
CREATE INDEX idx_survey_answer_question ON trx_survey_answer(question_id);

-- FGD indexes
CREATE INDEX idx_fgd_session_date ON trx_fgd_session(session_date);
CREATE INDEX idx_fgd_participant_session ON trx_fgd_participant(session_id);
CREATE INDEX idx_fgd_note_session ON trx_fgd_note(session_id);

-- Analysis indexes
CREATE INDEX idx_swot_analysis_entity ON trx_swot_analysis(entity_type, entity_id);
CREATE INDEX idx_swot_strengths_analysis_id ON trx_swot_strengths(analysis_id);
CREATE INDEX idx_swot_weaknesses_analysis_id ON trx_swot_weaknesses(analysis_id);
CREATE INDEX idx_swot_opportunities_analysis_id ON trx_swot_opportunities(analysis_id);
CREATE INDEX idx_swot_threats_analysis_id ON trx_swot_threats(analysis_id);
CREATE INDEX idx_root_cause_analysis_entity ON trx_root_cause_analysis(entity_type, entity_id);
CREATE INDEX idx_root_cause_factors_analysis_id ON trx_root_cause_factors(analysis_id);
CREATE INDEX idx_root_cause_actions_analysis_id ON trx_root_cause_actions(analysis_id);

-- DI indexes
CREATE INDEX idx_di_strategy_code ON master_di_strategy(strategy_code);
CREATE INDEX idx_di_strategy_active ON master_di_strategy(is_active);
CREATE INDEX idx_module_differentiation_module ON trx_module_differentiation(module_id);
CREATE INDEX idx_module_differentiation_strategy ON trx_module_differentiation(strategy_id);
CREATE INDEX idx_student_di_need_student ON trx_student_di_need(student_id);
CREATE INDEX idx_student_di_need_subject ON trx_student_di_need(subject_id);
CREATE INDEX idx_student_di_need_active ON trx_student_di_need(is_active);
CREATE INDEX idx_di_strategies_di_need_id ON student_di_strategies(di_need_id);
CREATE INDEX idx_di_strategies_category ON student_di_strategies(strategy_category);

-- Document indexes
CREATE INDEX idx_document_type ON doc_document(document_type);
CREATE INDEX idx_document_subject ON doc_document(subject_id);
CREATE INDEX idx_document_phase ON doc_document(phase_id);
CREATE INDEX idx_document_tags_document ON doc_document_tags(document_id);
CREATE INDEX idx_document_tags_tag ON doc_document_tags(tag);

-- Teaching module indexes
CREATE INDEX idx_teaching_module_subject ON trx_teaching_module(subject_id);
CREATE INDEX idx_teaching_module_phase ON trx_teaching_module(phase_id);
CREATE INDEX idx_module_local_context_module_id ON teaching_module_local_context(module_id);
CREATE INDEX idx_module_local_context_context_id ON teaching_module_local_context(local_context_id);

-- Student profile indexes
CREATE INDEX idx_student_profile_ext_student ON trx_student_profile_ext(student_id);
CREATE INDEX idx_student_profile_ext_date ON trx_student_profile_ext(profile_date);
CREATE INDEX idx_profile_attributes_profile_id ON student_profile_attributes(profile_id);
CREATE INDEX idx_profile_attributes_name ON student_profile_attributes(attribute_name);

-- ============================================================
-- SECTION 12: Seed Reference Data
-- ============================================================

-- Seed default roles
INSERT INTO auth_role (id, role_name, created_at) VALUES
    (uuidv7(), 'SUPERADMIN', CURRENT_TIMESTAMP),
    (uuidv7(), 'KEPALA_SEKOLAH', CURRENT_TIMESTAMP),
    (uuidv7(), 'WALI_KELAS', CURRENT_TIMESTAMP),
    (uuidv7(), 'GURU', CURRENT_TIMESTAMP),
    (uuidv7(), 'STAF', CURRENT_TIMESTAMP),
    (uuidv7(), 'ORANG_TUA', CURRENT_TIMESTAMP),
    (uuidv7(), 'SISWA', CURRENT_TIMESTAMP)
ON CONFLICT (role_name) DO NOTHING;

-- Seed default permissions
INSERT INTO auth_permission (id, permission_name, description, created_at) VALUES
    (uuidv7(), 'classroom:view', 'Melihat daftar rombongan belajar', CURRENT_TIMESTAMP),
    (uuidv7(), 'classroom:create', 'Membuat rombongan belajar baru', CURRENT_TIMESTAMP),
    (uuidv7(), 'classroom:update', 'Memperbarui data rombongan belajar', CURRENT_TIMESTAMP),
    (uuidv7(), 'classroom:delete', 'Menghapus rombongan belajar', CURRENT_TIMESTAMP),
    (uuidv7(), 'report:view', 'Melihat dokumen rapor', CURRENT_TIMESTAMP),
    (uuidv7(), 'report:finalize', 'Memfinalisasi dan menandatangani rapor AI', CURRENT_TIMESTAMP),
    (uuidv7(), 'student:view', 'Melihat data siswa', CURRENT_TIMESTAMP),
    (uuidv7(), 'student:create', 'Menambah data siswa baru', CURRENT_TIMESTAMP),
    (uuidv7(), 'student:update', 'Memperbarui data siswa', CURRENT_TIMESTAMP),
    (uuidv7(), 'assessment:view', 'Melihat data asesmen', CURRENT_TIMESTAMP),
    (uuidv7(), 'assessment:create', 'Membuat asesmen baru', CURRENT_TIMESTAMP),
    (uuidv7(), 'assessment:grade', 'Memberi nilai asesmen', CURRENT_TIMESTAMP)
ON CONFLICT (permission_name) DO NOTHING;

-- Seed academic years
INSERT INTO master_academic_year (id, year_name, semester, is_active, created_at) VALUES
    (uuidv7(), '2023-2024', 'Ganjil', false, CURRENT_TIMESTAMP),
    (uuidv7(), '2023-2024', 'Genap', false, CURRENT_TIMESTAMP),
    (uuidv7(), '2024-2025', 'Ganjil', true, CURRENT_TIMESTAMP),
    (uuidv7(), '2024-2025', 'Genap', false, CURRENT_TIMESTAMP),
    (uuidv7(), '2025-2026', 'Ganjil', false, CURRENT_TIMESTAMP),
    (uuidv7(), '2025-2026', 'Genap', false, CURRENT_TIMESTAMP)
ON CONFLICT (year_name, semester) DO NOTHING;

-- Seed phases
INSERT INTO master_phase (id, phase_code, phase_name, description, created_at, updated_at) VALUES
    (uuidv7(), 'FASE_A', 'Fase A', 'Kelas 1-2 SD (Usia 6-8 tahun)', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'FASE_B', 'Fase B', 'Kelas 3-4 SD (Usia 9-11 tahun)', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'FASE_C', 'Fase C', 'Kelas 5-6 SD (Usia 12-14 tahun)', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (phase_code) DO NOTHING;

-- Seed grades
INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT 
    uuidv7(),
    p.id,
    g.grade_level,
    g.grade_name
FROM (VALUES 
    (1, 'Kelas 1'),
    (2, 'Kelas 2'),
    (3, 'Kelas 3'),
    (4, 'Kelas 4'),
    (5, 'Kelas 5'),
    (6, 'Kelas 6')
) AS g(grade_level, grade_name)
CROSS JOIN master_phase p
WHERE p.phase_code = 'FASE_A' AND g.grade_level <= 2
   OR p.phase_code = 'FASE_B' AND g.grade_level BETWEEN 3 AND 4
   OR p.phase_code = 'FASE_C' AND g.grade_level BETWEEN 5 AND 6
ON CONFLICT DO NOTHING;

-- Seed cognitive stages
INSERT INTO dl_cognitive_stage (id, stage_order, stage_name, operational_verbs, created_at, updated_at) VALUES
    (uuidv7(), 1, 'C1-Remembering', 'Mengingat, menulik, menyebutkan, mengidentifikasi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 2, 'C2-Understanding', 'Memahami, menjelaskan, menafsirkan, memberi contoh', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 3, 'C3-Applying', 'Menerapkan, melaksanakan, menghitung, menggunakan', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 4, 'C4-Analyzing', 'Menganalisis, membedakan, membandingkan, mengorganisir', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 5, 'C5-Evaluating', 'Mengevaluasi, menilai, mengkritik, menguji', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 6, 'C6-Creating', 'Mencipta, merancang, menyusun, mengkombinasikan', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (stage_order) DO NOTHING;

-- Seed assessment levels
INSERT INTO dl_assessment_level (id, level_code, description, pisa_level, created_at, updated_at) VALUES
    (uuidv7(), 'LEVEL_1', 'Pemahaman Konsept Dasar', '1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'LEVEL_2', 'Penerapan Konsep', '2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'LEVEL_3', 'Analisis dan Penalaran', '3', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'LEVEL_4', 'Evaluasi dan Sintesis', '4', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'LEVEL_5', 'Penciptaan dan Inovasi', '5-6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (level_code) DO NOTHING;

-- Seed design elements
INSERT INTO dl_design_element (id, design_element_name, description, is_active, created_at, updated_at) VALUES
    (uuidv7(), 'Olahraga', 'Aktivitas gerak dan fisik', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'Seni', 'Aktivitas kreatif dan artistik', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'Bahasa', 'Aktivitas literasi dan komunikasi', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'Matematika', 'Aktivitas numerasi dan logika', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'Sains', 'Aktivitas eksplorasi alam dan ilmu pengetahuan', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (design_element_name) DO NOTHING;

-- Seed profile dimensions
INSERT INTO master_profile_dimension (id, dimension_code, dimension_name, description, is_active, created_at, updated_at) VALUES
    (uuidv7(), 'BERIMAN_NASIONALIST', 'Beriman, bertakwa kepada Tuhan YME, dan berakhlak mulia', 'Dimensi karakter keimanan dan spiritual', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'BERKEPENDUDAYAN_SEHAT_JASMANI', 'Berkependudayaan hidup sehat dan menjaga kebersihan', 'Dimensi kesehatan fisik dan mental', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'BERKEPENDUDAYAN_CARA_BELAJAR', 'Berkependudayaan cara belajar dan belajar sepanjang hayat', 'Dimensi cara belajar dan kemandirian', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'BERKEPENDUDAYAN_WIRAUSAHA', 'Berkependudayaan dalam kegiatan wirausaha', 'Dimensi kreativitas dan produktivitas', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'BERKEPENDUDAYAN_KELAYAKAN_BAHASA', 'Berkependudayaan dalam menulis, membaca, dan berbahasa', 'Dimensi literasi dan komunikasi', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'BERKEPENDUDAYAN_TEKNOLOGI_INFORMATIKA', 'Berkependudayaan dalam menggunakan teknologi secara bertanggung jawab', 'Dimensi kemampuan digital', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (dimension_code) DO NOTHING;

-- Seed local context categories
INSERT INTO master_local_context_category (id, category_code, category_name, description, created_at, updated_at) VALUES
    (uuidv7(), 'GEOGRAPHI', 'Geografi Lokal', 'Kondisi geografis dan lingkungan fisik sekitar', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'BUDAYA', 'Budaya Lokal', 'Adat istiadat, kebiasaan, dan nilai budaya masyarakat', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'EKONOMI', 'Ekonomi Lokal', 'Mata pencaharian dan aktivitas ekonomi masyarakat', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (uuidv7(), 'PENDIDIKAN', 'Pendidikan Lokal', 'Lembaga pendidikan non-formal yang ada di masyarakat', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (category_code) DO NOTHING;

-- ============================================================
-- SECTION 13: Validation Queries
-- ============================================================

-- Verify all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
