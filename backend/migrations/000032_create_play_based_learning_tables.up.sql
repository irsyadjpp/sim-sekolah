-- Migration: Phase 3 - Play-Based Learning Tables
-- Description: Creates tables for tracking play-based learning activities (Fase A specific)

-- Create play activity type master table
CREATE TABLE IF NOT EXISTS master_play_activity_type (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_code VARCHAR(20) UNIQUE NOT NULL,
    activity_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    learning_outcomes TEXT,  -- JSON array of learning outcomes
    materials_needed TEXT,  -- JSON array of required materials
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes
CREATE INDEX idx_play_activity_code ON master_play_activity_type(activity_code);
CREATE INDEX idx_play_activity_active ON master_play_activity_type(is_active);
CREATE INDEX idx_play_activity_deleted ON master_play_activity_type(deleted_at);

-- Create play-based activity table
CREATE TABLE IF NOT EXISTS trx_play_based_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    module_id UUID NOT NULL,
    activity_type_id UUID NOT NULL,
    activity_name VARCHAR(100) NOT NULL,
    duration_minutes INT NOT NULL,
    social_interaction_type VARCHAR(30) NOT NULL,  -- INDIVIDUAL, PAIR, GROUP, CLASS
    physical_activity_level VARCHAR(20) NOT NULL,  -- LOW, MEDIUM, HIGH
    learning_goals TEXT,  -- JSON array of learning goals
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID,
    CONSTRAINT fk_play_activity_module FOREIGN KEY (module_id) REFERENCES trx_teaching_module(id) ON DELETE CASCADE,
    CONSTRAINT fk_play_activity_type FOREIGN KEY (activity_type_id) REFERENCES master_play_activity_type(id)
);

-- Create indexes
CREATE INDEX idx_play_activity_module ON trx_play_based_activity(module_id);
CREATE INDEX idx_play_activity_type ON trx_play_based_activity(activity_type_id);
CREATE INDEX idx_play_interaction_type ON trx_play_based_activity(social_interaction_type);
CREATE INDEX idx_play_activity_level ON trx_play_based_activity(physical_activity_level);

-- Seed play activity types for Fase A
INSERT INTO master_play_activity_type (activity_code, activity_name, description, learning_outcomes, materials_needed, is_active) VALUES
('SENSORY_PLAY', 'Sensory Play', 'Eksplorasi sensori melalui bermain dengan berbagai tekstur', '["Pengembangan motorik halus", "Sensory awareness", "Fokus dan perhatian"]', '["Bahan tekstur berbeda", "Play dough", "Air dan pasir"]', true),
('CONSTRUCTIVE_PLAY', 'Constructive Play', 'Membangun dan mencipta sesuatu melalui bermain', '["Kreativitas", "Problem-solving", "Motorik halus"]', '["Blok bangunan", "Lego", "Balok kayu"]', true),
('DRAMATIC_PLAY', 'Dramatic Play', 'Bermain peran untuk mengembangkan imajinasi dan sosial', '["Keterampilan sosial", "Ekspresi diri", "Empati"]', ["Kostum boneka", "Panggung drama", "Properti bermain"]', true),
('GAMES_RULES', 'Games with Rules', 'Permainan dengan aturan untuk belajar disiplin dan strategi', '["Following directions", "Strategic thinking", "Self-regulation"]', '["Permainan papan", "Kartu permainan", "Puzzle"]', true),
('LANGUAGE_PLAY', 'Language Play', 'Permainan yang mengembangkan literasi dan komunikasi', '["Literasi awal", "Vocabulari", "Komunikasi"]', '["Buku cerita", "Flash cards", "Puzzle kata"]', true),
('PHYSICAL_PLAY', 'Physical Play', 'Permainan aktif untuk pengembangan motorik kasar', '["Motorik kasar", "Koordinasi", "Kesehatan fisik"]', '["Bola", "Tali skip", "Permainan outdoor"]', true),
('MUSIC_RHYTHM', 'Music and Rhythm', 'Eksplorasi suara dan ritme untuk pembelajaran', '["Musical awareness", "Ritme", "Listening skills"]', '["Alat musik sederhana", "Drum", "Rekaman suara"]', true),
('ART_CREATIVITY', 'Art and Creativity', 'Ekspresi artistik untuk kreativitas', '["Fine motor skills", "Ekspresi seni", "Kreativitas"]', '["Krayon", "Cat air", "Kolase"]', true)
ON CONFLICT (activity_code) DO NOTHING;

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_play_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_play_type_updated_at
    BEFORE UPDATE ON master_play_activity_type
    FOR EACH ROW
    EXECUTE FUNCTION update_play_updated_at();

CREATE TRIGGER trigger_update_play_activity_updated_at
    BEFORE UPDATE ON trx_play_based_activity
    FOR EACH ROW
    EXECUTE FUNCTION update_play_updated_at();
