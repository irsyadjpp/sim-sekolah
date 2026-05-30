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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider,
  Grid,
  IconButton,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiChevronLeft from "@/icons/nexture/ni-chevron-left";
import NiEdit from "@/icons/nexture/ni-edit";
import NiUsers from "@/icons/nexture/ni-users";
import NiVideo from "@/icons/nexture/ni-video";
import NiDownload from "@/icons/nexture/ni-download";
import NiPlus from "@/icons/nexture/ni-plus";
import NiTrash from "@/icons/nexture/ni-trash";
import NiFile from "@/icons/nexture/ni-file";
import NiBrain from "@/icons/nexture/ni-brain";

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

interface Participant {
  id: string;
  session_id: string;
  name: string;
  email: string;
  role: string;
  joined_at?: string;
}

interface FGDEntry {
  id: string;
  session_id: string;
  content: string;
  author: string;
  created_at: string;
}

interface SentimentData {
  sentiment: string;
  confidence: number;
  key_points: string[];
}

function FGDDetailPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [session, setSession] = useState<FGDSession | null>(null);
  const [participants, setParticipants] = useState<Participant[]>([]);
  const [entries, setEntries] = useState<FGDEntry[]>([]);
  const [newEntry, setNewEntry] = useState("");
  const [sentimentData, setSentimentData] = useState<SentimentData | null>(null);
  const [openAddParticipant, setOpenAddParticipant] = useState(false);
  const [newParticipant, setNewParticipant] = useState({ name: "", email: "", role: "participant" });

  const fetchSession = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSession(json.data);
        fetchParticipants();
        fetchEntries();
        fetchSentiment();
      } else {
        setError(json.message || "Failed to load session");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  const fetchParticipants = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/participants`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const json = await res.json();
      if (json.status === "success") {
        setParticipants(json.data || []);
      }
    } catch (err: any) {
      console.error("Failed to load participants:", err);
    }
  };

  const fetchEntries = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/entries`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setEntries(json.data || []);
      }
    } catch (err: any) {
      console.error("Failed to load entries:", err);
    }
  };

  const fetchSentiment = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/sentiment`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSentimentData(json.data);
      }
    } catch (err: any) {
      console.error("Failed to load sentiment:", err);
    }
  };

  useEffect(() => {
    fetchSession();
  }, [id]);

  const handleAddEntry = async () => {
    if (!newEntry.trim()) return;

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/entries`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content: newEntry }),
      });

      const json = await res.json();
      if (json.status === "success") {
        setNewEntry("");
        fetchEntries();
      } else {
        setError(json.message || "Failed to add entry");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const handleAddParticipant = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/participants`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(newParticipant),
        }
      );

      const json = await res.json();
      if (json.status === "success") {
        setOpenAddParticipant(false);
        setNewParticipant({ name: "", email: "", role: "participant" });
        fetchParticipants();
      } else {
        setError(json.message || "Failed to add participant");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const handleRemoveParticipant = async (participantId: string) => {
    if (!confirm("Hapus peserta ini?")) return;

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/participants/${participantId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (res.ok) {
        fetchParticipants();
      } else {
        setError("Gagal menghapus peserta");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const exportNotes = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/fgd/sessions/${id}/export`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${session?.title || "fgd"}_notes.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        setError("Failed to export notes");
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

  if (loading) {
    return (
      <Box className="flex justify-center items-center py-12">
        <CircularProgress size={48} />
      </Box>
    );
  }

  if (!session) {
    return (
      <Alert severity="error" className="m-4">
        Sesi tidak ditemukan
      </Alert>
    );
  }

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Box className="flex items-center gap-2">
          <IconButton onClick={() => navigate("/strategic-planning/data-collection/fgd")}>
            <NiChevronLeft />
          </IconButton>
          <Typography variant="h1" component="h1" className="mb-0">
            {session.title}
          </Typography>
          <Chip
            label={getStatusLabel(session.status)}
            size="small"
            color={getStatusColor(session.status) as any}
          />
        </Box>
        <Stack direction="row" spacing={2}>
          {session.conference_link && (
            <Button
              variant="outlined"
              startIcon={<NiVideo size="small" />}
              href={session.conference_link}
              target="_blank"
            >
              Join Conference
            </Button>
          )}
          <Button
            variant="outlined"
            startIcon={<NiEdit size="small" />}
            onClick={() => navigate(`/strategic-planning/data-collection/fgd/${session.id}/edit`)}
          >
            Edit
          </Button>
        </Stack>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Link to="/strategic-planning/data-collection/fgd">FGD Virtual</Link>
        <Typography variant="body2">{session.title}</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Grid container spacing={3} className="mb-6">
        <Grid size={{ xs: 12, md: 8 }}>
          <Card>
            <CardContent className="p-6">
              <Typography variant="h5" className="mb-4 font-bold">
                Informasi Sesi
              </Typography>
              <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Topik
                  </Typography>
                  <Typography variant="body1">{session.topic}</Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Status
                  </Typography>
                  <Chip
                    label={getStatusLabel(session.status)}
                    size="small"
                    color={getStatusColor(session.status) as any}
                  />
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Tanggal & Waktu
                  </Typography>
                  <Typography variant="body1">
                    {new Date(session.scheduled_date).toLocaleDateString("id-ID", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })}{" "}
                    - {session.scheduled_time}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Durasi
                  </Typography>
                  <Typography variant="body1">{session.duration_minutes} menit</Typography>
                </Grid>
                <Grid size={{ xs: 12 }}>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Deskripsi
                  </Typography>
                  <Typography variant="body1">{session.description || "-"}</Typography>
                </Grid>
              </Grid>
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
                    Peserta Terdaftar
                  </Typography>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <NiUsers size={20} />
                    <Typography variant="h3" className="font-bold">
                      {session.current_participants}/{session.max_participants}
                    </Typography>
                  </Stack>
                </Box>
                <Divider />
                <Box>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Notulensi Entries
                  </Typography>
                  <Typography variant="h3" className="font-bold">
                    {entries.length}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} className="mb-4">
        <Tab label="Notulensi" />
        <Tab label={`Peserta (${participants.length})`} />
        <Tab label="Analisis Sentimen" />
      </Tabs>

      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 8 }}>
            <Card>
              <CardContent className="p-6">
                <Box className="flex justify-between items-center mb-4">
                  <Typography variant="h5" className="font-bold">
                    Notulensi Kolaboratif
                  </Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<NiDownload size="small" />}
                    onClick={exportNotes}
                  >
                    Export
                  </Button>
                </Box>

                <Stack spacing={3} className="mb-4">
                  {entries.map((entry) => (
                    <Box key={entry.id} className="p-4 border rounded bg-gray-50">
                      <Box className="flex justify-between items-center mb-2">
                        <Typography variant="subtitle2" className="font-bold">
                          {entry.author}
                        </Typography>
                        <Typography variant="caption" className="text-text-secondary">
                          {new Date(entry.created_at).toLocaleString("id-ID")}
                        </Typography>
                      </Box>
                      <Typography variant="body2" className="whitespace-pre-wrap">
                        {entry.content}
                      </Typography>
                    </Box>
                  ))}
                </Stack>

                {entries.length === 0 && (
                  <Typography variant="body2" className="text-text-secondary text-center py-8">
                    Belum ada notulensi. Mulai dengan menambah entry di bawah.
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Tambah Notulensi
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  placeholder="Catat poin penting dari diskusi..."
                  value={newEntry}
                  onChange={(e) => setNewEntry(e.target.value)}
                  className="mb-4"
                />
                <Button
                  variant="contained"
                  fullWidth
                  onClick={handleAddEntry}
                  disabled={!newEntry.trim()}
                >
                  Tambah Entry
                </Button>
                <Typography variant="caption" className="text-text-secondary mt-2 block">
                  Real-time collaboration placeholder - notulensi akan disinkronkan secara real-time dengan
                  WebSocket atau polling
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 8 }}>
            <Card>
              <CardContent className="p-6">
                <Box className="flex justify-between items-center mb-4">
                  <Typography variant="h5" className="font-bold">
                    Daftar Peserta
                  </Typography>
                  <Button
                    variant="contained"
                    size="small"
                    startIcon={<NiPlus size="small" />}
                    onClick={() => setOpenAddParticipant(true)}
                    disabled={participants.length >= session.max_participants}
                  >
                    Tambah Peserta
                  </Button>
                </Box>

                <Stack spacing={2}>
                  {participants.length === 0 ? (
                    <Typography variant="body2" className="text-text-secondary text-center py-8">
                      Belum ada peserta
                    </Typography>
                  ) : (
                    participants.map((participant) => (
                      <Box
                        key={participant.id}
                        className="flex justify-between items-center p-4 border rounded"
                      >
                        <Box>
                          <Typography variant="subtitle1" className="font-bold">
                            {participant.name}
                          </Typography>
                          <Typography variant="body2" className="text-text-secondary">
                            {participant.email}
                          </Typography>
                          <Chip
                            label={participant.role}
                            size="small"
                            variant="outlined"
                            className="mt-1"
                          />
                        </Box>
                        <Stack direction="row" spacing={1}>
                          <Typography variant="caption" className="text-text-secondary">
                            {participant.joined_at
                              ? `Joined: ${new Date(participant.joined_at).toLocaleString("id-ID")}`
                              : "Belum join"}
                          </Typography>
                          <IconButton
                            size="small"
                            onClick={() => handleRemoveParticipant(participant.id)}
                          >
                            <NiTrash size="small" />
                          </IconButton>
                        </Stack>
                      </Box>
                    ))
                  )}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Ringkasan Peserta
                </Typography>
                <Stack spacing={3}>
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Total Terdaftar
                    </Typography>
                    <Typography variant="h3" className="font-bold">
                      {participants.length}
                    </Typography>
                  </Box>
                  <Divider />
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Kapasitas Tersedia
                    </Typography>
                    <Typography variant="h3" className="font-bold">
                      {session.max_participants - participants.length}
                    </Typography>
                  </Box>
                  <Divider />
                  <Box>
                    <Typography variant="subtitle2" className="text-text-secondary mb-1">
                      Sudah Join
                    </Typography>
                    <Typography variant="h3" className="font-bold text-success">
                      {participants.filter((p) => p.joined_at).length}
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 2 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Analisis Sentimen
                </Typography>
                {sentimentData ? (
                  <Stack spacing={3}>
                    <Box>
                      <Typography variant="subtitle2" className="text-text-secondary mb-1">
                        Sentimen Dominan
                      </Typography>
                      <Chip
                        label={sentimentData.sentiment === "positive" ? "Positif" : sentimentData.sentiment === "negative" ? "Negatif" : "Netral"}
                        size="large"
                        color={sentimentData.sentiment === "positive" ? "success" : sentimentData.sentiment === "negative" ? "error" : "default"}
                      />
                    </Box>
                    <Box>
                      <Typography variant="subtitle2" className="text-text-secondary mb-1">
                        Tingkat Keyakinan
                      </Typography>
                      <Typography variant="h3" className="font-bold">
                        {(sentimentData.confidence * 100).toFixed(1)}%
                      </Typography>
                    </Box>
                  </Stack>
                ) : (
                  <Typography variant="body2" className="text-text-secondary">
                    Tidak cukup data untuk analisis sentimen
                  </Typography>
                )}
                <Typography variant="caption" className="text-text-secondary mt-4 block">
                  Sentiment analysis placeholder - analisis akan menggunakan NLP untuk menganalisis
                  notulensi secara otomatis
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 8 }}>
            <Card>
              <CardContent className="p-6">
                <Typography variant="h5" className="mb-4 font-bold">
                  Poin Kunci
                </Typography>
                {sentimentData?.key_points && sentimentData.key_points.length > 0 ? (
                  <Stack spacing={2}>
                    {sentimentData.key_points.map((point, index) => (
                      <Box key={index} className="flex items-start gap-2">
                        <NiBrain className="text-primary mt-1" size={20} />
                        <Typography variant="body2">{point}</Typography>
                      </Box>
                    ))}
                  </Stack>
                ) : (
                  <Typography variant="body2" className="text-text-secondary">
                    Poin kunci akan ditampilkan setelah notulensi cukup untuk dianalisis
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Dialog open={openAddParticipant} onClose={() => setOpenAddParticipant(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Tambah Peserta</DialogTitle>
        <DialogContent>
          <Grid container spacing={3} className="mt-2">
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                label="Nama *"
                value={newParticipant.name}
                onChange={(e) => setNewParticipant({ ...newParticipant, name: e.target.value })}
                required
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                label="Email *"
                type="email"
                value={newParticipant.email}
                onChange={(e) => setNewParticipant({ ...newParticipant, email: e.target.value })}
                required
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                label="Role"
                value={newParticipant.role}
                onChange={(e) => setNewParticipant({ ...newParticipant, role: e.target.value })}
                select
              >
                <MenuItem value="participant">Peserta</MenuItem>
                <MenuItem value="moderator">Moderator</MenuItem>
                <MenuItem value="observer">Observer</MenuItem>
              </TextField>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddParticipant(false)}>Batal</Button>
          <Button onClick={handleAddParticipant} variant="contained">
            Tambah
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default function FGDDetailPageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR", "WALI_KELAS"]}>
      <FGDDetailPage />
    </PermissionGuard>
  );
}