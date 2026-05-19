/* eslint-disable @typescript-eslint/no-unused-vars */
import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as Yup from "yup";

import {
  Add as AddIcon,
  CalendarToday as CalendarIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  ToggleOff as InactiveIcon,
  ToggleOn as ActiveIcon,
} from "@mui/icons-material";
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

import { useClientTable } from "@/hooks/use-client-table";
import { useConfirm } from "@/hooks/use-confirm";
import { apiClient } from "@/lib/api-client";

export default function AcademicYearsPage() {
  const confirm = useConfirm();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [academicYears, setAcademicYears] = useState<any[]>([]);

  // Dialog states
  const [openFormDialog, setOpenFormDialog] = useState(false);
  const [editingYear, setEditingYear] = useState<any | null>(null);

  const fetchAcademicYears = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.get("/api/v1/academic-years");
      const json = res.data;
      if (json.status === "success") {
        setAcademicYears(json.data || []);
      } else {
        setError(json.message || "Gagal mengambil data tahun ajaran.");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Kesalahan koneksi saat menghubungi server.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAcademicYears();
  }, []);

  const formik = useFormik({
    initialValues: {
      year_name: "",
      semester: "Ganjil",
    },
    validationSchema: Yup.object({
      year_name: Yup.string().required("Nama tahun ajaran wajib diisi").max(20, "Maksimal 20 karakter"),
      semester: Yup.string().oneOf(["Ganjil", "Genap"]).required("Semester wajib dipilih"),
    }),
    onSubmit: async (values) => {
      setError(null);
      setSuccess(null);
      const url = editingYear ? `/api/v1/academic-years/${editingYear.id}` : `/api/v1/academic-years`;

      try {
        const res = editingYear ? await apiClient.put(url, values) : await apiClient.post(url, values);

        const json = res.data;
        if (json.status === "success") {
          setSuccess(editingYear ? "Tahun ajaran berhasil diperbarui." : "Tahun ajaran baru berhasil dibuat.");
          setOpenFormDialog(false);
          setEditingYear(null);
          formik.resetForm();
          fetchAcademicYears();
        } else {
          setError(json.message || "Gagal menyimpan data tahun ajaran.");
        }
      } catch (err: any) {
        setError(err.response?.data?.message || "Kesalahan koneksi saat menyimpan data.");
      }
    },
  });

  const handleOpenCreate = () => {
    setEditingYear(null);
    formik.resetForm();
    setOpenFormDialog(true);
  };

  const handleOpenEdit = (year: any) => {
    setEditingYear(year);
    formik.setValues({
      year_name: year.year_name,
      semester: year.semester,
    });
    setOpenFormDialog(true);
  };

  const handleActivate = async (id: string) => {
    setError(null);
    setSuccess(null);
    try {
      const res = await apiClient.patch(`/api/v1/academic-years/${id}/activate`);
      const json = res.data;
      if (json.status === "success") {
        setSuccess("Tahun ajaran aktif berhasil diperbarui.");
        fetchAcademicYears();
      } else {
        setError(json.message || "Gagal mengaktifkan tahun ajaran.");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Kesalahan koneksi saat mengaktifkan tahun ajaran.");
    }
  };

  const handleDelete = async (id: string) => {
    const isConfirmed = await confirm({
      title: "Hapus Tahun Ajaran",
      message: "Apakah Anda yakin ingin menghapus tahun ajaran ini? Tindakan ini tidak dapat dibatalkan.",
      confirmText: "Hapus",
      cancelText: "Batal",
      variant: "danger",
    });
    if (!isConfirmed) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await apiClient.delete(`/api/v1/academic-years/${id}`);
      const json = res.data;
      if (json.status === "success") {
        setSuccess("Tahun ajaran berhasil dihapus.");
        fetchAcademicYears();
      } else {
        setError(json.message || "Gagal menghapus tahun ajaran.");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Kesalahan koneksi saat menghapus tahun ajaran.");
    }
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "academic_years", data: academicYears, defaultLimit: 10 });

  return (
    <Box className="pb-10">
      <Grid container spacing={2.5} className="mb-8 w-full">
        <Grid size={{ xs: 12 }} className="flex items-center justify-between">
          <Box>
            <Typography variant="h1" component="h1" className="mb-0">
              Siklus Tahun Ajaran
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
                Beranda
              </Link>
              <Typography variant="body2" className="text-text-secondary">
                Sistem
              </Typography>
              <Typography variant="body2" className="text-text-secondary">
                Tahun Ajaran
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
            Tahun Ajaran Baru
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
                  sortDirection={sortBy === "year_name" ? sortDir : false}
                >
                  <TableSortLabel
                    active={sortBy === "year_name"}
                    direction={sortBy === "year_name" ? sortDir : "asc"}
                    onClick={() => handleSort("year_name")}
                  >
                    Tahun Ajaran
                  </TableSortLabel>
                </TableCell>
                <TableCell
                  className="font-black text-slate-700"
                  sortDirection={sortBy === "semester" ? sortDir : false}
                >
                  <TableSortLabel
                    active={sortBy === "semester"}
                    direction={sortBy === "semester" ? sortDir : "asc"}
                    onClick={() => handleSort("semester")}
                  >
                    Semester
                  </TableSortLabel>
                </TableCell>
                <TableCell
                  className="font-black text-slate-700"
                  sortDirection={sortBy === "is_active" ? sortDir : false}
                >
                  <TableSortLabel
                    active={sortBy === "is_active"}
                    direction={sortBy === "is_active" ? sortDir : "asc"}
                    onClick={() => handleSort("is_active")}
                  >
                    Status Aktif
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-black text-slate-700">Aksi</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedData.length > 0 ? (
                paginatedData.map((year) => (
                  <TableRow key={year.id} hover className="border-b border-slate-50 last:border-0">
                    <TableCell className="flex items-center gap-2 font-bold text-slate-800">
                      <CalendarIcon className="text-slate-400" />
                      {year.year_name}
                    </TableCell>
                    <TableCell className="font-bold text-slate-600">{year.semester}</TableCell>
                    <TableCell>
                      {year.is_active ? (
                        <Chip label="Aktif" color="success" icon={<ActiveIcon />} className="rounded-xl font-bold" />
                      ) : (
                        <Chip
                          label="Tidak Aktif"
                          color="default"
                          icon={<InactiveIcon />}
                          className="rounded-xl font-bold"
                        />
                      )}
                    </TableCell>
                    <TableCell>
                      <Box className="flex gap-2">
                        {!year.is_active && (
                          <Button
                            variant="outlined"
                            color="success"
                            onClick={() => handleActivate(year.id)}
                            className="rounded-xl font-bold"
                          >
                            Aktifkan
                          </Button>
                        )}
                        <Button
                          variant="outlined"
                          color="primary"
                          startIcon={<EditIcon />}
                          onClick={() => handleOpenEdit(year)}
                          className="rounded-xl font-bold"
                        >
                          Edit
                        </Button>
                        <Button
                          variant="outlined"
                          color="error"
                          startIcon={<DeleteIcon />}
                          onClick={() => handleDelete(year.id)}
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
                    Tidak ada data tahun ajaran. Silakan tambahkan baru.
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
          {editingYear ? "Edit Tahun Ajaran" : "Tahun Ajaran Baru"}
        </DialogTitle>
        <DialogContent className="flex flex-col gap-6 border-slate-100 py-6">
          <Box className="mt-2 flex flex-col gap-4">
            <TextField
              fullWidth
              label="Nama Tahun Ajaran"
              placeholder="Contoh: 2025/2026"
              name="year_name"
              value={formik.values.year_name}
              onChange={formik.handleChange}
              error={formik.touched.year_name && Boolean(formik.errors.year_name)}
              helperText={formik.touched.year_name && formik.errors.year_name}
            />

            <FormControl fullWidth variant="outlined">
              <InputLabel>Semester</InputLabel>
              <Select label="Semester" name="semester" value={formik.values.semester} onChange={formik.handleChange}>
                <MenuItem value="Ganjil">Ganjil</MenuItem>
                <MenuItem value="Genap">Genap</MenuItem>
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
