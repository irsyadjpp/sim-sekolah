import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

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

interface IndividualLearningPlan {
  id: string;
  student_id: string;
  plan_type: string;
  title: string;
  description: string;
  learning_objectives: string;
  strategies: string;
  resources: string;
  timeline_start: string;
  timeline_end: string;
  status: string;
  created_at: string;
}

interface Student {
  id: string;
  full_name: string;
  nisn: string;
}

export default function IndividualLearningPlanPage() {
  const { studentId } = useParams<{ studentId?: string }>();
  const [plans, setPlans] = useState<IndividualLearningPlan[]>([]);
  const [student, setStudent] = useState<Student | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    plan_type: "",
    title: "",
    description: "",
    learning_objectives: "",
    strategies: "",
    resources: "",
    timeline_start: "",
    timeline_end: "",
  });

  const fetchPlans = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const url = studentId ? `${DEFAULTS.API_URL}/api/v1/ilp/student/${studentId}` : `${DEFAULTS.API_URL}/api/v1/ilp`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setPlans(json.data.plans || []);
        if (json.data.student) {
          setStudent(json.data.student);
        }
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
    fetchPlans();
  }, [studentId]);

  const handleCreatePlan = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/ilp`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...formData,
          student_id: studentId,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenDialog(false);
        fetchPlans();
        setFormData({
          plan_type: "",
          title: "",
          description: "",
          learning_objectives: "",
          strategies: "",
          resources: "",
          timeline_start: "",
          timeline_end: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "DRAFT":
        return "default";
      case "ACTIVE":
        return "primary";
      case "IN_PROGRESS":
        return "info";
      case "COMPLETED":
        return "success";
      case "ARCHIVED":
        return "secondary";
      default:
        return "default";
    }
  };

  const getPlanTypeLabel = (type: string) => {
    switch (type) {
      case "REMEDIATION":
        return "Remediasi";
      case "ENRICHMENT":
        return "Pengayaan";
      case "SUPPORT":
        return "Pendukung";
      case "MODIFICATION":
        return "Modifikasi";
      default:
        return type;
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Individual Learning Plans (ILP)
        </Typography>
        <Button variant="contained" startIcon={<NiStar size="small" />} onClick={() => setOpenDialog(true)}>
          Buat Rencana Baru
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        {studentId ? (
          <>
            <Link to="/students">Siswa</Link>
            <Typography variant="body2">Rencana Pembelajaran</Typography>
          </>
        ) : (
          <>
            <Link to="/academic">Akademik</Link>
            <Typography variant="body2">Rencana Pembelajaran</Typography>
          </>
        )}
      </Breadcrumbs>

      {student && (
        <Alert severity="info" className="mb-6">
          Rencana pembelajaran untuk: <strong>{student.full_name}</strong> (NISN: {student.nisn})
        </Alert>
      )}

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Tipe</TableCell>
              <TableCell className="font-bold">Judul</TableCell>
              <TableCell className="font-bold">Tujuan Pembelajaran</TableCell>
              <TableCell className="font-bold">Timeline</TableCell>
              <TableCell className="font-bold">Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : plans.length > 0 ? (
              plans.map((plan) => (
                <TableRow key={plan.id} hover>
                  <TableCell>
                    <Chip label={getPlanTypeLabel(plan.plan_type)} size="small" />
                  </TableCell>
                  <TableCell className="font-medium">{plan.title}</TableCell>
                  <TableCell>{plan.learning_objectives}</TableCell>
                  <TableCell className="text-sm">
                    {plan.timeline_start} s/d {plan.timeline_end}
                  </TableCell>
                  <TableCell>
                    <Chip label={plan.status} color={getStatusColor(plan.status)} size="small" />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  Tidak ada rencana pembelajaran yang dibuat.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Buat Rencana Pembelajaran Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <FormControl fullWidth>
              <InputLabel>Tipe Rencana</InputLabel>
              <Select
                value={formData.plan_type}
                label="Tipe Rencana"
                onChange={(e) => setFormData({ ...formData, plan_type: e.target.value })}
              >
                <MenuItem value="REMEDIATION">Remediasi</MenuItem>
                <MenuItem value="ENRICHMENT">Pengayaan</MenuItem>
                <MenuItem value="SUPPORT">Pendukung</MenuItem>
                <MenuItem value="MODIFICATION">Modifikasi</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Judul"
              fullWidth
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
            <TextField
              label="Deskripsi"
              fullWidth
              multiline
              rows={3}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
            <TextField
              label="Tujuan Pembelajaran"
              fullWidth
              multiline
              rows={3}
              value={formData.learning_objectives}
              onChange={(e) => setFormData({ ...formData, learning_objectives: e.target.value })}
            />
            <TextField
              label="Strategi"
              fullWidth
              multiline
              rows={3}
              value={formData.strategies}
              onChange={(e) => setFormData({ ...formData, strategies: e.target.value })}
            />
            <TextField
              label="Sumber Daya"
              fullWidth
              multiline
              rows={2}
              value={formData.resources}
              onChange={(e) => setFormData({ ...formData, resources: e.target.value })}
            />
            <TextField
              label="Timeline Mulai"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={formData.timeline_start}
              onChange={(e) => setFormData({ ...formData, timeline_start: e.target.value })}
            />
            <TextField
              label="Timeline Selesai"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={formData.timeline_end}
              onChange={(e) => setFormData({ ...formData, timeline_end: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreatePlan}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
