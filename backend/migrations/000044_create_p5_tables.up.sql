-- Migration: Create P5 (Proyek Penguatan Profil Pelajar Pancasila) Tables
-- This migration creates the database schema for the P5 Project-Based Learning module
-- which includes project management, team formation, milestone tracking, and student participation

-- Ensure UUID extension is available (may already be enabled in main schema)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create p5_projects table
CREATE TABLE IF NOT EXISTS p5_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id UUID,
    classroom_id UUID,
    project_theme VARCHAR(100) NOT NULL,
    academic_year_id UUID,
    semester INTEGER DEFAULT 1,
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    total_weeks INTEGER DEFAULT 4,
    project_type VARCHAR(50) NOT NULL,
    max_team_size INTEGER DEFAULT 5,
    required_dimensions TEXT,
    status VARCHAR(20) DEFAULT 'PERENCANAAN',
    progress INTEGER DEFAULT 0,
    teaching_module_id UUID,
    rubric_id UUID,

    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for p5_projects
CREATE INDEX IF NOT EXISTS idx_p5_projects_subject ON p5_projects(subject_id);
CREATE INDEX IF NOT EXISTS idx_p5_projects_classroom ON p5_projects(classroom_id);
CREATE INDEX IF NOT EXISTS idx_p5_projects_theme ON p5_projects(project_theme);
CREATE INDEX IF NOT EXISTS idx_p5_projects_academic_year ON p5_projects(academic_year_id);
CREATE INDEX IF NOT EXISTS idx_p5_projects_status ON p5_projects(status);
CREATE INDEX IF NOT EXISTS idx_p5_projects_deleted_at ON p5_projects(deleted_at);

-- Add check constraints for p5_projects
ALTER TABLE p5_projects 
ADD CONSTRAINT IF NOT EXISTS chk_p5_project_type 
CHECK (project_type IN ('INDIVIDU', 'KELOMPOK', 'KELAS'));

ALTER TABLE p5_projects 
ADD CONSTRAINT IF NOT EXISTS chk_p5_project_status 
CHECK (status IN ('PERENCANAAN', 'BERJALAN', 'DIHENTIKAN', 'SELESAI', 'DIBATALKAN'));

ALTER TABLE p5_projects 
ADD CONSTRAINT IF NOT EXISTS chk_p5_project_progress 
CHECK (progress >= 0 AND progress <= 100);

-- Create p5_project_teams table
CREATE TABLE IF NOT EXISTS p5_project_teams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    team_code VARCHAR(20) UNIQUE NOT NULL,
    max_members INTEGER DEFAULT 5,
    current_size INTEGER DEFAULT 0,
    team_leader_id UUID,
    is_active BOOLEAN DEFAULT TRUE,

    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for p5_project_teams
CREATE INDEX IF NOT EXISTS idx_p5_teams_project ON p5_project_teams(project_id);
CREATE INDEX IF NOT EXISTS idx_p5_teams_leader ON p5_project_teams(team_leader_id);
CREATE INDEX IF NOT EXISTS idx_p5_teams_deleted_at ON p5_project_teams(deleted_at);

-- Create p5_team_members table
CREATE TABLE IF NOT EXISTS p5_team_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    team_id UUID NOT NULL,
    student_id UUID NOT NULL,
    role VARCHAR(50) DEFAULT 'ANGGOTA',
    joined_at VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,

    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for p5_team_members
CREATE INDEX IF NOT EXISTS idx_p5_team_members_team ON p5_team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_p5_team_members_student ON p5_team_members(student_id);
CREATE INDEX IF NOT EXISTS idx_p5_team_members_deleted_at ON p5_team_members(deleted_at);

-- Add check constraint for team member role
ALTER TABLE p5_team_members 
ADD CONSTRAINT IF NOT EXISTS chk_p5_team_member_role 
CHECK (role IN ('KETUA', 'ANGGOTA', 'PENGAMAT'));

-- Create p5_project_milestones table
CREATE TABLE IF NOT EXISTS p5_project_milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    sequence INTEGER DEFAULT 1,
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    required_hours DECIMAL(5,2) DEFAULT 2.0,
    deliverables TEXT,
    assessment_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'BELUM_MULAI',
    completion_date VARCHAR(50),

    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for p5_project_milestones
CREATE INDEX IF NOT EXISTS idx_p5_milestones_project ON p5_project_milestones(project_id);
CREATE INDEX IF NOT EXISTS idx_p5_milestones_sequence ON p5_project_milestones(sequence);
CREATE INDEX IF NOT EXISTS idx_p5_milestones_status ON p5_project_milestones(status);
CREATE INDEX IF NOT EXISTS idx_p5_milestones_deleted_at ON p5_project_milestones(deleted_at);

-- Add check constraints for milestones
ALTER TABLE p5_project_milestones 
ADD CONSTRAINT IF NOT EXISTS chk_p5_milestone_assessment_type 
CHECK (assessment_type IN ('FORMATIF', 'SUMATIF'));

ALTER TABLE p5_project_milestones 
ADD CONSTRAINT IF NOT EXISTS chk_p5_milestone_status 
CHECK (status IN ('BELUM_MULAI', 'SEDANG_BERJALAN', 'SELESAI', 'TERTUNDA'));

