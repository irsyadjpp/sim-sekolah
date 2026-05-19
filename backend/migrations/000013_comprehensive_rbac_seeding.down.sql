DELETE FROM auth_role_permission;
DELETE FROM auth_permission WHERE permission_name IN (
  'system:view', 'system:update', 'system:access',
  'school:view', 'school:update',
  'staff:view', 'staff:create', 'staff:update', 'staff:delete',
  'student:view', 'student:create', 'student:update', 'student:delete',
  'ppdb:view', 'ppdb:update',
  'curriculum:view', 'curriculum:update',
  'classroom:create', 'classroom:update', 'classroom:delete',
  'presence:view', 'presence:update',
  'modules:view', 'modules:update',
  'assessment:view', 'assessment:update',
  'counseling:view', 'counseling:create', 'counseling:update',
  'report:view'
);
