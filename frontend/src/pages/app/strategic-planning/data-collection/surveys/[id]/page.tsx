import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Chip,
  Divider,
  Grid,
  IconButton,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiChevronLeft from "@/icons/nexture/ni-chevron-left";
import NiEdit from "@/icons/nexture/ni-edit";
import NiCopy from "@/icons/nexture/ni-copy";
import NiShare from "@/icons/nexture/ni-share";
import NiDownload from "@/icons/nexture/ni-download";
import NiCheckCircle from "@/icons/nexture/ni-check-circle";
import NiXCircle from "@/icons/nexture/ni-x-circle";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TablePagination from "@mui/material/TablePagination";
import TableSortLabel from "@mui/material/TableSortLabel";

interface Survey {
  id: string;
  title: string;
  description: string;
  survey_type: string;
  target_audience: string;
  status: string;
  start_date: string;
  end_date: string;
  created_at: string;
  created_by: string;
  questions: any[];
}

interface Response {
  id: string;
  survey_id: string;
  respondent_name: string;
  respondent_type: string;
  submitted_at: string;
  answers: any[];
}

function SurveyDetailPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [survey, setSurvey] = useState<Survey | null>(null);
  const [responses, setResponses] = useState<Response[]>([]);
  const [responsesLoading, setResponsesLoading] = useState(false);
  const [shareLink, setShareLink] = useState<string | null>(null);
  const [copySuccess, setCopySuccess] = useState(false);

  const fetchSurvey = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSurvey(json.data);
      } else {
        setError(json.message || "Failed to load survey");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  const fetchResponses = async () => {
    setResponsesLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}/responses`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setResponses(json.data || []);
      } else {
        setError(json.message || "Failed to load responses");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setResponsesLoading(false);
    }
  };

  const generateShareLink = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}/share-link`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setShareLink(json.data.share_link);
      } else {
        setError(json.message || "Failed to generate share link");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const copyToClipboard = () => {
    if (shareLink) {
      navigator.clipboard.writeText(shareLink);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };

  const exportResponses = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}/export`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${survey?.title || "survey"}_responses.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        setError("Failed to export responses");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  useEffect(() => {
    fetchSurvey();
  }, [id]);

  useEffect(() => {
    if (activeTab === 1 && survey?.status === "active") {
      fetchResponses();
    }
  }, [activeTab, survey]);

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

  const { paginatedData, page, limit, total, handlePageChange, handleLimitChange } = useClientTable({
    key: "responses",
    data: responses,
    defaultLimit: 10,
  });

  if (loading) {
    return (
      <Box className="flex justify-center items-center py-12">
        <CircularProgress size={48} />
      </Box>
    );
  }

  if (!survey) {
    return (
      <Alert severity="error" className="m-4">
        Survey tidak ditemukan
      </Alert>
    );
  }

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Box className="flex items-center gap-2">
          <IconButton onClick={() => navigate("/strategic-planning/data-collection/surveys")}>
            <NiChevronLeft />
          </IconButton>
          <Typography variant="h1" component="h1" className="mb-0">
            {survey.title}
          </Typography>
          <Chip
            label={getStatusLabel(survey.status)}
            size="small"
            color={getStatusColor(survey.status) as any}
          />
        </Box>
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            startIcon={<NiShare size="small" />}
            onClick={generateShareLink}
          >
            Bagikan
          </Button>
          <Button
            variant="outlined"
            startIcon={<NiDownload size="small" />}
            onClick={exportResponses}
          >
            Export
          </Button>
          <Button
            variant="contained"
            startIcon={<NiEdit size="small" />}
            onClick={() => navigate(`/strategic-planning/data-collection/surveys/${survey.id}/edit`)}
          >
            Edit
          </Button>
        </Stack>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Link to="/strategic-planning/data-collection/surveys">Kuesioner</Link>
        <Typography variant="body2">{survey.title}</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {shareLink && (
        <Alert severity="info" className="mb-4">
          <Stack direction="row" spacing={2} alignItems="center">
            <Typography variant="body2">Link kuesioner: {shareLink}</Typography>
            <Button size="small" onClick={copyToClipboard}>
              {copySuccess ? "Tersalin!" : "Salin"}
            </Button>
          </Stack>
        </Alert>
      )}

      <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} className="mb-4">
        <Tab label="Detail" />
        <Tab label={`Responses (${responses.length})`} />
        <Tab label="Analytics" />
      </Tabs>

      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 8 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Informasi Kuesioner
                </Typography>
                <Grid container spacing={3}>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Judul
                    </Typography>
                    <Typography variant="body1">{survey.title}</Typography>
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Tipe Kuesioner
                    </Typography>
                    <Typography variant="body1">{survey.survey_type}</Typography>
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Target Audiens
                    </Typography>
                    <Typography variant="body1">{survey.target_audience}</Typography>
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Status
                    </Typography>
                    <Chip
                      label={getStatusLabel(survey.status)}
                      size="small"
                      color={getStatusColor(survey.status) as any}
                    />
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Tanggal Mulai
                    </Typography>
                    <Typography variant="body1">
                      {survey.start_date
                        ? new Date(survey.start_date).toLocaleDateString("id-ID", {
                          day: "numeric",
                          month: "long",
                          year: "numeric",
                        })
                        : "-"}
                    </Typography>
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Tanggal Selesai
                    </Typography>
                    <Typography variant="body1">
                      {survey.end_date
                        ? new Date(survey.end_date).toLocaleDateString("id-ID", {
                          day: "numeric",
                          month: "long",
                          year: "numeric",
                        })
                        : "-"}
                    </Typography>
                  </Grid>
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Deskripsi
                    </Typography>
                    <Typography variant="body1">{survey.description || "-"}</Typography>
                  </Grid>
                </Grid>

                <Divider className="my-4" />

                <Typography variant="h5" className="mb-4 font-bold">
                  Pertanyaan ({survey.questions.length})
                </Typography>
                {survey.questions.length === 0 ? (
                  <Typography variant="body2" className="text-text-secondary">
                    Belum ada pertanyaan
                  </Typography>
                ) : (
                  <Stack spacing={2}>
                    {survey.questions.map((question, index) => (
                      <Box key={question.id} className="pl-4 border-l-2 border-gray-200">
                        <Typography variant="subtitle1" className="font-bold mb-1">
                          {index + 1}. {question.question_text}
                          {question.required && <span className="text-error ml-1">*</span>}
                        </Typography>
                        {question.description && (
                          <Typography variant="body2" className="text-text-secondary mb-2">
                            {question.description}
                          </Typography>
                        )}
                        <Typography variant="caption" className="text-text-secondary">
                          Tipe: {question.question_type}
                        </Typography>
                      </Box>
                    ))}
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Statistik
                </Typography>
                <Stack spacing={3}>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Total Responses
                    </Typography>
                    <Typography variant="h3" className="font-bold">
                      {responses.length}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Total Pertanyaan
                    </Typography>
                    <Typography variant="h3" className="font-bold">
                      {survey.questions.length}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Status
                    </Typography>
                    <Stack direction="row" spacing={1} alignItems="center">
                      {survey.status === "active" ? (
                        <NiCheckCircle color="success" />
                      ) : (
                        <NiXCircle color="error" />
                      )}
                      <Typography variant="body1">{getStatusLabel(survey.status)}</Typography>
                    </Stack>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Card>
          <CardContent className="p-4">
            {survey.status !== "active" ? (
              <Alert severity="warning" className="mb-4">
                Survey harus dalam status aktif untuk melihat responses
              </Alert>
            ) : responsesLoading ? (
              <Box className="flex justify-center items-center py-12">
                <CircularProgress size={48} />
              </Box>
            ) : responses.length === 0 ? (
              <Typography variant="body2" className="text-text-secondary text-center py-12">
                Belum ada responses yang diterima
              </Typography>
            ) : (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell className="font-bold">Respondent</TableCell>
                      <TableCell className="font-bold">Tipe Respondent</TableCell>
                      <TableCell className="font-bold">Jawaban</TableCell>
                      <TableCell className="font-bold">Tanggal Submit</TableCell>
                      <TableCell align="right" className="font-bold">
                        Aksi
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {paginatedData.map((response) => (
                      <TableRow key={response.id} hover>
                        <TableCell>
                          <Typography variant="body2" className="font-medium">
                            {response.respondent_name}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip label={response.respondent_type} size="small" variant="outlined" />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {response.answers?.length || 0} jawaban
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {new Date(response.submitted_at).toLocaleDateString("id-ID", {
                              day: "numeric",
                              month: "long",
                              year: "numeric",
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <IconButton size="small">
                            <NiEyeOpen size="small" />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
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
          </CardContent>
        </Card>
      )}

      {activeTab === 2 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Overview
                </Typography>
                <Stack spacing={3}>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Total Responses
                    </Typography>
                    <Typography variant="h3" className="font-bold">
                      {responses.length}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Completion Rate
                    </Typography>
                    <Typography variant="h3" className="font-bold text-success">
                      100%
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Average Time
                    </Typography>
                    <Typography variant="h3" className="font-bold">
                      -- min
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 8 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Response Timeline
                </Typography>
                <Typography variant="body2" className="text-text-secondary">
                  Chart placeholder - Response timeline chart akan ditampilkan di sini
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Question Analytics
                </Typography>
                <Stack spacing={4}>
                  {survey.questions.map((question, index) => (
                    <Box key={question.id}>
                      <Typography variant="subtitle1" className="font-bold mb-2">
                        {index + 1}. {question.question_text}
                      </Typography>
                      <Typography variant="body2" className="text-text-secondary">
                        Analytics placeholder untuk pertanyaan ini
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}

export default function SurveyDetailPageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR"]}>
      <SurveyDetailPage />
    </PermissionGuard>
  );
}