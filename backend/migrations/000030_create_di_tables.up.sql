-- Migration: Phase 3 - Differentiated Instruction Tables
-- Description: Creates tables for Differentiated Instruction tracking

-- Create DI strategy master table
CREATE TABLE IF NOT EXISTS master_di_strategy (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strategy_code VARCHAR(20) UNIQUE NOT NULL,
    strategy_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    applicability TEXT,  -- JSON array of when to use
    examples TEXT,  -- JSON array of examples
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes
CREATE INDEX idx_di_strategy_code ON master_di_strategy(strategy_code);
CREATE INDEX idx_di_strategy_active ON master_di_strategy(is_active);
CREATE INDEX idx_di_strategy_deleted ON master_di_strategy(deleted_at);

-- Create module differentiation table
CREATE TABLE IF NOT EXISTS trx_module_differentiation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    module_id UUID NOT NULL,
    strategy_id UUID NOT NULL,
    target_students TEXT,  -- JSON array of student IDs
    modifications TEXT,
    resources TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID,
    CONSTRAINT fk_di_module FOREIGN KEY (module_id) REFERENCES trx_teaching_module(id) ON DELETE CASCADE,
    CONSTRAINT fk_di_strategy FOREIGN KEY (strategy_id) REFERENCES master_di_strategy(id)
);

-- Create indexes
CREATE INDEX idx_di_module ON trx_module_differentiation(module_id);
CREATE INDEX idx_di_strategy ON trx_module_differentiation(strategy_id);

-- Seed DI strategies for SD
INSERT INTO master_di_strategy (strategy_code, strategy_name, description, applicability, examples, is_active) VALUES
('VISUAL_SUPPORT', 'Visual Support', 'Menggunakan visual aids untuk membantu pemahaman', '["Siswa dengan gaya belajar visual", "Siswa dengan kesulitan bahasa", "Konsep abstrak"]', '["Gambar dan diagram", "Video pembelajaran", "Papan tulis warna-warni"]', true),
('AUDITORY_SUPPORT', 'Auditory Support', 'Menggunakan pendekatan audio untuk pembelajaran', '["Siswa dengan gaya belajar auditory", "Siswa dengan kesulitan membaca"]', '["Penjelasan lisan", "Audio materi", "Diskusi kelompok"]', true),
('KINESTHETIC_SUPPORT', 'Kinesthetic Support', 'Pembelajaran melalui gerak dan aktivitas fisik', '["Siswa dengan gaya belajar kinestetik", "Siswa yang sulit duduk diam"]', '["Hands-on activities", "Gerakan dan tarian", "Proyek praktis"]', true),
('EXTENDED_TIME', 'Extended Time', 'Memberikan waktu tambahan untuk tugas dan ujian', '["Siswa dengan kebutuhan khusus", "Siswa yang bekerja lebih lambat"]', '["Waktu ujian diperpanjang", "Tugas dengan deadline fleksibel"]', true),
('SIMPLIFIED_CONTENT', 'Simplified Content', "Menyederhanakan materi untuk pemahaman lebih mudah", '["Siswa dengan kesulitan akademik", "Siswa baru dalam bahasa pengantar"]', '["Bahan baca yang lebih singkat", "Instruksi langkah demi langkah", "Vocabular yang disederhanakan"]', true),
('PEER_TUTORING', 'Peer Tutoring', 'Belajar berpasangan dengan teman sebaya', '["Siswa yang membutuhkan bantuan tambahan", "Siswa yang bisa mengajar teman"]', '["Belajar berpasangan", "Kerja kelompok kecil", "Mentor sebaya"]', true),
('ASSISTIVE_TECHNOLOGY', 'Assistive Technology', 'Menggunakan teknologi bantuan untuk pembelajaran', '["Siswa dengan gangguan motorik", "Siswa dengan dyslexia"]', '["Text-to-speech", "Speech-to-text", "Kalkulator digital"]', true)
ON CONFLICT (strategy_code) DO NOTHING;

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_di_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_di_strategy_updated_at
    BEFORE UPDATE ON master_di_strategy
    FOR EACH ROW
    EXECUTE FUNCTION update_di_updated_at();
