/* eslint-disable @typescript-eslint/no-unused-vars */
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
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPlus from "@/icons/nexture/ni-plus";

interface KspDocument {
  id: string;
  academic_year: { year_name: string; semester: string };
  status: string;
  updated_at: string;
}

export default function KspListPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [docs, setDocs] = useState<KspDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/curriculum-documents`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setDocs(json.data || []);
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

  const handleCreateDraft = async () => {
    // TODO: We need active academic_year_id and school_id for the payload.
    // For now, let's assume the backend takes care of defaulting or the user needs a modal.
    // Actually, backend needs payload: { academic_year_id, school_id }.
    // We can fetch active year and school first, or backend can provide a simpler endpoint.
    // Since backend handler uses BodyParser(&req) which requires AcademicYearID and SchoolID.
    alert("Inisiasi otomatis belum diimplementasi (membutuhkan ID tahun ajaran aktif).");
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "FINAL":
        return "success";
      case "REVIEW":
        return "warning";
      default:
        return "default";
    }
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "ksp", data: docs, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("ksp-builder.title")}
        </Typography>
        <Button variant="contained" startIcon={<NiPlus size="small" />} onClick={handleCreateDraft}>
          {t("ksp-builder.create-draft")}
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">{t("ksp-builder.breadcrumb-home")}</Link>
        <Link to="/academic">{t("ksp-builder.breadcrumb-academic")}</Link>
        <Typography variant="body2">{t("ksp-builder.breadcrumb-ksp")}</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold" sortDirection={sortBy === "academic_year.year_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "academic_year.year_name"}
                  direction={sortBy === "academic_year.year_name" ? sortDir : "asc"}
                  onClick={() => handleSort("academic_year.year_name")}
                >
                  {t("ksp-builder.academic-year")}
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "status" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "status"}
                  direction={sortBy === "status" ? sortDir : "asc"}
                  onClick={() => handleSort("status")}
                >
                  Status
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "updated_at" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "updated_at"}
                  direction={sortBy === "updated_at" ? sortDir : "asc"}
                  onClick={() => handleSort("updated_at")}
                >
                  {t("ksp-builder.last-updated")}
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
              paginatedData.map((doc) => (
                <TableRow key={doc.id} hover>
                  <TableCell>
                    <Typography className="font-medium">
                      {doc.academic_year.year_name} ({doc.academic_year.semester})
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={doc.status} size="small" color={getStatusColor(doc.status) as any} />
                  </TableCell>
                  <TableCell>{new Date(doc.updated_at).toLocaleString()}</TableCell>
                  <TableCell align="center">
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<NiEyeOpen size="small" />}
                      onClick={() => navigate(`/academic/ksp/details?id=${doc.id}`)}
                    >
                      Buka Dokumen
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  {t("ksp-builder.no-data")}
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
