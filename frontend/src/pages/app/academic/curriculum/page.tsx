import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  FormControl,
  Grid,
  IconButton,
  InputAdornment,
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
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

interface LearningOutcome {
  id: string;
  cp_code: string;
  outcome_text: string;
  phase: { phase_name: string };
  subject: { subject_name: string };
}

export default function Page() {
  const navigate = useNavigate();
  const [data, setData] = useState<LearningOutcome[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filterSubject, setFilterSubject] = useState("Semua");
  const [filterPhase, setFilterPhase] = useState("Semua");
  const [searchQuery, setSearchQuery] = useState("");

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-outcomes?limit=10000`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        console.log("CP Data:", json.data);
        setData(json.data || []);
      } else {
        setError(json.message || "Failed to fetch data");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  const [subjects, setSubjects] = useState<string[]>(() => {
    try {
      const cached = localStorage.getItem("master_subjects");
      return cached ? JSON.parse(cached) : ["Semua"];
    } catch {
      return ["Semua"];
    }
  });

  const [phases, setPhases] = useState<string[]>(() => {
    try {
      const cached = localStorage.getItem("master_phases");
      return cached ? JSON.parse(cached) : ["Semua"];
    } catch {
      return ["Semua"];
    }
  });

  const fetchMasterData = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const [phaseRes, subjectRes] = await Promise.all([
        fetch(`${DEFAULTS.API_URL}/api/v1/phases?limit=100`, { headers: { Authorization: `Bearer ${token}` } }),
        fetch(`${DEFAULTS.API_URL}/api/v1/subjects?limit=100`, { headers: { Authorization: `Bearer ${token}` } }),
      ]);

      const phaseJson = await phaseRes.json();
      const subjectJson = await subjectRes.json();

      if (phaseJson.status === "success" && Array.isArray(phaseJson.data)) {
        const phaseNames = ["Semua", ...phaseJson.data.map((p: any) => p.phase_name)];
        setPhases(phaseNames);
        localStorage.setItem("master_phases", JSON.stringify(phaseNames));
      }

      if (subjectJson.status === "success" && Array.isArray(subjectJson.data)) {
        const subjectNames = ["Semua", ...subjectJson.data.map((s: any) => s.subject_name)];
        setSubjects(subjectNames);
        localStorage.setItem("master_subjects", JSON.stringify(subjectNames));
      }
    } catch (err) {
      console.error("Failed to fetch master data", err);
    }
  };

  useEffect(() => {
    fetchData();
    fetchMasterData();
  }, []);

  const filteredData = useMemo(() => {
    return data.filter((d) => {
      const subjName = d.subject?.subject_name || "";
      const phaseName = d.phase?.phase_name || "";
      const outcomeText = d.outcome_text || "";
      const cpCode = d.cp_code || "";

      const matchSubject = filterSubject === "Semua" || subjName === filterSubject;
      const matchPhase = filterPhase === "Semua" || phaseName === filterPhase;
      const matchSearch =
        subjName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        outcomeText.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cpCode.toLowerCase().includes(searchQuery.toLowerCase());
      return matchSubject && matchPhase && matchSearch;
    });
  }, [data, filterSubject, filterPhase, searchQuery]);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "curriculum", data: filteredData, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Capaian Pembelajaran (CP)
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => navigate("/academic/curriculum/create")}
        >
          Tambah CP Baru
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Capaian Pembelajaran</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="p-4">
          <Grid container spacing={3} alignItems="flex-end">
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                fullWidth
                placeholder="Cari kode atau teks CP..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                size="small"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <NiSearch size="small" />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 4 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Mata Pelajaran</InputLabel>
                <Select
                  value={filterSubject}
                  label="Mata Pelajaran"
                  onChange={(e) => setFilterSubject(e.target.value)}
                  IconComponent={NiChevronDownSmall}
                >
                  {subjects.map((s) => (
                    <MenuItem key={s} value={s}>
                      {s}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 4 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Fase</InputLabel>
                <Select
                  value={filterPhase}
                  label="Fase"
                  onChange={(e) => setFilterPhase(e.target.value)}
                  IconComponent={NiChevronDownSmall}
                >
                  {phases.map((p) => (
                    <MenuItem key={p} value={p}>
                      {p}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell className="font-bold" sortDirection={sortBy === "subject.subject_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "subject.subject_name"}
                  direction={sortBy === "subject.subject_name" ? sortDir : "asc"}
                  onClick={() => handleSort("subject.subject_name")}
                >
                  Mata Pelajaran
                </TableSortLabel>
              </TableCell>
              <TableCell
                align="center"
                className="font-bold"
                sortDirection={sortBy === "phase.phase_name" ? sortDir : false}
              >
                <TableSortLabel
                  active={sortBy === "phase.phase_name"}
                  direction={sortBy === "phase.phase_name" ? sortDir : "asc"}
                  onClick={() => handleSort("phase.phase_name")}
                >
                  Fase
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "outcome_text" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "outcome_text"}
                  direction={sortBy === "outcome_text" ? sortDir : "asc"}
                  onClick={() => handleSort("outcome_text")}
                >
                  Capaian Pembelajaran
                </TableSortLabel>
              </TableCell>
              <TableCell align="center" className="font-bold">
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
              paginatedData.map((d) => (
                <TableRow key={d.id} hover>
                  <TableCell>
                    <Typography variant="body2" className="font-bold">
                      {d.subject?.subject_name || "Tanpa Mapel"}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {d.cp_code}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Chip label={d.phase?.phase_name || "-"} size="small" color="primary" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" className="line-clamp-2">
                      {d.outcome_text || "-"}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      size="small"
                      color="info"
                      onClick={() => navigate(`/academic/curriculum/details?id=${d.id}`)}
                      title="Detail CP"
                    >
                      <NiEyeOpen size="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => navigate(`/academic/curriculum/objectives?cpId=${d.id}`)}
                      title="Kelola TP"
                    >
                      <NiChevronDownSmall size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Tidak ada data capaian pembelajaran.
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
    </Box>
  );
}
