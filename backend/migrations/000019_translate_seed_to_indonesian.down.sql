-- Revert dl_assessment_level
UPDATE dl_assessment_level SET description = 'Lower Order Thinking Skills' WHERE level_code = 'LOTS';
UPDATE dl_assessment_level SET description = 'Higher Order Thinking Skills' WHERE level_code = 'HOTS';

-- Revert dl_cognitive_stage
UPDATE dl_cognitive_stage SET stage_name = 'Understand', operational_verbs = NULL WHERE stage_order = 1;
UPDATE dl_cognitive_stage SET stage_name = 'Apply', operational_verbs = NULL WHERE stage_order = 2;
UPDATE dl_cognitive_stage SET stage_name = 'Reflect', operational_verbs = NULL WHERE stage_order = 3;

-- Revert dl_design_element
UPDATE dl_design_element SET design_element_name = 'Pedagogical Practices' WHERE design_element_name = 'Praktik Pedagogis';
UPDATE dl_design_element SET design_element_name = 'Learning Environment' WHERE design_element_name = 'Lingkungan Pembelajaran';
UPDATE dl_design_element SET design_element_name = 'Digital Utilization' WHERE design_element_name = 'Pemanfaatan Digital';
UPDATE dl_design_element SET design_element_name = 'Learning Partnerships' WHERE design_element_name = 'Kemitraan Pembelajaran';
