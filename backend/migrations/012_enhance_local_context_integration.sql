-- Migration: Phase 3 - Local Context Integration Enhancements
-- Description: Enhances local context integration with subjects and modules

-- Add local context linkage to subjects
ALTER TABLE master_subject 
ADD COLUMN IF NOT EXISTS local_context_ids UUID[];

-- Create index for local context lookup
CREATE INDEX IF NOT EXISTS idx_subject_local_context ON master_subject USING GIN(local_context_ids);

-- Add local context linkage to teaching modules
ALTER TABLE trx_teaching_module
ADD COLUMN IF NOT EXISTS local_context_ids UUID[];

-- Create index for module context lookup
CREATE INDEX IF NOT EXISTS idx_module_local_context ON trx_teaching_module USING GIN(local_context_ids);

-- Add context utilization tracking table
CREATE TABLE IF NOT EXISTS trx_local_context_utilization (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    context_id UUID NOT NULL,
    subject_id UUID,
    module_id UUID,
    utilization_type VARCHAR(30) NOT NULL,  -- EXAMPLE, CASE_STUDY, PROJECT_BASE, RESOURCE
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_utilization_context FOREIGN KEY (context_id) REFERENCES master_local_context(id) ON DELETE CASCADE,
    CONSTRAINT fk_utilization_subject FOREIGN KEY (subject_id) REFERENCES master_subject(id) ON DELETE CASCADE,
    CONSTRAINT fk_utilization_module FOREIGN KEY (module_id) REFERENCES trx_teaching_module(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_utilization_context ON trx_local_context_utilization(context_id);
CREATE INDEX idx_utilization_subject ON trx_local_context_utilization(subject_id);
CREATE INDEX idx_utilization_module ON trx_local_context_utilization(module_id);
CREATE INDEX idx_utilization_type ON trx_local_context_utilization(utilization_type);

-- Add kepulauan-specific local contexts if they don't exist
INSERT INTO master_local_context (context_code, context_name, context_category, description, examples, is_active) VALUES
('KEPULAUAN_SAYA', 'Kepulauan Selayar', 'GEOGRAPHY', 'Konteks geografis kepulauan Selayar sebagai rumah belajar', '["Pembelajaran tentang lingkungan laut", "Studi kasus budaya lokal", "Proyek pelestarian ekosistem"]', true),
('BUDAYA_BUGIS', 'Budaya Bugis', 'CULTURE', 'Konteks budaya Bugis untuk pembelajaran karakter', '["Pembelajaran nilai luhur Bugis", "Tradisi lokal dalam mata pelajaran", "Karakter gotong royong"]', true),
('MATA_PENCAHARIAN', 'Mata Pencaharian Tradisional', 'LIVELIHOOD', 'Konteks mata pencaharian masyarakat kepulauan', '["Matematika dalam pencaharian", "Sains dalam lingkungan laut", "Kewirausahaan lokal"]', true),
('SAMPAN_TANI', 'Sampah Tani dan Perkebunan', 'AGRICULTURE', 'Konteks pertanian khas pulau', '["Biologi tentang tanaman lokal", "Matematika dalam pertanian", "Proyek sekolah hijau"]', true)
ON CONFLICT (context_code) DO NOTHING;
