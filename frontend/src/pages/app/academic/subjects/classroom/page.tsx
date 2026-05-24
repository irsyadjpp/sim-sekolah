import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as Yup from "yup";

import {
  Add as AddIcon,
  AssignmentInd as AssignmentIcon,
  Delete as DeleteIcon,
  People as PeopleIcon,
} from "@mui/icons-material";
import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControl,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import { useConfirm } from "@/hooks/use-confirm";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

interface Classroom {
  id: string;
  classroom_name: string;
  school_id: string;
  school: { school_name: string };
  academic_year_id: string;
  academic_year: { year_name: string; semester: string };
  grade_id: string;
  grade: { grade_name: string };
  phase_id: string;
  phase: { phase_name: string };
  homeroom_teacher_id: string | null;
  homeroom: { full_name: string } | null;
  max_quota: number;
  class_characteristics: string;
}

export default function ClassroomsPage() {
  const confirm = useConfirm();
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  // Dialog state
  const [open, setOpen] = useState(false);
  const [editingClassroom, setEditingClassroom] = useState<any | null>(null);

  // Master data for dropdowns
  const [schools, setSchools] = useState<any[]>([]);
  const [academicYears, setAcademicYears] = useState<any[]>([]);
  const [grades, setGrades] = useState<any[]>([]);
  const [phases, setPhases] = useState<any[]>([]);
  const [teachers, setTeachers] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [students, setStudents] = useState<any[]>([]);

  // Teaching Assignment Dialog States
  const [openAssignmentDialog, setOpenAssignmentDialog] = useState(false);
  const [selectedClassroomForAssignment, setSelectedClassroomForAssignment] = useState<Classroom | null>(null);
  const [assignments, setAssignments] = useState<any[]>([]);
  const [newAssignmentSubject, setNewAssignmentSubject] = useState("");
  const [newAssignmentTeacher, setNewAssignmentTeacher] = useState("");

  // Enrollment Dialog States
  const [openEnrollmentDialog, setOpenEnrollmentDialog] = useState(false);
  const [selectedClassroomForEnrollment, setSelectedClassroomForEnrollment] = useState<Classroom | null>(null);
  const [enrollments, setEnrollments] = useState<any[]>([]);
  const [newEnrollmentStudent, setNewEnrollmentStudent] = useState("");

  // Dialog-specific Alerts
  const [dialogError, setDialogError] = useState<string | null>(null);
  const [dialogSuccess, setDialogSuccess] = useState<string | null>(null);
  const [dialogLoading, setDialogLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const [classroomRes, schoolRes, ayRes, gradeRes, phaseRes, teacherRes, subjectRes, studentRes] =
        await Promise.all([
          fetch(`${DEFAULTS.API_URL}/api/v1/classrooms?limit=10000`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/schools`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/academic-years`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/grades`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/phases`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/teachers`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/subjects`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/students?limit=200`, { headers: { Authorization: `Bearer ${token}` } }),
        ]);

      const [cJson, sJson, ayJson, gJson, pJson, tJson, subJson, stuJson] = await Promise.all([
        classroomRes.json(),
        schoolRes.json(),
        ayRes.json(),
        gradeRes.json(),
        phaseRes.json(),
        teacherRes.json(),
        subjectRes.json(),
        studentRes.json(),
      ]);

      if (cJson.status === "success") setClassrooms(cJson.data || []);
      if (sJson.status === "success") setSchools(sJson.data || []);
      if (ayJson.status === "success") setAcademicYears(ayJson.data || []);
      if (gJson.status === "success") setGrades(gJson.data || []);
      if (pJson.status === "success") setPhases(pJson.data || []);
      if (tJson.status === "success") setTeachers(tJson.data || []);
      if (subJson.status === "success") setSubjects(subJson.data || []);
      if (stuJson.status === "success") setStudents(stuJson.data || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formik = useFormik({
    initialValues: {
      school_id: editingClassroom?.school_id || schools[0]?.id || "",
      academic_year_id: editingClassroom?.academic_year_id || academicYears.find((ay) => ay.is_active)?.id || "",
      grade_id: editingClassroom?.grade_id || "",
      phase_id: editingClassroom?.phase_id || "",
      classroom_name: editingClassroom?.classroom_name || "",
      homeroom_teacher_id: editingClassroom?.homeroom_teacher_id || "",
      max_quota: editingClassroom?.max_quota || 28,
      class_characteristics: editingClassroom?.class_characteristics || "",
    },
    enableReinitialize: true,
    validationSchema: Yup.object({
      school_id: Yup.string().required("Sekolah wajib dipilih"),
      academic_year_id: Yup.string().required("Tahun ajaran wajib dipilih"),
      grade_id: Yup.string().required("Tingkat kelas wajib dipilih"),
      phase_id: Yup.string().required("Fase wajib dipilih"),
      classroom_name: Yup.string().required("Nama kelas wajib diisi"),
      max_quota: Yup.number().required("Kuota wajib diisi").min(1, "Minimal 1 siswa").max(100, "Maksimal 100 siswa"),
    }),
    onSubmit: async (values) => {
      const token = localStorage.getItem("accessToken");
      const url = editingClassroom
        ? `${DEFAULTS.API_URL}/api/v1/classrooms/${editingClassroom.id}`
        : `${DEFAULTS.API_URL}/api/v1/classrooms`;

      const method = editingClassroom ? "PUT" : "POST";

      try {
        const res = await fetch(url, {
          method,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(values),
        });
        const json = await res.json();
        if (json.status === "success") {
          setOpen(false);
          fetchData();
        } else {
          alert(json.message);
        }
      } catch (err: any) {
        alert(err.message);
      }
    },
  });

  const handleDelete = async (id: string) => {
    const ok = await confirm({
      title: "Hapus Rombongan Belajar",
      message: "Yakin ingin menghapus rombel ini?",
      confirmText: "Hapus",
      cancelText: "Batal",
    });
    if (!ok) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchData();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  // --- TEACHING ASSIGNMENTS CRUD HANDLERS ---
  const fetchAssignments = async (classroomId: string) => {
    setDialogLoading(true);
    setDialogError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classroomId}/assignments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setAssignments(json.data || []);
      } else {
        setDialogError(json.message || "Gagal memuat penugasan guru.");
      }
    } catch (err) {
      setDialogError("Koneksi gagal saat memuat penugasan.");
    } finally {
      setDialogLoading(false);
    }
  };

  const handleOpenAssignments = (c: Classroom) => {
    setSelectedClassroomForAssignment(c);
    setAssignments([]);
    setNewAssignmentSubject("");
    setNewAssignmentTeacher("");
    setDialogError(null);
    setDialogSuccess(null);
    setOpenAssignmentDialog(true);
    fetchAssignments(c.id);
  };

  const {
    paginatedData: paginatedAssignments,
    page: assignPage,
    limit: assignLimit,
    total: assignTotal,
    handlePageChange: setAssignPage,
    handleLimitChange: setAssignLimit,
  } = useClientTable({ key: "assignments", data: assignments, defaultLimit: 5 });

  const handleAddAssignment = async () => {
    if (!selectedClassroomForAssignment || !newAssignmentSubject || !newAssignmentTeacher) return;
    setDialogLoading(true);
    setDialogError(null);
    setDialogSuccess(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroomForAssignment.id}/assignments`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            classroom_id: selectedClassroomForAssignment.id,
            teacher_id: newAssignmentTeacher,
            subject_id: newAssignmentSubject,
          }),
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        setDialogSuccess("Penugasan guru berhasil ditambahkan.");
        setNewAssignmentSubject("");
        setNewAssignmentTeacher("");
        fetchAssignments(selectedClassroomForAssignment.id);
      } else {
        setDialogError(json.message || "Gagal menambah penugasan.");
      }
    } catch (err) {
      setDialogError("Koneksi gagal saat membuat penugasan.");
    } finally {
      setDialogLoading(false);
    }
  };

  const handleDeleteAssignment = async (id: string) => {
    if (!selectedClassroomForAssignment) return;
    setDialogLoading(true);
    setDialogError(null);
    setDialogSuccess(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroomForAssignment.id}/assignments/${id}`,
        {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        setDialogSuccess("Penugasan berhasil dihapus.");
        fetchAssignments(selectedClassroomForAssignment.id);
      } else {
        setDialogError(json.message || "Gagal menghapus penugasan.");
      }
    } catch (err) {
      setDialogError("Koneksi gagal saat menghapus penugasan.");
    } finally {
      setDialogLoading(false);
    }
  };

  // --- ENROLLMENTS CRUD HANDLERS ---
  const fetchEnrollments = async (classroomId: string) => {
    setDialogLoading(true);
    setDialogError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classroomId}/enrollments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setEnrollments(json.data || []);
      } else {
        setDialogError(json.message || "Gagal memuat daftar anggota kelas.");
      }
    } catch (err) {
      setDialogError("Koneksi gagal saat memuat anggota kelas.");
    } finally {
      setDialogLoading(false);
    }
  };

  const handleOpenEnrollments = (c: Classroom) => {
    setSelectedClassroomForEnrollment(c);
    setEnrollments([]);
    setNewEnrollmentStudent("");
    setDialogError(null);
    setDialogSuccess(null);
    setOpenEnrollmentDialog(true);
    fetchEnrollments(c.id);
  };

  const {
    paginatedData: paginatedEnrollments,
    page: enrollPage,
    limit: enrollLimit,
    total: enrollTotal,
    handlePageChange: setEnrollPage,
    handleLimitChange: setEnrollLimit,
  } = useClientTable({ key: "enrollments", data: enrollments, defaultLimit: 10 });

  const handleEnrollStudent = async () => {
    if (!selectedClassroomForEnrollment || !newEnrollmentStudent) return;
    setDialogLoading(true);
    setDialogError(null);
    setDialogSuccess(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroomForEnrollment.id}/enrollments`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            student_id: newEnrollmentStudent,
          }),
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        setDialogSuccess("Siswa berhasil didaftarkan ke kelas.");
        setNewEnrollmentStudent("");
        fetchEnrollments(selectedClassroomForEnrollment.id);
      } else {
        setDialogError(json.message || "Gagal mendaftarkan siswa.");
      }
    } catch (err) {
      setDialogError("Koneksi gagal saat mendaftarkan siswa.");
    } finally {
      setDialogLoading(false);
    }
  };

  const handleUnenrollStudent = async (enrollmentId: string) => {
    if (!selectedClassroomForEnrollment) return;
    if (!window.confirm("Apakah Anda yakin ingin mengeluarkan siswa ini dari kelas?")) return;
    setDialogLoading(true);
    setDialogError(null);
    setDialogSuccess(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroomForEnrollment.id}/enrollments/${enrollmentId}`,
        {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        setDialogSuccess("Siswa berhasil dikeluarkan dari kelas.");
        fetchEnrollments(selectedClassroomForEnrollment.id);
      } else {
        setDialogError(json.message || "Gagal mengeluarkan siswa.");
      }
    } catch (err) {
      setDialogError("Koneksi gagal saat mengeluarkan siswa.");
    } finally {
      setDialogLoading(false);
    }
  };

  const filteredClassrooms = classrooms.filter(
    (c) =>
      c.classroom_name.toLowerCase().includes(search.toLowerCase()) ||
      c.grade.grade_name.toLowerCase().includes(search.toLowerCase()),
  );

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "classrooms", data: filteredClassrooms, defaultLimit: 10 });

  return (
    <Box className="pb-10">
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Rombongan Belajar (Rombel)
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<NiPlus size="small" />}
          onClick={() => {
            setEditingClassroom(null);
            setOpen(true);
          }}
          className="rounded-2xl px-6 py-3 font-black shadow-xl"
        >
          Tambah Rombel
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home" className="hover:text-primary no-underline transition-colors">
          Beranda
        </Link>
        <Link to="/academic" className="hover:text-primary no-underline transition-colors">
          Akademik
        </Link>
        <Link to="/academic/subjects" className="hover:text-primary no-underline transition-colors">
          Pelajaran
        </Link>
        <Typography variant="body2" className="text-text-secondary">
          Kelas
        </Typography>
      </Breadcrumbs>

      <Card className="mb-6 rounded-[32px] border-none bg-white shadow-xl">
        <CardContent className="p-4">
          <TextField
            fullWidth
            placeholder="Cari nama rombel atau tingkat kelas..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            size="small"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <NiSearch size="small" />
                </InputAdornment>
              ),
            }}
          />
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4 rounded-2xl">
          {error}
        </Alert>
      )}

      <TableContainer component={Card} className="overflow-hidden rounded-[40px] border-none bg-white p-4 shadow-2xl">
        <Table>
          <TableHead className="bg-slate-50">
            <TableRow>
              <TableCell
                className="font-black text-slate-700"
                sortDirection={sortBy === "classroom_name" ? sortDir : false}
              >
                <TableSortLabel
                  active={sortBy === "classroom_name"}
                  direction={sortBy === "classroom_name" ? sortDir : "asc"}
                  onClick={() => handleSort("classroom_name")}
                >
                  Nama Rombel
                </TableSortLabel>
              </TableCell>
              <TableCell
                className="font-black text-slate-700"
                sortDirection={sortBy === "grade.grade_name" ? sortDir : false}
              >
                <TableSortLabel
                  active={sortBy === "grade.grade_name"}
                  direction={sortBy === "grade.grade_name" ? sortDir : "asc"}
                  onClick={() => handleSort("grade.grade_name")}
                >
                  Tingkat / Fase
                </TableSortLabel>
              </TableCell>
              <TableCell
                className="font-black text-slate-700"
                sortDirection={sortBy === "homeroom.full_name" ? sortDir : false}
              >
                <TableSortLabel
                  active={sortBy === "homeroom.full_name"}
                  direction={sortBy === "homeroom.full_name" ? sortDir : "asc"}
                  onClick={() => handleSort("homeroom.full_name")}
                >
                  Wali Kelas
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-black text-slate-700" sortDirection={sortBy === "max_quota" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "max_quota"}
                  direction={sortBy === "max_quota" ? sortDir : "asc"}
                  onClick={() => handleSort("max_quota")}
                >
                  Kuota
                </TableSortLabel>
              </TableCell>
              <TableCell
                className="font-black text-slate-700"
                sortDirection={sortBy === "academic_year.year_name" ? sortDir : false}
              >
                <TableSortLabel
                  active={sortBy === "academic_year.year_name"}
                  direction={sortBy === "academic_year.year_name" ? sortDir : "asc"}
                  onClick={() => handleSort("academic_year.year_name")}
                >
                  Tahun Ajaran
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-black text-slate-700" align="center">
                Aksi
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((c) => (
                <TableRow key={c.id} hover className="border-b border-slate-50 last:border-0">
                  <TableCell className="font-bold text-slate-800">{c.classroom_name}</TableCell>
                  <TableCell className="font-medium text-slate-600">
                    {c.grade.grade_name} / {c.phase?.phase_name || "-"}
                  </TableCell>
                  <TableCell className="font-bold text-slate-600">{c.homeroom?.full_name || "-"}</TableCell>
                  <TableCell className="font-bold text-slate-600">{c.max_quota} Siswa</TableCell>
                  <TableCell className="text-slate-600">
                    {c.academic_year.year_name} ({c.academic_year.semester})
                  </TableCell>
                  <TableCell align="center">
                    <Box className="flex justify-center gap-1">
                      <IconButton
                        size="small"
                        color="success"
                        title="Penugasan Guru"
                        onClick={() => handleOpenAssignments(c)}
                        className="rounded-xl border border-slate-100 p-2 transition-all hover:bg-slate-50"
                      >
                        <AssignmentIcon fontSize="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="warning"
                        title="Anggota Kelas"
                        onClick={() => handleOpenEnrollments(c)}
                        className="rounded-xl border border-slate-100 p-2 transition-all hover:bg-slate-50"
                      >
                        <PeopleIcon fontSize="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="primary"
                        title="Edit Rombel"
                        onClick={() => {
                          setEditingClassroom(c);
                          setOpen(true);
                        }}
                        className="rounded-xl border border-slate-100 p-2 transition-all hover:bg-slate-50"
                      >
                        <NiPen size="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="error"
                        title="Hapus Rombel"
                        onClick={() => handleDelete(c.id)}
                        className="rounded-xl border border-slate-100 p-2 transition-all hover:bg-slate-50"
                      >
                        <NiBinEmpty size="small" />
                      </IconButton>
                    </Box>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10 font-bold text-slate-400">
                  Tidak ada data rombel.
                </TableCell>
              </TableRow>
            )}
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

      {/* Dialog Form Rombel */}
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        fullWidth
        maxWidth="md"
        classes={{ paper: "rounded-[32px] p-4" }}
      >
        <form onSubmit={formik.handleSubmit}>
          <DialogTitle className="text-2xl font-black text-slate-800">
            {editingClassroom ? "Edit Rombongan Belajar" : "Tambah Rombel Baru"}
          </DialogTitle>
          <DialogContent className="flex flex-col gap-4 pt-4">
            <Grid container spacing={3} className="mt-1">
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth error={formik.touched.school_id && Boolean(formik.errors.school_id)}>
                  <InputLabel>Sekolah</InputLabel>
                  <Select
                    label="Sekolah"
                    name="school_id"
                    value={formik.values.school_id}
                    onChange={formik.handleChange}
                  >
                    {schools.map((s) => (
                      <MenuItem key={s.id} value={s.id}>
                        {s.school_name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.school_id && formik.errors.school_id && (
                    <FormHelperText>{formik.errors.school_id as any}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl
                  fullWidth
                  error={formik.touched.academic_year_id && Boolean(formik.errors.academic_year_id)}
                >
                  <InputLabel>Tahun Ajaran</InputLabel>
                  <Select
                    label="Tahun Ajaran"
                    name="academic_year_id"
                    value={formik.values.academic_year_id}
                    onChange={formik.handleChange}
                  >
                    {academicYears.map((ay) => (
                      <MenuItem key={ay.id} value={ay.id}>
                        {ay.year_name} ({ay.semester}) {ay.is_active ? "- Aktif" : ""}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.academic_year_id && formik.errors.academic_year_id && (
                    <FormHelperText>{formik.errors.academic_year_id as any}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth error={formik.touched.grade_id && Boolean(formik.errors.grade_id)}>
                  <InputLabel>Tingkat Kelas</InputLabel>
                  <Select
                    label="Tingkat Kelas"
                    name="grade_id"
                    value={formik.values.grade_id}
                    onChange={formik.handleChange}
                  >
                    {grades.map((g) => (
                      <MenuItem key={g.id} value={g.id}>
                        {g.grade_name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.grade_id && formik.errors.grade_id && (
                    <FormHelperText>{formik.errors.grade_id as any}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth error={formik.touched.phase_id && Boolean(formik.errors.phase_id)}>
                  <InputLabel>Fase</InputLabel>
                  <Select label="Fase" name="phase_id" value={formik.values.phase_id} onChange={formik.handleChange}>
                    {phases.map((p) => (
                      <MenuItem key={p.id} value={p.id}>
                        {p.phase_name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.phase_id && formik.errors.phase_id && (
                    <FormHelperText>{formik.errors.phase_id as any}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <TextField
                  fullWidth
                  label="Nama Rombel"
                  name="classroom_name"
                  value={formik.values.classroom_name}
                  onChange={formik.handleChange}
                  error={formik.touched.classroom_name && Boolean(formik.errors.classroom_name)}
                  helperText={formik.touched.classroom_name && (formik.errors.classroom_name as string)}
                  placeholder="Contoh: Kelas 1A, Kelas 2B"
                />
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Wali Kelas</InputLabel>
                  <Select
                    label="Wali Kelas"
                    name="homeroom_teacher_id"
                    value={formik.values.homeroom_teacher_id}
                    onChange={formik.handleChange}
                  >
                    <MenuItem value="">
                      <em>Belum Ditentukan</em>
                    </MenuItem>
                    {teachers.map((t) => (
                      <MenuItem key={t.id} value={t.id}>
                        {t.full_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <TextField
                  fullWidth
                  type="number"
                  label="Kuota Maksimal"
                  name="max_quota"
                  value={formik.values.max_quota}
                  onChange={formik.handleChange}
                  error={formik.touched.max_quota && Boolean(formik.errors.max_quota)}
                  helperText={formik.touched.max_quota && (formik.errors.max_quota as string)}
                />
              </Grid>
              <Grid size={{ xs: 12 }}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Karakteristik / Kebutuhan Belajar Kelas"
                  name="class_characteristics"
                  value={formik.values.class_characteristics}
                  onChange={formik.handleChange}
                  placeholder="Ceritakan karakteristik siswa di kelas ini untuk membantu AI memberikan saran pengajaran..."
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions className="gap-2">
            <Button variant="outlined" color="inherit" onClick={() => setOpen(false)} className="rounded-xl font-bold">
              Batal
            </Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={formik.isSubmitting}
              className="rounded-xl px-6 font-black shadow-lg"
            >
              {editingClassroom ? "Perbarui" : "Simpan"}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* --- TEACHING ASSIGNMENTS DIALOG --- */}
      <Dialog
        open={openAssignmentDialog}
        onClose={() => setOpenAssignmentDialog(false)}
        maxWidth="md"
        fullWidth
        classes={{ paper: "rounded-[32px] p-6" }}
      >
        <DialogTitle className="flex items-center gap-2 text-2xl font-black text-slate-800">
          <AssignmentIcon color="primary" />
          Penugasan Guru: {selectedClassroomForAssignment?.classroom_name}
        </DialogTitle>
        <DialogContent className="py-4">
          {dialogError && (
            <Alert severity="error" className="mb-4 rounded-xl font-bold">
              {dialogError}
            </Alert>
          )}
          {dialogSuccess && (
            <Alert severity="success" className="mb-4 rounded-xl font-bold">
              {dialogSuccess}
            </Alert>
          )}

          {dialogLoading && assignments.length === 0 ? (
            <Box className="flex justify-center py-10">
              <CircularProgress size={30} />
            </Box>
          ) : (
            <Box className="flex flex-col gap-6">
              {/* Assignments Table */}
              <TableContainer
                component={Paper}
                className="overflow-hidden rounded-2xl border border-slate-100 shadow-none"
              >
                <Table size="small">
                  <TableHead className="bg-slate-50">
                    <TableRow>
                      <TableCell className="py-3 font-black text-slate-700">Mata Pelajaran</TableCell>
                      <TableCell className="py-3 font-black text-slate-700">Guru Pengampu</TableCell>
                      <TableCell className="py-3 font-black text-slate-700" align="center">
                        Aksi
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {paginatedAssignments.length > 0 ? (
                      paginatedAssignments.map((a) => (
                        <TableRow key={a.id} hover>
                          <TableCell className="font-bold text-slate-800">{a.subject?.subject_name}</TableCell>
                          <TableCell className="font-medium text-slate-600">{a.teacher?.full_name}</TableCell>
                          <TableCell align="center">
                            <IconButton color="error" size="small" onClick={() => handleDeleteAssignment(a.id)}>
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={3} className="py-6 text-center font-bold text-slate-400">
                          Belum ada penugasan guru di kelas ini.
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
                <TablePagination
                  component="div"
                  count={assignTotal}
                  page={assignPage - 1}
                  onPageChange={(_, newPage) => setAssignPage(newPage + 1)}
                  rowsPerPage={assignLimit}
                  onRowsPerPageChange={(e) => setAssignLimit(parseInt(e.target.value, 10))}
                  labelRowsPerPage="Baris:"
                />
              </TableContainer>

              <Divider className="my-2" />

              {/* Add Assignment Form */}
              <Box className="rounded-2xl border border-slate-100 bg-slate-50 p-6">
                <Typography variant="subtitle1" className="mb-4 font-black text-slate-800">
                  Tambah Penugasan Baru
                </Typography>
                <Grid container spacing={3} alignItems="center">
                  <Grid size={{ xs: 12, sm: 5 }}>
                    <FormControl fullWidth variant="outlined">
                      <InputLabel>Mata Pelajaran</InputLabel>
                      <Select
                        label="Mata Pelajaran"
                        value={newAssignmentSubject}
                        onChange={(e) => setNewAssignmentSubject(e.target.value)}
                      >
                        {subjects.map((sub) => (
                          <MenuItem key={sub.id} value={sub.id}>
                            {sub.subject_name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 5 }}>
                    <FormControl fullWidth variant="outlined">
                      <InputLabel>Guru Pengampu</InputLabel>
                      <Select
                        label="Guru Pengampu"
                        value={newAssignmentTeacher}
                        onChange={(e) => setNewAssignmentTeacher(e.target.value)}
                      >
                        {teachers.map((t) => (
                          <MenuItem key={t.id} value={t.id}>
                            {t.full_name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 2 }}>
                    <Button
                      fullWidth
                      variant="contained"
                      color="primary"
                      onClick={handleAddAssignment}
                      startIcon={<AddIcon />}
                      className="rounded-xl py-3.5 font-bold shadow-lg"
                      disabled={dialogLoading || !newAssignmentSubject || !newAssignmentTeacher}
                    >
                      Tambah
                    </Button>
                  </Grid>
                </Grid>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button
            variant="outlined"
            color="inherit"
            onClick={() => setOpenAssignmentDialog(false)}
            className="rounded-xl font-bold"
          >
            Tutup
          </Button>
        </DialogActions>
      </Dialog>

      {/* --- ENROLLMENTS DIALOG --- */}
      <Dialog
        open={openEnrollmentDialog}
        onClose={() => setOpenEnrollmentDialog(false)}
        maxWidth="md"
        fullWidth
        classes={{ paper: "rounded-[32px] p-6" }}
      >
        <DialogTitle className="flex items-center gap-2 text-2xl font-black text-slate-800">
          <PeopleIcon color="primary" />
          Daftar Siswa Kelas: {selectedClassroomForEnrollment?.classroom_name}
        </DialogTitle>
        <DialogContent className="py-4">
          {dialogError && (
            <Alert severity="error" className="mb-4 rounded-xl font-bold">
              {dialogError}
            </Alert>
          )}
          {dialogSuccess && (
            <Alert severity="success" className="mb-4 rounded-xl font-bold">
              {dialogSuccess}
            </Alert>
          )}

          {dialogLoading && enrollments.length === 0 ? (
            <Box className="flex justify-center py-10">
              <CircularProgress size={30} />
            </Box>
          ) : (
            <Box className="flex flex-col gap-6">
              {/* Enrollments Table */}
              <TableContainer
                component={Paper}
                className="overflow-hidden rounded-2xl border border-slate-100 shadow-none"
              >
                <Table size="small">
                  <TableHead className="bg-slate-50">
                    <TableRow>
                      <TableCell className="py-3 font-black text-slate-700">NISN / NIK</TableCell>
                      <TableCell className="py-3 font-black text-slate-700">Nama Lengkap</TableCell>
                      <TableCell className="py-3 font-black text-slate-700" align="center">
                        Aksi
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {paginatedEnrollments.length > 0 ? (
                      paginatedEnrollments.map((e) => (
                        <TableRow key={e.id} hover>
                          <TableCell className="font-bold text-slate-600">
                            {e.student?.nisn || e.student?.nik || "-"}
                          </TableCell>
                          <TableCell className="font-bold text-slate-800">{e.student?.full_name}</TableCell>
                          <TableCell align="center">
                            <IconButton color="error" size="small" onClick={() => handleUnenrollStudent(e.id)}>
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={3} className="py-6 text-center font-bold text-slate-400">
                          Belum ada siswa yang terdaftar di kelas ini.
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
                <TablePagination
                  component="div"
                  count={enrollTotal}
                  page={enrollPage - 1}
                  onPageChange={(_, newPage) => setEnrollPage(newPage + 1)}
                  rowsPerPage={enrollLimit}
                  onRowsPerPageChange={(e) => setEnrollLimit(parseInt(e.target.value, 10))}
                  labelRowsPerPage="Baris:"
                />
              </TableContainer>

              <Divider className="my-2" />

              {/* Add Enrollment Form */}
              <Box className="rounded-2xl border border-slate-100 bg-slate-50 p-6">
                <Typography variant="subtitle1" className="mb-4 font-black text-slate-800">
                  Daftarkan Siswa Baru ke Kelas
                </Typography>
                <Grid container spacing={3} alignItems="center">
                  <Grid size={{ xs: 12, sm: 10 }}>
                    <FormControl fullWidth variant="outlined">
                      <InputLabel>Pilih Siswa Aktif</InputLabel>
                      <Select
                        label="Pilih Siswa Aktif"
                        value={newEnrollmentStudent}
                        onChange={(e) => setNewEnrollmentStudent(e.target.value)}
                      >
                        {students.map((stu) => {
                          const isAlreadyEnrolled = enrollments.some((e) => e.student_id === stu.id);
                          return (
                            <MenuItem key={stu.id} value={stu.id} disabled={isAlreadyEnrolled}>
                              {stu.full_name} {stu.nisn ? `(NISN: ${stu.nisn})` : ""}{" "}
                              {isAlreadyEnrolled ? "- Sudah Masuk Kelas" : ""}
                            </MenuItem>
                          );
                        })}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 2 }}>
                    <Button
                      fullWidth
                      variant="contained"
                      color="primary"
                      onClick={handleEnrollStudent}
                      startIcon={<AddIcon />}
                      className="rounded-xl py-3.5 font-bold shadow-lg"
                      disabled={dialogLoading || !newEnrollmentStudent}
                    >
                      Daftar
                    </Button>
                  </Grid>
                </Grid>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button
            variant="outlined"
            color="inherit"
            onClick={() => setOpenEnrollmentDialog(false)}
            className="rounded-xl font-bold"
          >
            Tutup
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
