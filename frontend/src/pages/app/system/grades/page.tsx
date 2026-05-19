/* eslint-disable @typescript-eslint/no-unused-vars */
import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as Yup from "yup";

import { Add as AddIcon, Class as ClassIcon, Delete as DeleteIcon, Edit as EditIcon } from "@mui/icons-material";
import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
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
import { useConfirm } from "@/hooks/use-confirm";

export default function GradesPage() {
  const confirm = useConfirm();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [grades, setGrades] = useState<any[]>([]);
  const [phases, setPhases] = useState<any[]>([]);

  // Dialog states
  const [openFormDialog, setOpenFormDialog] = useState(false);
  const [editingGrade, setEditingGrade] = useState<any | null>(null);

  const fetchGradesAndPhases = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const [gradeRes, phaseRes] = await Promise.all([
        fetch(`${DEFAULTS.API_URL}/api/v1/grades`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch(`${DEFAULTS.API_URL}/api/v1/phases`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      const gradeJson = await gradeRes.json();
      const phaseJson = await phaseRes.json();

      if (gradeJson.status === "success" && phaseJson.status === "success") {
        setGrades(gradeJson.data || []);
        setPhases(phaseJson.data || []);
      } else {
        setError("Gagal mengambil data tingkat kelas atau fase.");
      }
    } catch (err) {
      setError("Kesalahan koneksi saat menghubungi server.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGradesAndPhases();
  }, []);

  const formik = useFormik({
    initialValues: {
      grade_level: 1,
      grade_name: "",
      phase_id: "",
    },
    validationSchema: Yup.object({
      grade_level: Yup.number()
        .min(1, "Minimal tingkat 1")
        .max(12, "Maksimal tingkat 12")
        .required("Tingkat kelas wajib diisi"),
      grade_name: Yup.string().max(20, "Maksimal 20 karakter").required("Nama tingkat wajib diisi"),
      phase_id: Yup.string().uuid("ID Fase tidak valid").required("Fase wajib dipilih"),
    }),
    onSubmit: async (values) => {
      setError(null);
      setSuccess(null);
      const token = localStorage.getItem("accessToken");
      const url = editingGrade
        ? `${DEFAULTS.API_URL}/api/v1/grades/${editingGrade.id}`
        : `${DEFAULTS.API_URL}/api/v1/grades`;
      const method = editingGrade ? "PUT" : "POST";

      try {
        const res = await fetch(url, {
          method,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            grade_level: parseInt(values.grade_level.toString()),
            grade_name: values.grade_name,
            phase_id: values.phase_id,
          }),
        });
        const json = await res.json();
        if (json.status === "success") {
          setSuccess(editingGrade ? "Tingkat kelas berhasil diperbarui." : "Tingkat kelas baru berhasil dibuat.");
          setOpenFormDialog(false);
          setEditingGrade(null);
          formik.resetForm();
          fetchGradesAndPhases();
        } else {
          setError(json.message || "Gagal menyimpan data tingkat kelas.");
        }
      } catch (err) {
        setError("Kesalahan koneksi saat menyimpan data.");
      }
    },
  });

  const handleOpenCreate = () => {
    setEditingGrade(null);
    formik.resetForm();
    if (phases.length > 0) {
      formik.setFieldValue("phase_id", phases[0].id);
    }
    setOpenFormDialog(true);
  };

  const handleOpenEdit = (grade: any) => {
    setEditingGrade(grade);
    formik.setValues({
      grade_level: grade.grade_level,
      grade_name: grade.grade_name,
      phase_id: grade.phase_id,
    });
    setOpenFormDialog(true);
  };

  const handleDelete = async (id: string) => {
    const isConfirmed = await confirm({
      title: "Hapus Tingkat Kelas",
      message: "Apakah Anda yakin ingin menghapus tingkat kelas ini? Tindakan ini tidak dapat dibatalkan.",
      confirmText: "Hapus",
      cancelText: "Batal",
      variant: "danger",
    });
    if (!isConfirmed) return;
    setError(null);
    setSuccess(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/grades/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSuccess("Tingkat kelas berhasil dihapus.");
        fetchGradesAndPhases();
      } else {
        setError(json.message || "Gagal menghapus tingkat kelas.");
      }
    } catch (err) {
      setError("Kesalahan koneksi saat menghapus tingkat kelas.");
    }
  };

  const getPhaseName = (phaseId: string) => {
    const phase = phases.find((p) => p.id === phaseId);
    return phase ? phase.phase_name : "-";
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "grades", data: grades, defaultLimit: 10 });

  return (
    <Box className="pb-10">
      <Grid container spacing={2.5} className="mb-8 w-full">
        <Grid size={{ xs: 12 }} className="flex items-center justify-between">
          <Box>
            <Typography variant="h1" component="h1" className="mb-0">
              Master Tingkat Kelas
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
                Beranda
              </Link>
              <Typography variant="body2" className="text-text-secondary">
                Sistem
              </Typography>
              <Typography variant="body2" className="text-text-secondary">
                Tingkat Kelas
              </Typography>
            </Breadcrumbs>
          </Box>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={handleOpenCreate}
            className="rounded-2xl px-6 py-3 font-black shadow-xl"
          >
            Tingkat Kelas Baru
          </Button>
        </Grid>
      </Grid>

      {error && (
        <Alert severity="error" className="mb-6 rounded-2xl font-bold">
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" className="mb-6 rounded-2xl font-bold">
          {success}
        </Alert>
      )}

      <Card className="rounded-[40px] border-none bg-white p-6 shadow-2xl">
        <TableContainer component={Paper} className="overflow-hidden rounded-2xl border-none shadow-none">
          <Table>
            <TableHead className="bg-slate-50">
              <TableRow>
                <TableCell
                  className="font-black text-slate-700"
                  sortDirection={sortBy === "grade_level" ? sortDir : false}
                >
                  <TableSortLabel
                    active={sortBy === "grade_level"}
                    direction={sortBy === "grade_level" ? sortDir : "asc"}
                    onClick={() => handleSort("grade_level")}
                  >
                    Tingkat (Numeric)
                  </TableSortLabel>
                </TableCell>
                <TableCell
                  className="font-black text-slate-700"
                  sortDirection={sortBy === "grade_name" ? sortDir : false}
                >
                  <TableSortLabel
                    active={sortBy === "grade_name"}
                    direction={sortBy === "grade_name" ? sortDir : "asc"}
                    onClick={() => handleSort("grade_name")}
                  >
                    Nama Kelas
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700">Fase Kurikulum</TableCell>
                <TableCell className="font-black text-slate-700">Aksi</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedData.length > 0 ? (
                paginatedData.map((grade) => (
                  <TableRow key={grade.id} hover className="border-b border-slate-50 last:border-0">
                    <TableCell className="flex items-center gap-2 font-bold text-slate-800">
                      <ClassIcon className="text-slate-400" />
                      Tingkat {grade.grade_level}
                    </TableCell>
                    <TableCell className="font-bold text-slate-600">{grade.grade_name}</TableCell>
                    <TableCell className="text-slate-600">
                      <Chip
                        label={getPhaseName(grade.phase_id)}
                        color="primary"
                        variant="outlined"
                        className="rounded-xl font-bold"
                      />
                    </TableCell>
                    <TableCell>
                      <Box className="flex gap-2">
                        <Button
                          variant="outlined"
                          color="primary"
                          startIcon={<EditIcon />}
                          onClick={() => handleOpenEdit(grade)}
                          className="rounded-xl font-bold"
                        >
                          Edit
                        </Button>
                        <Button
                          variant="outlined"
                          color="error"
                          startIcon={<DeleteIcon />}
                          onClick={() => handleDelete(grade.id)}
                          className="rounded-xl font-bold"
                        >
                          Hapus
                        </Button>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} className="py-10 text-center font-bold text-slate-400">
                    Tidak ada data tingkat kelas. Silakan tambahkan baru.
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
      </Card>

      {/* Form Dialog */}
      <Dialog
        open={openFormDialog}
        onClose={() => setOpenFormDialog(false)}
        maxWidth="xs"
        fullWidth
        classes={{ paper: "rounded-[32px] p-6" }}
      >
        <DialogTitle className="text-2xl font-black text-slate-800">
          {editingGrade ? "Edit Tingkat Kelas" : "Tingkat Kelas Baru"}
        </DialogTitle>
        <DialogContent className="flex flex-col gap-6 border-slate-100 py-6">
          <Box className="mt-2 flex flex-col gap-4">
            <TextField
              fullWidth
              type="number"
              label="Tingkat (Numerik)"
              placeholder="Contoh: 1"
              name="grade_level"
              value={formik.values.grade_level}
              onChange={formik.handleChange}
              error={formik.touched.grade_level && Boolean(formik.errors.grade_level)}
              helperText={formik.touched.grade_level && formik.errors.grade_level}
            />

            <TextField
              fullWidth
              label="Nama Tingkat Kelas"
              placeholder="Contoh: Kelas I"
              name="grade_name"
              value={formik.values.grade_name}
              onChange={formik.handleChange}
              error={formik.touched.grade_name && Boolean(formik.errors.grade_name)}
              helperText={formik.touched.grade_name && formik.errors.grade_name}
            />

            <FormControl fullWidth variant="outlined">
              <InputLabel>Fase Kurikulum</InputLabel>
              <Select
                label="Fase Kurikulum"
                name="phase_id"
                value={formik.values.phase_id}
                onChange={formik.handleChange}
                error={formik.touched.phase_id && Boolean(formik.errors.phase_id)}
              >
                {phases.map((phase) => (
                  <MenuItem key={phase.id} value={phase.id}>
                    {phase.phase_name} ({phase.description})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions className="gap-2">
          <Button
            variant="outlined"
            color="inherit"
            onClick={() => setOpenFormDialog(false)}
            className="rounded-xl font-bold"
          >
            Tutup
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => formik.handleSubmit()}
            className="rounded-xl px-6 font-black shadow-lg"
          >
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
