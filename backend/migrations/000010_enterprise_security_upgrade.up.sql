-- 1. PILAR 1: DYNAMIC PERMISSIONS TABLES
CREATE TABLE IF NOT EXISTS auth_permission (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  permission_name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auth_role_permission (
  role_id UUID NOT NULL REFERENCES auth_role(id) ON DELETE CASCADE,
  permission_id UUID NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
  PRIMARY KEY (role_id, permission_id)
);

-- 2. PILAR 2: MFA TOTP SECRET STORAGE ON USER TABLE
ALTER TABLE auth_user ADD COLUMN IF NOT EXISTS totp_secret VARCHAR(100);

-- 3. PILAR 3: STATEFUL USER SESSIONS & DEVICE REGISTRY TABLE
CREATE TABLE IF NOT EXISTS auth_user_session (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
  user_agent TEXT NOT NULL,
  ip_address VARCHAR(50) NOT NULL,
  is_revoked BOOLEAN DEFAULT false,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_session_user ON auth_user_session(user_id);
CREATE INDEX IF NOT EXISTS idx_user_session_revoked ON auth_user_session(is_revoked);

-- 4. SEED INITIAL FEATURE-PERMISSIONS & ASSIGNMENT TO ROLES
INSERT INTO auth_permission (permission_name, description) VALUES
  ('classroom:view', 'Melihat daftar rombongan belajar'),
  ('classroom:create', 'Membuat rombongan belajar baru'),
  ('classroom:update', 'Memperbarui data rombongan belajar'),
  ('classroom:delete', 'Menghapus rombongan belajar'),
  ('report:view', 'Melihat dokumen rapor'),
  ('report:finalize', 'Memfinalisasi dan menandatangani rapor AI')
ON CONFLICT DO NOTHING;

-- Hubungkan hak akses classroom:view ke seluruh Guru dan Staf
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name IN ('GURU', 'HOMEROOM_TEACHER', 'CLERK') AND p.permission_name = 'classroom:view'
ON CONFLICT DO NOTHING;

-- Hubungkan hak akses report:finalize eksklusif hanya untuk Kepala Sekolah dan Wali Kelas
INSERT INTO auth_role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM auth_role r, auth_permission p
WHERE r.role_name IN ('KEPALA_SEKOLAH', 'HOMEROOM_TEACHER') AND p.permission_name = 'report:finalize'
ON CONFLICT DO NOTHING;
