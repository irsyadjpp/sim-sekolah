import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  Avatar,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Checkbox,
  Chip,
  CircularProgress,
  FormControl,
  Grid,
  InputLabel,
  ListItemText,
  MenuItem,
  OutlinedInput,
  Pagination,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface AuditLog {
  id: string;
  user_id: string | null;
  action: string;
  entity: string;
  entity_id: string;
  ip_address: string;
  created_at: string;
  user_full_name?: string;
  user_email?: string;
}

export default function SecurityAuditPage() {
  const { t } = useTranslation();
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [actionFilter, setActionFilter] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;

  // Sorting states
  const [sortField, setSortField] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Column visibility states
  const [visibleColumns, setVisibleColumns] = useState<string[]>(["actor", "action", "details", "ip", "time"]);

  const token = localStorage.getItem("accessToken");

  const handleSort = (field: string) => {
    const isAsc = sortField === field && sortOrder === "asc";
    setSortOrder(isAsc ? "desc" : "asc");
    setSortField(field);
  };

  const handleExportCSV = () => {
    if (logs.length === 0) {
      alert("Tidak ada data untuk diekspor");
      return;
    }
    const headers = ["Aktor", "Email", "Aksi", "Detail", "IP Address", "Waktu"];
    const csvRows = [headers.join(",")];

    logs.forEach((log) => {
      const row = [
        `"${log.user_full_name || "System"}"`,
        `"${log.user_email || "system@intranet.school"}"`,
        `"${log.action}"`,
        `"${getReadableDetails(log).replace(/"/g, '""')}"`,
        `"${log.ip_address || "127.0.0.1"}"`,
        `"${new Date(log.created_at).toLocaleString()}"`,
      ];
      csvRows.push(row.join(","));
    });

    const csvContent = "data:text/csv;charset=utf-8," + csvRows.join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `Audit_Log_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const sortedLogs = [...logs].sort((a, b) => {
    let aVal = (a as any)[sortField] || "";
    let bVal = (b as any)[sortField] || "";
    if (sortField === "user_full_name") {
      aVal = a.user_full_name || "System";
      bVal = b.user_full_name || "System";
    }
    if (sortField === "created_at") {
      return sortOrder === "asc"
        ? new Date(aVal).getTime() - new Date(bVal).getTime()
        : new Date(bVal).getTime() - new Date(aVal).getTime();
    }
    return sortOrder === "asc" ? String(aVal).localeCompare(String(bVal)) : String(bVal).localeCompare(String(aVal));
  });

  // Fetch audit logs from backend API
  const fetchLogs = async () => {
    setLoading(true);
    try {
      const url = new URL(`${DEFAULTS.API_URL}/api/v1/system/audit-logs`);
      url.searchParams.append("page", page.toString());
      url.searchParams.append("limit", limit.toString());
      if (search) url.searchParams.append("search", search);
      if (actionFilter) url.searchParams.append("action", actionFilter);

      const res = await fetch(url.toString(), {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setLogs(json.data || []);
        setTotal(json.pagination?.total_items || json.total || 0);
      }
    } catch (err) {
      console.error("Gagal memuat log audit:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [page, actionFilter]);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setPage(1);
      fetchLogs();
    }, 500);
    return () => clearTimeout(timer);
  }, [search]);

  // Helper to format action badges
  const getActionBadge = (action: string) => {
    switch (action.toUpperCase()) {
      case "CREATE":
        return (
          <Chip
            label={t("audit.action-create")}
            size="small"
            sx={{
              bgcolor: "rgba(16, 185, 129, 0.12)",
              color: "#10b981",
              fontWeight: "bold",
              border: "1px solid rgba(16, 185, 129, 0.3)",
            }}
          />
        );
      case "READ":
        return (
          <Chip
            label={t("audit.action-read")}
            size="small"
            sx={{
              bgcolor: "rgba(59, 130, 246, 0.12)",
              color: "#3b82f6",
              fontWeight: "bold",
              border: "1px solid rgba(59, 130, 246, 0.3)",
            }}
          />
        );
      case "UPDATE":
        return (
          <Chip
            label={t("audit.action-update")}
            size="small"
            sx={{
              bgcolor: "rgba(245, 158, 11, 0.12)",
              color: "#f59e0b",
              fontWeight: "bold",
              border: "1px solid rgba(245, 158, 11, 0.3)",
            }}
          />
        );
      case "DELETE":
        return (
          <Chip
            label={t("audit.action-delete")}
            size="small"
            sx={{
              bgcolor: "rgba(239, 68, 68, 0.12)",
              color: "#ef4444",
              fontWeight: "bold",
              border: "1px solid rgba(239, 68, 68, 0.3)",
            }}
          />
        );
      case "LOGIN":
        return (
          <Chip
            label={t("audit.action-login")}
            size="small"
            sx={{
              bgcolor: "rgba(139, 92, 246, 0.12)",
              color: "#8b5cf6",
              fontWeight: "bold",
              border: "1px solid rgba(139, 92, 246, 0.3)",
            }}
          />
        );
      case "MFA_ENABLE":
      case "MFA_DISABLE":
      case "MFA_SETUP":
        return (
          <Chip
            label={t("audit.action-mfa")}
            size="small"
            sx={{
              bgcolor: "rgba(20, 184, 166, 0.12)",
              color: "#14b8a6",
              fontWeight: "bold",
              border: "1px solid rgba(20, 184, 166, 0.3)",
            }}
          />
        );
      default:
        return <Chip label={action} size="small" sx={{ fontWeight: "bold" }} />;
    }
  };

  // Human-readable descriptions mapping
  const getReadableDetails = (log: AuditLog) => {
    const isIndo = localStorage.getItem("i18nextLng")?.startsWith("id");
    const entityLabel =
      log.entity === "student"
        ? isIndo
          ? "Profil Siswa"
          : "Student Profile"
        : log.entity === "student_parent"
          ? isIndo
            ? "Data Orang Tua Siswa"
            : "Student Parent Data"
          : log.entity === "security"
            ? isIndo
              ? "Pengaturan 2FA"
              : "2FA Settings"
            : log.entity === "auth"
              ? isIndo
                ? "Sesi Otentikasi"
                : "Auth Session"
              : log.entity;

    switch (log.action.toUpperCase()) {
      case "READ":
        return isIndo
          ? `Membuka detail ${entityLabel} (ID: ${log.entity_id})`
          : `Opened details of ${entityLabel} (ID: ${log.entity_id})`;
      case "CREATE":
        return isIndo
          ? `Membuat rekaman ${entityLabel} baru (ID: ${log.entity_id})`
          : `Created new ${entityLabel} record (ID: ${log.entity_id})`;
      case "UPDATE":
        return isIndo
          ? `Memperbarui ${entityLabel} (ID: ${log.entity_id})`
          : `Updated ${entityLabel} (ID: ${log.entity_id})`;
      case "DELETE":
        return isIndo
          ? `Menghapus data ${entityLabel} (ID: ${log.entity_id})`
          : `Deleted ${entityLabel} data (ID: ${log.entity_id})`;
      case "LOGIN":
        return isIndo ? `Berhasil login sistem melalui perangkat` : `Successfully signed into the system`;
      case "MFA_ENABLE":
        return isIndo ? `Mengaktifkan Autentikasi Dua Faktor (2FA)` : `Enabled Two-Factor Authentication (2FA)`;
      case "MFA_DISABLE":
        return isIndo ? `Menonaktifkan Autentikasi Dua Faktor (2FA)` : `Disabled Two-Factor Authentication (2FA)`;
      default:
        return `${log.action} on ${log.entity} (${log.entity_id})`;
    }
  };

  // Stats calculation
  const totalToday = total; // Simplified representation
  const activeUsersCount = new Set(logs.map((l) => l.user_id)).size;
  const alertCount = logs.filter((l) =>
    ["DELETE", "MFA_DISABLE", "MFA_ENABLE"].includes(l.action.toUpperCase()),
  ).length;

  return (
    <Box sx={{ pb: 6 }}>
      {/* Title Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h1" component="h1" sx={{ fontWeight: "bold", mb: 1, fontSize: "2rem" }}>
          {t("audit.title")}
        </Typography>
        <Breadcrumbs sx={{ mb: 2 }}>
          <Link to="/dashboards/default" style={{ textDecoration: "none", color: "inherit" }}>
            Home
          </Link>
          <Link to="/system" style={{ textDecoration: "none", color: "inherit" }}>
            Sistem
          </Link>
          <Typography color="text.secondary" variant="body2">
            {t("audit.title")}
          </Typography>
        </Breadcrumbs>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {t("audit.subtitle")}
        </Typography>
      </Box>

      {/* KPI Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, sm: 4 }}>
          <Card
            sx={{
              borderRadius: "16px",
              boxShadow: "0 4px 20px 0 rgba(0,0,0,0.05)",
              border: "1px solid rgba(0,0,0,0.08)",
              overflow: "hidden",
              position: "relative",
            }}
          >
            <Box sx={{ position: "absolute", top: 0, left: 0, height: "4px", width: "100%", bgcolor: "#3b82f6" }} />
            <CardContent sx={{ p: 3, display: "flex", alignItems: "center", justifyItems: "center" }}>
              <Box sx={{ mr: 2, p: 1.5, borderRadius: "12px", bgcolor: "rgba(59, 130, 246, 0.1)", display: "flex" }}>
                <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="#3b82f6" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ fontWeight: "medium" }}>
                  {t("audit.total-activities")}
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: "bold", mt: 0.5 }}>
                  {totalToday}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 4 }}>
          <Card
            sx={{
              borderRadius: "16px",
              boxShadow: "0 4px 20px 0 rgba(0,0,0,0.05)",
              border: "1px solid rgba(0,0,0,0.08)",
              overflow: "hidden",
              position: "relative",
            }}
          >
            <Box sx={{ position: "absolute", top: 0, left: 0, height: "4px", width: "100%", bgcolor: "#8b5cf6" }} />
            <CardContent sx={{ p: 3, display: "flex", alignItems: "center" }}>
              <Box sx={{ mr: 2, p: 1.5, borderRadius: "12px", bgcolor: "rgba(139, 92, 246, 0.1)", display: "flex" }}>
                <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="#8b5cf6" strokeWidth="2">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                  />
                </svg>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ fontWeight: "medium" }}>
                  {t("audit.unique-users")}
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: "bold", mt: 0.5 }}>
                  {activeUsersCount}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 4 }}>
          <Card
            sx={{
              borderRadius: "16px",
              boxShadow: "0 4px 20px 0 rgba(0,0,0,0.05)",
              border: "1px solid rgba(0,0,0,0.08)",
              overflow: "hidden",
              position: "relative",
            }}
          >
            <Box sx={{ position: "absolute", top: 0, left: 0, height: "4px", width: "100%", bgcolor: "#ef4444" }} />
            <CardContent sx={{ p: 3, display: "flex", alignItems: "center" }}>
              <Box sx={{ mr: 2, p: 1.5, borderRadius: "12px", bgcolor: "rgba(239, 68, 68, 0.1)", display: "flex" }}>
                <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="#ef4444" strokeWidth="2">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ fontWeight: "medium" }}>
                  {t("audit.security-alerts")}
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: "bold", mt: 0.5 }}>
                  {alertCount}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filter & Table Actions Panel */}
      <Card
        sx={{
          borderRadius: "16px",
          boxShadow: "0 4px 20px 0 rgba(0,0,0,0.05)",
          border: "1px solid rgba(0,0,0,0.08)",
          mb: 4,
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Grid container spacing={3} alignItems="center">
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                fullWidth
                size="small"
                placeholder={t("audit.search-placeholder")}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <Box sx={{ mr: 1, display: "flex", color: "text.secondary" }}>
                      <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                      </svg>
                    </Box>
                  ),
                }}
              />
            </Grid>

            {/* Column Visibility Select */}
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Pilih Kolom</InputLabel>
                <Select
                  multiple
                  value={visibleColumns}
                  onChange={(e) =>
                    setVisibleColumns(typeof e.target.value === "string" ? e.target.value.split(",") : e.target.value)
                  }
                  input={<OutlinedInput label="Pilih Kolom" />}
                  renderValue={(selected) => `Kolom (${selected.length})`}
                >
                  <MenuItem value="actor">
                    <Checkbox checked={visibleColumns.includes("actor")} />
                    <ListItemText primary="Aktor" />
                  </MenuItem>
                  <MenuItem value="action">
                    <Checkbox checked={visibleColumns.includes("action")} />
                    <ListItemText primary="Aksi" />
                  </MenuItem>
                  <MenuItem value="details">
                    <Checkbox checked={visibleColumns.includes("details")} />
                    <ListItemText primary="Detail" />
                  </MenuItem>
                  <MenuItem value="ip">
                    <Checkbox checked={visibleColumns.includes("ip")} />
                    <ListItemText primary="IP Address" />
                  </MenuItem>
                  <MenuItem value="time">
                    <Checkbox checked={visibleColumns.includes("time")} />
                    <ListItemText primary="Waktu" />
                  </MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* Export CSV Button */}
            <Grid size={{ xs: 12, md: 4 }} sx={{ display: "flex", justifyContent: "flex-end" }}>
              <Button
                fullWidth
                variant="contained"
                onClick={handleExportCSV}
                startIcon={
                  <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                }
                sx={{
                  bgcolor: "#10b981",
                  borderRadius: "12px",
                  fontWeight: "bold",
                  py: 1,
                  textTransform: "none",
                  "&:hover": { bgcolor: "#059669" },
                }}
              >
                Ekspor ke CSV
              </Button>
            </Grid>

            {/* Action Chips Filters */}
            <Grid size={{ xs: 12 }}>
              <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1.2 }}>
                {[
                  { value: "", label: t("audit.filter-action"), color: "#6b7280" },
                  { value: "READ", label: t("audit.action-read"), color: "#3b82f6" },
                  { value: "CREATE", label: t("audit.action-create"), color: "#10b981" },
                  { value: "UPDATE", label: t("audit.action-update"), color: "#f59e0b" },
                  { value: "DELETE", label: t("audit.action-delete"), color: "#ef4444" },
                  { value: "LOGIN", label: t("audit.action-login"), color: "#8b5cf6" },
                  { value: "MFA_ENABLE", label: t("audit.action-mfa"), color: "#14b8a6" },
                ].map((item) => {
                  const isActive = actionFilter === item.value;
                  return (
                    <Chip
                      key={item.value}
                      label={item.label}
                      onClick={() => {
                        setActionFilter(item.value);
                        setPage(1);
                      }}
                      sx={{
                        fontWeight: "bold",
                        fontSize: "0.85rem",
                        cursor: "pointer",
                        transition: "all 0.2s ease",
                        bgcolor: isActive ? item.color : "rgba(0, 0, 0, 0.04)",
                        color: isActive ? "#ffffff" : "text.secondary",
                        border: `1px solid ${isActive ? item.color : "rgba(0, 0, 0, 0.08)"}`,
                        "&:hover": {
                          bgcolor: isActive ? item.color : "rgba(0, 0, 0, 0.08)",
                          transform: "translateY(-1px)",
                        },
                      }}
                    />
                  );
                })}
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Audit Log Table Container */}
      <TableContainer
        component={Card}
        sx={{
          maxHeight: 600,
          borderRadius: "16px",
          boxShadow: "0 4px 20px 0 rgba(0,0,0,0.05)",
          border: "1px solid rgba(0,0,0,0.08)",
        }}
      >
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {visibleColumns.includes("actor") && (
                <TableCell
                  onClick={() => handleSort("user_full_name")}
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "rgba(240,240,240,0.9)",
                    cursor: "pointer",
                    "&:hover": { bgcolor: "rgba(220,220,220,0.9)" },
                  }}
                >
                  <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                    {t("audit.col-actor")}
                    {sortField === "user_full_name" ? (sortOrder === "asc" ? "🔼" : "🔽") : "↕️"}
                  </Box>
                </TableCell>
              )}
              {visibleColumns.includes("action") && (
                <TableCell
                  onClick={() => handleSort("action")}
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "rgba(240,240,240,0.9)",
                    cursor: "pointer",
                    "&:hover": { bgcolor: "rgba(220,220,220,0.9)" },
                  }}
                >
                  <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                    {t("audit.col-action")}
                    {sortField === "action" ? (sortOrder === "asc" ? "🔼" : "🔽") : "↕️"}
                  </Box>
                </TableCell>
              )}
              {visibleColumns.includes("details") && (
                <TableCell
                  onClick={() => handleSort("entity")}
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "rgba(240,240,240,0.9)",
                    cursor: "pointer",
                    "&:hover": { bgcolor: "rgba(220,220,220,0.9)" },
                  }}
                >
                  <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                    {t("audit.col-details")}
                    {sortField === "entity" ? (sortOrder === "asc" ? "🔼" : "🔽") : "↕️"}
                  </Box>
                </TableCell>
              )}
              {visibleColumns.includes("ip") && (
                <TableCell
                  onClick={() => handleSort("ip_address")}
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "rgba(240,240,240,0.9)",
                    cursor: "pointer",
                    "&:hover": { bgcolor: "rgba(220,220,220,0.9)" },
                  }}
                >
                  <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                    {t("audit.col-ip")}
                    {sortField === "ip_address" ? (sortOrder === "asc" ? "🔼" : "🔽") : "↕️"}
                  </Box>
                </TableCell>
              )}
              {visibleColumns.includes("time") && (
                <TableCell
                  onClick={() => handleSort("created_at")}
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "rgba(240,240,240,0.9)",
                    cursor: "pointer",
                    "&:hover": { bgcolor: "rgba(220,220,220,0.9)" },
                  }}
                >
                  <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                    {t("audit.col-time")}
                    {sortField === "created_at" ? (sortOrder === "asc" ? "🔼" : "🔽") : "↕️"}
                  </Box>
                </TableCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={visibleColumns.length || 1} align="center" sx={{ py: 10 }}>
                  <CircularProgress size={28} />
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {t("audit.loading")}
                  </Typography>
                </TableCell>
              </TableRow>
            ) : sortedLogs.length > 0 ? (
              sortedLogs.map((log) => {
                const initial = log.user_full_name ? log.user_full_name.charAt(0).toUpperCase() : "S";
                return (
                  <TableRow key={log.id} hover sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
                    {/* Actor Details */}
                    {visibleColumns.includes("actor") && (
                      <TableCell>
                        <Box sx={{ display: "flex", alignItems: "center" }}>
                          <Avatar
                            sx={{
                              width: 36,
                              height: 36,
                              mr: 1.5,
                              fontSize: "0.95rem",
                              fontWeight: "bold",
                              bgcolor: "#8b5cf6",
                            }}
                          >
                            {initial}
                          </Avatar>
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: "bold", color: "text.primary" }}>
                              {log.user_full_name || "System"}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {log.user_email || "system@intranet.school"}
                            </Typography>
                          </Box>
                        </Box>
                      </TableCell>
                    )}

                    {/* Action Badge */}
                    {visibleColumns.includes("action") && <TableCell>{getActionBadge(log.action)}</TableCell>}

                    {/* Human Readable Details */}
                    {visibleColumns.includes("details") && (
                      <TableCell sx={{ fontWeight: "medium", color: "text.primary" }}>
                        {getReadableDetails(log)}
                      </TableCell>
                    )}

                    {/* IP Address */}
                    {visibleColumns.includes("ip") && (
                      <TableCell>
                        <Chip
                          label={log.ip_address || "127.0.0.1"}
                          size="small"
                          variant="outlined"
                          sx={{ borderRadius: "6px", fontFamily: "monospace" }}
                        />
                      </TableCell>
                    )}

                    {/* Formatted Date */}
                    {visibleColumns.includes("time") && (
                      <TableCell>
                        <Box sx={{ display: "flex", alignItems: "center", color: "text.secondary" }}>
                          <svg
                            width="16"
                            height="16"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth="2"
                            style={{ marginRight: "4px" }}
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                            />
                          </svg>
                          <Typography variant="body2" sx={{ fontSize: "0.85rem" }}>
                            {new Date(log.created_at).toLocaleString()}
                          </Typography>
                        </Box>
                      </TableCell>
                    )}
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell colSpan={visibleColumns.length || 1} align="center" sx={{ py: 10 }}>
                  <Typography variant="body2" color="text.secondary">
                    {t("audit.no-logs")}
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Pagination controls */}
      {total > limit && (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
          <Pagination
            count={Math.ceil(total / limit)}
            page={page}
            onChange={(_, val) => setPage(val)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
}
