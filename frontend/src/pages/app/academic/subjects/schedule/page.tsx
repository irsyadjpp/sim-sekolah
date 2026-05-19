import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

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
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiCalendar from "@/icons/nexture/ni-calendar";
import NiClock from "@/icons/nexture/ni-clock";
import NiPlus from "@/icons/nexture/ni-plus";

interface Classroom {
  id: string;
  classroom_name: string;
}

interface Subject {
  id: string;
  subject_name: string;
}

interface Teacher {
  id: string;
  full_name: string;
}

interface TeachingAssignment {
  id: string;
  classroom_id: string;
  subject_id: string;
  teacher_id: string;
  subject?: Subject;
  teacher?: Teacher;
}

interface ClassSchedule {
  id: string;
  classroom_id: string;
  teaching_assignment_id: string;
  day_of_week: number;
  start_time: string;
  end_time: string;
  teaching_assignment?: TeachingAssignment;
}

const DAYS = [
  { value: 1, label: "Senin" },
  { value: 2, label: "Selasa" },
  { value: 3, label: "Rabu" },
  { value: 4, label: "Kamis" },
  { value: 5, label: "Jumat" },
  { value: 6, label: "Sabtu" },
];

export default function SchedulePage() {
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [selectedClassroom, setSelectedClassroom] = useState<string>("");
  const [assignments, setAssignments] = useState<TeachingAssignment[]>([]);
  const [schedules, setSchedules] = useState<ClassSchedule[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Active Day Tab (1 = Senin)
  const [activeTab, setActiveTab] = useState<number>(1);

  // Dialog State
  const [openModal, setOpenModal] = useState(false);
  const [formDay, setFormDay] = useState<number>(1);
  const [formAssignment, setFormAssignment] = useState<string>("");
  const [formStart, setFormStart] = useState<string>("07:30");
  const [formEnd, setFormEnd] = useState<string>("09:00");

  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    fetchClassrooms();
  }, []);

  useEffect(() => {
    if (selectedClassroom) {
      fetchSchedulesAndAssignments(selectedClassroom);
    } else {
      setSchedules([]);
      setAssignments([]);
    }
  }, [selectedClassroom]);

  const fetchClassrooms = async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        const loadedClassrooms = json.data || [];
        setClassrooms(loadedClassrooms);
        if (loadedClassrooms.length > 0) {
          setSelectedClassroom(loadedClassrooms[0].id);
        }
      }
    } catch (err: any) {
      console.error("Gagal mengambil data kelas", err);
    }
  };

  const fetchSchedulesAndAssignments = async (classroomId: string) => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch Schedules
      const schedRes = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classroomId}/schedules`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const schedJson = await schedRes.json();

      // 2. Fetch Assignments
      const assignRes = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classroomId}/assignments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const assignJson = await assignRes.json();

      if (schedJson.status === "success") {
        setSchedules(schedJson.data || []);
      }
      if (assignJson.status === "success") {
        setAssignments(assignJson.data || []);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenAdd = () => {
    setFormDay(activeTab);
    setFormAssignment("");
    setFormStart("07:30");
    setFormEnd("09:00");
    setOpenModal(true);
  };

  const handleSave = async () => {
    if (!formAssignment || !formStart || !formEnd) {
      alert("Harap lengkapi semua bidang.");
      return;
    }
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/schedules`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          classroom_id: selectedClassroom,
          teaching_assignment_id: formAssignment,
          day_of_week: formDay,
          start_time: formStart,
          end_time: formEnd,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenModal(false);
        fetchSchedulesAndAssignments(selectedClassroom);
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Apakah Anda yakin ingin menghapus jadwal ini?")) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/schedules/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchSchedulesAndAssignments(selectedClassroom);
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const filteredSchedules = schedules.filter((s) => s.day_of_week === activeTab);

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Jadwal Pelajaran
        </Typography>
        {selectedClassroom && (
          <Button variant="contained" color="primary" startIcon={<NiPlus size="small" />} onClick={handleOpenAdd}>
            Tambah Jadwal
          </Button>
        )}
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Link to="/academic/subjects">Pelajaran</Link>
        <Typography variant="body2">Jadwal</Typography>
      </Breadcrumbs>

      <Grid container spacing={3}>
        {/* Selector Classroom */}
        <Grid size={{ xs: 12 }}>
          <Card>
            <CardContent className="flex items-center gap-4">
              <FormControl size="small" style={{ minWidth: 250 }}>
                <InputLabel id="select-classroom-label">Pilih Rombongan Belajar (Kelas)</InputLabel>
                <Select
                  labelId="select-classroom-label"
                  value={selectedClassroom}
                  label="Pilih Rombongan Belajar (Kelas)"
                  onChange={(e) => setSelectedClassroom(e.target.value)}
                >
                  <MenuItem value="">
                    <em>-- Pilih Kelas --</em>
                  </MenuItem>
                  {classrooms.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.classroom_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              {selectedClassroom && (
                <Typography variant="body2" color="textSecondary">
                  Menampilkan jadwal pelajaran dan pembagian guru aktif.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {selectedClassroom ? (
          <Grid size={{ xs: 12 }}>
            {error && (
              <Alert severity="error" className="mb-4">
                {error}
              </Alert>
            )}

            <Card className="mb-4">
              <Tabs
                value={activeTab}
                onChange={(_, val) => setActiveTab(val)}
                indicatorColor="primary"
                textColor="primary"
                variant="fullWidth"
              >
                {DAYS.map((d) => (
                  <Tab key={d.value} label={d.label} value={d.value} />
                ))}
              </Tabs>
            </Card>

            {loading ? (
              <Box className="flex justify-center py-10">
                <CircularProgress />
              </Box>
            ) : filteredSchedules.length > 0 ? (
              <Grid container spacing={2}>
                {filteredSchedules.map((s) => {
                  const subjectName = s.teaching_assignment?.subject?.subject_name || "Mata Pelajaran";
                  const teacherName = s.teaching_assignment?.teacher?.full_name || "Guru";

                  return (
                    <Grid size={{ xs: 12, sm: 6, md: 4 }} key={s.id}>
                      <Card className="h-full border border-gray-100 shadow-sm transition-shadow duration-200 hover:shadow-md">
                        <CardContent className="relative flex h-full flex-col justify-between p-4">
                          <Box>
                            <Box className="mb-2 flex items-center gap-2">
                              <NiClock size="small" className="text-primary-500" />
                              <Typography variant="subtitle2" className="text-primary-700 font-bold">
                                {s.start_time} - {s.end_time}
                              </Typography>
                            </Box>
                            <Typography variant="h3" className="mb-1 font-semibold text-gray-800">
                              {subjectName}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" className="flex items-center gap-1">
                              {teacherName}
                            </Typography>
                          </Box>
                          <Box className="absolute top-2 right-2">
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => handleDelete(s.id)}
                              title="Hapus Jadwal"
                            >
                              <NiBinEmpty size="small" />
                            </IconButton>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  );
                })}
              </Grid>
            ) : (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                  <NiCalendar size="large" className="mb-2 text-gray-300" />
                  <Typography variant="h5" color="textSecondary" className="mb-1">
                    Tidak Ada Jadwal
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Belum ada mata pelajaran dijadwalkan pada hari ini.
                  </Typography>
                </CardContent>
              </Card>
            )}
          </Grid>
        ) : (
          <Grid size={{ xs: 12 }}>
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-20 text-center">
                <NiCalendar size="large" className="mb-4 text-gray-300" />
                <Typography variant="h4" className="mb-2 font-bold text-gray-700">
                  Pilih Rombongan Belajar
                </Typography>
                <Typography variant="body1" color="textSecondary" className="max-w-md">
                  Harap pilih kelas terlebih dahulu untuk melihat, menyusun, dan mengelola jadwal pelajaran.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Modal Tambah Jadwal */}
      <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Tambah Jadwal Pelajaran</DialogTitle>
        <DialogContent dividers className="flex flex-col gap-4">
          <FormControl fullWidth size="small">
            <InputLabel id="form-day-label">Hari</InputLabel>
            <Select
              labelId="form-day-label"
              value={formDay}
              label="Hari"
              onChange={(e) => setFormDay(Number(e.target.value))}
            >
              {DAYS.map((d) => (
                <MenuItem key={d.value} value={d.value}>
                  {d.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth size="small">
            <InputLabel id="form-assignment-label">Guru & Mata Pelajaran</InputLabel>
            <Select
              labelId="form-assignment-label"
              value={formAssignment}
              label="Guru & Mata Pelajaran"
              onChange={(e) => setFormAssignment(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Guru & Mapel --</em>
              </MenuItem>
              {assignments.map((a) => {
                const subName = a.subject?.subject_name || "Mata Pelajaran";
                const tName = a.teacher?.full_name || "Guru";
                return (
                  <MenuItem key={a.id} value={a.id}>
                    {subName} - {tName}
                  </MenuItem>
                );
              })}
            </Select>
          </FormControl>

          <Box className="flex gap-4">
            <TextField
              label="Jam Mulai"
              type="time"
              size="small"
              fullWidth
              value={formStart}
              onChange={(e) => setFormStart(e.target.value)}
              InputLabelProps={{ shrink: true }}
              inputProps={{ step: 300 }} // 5 min
            />
            <TextField
              label="Jam Selesai"
              type="time"
              size="small"
              fullWidth
              value={formEnd}
              onChange={(e) => setFormEnd(e.target.value)}
              InputLabelProps={{ shrink: true }}
              inputProps={{ step: 300 }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenModal(false)} color="inherit">
            Batal
          </Button>
          <Button onClick={handleSave} variant="contained" color="primary">
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
