import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import SparklesIcon from "@mui/icons-material/AutoAwesome";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CloseIcon from "@mui/icons-material/Close";
import EditIcon from "@mui/icons-material/Edit";
import PrintIcon from "@mui/icons-material/Print";
import SaveIcon from "@mui/icons-material/Save";
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
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import { useConfirm } from "@/hooks/use-confirm";

interface Classroom {
  id: string;
  name: string;
}

interface TeachingAssignment {
  id: string;
  subject_id: string;
  subject: { subject_name: string };
  teacher: { full_name: string };
}

interface Student {
  full_name: string;
  nisn: string;
}

interface ReportScore {
  id?: string;
  subject_id: string;
  final_score: number;
  competency_achieved: string;
  competency_needs_improvement: string;
  subject?: { subject_name: string };
}

interface ReportP5 {
  theme: string;
  description: string;
  predicate: string;
}

interface ReportDeepLearning {
  aspect: string;
  observation_notes: string;
}

interface ReportExtracurricular {
  activity_name: string;
  predicate: string;
  description: string;
}

interface ReportAttendance {
  sick: number;
  permission: number;
  unexcused: number;
}

interface StudentReport {
  id: string;
  classroom_id: string;
  student_id: string;
  semester: string;
  homeroom_notes: string;
  student_reflection: string;
  academic_narrative_ai: string;
  character_narrative_ai: string;
  status: string;
  is_finalized: boolean;
  student: Student;
  scores?: ReportScore[];
  p5?: ReportP5[];
  deep_learning?: ReportDeepLearning[];
  extracurriculars?: ReportExtracurricular[];
  attendance?: ReportAttendance;
}

