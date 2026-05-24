import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  FormControl,
  InputLabel,
  LinearProgress,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
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

interface Subject {
  id: string;
  name: string;
  code: string;
}

interface ProgressionDetail {
  id: string;
  student_id: string;
  subject_id: string;
  experience_id: string;
  experience_code: string;
  experience_name: string;
  mastery_level: number;
  last_assessed_at: string;
  notes: string;
}

interface ProgressionSummary {
  student_id: string;
  subject_id: string;
  progressions: ProgressionDetail[];
  average_mastery: number;
  readiness_status: string;
}

export default function LearningExperienceProgressionPage() {
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [progression, setProgression] = useState<ProgressionSummary | null>(null);

  const [selectedClassroomId, setSelectedClassroomId] = useState("");
  const [selectedStudentId, setSelectedStudentId] = useState("");
  const [selectedSubjectId, setSelectedSubjectId] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const token = localStorage.getItem("accessToken");

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

  const fetchSubjects = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects?limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setSubjects(json.data);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  const fetchProgression = useCallback(
    async (studentId: string, subjectId: string) => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(
          `${DEFAULTS.API_URL}/api/v1/students/${studentId}/subjects/${subjectId}/progression-summary`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        const json = await res.json();
        if (json.success === true) {
          setProgression(json.data);
        } else {
          setError(json.message);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [token],
  );

  useEffect(() => {
    fetchClassrooms();
  }, [fetchClassrooms]);

  useEffect(() => {
    if (selectedClassroomId) {
      fetchStudents(selectedClassroomId);
    } else {
      setStudents([]);
      setSelectedStudentId("");
    }
  }, [selectedClassroomId, fetchStudents]);

  useEffect(() => {
    fetchSubjects();
  }, [fetchSubjects]);

  useEffect(() => {
    if (selectedStudentId && selectedSubjectId) {
      fetchProgression(selectedStudentId, selectedSubjectId);
    } else {
      setProgression(null);
    }
  }, [selectedStudentId, selectedSubjectId, fetchProgression]);

  const getReadinessColor = (status: string) => {
    switch (status) {
      case "READY":
        return "success";
      case "NEEDS_IMPROVEMENT":
        return "warning";
      case "NOT_READY":
        return "error";
      default:
        return "default";
    }
  };

  const getReadinessLabel = (status: string) => {
    switch (status) {
      case "READY":
        return "Siap";
      case "NEEDS_IMPROVEMENT":
        return "Perlu Peningkatan";
      case "NOT_READY":
        return "Belum Siap";
      default:
        return status;
    }
  };

  const getExperienceColor = (code: string) => {
    switch (code) {
      case "MEMAHAMI":
        return "primary";
      case "MENAPLIKASI":
        return "secondary";
      case "MEREFEKSI":
        return "success";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Progres Tahap Pengalaman Belajar Siswa
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/learning-experiences">Tahap Pengalaman Belajar</Link>
        <Typography variant="body2">Progres</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="flex flex-wrap gap-4 p-4">
          <FormControl className="min-w-[200px]">
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

          <FormControl className="min-w-[300px]" disabled={!selectedClassroomId}>
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

          <FormControl className="min-w-[200px]" disabled={!selectedStudentId}>
            <InputLabel>Pilih Mata Pelajaran</InputLabel>
            <Select
              label="Pilih Mata Pelajaran"
              value={selectedSubjectId}
              onChange={(e) => setSelectedSubjectId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Mata Pelajaran --</em>
              </MenuItem>
              {subjects.map((s) => (
                <MenuItem key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {!selectedStudentId || !selectedSubjectId ? (
        <Alert severity="info">
          Pilih kelas, siswa, dan mata pelajaran untuk melihat progres tahap pengalaman belajar.
        </Alert>
      ) : loading ? (
        <Box className="flex justify-center p-10">
          <CircularProgress />
        </Box>
      ) : progression ? (
        <Box>
          <Card className="mb-6">
            <CardContent className="p-6">
              <Typography variant="h6" className="mb-4">
                Ringkasan Progres
              </Typography>
              <Box className="mb-4">
                <Typography variant="body2" className="mb-2">
                  Rata-rata Penguasaan: {(progression.average_mastery * 100).toFixed(1)}%
                </Typography>
                <LinearProgress variant="determinate" value={progression.average_mastery * 100} className="h-3" />
              </Box>
              <Chip
                label={`Status: ${getReadinessLabel(progression.readiness_status)}`}
                color={getReadinessColor(progression.readiness_status) as any}
                size="medium"
              />
            </CardContent>
          </Card>

          <TableContainer component={Card}>
            <Table>
              <TableHead>
                <TableRow className="bg-action-hover">
                  <TableCell className="font-bold">Tahap Pengalaman</TableCell>
                  <TableCell className="font-bold">Kode</TableCell>
                  <TableCell className="font-bold">Penguasaan</TableCell>
                  <TableCell className="font-bold">Progres</TableCell>
                  <TableCell className="font-bold">Terakhir Dinilai</TableCell>
                  <TableCell className="font-bold">Catatan</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {progression.progressions.length > 0 ? (
                  progression.progressions
                    .sort((a, b) => {
                      const order = { MEMAHAMI: 1, MENAPLIKASI: 2, MEREFLEKSI: 3 };
                      return (
                        (order[a.experience_code as keyof typeof order] || 0) -
                        (order[b.experience_code as keyof typeof order] || 0)
                      );
                    })
                    .map((p) => (
                      <TableRow key={p.id} hover>
                        <TableCell className="font-medium">{p.experience_name}</TableCell>
                        <TableCell>
                          <Chip
                            label={p.experience_code}
                            color={getExperienceColor(p.experience_code) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell className="font-medium">{(p.mastery_level * 100).toFixed(1)}%</TableCell>
                        <TableCell className="w-48">
                          <LinearProgress variant="determinate" value={p.mastery_level * 100} className="h-2" />
                        </TableCell>
                        <TableCell>
                          {p.last_assessed_at ? new Date(p.last_assessed_at).toLocaleDateString("id-ID") : "-"}
                        </TableCell>
                        <TableCell>{p.notes || "-"}</TableCell>
                      </TableRow>
                    ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={6} align="center" className="py-10">
                      Siswa ini belum memiliki data progres tahap pengalaman belajar.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      ) : null}
    </Box>
  );
}
