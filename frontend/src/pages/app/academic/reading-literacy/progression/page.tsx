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

interface Progression {
  student_id: string;
  assessments: {
    id: string;
    level_id: string;
    level_code: string;
    level_name: string;
    words_per_minute: number;
    accuracy_score: number;
    comprehension_score: number;
    fluency_rating: string;
    notes: string;
  }[];
}

export default function ReadingLiteracyProgressionPage() {
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [progression, setProgression] = useState<Progression | null>(null);

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

  const fetchProgression = useCallback(
    async (studentId: string) => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reading-literacy/students/${studentId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success") {
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
      fetchProgression(selectedStudentId);
    } else {
      setProgression(null);
    }
  }, [selectedStudentId, fetchProgression]);

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Progres Literasi Membaca Siswa
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/reading-literacy">Literasi Membaca</Link>
        <Typography variant="body2">Progres</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="flex gap-4 p-4">
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
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {!selectedStudentId ? (
        <Alert severity="info">Pilih kelas dan siswa untuk melihat riwayat literasi membacanya.</Alert>
      ) : loading ? (
        <Box className="flex justify-center p-10">
          <CircularProgress />
        </Box>
      ) : progression && progression.assessments ? (
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Level Target</TableCell>
                <TableCell className="font-bold">WPM</TableCell>
                <TableCell className="font-bold">Akurasi (%)</TableCell>
                <TableCell className="font-bold">Komprehensi (%)</TableCell>
                <TableCell className="font-bold">Kelancaran</TableCell>
                <TableCell className="font-bold">Catatan</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {progression.assessments.length > 0 ? (
                progression.assessments.map((a) => (
                  <TableRow key={a.id} hover>
                    <TableCell className="font-medium">
                      <span className="text-primary mr-2">{a.level_code}</span>
                      {a.level_name}
                    </TableCell>
                    <TableCell>{a.words_per_minute}</TableCell>
                    <TableCell>{a.accuracy_score}</TableCell>
                    <TableCell>{a.comprehension_score}</TableCell>
                    <TableCell>
                      <Chip
                        label={a.fluency_rating}
                        color={
                          a.fluency_rating === "TINGGI"
                            ? "success"
                            : a.fluency_rating === "SEDANG"
                              ? "warning"
                              : "error"
                        }
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{a.notes}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    Siswa ini belum memiliki riwayat asesmen membaca.
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
