import { useSnackbar } from "notistack";
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Box,
  Breadcrumbs,
  Button,
  Card,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  IconButton,
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
import { useConfirm } from "@/hooks/use-confirm";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";

interface SDAssessmentCriteria {
  id: string;
  assessment_type: string;
  phase_id: string;
  criteria_name: string;
  description: string;
  rubric_elements: string;
  is_active: boolean;
  type_description: string;
}

interface Phase {
  id: string;
  phase_name: string;
}

export default function CriteriaPage() {
  const { enqueueSnackbar } = useSnackbar();
  const confirm = useConfirm();

  const [criteria, setCriteria] = useState<SDAssessmentCriteria[]>([]);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [ageTypes, setAgeTypes] = useState<{ id: string; description: string }[]>([]);

  const [loading, setLoading] = useState(false);

  const [openModal, setOpenModal] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    assessment_type: "",
    phase_id: "",
    criteria_name: "",
    description: "",
    rubric_elements: "",
  });

  const token = localStorage.getItem("accessToken");

  const fetchPhases = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/phases?limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setPhases(json.data);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  const fetchAgeAppropriateTypes = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/penilaian/age-appropriate-types`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setAgeTypes(json.data || []);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  const fetchCriteria = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/sd-assessment-criteria`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setCriteria(json.data || []);
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchPhases();
    fetchAgeAppropriateTypes();
    fetchCriteria();
  }, [fetchPhases, fetchAgeAppropriateTypes, fetchCriteria]);

  const handleOpenNew = () => {
    setEditingId(null);
    setFormData({
      assessment_type: "",
      phase_id: "",
      criteria_name: "",
      description: "",
      rubric_elements: "",
    });
    setOpenModal(true);
  };

  const handleOpenEdit = (item: SDAssessmentCriteria) => {
    setEditingId(item.id);
    setFormData({
      assessment_type: item.assessment_type,
      phase_id: item.phase_id,
      criteria_name: item.criteria_name,
      description: item.description,
      rubric_elements: item.rubric_elements,
    });
    setOpenModal(true);
  };

  const handleSave = async () => {
    if (!formData.criteria_name || !formData.assessment_type) {
      enqueueSnackbar("Nama kriteria dan tipe asesmen wajib diisi", { variant: "warning" });
      return;
    }

    try {
      const url = editingId
        ? `${DEFAULTS.API_URL}/api/v1/sd-assessment-criteria/${editingId}`
        : `${DEFAULTS.API_URL}/api/v1/sd-assessment-criteria`;
      const method = editingId ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const json = await res.json();
      if (json.status === "success") {
        enqueueSnackbar("Kriteria berhasil disimpan", { variant: "success" });
        setOpenModal(false);
        fetchCriteria();
      } else {
        enqueueSnackbar(json.message || "Gagal menyimpan kriteria", { variant: "error" });
      }
    } catch (err: any) {
      enqueueSnackbar("Kesalahan koneksi", { variant: "error" });
    }
  };

  const handleDelete = async (id: string) => {
    const ok = await confirm({
      title: "Hapus Kriteria",
      message: "Apakah Anda yakin ingin menghapus kriteria asesmen ini?",
      confirmText: "Hapus",
      cancelText: "Batal",
    });
    if (!ok) return;

    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/sd-assessment-criteria/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        enqueueSnackbar("Kriteria berhasil dihapus", { variant: "success" });
        fetchCriteria();
      } else {
        enqueueSnackbar(json.message || "Gagal menghapus kriteria", { variant: "error" });
      }
    } catch (err: any) {
      enqueueSnackbar("Kesalahan koneksi", { variant: "error" });
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Kriteria Asesmen SD
        </Typography>
        <Button variant="contained" startIcon={<NiPlus size="small" />} onClick={handleOpenNew}>
          Tambah Kriteria
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Kriteria Asesmen SD</Typography>
      </Breadcrumbs>

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Nama Kriteria</TableCell>
              <TableCell className="font-bold">Tipe Asesmen SD</TableCell>
              <TableCell className="font-bold">Deskripsi</TableCell>
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
            ) : criteria.length > 0 ? (
              criteria.map((item) => (
                <TableRow key={item.id} hover>
                  <TableCell className="font-medium">{item.criteria_name}</TableCell>
                  <TableCell>{item.type_description || item.assessment_type}</TableCell>
                  <TableCell>{item.description}</TableCell>
                  <TableCell align="center">
                    <IconButton size="small" color="primary" onClick={() => handleOpenEdit(item)}>
                      <NiPen size="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDelete(item.id)}>
                      <NiBinEmpty size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Belum ada kriteria asesmen yang dibuat.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Modal */}
      <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? "Edit Kriteria" : "Tambah Kriteria"}</DialogTitle>
        <DialogContent dividers>
          <Box className="flex flex-col gap-4 pt-2">
            <TextField
              label="Nama Kriteria"
              fullWidth
              size="small"
              value={formData.criteria_name}
              onChange={(e) => setFormData({ ...formData, criteria_name: e.target.value })}
            />
            <FormControl fullWidth size="small">
              <InputLabel>Fase Belajar</InputLabel>
              <Select
                label="Fase Belajar"
                value={formData.phase_id}
                onChange={(e) => setFormData({ ...formData, phase_id: e.target.value })}
              >
                <MenuItem value="">
                  <em>Semua Fase</em>
                </MenuItem>
                {phases.map((p) => (
                  <MenuItem key={p.id} value={p.id}>
                    {p.phase_name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth size="small">
              <InputLabel>Tipe Asesmen Khusus SD</InputLabel>
              <Select
                label="Tipe Asesmen Khusus SD"
                value={formData.assessment_type}
                onChange={(e) => setFormData({ ...formData, assessment_type: e.target.value })}
              >
                <MenuItem value="">
                  <em>Pilih Tipe Asesmen</em>
                </MenuItem>
                {ageTypes.map((type) => (
                  <MenuItem key={type.id} value={type.id}>
                    {type.description}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Deskripsi"
              fullWidth
              multiline
              rows={3}
              size="small"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
            <TextField
              label="Elemen Rubrik (JSON format)"
              fullWidth
              multiline
              rows={4}
              size="small"
              value={formData.rubric_elements}
              onChange={(e) => setFormData({ ...formData, rubric_elements: e.target.value })}
              helperText='Contoh: [{"kriteria": "Kreativitas", "skor": 4}]'
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
