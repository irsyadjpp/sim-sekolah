/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  AccountBalanceOutlined,
  ArchitectureOutlined,
  AssignmentIndOutlined,
  BadgeOutlined,
  BoltOutlined,
  DomainOutlined,
  GroupsOutlined,
  HistoryEduOutlined,
  LibraryBooksOutlined,
  LocationOnOutlined,
  MenuBookOutlined,
  PersonOutline,
  SchoolOutlined,
  SignalCellularAltOutlined,
  WaterDropOutlined,
  WcOutlined,
  WifiOutlined,
} from "@mui/icons-material";
import {
  Alert,
  Avatar,
  Box,
  Breadcrumbs,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  Paper,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useThemeContext } from "@/theme/theme-provider";

interface School {
  id: string;
  npsn: string;
  school_name: string;
  address: string;
  district: string;
  regency: string;
  province: string;
  principal_name: string;
  operator_name: string;
  operating_hours: string;
  accreditation: string;
  status: string;
  phone: string;
  email: string;
  electricity_capacity: number;
  signal_status: string;
  water_source: string;
  internet_access: string;
  bos_status: string;
  curriculum: string;
  infrastructure_summary: string;
  graduation_data: string;
  teacher_pns_count: number;
  teacher_honor_count: number;
  teacher_certified_count: string;
  teacher_qualified_count: string;
  classroom_count: number;
  classroom_good_count: number;
  classroom_damaged_count: number;
  library_count: number;
  toilet_student_count: number;
  toilet_teacher_count: number;
  student_religion: string;
  student_ratio: string;
  vision: string;
  vision_meaning: string;
  mission: string;
  goal: string;
  total_students: number;
  male_students: number;
  female_students: number;
  total_teachers: number;
  male_teachers: number;
  female_teachers: number;
  education_form: string;
  country: string;
  total_staff: number;
  lab_count: number;
  rombel_count: number;
  sync_system: string;
  sync_compliance: string;
  latitude?: number;
  longitude?: number;
}

