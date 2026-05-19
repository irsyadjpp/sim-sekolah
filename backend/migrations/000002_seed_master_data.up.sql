-- 1. Seed master_phase
INSERT INTO master_phase (id, phase_code, phase_name, description) VALUES
  (uuid_generate_v4(), 'FAS-A', 'Fase A', 'Kelas 1–2: Fondasi literasi & numerasi dasar'),
  (uuid_generate_v4(), 'FAS-B', 'Fase B', 'Kelas 3–4: Pengembangan kemampuan berpikir'),
  (uuid_generate_v4(), 'FAS-C', 'Fase C', 'Kelas 5–6: Penguatan kompetensi & kemandirian'),
  (uuid_generate_v4(), 'FAS-D', 'Fase D', 'Kelas 7–9: SMP'),
  (uuid_generate_v4(), 'FAS-E', 'Fase E', 'Kelas 10: SMA'),
  (uuid_generate_v4(), 'FAS-F', 'Fase F', 'Kelas 11–12: SMA')
ON CONFLICT (phase_code) DO NOTHING;

-- 2. Seed master_grade (bergantung pada FK phase_id)
INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT uuid_generate_v4(), p.id, 1, 'Kelas 1' FROM master_phase p WHERE p.phase_code = 'FAS-A'
AND NOT EXISTS (SELECT 1 FROM master_grade WHERE grade_level = 1);

INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT uuid_generate_v4(), p.id, 2, 'Kelas 2' FROM master_phase p WHERE p.phase_code = 'FAS-A'
AND NOT EXISTS (SELECT 1 FROM master_grade WHERE grade_level = 2);

INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT uuid_generate_v4(), p.id, 3, 'Kelas 3' FROM master_phase p WHERE p.phase_code = 'FAS-B'
AND NOT EXISTS (SELECT 1 FROM master_grade WHERE grade_level = 3);

INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT uuid_generate_v4(), p.id, 4, 'Kelas 4' FROM master_phase p WHERE p.phase_code = 'FAS-B'
AND NOT EXISTS (SELECT 1 FROM master_grade WHERE grade_level = 4);

INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT uuid_generate_v4(), p.id, 5, 'Kelas 5' FROM master_phase p WHERE p.phase_code = 'FAS-C'
AND NOT EXISTS (SELECT 1 FROM master_grade WHERE grade_level = 5);

INSERT INTO master_grade (id, phase_id, grade_level, grade_name)
SELECT uuid_generate_v4(), p.id, 6, 'Kelas 6' FROM master_phase p WHERE p.phase_code = 'FAS-C'
AND NOT EXISTS (SELECT 1 FROM master_grade WHERE grade_level = 6);

-- 3. Seed master_profile_dimension
INSERT INTO master_profile_dimension (id, dimension_code, dimension_name, description) VALUES
  (uuid_generate_v4(), 'BERIMAN', 'Beriman, Bertakwa kepada Tuhan YME, dan Berakhlak Mulia', ''),
  (uuid_generate_v4(), 'BERKEBINEKAAN', 'Berkebinekaan Global', ''),
  (uuid_generate_v4(), 'BERGOTONG_ROYONG', 'Bergotong Royong', ''),
  (uuid_generate_v4(), 'MANDIRI', 'Mandiri', ''),
  (uuid_generate_v4(), 'BERNALAR_KRITIS', 'Bernalar Kritis', ''),
  (uuid_generate_v4(), 'KREATIF', 'Kreatif', ''),
  (uuid_generate_v4(), 'P5_TEMA_1', 'Tema P5: Gaya Hidup Berkelanjutan', ''),
  (uuid_generate_v4(), 'P5_TEMA_2', 'Tema P5: Kearifan Lokal', '')
ON CONFLICT (dimension_code) DO NOTHING;

-- 4. Seed dl_design_element
INSERT INTO dl_design_element (id, design_element_name) VALUES
  (uuid_generate_v4(), 'Praktik Pedagogis'),
  (uuid_generate_v4(), 'Lingkungan Pembelajaran'),
  (uuid_generate_v4(), 'Pemanfaatan Digital'),
  (uuid_generate_v4(), 'Kemitraan Pembelajaran')
ON CONFLICT (design_element_name) DO NOTHING;

-- 5. Seed dl_cognitive_stage
INSERT INTO dl_cognitive_stage (id, stage_order, stage_name, operational_verbs) VALUES
  (uuid_generate_v4(), 1, 'Mengaktifkan', 'Mengingat, Memahami, Menghubungkan'),
  (uuid_generate_v4(), 2, 'Menyelidiki', 'Menganalisis, Membandingkan, Mengevaluasi'),
  (uuid_generate_v4(), 3, 'Menciptakan', 'Merancang, Membangun, Menghasilkan')
ON CONFLICT (stage_name) DO NOTHING;

-- 6. Seed dl_assessment_level
INSERT INTO dl_assessment_level (id, level_code, description, pisa_level) VALUES
  (uuid_generate_v4(), 'LOTS', 'Lower Order Thinking Skills', 'Level 1-3'),
  (uuid_generate_v4(), 'HOTS', 'Higher Order Thinking Skills', 'Level 4-6')
ON CONFLICT (level_code) DO NOTHING;

-- 7. Seed master_local_context_category
INSERT INTO master_local_context_category (id, category_code, category_name, description) VALUES
  (uuid_generate_v4(), 'BAHARI', 'Kemaritiman & Pesisir Pantai', 'Konteks pembelajaran berbasis ekosistem laut dan pesisir Bonerate'),
  (uuid_generate_v4(), 'BUDAYA', 'Tradisi & Kebudayaan', 'Kearifan budaya Kepulauan Selayar'),
  (uuid_generate_v4(), 'ALAM', 'Flora & Fauna Kepulauan', 'Biodiversitas kawasan Taman Nasional Laut Takabonerate'),
  (uuid_generate_v4(), 'SOSIAL', 'Komunitas & Kemitraan', 'Relasi sosial komunitas pesisir dan kemitraan wali murid')
ON CONFLICT (category_code) DO NOTHING;

-- 8. Seed master_academic_year
INSERT INTO master_academic_year (id, year_name, semester, is_active)
SELECT uuid_generate_v4(), '2024/2025', 'Genap', false
WHERE NOT EXISTS (SELECT 1 FROM master_academic_year WHERE year_name = '2024/2025' AND semester = 'Genap');

INSERT INTO master_academic_year (id, year_name, semester, is_active)
SELECT uuid_generate_v4(), '2025/2026', 'Ganjil', true
WHERE NOT EXISTS (SELECT 1 FROM master_academic_year WHERE year_name = '2025/2026' AND semester = 'Ganjil');
