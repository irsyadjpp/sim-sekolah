-- Phase 3: Academic Quality & Supervision Tables
-- This migration creates tables for Academic Supervision, Teaching Reflection, and Intervention modules

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- ACADEMIC SUPERVISION MODULE TABLES
-- ============================================

-- Supervision Cycles
CREATE TABLE IF NOT EXISTS supervision_cycles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_name VARCHAR(100) NOT NULL,
    academic_year_id UUID NOT NULL,
    school_id UUID NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PLANNED',
    description TEXT,
    supervisor_id UUID NOT NULL,
    goals JSONB,
    expected_outcomes JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Teacher Observations
CREATE TABLE IF NOT EXISTS teacher_observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    supervision_cycle_id UUID,
    teacher_id UUID NOT NULL,
    observer_id UUID NOT NULL,
    subject_id UUID,
    classroom_id UUID,
    observation_date DATE NOT NULL,
    observation_type VARCHAR(50) DEFAULT 'CLASSROOM',
    status VARCHAR(20) DEFAULT 'SCHEDULED',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    lesson_topic VARCHAR(200),
    class_grade VARCHAR(50),
    strengths JSONB,
    areas_for_improvement JSONB,
    notes TEXT,
    score NUMERIC(3,2),
    max_score NUMERIC(3,2) DEFAULT 100.0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Supervision Feedback
CREATE TABLE IF NOT EXISTS supervision_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_id UUID NOT NULL,
    teacher_id UUID NOT NULL,
    feedback_date DATE NOT NULL DEFAULT CURRENT_DATE,
    feedback_provider_id UUID NOT NULL,
    status VARCHAR(20) DEFAULT 'DRAFT',
    strengths JSONB,
    improvement_areas JSONB,
    recommendations JSONB,
    action_plan TEXT,
    follow_up_date DATE,
    teacher_response TEXT,
    response_date TIMESTAMPTZ,
    is_acknowledged BOOLEAN DEFAULT false,
    overall_rating NUMERIC(3,2),
    comments TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Supervision Analytics
CREATE TABLE IF NOT EXISTS supervision_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school_id UUID NOT NULL,
    academic_year_id UUID NOT NULL,
    supervision_cycle_id UUID,
    analytics_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_observations INTEGER DEFAULT 0,
    completed_observations INTEGER DEFAULT 0,
    average_score NUMERIC(5,2),
    teachers_supervised INTEGER DEFAULT 0,
    improvement_rate NUMERIC(5,2),
    feedback_completion_rate NUMERIC(5,2),
    top_strengths JSONB,
    common_improvement_areas JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- ============================================
-- TEACHING REFLECTION MODULE TABLES
-- ============================================

-- Teaching Reflections
CREATE TABLE IF NOT EXISTS teaching_reflections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_id UUID NOT NULL,
    subject_id UUID,
    classroom_id UUID,
    reflection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    reflection_type VARCHAR(20) DEFAULT 'DAILY',
    status VARCHAR(20) DEFAULT 'DRAFT',
    lesson_topic VARCHAR(200),
    what_went_well JSONB,
    what_could_improve JSONB,
    student_engagement TEXT,
    teaching_strategies JSONB,
    challenges JSONB,
    solutions JSONB,
    next_steps JSONB,
    self_rating NUMERIC(3,2),
    notes TEXT,
    is_private BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Teaching Effectiveness Metrics
