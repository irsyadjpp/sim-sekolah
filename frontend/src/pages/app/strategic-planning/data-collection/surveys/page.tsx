import { useEffect, useMemo, useState } from "react";
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
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";
import NiEdit from "@/icons/nexture/ni-edit";
import NiTrash from "@/icons/nexture/ni-trash";

interface Survey {
  id: string;
  title: string;
  description: string;
  survey_type: string;
  target_audience: string;
  status: string;
  created_at: string;
  created_by: string;
  questions_count?: number;
  responses_count?: number;
}

function SurveysPage() {
  const navigate = useNavigate();
  const [data, setData] = useState<Survey[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys?limit=100`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setData(json.data || []);
      } else {
        setError(json.message || "Failed to fetch surveys");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredData = useMemo(() => {
    return data.filter((d) => {
      const title = d.title || "";
      const description = d.description || "";
      const searchLower = searchQuery.toLowerCase();
      return (
        title.toLowerCase().includes(searchLower) ||
        description.toLowerCase().includes(searchLower)
      );
    });
  }, [data, searchQuery]);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "surveys", data: filteredData, defaultLimit: 10 });

  const handleDelete = async (id: string) => {
    if (!confirm("Apakah Anda yakin ingin menghapus kuesioner ini?")) {
      return;
    }

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        fetchData();
      } else {
        setError("Gagal menghapus kuesioner");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "success";
      case "draft":
        return "warning";
      case "closed":
        return "default";
      default:
        return "default";
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "active":
        return "Aktif";
      case "draft":
        return "Draft";
      case "closed":
        return "Tutup";
      default:
        return status;
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Kuesioner Digital
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => navigate("/strategic-planning/data-collection/surveys/create")}
        >
          Buat Kuesioner Baru
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Typography variant="body2">Kuesioner</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="p-4">
          <Grid container spacing={3} alignItems="flex-end">
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                fullWidth
                placeholder="Cari kuesioner..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
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
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {loading ? (
        <Box className="flex justify-center items-center py-12">
          <CircularProgress size={48} />
        </Box>
      ) : (
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell className="font-bold" sortDirection={sortBy === "title" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "title"}
                    direction={sortBy === "title" ? sortDir : "asc"}
                    onClick={() => handleSort("title")}
                  >
                    Judul Kuesioner
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-bold">Tipe Kuesioner</TableCell>
                <TableCell className="font-bold">Target Audiens</TableCell>
                <TableCell className="font-bold">Status</TableCell>
                <TableCell className="font-bold">Responses</TableCell>
                <TableCell className="font-bold" sortDirection={sortBy === "created_at" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "created_at"}
                    direction={sortBy === "created_at" ? sortDir : "asc"}
                    onClick={() => handleSort("created_at")}
                  >
                    Dibuat
                  </TableSortLabel>
                </TableCell>
                <TableCell align="right" className="font-bold">
                  Aksi
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedData.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={8} align="center" className="py-12">
                    <Typography variant="body2" className="text-text-secondary">
                      Tidak ada kuesioner yang ditemukan
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                paginatedData.map((survey) => (
                  <TableRow key={survey.id} hover>
                    <TableCell>
                      <Typography variant="body2" className="font-medium">
                        {survey.title}
                      </Typography>
                      {survey.description && (
                        <Typography variant="caption" className="text-text-secondary line-clamp-1">
                          {survey.description}
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell>
                      <Chip label={survey.survey_type} size="small" variant="outlined" />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{survey.target_audience}</Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={getStatusLabel(survey.status)}
                        size="small"
                        color={getStatusColor(survey.status) as any}
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {survey.responses_count || survey.questions_count || 0}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(survey.created_at).toLocaleDateString("id-ID", {
                          day: "numeric",
                          month: "long",
                          year: "numeric",
                        })}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/strategic-planning/data-collection/surveys/${survey.id}`)}
                      >
                        <NiEyeOpen size="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/strategic-planning/data-collection/surveys/${survey.id}/edit`)}
                      >
                        <NiEdit size="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDelete(survey.id)}
                        color="error"
                      >
                        <NiTrash size="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25, 50]}
            component="div"
            count={total}
            rowsPerPage={limit}
            page={page}
            onPageChange={handlePageChange}
            onRowsPerPageChange={handleLimitChange}
            labelRowsPerPage="Baris per halaman:"
            labelDisplayedRows={({ from, to, count }) => `${from}-${to} dari ${count}`}
          />
        </TableContainer>
      )}
    </Box>
  );
}

export default function SurveysPageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR"]}>
      <SurveysPage />
    </PermissionGuard>
  );
}