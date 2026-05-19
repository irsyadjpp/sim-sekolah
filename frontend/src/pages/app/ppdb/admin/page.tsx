/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
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

export default function PPDBAdminPage() {
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
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/ppdb/admin/applicants`, {
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
        setError(json.message || "Gagal memuat daftar pendaftar.");
      }
    } catch (err) {
      setError("Kesalahan koneksi saat mengambil data pendaftar.");
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
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/ppdb/admin/applicants/${selectedApplicant.id}/verify`, {
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
        setVerifySuccessMsg(json.message || "Status verifikasi berhasil diperbarui.");

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
        setError(json.message || "Gagal memperbarui verifikasi.");
      }
    } catch (err) {
      setError("Terjadi kesalahan jaringan saat melakukan verifikasi.");
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
    switch (status) {
      case "Submitted":
        return <Chip label="Menunggu Verifikasi" color="warning" className="rounded-xl font-bold" />;
      case "Verified":
        return <Chip label="Terverifikasi" color="info" className="rounded-xl font-bold" />;
      case "Accepted":
        return <Chip label="Diterima" color="success" className="rounded-xl font-bold" />;
      case "Rejected":
        return <Chip label="Ditolak" color="error" className="rounded-xl font-bold" />;
      default:
        return <Chip label={status} color="default" className="rounded-xl font-bold" />;
    }
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
  } = useClientTable({ key: "ppdb_admin", data: filteredApplicants, defaultLimit: 10 });

  return (
    <Box className="pb-10">
      <Grid container spacing={2.5} className="mb-8 w-full">
        <Grid size={{ xs: 12 }}>
          <Typography variant="h1" component="h1" className="mb-0">
            Dasbor Operator PPDB Online
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
              Beranda
            </Link>
            <Typography variant="body2" className="text-text-secondary">
              Seleksi & Verifikasi PPDB
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
          <Tab label="Semua Pendaftar" className="font-bold" />
          <Tab label={`Menunggu Verifikasi (${stats.pending})`} className="font-bold" />
          <Tab label="Terverifikasi & Diterima" className="font-bold" />
          <Tab label="Ditolak" className="font-bold" />
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
                    Nama Calon Siswa
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700" sortDirection={sortBy === "nik" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "nik"}
                    direction={sortBy === "nik" ? sortDir : "asc"}
                    onClick={() => handleSort("nik")}
                  >
                    NIK
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700">Jalur Seleksi</TableCell>
                <TableCell className="font-black text-slate-700" sortDirection={sortBy === "status" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "status"}
                    direction={sortBy === "status" ? sortDir : "asc"}
                    onClick={() => handleSort("status")}
                  >
                    Status
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700">Aksi</TableCell>
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
                    <TableCell className="text-slate-600">{app.admission_path?.path_name}</TableCell>
                    <TableCell>{getStatusChip(app.status)}</TableCell>
                    <TableCell>
                      <Button
                        variant="outlined"
                        color="primary"
                        startIcon={<ViewIcon />}
                        onClick={() => handleOpenVerify(app)}
                        className="rounded-xl font-bold"
                      >
                        Detail & Verifikasi
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} className="py-10 text-center font-bold text-slate-400">
                    Tidak ada data pendaftar yang cocok dengan filter ini.
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
            labelRowsPerPage="Baris per halaman:"
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
        <DialogTitle className="text-2xl font-black text-slate-800">
          Detail Calon Siswa & Formulir Verifikasi
        </DialogTitle>
        <DialogContent dividers className="flex flex-col gap-6 border-slate-100 py-6">
          {selectedApplicant && (
            <Grid container spacing={3}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  Nama Lengkap
                </Typography>
                <Typography variant="body1" className="mb-4 font-black text-slate-800">
                  {selectedApplicant.full_name}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  NIK
                </Typography>
                <Typography variant="body1" className="mb-4 font-mono text-slate-800">
                  {selectedApplicant.nik}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  Tempat, Tanggal Lahir
                </Typography>
                <Typography variant="body1" className="mb-4 text-slate-800">
                  {selectedApplicant.birth_place}, {selectedApplicant.birth_date}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  Orang Tua (Ayah / Ibu)
                </Typography>
                <Typography variant="body1" className="mb-4 text-slate-800">
                  {selectedApplicant.parents?.father_name || "-"} / {selectedApplicant.parents?.mother_name || "-"}
                </Typography>

                <Typography variant="body2" className="mb-1 font-bold text-slate-400 uppercase">
                  Nomor HP / Kontak
                </Typography>
                <Typography variant="body1" className="font-bold text-slate-800">
                  {selectedApplicant.parents?.phone_number || "-"}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Typography variant="h6" className="text-primary mb-3 font-black">
                  Dokumen Pendukung
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
                            Uploaded
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
                          Lihat / Download
                        </Button>
                      </Paper>
                    ))}
                  </Box>
                ) : (
                  <Alert severity="info" className="rounded-xl">
                    Belum ada dokumen yang diunggah oleh pendaftar ini.
                  </Alert>
                )}

                <Divider className="my-6" />

                <Typography variant="h6" className="text-primary mb-4 font-black">
                  Keputusan Seleksi
                </Typography>

                {verifySuccessMsg && (
                  <Alert severity="success" className="mb-4 rounded-xl font-bold">
                    {verifySuccessMsg}
                  </Alert>
                )}

                <Box className="flex flex-col gap-4">
                  <FormControl fullWidth variant="outlined">
                    <InputLabel>Status Pendaftaran</InputLabel>
                    <Select
                      label="Status Pendaftaran"
                      value={verifyStatus}
                      onChange={(e) => setVerifyStatus(e.target.value)}
                    >
                      <MenuItem value="Verified">Terverifikasi (Verifikasi Berkas OK)</MenuItem>
                      <MenuItem value="Accepted">Diterima (Auto-Enroll ke database Siswa Aktif)</MenuItem>
                      <MenuItem value="Rejected">Ditolak</MenuItem>
                    </Select>
                  </FormControl>

                  {verifyStatus === "Accepted" && (
                    <Alert severity="warning" className="rounded-xl font-semibold">
                      Menerima pendaftar ini akan memicu transaksi di database untuk langsung membuat profil siswa aktif
                      (NIS baru, NISN, status aktif).
                    </Alert>
                  )}

                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Catatan Verifikator"
                    placeholder="Contoh: Berkas asli telah cocok, siap diproses lebih lanjut."
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
            Tutup
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmitVerification}
            className="rounded-xl px-6 font-black shadow-lg"
          >
            Simpan Keputusan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