export default function GradebookScoresPage() {
  const confirm = useConfirm();
  const navigate = useNavigate();
  const token = localStorage.getItem("accessToken");

  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [selectedClassroom, setSelectedClassroom] = useState<string>("");
  const [semester, setSemester] = useState<string>("Ganjil");

  const [reports, setReports] = useState<StudentReport[]>([]);
  const [assignments, setAssignments] = useState<TeachingAssignment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Manage Report Drawer/Dialog
  const [selectedReport, setSelectedReport] = useState<StudentReport | null>(null);
  const [openManageDialog, setOpenManageDialog] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  // Form States for Modal
  const [subjectScores, setSubjectScores] = useState<{ [subjectId: string]: ReportScore }>({});
  const [p5Theme, setP5Theme] = useState("Kewirausahaan");
  const [p5Desc, setP5Desc] = useState("");
  const [p5Pred, setP5Pred] = useState("Sangat Berkembang");
  const [extraName, setExtraName] = useState("");
  const [extraPred, setExtraPred] = useState("A");
  const [extraDesc, setExtraDesc] = useState("");
  const [sick, setSick] = useState<number>(0);
  const [perm, setPerm] = useState<number>(0);
  const [alpa, setAlpa] = useState<number>(0);
  const [homeroomNotes, setHomeroomNotes] = useState("");
  const [studentReflect, setStudentReflect] = useState("");
  const [dlAspect, setDlAspect] = useState("Gaya Belajar");

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "gradebook_scores", data: reports, defaultLimit: 10 });
  const [dlNotes, setDlNotes] = useState("");

  const [saving, setSaving] = useState(false);
  const [dialogError, setDialogError] = useState<string | null>(null);
  const [generatingAIId, setGeneratingAIId] = useState<string | null>(null);

  // Fetch classrooms on load
  useEffect(() => {
    const fetchClassrooms = async () => {
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success" && json.data) {
          setClassrooms(json.data);
          if (json.data.length > 0) {
            setSelectedClassroom(json.data[0].id);
          }
        }
      } catch (err: any) {
        setError("Gagal memuat data kelas.");
      }
    };
    fetchClassrooms();
  }, [token]);

  // Fetch reports & classroom assignments when selection changes
  const fetchReportsAndAssignments = async () => {
    if (!selectedClassroom) return;
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch reports
      const resRep = await fetch(
        `${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroom}/reports?semester=${semester}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      const jsonRep = await resRep.json();
      if (jsonRep.status === "success") {
        setReports(jsonRep.data || []);
      } else {
        setReports([]);
      }

      // 2. Fetch assignments
      const resAssign = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroom}/assignments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const jsonAssign = await resAssign.json();
      if (jsonAssign.status === "success") {
        setAssignments(jsonAssign.data || []);
      }
    } catch (err: any) {
      setError("Gagal menarik data rapor atau mata pelajaran.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReportsAndAssignments();
  }, [selectedClassroom, semester, token]);

  const handleGenerateClassReports = async () => {
    if (!selectedClassroom) return;
    setLoading(true);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroom}/reports/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ semester }),
      });
      const json = await res.json();
      if (json.status === "success" || res.ok) {
        fetchReportsAndAssignments();
      } else {
        setError(json.message || "Gagal menginisialisasi rapor kelas.");
      }
    } catch (err: any) {
      setError("Gagal menyambung ke server.");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAI = async (reportId: string) => {
    setGeneratingAIId(reportId);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${reportId}/generate-ai-description`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchReportsAndAssignments();
      } else {
        alert("Gagal menyusun Narasi AI: " + json.message);
      }
    } catch (err: any) {
      alert("Kesalahan jaringan: " + err.message);
    } finally {
      setGeneratingAIId(null);
    }
  };

  const handleFinalize = async (reportId: string) => {
    const ok = await confirm({
      title: "Finalisasi Rapor",
      message: "Apakah Anda yakin ingin memfinalisasi rapor ini? Rapor yang difinalisasi tidak dapat diubah kembali.",
      confirmText: "Finalisasi",
      cancelText: "Batal",
    });
    if (!ok) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${reportId}/finalize`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchReportsAndAssignments();
      } else {
        alert("Gagal finalisasi: " + json.message);
      }
    } catch (err: any) {
      alert("Kesalahan jaringan: " + err.message);
    }
  };

  // Open Manage dialog & initialize form fields
  const handleOpenManage = (rep: StudentReport) => {
    setSelectedReport(rep);
    setDialogError(null);

    // Load Subject scores
    const initialScores: { [subId: string]: ReportScore } = {};
    assignments.forEach((a) => {
      const existing = rep.scores?.find((s) => s.subject_id === a.subject_id);
      initialScores[a.subject_id] = {
        subject_id: a.subject_id,
        final_score: existing?.final_score || 0,
        competency_achieved: existing?.competency_achieved || "",
        competency_needs_improvement: existing?.competency_needs_improvement || "",
      };
    });
    setSubjectScores(initialScores);

    // Load P5
    const existingP5 = rep.p5?.[0];
    setP5Theme(existingP5?.theme || "Kewirausahaan");
    setP5Desc(existingP5?.description || "");
    setP5Pred(existingP5?.predicate || "Sangat Berkembang");

    // Load Extra
    const existingExtra = rep.extracurriculars?.[0];
    setExtraName(existingExtra?.activity_name || "");
    setExtraPred(existingExtra?.predicate || "A");
    setExtraDesc(existingExtra?.description || "");

    // Load Attendance
    setSick(rep.attendance?.sick || 0);
    setPerm(rep.attendance?.permission || 0);
    setAlpa(rep.attendance?.unexcused || 0);

    // Load Notes
    setHomeroomNotes(rep.homeroom_notes || "");
    setStudentReflect(rep.student_reflection || "");

    // Load DL
    const existingDL = rep.deep_learning?.[0];
    setDlAspect(existingDL?.aspect || "Gaya Belajar");
    setDlNotes(existingDL?.observation_notes || "");

    setActiveTab(0);
    setOpenManageDialog(true);
  };

  const handleSaveTab = async () => {
    if (!selectedReport) return;
    setSaving(true);
    setDialogError(null);
    try {
      const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      };

      if (activeTab === 0) {
        // Save Mapel Scores
        for (const subId of Object.keys(subjectScores)) {
          const sc = subjectScores[subId];
          const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${selectedReport.id}/scores`, {
            method: "PUT",
            headers,
            body: JSON.stringify(sc),
          });
          if (!res.ok) {
            const json = await res.json();
            throw new Error(`Gagal menyimpan nilai mapel: ${json.message}`);
          }
        }
      } else if (activeTab === 1) {
        // Save P5
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${selectedReport.id}/p5`, {
          method: "PUT",
          headers,
          body: JSON.stringify({
            theme: p5Theme,
            description: p5Desc,
            predicate: p5Pred,
          }),
        });
        if (!res.ok) {
          const json = await res.json();
          throw new Error(`Gagal menyimpan P5: ${json.message}`);
        }
      } else if (activeTab === 2) {
        // Save Extra
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${selectedReport.id}/extracurricular`, {
          method: "PUT",
          headers,
          body: JSON.stringify({
            activity_name: extraName,
            predicate: extraPred,
            description: extraDesc,
          }),
        });
        if (!res.ok) {
          const json = await res.json();
          throw new Error(`Gagal menyimpan ekstrakurikuler: ${json.message}`);
        }
      } else if (activeTab === 3) {
        // Save Reflection & DL
        const resNotes = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${selectedReport.id}/notes`, {
          method: "PUT",
          headers,
          body: JSON.stringify({
            homeroom_notes: homeroomNotes,
            student_reflection: studentReflect,
          }),
        });
        if (!resNotes.ok) {
          const json = await resNotes.json();
          throw new Error(`Gagal menyimpan Catatan: ${json.message}`);
        }

        const resDL = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${selectedReport.id}/deep-learning`, {
          method: "PUT",
          headers,
          body: JSON.stringify({
            aspect: dlAspect,
            observation_notes: dlNotes,
          }),
        });
        if (!resDL.ok) {
          const json = await resDL.json();
          throw new Error(`Gagal menyimpan refleksi mendalam: ${json.message}`);
        }
      } else if (activeTab === 4) {
        // Save Attendance
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${selectedReport.id}/attendance`, {
          method: "PUT",
          headers,
          body: JSON.stringify({
            sick: Number(sick),
            permission: Number(perm),
            unexcused: Number(alpa),
          }),
        });
        if (!res.ok) {
          const json = await res.json();
          throw new Error(`Gagal menyimpan absensi: ${json.message}`);
        }
      }

      fetchReportsAndAssignments();
      alert("Bagian data rapor berhasil disimpan!");
    } catch (err: any) {
      setDialogError(err.message || "Gagal menyimpan data.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box className="pb-10">
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Buku Rapor Merdeka
        </Typography>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Typography variant="body2">Laporan</Typography>
        <Typography variant="body2">Buku Rapor</Typography>
      </Breadcrumbs>

      {/* FILTER PANEL */}
      <Card className="shadow-darker-xs mb-6 border-none">
        <CardContent className="p-5">
          <Grid container spacing={3} alignItems="center">
            <Grid size={{ xs: 12, sm: 5 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Kelas / Rombel</InputLabel>
                <Select
                  value={selectedClassroom}
                  label="Kelas / Rombel"
                  onChange={(e) => setSelectedClassroom(e.target.value)}
                >
                  {classrooms.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      Kelas {c.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Semester</InputLabel>
                <Select value={semester} label="Semester" onChange={(e) => setSemester(e.target.value)}>
                  <MenuItem value="Ganjil">Semester Ganjil</MenuItem>
                  <MenuItem value="Genap">Semester Genap</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, sm: 3 }} className="flex justify-end">
              <Button
                fullWidth
                variant="contained"
                onClick={fetchReportsAndAssignments}
                disabled={loading || !selectedClassroom}
              >
                Tarik Rapor
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4 rounded-xl">
          {error}
        </Alert>
      )}

      {/* BODY REPORTS */}
      {loading ? (
        <Box className="flex justify-center py-20">
          <CircularProgress />
        </Box>
      ) : reports.length > 0 ? (
        <TableContainer component={Card} className="shadow-darker-xs border-none">
          <Table>
            <TableHead className="bg-action-hover">
              <TableRow>
                <TableCell className="font-bold" sortDirection={sortBy === "student.full_name" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "student.full_name"}
                    direction={sortBy === "student.full_name" ? sortDir : "asc"}
                    onClick={() => handleSort("student.full_name")}
                  >
                    Siswa
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-bold" sortDirection={sortBy === "status" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "status"}
                    direction={sortBy === "status" ? sortDir : "asc"}
                    onClick={() => handleSort("status")}
                  >
                    Status Rapor
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-bold">Narasi Akademik AI</TableCell>
                <TableCell className="font-bold">Narasi Karakter AI</TableCell>
                <TableCell className="font-bold" align="center">
                  Aksi & Pengelolaan
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedData.map((report) => {
                const hasAcademicAI = report.academic_narrative_ai?.trim().length > 0;
                const hasCharacterAI = report.character_narrative_ai?.trim().length > 0;

                return (
                  <TableRow key={report.id} hover>
                    <TableCell>
                      <Typography className="font-bold text-slate-800">{report.student?.full_name}</Typography>
                      <Typography variant="caption" className="font-mono text-slate-400">
                        NISN: {report.student?.nisn}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={report.status}
                        size="small"
                        color={report.status === "FINAL" ? "success" : "warning"}
                        icon={report.status === "FINAL" ? <CheckCircleIcon /> : undefined}
                        className="rounded-xl font-bold"
                      />
                    </TableCell>
                    <TableCell>
                      {hasAcademicAI ? (
                        <Typography variant="body2" className="line-clamp-2 max-w-xs text-slate-600 italic">
                          {report.academic_narrative_ai}
                        </Typography>
                      ) : (
                        <Typography variant="body2" className="text-slate-400">
                          Belum digenerasi
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell>
                      {hasCharacterAI ? (
                        <Typography variant="body2" className="line-clamp-2 max-w-xs text-slate-600 italic">
                          {report.character_narrative_ai}
                        </Typography>
                      ) : (
                        <Typography variant="body2" className="text-slate-400">
                          Belum digenerasi
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell align="center">
                      <Box className="flex items-center justify-center gap-2">
                        <Button
                          variant="outlined"
                          size="small"
                          startIcon={<EditIcon fontSize="small" />}
                          onClick={() => handleOpenManage(report)}
                          className="rounded-xl"
                        >
                          Kelola
                        </Button>
                        <Button
                          variant="contained"
                          color="secondary"
                          size="small"
                          disabled={generatingAIId !== null || report.is_finalized}
                          startIcon={
                            generatingAIId === report.id ? (
                              <CircularProgress size={14} color="inherit" />
                            ) : (
                              <SparklesIcon fontSize="small" />
                            )
                          }
                          onClick={() => handleGenerateAI(report.id)}
                          className="rounded-xl text-xs font-bold shadow-sm"
                        >
                          AI Narasi
                        </Button>
                        {!report.is_finalized ? (
                          <Button
                            variant="contained"
                            color="success"
                            size="small"
                            onClick={() => handleFinalize(report.id)}
                            className="rounded-xl text-xs font-bold shadow-sm"
                          >
                            Finalisasi
                          </Button>
                        ) : (
                          <Button
                            variant="contained"
                            color="info"
                            size="small"
                            startIcon={<PrintIcon fontSize="small" />}
                            onClick={() => navigate(`/reports/gradebook/print?id=${report.id}`)}
                            className="rounded-xl text-xs font-bold shadow-sm"
                          >
                            Cetak
                          </Button>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
          <TablePagination
            component="div"
            count={total}
            page={page - 1}
            onPageChange={(_, newPage) => handlePageChange(newPage + 1)}
            rowsPerPage={limit}
            onRowsPerPageChange={(e) => handleLimitChange(parseInt(e.target.value, 10))}
            labelRowsPerPage="Baris per halaman:"
          />
        </TableContainer>
      ) : (
        <Paper className="rounded-[32px] border border-dashed border-slate-200 bg-white p-12 text-center">
          <Box className="flex flex-col items-center justify-center gap-4">
            <Typography variant="h5" className="font-black text-slate-700">
              Belum ada draft Rapor di Kelas ini
            </Typography>
            <Typography variant="body2" className="max-w-md text-slate-400">
              Draft Buku Rapor untuk semester ini belum dibuat. Klik tombol di bawah untuk menginisialisasi data rapor
              murid secara otomatis berdasarkan data siswa terdaftar.
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleGenerateClassReports}
              className="mt-2 rounded-2xl px-8 py-3 font-bold shadow-lg"
              disabled={!selectedClassroom}
            >
              Inisialisasi Rapor Kelas
            </Button>
          </Box>
        </Paper>
      )}

      {/* MANAGE REPORT DIALOG */}
      <Dialog
        open={openManageDialog}
        onClose={() => setOpenManageDialog(false)}
        maxWidth="md"
        fullWidth
        scroll="paper"
        PaperProps={{
          className: "rounded-[32px] p-2",
        }}
      >
        <DialogTitle className="flex items-center justify-between border-b px-6 pb-4">
          <Box>
            <Typography variant="h4" className="mb-0 font-black text-slate-800">
              Kelola Rapor Murid
            </Typography>
            <Typography variant="subtitle2" className="text-primary font-bold">
              {selectedReport?.student?.full_name} ({selectedReport?.student?.nisn})
            </Typography>
          </Box>
          <IconButton onClick={() => setOpenManageDialog(false)}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent className="px-6 py-4">
          {dialogError && (
            <Alert severity="error" className="mb-4 rounded-xl">
              {dialogError}
            </Alert>
          )}

          {selectedReport?.is_finalized && (
            <Alert severity="info" className="mb-4 rounded-xl font-bold">
              Rapor ini sudah difinalisasi. Anda hanya dapat melihat data saja.
            </Alert>
          )}

          <Tabs
            value={activeTab}
            onChange={(e, v) => setActiveTab(v)}
            variant="scrollable"
            scrollButtons="auto"
            className="mb-6 border-b"
          >
            <Tab label="1. Nilai Mapel" className="text-sm font-bold" />
            <Tab label="2. Projek P5" className="text-sm font-bold" />
            <Tab label="3. Ekstrakurikuler" className="text-sm font-bold" />
            <Tab label="4. Catatan & Refleksi" className="text-sm font-bold" />
            <Tab label="5. Kehadiran" className="text-sm font-bold" />
          </Tabs>

          <Box className="min-h-[300px] py-2">
            {/* TAB 0: scores */}
            {activeTab === 0 && (
              <Box className="space-y-4">
                <Typography variant="h6" className="mb-4 font-bold text-slate-800">
                  Input Nilai Hasil Belajar (Merdeka)
                </Typography>
                {assignments.length === 0 ? (
                  <Typography className="text-slate-400">
                    Tidak ada mata pelajaran yang diampu di rombel ini.
                  </Typography>
                ) : (
                  assignments.map((a) => {
                    const currentScore: ReportScore = subjectScores[a.subject_id] || {
                      subject_id: a.subject_id,
                      final_score: 0,
                      competency_achieved: "",
                      competency_needs_improvement: "",
                    };

                    return (
                      <Paper key={a.id} className="mb-4 rounded-2xl border border-slate-100 bg-slate-50/30 p-4">
                        <Grid container spacing={3} alignItems="center">
                          <Grid size={{ xs: 12, md: 4 }}>
                            <Typography className="text-base font-black text-slate-800">
                              {a.subject?.subject_name}
                            </Typography>
                            <Typography variant="caption" className="text-slate-400">
                              Pengampu: {a.teacher?.full_name}
                            </Typography>
                          </Grid>
                          <Grid size={{ xs: 12, md: 2 }}>
                            <TextField
                              fullWidth
                              size="small"
                              type="number"
                              label="Nilai Akhir"
                              disabled={selectedReport?.is_finalized}
                              value={currentScore.final_score}
                              onChange={(e) =>
                                setSubjectScores({
                                  ...subjectScores,
                                  [a.subject_id]: {
                                    ...currentScore,
                                    final_score: Number(e.target.value),
                                  },
                                })
                              }
                              inputProps={{ min: 0, max: 100 }}
                            />
                          </Grid>
                          <Grid size={{ xs: 12, md: 3 }}>
                            <TextField
                              fullWidth
                              size="small"
                              label="Kompetensi Tercapai"
                              disabled={selectedReport?.is_finalized}
                              value={currentScore.competency_achieved}
                              onChange={(e) =>
                                setSubjectScores({
                                  ...subjectScores,
                                  [a.subject_id]: {
                                    ...currentScore,
                                    competency_achieved: e.target.value,
                                  },
                                })
                              }
                            />
                          </Grid>
                          <Grid size={{ xs: 12, md: 3 }}>
                            <TextField
                              fullWidth
                              size="small"
                              label="Perlu Peningkatan"
                              disabled={selectedReport?.is_finalized}
                              value={currentScore.competency_needs_improvement}
                              onChange={(e) =>
                                setSubjectScores({
                                  ...subjectScores,
                                  [a.subject_id]: {
                                    ...currentScore,
                                    competency_needs_improvement: e.target.value,
                                  },
                                })
                              }
                            />
                          </Grid>
                        </Grid>
                      </Paper>
                    );
                  })
                )}
              </Box>
            )}

            {/* TAB 1: P5 */}
            {activeTab === 1 && (
              <Grid container spacing={3}>
                <Grid size={{ xs: 12 }}>
                  <Typography variant="h6" className="mb-2 font-bold text-slate-800">
                    Projek Penguatan Profil Pelajar Pancasila (P5)
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Tema P5</InputLabel>
                    <Select
                      value={p5Theme}
                      label="Tema P5"
                      disabled={selectedReport?.is_finalized}
                      onChange={(e) => setP5Theme(e.target.value)}
                    >
                      <MenuItem value="Kewirausahaan">Kewirausahaan</MenuItem>
                      <MenuItem value="Gaya Hidup Berkelanjutan">Gaya Hidup Berkelanjutan</MenuItem>
                      <MenuItem value="Kearifan Lokal">Kearifan Lokal</MenuItem>
                      <MenuItem value="Bhinneka Tunggal Ika">Bhinneka Tunggal Ika</MenuItem>
                      <MenuItem value="Bangunlah Jiwa dan Raganya">Bangunlah Jiwa dan Raganya</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Predikat Capaian</InputLabel>
                    <Select
                      value={p5Pred}
                      label="Predikat Capaian"
                      disabled={selectedReport?.is_finalized}
                      onChange={(e) => setP5Pred(e.target.value)}
                    >
                      <MenuItem value="Belum Berkembang">Belum Berkembang</MenuItem>
                      <MenuItem value="Mulai Berkembang">Mulai Berkembang</MenuItem>
                      <MenuItem value="Berkembang Sesuai Harapan">Berkembang Sesuai Harapan</MenuItem>
                      <MenuItem value="Sangat Berkembang">Sangat Berkembang</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    label="Deskripsi Proses & Capaian Projek"
                    disabled={selectedReport?.is_finalized}
                    value={p5Desc}
                    onChange={(e) => setP5Desc(e.target.value)}
                    placeholder="Tulis detail proyek serta bagaimana murid mengekspresikan nilai karakter pancasila..."
                  />
                </Grid>
              </Grid>
            )}

            {/* TAB 2: Extracurricular */}
            {activeTab === 2 && (
              <Grid container spacing={3}>
                <Grid size={{ xs: 12 }}>
                  <Typography variant="h6" className="mb-2 font-bold text-slate-800">
                    Kegiatan Ekstrakurikuler
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 8 }}>
                  <TextField
                    fullWidth
                    size="small"
                    label="Nama Kegiatan"
                    disabled={selectedReport?.is_finalized}
                    value={extraName}
                    onChange={(e) => setExtraName(e.target.value)}
                    placeholder="Contoh: Pramuka, UKS, Palang Merah Remaja"
                  />
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Predikat</InputLabel>
                    <Select
                      value={extraPred}
                      label="Predikat"
                      disabled={selectedReport?.is_finalized}
                      onChange={(e) => setExtraPred(e.target.value)}
                    >
                      <MenuItem value="Sangat Baik">Sangat Baik</MenuItem>
                      <MenuItem value="Baik">Baik</MenuItem>
                      <MenuItem value="Cukup">Cukup</MenuItem>
                      <MenuItem value="Kurang">Kurang</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Deskripsi Keterangan"
                    disabled={selectedReport?.is_finalized}
                    value={extraDesc}
                    onChange={(e) => setExtraDesc(e.target.value)}
                    placeholder="Mampu mempraktikkan keterampilan dasar kepanduan dengan sangat baik..."
                  />
                </Grid>
              </Grid>
            )}

            {/* TAB 3: Reflection & Notes */}
            {activeTab === 3 && (
              <Grid container spacing={3}>
                <Grid size={{ xs: 12 }}>
                  <Typography variant="h6" className="mb-2 font-bold text-slate-800">
                    Catatan Wali Kelas & Refleksi Siswa
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Catatan Wali Kelas"
                    disabled={selectedReport?.is_finalized}
                    value={homeroomNotes}
                    onChange={(e) => setHomeroomNotes(e.target.value)}
                    placeholder="Catatan perkembangan belajar siswa untuk dibaca orang tua murid..."
                  />
                </Grid>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Refleksi Diri Murid"
                    disabled={selectedReport?.is_finalized}
                    value={studentReflect}
                    onChange={(e) => setStudentReflect(e.target.value)}
                    placeholder="Pandangan/refleksi anak terhadap keberhasilan belajarnya sendiri..."
                  />
                </Grid>

                <Grid size={{ xs: 12 }}>
                  <Divider className="my-2" />
                  <Typography variant="h6" className="mt-2 mb-2 font-bold text-slate-800">
                    Refleksi Mendalam (Deep Learning)
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Aspek Refleksi</InputLabel>
                    <Select
                      value={dlAspect}
                      label="Aspek Refleksi"
                      disabled={selectedReport?.is_finalized}
                      onChange={(e) => setDlAspect(e.target.value)}
                    >
                      <MenuItem value="Gaya Belajar">Gaya Belajar</MenuItem>
                      <MenuItem value="Tingkat Pemecahan Masalah">Pemecahan Masalah</MenuItem>
                      <MenuItem value="Kreativitas & Seni">Kreativitas & Seni</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid size={{ xs: 12, md: 8 }}>
                  <TextField
                    fullWidth
                    size="small"
                    label="Catatan Observasi Khusus"
                    disabled={selectedReport?.is_finalized}
                    value={dlNotes}
                    onChange={(e) => setDlNotes(e.target.value)}
                    placeholder="Observasi mendalam mengenai minat dan cara adaptasi belajar..."
                  />
                </Grid>
              </Grid>
            )}

            {/* TAB 4: Attendance */}
            {activeTab === 4 && (
              <Grid container spacing={3}>
                <Grid size={{ xs: 12 }}>
                  <Typography variant="h6" className="mb-2 font-bold text-slate-800">
                    Kehadiran / Presensi Siswa (Semester ini)
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <TextField
                    fullWidth
                    type="number"
                    size="small"
                    label="Sakit (hari)"
                    disabled={selectedReport?.is_finalized}
                    value={sick}
                    onChange={(e) => setSick(Number(e.target.value))}
                    inputProps={{ min: 0 }}
                  />
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <TextField
                    fullWidth
                    type="number"
                    size="small"
                    label="Izin (hari)"
                    disabled={selectedReport?.is_finalized}
                    value={perm}
                    onChange={(e) => setPerm(Number(e.target.value))}
                    inputProps={{ min: 0 }}
                  />
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <TextField
                    fullWidth
                    type="number"
                    size="small"
                    label="Tanpa Keterangan / Alpa (hari)"
                    disabled={selectedReport?.is_finalized}
                    value={alpa}
                    onChange={(e) => setAlpa(Number(e.target.value))}
                    inputProps={{ min: 0 }}
                  />
                </Grid>
              </Grid>
            )}
          </Box>
        </DialogContent>
        <DialogActions className="justify-between border-t p-4 px-6">
          <Button variant="text" color="inherit" onClick={() => setOpenManageDialog(false)} className="font-bold">
            Tutup
          </Button>

          {!selectedReport?.is_finalized && (
            <Button
              variant="contained"
              color="primary"
              startIcon={saving ? <CircularProgress size={16} color="inherit" /> : <SaveIcon />}
              onClick={handleSaveTab}
              disabled={saving}
              className="rounded-xl px-6 py-2 font-bold shadow-md"
            >
              Simpan Bagian Ini
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
}
