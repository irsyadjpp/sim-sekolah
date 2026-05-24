-- Migration: Create foundational skills assessment tables
-- Description: Create tables for tracking foundational skills (literasi-numerasi) assessment for SD Fase A
-- Created: 2024-05-24

-- Create master_foundational_skill_standard table
CREATE TABLE IF NOT EXISTS master_foundational_skill_standard (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    skill_type VARCHAR(20) NOT NULL,
    skill_code VARCHAR(20) UNIQUE NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    phase_id UUID,
    indicators TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Create indexes for master_foundational_skill_standard
CREATE INDEX IF NOT EXISTS idx_foundational_skill_type ON master_foundational_skill_standard(skill_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_foundational_skill_code ON master_foundational_skill_standard(skill_code) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_foundational_skill_phase ON master_foundational_skill_standard(phase_id) WHERE deleted_at IS NULL;

-- Add comments
COMMENT ON TABLE master_foundational_skill_standard IS 'Master table for foundational skill standards (literasi-numerasi) for SD';
COMMENT ON COLUMN master_foundational_skill_standard.skill_type IS 'Type of foundational skill: LITERASI, NUMERASI';
COMMENT ON COLUMN master_foundational_skill_standard.skill_code IS 'Unique code for the skill standard';
COMMENT ON COLUMN master_foundational_skill_standard.indicators IS 'JSON array of learning indicators';

-- Create trx_foundational_skill_assessment table
CREATE TABLE IF NOT EXISTS trx_foundational_skill_assessment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    skill_standard_id UUID NOT NULL,
    assessment_date DATE NOT NULL,
    mastery_level VARCHAR(20) NOT NULL,
    score DECIMAL(5,2),
    notes TEXT,
    teacher_id UUID,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Create indexes for trx_foundational_skill_assessment
CREATE INDEX IF NOT EXISTS idx_foundational_assessment_student ON trx_foundational_skill_assessment(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_foundational_assessment_standard ON trx_foundational_skill_assessment(skill_standard_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_foundational_assessment_date ON trx_foundational_skill_assessment(assessment_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_foundational_assessment_teacher ON trx_foundational_skill_assessment(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE trx_foundational_skill_assessment
ADD CONSTRAINT fk_foundational_assessment_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE trx_foundational_skill_assessment
ADD CONSTRAINT fk_foundational_assessment_standard
FOREIGN KEY (skill_standard_id) REFERENCES master_foundational_skill_standard(id) ON DELETE CASCADE;

ALTER TABLE trx_foundational_skill_assessment
ADD CONSTRAINT fk_foundational_assessment_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE trx_foundational_skill_assessment IS 'Transaction table for foundational skills assessment results';
COMMENT ON COLUMN trx_foundational_skill_assessment.mastery_level IS 'Mastery level: BELUM, SEDANG, MENGUASAI';
COMMENT ON COLUMN trx_foundational_skill_assessment.score IS 'Assessment score (0-100)';
