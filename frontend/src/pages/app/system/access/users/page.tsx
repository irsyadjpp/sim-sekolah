import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Checkbox,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  IconButton,
  InputAdornment,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import NiKey from "@/icons/nexture/ni-key";
import NiPen from "@/icons/nexture/ni-pen";
import NiSearch from "@/icons/nexture/ni-search";
import NiShieldCheck from "@/icons/nexture/ni-shield-check";

interface Role {
  ID: string;
  RoleName: string;
}

interface User {
  id: string;
  username: string;
  full_name: string;
  email: string;
  is_enabled: boolean;
  account_non_locked: boolean;
  roles: Role[];
}

export default function UsersPage() {
  const { t } = useTranslation();
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

  const [users, setUsers] = useState<User[]>([]);
  const [allRoles, setAllRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [error, setError] = useState<string | null>(null);

  // Modals state
  const [openStatusModal, setOpenStatusModal] = useState(false);
  const [openRoleModal, setOpenRoleModal] = useState(false);
  const [openPasswordModal, setOpenPasswordModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  // Status state
  const [statusEnabled, setStatusEnabled] = useState(true);
  const [statusUnlocked, setStatusUnlocked] = useState(true);

  // Roles state
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);

  // Password state
  const [newPassword, setNewPassword] = useState("");

  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    fetchRoles();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchUsers();
    }, 500);
    return () => clearTimeout(timer);
  }, [search]);

  const fetchRoles = async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/users/roles`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setAllRoles(json.data || []);
      }
    } catch (err: any) {
      console.error("Gagal mengambil roles", err);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/users?limit=10000&search=${search}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setUsers(json.data || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers for Status ---
  const handleOpenStatus = (u: User) => {
    setSelectedUser(u);
    setStatusEnabled(u.is_enabled);
    setStatusUnlocked(u.account_non_locked);
    setOpenStatusModal(true);
  };

  const handleSaveStatus = async () => {
    if (!selectedUser) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/users/${selectedUser.id}/status`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          is_enabled: statusEnabled,
          account_non_locked: statusUnlocked,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenStatusModal(false);
        fetchUsers();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  // --- Handlers for Roles ---
  const handleOpenRoles = (u: User) => {
    setSelectedUser(u);
    setSelectedRoles(u.roles?.map((r) => r.RoleName) || []);
    setOpenRoleModal(true);
  };

  const handleToggleRole = (roleName: string) => {
    setSelectedRoles((prev) => (prev.includes(roleName) ? prev.filter((r) => r !== roleName) : [...prev, roleName]));
  };

  const handleSaveRoles = async () => {
    if (!selectedUser) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/users/${selectedUser.id}/roles`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ role_names: selectedRoles }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenRoleModal(false);
        fetchUsers();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  // --- Handlers for Password ---
  const handleOpenPassword = (u: User) => {
    setSelectedUser(u);
    setNewPassword("");
    setOpenPasswordModal(true);
  };

  const handleSavePassword = async () => {
    if (!selectedUser) return;
    if (newPassword.length < 6) {
      alert("Password minimal 6 karakter");
      return;
    }
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/users/${selectedUser.id}/reset-password`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_password: newPassword }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenPasswordModal(false);
        alert("Password berhasil direset!");
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "users", data: users, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Manajemen Pengguna
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/system">Sistem</Link>
        <Link to="/system/access">Akses</Link>
        <Typography variant="body2">Pengguna</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="p-4">
          <TextField
            fullWidth
            placeholder="Cari nama, username, atau email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            size="small"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <NiSearch size="small" />
                </InputAdornment>
              ),
            }}
          />
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell className="font-bold" sortDirection={sortBy === "username" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "username"}
                  direction={sortBy === "username" ? sortDir : "asc"}
                  onClick={() => handleSort("username")}
                >
                  Username
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "full_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "full_name"}
                  direction={sortBy === "full_name" ? sortDir : "asc"}
                  onClick={() => handleSort("full_name")}
                >
                  Nama Lengkap
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold">Roles</TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "is_enabled" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "is_enabled"}
                  direction={sortBy === "is_enabled" ? sortDir : "asc"}
                  onClick={() => handleSort("is_enabled")}
                >
                  Status
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" align="center">
                Aksi
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((u) => (
                <TableRow key={u.id} hover>
                  <TableCell>{u.username}</TableCell>
                  <TableCell className="font-medium">
                    {u.full_name}
                    <Typography variant="caption" display="block" color="textSecondary">
                      {u.email}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    {u.roles?.map((r) => (
                      <Chip key={r.ID} label={getRoleLabel(r.RoleName)} size="small" className="mr-1 mb-1" />
                    ))}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={u.is_enabled ? "Aktif" : "Non-aktif"}
                      color={u.is_enabled ? "success" : "default"}
                      size="small"
                      className="mr-1"
                    />
                    {!u.account_non_locked && <Chip label="Terkunci" color="error" size="small" />}
                  </TableCell>
                  <TableCell align="center">
                    <IconButton size="small" color="info" onClick={() => handleOpenStatus(u)} title="Ubah Status">
                      <NiPen size="small" />
                    </IconButton>
                    <IconButton size="small" color="warning" onClick={() => handleOpenRoles(u)} title="Atur Roles">
                      <NiShieldCheck size="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleOpenPassword(u)} title="Reset Password">
                      <NiKey size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  Tidak ada data pengguna.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={total}
          page={page - 1}
          onPageChange={(_, newPage) => handlePageChange(newPage + 1)}
          rowsPerPage={limit}
          onRowsPerPageChange={(e) => handleLimitChange(parseInt(e.target.value, 10))}
          labelRowsPerPage="Baris per halaman:"
        />
      </TableContainer>

      {/* Modal Status */}
      <Dialog open={openStatusModal} onClose={() => setOpenStatusModal(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Ubah Status Pengguna</DialogTitle>
        <DialogContent dividers className="flex flex-col gap-2">
          <FormControlLabel
            control={<Checkbox checked={statusEnabled} onChange={(e) => setStatusEnabled(e.target.checked)} />}
            label="Akun Aktif (Enabled)"
          />
          <FormControlLabel
            control={<Checkbox checked={statusUnlocked} onChange={(e) => setStatusUnlocked(e.target.checked)} />}
            label="Akun Tidak Terkunci (Unlocked)"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenStatusModal(false)} color="inherit">
            Batal
          </Button>
          <Button onClick={handleSaveStatus} variant="contained" color="primary">
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal Roles */}
      <Dialog open={openRoleModal} onClose={() => setOpenRoleModal(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Atur Roles ({selectedUser?.username})</DialogTitle>
        <DialogContent dividers className="flex flex-col">
          {allRoles.length === 0 ? (
            <Typography variant="body2" color="textSecondary">
              Memuat roles...
            </Typography>
          ) : (
            allRoles.map((role) => (
              <FormControlLabel
                key={role.ID}
                control={
                  <Checkbox
                    checked={selectedRoles.includes(role.RoleName)}
                    onChange={() => handleToggleRole(role.RoleName)}
                  />
                }
                label={getRoleLabel(role.RoleName)}
              />
            ))
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenRoleModal(false)} color="inherit">
            Batal
          </Button>
          <Button onClick={handleSaveRoles} variant="contained" color="primary">
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal Password */}
      <Dialog open={openPasswordModal} onClose={() => setOpenPasswordModal(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Reset Password</DialogTitle>
        <DialogContent dividers>
          <Typography variant="body2" className="mb-4">
            Reset password untuk <strong>{selectedUser?.username}</strong>.
          </Typography>
          <TextField
            label="Password Baru"
            type="password"
            fullWidth
            size="small"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPasswordModal(false)} color="inherit">
            Batal
          </Button>
          <Button onClick={handleSavePassword} variant="contained" color="error">
            Reset
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
