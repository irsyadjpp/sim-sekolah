/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import AssignmentIcon from "@mui/icons-material/Assignment";
import BatteryChargingFullIcon from "@mui/icons-material/BatteryChargingFull";
// Contextual Deep Learning Icons
import BeachAccessIcon from "@mui/icons-material/BeachAccess";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ChecklistIcon from "@mui/icons-material/Checklist";
import ClassIcon from "@mui/icons-material/Class";
import DnsIcon from "@mui/icons-material/Dns";
import EmojiEmotionsIcon from "@mui/icons-material/EmojiEmotions";
import ErrorIcon from "@mui/icons-material/Error";
import ExploreIcon from "@mui/icons-material/Explore";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import InfoIcon from "@mui/icons-material/Info";
import MenuBookIcon from "@mui/icons-material/MenuBook";
import PeopleIcon from "@mui/icons-material/People";
// Import standard, reliable icons from MUI Icons Material
import SchoolIcon from "@mui/icons-material/School";
import SelfImprovementIcon from "@mui/icons-material/SelfImprovement";
import SettingsIcon from "@mui/icons-material/Settings";
import SignalCellularConnectedNoInternet0BarIcon from "@mui/icons-material/SignalCellularConnectedNoInternet0Bar";
import SpeedIcon from "@mui/icons-material/Speed";
import StorageIcon from "@mui/icons-material/Storage";
import SyncIcon from "@mui/icons-material/Sync";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  FormControlLabel,
  Grid,
  LinearProgress,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Switch,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

