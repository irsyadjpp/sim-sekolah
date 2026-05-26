-- Migration: Create reading literacy assessment tables
-- Description: Create tables for tracking reading literacy progression for SD students
-- Created: 2024-05-24

-- Create master_reading_level table
CREATE TABLE IF NOT EXISTS master_reading_level (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level_code VARCHAR(10) UNIQUE NOT NULL,
    level_name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    phase_id UUID,
    indicators TEXT,
    wpm_range TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for master_reading_level
CREATE INDEX IF NOT EXISTS idx_reading_level_code ON master_reading_level(level_code) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reading_level_phase ON master_reading_level(phase_id) WHERE deleted_at IS NULL;

-- Add comments
COMMENT ON TABLE master_reading_level IS 'Master table for reading levels (LEVEL_0 to LEVEL_6) for SD students';
COMMENT ON COLUMN master_reading_level.level_code IS 'Reading level code: LEVEL_0 to LEVEL_6';
COMMENT ON COLUMN master_reading_level.wpm_range IS 'Words per minute range for this level';
COMMENT ON COLUMN master_reading_level.indicators IS 'JSON array of reading indicators for this level';

-- Create trx_reading_literacy_assessment table
CREATE TABLE IF NOT EXISTS trx_reading_literacy_assessment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    reading_level_id UUID NOT NULL,
    assessment_date DATE NOT NULL,
    words_per_minute INTEGER,
    comprehension_score DECIMAL(5,2),
    fluency_rating VARCHAR(20),
    accuracy_score DECIMAL(5,2),
    notes TEXT,
    teacher_id UUID,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for trx_reading_literacy_assessment
CREATE INDEX IF NOT EXISTS idx_reading_assessment_student ON trx_reading_literacy_assessment(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reading_assessment_level ON trx_reading_literacy_assessment(reading_level_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reading_assessment_date ON trx_reading_literacy_assessment(assessment_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_reading_assessment_teacher ON trx_reading_literacy_assessment(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE trx_reading_literacy_assessment
ADD CONSTRAINT fk_reading_assessment_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE trx_reading_literacy_assessment
ADD CONSTRAINT fk_reading_assessment_level
FOREIGN KEY (reading_level_id) REFERENCES master_reading_level(id) ON DELETE CASCADE;

ALTER TABLE trx_reading_literacy_assessment
ADD CONSTRAINT fk_reading_assessment_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE trx_reading_literacy_assessment IS 'Transaction table for reading literacy assessment results';
COMMENT ON COLUMN trx_reading_literacy_assessment.words_per_minute IS 'Reading speed in words per minute';
COMMENT ON COLUMN trx_reading_literacy_assessment.comprehension_score IS 'Comprehension score (0-100)';
COMMENT ON COLUMN trx_reading_literacy_assessment.fluency_rating IS 'Fluency rating: RENDAH, SEDANG, TINGGI';
COMMENT ON COLUMN trx_reading_literacy_assessment.accuracy_score IS 'Reading accuracy score (0-100)';
