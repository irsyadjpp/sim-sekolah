-- Migration: Create Learning Experience Tables
-- Description: Creates tables for learning experience phases, activity mappings, and student progression tracking

-- Create master_learning_experience table
CREATE TABLE IF NOT EXISTS master_learning_experience (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experience_code VARCHAR(10) UNIQUE NOT NULL,  -- MEMAHAMI, MENAPLIKASI, MEREFLEKSI
    experience_name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    sequence_order INT NOT NULL,  -- 1, 2, 3
    key_indicators TEXT,  -- JSON array of indicators
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Create index on experience_code
CREATE INDEX idx_learning_experience_code ON master_learning_experience(experience_code);
-- Create index on is_active
CREATE INDEX idx_learning_experience_active ON master_learning_experience(is_active);
-- Create index on deleted_at
CREATE INDEX idx_learning_experience_deleted ON master_learning_experience(deleted_at);

-- Create trx_activity_experience_mapping table
CREATE TABLE IF NOT EXISTS trx_activity_experience_mapping (
    activity_id UUID NOT NULL,
    experience_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (activity_id, experience_id),
    CONSTRAINT fk_activity_experience_activity FOREIGN KEY (activity_id) REFERENCES trx_teaching_module_activity(id) ON DELETE CASCADE,
    CONSTRAINT fk_activity_experience_experience FOREIGN KEY (experience_id) REFERENCES master_learning_experience(id) ON DELETE CASCADE
);

-- Create index on experience_id
CREATE INDEX idx_activity_experience_experience ON trx_activity_experience_mapping(experience_id);

-- Create trx_student_experience_progression table
CREATE TABLE IF NOT EXISTS trx_student_experience_progression (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL,
    subject_id UUID NOT NULL,
    experience_id UUID NOT NULL,
    mastery_level DECIMAL(3,2) DEFAULT 0,  -- 0.00 to 1.00
    last_assessed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_progression_student FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_student_progression_subject FOREIGN KEY (subject_id) REFERENCES master_subject(id) ON DELETE CASCADE,
    CONSTRAINT fk_student_progression_experience FOREIGN KEY (experience_id) REFERENCES master_learning_experience(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_student_progression_student ON trx_student_experience_progression(student_id);
CREATE INDEX idx_student_progression_subject ON trx_student_experience_progression(subject_id);
CREATE INDEX idx_student_progression_experience ON trx_student_experience_progression(experience_id);
-- Create composite index for student+subject lookups
CREATE INDEX idx_student_progression_student_subject ON trx_student_experience_progression(student_id, subject_id);

-- Seed initial learning experience phases
INSERT INTO master_learning_experience (experience_code, experience_name, description, sequence_order, key_indicators, is_active) VALUES
('MEMAHAMI', 'Memahami', 'Fase memahami konsep dasar dan materi pembelajaran', 1, '["Mampu mengidentifikasi konsep dasar", "Mampu menjelaskan dengan kata-kata sendiri", "Mampu memberikan contoh konkret"]', true),
('MENAPLIKASI', 'Mengaplikasi', 'Fase menerapkan pengetahuan dalam situasi baru', 2, '["Mampu menggunakan konsep dalam konteks berbeda", "Mampu memecahkan masalah sederhana", "Mampu mendemonstrasikan pemahaman"]', true),
('MEREFEKSI', 'Merefleksi', 'Fase merefleksikan pembelajaran dan pengalaman', 3, '["Mampu mengevaluasi proses belajar", "Mampu mengidentifikasi kekuatan dan kelemahan", "Mampu merencanakan perbaikan"]', true)
ON CONFLICT (experience_code) DO NOTHING;

-- Create trigger for updated_at on master_learning_experience
CREATE OR REPLACE FUNCTION update_learning_experience_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_learning_experience_updated_at
    BEFORE UPDATE ON master_learning_experience
    FOR EACH ROW
    EXECUTE FUNCTION update_learning_experience_updated_at();

-- Create trigger for updated_at on trx_student_experience_progression
CREATE TRIGGER trigger_update_student_progression_updated_at
    BEFORE UPDATE ON trx_student_experience_progression
    FOR EACH ROW
    EXECUTE FUNCTION update_learning_experience_updated_at();
