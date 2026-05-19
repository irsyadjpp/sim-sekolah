-- Seed auth_role
INSERT INTO auth_role (id, role_name) VALUES
  (uuid_generate_v4(), 'ADMIN'),
  (uuid_generate_v4(), 'KEPALA_SEKOLAH'),
  (uuid_generate_v4(), 'GURU'),
  (uuid_generate_v4(), 'OPERATOR')
ON CONFLICT (role_name) DO NOTHING;

-- Seed auth_user admin awal
-- Password: 'admin123'
INSERT INTO auth_user (
  id, full_name, username, email, password_hash,
  account_non_expired, account_non_locked, credentials_non_expired, is_enabled
) VALUES (
  uuid_generate_v4(),
  'Administrator',
  'admin',
  'admin@upt-sdi-bonerate.sch.id',
  '$2a$10$4sSk39.BVbce.8fFhutlweFCoY2SabLOnuaXEcwSOthjP8js68726',
  true, true, true, true
) ON CONFLICT (username) DO NOTHING;

-- Assign role ADMIN ke admin user
INSERT INTO auth_user_role (user_id, role_id)
SELECT u.id, r.id
FROM auth_user u, auth_role r
WHERE u.username = 'admin' AND r.role_name = 'ADMIN'
ON CONFLICT DO NOTHING;
