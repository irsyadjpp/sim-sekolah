-- Migration: Enhance ATP (Alur Tujuan Pembelajaran) Table
-- Created: 2026-05-25
-- Description: This migration enhances the trx_atp and trx_atp_detail tables with meeting estimation, learning flow, and better ATP management

-- Add new columns to trx_atp table
ALTER TABLE trx_atp 
ADD COLUMN IF NOT EXISTS title VARCHAR(200) NOT NULL DEFAULT 'ATP Default',
ADD COLUMN IF NOT EXISTS academic_year_id UUID,
ADD COLUMN IF NOT EXISTS semester INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS total_meetings INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_hours DECIMAL(5,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'DRAFT',
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

-- Add indexes for new columns
CREATE INDEX IF NOT EXISTS idx_atp_academic_year ON trx_atp(academic_year_id);
CREATE INDEX IF NOT EXISTS idx_atp_semester ON trx_atp(semester);
CREATE INDEX IF NOT EXISTS idx_atp_status ON trx_atp(status);
CREATE INDEX IF NOT EXISTS idx_atp_version ON trx_atp(version);

-- Add comments for documentation
COMMENT ON COLUMN trx_atp.title IS 'Judul ATP untuk identifikasi yang lebih baik';
COMMENT ON COLUMN trx_atp.academic_year_id IS 'Tahun akademik terkait';
COMMENT ON COLUMN trx_atp.semester IS 'Semester: 1 atau 2';
COMMENT ON COLUMN trx_atp.total_meetings IS 'Total estimasi pertemuan untuk ATP';
COMMENT ON COLUMN trx_atp.total_hours IS 'Total jam pembelajaran untuk ATP';
COMMENT ON COLUMN trx_atp.status IS 'Status ATP: DRAFT, APPROVED, PUBLISHED';
COMMENT ON COLUMN trx_atp.version IS 'Versi ATP untuk tracking perubahan';

-- Add check constraint for semester
ALTER TABLE trx_atp 
ADD CONSTRAINT chk_semester 
CHECK (semester IN (1, 2));

-- Add check constraint for status
ALTER TABLE trx_atp 
ADD CONSTRAINT chk_atp_status 
CHECK (status IN ('DRAFT', 'APPROVED', 'PUBLISHED'));

-- Add new columns to trx_atp_detail table
ALTER TABLE trx_atp_detail 
ADD COLUMN IF NOT EXISTS meeting_number INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS estimated_hours DECIMAL(5,2) DEFAULT 1.0,
ADD COLUMN IF NOT EXISTS learning_flow VARCHAR(50);

-- Add index for new columns
CREATE INDEX IF NOT EXISTS idx_atp_detail_meeting_number ON trx_atp_detail(meeting_number);
CREATE INDEX IF NOT EXISTS idx_atp_detail_learning_flow ON trx_atp_detail(learning_flow);

-- Add comments for documentation
COMMENT ON COLUMN trx_atp_detail.meeting_number IS 'Nomor pertemuan ketika TP ini diajarkan';
COMMENT ON COLUMN trx_atp_detail.estimated_hours IS 'Alokasi waktu untuk TP ini (jam)';
COMMENT ON COLUMN trx_atp_detail.learning_flow IS 'Alur pembelajaran: INTRODUCTORY, DEVELOPMENT, PRACTICE, ASSESSMENT, REINFORCEMENT';

-- Add check constraint for learning_flow
ALTER TABLE trx_atp_detail 
ADD CONSTRAINT chk_learning_flow 
CHECK (learning_flow IS NULL OR learning_flow IN ('INTRODUCTORY', 'DEVELOPMENT', 'PRACTICE', 'ASSESSMENT', 'REINFORCEMENT'));
