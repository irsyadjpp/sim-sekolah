-- Character Intervention System
-- This migration creates tables for character development intervention tracking and recommendations

-- Character Intervention table to track interventions
CREATE TABLE master_character_intervention (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    intervention_name VARCHAR(100) NOT NULL,
    character_dimension VARCHAR(50) NOT NULL,  -- BERAKHLAK, BERKEBHINEASAN, BERNILAI_SANTUN, MANDIRI, BERTANGGUNG_JAWAB, GOTONG_ROYONG
    target_age_group VARCHAR(20),  -- FASE_A, FASE_B, FASE_C
    intervention_type VARCHAR(50) NOT NULL,  -- POSITIVE_REINFORCEMENT, BEHAVIOR_MODIFICATION, MENTORING, GROUP_ACTIVITY, COUNSELING
    description TEXT NOT NULL,
    strategies TEXT[],
    resources TEXT[],
    duration_weeks INT DEFAULT 4,
    success_criteria TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Student Character Intervention Assignment
CREATE TABLE trx_student_character_intervention (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    intervention_id UUID NOT NULL REFERENCES master_character_intervention(id) ON DELETE CASCADE,
    teacher_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    assignment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    target_start_date DATE NOT NULL,
    target_end_date DATE NOT NULL,
    current_status VARCHAR(20) DEFAULT 'ACTIVE',  -- PLANNED, ACTIVE, PAUSED, COMPLETED, CANCELLED
    priority_level VARCHAR(20) DEFAULT 'MEDIUM',  -- LOW, MEDIUM, HIGH, URGENT
    baseline_assessment TEXT,
    customized_strategies TEXT[],
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Character Intervention Progress Tracking
CREATE TABLE trx_character_intervention_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assignment_id UUID NOT NULL REFERENCES trx_student_character_intervention(id) ON DELETE CASCADE,
    observation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    observer_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    progress_rating VARCHAR(20),  -- NO_PROGRESS, MINIMAL, MODERATE, SIGNIFICANT, EXCELLENT
    behavioral_indicators TEXT[],
    specific_achievements TEXT[],
    challenges TEXT[],
    support_provided TEXT,
    next_steps TEXT[],
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Intervention Recommendation Engine Results
CREATE TABLE trx_intervention_recommendation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    p5_assessment_id UUID,  -- Link to P5 assessment if available
    recommended_interventions UUID[] NOT NULL,  -- Array of intervention IDs
    recommendation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    recommendation_source VARCHAR(50) NOT NULL,  -- P5_ASSESSMENT, TEACHER_OBSERVATION, PARENT_FEEDBACK, PEER_FEEDBACK
    confidence_score DECIMAL(3,2),  -- 0.00 to 1.00
    rationale TEXT,
    priority_ranking INT[],
    implementation_timeline_weeks INT DEFAULT 4,
    additional_notes TEXT,
    is_accepted BOOLEAN,
    accepted_by UUID REFERENCES auth_user(id),
    accepted_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Character Development Milestone Tracking
CREATE TABLE trx_character_milestone (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    character_dimension VARCHAR(50) NOT NULL,
    milestone_description TEXT NOT NULL,
    milestone_date DATE NOT NULL DEFAULT CURRENT_DATE,
    achievement_level VARCHAR(20) NOT NULL,  -- EMERGING, DEVELOPING, PROFICIENT, EXEMPLARY
    evidence TEXT[],
    observer_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    celebration_method VARCHAR(50),  -- VERBAL_PRAISE, CERTIFICATE, CLASS_RECOGNITION, PARENT_NOTIFICATION
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for better query performance
CREATE INDEX idx_character_intervention_dimension ON master_character_intervention(character_dimension);
CREATE INDEX idx_character_intervention_type ON master_character_intervention(intervention_type);
CREATE INDEX idx_character_intervention_active ON master_character_intervention(is_active);
CREATE INDEX idx_character_intervention_deleted ON master_character_intervention(deleted_at);
CREATE INDEX idx_student_intervention_student ON trx_student_character_intervention(student_id);
CREATE INDEX idx_student_intervention_intervention ON trx_student_character_intervention(intervention_id);
CREATE INDEX idx_student_intervention_teacher ON trx_student_character_intervention(teacher_id);
CREATE INDEX idx_student_intervention_status ON trx_student_character_intervention(current_status);
CREATE INDEX idx_student_intervention_deleted ON trx_student_character_intervention(deleted_at);
CREATE INDEX idx_intervention_progress_assignment ON trx_character_intervention_progress(assignment_id);
CREATE INDEX idx_intervention_progress_date ON trx_character_intervention_progress(observation_date);
CREATE INDEX idx_intervention_progress_deleted ON trx_character_intervention_progress(deleted_at);
CREATE INDEX idx_recommendation_student ON trx_intervention_recommendation(student_id);
CREATE INDEX idx_recommendation_date ON trx_intervention_recommendation(recommendation_date);
CREATE INDEX idx_recommendation_source ON trx_intervention_recommendation(recommendation_source);
CREATE INDEX idx_recommendation_deleted ON trx_intervention_recommendation(deleted_at);
CREATE INDEX idx_milestone_student ON trx_character_milestone(student_id);
CREATE INDEX idx_milestone_dimension ON trx_character_milestone(character_dimension);
CREATE INDEX idx_milestone_date ON trx_character_milestone(milestone_date);
CREATE INDEX idx_milestone_deleted ON trx_character_milestone(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_character_intervention IS 'Master table for character intervention strategies';
COMMENT ON TABLE trx_student_character_intervention IS 'Transaction table for student-specific intervention assignments';
COMMENT ON TABLE trx_character_intervention_progress IS 'Transaction table for tracking intervention progress';
COMMENT ON TABLE trx_intervention_recommendation IS 'Transaction table for intervention recommendations from recommendation engine';
COMMENT ON TABLE trx_character_milestone IS 'Transaction table for character development milestone tracking';
