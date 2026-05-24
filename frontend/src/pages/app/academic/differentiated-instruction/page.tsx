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

interface DifferentiatedInstruction {
  id: string;
  subject_id: string;
  module_id: string;
  di_type: string;
  content_adjustments: string;
  process_adjustments: string;
  product_adjustments: string;
  environment_adjustments: string;
  assessment_method: string;
  target_students: string;
  effectiveness_rating: number;
  notes: string;
  created_at: string;
}

export default function DifferentiatedInstructionPage() {
  const [instructions, setInstructions] = useState<DifferentiatedInstruction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    subject_id: "",
    module_id: "",
    di_type: "",
    content_adjustments: "",
    process_adjustments: "",
    product_adjustments: "",
    environment_adjustments: "",
    assessment_method: "",
    target_students: "",
    effectiveness_rating: 3,
    notes: "",
  });

  const fetchInstructions = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/di`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setInstructions(json.data.instructions || []);
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
    fetchInstructions();
  }, []);

  const handleCreateInstruction = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/di`, {
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
        fetchInstructions();
        setFormData({
          subject_id: "",
          module_id: "",
          di_type: "",
          content_adjustments: "",
          process_adjustments: "",
          product_adjustments: "",
          environment_adjustments: "",
          assessment_method: "",
          target_students: "",
          effectiveness_rating: 3,
          notes: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getDITypeLabel = (type: string) => {
    switch (type) {
      case "CONTENT":
        return "Konten";
      case "PROCESS":
        return "Proses";
      case "PRODUCT":
        return "Produk";
      case "ENVIRONMENT":
        return "Lingkungan";
      case "ASSESSMENT":
        return "Asesmen";
      default:
        return type;
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Differentiated Instruction (DI)
        </Typography>
        <Button variant="contained" startIcon={<NiStar size="small" />} onClick={() => setOpenDialog(true)}>
          Buat DI Baru
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Differentiated Instruction</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Sistem DI untuk memantau dan mengimplementasikan pendekatan pembelajaran yang berbeda sesuai kebutuhan siswa.
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
              <TableCell className="font-bold">Tipe DI</TableCell>
              <TableCell className="font-bold">Konten</TableCell>
              <TableCell className="font-bold">Proses</TableCell>
              <TableCell className="font-bold">Produk</TableCell>
              <TableCell className="font-bold">Asesmen</TableCell>
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
            ) : instructions.length > 0 ? (
              instructions.map((instruction) => (
                <TableRow key={instruction.id} hover>
                  <TableCell>
                    <Chip label={getDITypeLabel(instruction.di_type)} size="small" />
                  </TableCell>
                  <TableCell className="text-sm">{instruction.content_adjustments}</TableCell>
                  <TableCell className="text-sm">{instruction.process_adjustments}</TableCell>
                  <TableCell className="text-sm">{instruction.product_adjustments}</TableCell>
                  <TableCell className="text-sm">{instruction.assessment_method}</TableCell>
                  <TableCell>
                    <Chip label={`${instruction.effectiveness_rating}/5`} size="small" />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  Tidak ada data differentiated instruction.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Buat Differentiated Instruction Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
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
            <FormControl fullWidth>
              <InputLabel>Tipe DI</InputLabel>
              <Select
                value={formData.di_type}
                label="Tipe DI"
                onChange={(e) => setFormData({ ...formData, di_type: e.target.value })}
              >
                <MenuItem value="CONTENT">Konten</MenuItem>
                <MenuItem value="PROCESS">Proses</MenuItem>
                <MenuItem value="PRODUCT">Produk</MenuItem>
                <MenuItem value="ENVIRONMENT">Lingkungan</MenuItem>
                <MenuItem value="ASSESSMENT">Asesmen</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Penyesuaian Konten"
              fullWidth
              multiline
              rows={2}
              value={formData.content_adjustments}
              onChange={(e) => setFormData({ ...formData, content_adjustments: e.target.value })}
            />
            <TextField
              label="Penyesuaian Proses"
              fullWidth
              multiline
              rows={2}
              value={formData.process_adjustments}
              onChange={(e) => setFormData({ ...formData, process_adjustments: e.target.value })}
            />
            <TextField
              label="Penyesuaian Produk"
              fullWidth
              multiline
              rows={2}
              value={formData.product_adjustments}
              onChange={(e) => setFormData({ ...formData, product_adjustments: e.target.value })}
            />
            <TextField
              label="Penyesuaian Lingkungan"
              fullWidth
              multiline
              rows={2}
              value={formData.environment_adjustments}
              onChange={(e) => setFormData({ ...formData, environment_adjustments: e.target.value })}
            />
            <TextField
              label="Metode Asesmen"
              fullWidth
              value={formData.assessment_method}
              onChange={(e) => setFormData({ ...formData, assessment_method: e.target.value })}
            />
            <TextField
              label="Target Siswa"
              fullWidth
              multiline
              rows={2}
              value={formData.target_students}
              onChange={(e) => setFormData({ ...formData, target_students: e.target.value })}
            />
            <TextField
              label="Rating Efektivitas (1-5)"
              type="number"
              fullWidth
              value={formData.effectiveness_rating}
              onChange={(e) => setFormData({ ...formData, effectiveness_rating: parseInt(e.target.value) })}
            />
            <TextField
              label="Catatan"
              fullWidth
              multiline
              rows={2}
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateInstruction}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
