-- Migration: Create Rubric System Tables
-- Created: 2026-05-25
-- Description: This migration creates tables for comprehensive rubric system including rubrics, criteria, levels, and criteria level descriptions

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Rubric Table
-- Main rubric template/definition
CREATE TABLE IF NOT EXISTS master_rubric (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id UUID,
    assessment_type VARCHAR(50) NOT NULL,
    grade_level VARCHAR(50),
    max_score DECIMAL(5,2) DEFAULT 100,
    is_template BOOLEAN DEFAULT true,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for rubric
CREATE INDEX IF NOT EXISTS idx_rubric_subject ON master_rubric(subject_id);
CREATE INDEX IF NOT EXISTS idx_rubric_assessment_type ON master_rubric(assessment_type);
CREATE INDEX IF NOT EXISTS idx_rubric_grade_level ON master_rubric(grade_level);
CREATE INDEX IF NOT EXISTS idx_rubric_is_template ON master_rubric(is_template);
CREATE INDEX IF NOT EXISTS idx_rubric_is_active ON master_rubric(is_active);
CREATE INDEX IF NOT EXISTS idx_rubric_deleted_at ON master_rubric(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_rubric IS 'Template rubric untuk penilaian komprehensif';
COMMENT ON COLUMN master_rubric.assessment_type IS 'Jenis penilaian: PROJECT, PRESENTATION, WRITTEN_WORK, PRACTICAL, BEHAVIORAL, ORAL, OBSERVATION';
COMMENT ON COLUMN master_rubric.grade_level IS 'Tingkat kelas: 1-6, LOWER (1-3), UPPER (4-6), ALL';
COMMENT ON COLUMN master_rubric.is_template IS 'Apakah rubric ini dapat digunakan sebagai template';
COMMENT ON COLUMN master_rubric.max_score IS 'Nilai maksimum untuk rubric';

-- Add check constraint for assessment_type
ALTER TABLE master_rubric 
ADD CONSTRAINT chk_assessment_type 
CHECK (assessment_type IN ('PROJECT', 'PRESENTATION', 'WRITTEN_WORK', 'PRACTICAL', 'BEHAVIORAL', 'ORAL', 'OBSERVATION'));

-- RubricCriteria Table
-- Individual assessment criteria within a rubric
CREATE TABLE IF NOT EXISTS master_rubric_criteria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rubric_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    weight DECIMAL(5,2) DEFAULT 1.0,
    sequence INTEGER DEFAULT 1,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for rubric_criteria
CREATE INDEX IF NOT EXISTS idx_rubric_criteria_rubric ON master_rubric_criteria(rubric_id);
CREATE INDEX IF NOT EXISTS idx_rubric_criteria_sequence ON master_rubric_criteria(sequence);
CREATE INDEX IF NOT EXISTS idx_rubric_criteria_deleted_at ON master_rubric_criteria(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_rubric_criteria IS 'Kriteria penilaian dalam rubric';
COMMENT ON COLUMN master_rubric_criteria.weight IS 'Bobot kriteria dalam total skor';
COMMENT ON COLUMN master_rubric_criteria.sequence IS 'Urutan kriteria dalam rubric';
COMMENT ON COLUMN master_rubric_criteria.is_required IS 'Apakah kriteria ini wajib';

-- RubricLevel Table
-- Scoring levels (e.g., 1-4, or MB-SB-BSH-SAB)
CREATE TABLE IF NOT EXISTS master_rubric_level (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rubric_id UUID NOT NULL,
    level_code VARCHAR(20) NOT NULL,
    level_name VARCHAR(100) NOT NULL,
    point_value DECIMAL(5,2) NOT NULL,
    min_percentage DECIMAL(5,2) DEFAULT 0,
    max_percentage DECIMAL(5,2) DEFAULT 100,
    sequence INTEGER DEFAULT 1,
    color VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for rubric_level
CREATE INDEX IF NOT EXISTS idx_rubric_level_rubric ON master_rubric_level(rubric_id);
CREATE INDEX IF NOT EXISTS idx_rubric_level_level_code ON master_rubric_level(level_code);
CREATE INDEX IF NOT EXISTS idx_rubric_level_sequence ON master_rubric_level(sequence);
CREATE INDEX IF NOT EXISTS idx_rubric_level_deleted_at ON master_rubric_level(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_rubric_level IS 'Level penilaian dalam rubric';
COMMENT ON COLUMN master_rubric_level.level_code IS 'Kode level: 1, 2, 3, 4 atau MB, SB, BSH, SAB';
COMMENT ON COLUMN master_rubric_level.level_name IS 'Nama level dalam Bahasa Indonesia';
COMMENT ON COLUMN master_rubric_level.point_value IS 'Nilai numerik untuk level ini';
COMMENT ON COLUMN master_rubric_level.min_percentage IS 'Persentase minimum untuk level ini';
COMMENT ON COLUMN master_rubric_level.max_percentage IS 'Persentase maksimum untuk level ini';
COMMENT ON COLUMN master_rubric_level.color IS 'Kode warna untuk visualisasi (opsional)';

-- RubricCriteriaLevel Table
-- Specific descriptions for each criteria at each level
CREATE TABLE IF NOT EXISTS master_rubric_criteria_level (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    criteria_id UUID NOT NULL,
    level_id UUID NOT NULL,
    description TEXT NOT NULL,
    examples TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for rubric_criteria_level
CREATE INDEX IF NOT EXISTS idx_rubric_criteria_level_criteria ON master_rubric_criteria_level(criteria_id);
CREATE INDEX IF NOT EXISTS idx_rubric_criteria_level_level ON master_rubric_criteria_level(level_id);
CREATE INDEX IF NOT EXISTS idx_rubric_criteria_level_deleted_at ON master_rubric_criteria_level(deleted_at);

-- Add unique constraint to prevent duplicate criteria-level combinations
ALTER TABLE master_rubric_criteria_level 
ADD CONSTRAINT uq_criteria_level UNIQUE (criteria_id, level_id);

-- Add comments for documentation
COMMENT ON TABLE master_rubric_criteria_level IS 'Deskripsi kriteria pada setiap level penilaian';
COMMENT ON COLUMN master_rubric_criteria_level.description IS 'Deskripsi bagaimana kriteria ini terlihat pada level ini';
COMMENT ON COLUMN master_rubric_criteria_level.examples IS 'Contoh untuk kriteria pada level ini (opsional)';
