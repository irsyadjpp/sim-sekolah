DELETE FROM master_local_context_category WHERE category_code IN ('BAHARI','BUDAYA','ALAM','SOSIAL');
DELETE FROM master_academic_year WHERE year_name IN ('2024/2025','2025/2026');
DELETE FROM dl_assessment_level WHERE level_code IN ('LOTS','HOTS');
DELETE FROM dl_cognitive_stage WHERE stage_name IN ('Mengaktifkan','Menyelidiki','Menciptakan');
DELETE FROM dl_design_element WHERE design_element_name IN ('Praktik Pedagogis','Lingkungan Pembelajaran','Pemanfaatan Digital','Kemitraan Pembelajaran');
DELETE FROM master_profile_dimension WHERE dimension_code IN ('BERIMAN','BERKEBINEKAAN','BERGOTONG_ROYONG','MANDIRI','BERNALAR_KRITIS','KREATIF','P5_TEMA_1','P5_TEMA_2');
DELETE FROM master_grade;
DELETE FROM master_phase WHERE phase_code IN ('FAS-A','FAS-B','FAS-C','FAS-D','FAS-E','FAS-F');
