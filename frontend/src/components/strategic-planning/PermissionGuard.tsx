import { ReactNode } from "react";

import { Alert, Box } from "@mui/material";
import NiLock from "@/icons/nexture/ni-lock";

interface UserRole {
  role?: string;
  roles?: string[];
  permissions?: string[];
}

interface PermissionGuardProps {
  children: ReactNode;
  allowedRoles?: string[];
  allowedPermissions?: string[];
  fallback?: ReactNode;
}

export function getUserRole(): UserRole | null {
  try {
    const cachedUser = localStorage.getItem("-user-data");
    if (cachedUser) {
      return JSON.parse(cachedUser);
    }
  } catch (e) {
    console.error("Failed to parse user data", e);
  }
  return null;
}

export function hasPermission(
  user: UserRole | null,
  allowedRoles?: string[],
  allowedPermissions?: string[]
): boolean {
  if (!user) return false;

  // Check roles
  if (allowedRoles && allowedRoles.length > 0) {
    const userRoles = [user.role, ...(user.roles || [])].filter(Boolean);
    const hasRole = allowedRoles.some((allowedRole) => userRoles.includes(allowedRole));
    if (!hasRole) return false;
  }

  // Check permissions
  if (allowedPermissions && allowedPermissions.length > 0) {
    const userPermissions = user.permissions || [];
    const hasPermission = allowedPermissions.some((allowedPerm) =>
      userPermissions.includes(allowedPerm)
    );
    if (!hasPermission) return false;
  }

  return true;
}

export default function PermissionGuard({
  children,
  allowedRoles,
  allowedPermissions,
  fallback,
}: PermissionGuardProps) {
  const user = getUserRole();
  const canAccess = hasPermission(user, allowedRoles, allowedPermissions);

  if (!canAccess) {
    if (fallback) {
      return <>{fallback}</>;
    }

    return (
      <Box className="flex justify-center items-center py-12">
        <Alert
          severity="warning"
          icon={<NiLock size="small" />}
          className="max-w-md"
        >
          Anda tidak memiliki izin untuk mengakses halaman ini.
        </Alert>
      </Box>
    );
  }

  return <>{children}</>;
}