-- Create p5_student_participation table
CREATE TABLE IF NOT EXISTS p5_student_participation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL,
    student_id UUID NOT NULL,
    team_id UUID,
    role VARCHAR(50) DEFAULT 'ANGGOTA',

    -- Progress tracking
    overall_progress DECIMAL(5,2) DEFAULT 0.0,
    engagement_level VARCHAR(20) DEFAULT 'SEDANG',
    attendance_rate DECIMAL(5,2) DEFAULT 0.0,

    -- Dimension growth and feedback
    dimension_growth TEXT,
    challenges_faced TEXT,
    support_needed TEXT,

    -- Final assessment
    final_score DECIMAL(5,2),
    grade VARCHAR(20),
    teacher_feedback TEXT,

    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for p5_student_participation
CREATE INDEX IF NOT EXISTS idx_p5_participation_project ON p5_student_participation(project_id);
CREATE INDEX IF NOT EXISTS idx_p5_participation_student ON p5_student_participation(student_id);
CREATE INDEX IF NOT EXISTS idx_p5_participation_team ON p5_student_participation(team_id);
CREATE INDEX IF NOT EXISTS idx_p5_participation_deleted_at ON p5_student_participation(deleted_at);

-- Add check constraints for student participation
ALTER TABLE p5_student_participation 
ADD CONSTRAINT IF NOT EXISTS chk_p5_participation_role 
CHECK (role IN ('KETUA', 'ANGGOTA'));

ALTER TABLE p5_student_participation 
ADD CONSTRAINT IF NOT EXISTS chk_p5_participation_progress 
CHECK (overall_progress >= 0 AND overall_progress <= 100);

ALTER TABLE p5_student_participation 
ADD CONSTRAINT IF NOT EXISTS chk_p5_participation_engagement 
CHECK (engagement_level IN ('TINGGI', 'SEDANG', 'RENDAH'));

ALTER TABLE p5_student_participation 
ADD CONSTRAINT IF NOT EXISTS chk_p5_participation_attendance 
CHECK (attendance_rate >= 0 AND attendance_rate <= 100);

ALTER TABLE p5_student_participation 
ADD CONSTRAINT IF NOT EXISTS chk_p5_participation_score 
CHECK (final_score IS NULL OR (final_score >= 0 AND final_score <= 100));

-- Add comments for documentation
COMMENT ON TABLE p5_projects IS 'P5 (Proyek Penguatan Profil Pelajar Pancasila) projects';
COMMENT ON TABLE p5_project_teams IS 'Teams for P5 projects';
COMMENT ON TABLE p5_team_members IS 'Members of P5 project teams';
COMMENT ON TABLE p5_project_milestones IS 'Milestones/phases for P5 projects';
COMMENT ON TABLE p5_student_participation IS 'Individual student participation in P5 projects';

-- Add column comments for p5_projects
COMMENT ON COLUMN p5_projects.project_theme IS 'Theme of the P5 project (e.g., Kewirausahaan, Bhinneka Tunggal Ika)';
COMMENT ON COLUMN p5_projects.project_type IS 'Type of project: INDIVIDUAL, GROUP, or CLASS';
COMMENT ON COLUMN p5_projects.required_dimensions IS 'Profile dimensions required for this project (JSON array)';
COMMENT ON COLUMN p5_projects.status IS 'Project status: PLANNING, ONGOING, PAUSED, COMPLETED, or CANCELLED';

-- Add column comments for p5_project_milestones
COMMENT ON COLUMN p5_project_milestones.sequence IS 'Order of the milestone within the project';
COMMENT ON COLUMN p5_project_milestones.required_hours IS 'Estimated hours needed to complete this milestone';
COMMENT ON COLUMN p5_project_milestones.deliverables IS 'Expected deliverables for this milestone (JSON array)';
COMMENT ON COLUMN p5_project_milestones.assessment_type IS 'Type of assessment: FORMATIVE or SUMMATIVE';

-- Add column comments for p5_student_participation
COMMENT ON COLUMN p5_student_participation.dimension_growth IS 'JSON object tracking growth in profile dimensions';
COMMENT ON COLUMN p5_student_participation.engagement_level IS 'Student engagement level: HIGH, MEDIUM, or LOW';
COMMENT ON COLUMN p5_student_participation.attendance_rate IS 'Attendance rate as percentage';

-- Create trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all P5 tables (use IF NOT EXISTS via DROP TRIGGER)
DROP TRIGGER IF EXISTS update_p5_projects_updated_at ON p5_projects;
CREATE TRIGGER update_p5_projects_updated_at BEFORE UPDATE ON p5_projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_p5_project_teams_updated_at ON p5_project_teams;
CREATE TRIGGER update_p5_project_teams_updated_at BEFORE UPDATE ON p5_project_teams
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_p5_team_members_updated_at ON p5_team_members;
CREATE TRIGGER update_p5_team_members_updated_at BEFORE UPDATE ON p5_team_members
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_p5_project_milestones_updated_at ON p5_project_milestones;
CREATE TRIGGER update_p5_project_milestones_updated_at BEFORE UPDATE ON p5_project_milestones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_p5_student_participation_updated_at ON p5_student_participation;
CREATE TRIGGER update_p5_student_participation_updated_at BEFORE UPDATE ON p5_student_participation
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
