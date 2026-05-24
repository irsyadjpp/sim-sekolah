import { useSnackbar } from "notistack";
import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface Classroom {
  id: string;
  name: string;
}

interface Student {
  id: string;
  full_name: string;
  nis: string;
}

interface ReadingLevel {
  id: string;
  level_code: string;
  level_name: string;
}

export default function ReadingLiteracyAssessmentPage() {
  const { enqueueSnackbar } = useSnackbar();
  const navigate = useNavigate();

  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [levels, setLevels] = useState<ReadingLevel[]>([]);

  const [selectedClassroomId, setSelectedClassroomId] = useState("");
  const [selectedStudentId, setSelectedStudentId] = useState("");
  const [selectedLevelId, setSelectedLevelId] = useState("");
  const [wpm, setWpm] = useState<number>(0);
  const [compScore, setCompScore] = useState<number>(0);
  const [accScore, setAccScore] = useState<number>(0);
  const [fluency, setFluency] = useState("SEDANG");
  const [notes, setNotes] = useState("");

  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem("accessToken");
  const userString = localStorage.getItem("user");
  const user = userString ? JSON.parse(userString) : null;

  const fetchClassrooms = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms?limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setClassrooms(json.data);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  const fetchStudents = useCallback(
    async (classId: string) => {
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classId}/students`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success" && json.data) {
          setStudents(json.data);
        }
      } catch (err: any) {
        console.error(err);
      }
    },
    [token],
  );

  const fetchLevels = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reading-literacy/levels`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setLevels(json.data.levels || []);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  useEffect(() => {
    fetchClassrooms();
    fetchLevels();
  }, [fetchClassrooms, fetchLevels]);

  useEffect(() => {
    if (selectedClassroomId) {
      fetchStudents(selectedClassroomId);
    } else {
      setStudents([]);
      setSelectedStudentId("");
    }
  }, [selectedClassroomId, fetchStudents]);

  const handleSubmit = async () => {
    if (!selectedStudentId || !selectedLevelId) {
      enqueueSnackbar("Pilih siswa dan tingkat membaca terlebih dahulu.", { variant: "warning" });
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reading-literacy/assessments`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: selectedStudentId,
          level_id: selectedLevelId,
          teacher_id: user?.id || "",
          words_per_minute: Number(wpm),
          comprehension_score: Number(compScore),
          accuracy_score: Number(accScore),
          fluency_rating: fluency,
          notes,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        enqueueSnackbar("Asesmen literasi membaca berhasil disimpan!", { variant: "success" });
        navigate("/academic/reading-literacy/progression");
      } else {
        enqueueSnackbar(json.message || "Gagal menyimpan asesmen", { variant: "error" });
      }
    } catch (err: any) {
      enqueueSnackbar(err.message || "Terjadi kesalahan koneksi", { variant: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Form Asesmen Membaca
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/reading-literacy">Literasi Membaca</Link>
        <Typography variant="body2">Asesmen</Typography>
      </Breadcrumbs>

      <Card className="max-w-2xl">
        <CardContent className="flex flex-col gap-4 p-6">
          <FormControl size="small" fullWidth>
            <InputLabel>Pilih Kelas</InputLabel>
            <Select
              label="Pilih Kelas"
              value={selectedClassroomId}
              onChange={(e) => setSelectedClassroomId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Kelas --</em>
              </MenuItem>
              {classrooms.map((c) => (
                <MenuItem key={c.id} value={c.id}>
                  {c.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" fullWidth disabled={!selectedClassroomId}>
            <InputLabel>Pilih Siswa</InputLabel>
            <Select
              label="Pilih Siswa"
              value={selectedStudentId}
              onChange={(e) => setSelectedStudentId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Siswa --</em>
              </MenuItem>
              {students.map((s) => (
                <MenuItem key={s.id} value={s.id}>
                  {s.full_name} ({s.nis})
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" fullWidth>
            <InputLabel>Tingkat Membaca (Target)</InputLabel>
            <Select
              label="Tingkat Membaca (Target)"
              value={selectedLevelId}
              onChange={(e) => setSelectedLevelId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Tingkat --</em>
              </MenuItem>
              {levels.map((l) => (
                <MenuItem key={l.id} value={l.id}>
                  [{l.level_code}] {l.level_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            label="Kata per Menit (WPM)"
            type="number"
            size="small"
            fullWidth
            value={wpm}
            onChange={(e) => setWpm(parseInt(e.target.value) || 0)}
          />

          <TextField
            label="Skor Akurasi (0-100)"
            type="number"
            size="small"
            fullWidth
            value={accScore}
            onChange={(e) => setAccScore(parseInt(e.target.value) || 0)}
          />

          <TextField
            label="Skor Komprehensi (0-100)"
            type="number"
            size="small"
            fullWidth
            value={compScore}
            onChange={(e) => setCompScore(parseInt(e.target.value) || 0)}
          />

          <FormControl size="small" fullWidth>
            <InputLabel>Rating Kelancaran</InputLabel>
            <Select label="Rating Kelancaran" value={fluency} onChange={(e) => setFluency(e.target.value)}>
              <MenuItem value="RENDAH">Rendah (Tersendat/Mengeja)</MenuItem>
              <MenuItem value="SEDANG">Sedang (Cukup Lancar)</MenuItem>
              <MenuItem value="TINGGI">Tinggi (Lancar & Ekspresif)</MenuItem>
            </Select>
          </FormControl>

          <TextField
            label="Catatan Guru"
            multiline
            rows={3}
            size="small"
            fullWidth
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />

          <Box className="mt-4 flex justify-end gap-2">
            <Button component={Link} to="/academic/reading-literacy">
              Batal
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={loading || !selectedStudentId || !selectedLevelId}
            >
              {loading ? <CircularProgress size={24} /> : "Simpan Asesmen"}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
