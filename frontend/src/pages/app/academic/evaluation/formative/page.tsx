/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

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
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
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
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPlus from "@/icons/nexture/ni-plus";

interface Classroom {
  id: string;
  name: string;
}

interface TeachingAssignment {
  id: string;
  teacher: { full_name: string };
  subject: { subject_name: string };
}

interface Assessment {
  id: string;
  assessment_name: string;
  assessment_type: string;
  assessment_date: string;
}

export default function FormativePage() {
  const confirm = useConfirm();
  const navigate = useNavigate();
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [assignments, setAssignments] = useState<TeachingAssignment[]>([]);
  const [assessments, setAssessments] = useState<Assessment[]>([]);

  const [selectedClassroomId, setSelectedClassroomId] = useState("");
  const [selectedAssignmentId, setSelectedAssignmentId] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [openModal, setOpenModal] = useState(false);
  const [newAssessmentName, setNewAssessmentName] = useState("");
  const [newAssessmentDate, setNewAssessmentDate] = useState("");

  const token = localStorage.getItem("accessToken");

  // Load classrooms on mount
  useEffect(() => {
    fetchClassrooms();
  }, []);

  // Load assignments when classroom changes
  useEffect(() => {
    if (selectedClassroomId) {
      fetchAssignments(selectedClassroomId);
    } else {
      setAssignments([]);
      setSelectedAssignmentId("");
    }
  }, [selectedClassroomId]);

  // Load assessments when assignment changes
  useEffect(() => {
    if (selectedAssignmentId) {
      fetchAssessments(selectedAssignmentId);
    } else {
      setAssessments([]);
    }
  }, [selectedAssignmentId]);

  const fetchClassrooms = async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms?limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setClassrooms(json.data);
        if (json.data.length > 0) {
          setSelectedClassroomId(json.data[0].id);
        }
      }
    } catch (err: any) {
      console.error(err);
    }
  };

  const fetchAssignments = async (classId: string) => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classId}/assignments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setAssignments(json.data);
        if (json.data.length > 0) {
          setSelectedAssignmentId(json.data[0].id);
        }
      }
    } catch (err: any) {
      console.error(err);
    }
  };

  const fetchAssessments = async (assignId: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teaching-assignments/${assignId}/assessments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        const data: Assessment[] = json.data || [];
        // Filter only FORMATIF
        setAssessments(data.filter((a) => a.assessment_type === "FORMATIF"));
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newAssessmentName || !newAssessmentDate) {
      alert("Nama asesmen dan tanggal wajib diisi");
      return;
    }
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teaching-assignments/${selectedAssignmentId}/assessments`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          assessment_name: newAssessmentName,
          assessment_type: "FORMATIF",
          assessment_date: newAssessmentDate + "T00:00:00Z",
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenModal(false);
        setNewAssessmentName("");
        setNewAssessmentDate("");
        fetchAssessments(selectedAssignmentId);
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDelete = async (id: string) => {
    const ok = await confirm({
      title: "Hapus Asesmen Formatif",
      message: "Yakin ingin menghapus asesmen ini?",
      confirmText: "Hapus",
      cancelText: "Batal",
    });
    if (!ok) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/assessments/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchAssessments(selectedAssignmentId);
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "formative", data: assessments, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Asesmen Formatif
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => setOpenModal(true)}
          disabled={!selectedAssignmentId}
        >
          Buat Formatif Baru
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Evaluasi</Typography>
        <Typography variant="body2">Formatif</Typography>
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
            <InputLabel>Pilih Mata Pelajaran (Penugasan)</InputLabel>
            <Select
              label="Pilih Mata Pelajaran (Penugasan)"
              value={selectedAssignmentId}
              onChange={(e) => setSelectedAssignmentId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Penugasan --</em>
              </MenuItem>
              {assignments.map((a) => (
                <MenuItem key={a.id} value={a.id}>
                  {a.subject?.subject_name} ({a.teacher?.full_name})
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

      {!selectedAssignmentId ? (
        <Alert severity="info">Silakan pilih Kelas dan Penugasan terlebih dahulu untuk melihat data asesmen.</Alert>
      ) : (
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell className="font-bold" sortDirection={sortBy === "assessment_date" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "assessment_date"}
                    direction={sortBy === "assessment_date" ? sortDir : "asc"}
                    onClick={() => handleSort("assessment_date")}
                  >
                    Tanggal
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-bold" sortDirection={sortBy === "assessment_name" ? sortDir : false}>
                  <TableSortLabel
                    active={sortBy === "assessment_name"}
                    direction={sortBy === "assessment_name" ? sortDir : "asc"}
                    onClick={() => handleSort("assessment_name")}
                  >
                    Nama Asesmen
                  </TableSortLabel>
                </TableCell>
                <TableCell className="font-bold">Tipe</TableCell>
                <TableCell className="font-bold" align="center">
                  Aksi
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={4} align="center" className="py-10">
                    <CircularProgress size={24} />
                  </TableCell>
                </TableRow>
              ) : paginatedData.length > 0 ? (
                paginatedData.map((a) => (
                  <TableRow key={a.id} hover>
                    <TableCell>{new Date(a.assessment_date).toLocaleDateString("id-ID")}</TableCell>
                    <TableCell className="font-medium">{a.assessment_name}</TableCell>
                    <TableCell>{a.assessment_type}</TableCell>
                    <TableCell align="center">
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<NiEyeOpen size="small" />}
                        onClick={() => navigate(`/academic/evaluation/formative/details?id=${a.id}`)}
                        className="mr-2"
                      >
                        Input Nilai
                      </Button>
                      <IconButton size="small" color="error" onClick={() => handleDelete(a.id)}>
                        <NiBinEmpty size="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} align="center" className="py-10">
                    Tidak ada data asesmen formatif untuk kelas ini.
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
      )}

      {/* Modal Create */}
      <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Buat Asesmen Formatif Baru</DialogTitle>
        <DialogContent dividers>
          <Box className="flex flex-col gap-4 pt-2">
            <TextField
              label="Nama Asesmen (Misal: Ulangan Harian 1)"
              fullWidth
              size="small"
              value={newAssessmentName}
              onChange={(e) => setNewAssessmentName(e.target.value)}
            />
            <TextField
              label="Tanggal"
              type="date"
              fullWidth
              size="small"
              value={newAssessmentDate}
              onChange={(e) => setNewAssessmentDate(e.target.value)}
              slotProps={{ inputLabel: { shrink: true } }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenModal(false)} color="inherit">
            Batal
          </Button>
          <Button onClick={handleCreate} variant="contained" color="primary">
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
