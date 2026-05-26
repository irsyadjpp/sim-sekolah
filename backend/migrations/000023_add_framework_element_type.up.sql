-- Migration: Add framework_element_type to dl_design_element table
-- Description: Add framework classification to design elements according to Deep Learning 4 framework categories
-- Created: 2024-05-24

-- Add the framework_element_type column
ALTER TABLE dl_design_element 
ADD COLUMN IF NOT EXISTS framework_element_type VARCHAR(50);

-- Add index for framework element type
CREATE INDEX IF NOT EXISTS idx_dl_design_element_framework_type ON dl_design_element(framework_element_type) WHERE deleted_at IS NULL;

-- Update comment on the table
COMMENT ON TABLE dl_design_element IS 'Table for Deep Learning design elements with framework classification';
COMMENT ON COLUMN dl_design_element.framework_element_type IS 'Framework category: PRAKTIK_PEDAGOGIS, KEMITRAAN_PEMBELAJARAN, LINGKUNGAN_PEMBELAJARAN, PEMANFAATAN_DIGITAL';

-- Clear existing elements (will be recreated with correct classification)
DELETE FROM dl_design_element;

-- Insert standard framework elements according to Deep Learning 4 framework categories
INSERT INTO dl_design_element (design_element_name, description, framework_element_type, is_active, created_at, updated_at) VALUES
-- Praktik Pedagogis (Pedagogical Practices)
('Differentiated Instruction', 'Pendekatan pembelajaran yang disesuaikan dengan kebutuhan, kemampuan, dan minat peserta didik', 'PRAKTIK_PEDAGOGIS', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Formative Assessment', 'Penilaian yang dilakukan secara berkelanjutan selama proses pembelajaran untuk memberikan umpan balik', 'PRAKTIK_PEDAGOGIS', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Scaffolding', 'Dukungan sementara yang diberikan kepada peserta didik untuk membantu mereka mencapai tujuan pembelajaran', 'PRAKTIK_PEDAGOGIS', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Inquiry-Based Learning', 'Pembelajaran berbasis penyelidikan di mana peserta didik mengajukan pertanyaan dan mengeksplorasi topik', 'PRAKTIK_PEDAGOGIS', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- Kemitraan Pembelajaran (Learning Partnerships)
('Kemitraan Guru-Siswa', 'Kolaborasi aktif antara guru dan siswa dalam proses pembelajaran', 'KEMITRAAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Kemitraan Siswa-Siswa', 'Kerja sama dan kolaborasi antar siswa untuk mencapai tujuan bersama', 'KEMITRAAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Kemitraan Sekolah-Komunitas', 'Keterlibatan komunitas dan orang tua dalam pembelajaran', 'KEMITRAAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Kemitraan Sekolah-Expert', 'Kerja sama dengan pakar atau expert luar untuk mendukung pembelajaran', 'KEMITRAAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- Lingkungan Pembelajaran (Learning Environment)
('Lingkungan Kelas yang Kondusif', 'Pengaturan ruang kelas yang mendukung pembelajaran', 'LINGKUNGAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Lingkungan Sosial yang Positif', 'Budaya kelas yang saling menghargai dan mendukung', 'LINGKUNGAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Lingkungan Fisik yang Aman', 'Ruang fisik yang aman, nyaman, dan mendukung pembelajaran', 'LINGKUNGAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Lingkungan Digital yang Terintegrasi', 'Integrasi teknologi dalam lingkungan pembelajaran secara seamless', 'LINGKUNGAN_PEMBELAJARAN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- Pemanfaatan Digital (Digital Utilization)
('Pemanfaatan Media Digital', 'Penggunaan teknologi digital dalam pembelajaran', 'PEMANFAATAN_DIGITAL', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Pemanfaatan Platform Pembelajaran', 'Penggunaan LMS dan platform edukasi', 'PEMANFAATAN_DIGITAL', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Digital Collaboration Tools', 'Alat kolaborasi digital untuk kerja sama siswa', 'PEMANFAATAN_DIGITAL', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Digital Assessment Tools', 'Alat asesmen digital untuk evaluasi pembelajaran', 'PEMANFAATAN_DIGITAL', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
