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
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiStar from "@/icons/nexture/ni-star";

interface CharacterIntervention {
  id: string;
  intervention_name: string;
  character_dimension: string;
  target_age_group: string;
  intervention_type: string;
  description: string;
  duration_weeks: number;
  is_active: boolean;
}

interface StudentCharacterIntervention {
  id: string;
  student_id: string;
  intervention_id: string;
  assignment_date: string;
  target_start_date: string;
  target_end_date: string;
  current_status: string;
  priority_level: string;
  baseline_assessment: string;
}

interface InterventionRecommendation {
  id: string;
  student_id: string;
  recommended_interventions: string[];
  recommendation_date: string;
  recommendation_source: string;
  confidence_score: number;
  rationale: string;
  is_accepted: boolean;
}

interface CharacterMilestone {
  id: string;
  student_id: string;
  character_dimension: string;
  milestone_description: string;
  milestone_date: string;
  achievement_level: string;
  celebration_method: string;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function CharacterInterventionPage() {
  const { studentId } = useParams<{ studentId?: string }>();
  const [tabValue, setTabValue] = useState(0);
  const [interventions, setInterventions] = useState<CharacterIntervention[]>([]);
  const [studentInterventions, setStudentInterventions] = useState<StudentCharacterIntervention[]>([]);
  const [recommendations, setRecommendations] = useState<InterventionRecommendation[]>([]);
  const [milestones, setMilestones] = useState<CharacterMilestone[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openAssignmentDialog, setOpenAssignmentDialog] = useState(false);
  const [openMilestoneDialog, setOpenMilestoneDialog] = useState(false);

  const [assignmentFormData, setAssignmentFormData] = useState({
    intervention_id: "",
    target_start_date: "",
    target_end_date: "",
    priority_level: "MEDIUM",
    baseline_assessment: "",
    customized_strategies: "",
    notes: "",
  });

  const [milestoneFormData, setMilestoneFormData] = useState({
    character_dimension: "",
    milestone_description: "",
    achievement_level: "",
    evidence: "",
    celebration_method: "",
    notes: "",
  });

  const fetchInterventions = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/character-intervention/interventions`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setInterventions(json.data.interventions || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchStudentInterventions = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const url = studentId
        ? `${DEFAULTS.API_URL}/api/v1/character-intervention/student/${studentId}`
        : `${DEFAULTS.API_URL}/api/v1/character-intervention/assignments`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setStudentInterventions(json.data.assignments || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const fetchRecommendations = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const url = studentId
        ? `${DEFAULTS.API_URL}/api/v1/character-intervention/recommendations/student/${studentId}`
        : `${DEFAULTS.API_URL}/api/v1/character-intervention/recommendations`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setRecommendations(json.data.recommendations || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const fetchMilestones = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const url = studentId
        ? `${DEFAULTS.API_URL}/api/v1/character-intervention/milestones/student/${studentId}`
        : `${DEFAULTS.API_URL}/api/v1/character-intervention/milestones`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setMilestones(json.data.milestones || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchInterventions();
    fetchStudentInterventions();
    fetchRecommendations();
    fetchMilestones();
  }, [studentId]);

  const handleCreateAssignment = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/character-intervention/assignments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...assignmentFormData,
          student_id: studentId,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenAssignmentDialog(false);
        fetchStudentInterventions();
        setAssignmentFormData({
          intervention_id: "",
          target_start_date: "",
          target_end_date: "",
          priority_level: "MEDIUM",
          baseline_assessment: "",
          customized_strategies: "",
          notes: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleCreateMilestone = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/character-intervention/milestones`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...milestoneFormData,
          student_id: studentId,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenMilestoneDialog(false);
        fetchMilestones();
        setMilestoneFormData({
          character_dimension: "",
          milestone_description: "",
          achievement_level: "",
          evidence: "",
          celebration_method: "",
          notes: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleGenerateRecommendations = async () => {
    if (!studentId) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(
        `${DEFAULTS.API_URL}/api/v1/character-intervention/recommendations/generate/${studentId}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      const json = await res.json();
      if (json.status === "success") {
        fetchRecommendations();
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getCharacterDimensionLabel = (dimension: string) => {
    switch (dimension) {
      case "BERAKHLAK":
        return "Berakhlak";
      case "BERKEBHINEASAN":
        return "Berkhineasan";
      case "BERNILAI_SANTUN":
        return "Bernilai Santun";
      case "MANDIRI":
        return "Mandiri";
      case "BERTANGGUNG_JAWAB":
        return "Bertanggung Jawab";
      case "GOTONG_ROYONG":
        return "Gotong Royong";
      default:
        return dimension;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "LOW":
        return "default";
      case "MEDIUM":
        return "info";
      case "HIGH":
        return "warning";
      case "URGENT":
        return "error";
      default:
        return "default";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "PLANNED":
        return "default";
      case "ACTIVE":
        return "primary";
      case "PAUSED":
        return "warning";
      case "COMPLETED":
        return "success";
      case "CANCELLED":
        return "error";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Intervensi Karakter
        </Typography>
        {studentId && (
          <Button variant="outlined" startIcon={<NiStar size="small" />} onClick={handleGenerateRecommendations}>
            Generate Rekomendasi
          </Button>
        )}
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        {studentId ? (
          <>
            <Link to="/students">Siswa</Link>
            <Typography variant="body2">Intervensi Karakter</Typography>
          </>
        ) : (
          <>
            <Link to="/academic">Akademik</Link>
            <Typography variant="body2">Intervensi Karakter</Typography>
          </>
        )}
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Sistem rekomendasi dan tracking intervensi pengembangan karakter sesuai Kurikulum Merdeka.
      </Alert>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Box sx={{ borderBottom: 1, borderColor: "divider", mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Intervensi Tersedia" />
          <Tab label="Penugasan Siswa" />
          <Tab label="Rekomendasi" />
          <Tab label="Milestone" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Nama Intervensi</TableCell>
                <TableCell className="font-bold">Dimensi Karakter</TableCell>
                <TableCell className="font-bold">Tipe</TableCell>
                <TableCell className="font-bold">Fase Target</TableCell>
                <TableCell className="font-bold">Durasi (minggu)</TableCell>
                <TableCell className="font-bold">Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    <CircularProgress size={24} />
                  </TableCell>
                </TableRow>
              ) : interventions.length > 0 ? (
                interventions.map((intervention) => (
                  <TableRow key={intervention.id} hover>
                    <TableCell className="font-medium">{intervention.intervention_name}</TableCell>
                    <TableCell>
                      <Chip label={getCharacterDimensionLabel(intervention.character_dimension)} size="small" />
                    </TableCell>
                    <TableCell>{intervention.intervention_type}</TableCell>
                    <TableCell>{intervention.target_age_group}</TableCell>
                    <TableCell>{intervention.duration_weeks}</TableCell>
                    <TableCell>
                      <Chip
                        label={intervention.is_active ? "Aktif" : "Nonaktif"}
                        color={intervention.is_active ? "success" : "default"}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    Tidak ada intervensi yang tersedia.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box className="mb-4">
          <Button variant="outlined" startIcon={<NiStar size="small" />} onClick={() => setOpenAssignmentDialog(true)}>
            Buat Penugasan Baru
          </Button>
        </Box>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Tanggal Penugasan</TableCell>
                <TableCell className="font-bold">Timeline</TableCell>
                <TableCell className="font-bold">Status</TableCell>
                <TableCell className="font-bold">Prioritas</TableCell>
                <TableCell className="font-bold">Baseline</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {studentInterventions.length > 0 ? (
                studentInterventions.map((assignment) => (
                  <TableRow key={assignment.id} hover>
                    <TableCell className="text-sm">{assignment.assignment_date}</TableCell>
                    <TableCell className="text-sm">
                      {assignment.target_start_date} s/d {assignment.target_end_date}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={assignment.current_status}
                        color={getStatusColor(assignment.current_status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={assignment.priority_level}
                        color={getPriorityColor(assignment.priority_level)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell className="text-sm">{assignment.baseline_assessment}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center" className="py-10">
                    Tidak ada penugasan intervensi.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Tanggal Rekomendasi</TableCell>
                <TableCell className="font-bold">Sumber</TableCell>
                <TableCell className="font-bold">Confidence Score</TableCell>
                <TableCell className="font-bold">Rationale</TableCell>
                <TableCell className="font-bold">Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {recommendations.length > 0 ? (
                recommendations.map((rec) => (
                  <TableRow key={rec.id} hover>
                    <TableCell className="text-sm">{rec.recommendation_date}</TableCell>
                    <TableCell>
                      <Chip label={rec.recommendation_source} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip label={`${(rec.confidence_score * 100).toFixed(0)}%`} size="small" />
                    </TableCell>
                    <TableCell className="text-sm">{rec.rationale}</TableCell>
                    <TableCell>
                      <Chip
                        label={rec.is_accepted ? "Diterima" : "Pending"}
                        color={rec.is_accepted ? "success" : "default"}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center" className="py-10">
                    Tidak ada rekomendasi intervensi.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <Box className="mb-4">
          <Button variant="outlined" startIcon={<NiStar size="small" />} onClick={() => setOpenMilestoneDialog(true)}>
            Catat Milestone Baru
          </Button>
        </Box>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Dimensi Karakter</TableCell>
                <TableCell className="font-bold">Deskripsi Milestone</TableCell>
                <TableCell className="font-bold">Tanggal</TableCell>
                <TableCell className="font-bold">Tingkat Pencapaian</TableCell>
                <TableCell className="font-bold">Perayaan</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {milestones.length > 0 ? (
                milestones.map((milestone) => (
                  <TableRow key={milestone.id} hover>
                    <TableCell>
                      <Chip label={getCharacterDimensionLabel(milestone.character_dimension)} size="small" />
                    </TableCell>
                    <TableCell className="text-sm">{milestone.milestone_description}</TableCell>
                    <TableCell className="text-sm">{milestone.milestone_date}</TableCell>
                    <TableCell>
                      <Chip
                        label={milestone.achievement_level}
                        color={milestone.achievement_level === "EXEMPLARY" ? "success" : "info"}
                        size="small"
                      />
                    </TableCell>
                    <TableCell className="text-sm">{milestone.celebration_method}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center" className="py-10">
                    Tidak ada milestone yang dicatat.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Assignment Dialog */}
      <Dialog open={openAssignmentDialog} onClose={() => setOpenAssignmentDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Buat Penugasan Intervensi Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Intervention ID"
              fullWidth
              value={assignmentFormData.intervention_id}
              onChange={(e) => setAssignmentFormData({ ...assignmentFormData, intervention_id: e.target.value })}
            />
            <TextField
              label="Target Start Date"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={assignmentFormData.target_start_date}
              onChange={(e) => setAssignmentFormData({ ...assignmentFormData, target_start_date: e.target.value })}
            />
            <TextField
              label="Target End Date"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={assignmentFormData.target_end_date}
              onChange={(e) => setAssignmentFormData({ ...assignmentFormData, target_end_date: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Prioritas</InputLabel>
              <Select
                value={assignmentFormData.priority_level}
                label="Prioritas"
                onChange={(e) => setAssignmentFormData({ ...assignmentFormData, priority_level: e.target.value })}
              >
                <MenuItem value="LOW">Rendah</MenuItem>
                <MenuItem value="MEDIUM">Sedang</MenuItem>
                <MenuItem value="HIGH">Tinggi</MenuItem>
                <MenuItem value="URGENT">Urgent</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Baseline Assessment"
              fullWidth
              multiline
              rows={2}
              value={assignmentFormData.baseline_assessment}
              onChange={(e) => setAssignmentFormData({ ...assignmentFormData, baseline_assessment: e.target.value })}
            />
            <TextField
              label="Strategi Customized"
              fullWidth
              multiline
              rows={2}
              value={assignmentFormData.customized_strategies}
              onChange={(e) => setAssignmentFormData({ ...assignmentFormData, customized_strategies: e.target.value })}
            />
            <TextField
              label="Catatan"
              fullWidth
              multiline
              rows={2}
              value={assignmentFormData.notes}
              onChange={(e) => setAssignmentFormData({ ...assignmentFormData, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAssignmentDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateAssignment}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Milestone Dialog */}
      <Dialog open={openMilestoneDialog} onClose={() => setOpenMilestoneDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Catat Milestone Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <FormControl fullWidth>
              <InputLabel>Dimensi Karakter</InputLabel>
              <Select
                value={milestoneFormData.character_dimension}
                label="Dimensi Karakter"
                onChange={(e) => setMilestoneFormData({ ...milestoneFormData, character_dimension: e.target.value })}
              >
                <MenuItem value="BERAKHLAK">Berakhlak</MenuItem>
                <MenuItem value="BERKEBHINEASAN">Berkhineasan</MenuItem>
                <MenuItem value="BERNILAI_SANTUN">Bernilai Santun</MenuItem>
                <MenuItem value="MANDIRI">Mandiri</MenuItem>
                <MenuItem value="BERTANGGUNG_JAWAB">Bertanggung Jawab</MenuItem>
                <MenuItem value="GOTONG_ROYONG">Gotong Royong</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Deskripsi Milestone"
              fullWidth
              multiline
              rows={3}
              value={milestoneFormData.milestone_description}
              onChange={(e) => setMilestoneFormData({ ...milestoneFormData, milestone_description: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tingkat Pencapaian</InputLabel>
              <Select
                value={milestoneFormData.achievement_level}
                label="Tingkat Pencapaian"
                onChange={(e) => setMilestoneFormData({ ...milestoneFormData, achievement_level: e.target.value })}
              >
                <MenuItem value="EMERGING">Emerging</MenuItem>
                <MenuItem value="DEVELOPING">Developing</MenuItem>
                <MenuItem value="PROFICIENT">Proficient</MenuItem>
                <MenuItem value="EXEMPLARY">Exemplary</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Evidence"
              fullWidth
              multiline
              rows={2}
              value={milestoneFormData.evidence}
              onChange={(e) => setMilestoneFormData({ ...milestoneFormData, evidence: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Metode Perayaan</InputLabel>
              <Select
                value={milestoneFormData.celebration_method}
                label="Metode Perayaan"
                onChange={(e) => setMilestoneFormData({ ...milestoneFormData, celebration_method: e.target.value })}
              >
                <MenuItem value="VERBAL_PRAISE">Pujian Verbal</MenuItem>
                <MenuItem value="CERTIFICATE">Sertifikat</MenuItem>
                <MenuItem value="CLASS_RECOGNITION">Pengakuan Kelas</MenuItem>
                <MenuItem value="PARENT_NOTIFICATION">Notifikasi Orang Tua</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Catatan"
              fullWidth
              multiline
              rows={2}
              value={milestoneFormData.notes}
              onChange={(e) => setMilestoneFormData({ ...milestoneFormData, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenMilestoneDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateMilestone}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