CREATE TABLE IF NOT EXISTS teaching_effectiveness_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_id UUID NOT NULL,
    subject_id UUID,
    measurement_date DATE NOT NULL DEFAULT CURRENT_DATE,
    student_satisfaction NUMERIC(3,2),
    learning_outcomes NUMERIC(3,2),
    engagement_level NUMERIC(3,2),
    time_management NUMERIC(3,2),
    content_delivery NUMERIC(3,2),
    overall_effectiveness NUMERIC(3,2),
    strengths JSONB,
    improvement_areas JSONB,
    benchmark_comparison NUMERIC(3,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Teaching Quality Indicators
CREATE TABLE IF NOT EXISTS teaching_quality_indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_id UUID NOT NULL,
    assessment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    indicator_category VARCHAR(50),
    indicator_name VARCHAR(100) NOT NULL,
    quality_rating VARCHAR(30),
    score NUMERIC(3,2),
    evidence JSONB,
    feedback TEXT,
    action_required BOOLEAN DEFAULT false,
    action_plan TEXT,
    target_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Reflection Trends
CREATE TABLE IF NOT EXISTS reflection_trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_id UUID NOT NULL,
    trend_period VARCHAR(20),
    start_date DATE,
    end_date DATE,
    total_reflections INTEGER DEFAULT 0,
    average_self_rating NUMERIC(3,2),
    common_themes JSONB,
    improvement_areas JSONB,
    growth_indicators JSONB,
    recommendations JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- ============================================
-- INTERVENTION MODULE TABLES
-- ============================================

-- Remedial Programs
CREATE TABLE IF NOT EXISTS remedial_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    program_name VARCHAR(100) NOT NULL,
    subject_id UUID,
    target_grade VARCHAR(50),
    description TEXT,
    learning_gaps JSONB,
    strategies JSONB,
    resources JSONB,
    duration_weeks INTEGER DEFAULT 4,
    sessions_per_week INTEGER DEFAULT 2,
    success_criteria JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Enrichment Programs
CREATE TABLE IF NOT EXISTS enrichment_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    program_name VARCHAR(100) NOT NULL,
    subject_id UUID,
    target_grade VARCHAR(50),
    description TEXT,
    advanced_topics JSONB,
    projects JSONB,
    resources JSONB,
    duration_weeks INTEGER DEFAULT 4,
    sessions_per_week INTEGER DEFAULT 2,
    success_criteria JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Student Intervention Assignments
CREATE TABLE IF NOT EXISTS student_intervention_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    program_id UUID NOT NULL,
    intervention_type VARCHAR(20) NOT NULL,
    teacher_id UUID NOT NULL,
    assignment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PLANNED',
    priority_level VARCHAR(20) DEFAULT 'MEDIUM',
    baseline_score NUMERIC(5,2),
    target_score NUMERIC(5,2),
    current_score NUMERIC(5,2),
    progress NUMERIC(3,2),
    customized_plan TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Intervention Workflows
CREATE TABLE IF NOT EXISTS intervention_workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_name VARCHAR(100) NOT NULL,
    intervention_type VARCHAR(20) NOT NULL,
    trigger_conditions JSONB,
    workflow_steps JSONB,
    auto_assignment BOOLEAN DEFAULT false,
    notification_rules JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Intervention Analytics
CREATE TABLE IF NOT EXISTS intervention_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school_id UUID NOT NULL,
    academic_year_id UUID NOT NULL,
    analytics_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_remedial_assignments INTEGER DEFAULT 0,
    total_enrichment_assignments INTEGER DEFAULT 0,
    active_interventions INTEGER DEFAULT 0,
    completed_interventions INTEGER DEFAULT 0,
    average_improvement NUMERIC(5,2),
    success_rate NUMERIC(5,2),
    most_effective_strategies JSONB,
    common_learning_gaps JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Supervision indexes
CREATE INDEX IF NOT EXISTS idx_supervision_cycles_school ON supervision_cycles(school_id);
CREATE INDEX IF NOT EXISTS idx_supervision_cycles_academic_year ON supervision_cycles(academic_year_id);
CREATE INDEX IF NOT EXISTS idx_teacher_observations_teacher ON teacher_observations(teacher_id);
CREATE INDEX IF NOT EXISTS idx_teacher_observations_observer ON teacher_observations(observer_id);
CREATE INDEX IF NOT EXISTS idx_teacher_observations_cycle ON teacher_observations(supervision_cycle_id);
CREATE INDEX IF NOT EXISTS idx_supervision_feedback_observation ON supervision_feedback(observation_id);
CREATE INDEX IF NOT EXISTS idx_supervision_feedback_teacher ON supervision_feedback(teacher_id);
CREATE INDEX IF NOT EXISTS idx_supervision_analytics_school ON supervision_analytics(school_id);
CREATE INDEX IF NOT EXISTS idx_supervision_analytics_academic_year ON supervision_analytics(academic_year_id);

-- Teaching Reflection indexes
CREATE INDEX IF NOT EXISTS idx_teaching_reflections_teacher ON teaching_reflections(teacher_id);
CREATE INDEX IF NOT EXISTS idx_teaching_reflections_date ON teaching_reflections(reflection_date);
CREATE INDEX IF NOT EXISTS idx_teaching_effectiveness_teacher ON teaching_effectiveness_metrics(teacher_id);
CREATE INDEX IF NOT EXISTS idx_teaching_quality_teacher ON teaching_quality_indicators(teacher_id);
CREATE INDEX IF NOT EXISTS idx_reflection_trends_teacher ON reflection_trends(teacher_id);

-- Intervention indexes
CREATE INDEX IF NOT EXISTS idx_remedial_programs_subject ON remedial_programs(subject_id);
CREATE INDEX IF NOT EXISTS idx_enrichment_programs_subject ON enrichment_programs(subject_id);
CREATE INDEX IF NOT EXISTS idx_student_interventions_student ON student_intervention_assignments(student_id);
CREATE INDEX IF NOT EXISTS idx_student_interventions_program ON student_intervention_assignments(program_id);
CREATE INDEX IF NOT EXISTS idx_student_interventions_type ON student_intervention_assignments(intervention_type);
CREATE INDEX IF NOT EXISTS idx_intervention_analytics_school ON intervention_analytics(school_id);
CREATE INDEX IF NOT EXISTS idx_intervention_analytics_academic_year ON intervention_analytics(academic_year_id);

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE supervision_cycles IS 'Manages academic supervision cycles for quality assurance';
COMMENT ON TABLE teacher_observations IS 'Records classroom observations and evaluations';
COMMENT ON TABLE supervision_feedback IS 'Stores feedback given to teachers after observations';
COMMENT ON TABLE supervision_analytics IS 'Aggregated analytics for supervision effectiveness';

COMMENT ON TABLE teaching_reflections IS 'Teacher self-reflection journals and entries';
COMMENT ON TABLE teaching_effectiveness_metrics IS 'Metrics for measuring teaching effectiveness';
COMMENT ON TABLE teaching_quality_indicators IS 'Quality indicators for teaching performance';
COMMENT ON TABLE reflection_trends IS 'Trend analysis for teaching reflections over time';

COMMENT ON TABLE remedial_programs IS 'Remedial intervention programs for struggling students';
COMMENT ON TABLE enrichment_programs IS 'Enrichment programs for advanced students';
COMMENT ON TABLE student_intervention_assignments IS 'Student-specific intervention assignments';
COMMENT ON TABLE intervention_workflows IS 'Automated workflows for intervention management';
COMMENT ON TABLE intervention_analytics IS 'Analytics for intervention program effectiveness';