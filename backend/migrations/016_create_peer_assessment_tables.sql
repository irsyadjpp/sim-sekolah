-- Peer Assessment System (Simplified for SD)
-- This migration creates tables for self and peer assessment appropriate for elementary students

-- Peer Assessment Template (simplified rubrics for SD)
CREATE TABLE master_peer_assessment_template (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_name VARCHAR(100) NOT NULL,
    assessment_type VARCHAR(20) NOT NULL,  -- SELF, PEER, GROUP
    subject_id UUID REFERENCES master_subject(id),
    phase VARCHAR(20) NOT NULL,  -- FASE_A, FASE_B, FASE_C
    assessment_focus VARCHAR(50) NOT NULL,  -- COLLABORATION, COMMUNICATION, CREATIVITY, CRITICAL_THINKING, PARTICIPATION
    description TEXT NOT NULL,
    criteria JSONB NOT NULL,  -- Simplified criteria structure suitable for SD
    rating_scale JSONB NOT NULL,  -- Simple rating scales (emojis, stars, etc.)
    instructions TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Self Assessment Records
CREATE TABLE trx_self_assessment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    template_id UUID NOT NULL REFERENCES master_peer_assessment_template(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES auth_user(id) ON DELETE CASCADE,
    assessment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    context VARCHAR(100),  -- Which activity/project this is for
    responses JSONB NOT NULL,  -- Student's self-assessment responses
    self_reflection TEXT,
    goals_set TEXT[],
    confidence_level VARCHAR(20),  -- LOW, MEDIUM, HIGH
    teacher_feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Peer Assessment Records
CREATE TABLE trx_peer_assessment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessor_student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    assessed_student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    template_id UUID NOT NULL REFERENCES master_peer_assessment_template(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES auth_user(id) ON DELETE CASCADE,
    assessment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    context VARCHAR(100),  -- Which activity/project this is for
    responses JSONB NOT NULL,  -- Peer's assessment responses
    positive_feedback TEXT,
    constructive_feedback TEXT,
    suggestions TEXT[],
    relationship_context VARCHAR(50),  -- GROUP_MEMBER, CLASSMATE, PROJECT_PARTNER
    teacher_review_status VARCHAR(20) DEFAULT 'PENDING',  -- PENDING, APPROVED, REJECTED
    teacher_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure student doesn't assess themselves
    CONSTRAINT chk_different_students CHECK (assessor_student_id != assessed_student_id)
);

-- Group Assessment Records (for collaborative work)
CREATE TABLE trx_group_assessment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL,
    group_name VARCHAR(100) NOT NULL,
    template_id UUID NOT NULL REFERENCES master_peer_assessment_template(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES auth_user(id) ON DELETE CASCADE,
    assessment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    context VARCHAR(100),  -- Which project/activity
    project_description TEXT,
    group_responses JSONB NOT NULL,  -- Group-level assessment responses
    individual_contributions JSONB,  -- Individual contribution tracking
    collaboration_rating VARCHAR(20),  -- POOR, FAIR, GOOD, EXCELLENT
    group_goals TEXT[],
    group_reflection TEXT,
    teacher_feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Group Assessment Individual Members
CREATE TABLE trx_group_assessment_member (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_assessment_id UUID NOT NULL REFERENCES trx_group_assessment(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    role VARCHAR(50),  -- LEADER, CONTRIBUTOR, SUPPORTER, OBSERVER
    participation_rating VARCHAR(20),  -- LOW, MEDIUM, HIGH
    peer_feedback_received TEXT[],
    self_contribution_rating VARCHAR(20),
    contribution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Peer Assessment Guidelines for SD (age-appropriate instructions)
CREATE TABLE master_peer_assessment_guideline (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phase VARCHAR(20) NOT NULL,  -- FASE_A, FASE_B, FASE_C
    guideline_category VARCHAR(50) NOT NULL,  -- GIVING_FEEDBACK, RECEIVING_FEEDBACK, SELF_REFLECTION
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    examples TEXT[],
    do_s TEXT[],
    dont_s TEXT[],
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_peer_template_type ON master_peer_assessment_template(assessment_type);
CREATE INDEX idx_peer_template_phase ON master_peer_assessment_template(phase);
CREATE INDEX idx_peer_template_subject ON master_peer_assessment_template(subject_id);
CREATE INDEX idx_peer_template_active ON master_peer_assessment_template(is_active);
CREATE INDEX idx_self_assessment_student ON trx_self_assessment(student_id);
CREATE INDEX idx_self_assessment_template ON trx_self_assessment(template_id);
CREATE INDEX idx_self_assessment_date ON trx_self_assessment(assessment_date);
CREATE INDEX idx_peer_assessment_assessor ON trx_peer_assessment(assessor_student_id);
CREATE INDEX idx_peer_assessment_assessed ON trx_peer_assessment(assessed_student_id);
CREATE INDEX idx_peer_assessment_template ON trx_peer_assessment(template_id);
CREATE INDEX idx_peer_assessment_date ON trx_peer_assessment(assessment_date);
CREATE INDEX idx_group_assessment_group ON trx_group_assessment(group_id);
CREATE INDEX idx_group_assessment_template ON trx_group_assessment(template_id);
CREATE INDEX idx_group_assessment_member_group ON trx_group_assessment_member(group_assessment_id);
CREATE INDEX idx_group_assessment_member_student ON trx_group_assessment_member(student_id);
CREATE INDEX idx_peer_guideline_phase ON master_peer_assessment_guideline(phase);
CREATE INDEX idx_peer_guideline_category ON master_peer_assessment_guideline(guideline_category);
CREATE INDEX idx_peer_guideline_active ON master_peer_assessment_guideline(is_active);

-- Add comments for documentation
COMMENT ON TABLE master_peer_assessment_template IS 'Master table for peer assessment templates (simplified for SD)';
COMMENT ON TABLE trx_self_assessment IS 'Transaction table for student self-assessments';
COMMENT ON TABLE trx_peer_assessment IS 'Transaction table for peer-to-peer assessments';
COMMENT ON TABLE trx_group_assessment IS 'Transaction table for group assessments for collaborative work';
COMMENT ON TABLE trx_group_assessment_member IS 'Transaction table for individual member contributions in group assessments';
COMMENT ON TABLE master_peer_assessment_guideline IS 'Master table for age-appropriate peer assessment guidelines';
