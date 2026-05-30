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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Switch,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiPlus from "@/icons/nexture/ni-plus";
import NiCalendar from "@/icons/nexture/ni-calendar";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiEdit from "@/icons/nexture/ni-edit";
import NiTrash from "@/icons/nexture/ni-trash";
import NiVideo from "@/icons/nexture/ni-video";
import NiUsers from "@/icons/nexture/ni-users";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TablePagination from "@mui/material/TablePagination";
import TableSortLabel from "@mui/material/TableSortLabel";
import { LocalizationProvider, DatePicker } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";

interface FGDSession {
  id: string;
  title: string;
  description: string;
  topic: string;
  scheduled_date: string;
  scheduled_time: string;
  duration_minutes: number;
  status: string;
  max_participants: number;
  current_participants: number;
  conference_link?: string;
  conference_platform?: string;
  created_at: string;
  created_by: string;
}

interface CreateSessionData {
  title: string;
  description: string;
  topic: string;
  scheduled_date: string;
  scheduled_time: string;
  duration_minutes: number;
  max_participants: number;
  enable_conference: boolean;
}

function FGDPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sessions, setSessions] = useState<FGDSession[]>([]);
  const [activeTab, setActiveTab] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");

  const [formData, setFormData] = useState<CreateSessionData>({
    title: "",
    description: "",
    topic: "",
    scheduled_date: "",
    scheduled_time: "",
    duration_minutes: 60,
    max_participants: 10,
    enable_conference: false,
  });

  const TOPICS = [
    { value: "curriculum", label: "Kurikulum" },
    { value: "student_welfare", label: "Kesejahteraan Siswa" },
    { value: "facilities", label: "Sarpras" },
    { value: "strategic", label: "Strategis" },
    { value: "other", label: "Lainnya" },
  ];

  const STATUS_OPTIONS = [
    { value: "all", label: "Semua Status" },
    { value: "scheduled", label: "Terjadwal" },
    { value: "in_progress", label: "Sedang Berlangsung" },
    { value: "completed", label: "Selesai" },
    { value: "cancelled", label: "Dibatalkan" },
  ];

  const fetchSessions = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions?limit=100`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSessions(json.data || []);
      } else {
        setError(json.message || "Failed to load sessions");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const filteredSessions = sessions.filter((session) => {
    const matchesSearch =
      session.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      session.topic.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = filterStatus === "all" || session.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "fgd_sessions", data: filteredSessions, defaultLimit: 10 });

  const handleCreateSession = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const json = await res.json();

      if (json.status === "success") {
        setOpenDialog(false);
        fetchSessions();
        setFormData({
          title: "",
          description: "",
          topic: "",
          scheduled_date: "",
          scheduled_time: "",
          duration_minutes: 60,
          max_participants: 10,
          enable_conference: false,
        });
      } else {
        setError(json.message || "Failed to create session");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const handleDeleteSession = async (sessionId: string) => {
    if (!confirm("Apakah Anda yakin ingin menghapus sesi FGD ini?")) {
      return;
    }

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${sessionId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        fetchSessions();
      } else {
        setError("Gagal menghapus sesi");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "scheduled":
        return "info";
      case "in_progress":
        return "warning";
      case "completed":
        return "success";
      case "cancelled":
        return "error";
      default:
        return "default";
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "scheduled":
        return "Terjadwal";
      case "in_progress":
        return "Berlangsung";
      case "completed":
        return "Selesai";
      case "cancelled":
        return "Dibatalkan";
      default:
        return status;
    }
  };

  const upcomingSessions = sessions
    .filter((s) => s.status === "scheduled" && new Date(s.scheduled_date) >= new Date())
    .sort((a, b) => new Date(a.scheduled_date).getTime() - new Date(b.scheduled_date).getTime())
    .slice(0, 5);

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          FGD Virtual
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => setOpenDialog(true)}
        >
          Buat Sesi FGD
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Typography variant="body2">FGD Virtual</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} className="mb-4">
        <Tab label="Daftar Sesi" />
        <Tab label="Kalender" />
      </Tabs>

      {activeTab === 0 && (
        <>
          <Card className="mb-6">
            <CardContent className="p-4">
              <Grid container spacing={3} alignItems="flex-end">
                <Grid size={{ xs: 12, md: 4 }}>
                  <TextField
                    fullWidth
                    placeholder="Cari sesi FGD..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    size="small"
                  />
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Status</InputLabel>
                    <Select
                      label="Status"
                      value={filterStatus}
                      onChange={(e) => setFilterStatus(e.target.value)}
                    >
                      {STATUS_OPTIONS.map((status) => (
                        <MenuItem key={status.value} value={status.value}>
                          {status.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

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
                        Judul Sesi
                      </TableSortLabel>
                    </TableCell>
                    <TableCell className="font-bold">Topik</TableCell>
                    <TableCell className="font-bold">Jadwal</TableCell>
                    <TableCell className="font-bold">Durasi</TableCell>
                    <TableCell className="font-bold">Peserta</TableCell>
                    <TableCell className="font-bold">Status</TableCell>
                    <TableCell className="font-bold">Konferensi</TableCell>
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
                          Tidak ada sesi FGD yang ditemukan
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    paginatedData.map((session) => (
                      <TableRow key={session.id} hover>
                        <TableCell>
                          <Typography variant="body2" className="font-medium">
                            {session.title}
                          </Typography>
                          {session.description && (
                            <Typography variant="caption" className="text-text-secondary line-clamp-1">
                              {session.description}
                            </Typography>
                          )}
                        </TableCell>
                        <TableCell>
                          <Chip label={session.topic} size="small" variant="outlined" />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {new Date(session.scheduled_date).toLocaleDateString("id-ID", {
                              day: "numeric",
                              month: "short",
                              year: "numeric",
                            })}
                          </Typography>
                          <Typography variant="caption" className="text-text-secondary">
                            {session.scheduled_time}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{session.duration_minutes} menit</Typography>
                        </TableCell>
                        <TableCell>
                          <Stack direction="row" spacing={1} alignItems="center">
                            <NiUsers size={16} />
                            <Typography variant="body2">
                              {session.current_participants}/{session.max_participants}
                            </Typography>
                          </Stack>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={getStatusLabel(session.status)}
                            size="small"
                            color={getStatusColor(session.status) as any}
                          />
                        </TableCell>
                        <TableCell>
                          {session.conference_link ? (
                            <Button
                              size="small"
                              variant="outlined"
                              startIcon={<NiVideo size="small" />}
                              href={session.conference_link}
                              target="_blank"
                            >
                              Join
                            </Button>
                          ) : (
                            <Typography variant="caption" className="text-text-secondary">
                              -
                            </Typography>
                          )}
                        </TableCell>
                        <TableCell align="right">
                          <IconButton
                            size="small"
                            onClick={() => navigate(`/strategic-planning/data-collection/fgd/${session.id}`)}
                          >
                            <NiEyeOpen size="small" />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => navigate(`/strategic-planning/data-collection/fgd/${session.id}/edit`)}
                          >
                            <NiEdit size="small" />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteSession(session.id)}
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
        </>
      )}

      {activeTab === 1 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 8 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Kalender Sesi FGD
                </Typography>
                <Typography variant="body2" className="text-text-secondary">
                  Calendar view placeholder - Kalender interaktif akan ditampilkan di sini dengan integrasi
                  @mui/x-date-pickers CalendarView atau library kalender lainnya
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Sesi Akan Datang
                </Typography>
                {upcomingSessions.length === 0 ? (
                  <Typography variant="body2" className="text-text-secondary">
                    Tidak ada sesi yang akan datang
                  </Typography>
                ) : (
                  <Stack spacing={3}>
                    {upcomingSessions.map((session) => (
                      <Box key={session.id} className="p-3 border rounded">
                        <Typography variant="subtitle2" className="font-bold mb-1">
                          {session.title}
                        </Typography>
                        <Stack direction="row" spacing={1} className="mb-2" alignItems="center">
                          <NiCalendar size={16} />
                          <Typography variant="caption">
                            {new Date(session.scheduled_date).toLocaleDateString("id-ID", {
                              day: "numeric",
                              month: "short",
                              year: "numeric",
                            })}
                            , {session.scheduled_time}
                          </Typography>
                        </Stack>
                        <Button
                          size="small"
                          variant="outlined"
                          fullWidth
                          onClick={() => navigate(`/strategic-planning/data-collection/fgd/${session.id}`)}
                        >
                          Detail
                        </Button>
                      </Box>
                    ))}
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Buat Sesi FGD Baru</DialogTitle>
        <DialogContent>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Grid container spacing={3} className="mt-2">
              <Grid size={{ xs: 12 }}>
                <FormControl fullWidth>
                  <TextField
                    fullWidth
                    label="Judul Sesi *"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12 }}>
                <FormControl fullWidth>
                  <TextField
                    fullWidth
                    label="Deskripsi"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    multiline
                    rows={3}
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Topik</InputLabel>
                  <Select
                    label="Topik"
                    value={formData.topic}
                    onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                  >
                    {TOPICS.map((topic) => (
                      <MenuItem key={topic.value} value={topic.value}>
                        {topic.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <DatePicker
                    label="Tanggal"
                    value={formData.scheduled_date ? dayjs(formData.scheduled_date) : null}
                    onChange={(date) =>
                      setFormData({ ...formData, scheduled_date: date ? date.toISOString() : "" })
                    }
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <TextField
                    fullWidth
                    label="Waktu"
                    type="time"
                    value={formData.scheduled_time}
                    onChange={(e) => setFormData({ ...formData, scheduled_time: e.target.value })}
                    InputLabelProps={{ shrink: true }}
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <TextField
                    fullWidth
                    label="Durasi (menit)"
                    type="number"
                    value={formData.duration_minutes}
                    onChange={(e) =>
                      setFormData({ ...formData, duration_minutes: parseInt(e.target.value) || 60 })
                    }
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <TextField
                    fullWidth
                    label="Maks. Peserta"
                    type="number"
                    value={formData.max_participants}
                    onChange={(e) =>
                      setFormData({ ...formData, max_participants: parseInt(e.target.value) || 10 })
                    }
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={formData.enable_conference}
                      onChange={(e) => setFormData({ ...formData, enable_conference: e.target.checked })}
                    />
                  }
                  label="Aktifkan Konferensi Video"
                />
              </Grid>
            </Grid>
          </LocalizationProvider>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Batal</Button>
          <Button onClick={handleCreateSession} variant="contained">
            Buat Sesi
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default function FGDPageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR", "WALI_KELAS"]}>
      <FGDPage />
    </PermissionGuard>
  );
}