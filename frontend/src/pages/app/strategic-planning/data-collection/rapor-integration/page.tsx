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
  Divider,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  LinearProgress,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiRefresh from "@/icons/nexture/ni-refresh";
import NiSync from "@/icons/nexture/ni-sync";
import NiCheckCircle from "@/icons/nexture/ni-check-circle";
import NiXCircle from "@/icons/nexture/ni-x-circle";
import NiDownload from "@/icons/nexture/ni-download";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TablePagination from "@mui/material/TablePagination";
import TableSortLabel from "@mui/material/TableSortLabel";

interface RaporData {
  id: string;
  student_id: string;
  student_name: string;
  nisn: string;
  class_grade: string;
  academic_year: string;
  literacy_score: number;
  numeracy_score: number;
  character_score: number;
  sync_date: string;
}

interface SyncStatus {
  npsn: string;
  status: "idle" | "syncing" | "completed" | "failed";
  progress: number;
  message?: string;
  last_sync?: string;
}

function RaporIntegrationPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [syncStatus, setSyncStatus] = useState<SyncStatus>({
    npsn: "",
    status: "idle",
    progress: 0,
  });
  const [error, setError] = useState<string | null>(null);
  const [raporData, setRaporData] = useState<RaporData[]>([]);
  const [selectedYear, setSelectedYear] = useState("all");

  const ACADEMIC_YEARS = [
    { value: "all", label: "Semua Tahun" },
    { value: "2024-2025", label: "2024-2025" },
    { value: "2023-2024", label: "2023-2024" },
    { value: "2022-2023", label: "2022-2023" },
  ];

  const { paginatedData, page, limit, total, handlePageChange, handleLimitChange } = useClientTable({
    key: "rapor_data",
    data: raporData,
    defaultLimit: 10,
  });

  const handleNPSNSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!syncStatus.npsn || syncStatus.npsn.length !== 8) {
      setError("NPSN harus 8 digit angka");
      return;
    }

    setSyncStatus((prev) => ({ ...prev, status: "syncing", progress: 0, message: "Memulai sinkronisasi..." }));
    setError(null);

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/rapor/sync`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ npsn: syncStatus.npsn }),
      });

      const json = await res.json();

      if (json.status === "success") {
        setSyncStatus((prev) => ({
          ...prev,
          status: "completed",
          progress: 100,
          message: "Sinkronisasi berhasil!",
          last_sync: new Date().toISOString(),
        }));
        setRaporData(json.data || []);
      } else {
        setSyncStatus((prev) => ({
          ...prev,
          status: "failed",
          message: json.message || "Sinkronisasi gagal",
        }));
        setError(json.message || "Sinkronisasi gagal");
      }
    } catch (err: any) {
      setSyncStatus((prev) => ({
        ...prev,
        status: "failed",
        message: err.message || "Network error",
      }));
      setError(err.message || "Network error");
    }
  };

  const handleManualRefresh = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/strategic-planning/rapor/data?limit=1000&year=${selectedYear}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const json = await res.json();
      if (json.status === "success") {
        setRaporData(json.data || []);
      } else {
        setError(json.message || "Failed to refresh data");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  const exportData = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/strategic-planning/rapor/export?year=${selectedYear}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `rapor_data_${selectedYear}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        setError("Failed to export data");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  useEffect(() => {
    handleManualRefresh();
  }, [selectedYear]);

  const getScoreColor = (score: number) => {
    if (score >= 80) return "success";
    if (score >= 60) return "warning";
    return "error";
  };

  const calculateStats = () => {
    if (raporData.length === 0) {
      return { avgLiteracy: 0, avgNumeracy: 0, avgCharacter: 0 };
    }

    const totalLiteracy = raporData.reduce((sum, d) => sum + (d.literacy_score || 0), 0);
    const totalNumeracy = raporData.reduce((sum, d) => sum + (d.numeracy_score || 0), 0);
    const totalCharacter = raporData.reduce((sum, d) => sum + (d.character_score || 0), 0);

    return {
      avgLiteracy: (totalLiteracy / raporData.length).toFixed(1),
      avgNumeracy: (totalNumeracy / raporData.length).toFixed(1),
      avgCharacter: (totalCharacter / raporData.length).toFixed(1),
    };
  };

  const stats = calculateStats();

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Integrasi API Rapor Pendidikan
        </Typography>
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            startIcon={<NiRefresh size="small" />}
            onClick={handleManualRefresh}
            disabled={loading}
          >
            Refresh Data
          </Button>
          <Button
            variant="contained"
            startIcon={<NiDownload size="small" />}
            onClick={exportData}
          >
            Export Data
          </Button>
        </Stack>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Typography variant="body2">Integrasi Rapor</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Grid container spacing={3} className="mb-6">
        <Grid size={{ xs: 12, md: 8 }}>
          <Card>
            <CardContent className="p-6">
              <Typography variant="h5" className="mb-4 font-bold">
                Sinkronisasi Data Rapor
              </Typography>
              <form onSubmit={handleNPSNSubmit}>
                <Grid container spacing={3} alignItems="flex-end">
                  <Grid size={{ xs: 12, md: 6 }}>
                    <FormControl fullWidth>
                      <InputLabel>NPSN Sekolah</InputLabel>
                      <TextField
                        fullWidth
                        label="NPSN Sekolah"
                        value={syncStatus.npsn}
                        onChange={(e) => {
                          const value = e.target.value.replace(/\D/g, "").slice(0, 8);
                          setSyncStatus((prev) => ({ ...prev, npsn: value }));
                        }}
                        inputProps={{ maxLength: 8 }}
                        placeholder="Masukkan 8 digit NPSN"
                        disabled={syncStatus.status === "syncing"}
                      />
                    </FormControl>
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Button
                      type="submit"
                      variant="contained"
                      fullWidth
                      startIcon={<NiSync size="small" />}
                      disabled={syncStatus.status === "syncing" || !syncStatus.npsn || syncStatus.npsn.length !== 8}
                    >
                      {syncStatus.status === "syncing" ? "Sinkronisasi..." : "Sinkronkan Data"}
                    </Button>
                  </Grid>
                </Grid>
              </form>

              {syncStatus.status !== "idle" && (
                <Box className="mt-4">
                  <Box className="flex justify-between items-center mb-2">
                    <Typography variant="body2" className="flex items-center gap-2">
                      {syncStatus.status === "syncing" && <CircularProgress size={16} />}
                      {syncStatus.status === "syncing" && "Sinkronisasi berlangsung..."}
                      {syncStatus.status === "completed" && <NiCheckCircle color="success" />}
                      {syncStatus.status === "completed" && "Sinkronisasi selesai"}
                      {syncStatus.status === "failed" && <NiXCircle color="error" />}
                      {syncStatus.status === "failed" && "Sinkronisasi gagal"}
                    </Typography>
                    <Typography variant="caption">{syncStatus.progress}%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={syncStatus.progress}
                    color={syncStatus.status === "failed" ? "error" : "primary"}
                  />
                  {syncStatus.message && (
                    <Typography variant="caption" className="mt-2 block text-text-secondary">
                      {syncStatus.message}
                    </Typography>
                  )}
                  {syncStatus.last_sync && (
                    <Typography variant="caption" className="mt-1 block text-text-secondary">
                      Terakhir sinkron: {new Date(syncStatus.last_sync).toLocaleString("id-ID")}
                    </Typography>
                  )}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent className="p-6">
              <Typography variant="h5" className="mb-4 font-bold">
                Indikator Capaian
              </Typography>
              <Stack spacing={4}>
                <Box>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Rata-rata Literasi
                  </Typography>
                  <Typography variant="h3" className="font-bold">
                    {stats.avgLiteracy}
                  </Typography>
                  <Typography variant="caption" className="text-text-secondary">
                    dari {raporData.length} siswa
                  </Typography>
                </Box>
                <Divider />
                <Box>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Rata-rata Numerasi
                  </Typography>
                  <Typography variant="h3" className="font-bold">
                    {stats.avgNumeracy}
                  </Typography>
                  <Typography variant="caption" className="text-text-secondary">
                    dari {raporData.length} siswa
                  </Typography>
                </Box>
                <Divider />
                <Box>
                  <Typography variant="subtitle2" className="text-text-secondary mb-1">
                    Rata-rata Karakter
                  </Typography>
                  <Typography variant="h3" className="font-bold">
                    {stats.avgCharacter}
                  </Typography>
                  <Typography variant="caption" className="text-text-secondary">
                    dari {raporData.length} siswa
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card className="mb-6">
        <CardContent className="p-4">
          <Typography variant="h6" className="mb-4 font-bold">
            Perbandingan Historis
          </Typography>
          <Typography variant="body2" className="text-text-secondary">
            Chart placeholder - Perbandingan capaian literasi, numerasi, dan karakter antar tahun ajaran
          </Typography>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-4">
          <Box className="flex justify-between items-center mb-4">
            <Typography variant="h6" className="font-bold">
              Data Rapor ({raporData.length} siswa)
            </Typography>
            <Stack direction="row" spacing={2}>
              {ACADEMIC_YEARS.map((year) => (
                <Button
                  key={year.value}
                  size="small"
                  variant={selectedYear === year.value ? "contained" : "outlined"}
                  onClick={() => setSelectedYear(year.value)}
                >
                  {year.label}
                </Button>
              ))}
            </Stack>
          </Box>

          {loading ? (
            <Box className="flex justify-center items-center py-12">
              <CircularProgress size={48} />
            </Box>
          ) : raporData.length === 0 ? (
            <Typography variant="body2" className="text-text-secondary text-center py-12">
              Belum ada data rapor. Lakukan sinkronisasi dengan memasukkan NPSN sekolah.
            </Typography>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell className="font-bold">Nama Siswa</TableCell>
                    <TableCell className="font-bold">NISN</TableCell>
                    <TableCell className="font-bold">Kelas</TableCell>
                    <TableCell className="font-bold">Literasi</TableCell>
                    <TableCell className="font-bold">Numerasi</TableCell>
                    <TableCell className="font-bold">Karakter</TableCell>
                    <TableCell className="font-bold">Tanggal Sync</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {paginatedData.map((data) => (
                    <TableRow key={data.id} hover>
                      <TableCell>
                        <Typography variant="body2" className="font-medium">
                          {data.student_name}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{data.nisn}</Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{data.class_grade}</Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={data.literacy_score.toFixed(1)}
                          size="small"
                          color={getScoreColor(data.literacy_score) as any}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={data.numeracy_score.toFixed(1)}
                          size="small"
                          color={getScoreColor(data.numeracy_score) as any}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={data.character_score.toFixed(1)}
                          size="small"
                          color={getScoreColor(data.character_score) as any}
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {new Date(data.sync_date).toLocaleDateString("id-ID", {
                            day: "numeric",
                            month: "long",
                            year: "numeric",
                          })}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <TablePagination
                rowsPerPageOptions={[5, 10, 25, 50]}
                component="div"
                count={total}
                rowsPerPage={limit}
                page={page}
                onPageChange={handlePageChange}
                onRowsPerPageChange={handleLimitChange}
                labelRowsPerPage="Baris per halaman:"
                labelDisplayedRows={({ from, to, count }) => `${from}-${to} dari ${count}`}
              />
            </TableContainer>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}

export default function RaporIntegrationPageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "OPERATOR"]}>
      <RaporIntegrationPage />
    </PermissionGuard>
  );
}