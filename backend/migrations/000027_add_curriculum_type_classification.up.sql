-- Migration: Add curriculum type classification and co/extra-curricular tables
-- Description: Add Kurikulum Merdeka curriculum classification (intra/co/extra-curricular)
-- Created: 2024-05-24

-- Add curriculum_type column to trx_curriculum_document
ALTER TABLE trx_curriculum_document 
ADD COLUMN IF NOT EXISTS curriculum_type VARCHAR(20) NOT NULL DEFAULT 'INTRAKURIKULER';

-- Create index for curriculum type
CREATE INDEX IF NOT EXISTS idx_curriculum_type ON trx_curriculum_document(curriculum_type) WHERE deleted_at IS NULL;

-- Add comment
COMMENT ON COLUMN trx_curriculum_document.curriculum_type IS 'Curriculum type: INTRAKURIKULER, KOKURIKULER, EKSTRAKURIKULER';

-- Create trx_kokurikuler_activity table
CREATE TABLE IF NOT EXISTS trx_kokurikuler_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    curriculum_document_id UUID NOT NULL,
    activity_name VARCHAR(100) NOT NULL,
    linked_subject_id UUID,
    description TEXT,
    schedule TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for trx_kokurikuler_activity
CREATE INDEX IF NOT EXISTS idx_kokurikuler_document ON trx_kokurikuler_activity(curriculum_document_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_kokurikuler_subject ON trx_kokurikuler_activity(linked_subject_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE trx_kokurikuler_activity
ADD CONSTRAINT fk_kokurikuler_document
FOREIGN KEY (curriculum_document_id) REFERENCES trx_curriculum_document(id) ON DELETE CASCADE;

ALTER TABLE trx_kokurikuler_activity
ADD CONSTRAINT fk_kokurikuler_subject
FOREIGN KEY (linked_subject_id) REFERENCES master_subject(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE trx_kokurikuler_activity IS 'Co-curricular activities that support main curriculum';
COMMENT ON COLUMN trx_kokurikuler_activity.linked_subject_id IS 'Related subject for this co-curricular activity';

-- Create trx_ekstrakurikuler_activity table
CREATE TABLE IF NOT EXISTS trx_ekstrakurikuler_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    curriculum_document_id UUID NOT NULL,
    activity_name VARCHAR(100) NOT NULL,
    activity_category VARCHAR(50),
    description TEXT,
    schedule TEXT,
    instructor_id UUID,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for trx_ekstrakurikuler_activity
CREATE INDEX IF NOT EXISTS idx_ekstrakurikuler_document ON trx_ekstrakurikuler_activity(curriculum_document_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_ekstrakurikuler_category ON trx_ekstrakurikuler_activity(activity_category) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_ekstrakurikuler_instructor ON trx_ekstrakurikuler_activity(instructor_id) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE trx_ekstrakurikuler_activity
ADD CONSTRAINT fk_ekstrakurikuler_document
FOREIGN KEY (curriculum_document_id) REFERENCES trx_curriculum_document(id) ON DELETE CASCADE;

ALTER TABLE trx_ekstrakurikuler_activity
ADD CONSTRAINT fk_ekstrakurikuler_instructor
FOREIGN KEY (instructor_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE trx_ekstrakurikuler_activity IS 'Extra-curricular activities outside the main curriculum';
COMMENT ON COLUMN trx_ekstrakurikuler_activity.activity_category IS 'Category: OLAHRAGA, SENI, ORGANISASI, LAINNYA';
COMMENT ON COLUMN trx_ekstrakurikuler_activity.instructor_id IS 'Instructor or coach for this activity';

-- Insert sample co-curricular activities
INSERT INTO trx_kokurikuler_activity (activity_name, description, linked_subject_id, schedule, is_active) VALUES
('Penguatan Literasi dan Numerasi', 'Kegiatan tambahan untuk memperkuat kemampuan dasar membaca dan berhitung', NULL, 'Pagi hari (07:00-08:00)', true),
('Pendidikan Karakter', 'Pembentukan karakter dan budi pekerti siswa', NULL, 'Setiap hari Jumat (13:00-15:00)', true),
('Bimbingan Belajar', 'Bimbingan tambahan untuk siswa yang membutuhkan dukungan', NULL, 'Setelah pelajaran (15:00-16:30)', true);

-- Insert sample extra-curricular activities
INSERT INTO trx_ekstrakurikuler_activity (activity_name, activity_category, description, schedule, is_active) VALUES
('Pramuka', 'ORGANISASI', 'Kegiatan kepramukaan untuk melatih kemandirian dan kedisiplinan', 'Setiap hari Sabtu (08:00-12:00)', true),
('Seni Tari Daerah', 'SENI', 'Mempelajari tari tradisional daerah setempat', 'Setiap hari Selasa (15:00-16:30)', true),
('Futsal Sekolah', 'OLAHRAGA', 'Latihan futsal untuk kesehatan dan kerjasama tim', 'Setiap hari Kamis (15:00-16:30)', true),
('Paduan Suara', 'SENIMUSIK', 'Latihan menyanyi paduan suara', 'Setiap hari Rabu (15:00-16:30)', true),
('Pecinta Alam', 'ORGANISASI', 'Kegiatan cinta alam dan lingkungan', 'Setiap hari Jumat (15:00-16:30)', true);
