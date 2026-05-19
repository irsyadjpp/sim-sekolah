DROP TABLE IF EXISTS auth_user_session CASCADE;
DROP TABLE IF EXISTS auth_role_permission CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
ALTER TABLE auth_user DROP COLUMN IF EXISTS totp_secret;
