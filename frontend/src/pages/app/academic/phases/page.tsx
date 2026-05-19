import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import * as Yup from "yup";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  IconButton,
  InputAdornment,
  Snackbar,
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

import ToastEditor from "@/components/ToastEditor";
import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import { useConfirm } from "@/hooks/use-confirm";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

interface Phase {
  id: string;
  phase_code: string;
  phase_name: string;
  description: string;
}

export default function PhasesPage() {
  const confirm = useConfirm();
  const { t } = useTranslation();
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: "success" | "error" }>({
    open: false,
    message: "",
    severity: "success",
  });

  // Dialog state
  const [open, setOpen] = useState(false);
  const [editingPhase, setEditingPhase] = useState<Phase | null>(null);

  const fetchPhases = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/phases?limit=100&search=${search}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setPhases(json.data || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchPhases();
    }, 500);
    return () => clearTimeout(timer);
  }, [search]);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "phases", data: phases, defaultLimit: 10 });

  const formik = useFormik({
    initialValues: {
      phase_code: editingPhase?.phase_code || "",
      phase_name: editingPhase?.phase_name || "",
      description: editingPhase?.description || "",
    },
    enableReinitialize: true,
    validationSchema: Yup.object({
      phase_code: Yup.string().required("Kode wajib diisi"),
      phase_name: Yup.string().required("Nama wajib diisi"),
    }),
    onSubmit: async (values) => {
      const token = localStorage.getItem("accessToken");
      const url = editingPhase
        ? `${DEFAULTS.API_URL}/api/v1/phases/${editingPhase.id}`
        : `${DEFAULTS.API_URL}/api/v1/phases`;

      const method = editingPhase ? "PUT" : "POST";

      try {
        const res = await fetch(url, {
          method,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(values),
        });
        const json = await res.json();
        if (json.status === "success") {
          setOpen(false);
          const phaseData = json.data;

          if (editingPhase) {
            setPhases((prev) => prev.map((p) => (p.id === editingPhase.id ? phaseData : p)));
            setSnackbar({
              open: true,
              message: t("academic-phases.update-success", "Fase belajar berhasil diperbarui!"),
              severity: "success",
            });
          } else {
            setPhases((prev) => [phaseData, ...prev]);
            setSnackbar({
              open: true,
              message: t("academic-phases.create-success", "Fase belajar baru berhasil ditambahkan!"),
              severity: "success",
            });
          }
        } else {
          setSnackbar({
            open: true,
            message: json.message || t("academic-phases.error", "Gagal menyimpan data fase belajar"),
            severity: "error",
          });
        }
      } catch (err: any) {
        setSnackbar({
          open: true,
          message: err.message || t("academic-phases.error", "Gagal menyimpan data fase belajar"),
          severity: "error",
        });
      }
    },
  });

  const handleDelete = async (id: string) => {
    const isConfirmed = await confirm({
      title: t("academic-phases.delete-title", "Hapus Fase Belajar?"),
      message: t(
        "academic-phases.delete-confirm",
        "Yakin ingin menghapus fase ini? Menghapus fase akan berdampak pada data Kelas dan CP terkait.",
      ),
      confirmText: t("common.delete", "Hapus"),
      cancelText: t("common.cancel", "Batal"),
      variant: "danger",
    });

    if (!isConfirmed) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/phases/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        // Optimistic update: filter out from local state instantly
        setPhases((prev) => prev.filter((p) => p.id !== id));

        setSnackbar({
          open: true,
          message: t("academic-phases.delete-success", "Fase belajar berhasil dihapus!"),
          severity: "success",
        });
      } else {
        setSnackbar({
          open: true,
          message: json.message || t("academic-phases.delete-error", "Gagal menghapus fase belajar"),
          severity: "error",
        });
      }
    } catch (err: any) {
      setSnackbar({
        open: true,
        message: err.message || t("academic-phases.delete-error", "Gagal menghapus fase belajar"),
        severity: "error",
      });
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Master Fase Belajar
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => {
            setEditingPhase(null);
            setOpen(true);
          }}
        >
          Tambah Fase
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Fase</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="p-4">
          <TextField
            fullWidth
            placeholder="Cari kode atau nama fase..."
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
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold" sortDirection={sortBy === "phase_code" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "phase_code"}
                  direction={sortBy === "phase_code" ? sortDir : "asc"}
                  onClick={() => handleSort("phase_code")}
                >
                  Kode
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "phase_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "phase_name"}
                  direction={sortBy === "phase_name" ? sortDir : "asc"}
                  onClick={() => handleSort("phase_name")}
                >
                  Nama Fase
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold">Keterangan</TableCell>
              <TableCell className="font-bold" align="center">
                Aksi
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell className="text-primary font-medium">{p.phase_code}</TableCell>
                  <TableCell className="font-medium">{p.phase_name}</TableCell>
                  <TableCell>{p.description ? p.description.replace(/<[^>]*>/g, "") : ""}</TableCell>
                  <TableCell align="center">
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => {
                        setEditingPhase(p);
                        setOpen(true);
                      }}
                    >
                      <NiPen size="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDelete(p.id)}>
                      <NiBinEmpty size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Tidak ada data fase.
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

      {/* Dialog Form */}
      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <form onSubmit={formik.handleSubmit}>
          <DialogTitle>{editingPhase ? "Edit Fase Belajar" : "Tambah Fase Baru"}</DialogTitle>
          <DialogContent className="pt-2!">
            <Grid container spacing={3}>
              <Grid size={12}>
                <TextField
                  fullWidth
                  label="Kode Fase"
                  name="phase_code"
                  value={formik.values.phase_code}
                  onChange={formik.handleChange}
                  error={formik.touched.phase_code && Boolean(formik.errors.phase_code)}
                  helperText={formik.touched.phase_code && (formik.errors.phase_code as string)}
                  placeholder="Contoh: A, B, C"
                />
              </Grid>
              <Grid size={12}>
                <TextField
                  fullWidth
                  label="Nama Fase"
                  name="phase_name"
                  value={formik.values.phase_name}
                  onChange={formik.handleChange}
                  error={formik.touched.phase_name && Boolean(formik.errors.phase_name)}
                  helperText={formik.touched.phase_name && (formik.errors.phase_name as string)}
                  placeholder="Contoh: Fase A"
                />
              </Grid>
              <Grid size={12}>
                <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                  Keterangan
                </Typography>
                <ToastEditor
                  value={formik.values.description}
                  onChange={(val) => formik.setFieldValue("description", val)}
                  height="200px"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions className="p-4">
            <Button onClick={() => setOpen(false)}>Batal</Button>
            <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
              {editingPhase ? "Perbarui" : "Simpan"}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

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
          sx={{ borderRadius: 2, fontWeight: 500 }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