export default function DashboardPage() {
  const [selectedRole, setSelectedRole] = useState<"KEPALA_SEKOLAH" | "GURU" | "OPERATOR">("KEPALA_SEKOLAH");
  const [isOffline, setIsOffline] = useState(false);
  const [loading, setLoading] = useState(false);
  const [usingFallback, setUsingFallback] = useState(false);

  // Dashboard state placeholders
  const [pimpinanData, setPimpinanData] = useState<any>(null);
  const [guruData, setGuruData] = useState<any>(null);
  const [operatorData, setOperatorData] = useState<any>(null);

  const [checklist, setChecklist] = useState({
    modul: false,
    formatif: true,
    rapor: false,
  });

  // Attempt to load default role from localStorage
  useEffect(() => {
    const cachedUser = localStorage.getItem("-user-data");
    if (cachedUser) {
      try {
        const d = JSON.parse(cachedUser);
        const roles = d.roles || [];
        if (roles.includes("SUPER_ADMIN") || roles.includes("ADMIN_SEKOLAH")) {
          setSelectedRole("OPERATOR");
        } else if (roles.includes("GURU")) {
          setSelectedRole("GURU");
        } else {
          setSelectedRole("KEPALA_SEKOLAH");
        }
      } catch (e) {
        console.error("Failed to parse cached user for role", e);
      }
    }
  }, []);

  // Fetch Dashboard Data from Backend
  const fetchDashboardData = async () => {
    if (isOffline) {
      setUsingFallback(true);
      return;
    }

    setLoading(true);
    setUsingFallback(false);

    try {
      const token = localStorage.getItem("accessToken");
      let endpoint = "pimpinan";
      if (selectedRole === "GURU") endpoint = "guru";
      if (selectedRole === "OPERATOR") endpoint = "operator";

      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/dashboard/${endpoint}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error("HTTP failure");
      }

      const json = await res.json();
      const dashboardData = json.data || json;
      if (selectedRole === "KEPALA_SEKOLAH") {
        setPimpinanData(dashboardData);
      } else if (selectedRole === "GURU") {
        setGuruData(dashboardData);
      } else {
        setOperatorData(dashboardData);
      }
    } catch (e) {
      console.warn("Failed to fetch dashboard, falling back to gorgeous offline cache simulation", e);
      setUsingFallback(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [selectedRole, isOffline]);

  const handleToggleCheck = (key: "modul" | "formatif" | "rapor") => {
    setChecklist((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <Grid container spacing={4}>
      {/* HEADER SECTION */}
      <Grid size={12} className="mb-2">
        <Box className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
          <Box>
            <Typography variant="h1" component="h1" className="mb-0">
              Selamat Datang!
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/dashboards/default">
                Beranda
              </Link>
              <Typography variant="body2">Dasbor SIMS</Typography>
            </Breadcrumbs>
          </Box>

          {/* SIMULATION PANEL */}
          <Box className="bg-grey-500/5 border-grey-500/10 flex flex-wrap items-center gap-3 rounded-2xl border p-2">
            <Typography variant="caption" className="text-text-secondary ml-2 font-semibold">
              SIMULASI:
            </Typography>
            <Box className="flex gap-1">
              <Button
                variant={selectedRole === "KEPALA_SEKOLAH" ? "contained" : "text"}
                size="small"
                onClick={() => setSelectedRole("KEPALA_SEKOLAH")}
                className="px-3! py-1"
              >
                Kepala Sekolah
              </Button>
              <Button
                variant={selectedRole === "GURU" ? "contained" : "text"}
                size="small"
                onClick={() => setSelectedRole("GURU")}
                className="px-3! py-1"
              >
                Guru
              </Button>
              <Button
                variant={selectedRole === "OPERATOR" ? "contained" : "text"}
                size="small"
                onClick={() => setSelectedRole("OPERATOR")}
                className="px-3! py-1"
              >
                Operator
              </Button>
            </Box>
            <Divider orientation="vertical" flexItem className="my-1" />
            <FormControlLabel
              control={
                <Switch
                  checked={isOffline}
                  onChange={(e) => setIsOffline(e.target.checked)}
                  color="warning"
                  size="small"
                />
              }
              label={
                <Typography variant="caption" className="font-semibold">
                  Mode Luring
                </Typography>
              }
              className="mr-2 ml-1!"
            />
          </Box>
        </Box>
      </Grid>

      {/* STATUS BANNER */}
      {(isOffline || usingFallback) && (
        <Grid size={12}>
          <Alert
            severity="warning"
            icon={<SignalCellularConnectedNoInternet0BarIcon className="text-warning" />}
            className="border-warning/20 bg-warning-500/10! rounded-2xl border"
          >
            <Box className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
              <Typography variant="body2" className="text-warning-800 font-semibold">
                {isOffline
                  ? "⚡ Mode Luring Aktif (Data Terakhir: 07.30 WITA) - Menghindari sinkronisasi berat demi stabilitas koneksi Bonerate."
                  : "⚠️ Menggunakan cache data lokal offline karena peladen lokal sedang inisialisasi / sibuk."}
              </Typography>
              <Chip label="Offline Cache" size="small" className="bg-warning text-warning-contrast font-bold" />
            </Box>
          </Alert>
        </Grid>
      )}

      {/* ENERGY SAVING TIP BANNER */}
      <Grid size={12}>
        <Box className="bg-primary-500/5 border-primary-500/10 flex items-start gap-3 rounded-2xl border p-4">
          <BatteryChargingFullIcon className="text-primary mt-0.5" />
          <Box>
            <Typography variant="subtitle2" className="text-primary font-bold">
              Tips Efisiensi Daya UPT SDI Bonerate No 85
            </Typography>
            <Typography variant="body2" className="text-text-secondary text-sm">
              Mengingat keterbatasan daya listrik sekolah (1.300 Watt) dan seringnya terjadi pemadaman, Anda sangat
              disarankan untuk mengaktifkan <strong>Mode Gelap (Dark Mode)</strong> di menu kanan atas. Mode ini
              mengurangi konsumsi baterai perangkat pintar Anda hingga <strong>40%</strong>.
            </Typography>
          </Box>
        </Box>
      </Grid>

      {/* ----------------- 1. DASBOR KEPALA SEKOLAH ----------------- */}
      {selectedRole === "KEPALA_SEKOLAH" && (
        <>
          {/* STATS ROW */}
          <Grid size={{ xs: 12, md: 3 }}>
            <Card className="shadow-sm">
              <CardContent className="flex flex-col gap-2">
                <Box className="flex items-center justify-between">
                  <Typography variant="subtitle2" className="text-text-secondary tracking-wider uppercase">
                    Total Hadir
                  </Typography>
                  <CheckCircleIcon className="text-success" />
                </Box>
                <Typography variant="h2" className="text-success font-extrabold">
                  96%
                </Typography>
                <Typography variant="caption" className="text-text-secondary">
                  Persentase siswa hadir hari ini (Sangat Baik)
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <Card className="shadow-sm">
              <CardContent className="flex flex-col gap-2">
                <Box className="flex items-center justify-between">
                  <Typography variant="subtitle2" className="text-text-secondary tracking-wider uppercase">
                    Guru Aktif
                  </Typography>
                  <SchoolIcon className="text-primary" />
                </Box>
                <Typography variant="h2" className="text-primary font-extrabold">
                  18 / 20
                </Typography>
                <Typography variant="caption" className="text-text-secondary">
                  2 Guru berhalangan (Izin Dinas)
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <Card className="shadow-sm">
              <CardContent className="flex flex-col gap-2">
                <Box className="flex items-center justify-between">
                  <Typography variant="subtitle2" className="text-text-secondary tracking-wider uppercase">
                    Status KSP
                  </Typography>
                  <CheckCircleIcon className="text-success" />
                </Box>
                <Box className="flex items-center gap-2">
                  <Typography variant="h2" className="text-success font-extrabold">
                    {pimpinanData?.ksp_progress?.[0]?.persentase_selesai || "100"}%
                  </Typography>
                  <Chip label="Disahkan" size="small" color="success" className="font-bold" />
                </Box>
                <Typography variant="caption" className="text-text-secondary">
                  Dokumen KSP TA 2025/2026 terverifikasi
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <Card className="shadow-sm">
              <CardContent className="flex flex-col gap-2">
                <Box className="flex items-center justify-between">
                  <Typography variant="subtitle2" className="text-text-secondary tracking-wider uppercase">
                    Kesiapan Modul
                  </Typography>
                  <WarningAmberIcon className="text-warning" />
                </Box>
                <Box className="flex items-center gap-2">
                  <Typography variant="h2" className="text-warning font-extrabold">
                    85%
                  </Typography>
                  <Chip label="Evaluasi" size="small" color="warning" className="text-warning-contrast font-bold" />
                </Box>
                <Typography variant="caption" className="text-text-secondary">
                  3 Guru kelas belum melengkapi Modul Ajar
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* DYNAMIC PROGRESS INDICATORS */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <ClassIcon className="text-primary" /> Mutu Kognitif (Deep Learning)
                </Typography>

                <Box className="mt-2 flex flex-col gap-5">
                  {/* LOTS */}
                  <Box>
                    <Box className="mb-1 flex items-center justify-between">
                      <Typography variant="body2" className="text-text-primary font-semibold">
                        Penalaran Dasar (LOTS / Level PISA 1-3)
                      </Typography>
                      <Typography variant="body2" className="text-primary font-bold">
                        {pimpinanData?.cognitive_stats?.find((s: any) => s.tingkat_kognitif === "LOTS")
                          ?.rata_rata_nilai || "82"}
                        %
                      </Typography>
                    </Box>
                    <Box className="bg-grey-500/10 h-3.5 w-full rounded-full">
                      <Box
                        className="bg-primary h-3.5 rounded-full"
                        style={{
                          width: `${pimpinanData?.cognitive_stats?.find((s: any) => s.tingkat_kognitif === "LOTS")?.rata_rata_nilai || 82}%`,
                          backgroundImage:
                            "linear-gradient(90deg, var(--mui-palette-primary-main) 0%, var(--mui-palette-secondary-main) 100%)",
                        }}
                      />
                    </Box>
                    <Typography variant="caption" className="text-text-secondary mt-1 block">
                      Pemahaman hafalan, identifikasi fakta dasar, dan operasi rutin.
                    </Typography>
                  </Box>

                  {/* HOTS */}
                  <Box>
                    <Box className="mb-1 flex items-center justify-between">
                      <Typography variant="body2" className="text-text-primary font-semibold">
                        Penalaran Kritis (HOTS / Level PISA 4-6)
                      </Typography>
                      <Typography variant="body2" className="text-success font-bold">
                        {pimpinanData?.cognitive_stats?.find((s: any) => s.tingkat_kognitif === "HOTS")
                          ?.rata_rata_nilai || "68"}
                        %
                      </Typography>
                    </Box>
                    <Box className="bg-grey-500/10 h-3.5 w-full rounded-full">
                      <Box
                        className="bg-success h-3.5 rounded-full"
                        style={{
                          width: `${pimpinanData?.cognitive_stats?.find((s: any) => s.tingkat_kognitif === "HOTS")?.rata_rata_nilai || 68}%`,
                          backgroundImage:
                            "linear-gradient(90deg, var(--mui-palette-success-main) 0%, var(--mui-palette-success-light) 100%)",
                        }}
                      />
                    </Box>
                    <Typography variant="caption" className="text-text-secondary mt-1 block">
                      Analisis mandiri, penalaran ilmiah, perumusan argumen kritis.
                    </Typography>
                  </Box>

                  <Alert severity="info" className="bg-primary-500/5! border-primary-500/10 mt-2 border">
                    <Typography variant="caption" className="text-text-secondary">
                      <strong>Catatan Pedagogis:</strong> Transformasi Deep Learning menargetkan capaian HOTS sekolah
                      &gt;75% pada akhir TA ini.
                    </Typography>
                  </Alert>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* GRADUATE 8 DIMENSIONS */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-3">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <AssignmentIcon className="text-primary" /> Profil Lulusan (8 Dimensi)
                </Typography>

                <Box className="mt-2 grid grid-cols-1 gap-3 sm:grid-cols-2">
                  {[
                    { label: "Keimanan & Takwa", value: 92, status: "Aman" },
                    { label: "Kewargaan Global", value: 85, status: "Aman" },
                    { label: "Penalaran Kritis", value: 72, status: "Perhatian" },
                    { label: "Kreativitas", value: 70, status: "Perhatian" },
                    { label: "Gotong Royong", value: 88, status: "Aman" },
                    { label: "Kemandirian", value: 80, status: "Aman" },
                    { label: "Kesehatan", value: 78, status: "Aman" },
                    { label: "Komunikasi", value: 74, status: "Perhatian" },
                  ].map((dim) => {
                    const dbVal = pimpinanData?.p5_character_stats?.find(
                      (s: any) => s.dimension_name === dim.label,
                    )?.jumlah_siswa;
                    // Scale values if database view contains items
                    const actualValue = dbVal ? Math.min(100, 75 + dbVal * 5) : dim.value;
                    return (
                      <Box
                        key={dim.label}
                        className="bg-grey-500/5 border-grey-500/10 flex flex-col gap-1 rounded-xl border p-2.5"
                      >
                        <Box className="flex items-center justify-between">
                          <Typography variant="caption" className="text-text-primary font-bold">
                            {dim.label}
                          </Typography>
                          <Typography
                            variant="caption"
                            className={`font-extrabold ${actualValue >= 80 ? "text-success" : "text-warning"}`}
                          >
                            {actualValue}%
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={actualValue}
                          color={actualValue >= 80 ? "success" : "warning"}
                          className="h-1.5 rounded-full"
                        />
                      </Box>
                    );
                  })}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* (NEW) WIDGET: PETA PEMANFAATAN ELEMEN DESAIN (COASTAL & COMMUNITY HIGHLIGHT) */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <BeachAccessIcon className="text-primary" /> Peta Elemen Desain (Deep Learning)
                </Typography>
                <Typography variant="caption" className="text-text-secondary -mt-2 block">
                  Frekuensi pengintegrasian 4 Elemen Desain Pembelajaran mendalam pada Modul Ajar guru:
                </Typography>

                <Box className="mt-1 flex flex-col gap-3.5">
                  {(
                    pimpinanData?.design_elements_mapping || [
                      { label: "Praktik Pedagogis", value: 42, color: "var(--mui-palette-primary-main)" },
                      {
                        label: "Lingkungan Belajar (Pesisir Pantai)",
                        value: 35,
                        color: "var(--mui-palette-success-main)",
                        highlight: true,
                      },
                      {
                        label: "Kemitraan Belajar (Wali & Komite)",
                        value: 28,
                        color: "var(--mui-palette-secondary-main)",
                      },
                      { label: "Pemanfaatan Digital (Lokal Intranet)", value: 12, color: "orange" },
                    ]
                  ).map((elem: any) => (
                    <Box
                      key={elem.label}
                      className={`rounded-2xl border p-3 transition-all ${elem.highlight ? "bg-success-500/5 border-success/30 shadow-xs" : "bg-grey-500/5 border-grey-500/10"}`}
                    >
                      <Box className="mb-1 flex items-center justify-between">
                        <Box className="flex items-center gap-2">
                          <Box
                            className="text-text-secondary"
                            style={{ color: elem.highlight ? "var(--mui-palette-success-main)" : "inherit" }}
                          >
                            {elem.label.includes("Pesisir") ? (
                              <BeachAccessIcon fontSize="small" />
                            ) : (
                              <SchoolIcon fontSize="small" />
                            )}
                          </Box>
                          <Typography
                            variant="body2"
                            className={`font-bold ${elem.highlight ? "text-success-800" : "text-text-primary"}`}
                          >
                            {elem.label}
                          </Typography>
                        </Box>
                        <Box className="flex items-center gap-1.5">
                          <Typography variant="body2" className="text-text-primary font-extrabold">
                            {elem.value} kali
                          </Typography>
                          {elem.highlight && (
                            <Chip
                              label="Visi Bahari"
                              size="small"
                              color="success"
                              className="text-xxs h-5 font-extrabold"
                            />
                          )}
                        </Box>
                      </Box>
                      <Box className="bg-grey-500/10 h-2 w-full rounded-full">
                        <Box
                          className="h-2 rounded-full"
                          style={{ width: `${(elem.value / 50) * 100}%`, backgroundColor: elem.color }}
                        />
                      </Box>
                    </Box>
                  ))}

                  <Alert severity="success" className="bg-success-500/5! border-success/15 mt-1 rounded-xl border">
                    <Typography variant="caption" className="text-text-secondary">
                      <strong>💡 Analisis Keunggulan Bahari:</strong> Pemanfaatan alam pesisir pantai Bonerate sebagai
                      lingkungan belajar aktif meningkat sebesar <strong>15%</strong> pada modul ajar guru bulan ini!
                    </Typography>
                  </Alert>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* LEARNING PARTNERSHIP & ALERTS */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <PeopleIcon className="text-primary" /> Kemitraan Belajar (Orang Tua &amp; Komite)
                </Typography>

                <Box className="mt-2 flex flex-col gap-4">
                  <Box className="flex items-center gap-3">
                    <Box className="bg-success-500/10 text-success flex rounded-full p-2">
                      <CheckCircleIcon fontSize="medium" />
                    </Box>
                    <Box className="flex-1">
                      <Typography variant="body2" className="text-text-primary font-bold">
                        Kehadiran Rapat Komite
                      </Typography>
                      <Typography variant="caption" className="text-text-secondary">
                        Tingkat kehadiran wali murid kelas I - VI mencapai <strong>90%</strong>.
                      </Typography>
                    </Box>
                    <Chip label="Tinggi" size="small" color="success" className="font-bold" />
                  </Box>

                  <Box className="flex items-center gap-3">
                    <Box className="bg-success-500/10 text-success flex rounded-full p-2">
                      <CheckCircleIcon fontSize="medium" />
                    </Box>
                    <Box className="flex-1">
                      <Typography variant="body2" className="text-text-primary font-bold">
                        Partisipasi Program Pesisir
                      </Typography>
                      <Typography variant="caption" className="text-text-secondary">
                        Keterlibatan orang tua dalam projek konservasi pantai Bonerate mencapai <strong>85%</strong>.
                      </Typography>
                    </Box>
                    <Chip label="Tinggi" size="small" color="success" className="font-bold" />
                  </Box>

                  <Divider className="my-1" />

                  {/* Alerts within same column to optimize space */}
                  <Alert
                    severity="warning"
                    icon={<WarningAmberIcon />}
                    className="border-warning/20 bg-warning-500/5! mt-1 rounded-xl border"
                  >
                    <Typography variant="body2" className="text-warning-800 font-bold">
                      Wali Kelas V-B belum mengisi Nilai Sumatif
                    </Typography>
                    <Typography variant="caption" className="text-text-secondary mt-0.5 block">
                      Batas waktu penginputan tersisa <strong>2 hari lagi</strong>. Harap koordinasikan dengan wali
                      kelas terkait.
                    </Typography>
                  </Alert>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </>
      )}

      {/* ----------------- 2. DASBOR GURU & WALI KELAS ----------------- */}
      {selectedRole === "GURU" && (
        <>
          {/* TEACHER ACTION LINKS */}
          <Grid size={12}>
            <Box className="flex flex-wrap gap-3">
              <Button
                variant="contained"
                color="primary"
                component={Link}
                to="/learning/modules"
                className="rounded-2xl px-6! py-2.5 font-bold shadow-md"
                startIcon={<MenuBookIcon />}
              >
                Buat Modul Ajar (AI)
              </Button>
              <Button
                variant="outlined"
                color="inherit"
                component={Link}
                to="/reports/gradebook/scores"
                className="border-grey-500/20 hover:border-grey-500/40 bg-background-paper rounded-2xl px-6! py-2.5 font-bold"
                startIcon={<AssignmentIcon />}
              >
                Buku Nilai Kelas
              </Button>
              <Button variant="text" color="primary" component={Link} to="/academic/ksp" className="font-bold">
                Lihat Panduan KSP
              </Button>
            </Box>
          </Grid>

          {/* TODAY'S SCHEDULE & PRESENCE */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <ClassIcon className="text-primary" /> Jadwal Mengajar Hari Ini
                </Typography>

                <Box className="mt-2 flex flex-col gap-3">
                  {/* Lesson 1 */}
                  <Box className="bg-grey-500/5 border-grey-500/10 flex flex-col justify-between gap-3 rounded-2xl border p-3.5 sm:flex-row sm:items-center">
                    <Box>
                      <Box className="mb-1 flex items-center gap-2">
                        <Chip label="07.30 - 08.50 WITA" size="small" color="primary" className="font-bold" />
                        <Typography variant="caption" className="text-text-secondary font-bold">
                          4 jam pelajaran
                        </Typography>
                      </Box>
                      <Typography variant="body1" className="text-text-primary font-bold">
                        Matematika (Fase B - Kelas IV-A)
                      </Typography>
                      <Typography variant="caption" className="text-warning mt-0.5 block font-semibold">
                        ⚠️ Jurnal Presensi: Belum diisi
                      </Typography>
                    </Box>
                    <Button
                      variant="contained"
                      color="warning"
                      size="small"
                      component={Link}
                      to="/students/presence/daily"
                      className="rounded-xl px-4 py-1.5! font-bold shadow-sm"
                    >
                      Isi Presensi
                    </Button>
                  </Box>

                  {/* Lesson 2 */}
                  <Box className="bg-grey-500/5 border-grey-500/10 flex flex-col justify-between gap-3 rounded-2xl border p-3.5 sm:flex-row sm:items-center">
                    <Box>
                      <Box className="mb-1 flex items-center gap-2">
                        <Chip label="09.10 - 10.30 WITA" size="small" color="primary" className="font-bold" />
                        <Typography variant="caption" className="text-text-secondary font-bold">
                          4 jam pelajaran
                        </Typography>
                      </Box>
                      <Typography variant="body1" className="text-text-primary font-bold">
                        IPAS (Fase B - Kelas IV-A)
                      </Typography>
                      <Typography variant="caption" className="text-success mt-0.5 block font-semibold">
                        ✅ Jurnal Presensi: Lengkap
                      </Typography>
                    </Box>
                    <Button
                      disabled
                      variant="outlined"
                      size="small"
                      className="text-text-secondary! rounded-xl px-4 py-1.5! font-bold"
                    >
                      Selesai
                    </Button>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* ASYNCHRONOUS AI TASKS QUEUE */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <HourglassEmptyIcon className="text-primary" /> Status Antrean AI Lokal
                </Typography>
                <Typography variant="caption" className="text-text-secondary -mt-2 block">
                  Karena AI dijalankan di peladen lokal sekolah, pemrosesan dilakukan secara asinkron untuk menjaga
                  kinerja server tetap stabil.
                </Typography>

                <Box className="mt-2 flex flex-col gap-3">
                  {(guruData?.automation_queue && guruData.automation_queue.length > 0
                    ? guruData.automation_queue.slice(0, 2)
                    : [
                        { task_type: "PERUMUSAN_MODUL", status: "PROSES" },
                        { task_type: "NARASI_RAPOR", status: "SELESAI" },
                      ]
                  ).map((task: any, idx: number) => {
                    const isProcessing = task.status === "PROSES" || task.status === "ANTREAN";
                    return (
                      <Box
                        key={task.id || idx}
                        className={`flex items-center justify-between rounded-2xl border p-3 ${isProcessing ? "bg-primary-500/5 border-primary-500/10" : "bg-success-500/5 border-success-500/10"}`}
                      >
                        <Box className="flex items-start gap-2.5">
                          {isProcessing ? (
                            <SyncIcon className="text-primary mt-0.5 animate-spin" />
                          ) : (
                            <CheckCircleIcon className="text-success mt-0.5" />
                          )}
                          <Box>
                            <Typography variant="body2" className="text-text-primary font-bold">
                              {task.task_type.replace("_", " ")}
                            </Typography>
                            <Typography variant="caption" className="text-text-secondary">
                              {task.error_log
                                ? "Gagal: " + task.error_log.substring(0, 40) + "..."
                                : "Sintesis deskripsi capaian lokal"}
                            </Typography>
                          </Box>
                        </Box>
                        <Box className="flex flex-col items-end gap-1 text-right">
                          <Chip
                            label={
                              task.status === "ANTREAN"
                                ? "Mengantre"
                                : task.status === "PROSES"
                                  ? "Memproses"
                                  : task.status
                            }
                            size="small"
                            color={isProcessing ? "primary" : task.status === "GAGAL" ? "error" : "success"}
                            className="font-bold"
                          />
                        </Box>
                      </Box>
                    );
                  })}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* (NEW) WIDGET: RUANG "PRAKTIK BERKESADARAN" (MINDFUL LEARNING JOURNAL WEEKLY MOODS) */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-3">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <SelfImprovementIcon className="text-primary" /> Praktik Berkesadaran (Jurnal Kelas)
                </Typography>
                <Typography variant="caption" className="text-text-secondary -mt-2 block">
                  Indeks suasana belajar mendalam (*Deep Learning*) murid di kelas minggu ini:
                </Typography>

                <Box className="mt-1.5 flex flex-col gap-3">
                  {(
                    guruData?.mindful_observations || [
                      {
                        aspect: "Berkesadaran (Mindful)",
                        percentage: 90,
                        ref: "Anak-anak hening sejenak mendengarkan deru ombak pantai Bonerate sebelum mulai menggambar pola laut.",
                      },
                      {
                        aspect: "Bermakna (Meaningful)",
                        percentage: 85,
                        ref: "Belajar operasi matematika langsung menggunakan media kerang dan pasir pantai.",
                      },
                      {
                        aspect: "Menggembirakan (Joyful)",
                        percentage: 95,
                        ref: "Eksplorasi langsung biotopo pantai pesisir sangat memicu rasa ingin tahu siswa kelas IV!",
                      },
                    ]
                  ).map((obs: any, idx: number) => {
                    const colors = ["primary", "success", "secondary"];
                    const icons = [
                      <SelfImprovementIcon className="text-primary" />,
                      <ExploreIcon className="text-success" />,
                      <EmojiEmotionsIcon className="text-secondary" />,
                    ];
                    return (
                      <Box
                        key={obs.aspect}
                        className={`rounded-2xl border p-3 ${idx === 0 ? "bg-primary-500/5 border-primary-500/10" : idx === 1 ? "bg-success-500/5 border-success-500/10" : "bg-secondary-500/5 border-secondary-500/10"}`}
                      >
                        <Box className="mb-1 flex items-center justify-between">
                          <Box className="flex items-center gap-2">
                            {icons[idx % 3]}
                            <Typography variant="body2" className="text-text-primary font-bold">
                              {obs.aspect}
                            </Typography>
                          </Box>
                          <Typography
                            variant="body2"
                            className="font-extrabold"
                            style={{ color: `var(--mui-palette-${colors[idx % 3]}-main)` }}
                          >
                            {obs.percentage}%
                          </Typography>
                        </Box>
                        <Typography variant="caption" className="text-text-secondary mb-1 block">
                          {obs.ref}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={obs.percentage}
                          color={colors[idx % 3] as any}
                          className="h-1.5 rounded-full"
                        />
                      </Box>
                    );
                  })}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* TEACHER ADMINISTRATIVE CHECKLIST */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-3">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <ChecklistIcon className="text-primary" /> Tugas Administrasi Anda
                </Typography>

                <List className="mt-1 flex flex-col gap-2 p-0">
                  <ListItemButton
                    onClick={() => handleToggleCheck("modul")}
                    className={`rounded-2xl border transition-all ${checklist.modul ? "bg-success-500/5 border-success/30" : "bg-grey-500/5 border-grey-500/10"}`}
                  >
                    <ListItemIcon className="min-w-8">
                      <Box
                        className={`flex h-5 w-5 items-center justify-center rounded-md border transition-all ${checklist.modul ? "bg-success border-success text-white" : "border-grey-500"}`}
                      >
                        {checklist.modul && "✓"}
                      </Box>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography
                          variant="body2"
                          className={`font-bold ${checklist.modul ? "text-text-secondary line-through" : "text-text-primary"}`}
                        >
                          Susun Modul Ajar Minggu Depan
                        </Typography>
                      }
                      secondary={
                        <Typography variant="caption" className="text-text-secondary">
                          Wajib diserahkan ke Kepala Sekolah
                        </Typography>
                      }
                    />
                  </ListItemButton>

                  <ListItemButton
                    onClick={() => handleToggleCheck("formatif")}
                    className={`rounded-2xl border transition-all ${checklist.formatif ? "bg-success-500/5 border-success/30" : "bg-grey-500/5 border-grey-500/10"}`}
                  >
                    <ListItemIcon className="min-w-8">
                      <Box
                        className={`flex h-5 w-5 items-center justify-center rounded-md border transition-all ${checklist.formatif ? "bg-success border-success text-white" : "border-grey-500"}`}
                      >
                        {checklist.formatif && "✓"}
                      </Box>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography
                          variant="body2"
                          className={`font-bold ${checklist.formatif ? "text-text-secondary line-through" : "text-text-primary"}`}
                        >
                          Input Formatif Harian
                        </Typography>
                      }
                      secondary={
                        <Typography variant="caption" className="text-text-secondary">
                          Selesai diinput untuk Rombel IV-A
                        </Typography>
                      }
                    />
                  </ListItemButton>

                  <ListItemButton
                    onClick={() => handleToggleCheck("rapor")}
                    className={`rounded-2xl border transition-all ${checklist.rapor ? "bg-success-500/5 border-success/30" : "bg-grey-500/5 border-grey-500/10"}`}
                  >
                    <ListItemIcon className="min-w-8">
                      <Box
                        className={`flex h-5 w-5 items-center justify-center rounded-md border transition-all ${checklist.rapor ? "bg-success border-success text-white" : "border-grey-500"}`}
                      >
                        {checklist.rapor && "✓"}
                      </Box>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography
                          variant="body2"
                          className={`font-bold ${checklist.rapor ? "text-text-secondary line-through" : "text-text-primary"}`}
                        >
                          Cetak Rapor Tengah Semester
                        </Typography>
                      }
                      secondary={
                        <Typography variant="caption" className="text-text-secondary">
                          Batas waktu sebelum 25 Mei 2026
                        </Typography>
                      }
                    />
                  </ListItemButton>
                </List>

                {/* SPECIAL WATCH / INTERVENSI DINI SISWA */}
                <Box className="mt-2 flex flex-col gap-2">
                  <Typography variant="subtitle2" className="text-text-primary flex items-center gap-1.5 font-bold">
                    <WarningAmberIcon className="text-warning" fontSize="small" /> Pantauan Khusus
                  </Typography>
                  {(guruData?.student_watch && guruData.student_watch.length > 0
                    ? guruData.student_watch.slice(0, 1)
                    : [{ nama_siswa: "Ahmad Fauzi", total_absen: 4, status_peringatan: "PERLU INTERVENSI" }]
                  ).map((stud: any, idx: number) => (
                    <Box
                      key={stud.nama_siswa || idx}
                      className="bg-error-500/5 border-error/15 flex items-center justify-between rounded-xl border p-2"
                    >
                      <Typography variant="caption" className="text-text-primary font-bold">
                        {stud.nama_siswa}
                      </Typography>
                      <Chip
                        label={`Absen ${stud.total_absen} Hari`}
                        size="small"
                        color="error"
                        className="text-xxs h-5 font-bold"
                      />
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* DEEP LEARNING MODUL MAP */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-3">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <AssignmentIcon className="text-primary" /> Peta Modul (Deep Learning)
                </Typography>
                <Typography variant="caption" className="text-text-secondary -mt-2 block">
                  Kesesuaian rancangan Modul Ajar minggu ini dengan standar pembelajaran mendalam:
                </Typography>

                <Box className="mt-1 flex flex-col gap-2.5">
                  {(guruData?.module_compliance && guruData.module_compliance.length > 0
                    ? [
                        {
                          label: "Tahap 1: Memahami (LOTS)",
                          val: guruData.module_compliance[0].jumlah_tahap_terpenuhi >= 1,
                        },
                        {
                          label: "Tahap 2: Mengaplikasi (MOTS)",
                          val: guruData.module_compliance[0].jumlah_tahap_terpenuhi >= 2,
                        },
                        {
                          label: "Tahap 3: Merefleksi (HOTS)",
                          val: guruData.module_compliance[0].jumlah_tahap_terpenuhi >= 3,
                        },
                        { label: "Prinsip: Berkesadaran & Bermakna", val: true },
                        { label: "Prinsip: Menggembirakan (Joyful)", val: false },
                      ]
                    : [
                        { label: "Tahap 1: Memahami (LOTS)", val: true },
                        { label: "Tahap 2: Mengaplikasi (MOTS)", val: true },
                        { label: "Tahap 3: Merefleksi (HOTS)", val: false },
                        { label: "Prinsip: Berkesadaran & Bermakna", val: true },
                        { label: "Prinsip: Menggembirakan (Joyful)", val: false },
                      ]
                  ).map((item) => (
                    <Box
                      key={item.label}
                      className="bg-grey-500/5 border-grey-500/10 flex items-center justify-between rounded-xl border p-2"
                    >
                      <Typography variant="body2" className="text-text-primary text-sm font-semibold">
                        {item.label}
                      </Typography>
                      {item.val ? (
                        <Chip label="Terpenuhi" size="small" color="success" className="text-xxs h-6 font-bold" />
                      ) : (
                        <Chip
                          label="Belum Ada"
                          size="small"
                          color="warning"
                          className="text-xxs text-warning-contrast h-6 font-bold"
                        />
                      )}
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </>
      )}

      {/* ----------------- 3. DASBOR OPERATOR SISTEM ----------------- */}
      {selectedRole === "OPERATOR" && (
        <>
          {/* OPERATOR ACTION LINKS */}
          <Grid size={12}>
            <Box className="flex flex-wrap gap-3">
              <Button
                variant="contained"
                color="primary"
                component={Link}
                to="/students/records/identity"
                className="rounded-2xl px-6! py-2.5 font-bold shadow-md"
                startIcon={<PeopleIcon />}
              >
                Tambah Siswa Baru
              </Button>
              <Button
                variant="outlined"
                color="inherit"
                component={Link}
                to="/academic/subjects/classroom"
                className="border-grey-500/20 hover:border-grey-500/40 bg-background-paper rounded-2xl px-6! py-2.5 font-bold"
                startIcon={<ClassIcon />}
              >
                Atur Rombongan Belajar
              </Button>
              <Button variant="text" color="primary" component={Link} to="/profile/school" className="font-bold">
                Kelola Profil UPT SDI 85
              </Button>
            </Box>
          </Grid>

          {/* INTRANET LOCAL HARDWARE PERFORMANCE */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <DnsIcon className="text-primary" /> Beban Peladen Lokal (Intranet)
                </Typography>

                <Box className="mt-2 flex flex-col gap-4">
                  {/* CPU Load */}
                  <Box className="flex items-center justify-between gap-4">
                    <Box className="flex min-w-32 items-center gap-2.5">
                      <SpeedIcon className="text-text-secondary" />
                      <Typography variant="body2" className="text-text-primary font-bold">
                        Beban CPU
                      </Typography>
                    </Box>
                    <Box className="flex-1">
                      <LinearProgress
                        variant="determinate"
                        value={operatorData?.server_telemetry?.[0]?.cpu_usage_percent || 42}
                        color="success"
                        className="h-2.5 rounded-full"
                      />
                    </Box>
                    <Typography variant="body2" className="text-success min-w-10 text-right font-extrabold">
                      {operatorData?.server_telemetry?.[0]?.cpu_usage_percent || 42}%
                    </Typography>
                  </Box>

                  {/* RAM Load */}
                  <Box className="flex items-center justify-between gap-4">
                    <Box className="flex min-w-32 items-center gap-2.5">
                      <StorageIcon className="text-text-secondary" />
                      <Typography variant="body2" className="text-text-primary font-bold">
                        Memori RAM
                      </Typography>
                    </Box>
                    <Box className="flex-1">
                      <LinearProgress
                        variant="determinate"
                        value={operatorData?.server_telemetry?.[0]?.ram_usage_percent || 48}
                        color="success"
                        className="h-2.5 rounded-full"
                      />
                    </Box>
                    <Typography variant="body2" className="text-success min-w-10 text-right font-extrabold">
                      {operatorData?.server_telemetry?.[0]?.ram_usage_percent || 48}%
                    </Typography>
                  </Box>

                  {/* Server Temp */}
                  <Box className="flex items-center justify-between gap-4">
                    <Box className="flex min-w-32 items-center gap-2.5">
                      <ThermostatIcon className="text-text-secondary" />
                      <Typography variant="body2" className="text-text-primary font-bold">
                        Suhu Peladen
                      </Typography>
                    </Box>
                    <Box className="flex-1">
                      <LinearProgress
                        variant="determinate"
                        value={operatorData?.server_telemetry?.[0]?.server_temperature_c || 46}
                        color="success"
                        className="h-2.5 rounded-full"
                      />
                    </Box>
                    <Typography variant="body2" className="text-success min-w-10 text-right font-extrabold">
                      {operatorData?.server_telemetry?.[0]?.server_temperature_c || 46}°C
                    </Typography>
                  </Box>

                  {/* Storage Available */}
                  <Box className="flex items-center justify-between gap-4">
                    <Box className="flex min-w-32 items-center gap-2.5">
                      <SettingsIcon className="text-text-secondary" />
                      <Typography variant="body2" className="text-text-primary font-bold">
                        Penyimpanan Bebas
                      </Typography>
                    </Box>
                    <Box className="flex-1">
                      <LinearProgress variant="determinate" value={85} color="success" className="h-2.5 rounded-full" />
                    </Box>
                    <Typography variant="body2" className="text-success min-w-10 text-right font-extrabold">
                      {operatorData?.server_telemetry?.[0]?.storage_free_gb || 850} GB
                    </Typography>
                  </Box>

                  <Typography variant="caption" className="text-text-secondary mt-1">
                    *Kapasitas komputasi dibatasi oleh keterbatasan daya 1.300 Watt sekolah untuk meminimalisasi
                    lonjakan daya AC pendingin peladen.
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* BACKEND SYSTEMS HEALTH */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <CheckCircleIcon className="text-success" /> Kesehatan Status Layanan
                </Typography>

                <Box className="mt-2 flex flex-col gap-3.5">
                  {(
                    operatorData?.services_health || [
                      {
                        service: "Database Utama (PostgreSQL)",
                        desc: "Menampung seluruh tabel data induk sekolah",
                        status: "Berjalan",
                      },
                      {
                        service: "Mesin Otomasi Sistem (Lokal)",
                        desc: "Penyusun dokumen KSP & modul ajar mandiri secara asinkron",
                        status: "Berjalan",
                      },
                      {
                        service: "Antrean Pesan Lokal (Redis)",
                        desc: "Manajer antrean tugas operasional intranet",
                        status: "Berjalan",
                      },
                    ]
                  ).map((srv: any) => (
                    <Box
                      key={srv.service}
                      className="bg-grey-500/5 border-grey-500/10 flex items-center justify-between gap-3 rounded-2xl border p-3"
                    >
                      <Box>
                        <Typography variant="body2" className="text-text-primary font-bold">
                          {srv.service}
                        </Typography>
                        <Typography variant="caption" className="text-text-secondary mt-0.5 block">
                          {srv.desc}
                        </Typography>
                      </Box>
                      <Chip label={srv.status} size="small" color="success" className="font-bold" />
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* DATA COMPLETENESS INDEX FOR RAG CONTEXT STRENGTH */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <AssignmentIcon className="text-primary" /> Kelengkapan Atribut Konteks RAG
                </Typography>
                <Typography variant="caption" className="text-text-secondary -mt-2 block">
                  Indeks ini mengukur tingkat kelengkapan data referensi sekolah. Semakin lengkap, kualitas perumusan
                  dokumen AI RAG semakin presisi.
                </Typography>

                <Box className="mt-2 flex flex-col gap-4">
                  {/* School Profile */}
                  <Box>
                    <Box className="mb-1 flex items-center justify-between">
                      <Typography variant="body2" className="text-text-primary font-semibold">
                        Identitas &amp; Geografis Sekolah
                      </Typography>
                      <Typography variant="body2" className="text-success font-bold">
                        {operatorData?.data_completeness?.[0]?.persentase_profil_dasar || 100}% Lengkap
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={operatorData?.data_completeness?.[0]?.persentase_profil_dasar || 100}
                      color="success"
                      className="h-2 rounded-full"
                    />
                  </Box>

                  {/* Staff Info */}
                  <Box>
                    <Box className="mb-1 flex items-center justify-between">
                      <Typography variant="body2" className="text-text-primary font-semibold">
                        Profil Pendidik &amp; Kependidikan
                      </Typography>
                      <Typography variant="body2" className="text-success font-bold">
                        {operatorData?.data_completeness?.[0]?.persentase_data_guru || 100}% Lengkap
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={operatorData?.data_completeness?.[0]?.persentase_data_guru || 100}
                      color="success"
                      className="h-2 rounded-full"
                    />
                  </Box>

                  {/* Students Info */}
                  <Box>
                    <Box className="mb-1 flex items-center justify-between">
                      <Typography variant="body2" className="text-text-primary font-semibold">
                        Data Induk Siswa &amp; Rekam Wali
                      </Typography>
                      <Typography variant="body2" className="text-warning font-bold">
                        {operatorData?.data_completeness?.[0]?.persentase_data_siswa || 94}% Lengkap
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={operatorData?.data_completeness?.[0]?.persentase_data_siswa || 94}
                      color="warning"
                      className="h-2 rounded-full"
                    />
                    <Typography variant="caption" className="text-text-secondary mt-1 block">
                      ⚠️ Sebanyak 12 data NISN &amp; wali murid kelas I baru masih belum diisi lengkap.
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* RAG VECTOR DB REGULATION INGESTION LOG */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Card className="h-full shadow-sm">
              <CardContent className="flex flex-col gap-4">
                <Typography variant="h6" className="flex items-center gap-2 border-b pb-2 font-bold">
                  <SyncIcon className="text-primary" /> Log Pembaruan Regulasi RAG
                </Typography>
                <Typography variant="caption" className="text-text-secondary -mt-2 block">
                  Log penyerapan data (*ingestion*) kebijakan nasional dan panduan kurikulum baru ke dalam Vector DB
                  peladen lokal.
                </Typography>

                <Box className="mt-1 flex flex-col gap-3">
                  {[
                    { date: "14 Mei 2026", task: "Ingest PDF Panduan Kurikulum Merdeka Terkini", status: "Selesai" },
                    {
                      date: "10 Mei 2026",
                      task: "Sinkronisasi Pangkalan Capaian Pembelajaran (CP) 2025/2026",
                      status: "Selesai",
                    },
                    {
                      date: "05 Mei 2026",
                      task: "Pembaruan Aturan Evaluasi Akademik Dinas Kabupaten",
                      status: "Selesai",
                    },
                  ].map((log) => (
                    <Box
                      key={log.task}
                      className="bg-grey-500/5 border-grey-500/10 flex items-center justify-between gap-4 rounded-2xl border p-3"
                    >
                      <Box>
                        <Box className="mb-0.5 flex items-center gap-2">
                          <Typography variant="caption" className="text-primary font-bold">
                            {log.date}
                          </Typography>
                        </Box>
                        <Typography variant="body2" className="text-text-primary text-sm font-bold">
                          {log.task}
                        </Typography>
                      </Box>
                      <Chip label={log.status} size="small" color="success" className="text-xxs h-6 font-bold" />
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </>
      )}
    </Grid>
  );
}
