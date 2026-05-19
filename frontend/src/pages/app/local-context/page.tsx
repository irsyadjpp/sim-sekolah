import { useFormik } from "formik";
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as Yup from "yup";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  Grid,
  IconButton,
  InputAdornment,
  InputLabel,
  MenuItem,
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
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

interface Category {
  id: string;
  category_code: string;
  category_name: string;
}

interface LocalContext {
  id: string;
  category_id: string;
  title: string;
  description: string;
  location: string;
  scope_type: string;
  is_active: boolean;
  category?: Category;
}

export default function LocalContextPage() {
  const [contexts, setContexts] = useState<LocalContext[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("");

  // Dialog state
  const [open, setOpen] = useState(false);
  const [editingContext, setEditingContext] = useState<LocalContext | null>(null);
  const confirm = useConfirm();

  const fetchData = useCallback(async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      // Fetch Categories first
      const catRes = await fetch(`${DEFAULTS.API_URL}/api/v1/local-contexts/categories`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const catJson = await catRes.json();
      if (catJson.status === "success") setCategories(catJson.data || []);

      // Fetch Contexts
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/local-contexts?limit=10000&search=${search}&category_id=${filterCategory}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        setContexts(json.data || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [search, filterCategory]);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchData();
    }, 500);
    return () => clearTimeout(timer);
  }, [fetchData]);

  const formik = useFormik({
    initialValues: {
      category_id: editingContext?.category_id || "",
      title: editingContext?.title || "",
      description: editingContext?.description || "",
      location: editingContext?.location || "",
      scope_type: editingContext?.scope_type || "SCHOOL",
      is_active: editingContext?.is_active ?? true,
    },
    enableReinitialize: true,
    validationSchema: Yup.object({
      category_id: Yup.string().required("Kategori wajib dipilih"),
      title: Yup.string().required("Judul wajib diisi"),
      scope_type: Yup.string().required("Scope wajib dipilih"),
    }),
    onSubmit: async (values) => {
      const token = localStorage.getItem("accessToken");
      const url = editingContext
        ? `${DEFAULTS.API_URL}/api/v1/local-contexts/${editingContext.id}`
        : `${DEFAULTS.API_URL}/api/v1/local-contexts`;

      const method = editingContext ? "PUT" : "POST";

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
          fetchData();
        } else {
          alert(json.message);
        }
      } catch (err: any) {
        alert(err.message);
      }
    },
  });

  const handleDelete = async (id: string) => {
    const ok = await confirm({
      title: "Hapus Konteks Lokal",
      message: "Yakin ingin menghapus konteks ini?",
      confirmText: "Hapus",
      cancelText: "Batal",
    });
    if (!ok) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/local-contexts/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchData();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "local_contexts", data: contexts, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Konteks Lokal Sekolah
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => {
            setEditingContext(null);
            setOpen(true);
          }}
        >
          Tambah Konteks
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/local-context">Konteks Lokal</Link>
        <Typography variant="body2">Kelola</Typography>
      </Breadcrumbs>

      <Card className="mb-6 overflow-visible">
        <CardContent className="p-4">
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, md: 8 }}>
              <TextField
                fullWidth
                placeholder="Cari judul atau deskripsi konteks..."
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
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Filter Kategori</InputLabel>
                <Select
                  label="Filter Kategori"
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                >
                  <MenuItem value="">Semua Kategori</MenuItem>
                  {categories.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.category_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
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
              <TableCell className="font-bold">Kategori</TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "title" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "title"}
                  direction={sortBy === "title" ? sortDir : "asc"}
                  onClick={() => handleSort("title")}
                >
                  Judul Konteks
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "scope_type" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "scope_type"}
                  direction={sortBy === "scope_type" ? sortDir : "asc"}
                  onClick={() => handleSort("scope_type")}
                >
                  Scope
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "is_active" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "is_active"}
                  direction={sortBy === "is_active" ? sortDir : "asc"}
                  onClick={() => handleSort("is_active")}
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
              paginatedData.map((c) => (
                <TableRow key={c.id} hover>
                  <TableCell>
                    <Chip label={c.category?.category_name} size="small" variant="outlined" color="primary" />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" className="font-bold">
                      {c.title}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" className="line-clamp-1">
                      {c.description}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={c.scope_type} size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={c.is_active ? "Aktif" : "Non-aktif"}
                      color={c.is_active ? "success" : "default"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => {
                        setEditingContext(c);
                        setOpen(true);
                      }}
                    >
                      <NiPen size="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDelete(c.id)}>
                      <NiBinEmpty size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  Belum ada data konteks lokal.
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
      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="md">
        <form onSubmit={formik.handleSubmit}>
          <DialogTitle>{editingContext ? "Edit Konteks Lokal" : "Tambah Konteks Lokal Baru"}</DialogTitle>
          <DialogContent className="pt-2!">
            <Grid container spacing={3}>
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth error={formik.touched.category_id && Boolean(formik.errors.category_id)}>
                  <InputLabel>Kategori Konteks</InputLabel>
                  <Select
                    label="Kategori Konteks"
                    name="category_id"
                    value={formik.values.category_id}
                    onChange={formik.handleChange}
                  >
                    {categories.map((c) => (
                      <MenuItem key={c.id} value={c.id}>
                        {c.category_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Scope</InputLabel>
                  <Select
                    label="Scope"
                    name="scope_type"
                    value={formik.values.scope_type}
                    onChange={formik.handleChange}
                  >
                    <MenuItem value="SCHOOL">SCHOOL (Tingkat Sekolah)</MenuItem>
                    <MenuItem value="VILLAGE">VILLAGE (Tingkat Desa/Lingkungan)</MenuItem>
                    <MenuItem value="CLASS">CLASS (Tingkat Kelas)</MenuItem>
                    <MenuItem value="STUDENT">STUDENT (Spesifik Siswa)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12 }}>
                <TextField
                  fullWidth
                  label="Judul Konteks"
                  name="title"
                  value={formik.values.title}
                  onChange={formik.handleChange}
                  error={formik.touched.title && Boolean(formik.errors.title)}
                  helperText={formik.touched.title && (formik.errors.title as string)}
                  placeholder="Contoh: Lingkungan Pesisir Pantai Bonerate"
                />
              </Grid>
              <Grid size={{ xs: 12 }}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Deskripsi Detail"
                  name="description"
                  value={formik.values.description}
                  onChange={formik.handleChange}
                  placeholder="Jelaskan secara mendalam tentang konteks ini..."
                />
              </Grid>
              <Grid size={{ xs: 12, md: 8 }}>
                <TextField
                  fullWidth
                  label="Lokasi Spesifik (Opsional)"
                  name="location"
                  value={formik.values.location}
                  onChange={formik.handleChange}
                />
              </Grid>
              <Grid size={{ xs: 12, md: 4 }}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    label="Status"
                    name="is_active"
                    value={formik.values.is_active}
                    onChange={formik.handleChange}
                  >
                    <MenuItem value={true as any}>Aktif</MenuItem>
                    <MenuItem value={false as any}>Non-aktif</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions className="p-4">
            <Button onClick={() => setOpen(false)}>Batal</Button>
            <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
              {editingContext ? "Perbarui" : "Simpan"}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
}
