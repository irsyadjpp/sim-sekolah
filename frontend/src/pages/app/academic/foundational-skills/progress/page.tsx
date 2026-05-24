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

interface Progress {
  student_id: string;
  assessments: {
    id: string;
    standard_id: string;
    skill_code: string;
    skill_name: string;
    skill_type: string;
    mastery_level: string;
    score: number;
    notes: string;
  }[];
}

export default function FoundationalSkillsProgressPage() {
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [progress, setProgress] = useState<Progress | null>(null);

  const [selectedClassroomId, setSelectedClassroomId] = useState("");
  const [selectedStudentId, setSelectedStudentId] = useState("");

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

  const fetchProgress = useCallback(
    async (studentId: string) => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/foundational-skills/students/${studentId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success") {
          setProgress(json.data);
        } else {
          setError(json.message);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [token, setError],
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
    if (selectedStudentId) {
      fetchProgress(selectedStudentId);
    } else {
      setProgress(null);
    }
  }, [selectedStudentId, fetchProgress]);

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Progres Keterampilan Dasar Siswa
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/foundational-skills">Keterampilan Dasar</Link>
        <Typography variant="body2">Progres</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="flex gap-4 p-4">
          <FormControl size="small" className="min-w-[200px]">
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

          <FormControl size="small" className="min-w-[300px]" disabled={!selectedClassroomId}>
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
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {!selectedStudentId ? (
        <Alert severity="info">Pilih kelas dan siswa untuk melihat riwayat keterampilan dasarnya.</Alert>
      ) : loading ? (
        <Box className="flex justify-center p-10">
          <CircularProgress />
        </Box>
      ) : progress && progress.assessments ? (
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Tipe Keterampilan</TableCell>
                <TableCell className="font-bold">Kode / Nama</TableCell>
                <TableCell className="font-bold">Tingkat Penguasaan</TableCell>
                <TableCell className="font-bold">Skor</TableCell>
                <TableCell className="font-bold">Catatan</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {progress.assessments.length > 0 ? (
                progress.assessments.map((a) => (
                  <TableRow key={a.id} hover>
                    <TableCell>
                      <Chip
                        label={a.skill_type}
                        color={a.skill_type === "LITERASI" ? "primary" : "secondary"}
                        size="small"
                      />
                    </TableCell>
                    <TableCell className="font-medium">
                      <span className="text-primary mr-2">{a.skill_code}</span>
                      {a.skill_name}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={a.mastery_level}
                        color={
                          a.mastery_level === "MENGUASAI"
                            ? "success"
                            : a.mastery_level === "SEDANG"
                              ? "warning"
                              : "error"
                        }
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{a.score}</TableCell>
                    <TableCell>{a.notes}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center" className="py-10">
                    Siswa ini belum memiliki data asesmen keterampilan dasar.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      ) : null}
    </Box>
  );
}
