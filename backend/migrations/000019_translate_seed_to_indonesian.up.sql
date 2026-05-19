-- De-duplicate duplicate English rows from dl_cognitive_stage
DELETE FROM dl_cognitive_stage WHERE stage_name IN ('Understand', 'Apply', 'Reflect');

-- De-duplicate duplicate English rows from dl_design_element
DELETE FROM dl_design_element WHERE design_element_name IN ('Pedagogical Practices', 'Learning Environment', 'Digital Utilization', 'Learning Partnerships');

-- Translate dl_assessment_level
UPDATE dl_assessment_level SET description = 'Kemampuan Berpikir Tingkat Rendah (LOTS)' WHERE level_code = 'LOTS';
UPDATE dl_assessment_level SET description = 'Kemampuan Berpikir Tingkat Tinggi (HOTS)' WHERE level_code = 'HOTS';

-- Translate dl_cognitive_stage
UPDATE dl_cognitive_stage SET stage_name = 'Mengaktifkan', operational_verbs = 'Mengingat, Memahami, Menghubungkan' WHERE stage_order = 1;
UPDATE dl_cognitive_stage SET stage_name = 'Menyelidiki', operational_verbs = 'Menganalisis, Membandingkan, Mengevaluasi' WHERE stage_order = 2;
UPDATE dl_cognitive_stage SET stage_name = 'Merefleksi', operational_verbs = 'Merancang, Membangun, Menghasilkan, Merefleksikan' WHERE stage_order = 3;

-- Translate dl_design_element
UPDATE dl_design_element SET design_element_name = 'Praktik Pedagogis' WHERE design_element_name = 'Praktik Pedagogis' OR design_element_name = 'Pedagogical Practices';
UPDATE dl_design_element SET design_element_name = 'Lingkungan Pembelajaran' WHERE design_element_name = 'Lingkungan Pembelajaran' OR design_element_name = 'Learning Environment';
UPDATE dl_design_element SET design_element_name = 'Pemanfaatan Digital' WHERE design_element_name = 'Pemanfaatan Digital' OR design_element_name = 'Digital Utilization';
UPDATE dl_design_element SET design_element_name = 'Kemitraan Pembelajaran' WHERE design_element_name = 'Kemitraan Pembelajaran' OR design_element_name = 'Learning Partnerships';
