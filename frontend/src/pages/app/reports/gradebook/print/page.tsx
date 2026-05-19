/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import { ArrowBack as ArrowLeftIcon, Print as PrintIcon } from "@mui/icons-material";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface Student {
  full_name: string;
  nisn: string;
  nis: string;
  gender: string;
}

interface Classroom {
  name: string;
}

interface ReportScore {
  id: string;
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
  classroom?: Classroom;
  scores?: ReportScore[];
  p5?: ReportP5[];
  deep_learning?: ReportDeepLearning[];
  extracurriculars?: ReportExtracurricular[];
  attendance?: ReportAttendance;
}

export default function ReportPrintPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const id = searchParams.get("id");
  const token = localStorage.getItem("accessToken");

  const [report, setReport] = useState<StudentReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setError("ID Rapor wajib disertakan.");
      setLoading(false);
      return;
    }

    const fetchReportDetail = async () => {
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reports/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success" && json.data) {
          setReport(json.data);
        } else {
          setError(json.message || "Rapor tidak ditemukan.");
        }
      } catch (err: any) {
        setError("Gagal menghubungi server untuk memuat rapor.");
      } finally {
        setLoading(false);
      }
    };

    fetchReportDetail();
  }, [id, token]);

  const handlePrint = () => {
    window.print();
  };

  return (
    <Box className="pb-10">
      {/* FLOATING ACTION PANEL FOR PRINTING (Hidden during print) */}
      <Card className="shadow-darker-xs mb-6 border-none print:hidden">
        <CardContent className="flex items-center justify-between p-4">
          <Button
            variant="text"
            color="inherit"
            startIcon={<ArrowLeftIcon />}
            onClick={() => navigate("/reports/gradebook/scores")}
            className="font-bold"
          >
            Buku Rapor
          </Button>
          <Box className="flex gap-3">
            <Button
              variant="contained"
              color="primary"
              startIcon={<PrintIcon />}
              onClick={handlePrint}
              disabled={loading || Boolean(error) || !report}
              className="rounded-xl px-6 font-bold shadow-md"
            >
              Cetak Dokumen
            </Button>
          </Box>
        </CardContent>
      </Card>

      {loading ? (
        <Box className="mx-auto flex max-w-[800px] justify-center rounded-3xl bg-white py-20 shadow-xl">
          <CircularProgress />
        </Box>
      ) : error || !report ? (
        <Box className="mx-auto max-w-[800px] rounded-3xl bg-white p-6 shadow-xl">
          <Alert severity="error" className="mb-4">
            {error || "Terjadi kesalahan memuat dokumen rapor."}
          </Alert>
        </Box>
      ) : (
        <Paper
          className="mx-auto max-w-[800px] border border-slate-200 bg-white p-10 shadow-2xl print:m-0 print:border-none print:p-0 print:shadow-none"
          style={{ minHeight: "297mm", fontFamily: "'Inter', sans-serif" }}
        >
          {/* HEADER SEKOLAH */}
          <Box className="mb-6 text-center">
            <Typography variant="h4" className="font-extrabold tracking-tight text-slate-900 uppercase">
              UPT SDI BONERATE NO. 85 KEPULAUAN SELAYAR
            </Typography>
            <Typography variant="body2" className="font-medium text-slate-500">
              Jl. Majapahit No. 312, Desa Bonerate, Pasimarannu, Kab. Kepulauan Selayar, Sulawesi Selatan
            </Typography>
            <Typography variant="caption" className="text-slate-400">
              Status Akreditasi: Negeri • Kode Pos: 92832 • Astronomis: Lintang -7.3458 Bujur 121.1456
            </Typography>
            <Divider className="mt-4 border-2 border-slate-900" />
          </Box>

          <Typography variant="h5" align="center" className="mb-8 font-black text-slate-800 uppercase">
            LAPORAN HASIL BELAJAR (RAPOR MERDEKA)
          </Typography>

          {/* METADATA SISWA */}
          <Grid container spacing={2} className="mb-8 text-sm">
            <Grid size={{ xs: 6 }}>
              <table className="w-full border-collapse">
                <tbody>
                  <tr>
                    <td className="w-1/3 py-1 font-bold text-slate-500">Nama Siswa</td>
                    <td className="w-2/3 py-1 font-extrabold text-slate-900">: {report.student?.full_name}</td>
                  </tr>
                  <tr>
                    <td className="py-1 font-bold text-slate-500">NIS / NISN</td>
                    <td className="py-1 font-mono text-slate-800">
                      : {report.student?.nis || "-"} / {report.student?.nisn || "-"}
                    </td>
                  </tr>
                  <tr>
                    <td className="py-1 font-bold text-slate-500">Jenis Kelamin</td>
                    <td className="py-1 text-slate-800">
                      : {report.student?.gender === "L" ? "Laki-laki" : "Perempuan"}
                    </td>
                  </tr>
                </tbody>
              </table>
            </Grid>
            <Grid size={{ xs: 6 }}>
              <table className="w-full border-collapse">
                <tbody>
                  <tr>
                    <td className="w-1/3 py-1 font-bold text-slate-500">Kelas / Rombel</td>
                    <td className="w-2/3 py-1 font-bold text-slate-800">: Kelas {report.classroom?.name || "-"}</td>
                  </tr>
                  <tr>
                    <td className="py-1 font-bold text-slate-500">Semester</td>
                    <td className="py-1 text-slate-800">: {report.semester}</td>
                  </tr>
                  <tr>
                    <td className="py-1 font-bold text-slate-500">Tahun Ajaran</td>
                    <td className="py-1 text-slate-800">: 2025/2026</td>
                  </tr>
                </tbody>
              </table>
            </Grid>
          </Grid>

          {/* 1. NILAI ACADEMIC */}
          <Typography variant="subtitle1" className="mb-2 border-b-2 pb-1 font-extrabold text-slate-900 uppercase">
            A. Nilai Hasil Belajar & Capaian Kompetensi
          </Typography>
          <TableContainer component={Box} className="mb-8 overflow-hidden rounded-lg border border-slate-300">
            <Table size="small">
              <TableHead className="border-b border-slate-300 bg-slate-100">
                <TableRow>
                  <TableCell className="w-1/3 font-extrabold text-slate-800">Mata Pelajaran</TableCell>
                  <TableCell className="w-12 text-center font-extrabold text-slate-800">Nilai</TableCell>
                  <TableCell className="font-extrabold text-slate-800">Capaian Kompetensi</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {report.scores && report.scores.length > 0 ? (
                  report.scores.map((sc) => (
                    <TableRow key={sc.id} className="border-b border-slate-200">
                      <TableCell className="py-2 font-extrabold text-slate-800">{sc.subject?.subject_name}</TableCell>
                      <TableCell align="center" className="py-2 font-extrabold text-slate-900">
                        {sc.final_score}
                      </TableCell>
                      <TableCell className="py-2 text-xs leading-relaxed text-slate-700">
                        {sc.competency_achieved && (
                          <div className="mb-1">
                            <strong>Tercapai: </strong>
                            {sc.competency_achieved}
                          </div>
                        )}
                        {sc.competency_needs_improvement && (
                          <div>
                            <strong>Perlu Peningkatan: </strong>
                            {sc.competency_needs_improvement}
                          </div>
                        )}
                        {!sc.competency_achieved && !sc.competency_needs_improvement && "-"}
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={3} align="center" className="py-4 text-slate-400">
                      Belum ada nilai pelajaran.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {/* 2. P5 PROJEK */}
          <Typography variant="subtitle1" className="mb-2 border-b-2 pb-1 font-extrabold text-slate-900 uppercase">
            B. Projek Penguatan Profil Pelajar Pancasila (P5)
          </Typography>
          <TableContainer component={Box} className="mb-8 overflow-hidden rounded-lg border border-slate-300">
            <Table size="small">
              <TableHead className="border-b border-slate-300 bg-slate-100">
                <TableRow>
                  <TableCell className="w-1/3 font-extrabold text-slate-800">Tema Projek</TableCell>
                  <TableCell className="w-1/4 text-center font-extrabold text-slate-800">Capaian</TableCell>
                  <TableCell className="font-extrabold text-slate-800">Deskripsi Projek</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {report.p5 && report.p5.length > 0 ? (
                  report.p5.map((p, idx) => (
                    <TableRow key={idx} className="border-b border-slate-200">
                      <TableCell className="py-2 font-extrabold text-slate-800">{p.theme}</TableCell>
                      <TableCell align="center" className="py-2">
                        <Chip label={p.predicate} size="small" color="primary" className="text-xs font-bold" />
                      </TableCell>
                      <TableCell className="py-2 text-xs leading-relaxed text-slate-700">{p.description}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={3} align="center" className="py-4 text-slate-400">
                      Belum ada catatan projek P5.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {/* 3. EKSTRAKURIKULER */}
          <Typography variant="subtitle1" className="mb-2 border-b-2 pb-1 font-extrabold text-slate-900 uppercase">
            C. Ekstrakurikuler
          </Typography>
          <TableContainer component={Box} className="mb-8 overflow-hidden rounded-lg border border-slate-300">
            <Table size="small">
              <TableHead className="border-b border-slate-300 bg-slate-100">
                <TableRow>
                  <TableCell className="w-1/3 font-extrabold text-slate-800">Kegiatan Ekstrakurikuler</TableCell>
                  <TableCell className="w-12 text-center font-extrabold text-slate-800">Predikat</TableCell>
                  <TableCell className="font-extrabold text-slate-800">Deskripsi</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {report.extracurriculars && report.extracurriculars.length > 0 ? (
                  report.extracurriculars.map((e, idx) => (
                    <TableRow key={idx} className="border-b border-slate-200">
                      <TableCell className="py-2 font-extrabold text-slate-800">{e.activity_name}</TableCell>
                      <TableCell align="center" className="py-2 font-bold">
                        {e.predicate}
                      </TableCell>
                      <TableCell className="py-2 text-xs leading-relaxed text-slate-700">{e.description}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={3} align="center" className="py-4 text-slate-400">
                      Tidak mengikuti kegiatan ekstrakurikuler.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {/* 4. NARASI AI & CATATAN WALI KELAS */}
          <Typography variant="subtitle1" className="mb-2 border-b-2 pb-1 font-extrabold text-slate-900 uppercase">
            D. Narasi Deskripsi Karakter & Akademik (AI Assistant)
          </Typography>
          <Box className="mb-8 space-y-4 text-xs leading-relaxed text-slate-800">
            <Paper className="rounded-xl border border-slate-200 bg-slate-50/50 p-4">
              <Typography variant="subtitle2" className="mb-1 font-black text-slate-900 uppercase">
                1. Perkembangan Karakter P5
              </Typography>
              <Typography className="italic">{report.character_narrative_ai || "Belum disusun."}</Typography>
            </Paper>
            <Paper className="rounded-xl border border-slate-200 bg-slate-50/50 p-4">
              <Typography variant="subtitle2" className="mb-1 font-black text-slate-900 uppercase">
                2. Kematangan Akademik (HOTS/LOTS)
              </Typography>
              <Typography className="italic">{report.academic_narrative_ai || "Belum disusun."}</Typography>
            </Paper>
            <Paper className="rounded-xl border border-slate-200 bg-slate-50/50 p-4">
              <Typography variant="subtitle2" className="mb-1 font-black text-slate-900 uppercase">
                3. Catatan Wali Kelas & Refleksi
              </Typography>
              <Typography className="mb-2">
                <strong>Catatan Guru: </strong> {report.homeroom_notes || "-"}
              </Typography>
              <Typography>
                <strong>Refleksi Diri Murid: </strong> {report.student_reflection || "-"}
              </Typography>
            </Paper>
          </Box>

          {/* 5. KEHADIRAN & REFLEKSI */}
          <Grid container spacing={4} className="mb-12">
            <Grid size={{ xs: 6 }}>
              <Typography variant="subtitle2" className="mb-2 font-extrabold text-slate-950 uppercase">
                E. Absensi Kehadiran
              </Typography>
              <table className="w-full border border-slate-300 text-xs">
                <tbody>
                  <tr className="border-b border-slate-200">
                    <td className="p-2 font-bold text-slate-600">Sakit</td>
                    <td className="p-2 font-bold text-slate-900" align="center">
                      {report.attendance?.sick || 0} hari
                    </td>
                  </tr>
                  <tr className="border-b border-slate-200">
                    <td className="p-2 font-bold text-slate-600">Izin</td>
                    <td className="p-2 font-bold text-slate-900" align="center">
                      {report.attendance?.permission || 0} hari
                    </td>
                  </tr>
                  <tr>
                    <td className="p-2 font-bold text-slate-600">Tanpa Keterangan (Alpa)</td>
                    <td className="p-2 font-bold text-slate-900" align="center">
                      {report.attendance?.unexcused || 0} hari
                    </td>
                  </tr>
                </tbody>
              </table>
            </Grid>
            <Grid size={{ xs: 6 }}>
              {report.deep_learning && report.deep_learning.length > 0 && (
                <Box>
                  <Typography variant="subtitle2" className="mb-2 font-extrabold text-slate-950 uppercase">
                    F. Refleksi Mendalam (Deep Learning)
                  </Typography>
                  <Paper className="rounded-lg border border-slate-300 p-3 text-xs leading-relaxed">
                    <strong className="text-slate-800">{report.deep_learning[0].aspect}:</strong>
                    <div className="mt-1 text-slate-600 italic">"{report.deep_learning[0].observation_notes}"</div>
                  </Paper>
                </Box>
              )}
            </Grid>
          </Grid>

          {/* AREA TANDA TANGAN */}
          <Box className="mt-16 text-xs text-slate-800">
            <Grid container spacing={2}>
              <Grid size={{ xs: 4 }} className="text-center">
                <Typography>Mengetahui,</Typography>
                <Typography className="mb-20">Orang Tua/Wali Murid</Typography>
                <Typography className="inline-block w-40 border-b border-slate-900 pb-1 font-black">
                  ..........................................
                </Typography>
              </Grid>
              <Grid size={{ xs: 4 }} className="text-center">
                <Typography className="invisible">Space</Typography>
                <Typography className="mb-20">Kepala Satuan Pendidikan</Typography>
                <Typography className="inline-block w-40 border-b border-slate-900 pb-1 font-black">
                  H. M. Yusuf, S.Pd.
                </Typography>
                <Typography variant="caption" className="block text-slate-500">
                  NIP. 19741203 199803 1 004
                </Typography>
              </Grid>
              <Grid size={{ xs: 4 }} className="text-center">
                <Typography>
                  Bonerate, {new Date().toLocaleDateString("id-ID", { day: "numeric", month: "long", year: "numeric" })}
                </Typography>
                <Typography className="mb-20">Wali Kelas</Typography>
                <Typography className="inline-block w-40 border-b border-slate-900 pb-1 font-black">
                  Dra. Nurhayati
                </Typography>
                <Typography variant="caption" className="block text-slate-500">
                  NIP. 19680512 199307 2 001
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      )}
    </Box>
  );
}
