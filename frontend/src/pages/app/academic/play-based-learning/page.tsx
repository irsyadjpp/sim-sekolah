import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiStar from "@/icons/nexture/ni-star";

interface PlayBasedActivity {
  id: string;
  activity_name: string;
  play_type: string;
  phase: string;
  learning_objectives: string;
  materials: string;
  space_requirements: string;
  duration_minutes: number;
  facilitator_notes: string;
  created_at: string;
}

interface PlayBasedSession {
  id: string;
  student_id: string;
  activity_id: string;
  session_date: string;
  duration_minutes: number;
  participation_level: string;
  social_interaction: string;
  skill_development: string;
  engagement_level: string;
  notes: string;
}

export default function PlayBasedLearningPage() {
  const [activities, setActivities] = useState<PlayBasedActivity[]>([]);
  const [sessions, setSessions] = useState<PlayBasedSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openActivityDialog, setOpenActivityDialog] = useState(false);
  const [openSessionDialog, setOpenSessionDialog] = useState(false);
  const [activityFormData, setActivityFormData] = useState({
    activity_name: "",
    play_type: "",
    phase: "",
    learning_objectives: "",
    materials: "",
    space_requirements: "",
    duration_minutes: 30,
    facilitator_notes: "",
  });
  const [sessionFormData, setSessionFormData] = useState({
    student_id: "",
    activity_id: "",
    session_date: "",
    duration_minutes: 30,
    participation_level: "",
    social_interaction: "",
    skill_development: "",
    engagement_level: "",
    notes: "",
  });

  const fetchActivities = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/play-based-learning/activities`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setActivities(json.data.activities || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSessions = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/play-based-learning/sessions`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSessions(json.data.sessions || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchActivities();
    fetchSessions();
  }, []);

  const handleCreateActivity = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/play-based-learning/activities`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(activityFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenActivityDialog(false);
        fetchActivities();
        setActivityFormData({
          activity_name: "",
          play_type: "",
          phase: "",
          learning_objectives: "",
          materials: "",
          space_requirements: "",
          duration_minutes: 30,
          facilitator_notes: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleCreateSession = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/play-based-learning/sessions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(sessionFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenSessionDialog(false);
        fetchSessions();
        setSessionFormData({
          student_id: "",
          activity_id: "",
          session_date: "",
          duration_minutes: 30,
          participation_level: "",
          social_interaction: "",
          skill_development: "",
          engagement_level: "",
          notes: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getPlayTypeLabel = (type: string) => {
    switch (type) {
      case "FREE_PLAY":
        return "Bermain Bebas";
      case "GUIDED_PLAY":
        return "Bermain Terpandu";
      case "STRUCTURED_PLAY":
        return "Bermain Terstruktur";
      case "GAMES":
        return "Permainan";
      case "DRAMATIC_PLAY":
        return "Bermain Peran";
      default:
        return type;
    }
  };

  const getParticipationColor = (level: string) => {
    switch (level) {
      case "PASSIVE":
        return "error";
      case "MODERATE":
        return "info";
      case "ACTIVE":
        return "success";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Play-Based Learning (Fase A)
        </Typography>
        <Box className="flex gap-2">
          <Button variant="outlined" startIcon={<NiStar size="small" />} onClick={() => setOpenSessionDialog(true)}>
            Catat Sesi Baru
          </Button>
          <Button variant="contained" startIcon={<NiStar size="small" />} onClick={() => setOpenActivityDialog(true)}>
            Aktivitas Baru
          </Button>
        </Box>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Play-Based Learning</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Sistem pembelajaran berbasis main untuk Fase A (Kelas 1-2 SD) sesuai Kurikulum Merdeka.
      </Alert>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Typography variant="h6" className="mb-4 font-bold">
        Aktivitas Bermain
      </Typography>
      <TableContainer component={Card} className="mb-6">
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Nama Aktivitas</TableCell>
              <TableCell className="font-bold">Tipe Main</TableCell>
              <TableCell className="font-bold">Fase</TableCell>
              <TableCell className="font-bold">Durasi (menit)</TableCell>
              <TableCell className="font-bold">Tujuan Pembelajaran</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : activities.length > 0 ? (
              activities.map((activity) => (
                <TableRow key={activity.id} hover>
                  <TableCell className="font-medium">{activity.activity_name}</TableCell>
                  <TableCell>
                    <Chip label={getPlayTypeLabel(activity.play_type)} size="small" />
                  </TableCell>
                  <TableCell>{activity.phase}</TableCell>
                  <TableCell>{activity.duration_minutes}</TableCell>
                  <TableCell className="text-sm">{activity.learning_objectives}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  Tidak ada aktivitas bermain yang dibuat.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h6" className="mb-4 font-bold">
        Sesi Bermain
      </Typography>
      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Student ID</TableCell>
              <TableCell className="font-bold">Activity ID</TableCell>
              <TableCell className="font-bold">Tanggal</TableCell>
              <TableCell className="font-bold">Durasi</TableCell>
              <TableCell className="font-bold">Partisipasi</TableCell>
              <TableCell className="font-bold">Interaksi Sosial</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : sessions.length > 0 ? (
              sessions.map((session) => (
                <TableRow key={session.id} hover>
                  <TableCell className="text-sm">{session.student_id}</TableCell>
                  <TableCell className="text-sm">{session.activity_id}</TableCell>
                  <TableCell className="text-sm">{session.session_date}</TableCell>
                  <TableCell>{session.duration_minutes} menit</TableCell>
                  <TableCell>
                    <Chip
                      label={session.participation_level}
                      color={getParticipationColor(session.participation_level)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell className="text-sm">{session.social_interaction}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  Tidak ada sesi bermain yang dicatat.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Activity Dialog */}
      <Dialog open={openActivityDialog} onClose={() => setOpenActivityDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Aktivitas Bermain Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Nama Aktivitas"
              fullWidth
              value={activityFormData.activity_name}
              onChange={(e) => setActivityFormData({ ...activityFormData, activity_name: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tipe Main</InputLabel>
              <Select
                value={activityFormData.play_type}
                label="Tipe Main"
                onChange={(e) => setActivityFormData({ ...activityFormData, play_type: e.target.value })}
              >
                <MenuItem value="FREE_PLAY">Bermain Bebas</MenuItem>
                <MenuItem value="GUIDED_PLAY">Bermain Terpandu</MenuItem>
                <MenuItem value="STRUCTURED_PLAY">Bermain Terstruktur</MenuItem>
                <MenuItem value="GAMES">Permainan</MenuItem>
                <MenuItem value="DRAMATIC_PLAY">Bermain Peran</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Fase</InputLabel>
              <Select
                value={activityFormData.phase}
                label="Fase"
                onChange={(e) => setActivityFormData({ ...activityFormData, phase: e.target.value })}
              >
                <MenuItem value="A">Fase A (Kelas 1-2)</MenuItem>
                <MenuItem value="B">Fase B (Kelas 3-4)</MenuItem>
                <MenuItem value="C">Fase C (Kelas 5-6)</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Tujuan Pembelajaran"
              fullWidth
              multiline
              rows={3}
              value={activityFormData.learning_objectives}
              onChange={(e) => setActivityFormData({ ...activityFormData, learning_objectives: e.target.value })}
            />
            <TextField
              label="Material"
              fullWidth
              multiline
              rows={2}
              value={activityFormData.materials}
              onChange={(e) => setActivityFormData({ ...activityFormData, materials: e.target.value })}
            />
            <TextField
              label="Kebutuhan Ruang"
              fullWidth
              value={activityFormData.space_requirements}
              onChange={(e) => setActivityFormData({ ...activityFormData, space_requirements: e.target.value })}
            />
            <TextField
              label="Durasi (menit)"
              type="number"
              fullWidth
              value={activityFormData.duration_minutes}
              onChange={(e) => setActivityFormData({ ...activityFormData, duration_minutes: parseInt(e.target.value) })}
            />
            <TextField
              label="Catatan Fasilitator"
              fullWidth
              multiline
              rows={2}
              value={activityFormData.facilitator_notes}
              onChange={(e) => setActivityFormData({ ...activityFormData, facilitator_notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenActivityDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateActivity}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Session Dialog */}
      <Dialog open={openSessionDialog} onClose={() => setOpenSessionDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Sesi Bermain Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Student ID"
              fullWidth
              value={sessionFormData.student_id}
              onChange={(e) => setSessionFormData({ ...sessionFormData, student_id: e.target.value })}
            />
            <TextField
              label="Activity ID"
              fullWidth
              value={sessionFormData.activity_id}
              onChange={(e) => setSessionFormData({ ...sessionFormData, activity_id: e.target.value })}
            />
            <TextField
              label="Tanggal Sesi"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={sessionFormData.session_date}
              onChange={(e) => setSessionFormData({ ...sessionFormData, session_date: e.target.value })}
            />
            <TextField
              label="Durasi (menit)"
              type="number"
              fullWidth
              value={sessionFormData.duration_minutes}
              onChange={(e) => setSessionFormData({ ...sessionFormData, duration_minutes: parseInt(e.target.value) })}
            />
            <FormControl fullWidth>
              <InputLabel>Tingkat Partisipasi</InputLabel>
              <Select
                value={sessionFormData.participation_level}
                label="Tingkat Partisipasi"
                onChange={(e) => setSessionFormData({ ...sessionFormData, participation_level: e.target.value })}
              >
                <MenuItem value="PASSIVE">Pasif</MenuItem>
                <MenuItem value="MODERATE">Sedang</MenuItem>
                <MenuItem value="ACTIVE">Aktif</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Interaksi Sosial"
              fullWidth
              multiline
              rows={2}
              value={sessionFormData.social_interaction}
              onChange={(e) => setSessionFormData({ ...sessionFormData, social_interaction: e.target.value })}
            />
            <TextField
              label="Pengembangan Skill"
              fullWidth
              multiline
              rows={2}
              value={sessionFormData.skill_development}
              onChange={(e) => setSessionFormData({ ...sessionFormData, skill_development: e.target.value })}
            />
            <TextField
              label="Catatan"
              fullWidth
              multiline
              rows={2}
              value={sessionFormData.notes}
              onChange={(e) => setSessionFormData({ ...sessionFormData, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenSessionDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateSession}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
