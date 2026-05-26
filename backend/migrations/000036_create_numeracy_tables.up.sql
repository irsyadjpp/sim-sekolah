-- Migration: Create numeracy assessment tables
-- Description: Create tables for numeracy (mathematics) assessment, tracking, and growth for SD Kurikulum Merdeka
-- Created: 2025-05-25

-- Create numeracy_indicators table
CREATE TABLE IF NOT EXISTS numeracy_indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phase_id UUID NOT NULL,
    numeracy_type VARCHAR(20) NOT NULL,
    indicator_code VARCHAR(20) UNIQUE NOT NULL,
    indicator_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    grade_level VARCHAR(10),
    min_age INT,
    max_age INT,
    difficulty VARCHAR(10),
    examples TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for numeracy_indicators
CREATE INDEX IF NOT EXISTS idx_numeracy_indicators_phase ON numeracy_indicators(phase_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_indicators_type ON numeracy_indicators(numeracy_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_indicators_grade ON numeracy_indicators(grade_level) WHERE deleted_at IS NULL;

-- Add foreign key constraint
ALTER TABLE numeracy_indicators
ADD CONSTRAINT fk_numeracy_indicators_phase
FOREIGN KEY (phase_id) REFERENCES master_phase(id) ON DELETE CASCADE;

-- Add comments
COMMENT ON TABLE numeracy_indicators IS 'Master table for numeracy learning indicators per phase';
COMMENT ON COLUMN numeracy_indicators.numeracy_type IS 'Type of numeracy: NUMBERS, OPERATIONS, GEOMETRY, MEASUREMENT, DATA_ANALYSIS';
COMMENT ON COLUMN numeracy_indicators.indicator_code IS 'Unique code for the numeracy indicator';
COMMENT ON COLUMN numeracy_indicators.difficulty IS 'Difficulty level: LOW, MEDIUM, HIGH';
COMMENT ON COLUMN numeracy_indicators.examples IS 'JSON array of example problems';

-- Create numeracy_assessments table
CREATE TABLE IF NOT EXISTS numeracy_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    indicator_id UUID NOT NULL,
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(20) NOT NULL,
    score NUMERIC(5,2),
    mastery_level VARCHAR(20) NOT NULL,
    response_time INT,
    attempts INT DEFAULT 1,
    teacher_id UUID,
    notes TEXT,
    evidence_files TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for numeracy_assessments
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_student ON numeracy_assessments(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_indicator ON numeracy_assessments(indicator_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_date ON numeracy_assessments(assessment_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_type ON numeracy_assessments(assessment_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_mastery ON numeracy_assessments(mastery_level) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_assessments_teacher ON numeracy_assessments(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE numeracy_assessments
ADD CONSTRAINT fk_numeracy_assessments_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE numeracy_assessments
ADD CONSTRAINT fk_numeracy_assessments_indicator
FOREIGN KEY (indicator_id) REFERENCES numeracy_indicators(id) ON DELETE CASCADE;

ALTER TABLE numeracy_assessments
ADD CONSTRAINT fk_numeracy_assessments_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE numeracy_assessments IS 'Transaction table for individual numeracy assessment results';
COMMENT ON COLUMN numeracy_assessments.assessment_type IS 'Type of assessment: DIAGNOSTIC, FORMATIVE, SUMMATIVE';
COMMENT ON COLUMN numeracy_assessments.mastery_level IS 'Mastery level: BELUM, SEDANG, MENGUASAI';
COMMENT ON COLUMN numeracy_assessments.response_time IS 'Response time in seconds';
COMMENT ON COLUMN numeracy_assessments.evidence_files IS 'JSON array of evidence file paths';

-- Create numeracy_growth table
CREATE TABLE IF NOT EXISTS numeracy_growth (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    period VARCHAR(20) NOT NULL,
    academic_year_id UUID NOT NULL,
    overall_score NUMERIC(5,2),
    numbers_score NUMERIC(5,2),
    operations_score NUMERIC(5,2),
    geometry_score NUMERIC(5,2),
    measurement_score NUMERIC(5,2),
    data_analysis_score NUMERIC(5,2),
    mastery_rate NUMERIC(5,2),
    growth_rate NUMERIC(5,2),
    percentile INT,
    teacher_id UUID,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    UNIQUE(student_id, period, academic_year_id)
);

-- Create indexes for numeracy_growth
CREATE INDEX IF NOT EXISTS idx_numeracy_growth_student ON numeracy_growth(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_growth_period ON numeracy_growth(period) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_growth_academic_year ON numeracy_growth(academic_year_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_growth_teacher ON numeracy_growth(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE numeracy_growth
ADD CONSTRAINT fk_numeracy_growth_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE numeracy_growth
ADD CONSTRAINT fk_numeracy_growth_academic_year
FOREIGN KEY (academic_year_id) REFERENCES master_academic_year(id) ON DELETE CASCADE;

ALTER TABLE numeracy_growth
ADD CONSTRAINT fk_numeracy_growth_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE numeracy_growth IS 'Summary table for student numeracy growth per period';
COMMENT ON COLUMN numeracy_growth.period IS 'Period: SEMESTER_1, SEMESTER_2';
COMMENT ON COLUMN numeracy_growth.mastery_rate IS 'Percentage of indicators mastered (0-100)';
COMMENT ON COLUMN numeracy_growth.growth_rate IS 'Growth rate from previous period';
COMMENT ON COLUMN numeracy_growth.percentile IS 'National percentile rank';

-- Create numeracy_interventions table
CREATE TABLE IF NOT EXISTS numeracy_interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    indicator_id UUID NOT NULL,
    intervention_type VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) NOT NULL,
    activities TEXT,
    teacher_id UUID,
    outcome TEXT,
    effectiveness VARCHAR(10),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Create indexes for numeracy_interventions
CREATE INDEX IF NOT EXISTS idx_numeracy_interventions_student ON numeracy_interventions(student_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_interventions_indicator ON numeracy_interventions(indicator_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_interventions_type ON numeracy_interventions(intervention_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_interventions_status ON numeracy_interventions(status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_interventions_dates ON numeracy_interventions(start_date, end_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_numeracy_interventions_teacher ON numeracy_interventions(teacher_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE numeracy_interventions
ADD CONSTRAINT fk_numeracy_interventions_student
FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE numeracy_interventions
ADD CONSTRAINT fk_numeracy_interventions_indicator
FOREIGN KEY (indicator_id) REFERENCES numeracy_indicators(id) ON DELETE CASCADE;

ALTER TABLE numeracy_interventions
ADD CONSTRAINT fk_numeracy_interventions_teacher
FOREIGN KEY (teacher_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE numeracy_interventions IS 'Remedial and enrichment activities for numeracy';
COMMENT ON COLUMN numeracy_interventions.intervention_type IS 'Type: REMEDIAL, ENRICHMENT';
COMMENT ON COLUMN numeracy_interventions.status IS 'Status: PLANNED, ONGOING, COMPLETED';
COMMENT ON COLUMN numeracy_interventions.activities IS 'JSON array of intervention activities';
COMMENT ON COLUMN numeracy_interventions.effectiveness IS 'Effectiveness: LOW, MEDIUM, HIGH';

-- Seed initial numeracy indicators for SD phases
-- Fase A (Kelas 1-2)
INSERT INTO numeracy_indicators (phase_id, numeracy_type, indicator_code, indicator_name, description, grade_level, min_age, max_age, difficulty, examples) VALUES
-- Select phase IDs from master_phase table (will be populated in actual deployment)
-- For Fase A - Numeracy: Numbers
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'NUMBERS', 'N-F1-01', 'Mengenal Bilangan 1-10', 'Siswa dapat mengenal dan menyebutkan bilangan 1-10', '1', 6, 7, 'LOW', '["Menghitung objek", "Menulis angka"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'NUMBERS', 'N-F1-02', 'Mengenal Bilangan 11-20', 'Siswa dapat mengenal dan menyebutkan bilangan 11-20', '1', 6, 7, 'MEDIUM', '["Menghitung kelompok", "Menulis angka"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'NUMBERS', 'N-F2-01', 'Mengenal Bilangan sampai 100', 'Siswa dapat mengenal bilangan sampai 100', '2', 7, 8, 'MEDIUM', '["Menghitung berurutan", "Membilang objek"]'),

-- Fase A - Operations
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'OPERATIONS', 'O-F1-01', 'Penjumlahan Sederhana', 'Siswa dapat melakukan penjumlahan sederhana', '1', 6, 7, 'LOW', '["1 + 1", "2 + 3"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'OPERATIONS', 'O-F1-02', 'Pengurangan Sederhana', 'Siswa dapat melakukan pengurangan sederhana', '1', 6, 7, 'LOW', '["3 - 1", "5 - 2"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'OPERATIONS', 'O-F2-01', 'Penjumlahan dan Pengurangan', 'Siswa dapat melakukan penjumlahan dan pengurangan', '2', 7, 8, 'MEDIUM', '["10 + 5", "15 - 7"]'),

-- Fase A - Geometry
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'GEOMETRY', 'G-F1-01', 'Mengenal Bangun Datar Sederhana', 'Siswa dapat mengenal bangun datar sederhana', '1', 6, 7, 'LOW', '["Persegi", "Lingkaran", "Segitiga"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_A' LIMIT 1), 'GEOMETRY', 'G-F2-01', 'Mengenal Bangun Ruang Sederhana', 'Siswa dapat mengenal bangun ruang sederhana', '2', 7, 8, 'MEDIUM', '["Kubus", "Bola", "Tabung"]'),

-- Fase B (Kelas 3-4)
-- Fase B - Numbers
((SELECT id FROM master_phase WHERE phase_code = 'FASE_B' LIMIT 1), 'NUMBERS', 'N-F3-01', 'Mengenal Bilangan sampai 1000', 'Siswa dapat mengenal bilangan sampai 1000', '3', 8, 9, 'MEDIUM', '["Membilang ratusan", "Menulis angka besar"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_B' LIMIT 1), 'NUMBERS', 'N-F4-01', 'Mengenal Bilangan sampai 10000', 'Siswa dapat mengenal bilangan sampai 10000', '4', 9, 10, 'MEDIUM', '["Nilai tempat", "Membandingkan bilangan"]'),

-- Fase B - Operations
((SELECT id FROM master_phase WHERE phase_code = 'FASE_B' LIMIT 1), 'OPERATIONS', 'O-F3-01', 'Perkalian Dasar', 'Siswa dapat melakukan perkalian dasar', '3', 8, 9, 'MEDIUM', '["2 x 3", "5 x 4"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_B' LIMIT 1), 'OPERATIONS', 'O-F4-01', 'Pembagian Dasar', 'Siswa dapat melakukan pembagian dasar', '4', 9, 10, 'MEDIUM', '["12 : 3", "20 : 4"]'),

-- Fase C (Kelas 5-6)
-- Fase C - Numbers
((SELECT id FROM master_phase WHERE phase_code = 'FASE_C' LIMIT 1), 'NUMBERS', 'N-F5-01', 'Operasi Bilangan Bulat', 'Siswa dapat melakukan operasi bilangan bulat', '5', 10, 11, 'HIGH', '["Penjumlahan negatif", "Pengurangan negatif"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_C' LIMIT 1), 'NUMBERS', 'N-F6-01', 'Pecahan dan Desimal', 'Siswa dapat memahami pecahan dan desimal', '6', 11, 12, 'HIGH', '["Konversi pecahan", "Operasi desimal"]'),

-- Fase C - Operations
((SELECT id FROM master_phase WHERE phase_code = 'FASE_C' LIMIT 1), 'OPERATIONS', 'O-F5-01', 'Operasi Campuran', 'Siswa dapat melakukan operasi campuran', '5', 10, 11, 'HIGH', '["Penjumlahan pecahan", "Perkalian desimal"]'),
((SELECT id FROM master_phase WHERE phase_code = 'FASE_C' LIMIT 1), 'OPERATIONS', 'O-F6-01', 'Penerapan Operasi dalam Masalah', 'Siswa dapat menerapkan operasi dalam masalah nyata', '6', 11, 12, 'HIGH', '["Cerita matematika", "Pemecahan masalah"]');

ON CONFLICT (indicator_code) DO NOTHING;