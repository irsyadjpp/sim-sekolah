/* eslint-disable @typescript-eslint/no-unused-vars */
import "react-quill-new/dist/quill.snow.css";

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
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
  Grid,
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
import { useConfirm } from "@/hooks/use-confirm";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

interface Subject {
  id: string;
  subject_code: string;
  subject_name: string;
  rational?: string;
  goals?: string;
  characteristics?: string;
  is_active: boolean;
}

export default function SubjectsPage() {
  const { t } = useTranslation();
  const confirm = useConfirm();
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const fetchSubjects = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects?limit=10000&search=${search}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSubjects(json.data || []);
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
      fetchSubjects();
    }, 500);
    return () => clearTimeout(timer);
  }, [search]);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "subjects", data: subjects, defaultLimit: 10 });

  const handleDelete = async (id: string) => {
    const ok = await confirm({
      title: t("academic.subjects-delete-title"),
      message: t("academic.subjects-delete-confirm"),
      confirmText: t("common-ui.delete"),
      cancelText: t("common-ui.cancel"),
    });
    if (!ok) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchSubjects();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Mata Pelajaran
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => navigate("/academic/subjects/create")}
        >
          Tambah Mapel
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Mata Pelajaran</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="p-4">
          <TextField
            fullWidth
            placeholder="Cari kode atau nama mata pelajaran..."
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
              <TableCell className="font-bold" sortDirection={sortBy === "subject_code" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "subject_code"}
                  direction={sortBy === "subject_code" ? sortDir : "asc"}
                  onClick={() => handleSort("subject_code")}
                >
                  Kode
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "subject_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "subject_name"}
                  direction={sortBy === "subject_name" ? sortDir : "asc"}
                  onClick={() => handleSort("subject_name")}
                >
                  Nama Mata Pelajaran
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
                <TableCell colSpan={4} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((s) => (
                <TableRow key={s.id} hover>
                  <TableCell>{s.subject_code}</TableCell>
                  <TableCell className="font-medium">{s.subject_name}</TableCell>
                  <TableCell>
                    <Chip
                      label={s.is_active ? "Aktif" : "Non-aktif"}
                      color={s.is_active ? "success" : "default"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      size="small"
                      color="info"
                      onClick={() => navigate(`/academic/subjects/view?id=${s.id}`)}
                    >
                      <NiEyeOpen size="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => navigate(`/academic/subjects/edit?id=${s.id}`)}
                    >
                      <NiPen size="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDelete(s.id)}>
                      <NiBinEmpty size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Tidak ada data mata pelajaran.
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
