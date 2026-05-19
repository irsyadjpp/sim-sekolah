/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Skeleton,
  Snackbar,
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
import NiCalendar from "@/icons/nexture/ni-calendar";
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

interface DailyAttendance {
  student_id: string;
  status: string;
  notes: string;
}

const ATTENDANCE_STATUSES = [
  { value: "HADIR", label: "Hadir", color: "#10b981", bg: "#ecfdf5" },
  { value: "SAKIT", label: "Sakit", color: "#f59e0b", bg: "#fffbeb" },
  { value: "IZIN", label: "Izin", color: "#3b82f6", bg: "#eff6ff" },
  { value: "ALPA", label: "Alpa", color: "#ef4444", bg: "#fef2f2" },
];

export default function DailyPresencePage() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const queryClassroomId = searchParams.get("classroomId");

  const [classrooms, setClassrooms] = useState<{ id: string; classroom_name: string }[]>([]);
  const [selectedClassroom, setSelectedClassroom] = useState<string>("");
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().substring(0, 10));

  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [attendanceMap, setAttendanceMap] = useState<Record<string, DailyAttendance>>({});

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error">("success");

  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    fetchClassrooms();
  }, []);

  useEffect(() => {
    if (selectedClassroom && selectedDate) {
      fetchPresenceData(selectedClassroom, selectedDate);
    } else {
      setEnrollments([]);
      setAttendanceMap({});
    }
  }, [selectedClassroom, selectedDate]);

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
          const defaultSelect =
            queryClassroomId && loadedClassrooms.some((c: any) => c.id === queryClassroomId)
              ? queryClassroomId
              : loadedClassrooms[0].id;
          setSelectedClassroom(defaultSelect);
        }
      }
    } catch (err: any) {
      console.error("Gagal mengambil data kelas", err);
    }
  };

  const fetchPresenceData = async (classroomId: string, date: string) => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch Students (Enrollments)
      const enrRes = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classroomId}/enrollments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const enrJson = await enrRes.json();
      if (enrJson.status !== "success") throw new Error(enrJson.message);
      const enrData = enrJson.data as Enrollment[];
      setEnrollments(enrData);

      // 2. Fetch Daily Attendances
      const attRes = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classroomId}/attendances?date=${date}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const attJson = await attRes.json();
      const existingAttendance: Record<string, DailyAttendance> = {};
      if (attJson.status === "success" && attJson.data) {
        attJson.data.forEach((a: any) => {
          existingAttendance[a.student_id] = {
            student_id: a.student_id,
            status: a.status,
            notes: a.notes || "",
          };
        });
      }

      // 3. Populate Map
      const initialMap: Record<string, DailyAttendance> = {};
      enrData.forEach((e) => {
        const sid = e.student.id;
        initialMap[sid] = existingAttendance[sid] || {
          student_id: sid,
          status: "HADIR",
          notes: "",
        };
      });
      setAttendanceMap(initialMap);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = (studentId: string, status: string) => {
    setAttendanceMap((prev) => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        status,
      },
    }));
  };

  const handleNotesChange = (studentId: string, notes: string) => {
    setAttendanceMap((prev) => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        notes,
      },
    }));
  };

  const handleSaveAll = async () => {
    setSaving(true);
    try {
      const payload = Object.values(attendanceMap);
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/classrooms/${selectedClassroom}/attendances?date=${selectedDate}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ attendances: payload }),
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        setSnackbarMessage("Presensi berhasil disimpan!");
        setSnackbarSeverity("success");
        setSnackbarOpen(true);
      } else {
        setSnackbarMessage(json.message || "Gagal menyimpan presensi.");
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

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "daily_presence", data: enrollments, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Presensi Harian Siswa
        </Typography>
        {selectedClassroom && (
          <Button
            variant="contained"
            color="primary"
            startIcon={<NiFloppyDisk size="small" />}
            onClick={handleSaveAll}
            disabled={saving}
          >
            {saving ? "Menyimpan..." : "Simpan Presensi"}
          </Button>
        )}
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/students">Kesiswaan</Link>
        <Link to="/students/presence">Kehadiran</Link>
        <Typography variant="body2">Harian</Typography>
      </Breadcrumbs>

      <Grid container spacing={3}>
        {/* Filters Classroom & Date */}
        <Grid size={{ xs: 12 }}>
          <Card>
            <CardContent className="flex flex-wrap items-center gap-4">
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

              <TextField
                label="Tanggal Presensi"
                type="date"
                size="small"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
                style={{ width: 200 }}
              />
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

            {loading ? (
              <TableContainer component={Card}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell className="w-12 text-center font-bold">No</TableCell>
                      <TableCell className="w-48 font-bold">NISN</TableCell>
                      <TableCell className="font-bold">Nama Siswa</TableCell>
                      <TableCell className="w-80 text-center font-bold">Kehadiran</TableCell>
                      <TableCell className="font-bold">Keterangan / Catatan</TableCell>
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
                        <TableCell align="center">
                          <Box className="flex items-center justify-center gap-1">
                            {[1, 2, 3, 4].map((i) => (
                              <Skeleton key={i} variant="rectangular" width={65} height={30} className="rounded-md" />
                            ))}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Skeleton variant="rectangular" width="100%" height={30} className="rounded-md" />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : enrollments.length > 0 ? (
              <TableContainer component={Card}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell className="w-12 text-center font-bold">No</TableCell>
                      <TableCell className="w-48 font-bold" sortDirection={sortBy === "student.nisn" ? sortDir : false}>
                        <TableSortLabel
                          active={sortBy === "student.nisn"}
                          direction={sortBy === "student.nisn" ? sortDir : "asc"}
                          onClick={() => handleSort("student.nisn")}
                        >
                          NISN
                        </TableSortLabel>
                      </TableCell>
                      <TableCell className="font-bold" sortDirection={sortBy === "student.full_name" ? sortDir : false}>
                        <TableSortLabel
                          active={sortBy === "student.full_name"}
                          direction={sortBy === "student.full_name" ? sortDir : "asc"}
                          onClick={() => handleSort("student.full_name")}
                        >
                          Nama Siswa
                        </TableSortLabel>
                      </TableCell>
                      <TableCell className="w-80 text-center font-bold">Kehadiran</TableCell>
                      <TableCell className="font-bold">Keterangan / Catatan</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {paginatedData.map((e, idx) => {
                      const record = attendanceMap[e.student.id] || { status: "HADIR", notes: "" };
                      const realIndex = (page - 1) * limit + idx + 1;
                      return (
                        <TableRow key={e.id} hover>
                          <TableCell align="center">{realIndex}</TableCell>
                          <TableCell>{e.student.nisn}</TableCell>
                          <TableCell className="font-medium">{e.student.full_name}</TableCell>
                          <TableCell align="center">
                            <Box className="flex items-center justify-center gap-1">
                              {ATTENDANCE_STATUSES.map((status) => {
                                const active = record.status === status.value;
                                return (
                                  <Button
                                    key={status.value}
                                    size="small"
                                    variant={active ? "contained" : "outlined"}
                                    onClick={() => handleStatusChange(e.student.id, status.value)}
                                    aria-label={`Tandai ${e.student.full_name} sebagai ${status.label}`}
                                    style={{
                                      backgroundColor: active ? status.color : "transparent",
                                      borderColor: status.color,
                                      color: active ? "#ffffff" : status.color,
                                      minWidth: 65,
                                      fontWeight: active ? "bold" : "normal",
                                    }}
                                  >
                                    {status.label}
                                  </Button>
                                );
                              })}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <TextField
                              size="small"
                              fullWidth
                              placeholder="Catatan jika sakit/izin/alpa..."
                              aria-label={`Catatan presensi untuk ${e.student.full_name}`}
                              value={record.notes}
                              onChange={(ev) => handleNotesChange(e.student.id, ev.target.value)}
                            />
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
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                  <NiCalendar size="large" className="mb-2 text-gray-300" />
                  <Typography variant="h5" color="textSecondary" className="mb-1">
                    Tidak Ada Siswa
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Belum ada siswa terdaftar di dalam rombongan belajar ini.
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
                  Presensi Rombongan Belajar
                </Typography>
                <Typography variant="body1" color="textSecondary" className="max-w-md">
                  Harap pilih kelas dan tentukan tanggal presensi terlebih dahulu untuk mencatat atau melihat daftar
                  kehadiran harian siswa.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

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
