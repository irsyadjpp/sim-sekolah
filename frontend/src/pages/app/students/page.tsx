import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
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
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

interface Student {
  id: string;
  nisn: string;
  full_name: string;
  gender: string;
  school_id: string;
}

export default function StudentsPage() {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const fetchData = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students?limit=10000&search=${search}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setStudents(json.data || []);
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
      fetchData();
    }, 500);
    return () => clearTimeout(timer);
  }, [search]);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "students", data: students, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Manajemen Siswa
        </Typography>
        <Button variant="contained" startIcon={<NiPlus size="small" />} component={Link} to="/students/create">
          Tambah Siswa
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Typography variant="body2">Siswa</Typography>
      </Breadcrumbs>

      <Card className="mb-6 overflow-visible">
        <CardContent className="p-4">
          <TextField
            fullWidth
            placeholder="Cari NISN atau Nama Siswa..."
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
              <TableCell className="font-bold" sortDirection={sortBy === "nisn" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "nisn"}
                  direction={sortBy === "nisn" ? sortDir : "asc"}
                  onClick={() => handleSort("nisn")}
                >
                  NISN
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
              <TableCell className="font-bold" sortDirection={sortBy === "gender" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "gender"}
                  direction={sortBy === "gender" ? sortDir : "asc"}
                  onClick={() => handleSort("gender")}
                >
                  L/P
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
                <TableCell colSpan={4} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((s) => (
                <TableRow key={s.id} hover>
                  <TableCell className="font-mono">{s.nisn}</TableCell>
                  <TableCell className="font-bold">{s.full_name}</TableCell>
                  <TableCell>
                    <Chip label={s.gender} size="small" color={s.gender === "L" ? "info" : "error"} />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton size="small" color="primary" onClick={() => navigate(`/students/details?id=${s.id}`)}>
                      <NiPen size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Belum ada data siswa.
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
    </Box>
  );
}
