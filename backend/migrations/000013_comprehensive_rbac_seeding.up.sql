-- 1. SEED ALL 31 FEATURE PERMISSIONS
INSERT INTO auth_permission (permission_name, description) VALUES
  ('system:view', 'Melihat status sistem dan log analitik'),
  ('system:update', 'Mengonfigurasi pengaturan sistem sekolah'),
  ('system:access', 'Mengelola hak akses, peran, dan perizinan pengguna'),
  ('school:view', 'Melihat profil sekolah, tingkat kelas, dan siklus tahun ajaran'),
  ('school:update', 'Mengedit profil sekolah dan parameter tahun ajaran'),
  ('staff:view', 'Melihat daftar dan profil guru/staf'),
  ('staff:create', 'Menambah data guru/staf baru'),
  ('staff:update', 'Mengedit data profil guru/staf'),
  ('staff:delete', 'Menonaktifkan data guru/staf'),
  ('student:view', 'Melihat profil lengkap siswa (Student Profile 360)'),
  ('student:create', 'Menerima dan mendaftarkan siswa baru'),
  ('student:update', 'Mengedit data biodata, keluarga, dan status siswa'),
  ('student:delete', 'Menghapus atau mengeluarkan data siswa'),
  ('ppdb:view', 'Melihat daftar calon siswa baru yang mendaftar online'),
  ('ppdb:update', 'Memverifikasi dokumen berkas dan status kelolosan PPDB'),
  ('curriculum:view', 'Melihat standar belajar, tujuan pembelajaran, dan alur tujuan'),
  ('curriculum:update', 'Menyusun dan merancang dokumen KSP (Kurikulum Satuan Pendidikan)'),
  ('classroom:view', 'Melihat data kelas dan jadwal pelajaran'),
  ('classroom:create', 'Membuat rombongan belajar / kelas baru'),
  ('classroom:update', 'Mengatur wali kelas, mata pelajaran, dan jadwal di kelas'),
  ('classroom:delete', 'Menghapus rombongan belajar / kelas'),
  ('presence:view', 'Melihat catatan kehadiran/presensi harian siswa'),
  ('presence:update', 'Mencatat presensi harian siswa'),
  ('modules:view', 'Melihat modul ajar dan pustaka bahan pembelajaran'),
  ('modules:update', 'Mengunggah, mengedit, dan mengarsipkan modul ajar'),
  ('assessment:view', 'Melihat hasil asesmen, bank soal, dan rekapan nilai'),
  ('assessment:update', 'Menginput nilai formatif, sumatif, dan rubrik asesmen'),
  ('counseling:view', 'Melihat peringatan dini EWS dan jurnal anekdot konseling'),
  ('counseling:create', 'Mencatat jurnal observasi anekdot murid secara cepat'),
  ('counseling:update', 'Memicu analisis risiko EWS harian dan memperbarui status intervensi'),
  ('report:view', 'Melihat pratinjau rapor murid'),
  ('report:finalize', 'Menandatangani, memfinalisasi, dan mencetak rapor digital')
ON CONFLICT (permission_name) DO UPDATE SET description = EXCLUDED.description;

-- 2. SEED ROLE-PERMISSION MAPPINGS DEKLARATIF
-- a) ADMIN mendapatkan akses penuh (seluruh 32 izin)
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name = 'ADMIN'
ON CONFLICT DO NOTHING;

-- b) KEPALA_SEKOLAH mendapatkan izin kepemimpinan dan validasi
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name = 'KEPALA_SEKOLAH'
  AND p.permission_name IN (
    'system:view', 'school:view', 'school:update', 'staff:view', 'student:view',
    'curriculum:view', 'classroom:view', 'presence:view', 'modules:view',
    'assessment:view', 'counseling:view', 'report:view', 'report:finalize'
  )
ON CONFLICT DO NOTHING;

-- c) OPERATOR mendapatkan izin administratif penuh
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name = 'OPERATOR'
  AND p.permission_name IN (
    'school:view', 'school:update', 'staff:view', 'staff:create', 'staff:update', 'staff:delete',
    'student:view', 'student:create', 'student:update', 'student:delete', 'ppdb:view', 'ppdb:update',
    'classroom:view', 'classroom:create', 'classroom:update', 'classroom:delete'
  )
ON CONFLICT DO NOTHING;

-- d) GURU dan HOMEROOM_TEACHER mendapatkan izin pembelajaran sehari-hari
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name IN ('GURU', 'HOMEROOM_TEACHER')
  AND p.permission_name IN (
    'school:view', 'staff:view', 'student:view', 'curriculum:view', 'classroom:view',
    'presence:view', 'presence:update', 'modules:view', 'modules:update',
    'assessment:view', 'assessment:update', 'counseling:view', 'counseling:create', 'counseling:update',
    'report:view'
  )
ON CONFLICT DO NOTHING;

-- e) HOMEROOM_TEACHER mendapatkan otorisasi finalisasi rapor tambahan
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name = 'HOMEROOM_TEACHER'
  AND p.permission_name = 'report:finalize'
ON CONFLICT DO NOTHING;

-- f) CLERK mendapatkan izin klerikal PPDB & kesiswaan
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name = 'CLERK'
  AND p.permission_name IN (
    'school:view', 'student:view', 'student:create', 'student:update',
    'ppdb:view', 'ppdb:update', 'classroom:view'
  )
ON CONFLICT DO NOTHING;

-- g) STUDENT dan PARENT mendapatkan izin portal akses mandiri
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name IN ('STUDENT', 'PARENT')
  AND p.permission_name IN (
    'school:view', 'curriculum:view', 'classroom:view', 'presence:view',
    'assessment:view', 'report:view'
  )
ON CONFLICT DO NOTHING;
