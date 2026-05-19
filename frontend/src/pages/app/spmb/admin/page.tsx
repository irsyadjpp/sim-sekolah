/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  AssignmentTurnedIn as VerifyIcon,
  Cancel as RejectIcon,
  CheckCircle as SuccessIcon,
  CloudDownload as DownloadIcon,
  HourglassEmpty as PendingIcon,
  Info as InfoIcon,
  People as PeopleIcon,
  Visibility as ViewIcon,
} from "@mui/icons-material";
import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Skeleton,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import { spmbStatusLabel } from "@/i18n/spmb-status";

export default function SPMBAdminPage() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [applicants, setApplicants] = useState<any[]>([]);
  const [selectedApplicant, setSelectedApplicant] = useState<any | null>(null);

  // Verification dialog state
  const [openVerifyDialog, setOpenVerifyDialog] = useState(false);
  const [verifyStatus, setVerifyStatus] = useState("Verified");
  const [verifyNotes, setVerifyNotes] = useState("");
  const [verifySuccessMsg, setVerifySuccessMsg] = useState<string | null>(null);

  // Statistics
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    verified: 0,
    accepted: 0,
    rejected: 0,
  });

  const fetchApplicants = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/admin/applicants`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        const list = json.data || [];
        setApplicants(list);

        // Compute statistics
        const total = list.length;
        const pending = list.filter((a: any) => a.status === "Submitted").length;
        const verified = list.filter((a: any) => a.status === "Verified").length;
        const accepted = list.filter((a: any) => a.status === "Accepted").length;
        const rejected = list.filter((a: any) => a.status === "Rejected").length;
        setStats({ total, pending, verified, accepted, rejected });
      } else {
        setError(json.message || t("spmb.admin.load-error"));
      }
    } catch (err) {
      setError(t("spmb.admin.connection-error"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplicants();
  }, []);

  const handleOpenVerify = (applicant: any) => {
    setSelectedApplicant(applicant);
    setVerifyStatus(applicant.status === "Submitted" ? "Verified" : applicant.status);
    setVerifyNotes("");
    setVerifySuccessMsg(null);
    setOpenVerifyDialog(true);
  };

  const handleSubmitVerification = async () => {
    if (!selectedApplicant) return;
    setError(null);
    setVerifySuccessMsg(null);

    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/admin/applicants/${selectedApplicant.id}/verify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: verifyStatus,
          notes: verifyNotes,
        }),
      });

      const json = await res.json();
      if (json.status === "success") {
        setVerifySuccessMsg(json.message || t("spmb.admin.verify-success"));

        // Optimistic UI update
        setApplicants((prev) =>
          prev.map((app) => (app.id === selectedApplicant.id ? { ...app, status: verifyStatus } : app)),
        );

        // Update stats optimistically
        setStats((prev) => {
          const oldStatus = selectedApplicant.status.toLowerCase();
          const newStatus = verifyStatus.toLowerCase();
          return {
            ...prev,
            [oldStatus === "submitted" ? "pending" : oldStatus]: Math.max(
              0,
              prev[oldStatus === "submitted" ? "pending" : (oldStatus as keyof typeof prev)] - 1,
            ),
            [newStatus === "submitted" ? "pending" : newStatus]:
              prev[newStatus === "submitted" ? "pending" : (newStatus as keyof typeof prev)] + 1,
          };
        });

        setTimeout(() => {
          setOpenVerifyDialog(false);
          setSelectedApplicant(null);
        }, 2000);
      } else {
        setError(json.message || t("spmb.admin.verify-error"));
      }
    } catch (err) {
      setError(t("spmb.admin.network-error-verify"));
    }
  };

  const filteredApplicants = applicants.filter((a: any) => {
    if (activeTab === 0) return true; // Semua
    if (activeTab === 1) return a.status === "Submitted"; // Menunggu
    if (activeTab === 2) return a.status === "Verified" || a.status === "Accepted"; // Terverifikasi / Diterima
    if (activeTab === 3) return a.status === "Rejected"; // Ditolak
    return true;
  });

  const getStatusChip = (status: string) => {
    const label = spmbStatusLabel(status);
    const color =
      status === "Submitted"
        ? "warning"
        : status === "Verified"
          ? "info"
          : status === "Accepted"
            ? "success"
            : status === "Rejected"
              ? "error"
              : "default";
    return <Chip label={label} color={color} className="rounded-xl font-bold" />;
  };

  const {
    paginatedData,
    page: tablePage,
    limit,
    total,
    sortBy,
    sortDir,
    handlePageChange,
    handleLimitChange,
    handleSort,
  } = useClientTable({ key: "spmb_admin", data: filteredApplicants, defaultLimit: 10 });

  return (
    <Box className="pb-10">
      <Grid container spacing={2.5} className="mb-8 w-full">
        <Grid size={{ xs: 12 }}>
          <Typography variant="h1" component="h1" className="mb-0">
            Dasbor Operator SPMB Online
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
              Beranda
            </Link>
            <Typography variant="body2" className="text-text-secondary">
              Seleksi & Verifikasi SPMB
            </Typography>
          </Breadcrumbs>
        </Grid>
      </Grid>

      <Grid container spacing={4} className="mb-8">
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="rounded-3xl border border-slate-100 bg-white p-4 shadow-sm">
            <Box className="flex items-center gap-4">
              <Box className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-blue-500">
                <PeopleIcon />
              </Box>
              <Box>
                <Typography variant="caption" className="font-bold text-slate-400 uppercase">
                  Total Pendaftar
                </Typography>
                <Typography variant="h4" className="font-black text-slate-800">
                  {stats.total}
                </Typography>
              </Box>
            </Box>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="rounded-3xl border border-slate-100 bg-white p-4 shadow-sm">
            <Box className="flex items-center gap-4">
              <Box className="flex h-12 w-12 animate-pulse items-center justify-center rounded-2xl bg-amber-50 text-amber-500">
                <PendingIcon />
              </Box>
              <Box>
                <Typography variant="caption" className="font-bold text-slate-400 uppercase">
                  Menunggu Verifikasi
                </Typography>
                <Typography variant="h4" className="font-black text-slate-800">
                  {stats.pending}
                </Typography>
              </Box>
            </Box>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="rounded-3xl border border-slate-100 bg-white p-4 shadow-sm">
            <Box className="flex items-center gap-4">
              <Box className="flex h-12 w-12 items-center justify-center rounded-2xl bg-green-50 text-green-500">
                <SuccessIcon />
              </Box>
              <Box>
                <Typography variant="caption" className="font-bold text-slate-400 uppercase">
                  Diterima
                </Typography>
                <Typography variant="h4" className="font-black text-slate-800">
                  {stats.accepted}
                </Typography>
              </Box>
            </Box>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="rounded-3xl border border-slate-100 bg-white p-4 shadow-sm">
            <Box className="flex items-center gap-4">
              <Box className="flex h-12 w-12 items-center justify-center rounded-2xl bg-red-50 text-red-500">
                <RejectIcon />
              </Box>
              <Box>
                <Typography variant="caption" className="font-bold text-slate-400 uppercase">
                  Ditolak
                </Typography>
                <Typography variant="h4" className="font-black text-slate-800">
                  {stats.rejected}
                </Typography>
              </Box>
            </Box>
          </Card>
        </Grid>
      </Grid>

      {error && (
        <Alert severity="error" className="mb-6 rounded-2xl font-bold">
          {error}
        </Alert>
      )}

      <Card className="rounded-[40px] border-none bg-white p-6 shadow-2xl">
        <Tabs
          value={activeTab}
          onChange={(_, val) => setActiveTab(val)}
          className="mb-6 border-b border-slate-100"
          textColor="primary"
          indicatorColor="primary"
        >
          <Tab label={t("spmb.admin.tab-all")} className="font-bold" />
          <Tab label={t("spmb.admin.tab-pending", { count: stats.pending })} className="font-bold" />
          <Tab label={t("spmb.admin.tab-verified")} className="font-bold" />
          <Tab label={t("spmb.admin.tab-rejected")} className="font-bold" />
        </Tabs>

        <TableContainer component={Paper} className="overflow-hidden rounded-2xl border-none shadow-none">
          <Table>
            <TableHead className="bg-slate-50">
              <TableRow>
                <TableCell
                  className="font-black text-slate-700"
                  sortDirection={sortBy === "full_name" ? sortDir : false}
                >
                  <TableSortLabel
                    active={sortBy === "full_name"}
                    direction={sortBy === "full_name" ? sortDir : "asc"}
                    onClick={() => handleSort("full_name")}
                  >
                    {t("spmb.admin.col-student-name")}
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700" sortDirection={sortBy === "nik" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "nik"}
                    direction={sortBy === "nik" ? sortDir : "asc"}
                    onClick={() => handleSort("nik")}
                  >
                    {t("spmb.admin.col-nik")}
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700">{t("spmb.admin.col-path")}</TableCell>
                <TableCell className="font-black text-slate-700" sortDirection={sortBy === "status" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "status"}
                    direction={sortBy === "status" ? sortDir : "asc"}
                    onClick={() => handleSort("status")}
                  >
                    {t("spmb.admin.col-status")}
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700">{t("spmb.admin.col-actions")}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                Array.from(new Array(5)).map((_, idx) => (
                  <TableRow key={idx}>
                    <TableCell>
                      <Skeleton width="80%" height={24} />
                    </TableCell>
                    <TableCell>
                      <Skeleton width="60%" height={24} />
                    </TableCell>
                    <TableCell>
                      <Skeleton width="50%" height={24} />
                    </TableCell>
                    <TableCell>
                      <Skeleton width={100} height={32} className="rounded-xl" />
                    </TableCell>
                    <TableCell>
                      <Skeleton width={120} height={40} className="rounded-xl" />
                    </TableCell>
                  </TableRow>
                ))
              ) : paginatedData.length > 0 ? (
                paginatedData.map((app) => (
                  <TableRow key={app.id} hover className="border-b border-slate-50 last:border-0">
                    <TableCell className="font-bold text-slate-800">{app.full_name}</TableCell>
                    <TableCell className="font-mono text-slate-600">{app.nik}</TableCell>
                    <TableCell className="text-slate-600">{app.admission_path?.name}</TableCell>
                    <TableCell>{getStatusChip(app.status)}</TableCell>
                    <TableCell>
                      <Button
                        variant="outlined"
                        color="primary"
                        startIcon={<ViewIcon />}
                        onClick={() => handleOpenVerify(app)}
                        className="rounded-xl font-bold"
                      >
                        {t("spmb.admin.detail-verify-btn")}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} className="py-10 text-center font-bold text-slate-400">
                    {t("spmb.admin.empty-filter")}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
          <TablePagination
            component="div"
            count={total}
            page={tablePage - 1}
            onPageChange={(_, newPage) => handlePageChange(newPage + 1)}
            rowsPerPage={limit}
            onRowsPerPageChange={(e) => handleLimitChange(parseInt(e.target.value, 10))}
            labelRowsPerPage={t("common-ui.rows-per-page")}
          />
        </TableContainer>
      </Card>

      {/* Verification & Detail Dialog */}
      <Dialog
        open={openVerifyDialog}
        onClose={() => setOpenVerifyDialog(false)}
        maxWidth="md"
        fullWidth
        classes={{ paper: "rounded-[32px] p-6" }}
      >
        <DialogTitle className="text-2xl font-black text-slate-800">{t("spmb.admin.dialog-title")}</DialogTitle>
        <DialogContent dividers className="flex flex-col gap-6 border-slate-100 py-6">
          {selectedApplicant && (
            <Grid container spacing={3}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  {t("spmb.admin.label-full-name")}
                </Typography>
                <Typography variant="body1" className="mb-4 font-black text-slate-800">
                  {selectedApplicant.full_name}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  {t("spmb.admin.col-nik")}
                </Typography>
                <Typography variant="body1" className="mb-4 font-mono text-slate-800">
                  {selectedApplicant.nik}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  {t("spmb.admin.label-birth")}
                </Typography>
                <Typography variant="body1" className="mb-4 text-slate-800">
                  {selectedApplicant.birth_place}, {selectedApplicant.birth_date}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  {t("spmb.admin.label-parents")}
                </Typography>
                <Typography variant="body1" className="mb-4 text-slate-800">
                  {selectedApplicant.parent?.father_name || "-"} / {selectedApplicant.parent?.mother_name || "-"}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  {t("spmb.admin.label-phone")}
                </Typography>
                <Typography variant="body1" className="font-bold text-slate-800">
                  {selectedApplicant.parent?.phone_number || "-"}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Typography variant="h6" className="text-primary mb-3 font-black">
                  {t("spmb.admin.documents-title")}
                </Typography>
                {selectedApplicant.documents && selectedApplicant.documents.length > 0 ? (
                  <Box className="flex flex-col gap-2">
                    {selectedApplicant.documents.map((doc: any) => (
                      <Paper
                        key={doc.id}
                        className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/50 p-3"
                      >
                        <Box>
                          <Typography variant="body2" className="font-bold text-slate-800">
                            {doc.document_type}
                          </Typography>
                          <Typography variant="caption" className="font-mono text-slate-400">
                            {t("spmb.admin.uploaded-caption")}
                          </Typography>
                        </Box>
                        <Button
                          variant="text"
                          color="primary"
                          href={`${DEFAULTS.API_URL}${doc.file_path}`}
                          target="_blank"
                          startIcon={<DownloadIcon />}
                          className="font-bold"
                        >
                          {t("spmb.admin.view-download")}
                        </Button>
                      </Paper>
                    ))}
                  </Box>
                ) : (
                  <Alert severity="info" className="rounded-xl">
                    {t("spmb.admin.no-documents")}
                  </Alert>
                )}

                <Divider className="my-6" />

                <Typography variant="h6" className="text-primary mb-4 font-black">
                  {t("spmb.admin.decision-title")}
                </Typography>

                {verifySuccessMsg && (
                  <Alert severity="success" className="mb-4 rounded-xl font-bold">
                    {verifySuccessMsg}
                  </Alert>
                )}

                <Box className="flex flex-col gap-4">
                  <FormControl fullWidth variant="outlined">
                    <InputLabel>{t("spmb.admin.registration-status")}</InputLabel>
                    <Select
                      label={t("spmb.admin.registration-status")}
                      value={verifyStatus}
                      onChange={(e) => setVerifyStatus(e.target.value)}
                    >
                      <MenuItem value="Verified">{t("spmb.admin.menu-verified")}</MenuItem>
                      <MenuItem value="Accepted">{t("spmb.admin.menu-accepted")}</MenuItem>
                      <MenuItem value="Rejected">{t("spmb.admin.menu-rejected")}</MenuItem>
                    </Select>
                  </FormControl>

                  {verifyStatus === "Accepted" && (
                    <Alert severity="warning" className="rounded-xl font-semibold">
                      {t("spmb.admin.accepted-warning")}
                    </Alert>
                  )}

                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label={t("spmb.admin.verifier-notes")}
                    placeholder={t("spmb.admin.verifier-notes-placeholder")}
                    value={verifyNotes}
                    onChange={(e) => setVerifyNotes(e.target.value)}
                  />
                </Box>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions className="gap-2">
          <Button
            variant="outlined"
            color="inherit"
            onClick={() => setOpenVerifyDialog(false)}
            className="rounded-xl font-bold"
          >
            {t("spmb.admin.close-btn")}
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmitVerification}
            className="rounded-xl px-6 font-black shadow-lg"
          >
            {t("spmb.admin.save-decision-btn")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
