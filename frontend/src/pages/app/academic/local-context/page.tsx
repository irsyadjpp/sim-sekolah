import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiStar from "@/icons/nexture/ni-star";

interface LocalContextUtilization {
  id: string;
  local_context_id: string;
  utilization_type: string;
  subject_id: string;
  module_id: string;
  activity_id: string;
  integration_level: string;
  implementation_notes: string;
  student_engagement_level: string;
  effectiveness_rating: number;
  created_at: string;
}

export default function LocalContextPage() {
  const [utilizations, setUtilizations] = useState<LocalContextUtilization[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    local_context_id: "",
    utilization_type: "",
    subject_id: "",
    module_id: "",
    activity_id: "",
    integration_level: "",
    implementation_notes: "",
    student_engagement_level: "",
    effectiveness_rating: 3,
  });

  const fetchUtilizations = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/local-context/utilizations`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setUtilizations(json.data.utilizations || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUtilizations();
  }, []);

  const handleCreateUtilization = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/local-context/utilizations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenDialog(false);
        fetchUtilizations();
        setFormData({
          local_context_id: "",
          utilization_type: "",
          subject_id: "",
          module_id: "",
          activity_id: "",
          integration_level: "",
          implementation_notes: "",
          student_engagement_level: "",
          effectiveness_rating: 3,
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getIntegrationLevelColor = (level: string) => {
    switch (level) {
      case "MINIMAL":
        return "default";
      case "MODERATE":
        return "info";
      case "EXTENSIVE":
        return "success";
      default:
        return "default";
    }
  };

  const getEngagementLevelColor = (level: string) => {
    switch (level) {
      case "LOW":
        return "error";
      case "MODERATE":
        return "info";
      case "HIGH":
        return "success";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Integrasi Konteks Lokal
        </Typography>
        <Button variant="contained" startIcon={<NiStar size="small" />} onClick={() => setOpenDialog(true)}>
          Integrasi Baru
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Integrasi Konteks Lokal</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Integrasi konteks lokal ke dalam mata pelajaran dan modul pembelajaran untuk relevansi dan ketertarikan siswa.
      </Alert>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Tipe Utilisasi</TableCell>
              <TableCell className="font-bold">Subject ID</TableCell>
              <TableCell className="font-bold">Module ID</TableCell>
              <TableCell className="font-bold">Tingkat Integrasi</TableCell>
              <TableCell className="font-bold">Keterlibatan Siswa</TableCell>
              <TableCell className="font-bold">Rating Efektivitas</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : utilizations.length > 0 ? (
              utilizations.map((utilization) => (
                <TableRow key={utilization.id} hover>
                  <TableCell>
                    <Chip label={utilization.utilization_type} size="small" />
                  </TableCell>
                  <TableCell className="text-sm">{utilization.subject_id}</TableCell>
                  <TableCell className="text-sm">{utilization.module_id}</TableCell>
                  <TableCell>
                    <Chip
                      label={utilization.integration_level}
                      color={getIntegrationLevelColor(utilization.integration_level)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={utilization.student_engagement_level}
                      color={getEngagementLevelColor(utilization.student_engagement_level)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip label={`${utilization.effectiveness_rating}/5`} size="small" />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  Tidak ada data integrasi konteks lokal.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Integrasi Konteks Lokal Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Local Context ID"
              fullWidth
              value={formData.local_context_id}
              onChange={(e) => setFormData({ ...formData, local_context_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tipe Utilisasi</InputLabel>
              <Select
                value={formData.utilization_type}
                label="Tipe Utilisasi"
                onChange={(e) => setFormData({ ...formData, utilization_type: e.target.value })}
              >
                <MenuItem value="SUBJECT">Mata Pelajaran</MenuItem>
                <MenuItem value="MODULE">Modul Pembelajaran</MenuItem>
                <MenuItem value="ACTIVITY">Aktivitas</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Subject ID"
              fullWidth
              value={formData.subject_id}
              onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })}
            />
            <TextField
              label="Module ID"
              fullWidth
              value={formData.module_id}
              onChange={(e) => setFormData({ ...formData, module_id: e.target.value })}
            />
            <TextField
              label="Activity ID"
              fullWidth
              value={formData.activity_id}
              onChange={(e) => setFormData({ ...formData, activity_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tingkat Integrasi</InputLabel>
              <Select
                value={formData.integration_level}
                label="Tingkat Integrasi"
                onChange={(e) => setFormData({ ...formData, integration_level: e.target.value })}
              >
                <MenuItem value="MINIMAL">Minimal</MenuItem>
                <MenuItem value="MODERATE">Moderat</MenuItem>
                <MenuItem value="EXTENSIVE">Ekstensif</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Catatan Implementasi"
              fullWidth
              multiline
              rows={3}
              value={formData.implementation_notes}
              onChange={(e) => setFormData({ ...formData, implementation_notes: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tingkat Keterlibatan Siswa</InputLabel>
              <Select
                value={formData.student_engagement_level}
                label="Tingkat Keterlibatan Siswa"
                onChange={(e) => setFormData({ ...formData, student_engagement_level: e.target.value })}
              >
                <MenuItem value="LOW">Rendah</MenuItem>
                <MenuItem value="MODERATE">Sedang</MenuItem>
                <MenuItem value="HIGH">Tinggi</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Rating Efektivitas (1-5)"
              type="number"
              fullWidth
              value={formData.effectiveness_rating}
              onChange={(e) => setFormData({ ...formData, effectiveness_rating: parseInt(e.target.value) })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateUtilization}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
