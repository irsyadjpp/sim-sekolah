DROP TABLE IF EXISTS trx_academic_promotion_log CASCADE;
ALTER TABLE master_student ALTER COLUMN student_status SET DEFAULT 'Aktif';
