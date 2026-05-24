import { useSnackbar } from "notistack";
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
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

interface KokurikulerActivity {
  id: string;
  curriculum_document_id: string;
  activity_name: string;
  linked_subject_id: string;
  linked_subject_name?: string;
  description: string;
  schedule: string;
  is_active: boolean;
}

interface CurriculumDocument {
  id: string;
  academic_year: { year_name: string; semester: string };
  curriculum_type: string;
  status: string;
}

interface Subject {
  id: string;
  subject_name: string;
}

export default function KokurikulerPage() {
  const { enqueueSnackbar } = useSnackbar();
  const confirm = useConfirm();

  const [activities, setActivities] = useState<KokurikulerActivity[]>([]);
  const [documents, setDocuments] = useState<CurriculumDocument[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedDocId, setSelectedDocId] = useState("");

  const [loading, setLoading] = useState(false);

  const [openModal, setOpenModal] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    activity_name: "",
    linked_subject_id: "",
    description: "",
    schedule: "",
  });

  const token = localStorage.getItem("accessToken");

  const fetchDocuments = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/curriculum-documents`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setDocuments(json.data);
        if (json.data.length > 0) {
          setSelectedDocId(json.data[0].id);
        }
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  const fetchSubjects = useCallback(async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects?limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setSubjects(json.data);
      }
    } catch (err: any) {
      console.error(err);
    }
  }, [token]);

  const fetchActivities = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/kokurikuler`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        const filtered = (json.data || []).filter((a: any) => a.curriculum_document_id === selectedDocId);
        setActivities(filtered);
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [selectedDocId, token]);

  useEffect(() => {
    fetchDocuments();
    fetchSubjects();
  }, [fetchDocuments, fetchSubjects]);

  useEffect(() => {
    if (selectedDocId) {
      fetchActivities();
    } else {
      setActivities([]);
    }
  }, [selectedDocId, fetchActivities]);

  const handleOpenNew = () => {
    setEditingId(null);
    setFormData({
      activity_name: "",
      linked_subject_id: "",
      description: "",
      schedule: "",
    });
    setOpenModal(true);
  };

  const handleOpenEdit = (item: KokurikulerActivity) => {
    setEditingId(item.id);
    setFormData({
      activity_name: item.activity_name,
      linked_subject_id: item.linked_subject_id || "",
      description: item.description,
      schedule: item.schedule,
    });
    setOpenModal(true);
  };

  const handleSave = async () => {
    if (!formData.activity_name) {
      enqueueSnackbar("Nama aktivitas wajib diisi", { variant: "warning" });
      return;
    }

    try {
      const url = editingId
        ? `${DEFAULTS.API_URL}/api/v1/kokurikuler/${editingId}`
        : `${DEFAULTS.API_URL}/api/v1/kokurikuler`;
      const method = editingId ? "PUT" : "POST";
      const payload = editingId ? formData : { ...formData, curriculum_document_id: selectedDocId };

      const res = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const json = await res.json();
      if (json.status === "success") {
        enqueueSnackbar("Aktivitas kokurikuler berhasil disimpan", { variant: "success" });
        setOpenModal(false);
        fetchActivities();
      } else {
        enqueueSnackbar(json.message || "Gagal menyimpan aktivitas", { variant: "error" });
      }
    } catch (err: any) {
      enqueueSnackbar("Kesalahan koneksi", { variant: "error" });
    }
  };

  const handleDelete = async (id: string) => {
    const ok = await confirm({
      title: "Hapus Aktivitas",
      message: "Apakah Anda yakin ingin menghapus aktivitas kokurikuler ini?",
      confirmText: "Hapus",
      cancelText: "Batal",
    });
    if (!ok) return;

    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/kokurikuler/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        enqueueSnackbar("Aktivitas berhasil dihapus", { variant: "success" });
        fetchActivities();
      } else {
        enqueueSnackbar(json.message || "Gagal menghapus aktivitas", { variant: "error" });
      }
    } catch (err: any) {
      enqueueSnackbar("Kesalahan koneksi", { variant: "error" });
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Aktivitas Kokurikuler
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={handleOpenNew}
          disabled={!selectedDocId}
        >
          Tambah Aktivitas
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Kokurikuler</Typography>
      </Breadcrumbs>

      <Card className="mb-6">
        <CardContent className="flex gap-4 p-4">
          <FormControl size="small" className="min-w-[300px]">
            <InputLabel>Dokumen Kurikulum KSP</InputLabel>
            <Select
              label="Dokumen Kurikulum KSP"
              value={selectedDocId}
              onChange={(e) => setSelectedDocId(e.target.value)}
            >
              <MenuItem value="">
                <em>-- Pilih Dokumen KSP --</em>
              </MenuItem>
              {documents.map((d) => (
                <MenuItem key={d.id} value={d.id}>
                  {d.academic_year?.year_name} ({d.academic_year?.semester}) - {d.curriculum_type} [{d.status}]
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </CardContent>
      </Card>

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Nama Aktivitas</TableCell>
              <TableCell className="font-bold">Mata Pelajaran Terkait</TableCell>
              <TableCell className="font-bold">Jadwal</TableCell>
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
            ) : activities.length > 0 ? (
              activities.map((item) => {
                const subject = subjects.find((s) => s.id === item.linked_subject_id);
                return (
                  <TableRow key={item.id} hover>
                    <TableCell className="font-medium">
                      {item.activity_name}
                      <Typography variant="caption" display="block" color="textSecondary">
                        {item.description}
                      </Typography>
                    </TableCell>
                    <TableCell>{subject ? subject.subject_name : "-"}</TableCell>
                    <TableCell>{item.schedule || "-"}</TableCell>
                    <TableCell align="center">
                      <IconButton size="small" color="primary" onClick={() => handleOpenEdit(item)}>
                        <NiPen size="small" />
                      </IconButton>
                      <IconButton size="small" color="error" onClick={() => handleDelete(item.id)}>
                        <NiBinEmpty size="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Belum ada aktivitas kokurikuler untuk dokumen ini.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Modal */}
      <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? "Edit Aktivitas Kokurikuler" : "Tambah Aktivitas Kokurikuler"}</DialogTitle>
        <DialogContent dividers>
          <Box className="flex flex-col gap-4 pt-2">
            <TextField
              label="Nama Aktivitas"
              fullWidth
              size="small"
              value={formData.activity_name}
              onChange={(e) => setFormData({ ...formData, activity_name: e.target.value })}
            />
            <FormControl fullWidth size="small">
              <InputLabel>Mata Pelajaran Terkait (Opsional)</InputLabel>
              <Select
                label="Mata Pelajaran Terkait (Opsional)"
                value={formData.linked_subject_id}
                onChange={(e) => setFormData({ ...formData, linked_subject_id: e.target.value })}
              >
                <MenuItem value="">
                  <em>Tanpa Mapel Terkait</em>
                </MenuItem>
                {subjects.map((s) => (
                  <MenuItem key={s.id} value={s.id}>
                    {s.subject_name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Jadwal Pelaksanaan"
              fullWidth
              size="small"
              value={formData.schedule}
              onChange={(e) => setFormData({ ...formData, schedule: e.target.value })}
              helperText="Contoh: Setiap Sabtu, Pukul 08:00 - 10:00"
            />
            <TextField
              label="Deskripsi"
              fullWidth
              multiline
              rows={3}
              size="small"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
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
