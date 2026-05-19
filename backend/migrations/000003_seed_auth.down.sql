DELETE FROM auth_user_role WHERE user_id IN (SELECT id FROM auth_user WHERE username = 'admin');
DELETE FROM auth_user WHERE username = 'admin';
DELETE FROM auth_role WHERE role_name IN ('ADMIN','KEPALA_SEKOLAH','GURU','OPERATOR');
