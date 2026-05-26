-- Rollback for Phase 4: Advanced Features & Interoperability
-- This removes all Phase 4 tables and components

-- ============================================
-- DROP NOTIFICATION SYSTEM TABLES
-- ============================================

DROP TABLE IF EXISTS notification_statistics;
DROP TABLE IF EXISTS notification_preferences;
DROP TABLE IF EXISTS notification_delivery;
DROP TABLE IF EXISTS notification_rules;
DROP TABLE IF EXISTS notification_templates;

-- ============================================
-- DROP DAPODIK INTEGRATION TABLES
-- ============================================

DROP TABLE IF EXISTS national_assessment_standards;
DROP TABLE IF EXISTS dapodik_mapping;
DROP TABLE IF EXISTS dapodik_sync_history;
DROP TABLE IF EXISTS dapodik_sync_config;

-- ============================================
-- DROP QUESTION BANK SYSTEM TABLES
-- ============================================

DROP TABLE IF EXISTS question_exports;
DROP TABLE IF EXISTS question_imports;
DROP TABLE IF EXISTS question_reviews;
DROP TABLE IF EXISTS question_categories;
DROP TABLE IF EXISTS question_tag_associations;
DROP TABLE IF EXISTS question_tags;
DROP TABLE IF EXISTS question_usage_analytics;
DROP TABLE IF EXISTS question_difficulty_calibration;
DROP TABLE IF EXISTS question_sets;
DROP TABLE IF EXISTS question_answers;
DROP TABLE IF EXISTS question_options;
DROP TABLE IF EXISTS questions;

-- ============================================
-- DROP DOCUMENT REPOSITORY TABLES
-- ============================================

DROP TABLE IF EXISTS accreditation_documents;
DROP TABLE IF EXISTS document_shares;
DROP TABLE IF EXISTS document_access_logs;
DROP TABLE IF EXISTS document_tag_associations;
DROP TABLE IF EXISTS document_tags;
DROP TABLE IF EXISTS document_categories;
DROP TABLE IF EXISTS document_approvals;
DROP TABLE IF EXISTS document_versions;
DROP TABLE IF EXISTS documents;