/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CircularProgress,
  Grid,
  Skeleton,
  Snackbar,
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
import NiFloppyDisk from "@/icons/nexture/ni-floppy-disk";

interface Student {
  id: string;
  full_name: string;
  nisn: string;
}

interface Enrollment {
  id: string;
  student: Student;
}

interface AssessmentScore {
  student_id: string;
  score: number | string;
  notes: string;
}

interface AssessmentDetail {
  id: string;
  assessment_name: string;
  assessment_type: string;
  teaching_assignment: {
    classroom_id: string;
    subject: { subject_name: string };
    teacher: { full_name: string };
  };
}

export default function SummativeDetailsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const id = query.get("id");

  const [assessment, setAssessment] = useState<AssessmentDetail | null>(null);
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [scores, setScores] = useState<Record<string, AssessmentScore>>({});

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error">("success");

  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    if (!id) {
      navigate("/academic/evaluation/summative");
      return;
    }
    fetchData();
  }, [id]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch Assessment Detail
      const resAss = await fetch(`${DEFAULTS.API_URL}/api/v1/assessments/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const jsonAss = await resAss.json();
      if (jsonAss.status !== "success") throw new Error(jsonAss.message);
      const assData = jsonAss.data as AssessmentDetail;
      setAssessment(assData);

      // 2. Fetch Enrollments
      const classId = assData.teaching_assignment.classroom_id;
      const resEnr = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classId}/enrollments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const jsonEnr = await resEnr.json();
      if (jsonEnr.status !== "success") throw new Error(jsonEnr.message);
      const enrData = jsonEnr.data as Enrollment[];
      setEnrollments(enrData);

      // 3. Fetch Existing Scores
      const resSco = await fetch(`${DEFAULTS.API_URL}/api/v1/assessments/${id}/scores`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const jsonSco = await resSco.json();
      const existingScores: Record<string, AssessmentScore> = {};
      if (jsonSco.status === "success" && jsonSco.data) {
        jsonSco.data.forEach((s: any) => {
          existingScores[s.student_id] = {
            student_id: s.student_id,
            score: s.score,
            notes: s.notes || "",
          };
        });
      }

      // 4. Initialize Scores state
      const initialScores: Record<string, AssessmentScore> = {};
      enrData.forEach((e) => {
        const sid = e.student.id;
        initialScores[sid] = existingScores[sid] || { student_id: sid, score: "", notes: "" };
      });
      setScores(initialScores);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleScoreChange = (studentId: string, field: "score" | "notes", value: string) => {
    setScores((prev) => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        [field]: value,
      },
    }));
  };

  const handleSaveAll = async () => {
    setSaving(true);
    try {
      const payload = Object.values(scores).map((s) => ({
        student_id: s.student_id,
        score: Number(s.score) || 0,
        notes: s.notes,
      }));

      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/assessments/${id}/scores`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ scores: payload }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setSnackbarMessage("Nilai berhasil disimpan!");
        setSnackbarSeverity("success");
        setSnackbarOpen(true);
      } else {
        setSnackbarMessage(json.message || "Gagal menyimpan nilai.");
        setSnackbarSeverity("error");
        setSnackbarOpen(true);
      }
    } catch (err: any) {
      setSnackbarMessage(err.message || "Gagal menyambung ke server.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Input Nilai Sumatif
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiFloppyDisk size="small" />}
          onClick={handleSaveAll}
          disabled={saving || loading}
        >
          {saving ? "Menyimpan..." : "Simpan Semua"}
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/evaluation/summative">Sumatif</Link>
        <Typography variant="body2">{assessment ? assessment.assessment_name : "Memuat..."}</Typography>
      </Breadcrumbs>

      {loading ? (
        <>
          <Card className="mb-6 p-4">
            <Grid container spacing={2}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Skeleton variant="text" width={100} />
                <Skeleton variant="text" width="60%" height={30} />
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <Skeleton variant="text" width={100} />
                <Skeleton variant="text" width="60%" height={30} />
              </Grid>
            </Grid>
          </Card>

          <TableContainer component={Card}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell className="w-12 text-center font-bold">No</TableCell>
                  <TableCell className="w-48 font-bold">NISN</TableCell>
                  <TableCell className="font-bold">Nama Siswa</TableCell>
                  <TableCell className="w-48 font-bold">Nilai Angka (0-100)</TableCell>
                  <TableCell className="font-bold">Catatan Umpan Balik</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {[1, 2, 3, 4, 5].map((item) => (
                  <TableRow key={item}>
                    <TableCell align="center">
                      <Skeleton variant="text" width={20} />
                    </TableCell>
                    <TableCell>
                      <Skeleton variant="text" width={100} />
                    </TableCell>
                    <TableCell>
                      <Skeleton variant="text" width="60%" />
                    </TableCell>
                    <TableCell>
                      <Skeleton variant="rectangular" width="100%" height={30} className="rounded-md" />
                    </TableCell>
                    <TableCell>
                      <Skeleton variant="rectangular" width="100%" height={30} className="rounded-md" />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      ) : error || !assessment ? (
        <Alert severity="error">{error || "Data asesmen tidak ditemukan."}</Alert>
      ) : (
        <>
          <Card className="mb-6 p-4">
            <Grid container spacing={2}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Typography variant="subtitle2" color="textSecondary">
                  Nama Asesmen
                </Typography>
                <Typography variant="body1" className="font-medium">
                  {assessment.assessment_name}
                </Typography>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <Typography variant="subtitle2" color="textSecondary">
                  Mata Pelajaran
                </Typography>
                <Typography variant="body1" className="font-medium">
                  {assessment.teaching_assignment?.subject?.subject_name}
                </Typography>
              </Grid>
            </Grid>
          </Card>

          <TableContainer component={Card}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell className="w-12 text-center font-bold">No</TableCell>
                  <TableCell className="w-48 font-bold">NISN</TableCell>
                  <TableCell className="font-bold">Nama Siswa</TableCell>
                  <TableCell className="w-48 font-bold">Nilai Angka (0-100)</TableCell>
                  <TableCell className="font-bold">Catatan Umpan Balik</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {enrollments.length > 0 ? (
                  enrollments.map((e, idx) => {
                    const s = scores[e.student.id] || { score: "", notes: "" };
                    return (
                      <TableRow key={e.id} hover>
                        <TableCell align="center">{idx + 1}</TableCell>
                        <TableCell>{e.student.nisn}</TableCell>
                        <TableCell className="font-medium">{e.student.full_name}</TableCell>
                        <TableCell>
                          <TextField
                            type="number"
                            size="small"
                            fullWidth
                            aria-label={`Nilai angka sumatif untuk ${e.student.full_name}`}
                            value={s.score}
                            onChange={(ev) => handleScoreChange(e.student.id, "score", ev.target.value)}
                            slotProps={{ htmlInput: { min: 0, max: 100 } }}
                          />
                        </TableCell>
                        <TableCell>
                          <TextField
                            size="small"
                            fullWidth
                            placeholder="Catatan..."
                            aria-label={`Catatan umpan balik sumatif untuk ${e.student.full_name}`}
                            value={s.notes}
                            onChange={(ev) => handleScoreChange(e.student.id, "notes", ev.target.value)}
                          />
                        </TableCell>
                      </TableRow>
                    );
                  })
                ) : (
                  <TableRow>
                    <TableCell colSpan={5} align="center" className="py-10">
                      Tidak ada siswa yang terdaftar di kelas ini.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbarOpen(false)}
          severity={snackbarSeverity}
          sx={{ width: "100%", borderRadius: "16px", fontWeight: "bold" }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
}
