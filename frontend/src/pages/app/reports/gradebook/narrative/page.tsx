/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

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
import NiFlash from "@/icons/nexture/ni-flash";

interface StudentReport {
  id: string;
  student: { full_name: string; nisn: string };
  status: string;
  academic_narrative_ai: string;
  character_narrative_ai: string;
  is_finalized: boolean;
}

export default function ReportNarrativePage() {
  const { t } = useTranslation();
  const [reports, setReports] = useState<StudentReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generatingId, setGeneratingId] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setReports(json.data || []);
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
    useClientTable({ key: "report_narrative", data: reports, defaultLimit: 10 });

  const handleGenerateAI = async (id: string) => {
    setGeneratingId(id);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${id}/generate-ai-description`, {
        method: "POST",
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
    } finally {
      setGeneratingId(null);
    }
  };

  return (
    <Box>
      <Typography variant="h1" component="h1" className="mb-2">
        Narasi Rapor Otomatis (AI)
      </Typography>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/reports">Laporan</Link>
        <Typography variant="body2">Narasi Rapor</Typography>
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
              <TableCell className="font-bold" sortDirection={sortBy === "student.full_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "student.full_name"}
                  direction={sortBy === "student.full_name" ? sortDir : "asc"}
                  onClick={() => handleSort("student.full_name")}
                >
                  Siswa
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
              <TableCell className="font-bold">Narasi Akademik</TableCell>
              <TableCell className="font-bold">Narasi Karakter</TableCell>
              <TableCell className="font-bold" align="center">
                Aksi AI
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
              paginatedData.map((report) => (
                <TableRow key={report.id} hover>
                  <TableCell>
                    <Typography className="font-medium">{report.student.full_name}</Typography>
                    <Typography variant="caption" color="textSecondary">
                      NISN: {report.student.nisn}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={report.status}
                      size="small"
                      color={report.status === "FINAL" ? "success" : "default"}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" className="line-clamp-2 max-w-xs">
                      {report.academic_narrative_ai || "Belum ada narasi."}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" className="line-clamp-2 max-w-xs">
                      {report.character_narrative_ai || "Belum ada narasi."}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Button
                      variant="contained"
                      size="small"
                      color="secondary"
                      startIcon={
                        generatingId === report.id ? (
                          <CircularProgress size={14} color="inherit" />
                        ) : (
                          <NiFlash size="small" />
                        )
                      }
                      onClick={() => handleGenerateAI(report.id)}
                      disabled={generatingId !== null || report.is_finalized}
                    >
                      {report.academic_narrative_ai ? "Regenerasi" : "Generate"}
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10 text-gray-500">
                  Tidak ada data rapor untuk rombel ini.
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
