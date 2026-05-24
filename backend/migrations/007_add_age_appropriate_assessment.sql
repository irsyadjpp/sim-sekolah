-- Migration: Add age-appropriate assessment types for SD
-- Description: Add SD-specific assessment classification and criteria tables
-- Created: 2024-05-24

-- Add age_appropriate_type column to trx_assessment
ALTER TABLE trx_assessment 
ADD COLUMN IF NOT EXISTS age_appropriate_type VARCHAR(30);

-- Create index for age appropriate type
CREATE INDEX IF NOT EXISTS idx_assessment_age_appropriate ON trx_assessment(age_appropriate_type) WHERE deleted_at IS NULL;

-- Add comment
COMMENT ON COLUMN trx_assessment.age_appropriate_type IS 'SD-specific age-appropriate assessment type: FASE_A_OBSERVATION, FASE_A_PORTFOLIO, FASE_B_PERFORMANCE, FASE_B_PROJECT, FASE_C_PROJECT_COMPLEX, FASE_C_COLLABORATIVE, FASE_C_PEER_ASSESSMENT';

-- Create master_sd_assessment_criteria table
CREATE TABLE IF NOT EXISTS master_sd_assessment_criteria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_type VARCHAR(30) NOT NULL,
    phase_id UUID,
    criteria_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    rubric_elements JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Create indexes for master_sd_assessment_criteria
CREATE INDEX IF NOT EXISTS idx_sd_criteria_type ON master_sd_assessment_criteria(assessment_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_sd_criteria_phase ON master_sd_assessment_criteria(phase_id) WHERE deleted_at IS NULL;

-- Add foreign key constraint
ALTER TABLE master_sd_assessment_criteria
ADD CONSTRAINT fk_sd_criteria_phase
FOREIGN KEY (phase_id) REFERENCES master_phase(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE master_sd_assessment_criteria IS 'Master table for SD-specific assessment criteria per phase and assessment type';
COMMENT ON COLUMN master_sd_assessment_criteria.assessment_type IS 'Age-appropriate assessment type for SD';
COMMENT ON COLUMN master_sd_assessment_criteria.rubric_elements IS 'JSON rubric elements for assessment criteria';

-- Insert standard SD assessment criteria
INSERT INTO master_sd_assessment_criteria (assessment_type, criteria_name, description, rubric_elements, is_active) VALUES
-- Fase A Criteria
('FASE_A_OBSERVATION', 'Partisipasi dalam Bermain', 'Siswa aktif berpartisipasi dalam kegiatan bermain', '{"levels": [{"name": "Belum", "description": "Siswa pasif dalam kegiatan"}, {"name": "Sedang", "description": "Siswa kadang-kadang berpartisipasi"}, {"name": "Menguasai", "description": "Siswa sangat aktif dan antusias"}]}', true),
('FASE_A_OBSERVATION', 'Kerjasama dengan Teman', 'Siswa dapat bekerja sama dalam kegiatan kelompok sederhana', '{"levels": [{"name": "Belum", "description": "Suka bermain sendiri"}, {"name": "Sedang", "description": "Kadang bermain bersama"}, {"name": "Menguasai", "description": "Senang bermain dan bekerja sama"}]}', true),
('FASE_A_PORTFOLIO', 'Kumpulan Karya', 'Portofolio berisi karya-karya siswa yang menunjukkan perkembangan', '{"elements": ["Lukisan", "Kerajinan tangan", "Tulisan sederhana", "Proyek kelas"]}', true),

-- Fase B Criteria
('FASE_B_PERFORMANCE', 'Kemampuan Presentasi', 'Siswa dapat mempresentasikan hasil kerja sederhana', '{"levels": [{"name": "Belum", "description": "Sangat ragu-ragu"}, {"name": "Sedang", "description": "Cukup lancar dengan bantuan"}, {"name": "Menguasai", "description": "Percaya diri dan lancar"}]}', true),
('FASE_B_PERFORMANCE', 'Pemahaman Konsep', 'Siswa mendemonstrasikan pemahaman konsep dasar', '{"levels": [{"name": "Belum", "description": "Memahami sangat terbatas"}, {"name": "Sedang", "description": "Memahami sebagian"}, {"name": "Menguasai", "description": "Memahami dengan baik"}]}', true),
('FASE_B_PROJECT', 'Penyelesaian Tugas', 'Siswa dapat menyelesaikan proyek sederhana dengan bimbingan', '{"criteria": ["Perencanaan", "Pelaksanaan", "Hasil akhir"]}', true),

-- Fase C Criteria
('FASE_C_PROJECT_COMPLEX', 'Analisis Masalah', 'Siswa dapat menganalisis masalah dalam proyek kompleks', '{"levels": [{"name": "Belum", "description": "Membutuhkan bantuan penuh"}, {"name": "Sedang", "description": "Dapat menganalisis dengan bimbingan"}, {"name": "Menguasai", "description": "Dapat menganalisis secara mandiri"}]}', true),
('FASE_C_PROJECT_COMPLEX', 'Kreativitas Solusi', 'Siswa memberikan solusi yang kreatif untuk masalah', '{"levels": [{"name": "Belum", "description": "Solusi umum saja"}, {"name": "Sedang", "description": "Ada ide-ide kreatif"}, {"name": "Menguasai", "description": "Solusi sangat kreatif dan inovatif"}]}', true),
('FASE_C_COLLABORATIVE', 'Kontribusi Tim', 'Kontribusi aktif dalam kerja tim', '{"levels": [{"name": "Belum", "description": "Kontribusi minimal"}, {"name": "Sedang", "description": "Kontribusi cukup baik"}, {"name": "Menguasai", "description": "Kontribusi sangat aktif"}]}', true),
('FASE_C_PEER_ASSESSMENT', 'Objektivitas Penilaian', 'Kemampuan menilai teman secara adil dan objektif', '{"levels": [{"name": "Belum", "description": "Sangat subjektif"}, {"name": "Sedang", "description": "Cukup objektif"}, {"name": "Menguasai", "description": "Sangat objektif dan adil"}]}', true);
