import RolePermissionList from "./sections/role-permission-list";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import GroupIcon from "@mui/icons-material/Group";
import LockIcon from "@mui/icons-material/Lock";
import SaveIcon from "@mui/icons-material/Save";
import ShieldIcon from "@mui/icons-material/Shield";
import {
  Alert,
  Avatar,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Fade,
  Grid,
  ListItemIcon,
  ListItemText,
  MenuItem,
  MenuList,
  Paper,
  Snackbar,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface Role {
  ID: string;
  RoleName: string;
}

interface Permission {
  id: string;
  permission_name: string;
  description: string;
}

// Helper to map UI action grid cells to database permission names (needed for clean toggle)
const getPermissionName = (moduleKey: string, action: "view" | "create" | "edit" | "delete"): string | null => {
  if (moduleKey === "system") {
    if (action === "view") return "system:view";
    if (action === "create") return "system:access";
    if (action === "edit") return "system:update";
    return null;
  }
  if (moduleKey === "school") {
    if (action === "view") return "school:view";
    if (action === "edit") return "school:update";
    return null;
  }
  if (moduleKey === "staff") {
    if (action === "view") return "staff:view";
    if (action === "create") return "staff:create";
    if (action === "edit") return "staff:update";
    if (action === "delete") return "staff:delete";
  }
  if (moduleKey === "student") {
    if (action === "view") return "student:view";
    if (action === "create") return "student:create";
    if (action === "edit") return "student:update";
    if (action === "delete") return "student:delete";
  }
  if (moduleKey === "ppdb") {
    if (action === "view") return "ppdb:view";
    if (action === "edit") return "ppdb:update";
    return null;
  }
  if (moduleKey === "curriculum") {
    if (action === "view") return "curriculum:view";
    if (action === "edit") return "curriculum:update";
    return null;
  }
  if (moduleKey === "classroom") {
    if (action === "view") return "classroom:view";
    if (action === "create") return "classroom:create";
    if (action === "edit") return "classroom:update";
    if (action === "delete") return "classroom:delete";
  }
  if (moduleKey === "presence") {
    if (action === "view") return "presence:view";
    if (action === "edit") return "presence:update";
    return null;
  }
  if (moduleKey === "modules") {
    if (action === "view") return "modules:view";
    if (action === "edit") return "modules:update";
    return null;
  }
  if (moduleKey === "assessment") {
    if (action === "view") return "assessment:view";
    if (action === "edit") return "assessment:update";
    return null;
  }
  if (moduleKey === "counseling") {
    if (action === "view") return "counseling:view";
    if (action === "create") return "counseling:create";
    if (action === "edit") return "counseling:update";
    return null;
  }
  if (moduleKey === "report") {
    if (action === "view") return "report:view";
    if (action === "edit") return "report:finalize";
    return null;
  }
  return null;
};

export default function RolesPage() {
  const { t } = useTranslation();
  const [roles, setRoles] = useState<Role[]>([]);
  const [allPermissions, setAllPermissions] = useState<Permission[]>([]);

  // Maps roleId -> Set of active permission IDs
  const [originalPermissions, setOriginalPermissions] = useState<Record<string, Set<string>>>({});
  const [localPermissions, setLocalPermissions] = useState<Record<string, Set<string>>>({});

  const [selectedRoleId, setSelectedRoleId] = useState<string | null>(null);

  const [loading, setLoading] = useState(true);

  const getRoleLabel = (roleName: string): string => {
    const key = `rbac.role-${roleName}`;
    const translated = t(key);
    if (translated === key) {
      return roleName
        .toLowerCase()
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
    }
    return translated;
  };
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: "success" | "error" }>({
    open: false,
    message: "",
    severity: "success",
  });

  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch Roles
      const rolesRes = await fetch(`${DEFAULTS.API_URL}/api/v1/users/roles`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const rolesJson = await rolesRes.json();
      if (rolesJson.status !== "success") {
        throw new Error(rolesJson.message || "Gagal mengambil data roles");
      }
      const fetchedRoles: Role[] = rolesJson.data || [];
      setRoles(fetchedRoles);

      // 2. Fetch All Available Permissions
      const permsRes = await fetch(`${DEFAULTS.API_URL}/api/v1/permissions`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const permsJson = await permsRes.json();
      if (permsJson.status !== "success") {
        throw new Error(permsJson.message || "Gagal mengambil data perizinan");
      }
      const fetchedPerms: Permission[] = permsJson.data || [];
      setAllPermissions(fetchedPerms);

      // 3. Parallel fetch permissions for each role to build initial mapping
      const mappingOriginal: Record<string, Set<string>> = {};
      const mappingLocal: Record<string, Set<string>> = {};

      await Promise.all(
        fetchedRoles.map(async (role) => {
          try {
            const rolePermsRes = await fetch(`${DEFAULTS.API_URL}/api/v1/permissions/roles/${role.ID}`, {
              headers: { Authorization: `Bearer ${token}` },
            });
            const rolePermsJson = await rolePermsRes.json();
            if (rolePermsJson.status === "success") {
              const activePerms: Permission[] = rolePermsJson.data || [];
              const activeIds = activePerms.map((p) => p.id);
              mappingOriginal[role.ID] = new Set(activeIds);
              mappingLocal[role.ID] = new Set(activeIds);
            } else {
              mappingOriginal[role.ID] = new Set();
              mappingLocal[role.ID] = new Set();
            }
          } catch (e) {
            mappingOriginal[role.ID] = new Set();
            mappingLocal[role.ID] = new Set();
          }
        }),
      );

      setOriginalPermissions(mappingOriginal);
      setLocalPermissions(mappingLocal);

      // Auto select first role if available
      if (fetchedRoles.length > 0) {
        setSelectedRoleId(fetchedRoles[0].ID);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePermission = (moduleKey: string, action: "view" | "create" | "edit" | "delete") => {
    if (!selectedRoleId) return;

    const permName = getPermissionName(moduleKey, action);
    if (!permName) return;

    const permObj = allPermissions.find((p) => p.permission_name === permName);
    if (!permObj) return;

    const permId = permObj.id;

    setLocalPermissions((prev) => {
      const currentSet = new Set(prev[selectedRoleId] || []);
      if (currentSet.has(permId)) {
        currentSet.delete(permId);
      } else {
        currentSet.add(permId);
      }
      return {
        ...prev,
        [selectedRoleId]: currentSet,
      };
    });
  };

  const checkIsDirty = (): boolean => {
    if (!selectedRoleId) return false;
    const originalSet = originalPermissions[selectedRoleId] || new Set();
    const localSet = localPermissions[selectedRoleId] || new Set();

    if (originalSet.size !== localSet.size) return true;
    for (const id of Array.from(localSet)) {
      if (!originalSet.has(id)) return true;
    }
    return false;
  };

  const handleSaveChanges = async () => {
    if (!selectedRoleId) return;
    setSaving(true);
    try {
      const activeIds = Array.from(localPermissions[selectedRoleId] || []);
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/permissions/roles/${selectedRoleId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ permission_ids: activeIds }),
      });
      const json = await res.json();
      if (json.status === "success") {
        // Sync original state with successfully saved local state
        setOriginalPermissions((prev) => ({
          ...prev,
          [selectedRoleId]: new Set(activeIds),
        }));
        setSnackbar({
          open: true,
          message: t("rbac.save-success"),
          severity: "success",
        });
      } else {
        throw new Error(json.message || t("rbac.save-error"));
      }
    } catch (err: any) {
      setSnackbar({
        open: true,
        message: err.message || t("rbac.save-error"),
        severity: "error",
      });
    } finally {
      setSaving(false);
    }
  };

  const selectedRole = roles.find((r) => r.ID === selectedRoleId);
  const isDirty = checkIsDirty();

  return (
    <Box sx={{ pb: 10, position: "relative" }}>
      <Box className="mb-2 flex items-center justify-between">
        <Typography
          variant="h1"
          component="h1"
          className="mb-0"
          sx={{ display: "flex", alignItems: "center", gap: 1.5 }}
        >
          <ShieldIcon color="primary" sx={{ fontSize: 36 }} />
          {t("rbac.title")}
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">{t("staff-form.breadcrumb-home")}</Link>
        <Link to="/system">Sistem</Link>
        <Link to="/system/access">Akses</Link>
        <Typography variant="body2">Peran & Izin</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4" sx={{ borderRadius: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* LEFT PANEL: ROLES LIST */}
        <Grid size={{ xs: 12, md: 3 }}>
          <Card className="mb-5" sx={{ borderRadius: 3, boxShadow: "0 4px 20px rgba(0,0,0,0.05)" }}>
            <CardContent className="flex flex-col items-center gap-5">
              <Box className="flex flex-col items-center">
                <Avatar
                  alt="avatar"
                  className="bg-primary-lighter text-primary-main mb-2 h-20 w-20 rounded-4xl"
                  sx={{ width: 80, height: 80 }}
                >
                  <ShieldIcon sx={{ fontSize: 40, color: "primary.main" }} />
                </Avatar>
                <Typography variant="subtitle1" component="p" sx={{ fontWeight: 700 }}>
                  Manajemen Peran
                </Typography>
                <Typography variant="body2" component="p" className="text-text-secondary -mt-0.5">
                  UPT SDI Bonerate No. 85
                </Typography>
              </Box>

              <Box className="w-full">
                {loading ? (
                  <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", py: 5 }}>
                    <CircularProgress size={28} sx={{ mr: 1.5 }} />
                    <Typography variant="body2" color="textSecondary">
                      {t("rbac.loading")}
                    </Typography>
                  </Box>
                ) : (
                  <MenuList className="p-0">
                    {roles.map((role) => {
                      const isSelected = selectedRoleId === role.ID;
                      const activeCount = localPermissions[role.ID]?.size || 0;
                      return (
                        <MenuItem
                          key={role.ID}
                          selected={isSelected}
                          onClick={() => setSelectedRoleId(role.ID)}
                          sx={{
                            borderRadius: 2,
                            mb: 0.5,
                            py: 1.5,
                            backgroundColor: isSelected ? "primary.lighter" : "transparent",
                            color: isSelected ? "primary.main" : "text.primary",
                            "&.Mui-selected": {
                              backgroundColor: "rgba(25, 118, 210, 0.08)",
                              "&:hover": {
                                backgroundColor: "rgba(25, 118, 210, 0.12)",
                              },
                            },
                          }}
                        >
                          <ListItemIcon sx={{ minWidth: 36 }}>
                            <GroupIcon fontSize="small" color={isSelected ? "primary" : "inherit"} />
                          </ListItemIcon>
                          <ListItemText
                            primary={getRoleLabel(role.RoleName)}
                            primaryTypographyProps={{ sx: { fontWeight: isSelected ? 700 : 500, fontSize: "0.9rem" } }}
                            secondary={`${activeCount} Hak Akses`}
                            secondaryTypographyProps={{
                              sx: { fontSize: "0.75rem", color: isSelected ? "primary.main" : "text.secondary" },
                            }}
                          />
                        </MenuItem>
                      );
                    })}
                  </MenuList>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* RIGHT PANEL: PERMISSIONS MATRIX TABLE */}
        <Grid size={{ xs: 12, md: 9 }}>
          <Card sx={{ borderRadius: 3, boxShadow: "0 4px 20px rgba(0,0,0,0.05)", overflow: "visible" }}>
            <Box
              sx={{
                p: 2.5,
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                backgroundColor: "action.hover",
              }}
            >
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <LockIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {t("rbac.permissions-matrix")} —{" "}
                  <Box component="span" sx={{ color: "primary.main", fontWeight: 700 }}>
                    {selectedRole ? getRoleLabel(selectedRole.RoleName) : "..."}
                  </Box>
                </Typography>
              </Box>
              {isDirty && (
                <Chip
                  label="Perubahan Belum Disimpan"
                  color="warning"
                  size="small"
                  sx={{ fontWeight: 600, animation: "pulse 2s infinite" }}
                />
              )}
            </Box>
            <Divider />

            <RolePermissionList
              selectedRoleId={selectedRoleId}
              selectedRoleName={selectedRole?.RoleName}
              allPermissions={allPermissions}
              localPermissions={localPermissions}
              saving={saving}
              loading={loading}
              handleTogglePermission={handleTogglePermission}
            />
          </Card>
        </Grid>
      </Grid>

      {/* FLOATING ACTION BAR FOR UNSAVED CHANGES */}
      <Fade in={isDirty}>
        <Paper
          elevation={6}
          sx={{
            position: "fixed",
            bottom: 24,
            left: "50%",
            transform: "translateX(-50%)",
            zIndex: 1100,
            p: 2,
            px: 4,
            borderRadius: 4,
            display: "flex",
            alignItems: "center",
            gap: 3,
            backgroundColor: "background.paper",
            border: "1px solid",
            borderColor: "primary.main",
            boxShadow: "0 10px 30px rgba(25, 118, 210, 0.15)",
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
            <ShieldIcon color="warning" />
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              Ada perubahan izin hak akses yang belum disimpan.
            </Typography>
          </Box>
          <Box sx={{ display: "flex", gap: 1.5 }}>
            <Button
              variant="outlined"
              size="small"
              color="inherit"
              disabled={saving}
              onClick={() => {
                // Discard changes
                if (selectedRoleId) {
                  setLocalPermissions((prev) => ({
                    ...prev,
                    [selectedRoleId]: new Set(originalPermissions[selectedRoleId] || []),
                  }));
                }
              }}
              sx={{ borderRadius: 2 }}
            >
              Reset
            </Button>
            <Button
              variant="contained"
              size="small"
              color="primary"
              disabled={saving}
              onClick={handleSaveChanges}
              startIcon={saving ? <CircularProgress size={16} color="inherit" /> : <SaveIcon />}
              sx={{ borderRadius: 2, px: 3, fontWeight: 600 }}
            >
              {saving ? t("rbac.saving") : t("rbac.save-button")}
            </Button>
          </Box>
        </Paper>
      </Fade>

      {/* FEEDBACK TOAST SNACKBAR */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          variant="filled"
          icon={<CheckCircleIcon />}
          sx={{ borderRadius: 2, fontWeight: 500 }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
