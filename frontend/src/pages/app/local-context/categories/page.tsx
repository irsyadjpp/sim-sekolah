import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import NiPlus from "@/icons/nexture/ni-plus";

interface Category {
  id: string;
  category_code: string;
  category_name: string;
  description: string;
}

export default function ContextCategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/local-contexts/categories`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setCategories(json.data || []);
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
    fetchData();
  }, []);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "context_categories", data: categories, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Kategori Konteks Lokal
        </Typography>
        <Button variant="contained" disabled startIcon={<NiPlus size="small" />}>
          Tambah Kategori (Opsional)
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/local-context">Konteks Lokal</Link>
        <Typography variant="body2">Kategori</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell className="font-bold" sortDirection={sortBy === "category_code" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "category_code"}
                  direction={sortBy === "category_code" ? sortDir : "asc"}
                  onClick={() => handleSort("category_code")}
                >
                  Kode Kategori
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "category_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "category_name"}
                  direction={sortBy === "category_name" ? sortDir : "asc"}
                  onClick={() => handleSort("category_name")}
                >
                  Nama Kategori
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold">Deskripsi</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((c) => (
                <TableRow key={c.id} hover>
                  <TableCell className="text-primary font-mono font-bold">{c.category_code}</TableCell>
                  <TableCell className="font-medium">{c.category_name}</TableCell>
                  <TableCell>{c.description}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-10">
                  Tidak ada kategori ditemukan.
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

      <Alert severity="info" className="mt-6">
        Kategori di atas adalah kategori standar untuk <strong>Kurikulum Merdeka & Deep Learning</strong>. Data ini
        digunakan untuk mengelompokkan Lingkungan, Sosial, Budaya, dan Pengalaman Nyata siswa.
      </Alert>
    </Box>
  );
}