export default function Page() {
  const { t } = useTranslation();
  const { isDarkMode } = useThemeContext();
  const [school, setSchool] = useState<School | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/schools`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const json = await res.json();

      if (json.status === "success" && json.data.length > 0) {
        setSchool(json.data[0]);
      } else {
        setError("Data sekolah tidak ditemukan");
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Grid container spacing={4}>
      <Grid size={{ xs: 12 }}>
        <Typography variant="h1" component="h1" className="mb-2">
          {t("menu-school")}
        </Typography>
        <Breadcrumbs>
          <Link color="inherit" to="/home" className="hover:text-primary transition-colors">
            {t("menu-home")}
          </Link>
          <Typography color="inherit">{t("menu-institution")}</Typography>
          <Typography variant="body2">{t("menu-school")}</Typography>
        </Breadcrumbs>
      </Grid>

      {error && !loading && (
        <Grid size={{ xs: 12 }}>
          <Alert severity="error">{error}</Alert>
        </Grid>
      )}

      {/* Profil Utama */}
      <Grid size={{ xs: 12 }}>
        <Card className="border-divider relative mt-8 overflow-visible rounded-[24px] border bg-gradient-to-b from-white to-slate-50/50 shadow-md">
          <Box className="bg-primary/5 relative flex h-40 justify-center overflow-hidden rounded-t-[24px]">
            <Box className="from-primary absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] via-transparent to-transparent opacity-10" />
            <Avatar
              sx={{ width: 120, height: 120 }}
              className="bg-primary absolute -top-12 z-10 border-8 border-white text-white shadow-xl"
            >
              <SchoolOutlined sx={{ fontSize: 60 }} />
            </Avatar>
          </Box>
          <CardContent className="px-10 pt-20 pb-10">
            <Typography
              variant="h3"
              align="center"
              className="mb-2 flex justify-center font-bold tracking-tight text-slate-800 uppercase"
            >
              {loading ? <Skeleton width={320} /> : school?.school_name}
            </Typography>
            <Box className="mb-4 flex flex-wrap items-center justify-center gap-3">
              {loading ? (
                <>
                  <Skeleton width={120} height={32} />
                  <Skeleton width={100} height={32} />
                  <Skeleton width={110} height={32} />
                </>
              ) : (
                <>
                  <Chip
                    label={school?.education_form || "Sekolah Dasar (SD)"}
                    color="warning"
                    variant="filled"
                    className="font-bold shadow-sm"
                  />
                  <Chip label={`NPSN: ${school?.npsn}`} color="primary" variant="outlined" className="font-bold" />
                  <Chip
                    label={`Akreditasi: ${school?.accreditation}`}
                    color="success"
                    variant="outlined"
                    className="font-medium"
                  />
                  <Chip label={school?.status} color="info" variant="outlined" className="font-medium" />
                  <Chip
                    label={school?.curriculum}
                    icon={<LibraryBooksOutlined />}
                    color="secondary"
                    variant="outlined"
                    className="font-medium"
                  />
                </>
              )}
            </Box>
            <Typography
              variant="body1"
              color="textSecondary"
              align="center"
              className="mx-auto mb-8 flex max-w-2xl items-center justify-center gap-2"
            >
              <LocationOnOutlined fontSize="small" className="text-primary" />
              {loading ? (
                <Skeleton width={250} />
              ) : (
                `${school?.address || ""}${school?.country ? `, ${school?.country}` : ""}`
              )}
            </Typography>

            <Divider className="my-8" />

            <Grid container spacing={4} className="text-center sm:text-left">
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Box className="flex items-start gap-3">
                  <Avatar className="bg-primary/10 text-primary mt-1">
                    <PersonOutline />
                  </Avatar>
                  <Box className="grow">
                    <Typography
                      variant="caption"
                      color="textSecondary"
                      className="mb-1 block font-bold tracking-wider uppercase"
                    >
                      Kepala Sekolah
                    </Typography>
                    <Typography variant="h6" className="leading-tight font-bold text-slate-800">
                      {loading ? <Skeleton width={120} /> : school?.principal_name}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Box className="flex items-start gap-3">
                  <Avatar className="bg-secondary/10 text-secondary mt-1">
                    <AssignmentIndOutlined />
                  </Avatar>
                  <Box className="grow">
                    <Typography
                      variant="caption"
                      color="textSecondary"
                      className="mb-1 block font-bold tracking-wider uppercase"
                    >
                      Operator Sekolah
                    </Typography>
                    <Typography variant="h6" className="leading-tight font-bold text-slate-800">
                      {loading ? <Skeleton width={120} /> : school?.operator_name}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Box className="flex items-start gap-3">
                  <Avatar className="bg-warning/10 text-warning mt-1">
                    <BoltOutlined />
                  </Avatar>
                  <Box className="grow">
                    <Typography
                      variant="caption"
                      color="textSecondary"
                      className="mb-1 block font-bold tracking-wider uppercase"
                    >
                      Listrik & Energi
                    </Typography>
                    <Typography variant="h6" className="leading-tight font-bold text-slate-800">
                      {loading ? <Skeleton width={100} /> : `${school?.electricity_capacity} Watt`}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Box className="flex items-start gap-3">
                  <Avatar className="bg-info/10 text-info mt-1">
                    <SignalCellularAltOutlined />
                  </Avatar>
                  <Box className="grow">
                    <Typography
                      variant="caption"
                      color="textSecondary"
                      className="mb-1 block font-bold tracking-wider uppercase"
                    >
                      Waktu Penyelenggaraan
                    </Typography>
                    <Typography variant="h6" className="text-sm leading-tight font-bold text-slate-800">
                      {loading ? <Skeleton width={100} /> : school?.operating_hours}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>

      {/* Statistik & SDM */}
      <Grid container size={{ xs: 12 }} spacing={4}>
        <Grid size={{ xs: 12, md: 6 }}>
          <Card className="border-divider bg-primary/5 h-full rounded-[24px] border shadow-sm">
            <CardContent className="p-8">
              <Box className="mb-6 flex items-center gap-4">
                <Avatar className="bg-primary text-white shadow-lg">
                  <GroupsOutlined />
                </Avatar>
                <Box>
                  <Typography variant="h5" className="leading-tight font-bold text-slate-800">
                    Peserta Didik
                  </Typography>
                  <Typography variant="caption" className="font-medium text-slate-500">
                    Data Terupdate TA 2025/2026
                  </Typography>
                </Box>
              </Box>
              <Grid container spacing={4}>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="h2" className="text-primary mb-1 leading-none font-black">
                    {loading ? <Skeleton width={60} /> : school?.total_students}
                  </Typography>
                  <Typography
                    variant="body1"
                    color="textSecondary"
                    className="mb-4 font-bold tracking-tighter uppercase"
                  >
                    Siswa Aktif
                  </Typography>

                  <Typography variant="h4" className="mb-1 font-bold text-slate-700">
                    {loading ? <Skeleton width={50} /> : school?.rombel_count || 12}
                  </Typography>
                  <Typography variant="caption" color="textSecondary" className="font-bold tracking-tighter uppercase">
                    Rombongan Belajar
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }} className="flex flex-col justify-center">
                  <Box className="border-primary/10 mb-2 flex items-center justify-between rounded-xl border bg-white/60 p-3">
                    <Typography variant="body2" className="text-slate-600">
                      Laki-laki
                    </Typography>
                    <Typography variant="body2" className="text-primary font-bold">
                      {loading ? <Skeleton width={30} /> : school?.male_students}
                    </Typography>
                  </Box>
                  <Box className="border-primary/10 flex items-center justify-between rounded-xl border bg-white/60 p-3">
                    <Typography variant="body2" className="text-slate-600">
                      Perempuan
                    </Typography>
                    <Typography variant="body2" className="text-primary font-bold">
                      {loading ? <Skeleton width={30} /> : school?.female_students}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
              <Divider className="my-6" />
              <Grid container spacing={2}>
                <Grid size={{ xs: 6 }}>
                  <Box className="flex items-center gap-2">
                    <WcOutlined fontSize="small" className="text-primary/60" />
                    <Typography variant="body2" className="text-slate-600">
                      Agama: <strong>{loading ? <Skeleton width={60} /> : school?.student_religion}</strong>
                    </Typography>
                  </Box>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Box className="flex items-center gap-2">
                    <HistoryEduOutlined fontSize="small" className="text-primary/60" />
                    <Typography variant="body2" className="text-slate-600">
                      Rasio: <strong>{loading ? <Skeleton width={40} /> : school?.student_ratio}</strong>
                    </Typography>
                  </Box>
                </Grid>
                <Grid size={{ xs: 12 }}>
                  {loading ? (
                    <Skeleton width="100%" height={40} />
                  ) : (
                    <Alert
                      icon={<SchoolOutlined fontSize="small" />}
                      severity="info"
                      className="bg-primary/10 text-primary rounded-xl border-none font-medium"
                    >
                      {school?.graduation_data}
                    </Alert>
                  )}
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Card className="border-divider bg-success/5 h-full rounded-[24px] border shadow-sm">
            <CardContent className="p-8">
              <Box className="mb-6 flex items-center gap-4">
                <Avatar className="bg-success text-white shadow-lg">
                  <BadgeOutlined />
                </Avatar>
                <Box>
                  <Typography variant="h5" className="leading-tight font-bold text-slate-800">
                    Sumber Daya Manusia (PTK)
                  </Typography>
                  <Typography variant="caption" className="font-medium text-slate-500">
                    Total PTK:{" "}
                    {loading ? (
                      <Skeleton width={60} />
                    ) : (
                      `${(school?.total_teachers || 0) + (school?.total_staff || 0)}`
                    )}{" "}
                    Orang
                  </Typography>
                </Box>
              </Box>
              <Grid container spacing={4}>
                <Grid size={{ xs: 6 }}>
                  <Box className="flex flex-col gap-4">
                    <Box>
                      <Typography variant="h4" className="text-success leading-none font-black">
                        {loading ? <Skeleton width={40} /> : school?.total_teachers}
                      </Typography>
                      <Typography variant="caption" className="font-bold tracking-widest text-slate-500 uppercase">
                        Guru Pengajar
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h4" className="leading-none font-black text-indigo-600">
                        {loading ? <Skeleton width={40} /> : school?.total_staff || 4}
                      </Typography>
                      <Typography variant="caption" className="font-bold tracking-widest text-slate-500 uppercase">
                        Pegawai (Tendik)
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid size={{ xs: 6 }} className="flex flex-col justify-center">
                  <Box className="border-success/10 mb-2 flex items-center justify-between rounded-xl border bg-white/60 p-3">
                    <Typography variant="body2" className="text-slate-600">
                      PNS/PPPK
                    </Typography>
                    <Typography variant="body2" className="text-success font-bold">
                      {loading ? <Skeleton width={30} /> : school?.teacher_pns_count}
                    </Typography>
                  </Box>
                  <Box className="border-success/10 mb-2 flex items-center justify-between rounded-xl border bg-white/60 p-3">
                    <Typography variant="body2" className="text-slate-600">
                      Honorer
                    </Typography>
                    <Typography variant="body2" className="text-success font-bold">
                      {loading ? <Skeleton width={30} /> : school?.teacher_honor_count}
                    </Typography>
                  </Box>
                  <Box className="border-success/10 flex items-center justify-between rounded-xl border bg-white/60 p-3 text-xs">
                    <Typography variant="body2" className="font-medium text-slate-500">
                      {loading ? (
                        <Skeleton width={60} />
                      ) : (
                        `L: ${school?.male_teachers} | P: ${school?.female_teachers}`
                      )}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
              <Divider className="my-6" />
              <Grid container spacing={2}>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" className="text-slate-600">
                    Kualifikasi S1:{" "}
                    <strong>{loading ? <Skeleton width={60} /> : school?.teacher_qualified_count}</strong>
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" className="text-slate-600">
                    Tersertifikasi:{" "}
                    <strong>{loading ? <Skeleton width={60} /> : school?.teacher_certified_count}</strong>
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Visi & Misi */}
      <Grid container size={{ xs: 12 }} spacing={4}>
        <Grid size={{ xs: 12, md: 6 }}>
          <Card className="border-divider border-l-primary h-full rounded-[24px] border border-l-8 bg-white shadow-sm transition-all hover:shadow-md">
            <CardContent className="p-8">
              <Box className="mb-6 flex items-center gap-4">
                <Avatar className="bg-primary/10 text-primary">
                  <MenuBookOutlined />
                </Avatar>
                <Typography variant="h4" className="font-bold text-slate-800">
                  Visi Sekolah
                </Typography>
              </Box>
              <Typography variant="h5" className="mb-8 leading-relaxed font-medium text-slate-700 italic">
                {loading ? <Skeleton width="100%" /> : `"${school?.vision}"`}
              </Typography>
              <Box className="rounded-2xl border border-slate-100 bg-slate-50 p-6">
                <Typography
                  variant="subtitle2"
                  className="text-primary mb-4 text-[10px] font-bold tracking-[0.2em] uppercase"
                >
                  Filosofi & Makna Visi
                </Typography>
                <Typography variant="body2" className="leading-relaxed whitespace-pre-line text-slate-600">
                  {loading ? (
                    <>
                      <Skeleton width="100%" />
                      <Skeleton width="100%" />
                      <Skeleton width="90%" />
                    </>
                  ) : (
                    school?.vision_meaning
                  )}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 6 }}>
          <Card className="border-divider border-l-secondary h-full rounded-[24px] border border-l-8 bg-white shadow-sm transition-all hover:shadow-md">
            <CardContent className="p-8">
              <Box className="mb-6 flex items-center gap-4">
                <Avatar className="bg-secondary/10 text-secondary">
                  <DomainOutlined />
                </Avatar>
                <Typography variant="h4" className="font-bold text-slate-800">
                  Misi & Tujuan
                </Typography>
              </Box>
              <Box className="mb-8">
                <Typography
                  variant="subtitle2"
                  className="text-secondary mb-4 text-[10px] font-bold tracking-[0.2em] uppercase"
                >
                  Misi Strategis
                </Typography>
                <Typography variant="body2" className="leading-relaxed whitespace-pre-line text-slate-600">
                  {loading ? (
                    <>
                      <Skeleton width="100%" />
                      <Skeleton width="100%" />
                      <Skeleton width="100%" />
                      <Skeleton width="85%" />
                    </>
                  ) : (
                    school?.mission
                  )}
                </Typography>
              </Box>
              <Box className="bg-secondary/5 border-secondary/10 rounded-2xl border p-6">
                <Typography
                  variant="subtitle2"
                  className="text-secondary mb-2 text-[10px] font-bold tracking-[0.2em] uppercase"
                >
                  Output yang Diharapkan
                </Typography>
                <Typography variant="body2" className="leading-relaxed font-medium text-slate-700">
                  {loading ? <Skeleton width="100%" /> : school?.goal}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Rasio Pendidikan & Sinkronisasi Dapodik */}
      <Grid container size={{ xs: 12 }} spacing={4}>
        <Grid size={{ xs: 12, md: 6 }}>
          <Card className="border-divider h-full rounded-[24px] border bg-gradient-to-tr from-indigo-50/70 via-white to-white p-6 shadow-md">
            <CardContent>
              <Box className="mb-6 flex items-center gap-3">
                <Avatar className="bg-indigo-600 text-white">
                  <HistoryEduOutlined />
                </Avatar>
                <Typography variant="h4" className="font-bold text-slate-800">
                  Rasio & Efektivitas Pendidikan
                </Typography>
              </Box>

              <Box className="relative mb-6 rounded-2xl border border-slate-100 bg-slate-50 p-5">
                <Typography
                  variant="subtitle2"
                  className="mb-2 block text-[9px] font-bold tracking-widest text-indigo-600 uppercase"
                >
                  Rasio Guru terhadap Rombel
                </Typography>
                <Typography variant="h5" className="mb-2 font-mono font-black text-slate-800">
                  {loading ? (
                    <Skeleton width={180} />
                  ) : (
                    `${school?.total_teachers || 20} Guru / ${school?.rombel_count || 12} Rombel ≈ ${((school?.total_teachers || 20) / (school?.rombel_count || 12)).toFixed(2)}`
                  )}
                </Typography>
                <Typography variant="body2" className="leading-relaxed text-slate-600 italic">
                  Artinya, ketersediaan guru sangat mencukupi, rata-rata terdapat 1 hingga 2 guru untuk menangani setiap
                  rombel.
                </Typography>
              </Box>

              <Box className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
                <Typography
                  variant="subtitle2"
                  className="mb-2 block text-[9px] font-bold tracking-widest text-indigo-600 uppercase"
                >
                  Rasio Guru terhadap Siswa
                </Typography>
                <Typography variant="h5" className="mb-2 font-mono font-black text-slate-800">
                  {loading ? (
                    <Skeleton width={180} />
                  ) : (
                    `${school?.total_students || 251} Siswa / ${school?.total_teachers || 20} Guru ≈ ${((school?.total_students || 251) / (school?.total_teachers || 20)).toFixed(2)}`
                  )}
                </Typography>
                <Typography variant="body2" className="leading-relaxed text-slate-600 italic">
                  Artinya, setiap 1 orang guru secara statistik membimbing 12-13 siswa. Jauh di bawah batas maksimal
                  nasional (1:28), menandakan perhatian guru ke siswa sangat tinggi.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Card className="border-divider h-full rounded-[24px] border bg-gradient-to-tr from-emerald-50/70 via-white to-white p-6 shadow-md">
            <CardContent>
              <Box className="mb-6 flex items-center gap-3">
                <Avatar className="bg-emerald-600 text-white">
                  <SignalCellularAltOutlined />
                </Avatar>
                <Typography variant="h4" className="font-bold text-slate-800">
                  Sinkronisasi Data Pusat
                </Typography>
              </Box>

              <Box className="mb-6 rounded-2xl border border-slate-100 bg-slate-50 p-5">
                <Typography
                  variant="subtitle2"
                  className="mb-1 text-[9px] font-bold tracking-widest text-slate-500 uppercase"
                >
                  Sistem Sumber Data
                </Typography>
                <Typography variant="h6" className="mb-2 font-bold text-slate-800">
                  {loading ? (
                    <Skeleton width={200} />
                  ) : (
                    school?.sync_system || "Dapodikdasmen (Data Pokok Pendidikan Dasar dan Menengah)"
                  )}
                </Typography>
                <Typography variant="body2" className="text-slate-600">
                  Pusat basis data integrasi resmi Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi
                  (Kemendikbudristek).
                </Typography>
              </Box>

              <Box className="flex items-start gap-4 rounded-2xl border border-emerald-100 bg-emerald-50/50 p-5">
                <Chip label="ONLINE" color="success" size="small" className="mt-1 font-extrabold" />
                <Box className="grow">
                  <Typography
                    variant="subtitle2"
                    className="mb-1 text-[9px] font-bold tracking-widest text-emerald-800 uppercase"
                  >
                    Kepatuhan Sinkronisasi
                  </Typography>
                  <Typography variant="body2" className="leading-relaxed font-semibold text-slate-700">
                    {loading ? <Skeleton width="100%" /> : school?.sync_compliance || "Aktif melakukan pengiriman data"}
                  </Typography>
                  <Typography variant="caption" color="textSecondary" className="mt-1 block">
                    Diperbarui berkala secara otomatis untuk integrasi Dana BOS dan validasi tunjangan PTK.
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Sarana & Fasilitas */}
      <Grid size={{ xs: 12 }}>
        <Card
          className={`border-divider relative overflow-hidden rounded-[24px] border shadow-sm transition-colors ${
            isDarkMode ? "bg-slate-900 text-white" : "bg-slate-50 text-slate-800"
          }`}
        >
          <Box className="bg-primary absolute top-0 right-0 -mt-32 -mr-32 h-64 w-64 rounded-full opacity-5" />
          <CardContent className="relative z-10 p-10">
            <Box className="mb-10 flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
              <Box className="grow">
                <Typography variant="h3" className="mb-2 flex items-center gap-3 font-bold">
                  <ArchitectureOutlined sx={{ fontSize: 40 }} /> Sarana & Prasarana
                </Typography>
                <Typography variant="body1" className={`max-w-2xl ${isDarkMode ? "text-slate-400" : "text-slate-600"}`}>
                  {loading ? (
                    <>
                      <Skeleton width="100%" />
                      <Skeleton width="85%" />
                    </>
                  ) : (
                    school?.infrastructure_summary
                  )}
                </Typography>
              </Box>
              <Chip label="Persentase Layak: 100%" color="success" className="h-10 px-4 text-sm font-bold" />
            </Box>

            <Grid container spacing={3}>
              <Grid size={{ xs: 12, md: 8 }}>
                <TableContainer
                  component={Paper}
                  className={`rounded-2xl border shadow-none ${
                    isDarkMode ? "border-slate-700 bg-slate-800/50" : "border-slate-200 bg-white"
                  }`}
                >
                  <Table size="small">
                    <TableBody>
                      <TableRow>
                        <TableCell
                          className={`font-medium ${isDarkMode ? "border-slate-700 text-slate-400" : "border-slate-200 text-slate-500"}`}
                        >
                          Ruang Kelas
                        </TableCell>
                        <TableCell
                          className={`font-bold ${isDarkMode ? "border-slate-700 text-white" : "border-slate-200 text-slate-800"}`}
                        >
                          {loading ? (
                            <Skeleton width="100%" />
                          ) : (
                            `${school?.classroom_count} Unit (Tersedia & Digunakan Penuh, ${school?.classroom_good_count} Baik, ${school?.classroom_damaged_count} Rusak Ringan)`
                          )}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell
                          className={`font-medium ${isDarkMode ? "border-slate-700 text-slate-400" : "border-slate-200 text-slate-500"}`}
                        >
                          Ruang Laboratorium
                        </TableCell>
                        <TableCell
                          className={`font-bold ${isDarkMode ? "border-slate-700 text-white" : "border-slate-200 text-slate-800"}`}
                        >
                          {loading ? <Skeleton width={150} /> : `${school?.lab_count || 0} Unit (Belum Tersedia)`}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell
                          className={`font-medium ${isDarkMode ? "border-slate-700 text-slate-400" : "border-slate-200 text-slate-500"}`}
                        >
                          Ruang Perpustakaan
                        </TableCell>
                        <TableCell
                          className={`font-bold ${isDarkMode ? "border-slate-700 text-white" : "border-slate-200 text-slate-800"}`}
                        >
                          {loading ? <Skeleton width={150} /> : `${school?.library_count || 0} Unit (Belum Tersedia)`}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell
                          className={`font-medium ${isDarkMode ? "border-slate-700 text-slate-400" : "border-slate-200 text-slate-500"}`}
                        >
                          Sanitasi (Toilet)
                        </TableCell>
                        <TableCell
                          className={`font-bold ${isDarkMode ? "border-slate-700 text-white" : "border-slate-200 text-slate-800"}`}
                        >
                          {loading ? (
                            <Skeleton width={180} />
                          ) : (
                            `Siswa: ${school?.toilet_student_count} Unit | Guru: ${school?.toilet_teacher_count} Unit`
                          )}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
              <Grid size={{ xs: 12, md: 4 }}>
                <Box className="grid h-full grid-cols-2 gap-3">
                  <Box
                    className={`flex flex-col justify-center rounded-2xl border p-4 ${
                      isDarkMode ? "border-slate-700 bg-slate-800/80" : "border-slate-200 bg-white"
                    }`}
                  >
                    <WifiOutlined className="text-primary mb-2" />
                    <Typography
                      variant="caption"
                      className={`mb-2 block text-[8px] font-bold tracking-widest uppercase ${isDarkMode ? "text-slate-500" : "text-slate-400"}`}
                    >
                      Akses Internet
                    </Typography>
                    <Typography
                      variant="body2"
                      className={`leading-tight font-bold ${isDarkMode ? "text-white" : "text-slate-800"}`}
                    >
                      {loading ? <Skeleton width={80} /> : school?.internet_access}
                    </Typography>
                  </Box>
                  <Box
                    className={`flex flex-col justify-center rounded-2xl border p-4 ${
                      isDarkMode ? "border-slate-700 bg-slate-800/80" : "border-slate-200 bg-white"
                    }`}
                  >
                    <WaterDropOutlined className="mb-2 text-cyan-400" />
                    <Typography
                      variant="caption"
                      className={`mb-2 block text-[8px] font-bold tracking-widest uppercase ${isDarkMode ? "text-slate-500" : "text-slate-400"}`}
                    >
                      Sumber Air
                    </Typography>
                    <Typography
                      variant="body2"
                      className={`leading-tight font-bold ${isDarkMode ? "text-white" : "text-slate-800"}`}
                    >
                      {loading ? <Skeleton width={80} /> : school?.water_source}
                    </Typography>
                  </Box>
                  <Box
                    className={`flex flex-col justify-center rounded-2xl border p-4 ${
                      isDarkMode ? "border-slate-700 bg-slate-800/80" : "border-slate-200 bg-white"
                    }`}
                  >
                    <AccountBalanceOutlined className="mb-2 text-indigo-400" />
                    <Typography
                      variant="caption"
                      className={`mb-2 block text-[8px] font-bold tracking-widest uppercase ${isDarkMode ? "text-slate-500" : "text-slate-400"}`}
                    >
                      Pembiayaan BOS
                    </Typography>
                    <Typography
                      variant="body2"
                      className={`leading-tight font-bold ${isDarkMode ? "text-white" : "text-slate-800"}`}
                    >
                      {loading ? <Skeleton width={80} /> : school?.bos_status}
                    </Typography>
                  </Box>
                  <Box
                    className={`flex flex-col justify-center rounded-2xl border p-4 ${
                      isDarkMode ? "border-slate-700 bg-slate-800/80" : "border-slate-200 bg-white"
                    }`}
                  >
                    <LocationOnOutlined className="mb-2 text-rose-400" />
                    <Typography
                      variant="caption"
                      className={`mb-2 block text-[8px] font-bold tracking-widest uppercase ${isDarkMode ? "text-slate-500" : "text-slate-400"}`}
                    >
                      Koordinat
                    </Typography>
                    <Typography
                      variant="body2"
                      className={`text-xs leading-tight font-bold ${isDarkMode ? "text-white" : "text-slate-800"}`}
                    >
                      {loading ? <Skeleton width={120} /> : `L: ${school?.latitude} / B: ${school?.longitude}`}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
