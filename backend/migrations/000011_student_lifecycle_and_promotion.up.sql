-- 1. STANDARDISASI STATUS SISWA (MAPPING DATA LAMA)
UPDATE master_student SET student_status = 'active' WHERE student_status = 'Aktif' OR student_status IS NULL;
UPDATE master_student SET student_status = 'graduated' WHERE student_status = 'Lulus';
UPDATE master_student SET student_status = 'withdrawn' WHERE student_status IN ('Mutasi', 'Keluar');

-- Set default baru pada skema kolom status siswa
ALTER TABLE master_student ALTER COLUMN student_status SET DEFAULT 'active';

-- 2. TABEL LOG SEJARAH PROMOSI KELAS SISWA (AUDIT TRAIL)
CREATE TABLE IF NOT EXISTS trx_academic_promotion_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES master_student(id) ON DELETE CASCADE,
  source_classroom_id UUID NOT NULL,
  target_classroom_id UUID NOT NULL,
  promoted_by UUID NOT NULL,
  promoted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_promotion_student ON trx_academic_promotion_log(student_id);
