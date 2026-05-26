-- Migration: Create Lesson Planning Tables
-- Created: 2026-05-25
-- Description: This migration creates tables for comprehensive lesson planning system including lesson plans, templates, sections, and resources

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Lesson Plan Table
-- Comprehensive lesson plan (RPP) storage
CREATE TABLE IF NOT EXISTS master_lesson_plan (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    subject_id UUID,
    classroom_id UUID,
    atp_id UUID,
    teaching_module_id UUID,
    template_id UUID,
    meeting_date VARCHAR(50),
    meeting_number INTEGER DEFAULT 1,
    duration_minutes INTEGER DEFAULT 45,
    learning_objectives TEXT,
    core_material TEXT,
    teaching_methods TEXT,
    assessment_methods TEXT,
    status VARCHAR(20) DEFAULT 'DRAFT',
    version INTEGER DEFAULT 1,
    academic_year_id UUID,
    semester INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for lesson_plan
CREATE INDEX IF NOT EXISTS idx_lesson_plan_subject ON master_lesson_plan(subject_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_classroom ON master_lesson_plan(classroom_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_atp ON master_lesson_plan(atp_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_teaching_module ON master_lesson_plan(teaching_module_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_template ON master_lesson_plan(template_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_status ON master_lesson_plan(status);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_academic_year ON master_lesson_plan(academic_year_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_deleted_at ON master_lesson_plan(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_lesson_plan IS 'Rencana Pembelajaran (RPP) komprehensif';
COMMENT ON COLUMN master_lesson_plan.meeting_date IS 'Tanggal pertemuan (misal: Pertemuan 1, 2 Mei)';
COMMENT ON COLUMN master_lesson_plan.meeting_number IS 'Nomor urut pertemuan';
COMMENT ON COLUMN master_lesson_plan.duration_minutes IS 'Durasi pembelajaran dalam menit';
COMMENT ON COLUMN master_lesson_plan.learning_objectives IS 'Tujuan pembelajaran';
COMMENT ON COLUMN master_lesson_plan.core_material IS 'Materi pokok';
COMMENT ON COLUMN master_lesson_plan.teaching_methods IS 'Metode pembelajaran (comma-separated)';
COMMENT ON COLUMN master_lesson_plan.assessment_methods IS 'Metode penilaian (comma-separated)';
COMMENT ON COLUMN master_lesson_plan.status IS 'Status: DRAFT, REVIEW, APPROVED, PUBLISHED';
COMMENT ON COLUMN master_lesson_plan.version IS 'Versi RPP untuk tracking perubahan';

-- Add check constraints
ALTER TABLE master_lesson_plan 
ADD CONSTRAINT chk_lesson_plan_status 
CHECK (status IN ('DRAFT', 'REVIEW', 'APPROVED', 'PUBLISHED'));

ALTER TABLE master_lesson_plan 
ADD CONSTRAINT chk_lesson_plan_semester 
CHECK (semester IN (1, 2));

-- Lesson Plan Template Table
-- Reusable lesson plan templates
CREATE TABLE IF NOT EXISTS master_lesson_plan_template (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id UUID,
    grade_level VARCHAR(50),
    category VARCHAR(100),
    default_duration_minutes INTEGER DEFAULT 45,
    default_sections TEXT,
    is_active BOOLEAN DEFAULT true,
    is_system BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for lesson_plan_template
CREATE INDEX IF NOT EXISTS idx_lesson_plan_template_subject ON master_lesson_plan_template(subject_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_template_grade_level ON master_lesson_plan_template(grade_level);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_template_category ON master_lesson_plan_template(category);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_template_is_active ON master_lesson_plan_template(is_active);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_template_deleted_at ON master_lesson_plan_template(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_lesson_plan_template IS 'Template Rencana Pembelajaran untuk reuse';
COMMENT ON COLUMN master_lesson_plan_template.grade_level IS 'Tingkat kelas: 1-6, LOWER (1-3), UPPER (4-6), ALL';
COMMENT ON COLUMN master_lesson_plan_template.category IS 'Kategori template (misal: Numerasi, Literasi, P5)';
COMMENT ON COLUMN master_lesson_plan_template.default_sections IS 'Default sections dalam JSON format';
COMMENT ON COLUMN master_lesson_plan_template.is_system IS 'Template sistem vs template user';

-- Lesson Plan Section Table
-- Sections of a lesson plan
CREATE TABLE IF NOT EXISTS master_lesson_plan_section (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lesson_plan_id UUID NOT NULL,
    section_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    duration_minutes INTEGER DEFAULT 10,
    sequence INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for lesson_plan_section
CREATE INDEX IF NOT EXISTS idx_lesson_plan_section_lesson_plan ON master_lesson_plan_section(lesson_plan_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_section_type ON master_lesson_plan_section(section_type);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_section_sequence ON master_lesson_plan_section(sequence);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_section_deleted_at ON master_lesson_plan_section(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_lesson_plan_section IS 'Bagian-bagian RPP (Pendahuluan, Kegiatan Inti, Penutup, dll)';
COMMENT ON COLUMN master_lesson_plan_section.section_type IS 'Tipe bagian: OPENING, CORE_ACTIVITY, CLOSING, ASSESSMENT, REFLECTION';
COMMENT ON COLUMN master_lesson_plan_section.duration_minutes IS 'Durasi bagian dalam menit';
COMMENT ON COLUMN master_lesson_plan_section.sequence IS 'Urutan bagian dalam RPP';

-- Add check constraint for section_type
ALTER TABLE master_lesson_plan_section 
ADD CONSTRAINT chk_section_type 
CHECK (section_type IN ('PENDAHULUAN', 'KEGIATAN_INTI', 'PENUTUP', 'ASESMEN', 'REFLEKSI'));

-- Lesson Plan Resource Table
-- Resources/media used in lesson plans
CREATE TABLE IF NOT EXISTS master_lesson_plan_resource (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lesson_plan_id UUID NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    url VARCHAR(500),
    file_path VARCHAR(500),
    file_size BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for lesson_plan_resource
CREATE INDEX IF NOT EXISTS idx_lesson_plan_resource_lesson_plan ON master_lesson_plan_resource(lesson_plan_id);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_resource_type ON master_lesson_plan_resource(resource_type);
CREATE INDEX IF NOT EXISTS idx_lesson_plan_resource_deleted_at ON master_lesson_plan_resource(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_lesson_plan_resource IS 'Sumber daya/media yang digunakan dalam RPP';
COMMENT ON COLUMN master_lesson_plan_resource.resource_type IS 'Tipe sumber daya: MATERIAL, MEDIA, TOOL, REFERENCE';
COMMENT ON COLUMN master_lesson_plan_resource.url IS 'URL ke sumber daya eksternal';
COMMENT ON COLUMN master_lesson_plan_resource.file_path IS 'Path file lokal';
COMMENT ON COLUMN master_lesson_plan_resource.file_size IS 'Ukuran file dalam bytes';
COMMENT ON COLUMN master_lesson_plan_resource.mime_type IS 'Tipe MIME file';

-- Add check constraint for resource_type
ALTER TABLE master_lesson_plan_resource 
ADD CONSTRAINT chk_resource_type 
CHECK (resource_type IN ('MATERI', 'MEDIA', 'ALAT', 'REFERENSI'));
