-- Seed tambahan role ideal tingkat SD (English)
INSERT INTO auth_role (id, role_name) VALUES
  (uuid_generate_v4(), 'CLERK'),
  (uuid_generate_v4(), 'HOMEROOM_TEACHER'),
  (uuid_generate_v4(), 'EXTRACURRICULAR_INSTRUCTOR'),
  (uuid_generate_v4(), 'STUDENT'),
  (uuid_generate_v4(), 'PARENT')
ON CONFLICT (role_name) DO NOTHING;
