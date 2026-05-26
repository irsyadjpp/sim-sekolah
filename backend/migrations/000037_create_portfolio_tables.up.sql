-- Migration: Create portfolio and learning evidence tables
-- Description: Create tables for student portfolio management, artifact tracking, and learning evidence validation
-- Created: 2025-05-25

-- Create portfolios table
CREATE TABLE IF NOT EXISTS portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    portfolio_type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id UUID,
    project_id UUID,
    period VARCHAR(20),
    academic_year_id UUID NOT NULL,
    teacher_id UUID,
    is_published BOOLEAN DEFAULT false,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for portfolios
CREATE INDEX IF NOT EXISTS idx_portfolios_student ON portfolios(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_type ON portfolios(portfolio_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_subject ON portfolios(subject_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_project ON portfolios(project_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_period ON portfolios(period) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_academic_year ON portfolios(academic_year_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_published ON portfolios(is_published) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_portfolios_teacher ON portfolios(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE portfolios
ADD CONSTRAINT fk_portfolios_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE portfolios
ADD CONSTRAINT fk_portfolios_academic_year
FOREIGN KEY (academic_year_id) REFERENCES master_academic_year(id) ON DELETE CASCADE;

ALTER TABLE portfolios
ADD CONSTRAINT fk_portfolios_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE portfolios IS 'Master table for student learning portfolios';
COMMENT ON COLUMN portfolios.portfolio_type IS 'Type: STUDENT, PROJECT, SUBJECT, CHARACTER';
COMMENT ON COLUMN portfolios.is_published IS 'Whether portfolio is published for sharing';
COMMENT ON COLUMN portfolios.period IS 'Period: SEMESTER_1, SEMESTER_2';

-- Create portfolio_artifacts table
CREATE TABLE IF NOT EXISTS portfolio_artifacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID NOT NULL,
    artifact_type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    file_url VARCHAR(500),
    file_name VARCHAR(255),
    file_size BIGINT,
    file_type VARCHAR(50),
    thumbnail_url VARCHAR(500),
    competency_ids TEXT,
    skills TEXT,
    reflection TEXT,
    teacher_feedback TEXT,
    teacher_id UUID,
    is_featured BOOLEAN DEFAULT false,
    display_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for portfolio_artifacts
CREATE INDEX IF NOT EXISTS idx_artifacts_portfolio ON portfolio_artifacts(portfolio_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_artifacts_type ON portfolio_artifacts(artifact_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_artifacts_featured ON portfolio_artifacts(is_featured) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_artifacts_order ON portfolio_artifacts(display_order) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_artifacts_teacher ON portfolio_artifacts(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE portfolio_artifacts
ADD CONSTRAINT fk_artifacts_portfolio
FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE;

ALTER TABLE portfolio_artifacts
ADD CONSTRAINT fk_artifacts_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE portfolio_artifacts IS 'Individual artifacts within student portfolios';
COMMENT ON COLUMN portfolio_artifacts.artifact_type IS 'Type: DOCUMENT, IMAGE, VIDEO, AUDIO, PROJECT, ASSESSMENT, REFLECTION, CERTIFICATE';
COMMENT ON COLUMN portfolio_artifacts.competency_ids IS 'JSON array of competency IDs linked to this artifact';
COMMENT ON COLUMN portfolio_artifacts.skills IS 'JSON array of skills demonstrated';
COMMENT ON COLUMN portfolio_artifacts.is_featured IS 'Whether artifact is featured in portfolio';

-- Create learning_evidence table
CREATE TABLE IF NOT EXISTS learning_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    artifact_id UUID NOT NULL,
    competency_id UUID NOT NULL,
    competency_type VARCHAR(20) NOT NULL,
    evidence_date DATE NOT NULL,
    mastery_level VARCHAR(20) NOT NULL,
    teacher_id UUID,
    validation_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    validation_notes TEXT,
    validated_by UUID,
    validated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Create indexes for learning_evidence
CREATE INDEX IF NOT EXISTS idx_learning_evidence_student ON learning_evidence(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_artifact ON learning_evidence(artifact_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_competency ON learning_evidence(competency_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_type ON learning_evidence(competency_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_date ON learning_evidence(evidence_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_mastery ON learning_evidence(mastery_level) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_status ON learning_evidence(validation_status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_teacher ON learning_evidence(teacher_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_learning_evidence_validator ON learning_evidence(validated_by) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE learning_evidence
ADD CONSTRAINT fk_learning_evidence_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE learning_evidence
ADD CONSTRAINT fk_learning_evidence_artifact
FOREIGN KEY (artifact_id) REFERENCES portfolio_artifacts(id) ON DELETE CASCADE;

ALTER TABLE learning_evidence
ADD CONSTRAINT fk_learning_evidence_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

ALTER TABLE learning_evidence
ADD CONSTRAINT fk_learning_evidence_validator
FOREIGN KEY (validated_by) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE learning_evidence IS 'Evidence of learning linked to competencies with validation workflow';
COMMENT ON COLUMN learning_evidence.competency_type IS 'Type: CP, TP, PROJECT';
COMMENT ON COLUMN learning_evidence.mastery_level IS 'Mastery level: BELUM, SEDANG, MENGUASAI';
COMMENT ON COLUMN learning_evidence.validation_status IS 'Validation status: PENDING, APPROVED, REJECTED';

-- Create portfolio_reviews table
CREATE TABLE IF NOT EXISTS portfolio_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID NOT NULL,
    reviewer_id UUID NOT NULL,
    review_date DATE NOT NULL,
    overall_rating INT CHECK (overall_rating >= 1 AND overall_rating <= 5),
    strengths TEXT,
    areas_for_improvement TEXT,
    recommendations TEXT,
    is_formal BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    UNIQUE(portfolio_id, reviewer_id)
);

-- Create indexes for portfolio_reviews
CREATE INDEX IF NOT EXISTS idx_reviews_portfolio ON portfolio_reviews(portfolio_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reviews_reviewer ON portfolio_reviews(reviewer_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reviews_date ON portfolio_reviews(review_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reviews_formal ON portfolio_reviews(is_formal) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE portfolio_reviews
ADD CONSTRAINT fk_portfolio_reviews_portfolio
FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE;

ALTER TABLE portfolio_reviews
ADD CONSTRAINT fk_portfolio_reviews_reviewer
FOREIGN KEY (reviewer_id) REFERENCES auth_user(id) ON DELETE CASCADE;

-- Add comments
COMMENT ON TABLE portfolio_reviews IS 'Teacher reviews of student portfolios';
COMMENT ON COLUMN portfolio_reviews.overall_rating IS 'Overall rating 1-5';
COMMENT ON COLUMN portfolio_reviews.is_formal IS 'Whether this is a formal review for assessment';

-- Seed initial portfolio types for reference
-- This can be expanded based on specific school requirements