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

interface Standard {
  id: string;
  skill_code: string;
  skill_name: string;
  skill_type: string;
}

export default function FoundationalSkillsAssessmentPage() {
  const { enqueueSnackbar } = useSnackbar();
  const navigate = useNavigate();

  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [standards, setStandards] = useState<Standard[]>([]);

  const [selectedClassroomId, setSelectedClassroomId] = useState("");
  const [selectedStudentId, setSelectedStudentId] = useState("");
  const [selectedStandardId, setSelectedStandardId] = useState("");
  const [masteryLevel, setMasteryLevel] = useState("BELUM");
  const [score, setScore] = useState<number>(0);
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

  const fetchStandards = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/foundational-skills/standards`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setStandards(json.data.standards || []);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  useEffect(() => {
    fetchClassrooms();
    fetchStandards();
  }, [fetchClassrooms, fetchStandards]);

  useEffect(() => {
    if (selectedClassroomId) {
      fetchStudents(selectedClassroomId);
    } else {
      setStudents([]);
      setSelectedStudentId("");
    }
  }, [selectedClassroomId, fetchStudents]);

  const handleSubmit = async () => {
    if (!selectedStudentId || !selectedStandardId) {
      enqueueSnackbar("Pilih siswa dan standar keterampilan terlebih dahulu.", { variant: "warning" });
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/foundational-skills/assessments`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: selectedStudentId,
          standard_id: selectedStandardId,
          teacher_id: user?.id || "",
          mastery_level: masteryLevel,
          score: Number(score),
          notes,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        enqueueSnackbar("Asesmen keterampilan dasar berhasil disimpan!", { variant: "success" });
        navigate("/academic/foundational-skills/progress");
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
          Form Asesmen Keterampilan Dasar
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/foundational-skills">Keterampilan Dasar</Link>
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
            <InputLabel>Pilih Standar Keterampilan</InputLabel>
            <Select
              label="Pilih Standar Keterampilan"
              value={selectedStandardId}
              onChange={(e) => setSelectedStandardId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Standar --</em>
              </MenuItem>
              {standards.map((s) => (
                <MenuItem key={s.id} value={s.id}>
                  [{s.skill_type}] {s.skill_code} - {s.skill_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" fullWidth>
            <InputLabel>Tingkat Penguasaan (Mastery Level)</InputLabel>
            <Select
              label="Tingkat Penguasaan (Mastery Level)"
              value={masteryLevel}
              onChange={(e) => setMasteryLevel(e.target.value)}
            >
              <MenuItem value="BELUM">Belum Menguasai (BELUM)</MenuItem>
              <MenuItem value="SEDANG">Sedang Berkembang (SEDANG)</MenuItem>
              <MenuItem value="MENGUASAI">Sudah Menguasai (MENGUASAI)</MenuItem>
            </Select>
          </FormControl>

          <TextField
            label="Skor (0-100)"
            type="number"
            size="small"
            fullWidth
            value={score}
            onChange={(e) => setScore(parseInt(e.target.value) || 0)}
          />

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
            <Button component={Link} to="/academic/foundational-skills">
              Batal
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={loading || !selectedStudentId || !selectedStandardId}
            >
              {loading ? <CircularProgress size={24} /> : "Simpan Asesmen"}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
