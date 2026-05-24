-- Migration: Phase 3 - Individual Learning Plans Tables
-- Description: Creates tables for SD-appropriate Individual Learning Plans

-- Create ILP table
CREATE TABLE IF NOT EXISTS trx_individual_learning_plan (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL,
    academic_year_id UUID NOT NULL,
    title VARCHAR(150) NOT NULL,
    goals TEXT,  -- JSON array of learning goals
    strategies TEXT,  -- JSON array of learning strategies
    accommodations TEXT,  -- JSON array of special accommodations
    parent_notes TEXT,
    teacher_notes TEXT,
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- ACTIVE, COMPLETED, ARCHIVED
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT fk_ilp_student FOREIGN KEY (student_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_ilp_academic_year FOREIGN KEY (academic_year_id) REFERENCES master_academic_year(id)
);

-- Create indexes
CREATE INDEX idx_ilp_student ON trx_individual_learning_plan(student_id);
CREATE INDEX idx_ilp_academic_year ON trx_individual_learning_plan(academic_year_id);
CREATE INDEX idx_ilp_status ON trx_individual_learning_plan(status);
CREATE INDEX idx_ilp_deleted ON trx_individual_learning_plan(deleted_at);

-- Create ILP milestone table
CREATE TABLE IF NOT EXISTS trx_ilp_milestone (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ilp_id UUID NOT NULL,
    milestone_name VARCHAR(100) NOT NULL,
    target_date DATE NOT NULL,
    achieved BOOLEAN DEFAULT false,
    achieved_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_milestone_ilp FOREIGN KEY (ilp_id) REFERENCES trx_individual_learning_plan(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_milestone_ilp ON trx_ilp_milestone(ilp_id);
CREATE INDEX idx_milestone_target_date ON trx_ilp_milestone(target_date);
CREATE INDEX idx_milestone_achieved ON trx_ilp_milestone(achieved);

-- Create ILP template table
CREATE TABLE IF NOT EXISTS master_ilp_template (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_code VARCHAR(20) UNIQUE NOT NULL,
    template_name VARCHAR(100) NOT NULL,
    phase_id UUID,
    description TEXT NOT NULL,
    default_goals TEXT,  -- JSON array
    default_strategies TEXT,  -- JSON array
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT fk_ilp_template_phase FOREIGN KEY (phase_id) REFERENCES master_phase(id)
);

-- Create indexes
CREATE INDEX idx_ilp_template_code ON master_ilp_template(template_code);
CREATE INDEX idx_ilp_template_phase ON master_ilp_template(phase_id);
CREATE INDEX idx_ilp_template_active ON master_ilp_template(is_active);
CREATE INDEX idx_ilp_template_deleted ON master_ilp_template(deleted_at);

-- Seed ILP templates for SD
INSERT INTO master_ilp_template (template_code, template_name, phase_id, description, default_goals, default_strategies, is_active) VALUES
('ILP_FASE_A', 'ILP Fase A (Kelas 1-2)', NULL, 'Template ILP untuk Fase A dengan fokus pada literasi, numerasi, dan sosialisasi', '["Penguasaan literasi dasar", "Penguasaan numerasi dasar", "Sosialisasi dan kerjasama"]', '["Pembelajaran berbasis bermain", "Penggunaan media visual", "Pendampingan individual"]', true),
('ILP_FASE_B', 'ILP Fase B (Kelas 3-4)', NULL, 'Template ILP untuk Fase B dengan fokus pada pengembangan konsep dan keterampilan', '["Penguasaan membaca lancar", "Penguasaan berhitung kompleks", "Pengembangan kreativitas"]', '["Pembelajaran kontekstual", "Proyek berbasis masalah", "Kerja kolaboratif"]', true),
('ILP_FASE_C', 'ILP Fase C (Kelas 5-6)', NULL, 'Template ILP untuk Fase C dengan fokus pada penguasaan mendalam dan kemandirian', '["Pemahaman konsep abstrak", "Pemecahan masalah kompleks", "Kemandirian belajar"]', '["Inquiry-based learning", "Penelitian sederhana", "Refleksi metakognitif"]', true)
ON CONFLICT (template_code) DO NOTHING;

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_ilp_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_ilp_updated_at
    BEFORE UPDATE ON trx_individual_learning_plan
    FOR EACH ROW
    EXECUTE FUNCTION update_ilp_updated_at();

CREATE TRIGGER trigger_update_milestone_updated_at
    BEFORE UPDATE ON trx_ilp_milestone
    FOR EACH ROW
    EXECUTE FUNCTION update_ilp_updated_at();

CREATE TRIGGER trigger_update_ilp_template_updated_at
    BEFORE UPDATE ON master_ilp_template
    FOR EACH ROW
    EXECUTE FUNCTION update_ilp_updated_at();
