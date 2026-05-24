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

interface PeerAssessmentTemplate {
  id: string;
  template_name: string;
  assessment_type: string;
  phase: string;
  assessment_focus: string;
  description: string;
  is_active: boolean;
}

interface SelfAssessment {
  id: string;
  student_id: string;
  template_id: string;
  assessment_date: string;
  context: string;
  confidence_level: string;
  teacher_feedback: string;
}

interface PeerAssessment {
  id: string;
  assessor_student_id: string;
  assessed_student_id: string;
  template_id: string;
  assessment_date: string;
  context: string;
  relationship_context: string;
  teacher_review_status: string;
}

interface GroupAssessment {
  id: string;
  group_id: string;
  group_name: string;
  template_id: string;
  assessment_date: string;
  context: string;
  collaboration_rating: string;
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

export default function PeerAssessmentPage() {
  const [tabValue, setTabValue] = useState(0);
  const [templates, setTemplates] = useState<PeerAssessmentTemplate[]>([]);
  const [selfAssessments, setSelfAssessments] = useState<SelfAssessment[]>([]);
  const [peerAssessments, setPeerAssessments] = useState<PeerAssessment[]>([]);
  const [groupAssessments, setGroupAssessments] = useState<GroupAssessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [openSelfAssessmentDialog, setOpenSelfAssessmentDialog] = useState(false);
  const [openPeerAssessmentDialog, setOpenPeerAssessmentDialog] = useState(false);

  const [templateFormData, setTemplateFormData] = useState({
    template_name: "",
    assessment_type: "PEER",
    subject_id: "",
    phase: "FASE_A",
    assessment_focus: "COLLABORATION",
    description: "",
    criteria: "",
    rating_scale: "",
    instructions: "",
  });

  const [selfAssessmentFormData, setSelfAssessmentFormData] = useState({
    student_id: "",
    template_id: "",
    context: "",
    responses: "",
    self_reflection: "",
    goals_set: "",
    confidence_level: "MEDIUM",
  });

  const [peerAssessmentFormData, setPeerAssessmentFormData] = useState({
    assessor_student_id: "",
    assessed_student_id: "",
    template_id: "",
    context: "",
    responses: "",
    positive_feedback: "",
    constructive_feedback: "",
    suggestions: "",
    relationship_context: "CLASSMATE",
  });

  const fetchTemplates = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/templates`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setTemplates(json.data.templates || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSelfAssessments = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/self-assessments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSelfAssessments(json.data.self_assessments || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const fetchPeerAssessments = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/peer-assessments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setPeerAssessments(json.data.peer_assessments || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const fetchGroupAssessments = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/group-assessments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setGroupAssessments(json.data.group_assessments || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchTemplates();
    fetchSelfAssessments();
    fetchPeerAssessments();
    fetchGroupAssessments();
  }, []);

  const handleCreateTemplate = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/templates`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(templateFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenTemplateDialog(false);
        fetchTemplates();
        setTemplateFormData({
          template_name: "",
          assessment_type: "PEER",
          subject_id: "",
          phase: "FASE_A",
          assessment_focus: "COLLABORATION",
          description: "",
          criteria: "",
          rating_scale: "",
          instructions: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleCreateSelfAssessment = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/self-assessments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(selfAssessmentFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenSelfAssessmentDialog(false);
        fetchSelfAssessments();
        setSelfAssessmentFormData({
          student_id: "",
          template_id: "",
          context: "",
          responses: "",
          self_reflection: "",
          goals_set: "",
          confidence_level: "MEDIUM",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleCreatePeerAssessment = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/peer-assessment/peer-assessments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(peerAssessmentFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenPeerAssessmentDialog(false);
        fetchPeerAssessments();
        setPeerAssessmentFormData({
          assessor_student_id: "",
          assessed_student_id: "",
          template_id: "",
          context: "",
          responses: "",
          positive_feedback: "",
          constructive_feedback: "",
          suggestions: "",
          relationship_context: "CLASSMATE",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getAssessmentTypeLabel = (type: string) => {
    switch (type) {
      case "SELF":
        return "Diri Sendiri";
      case "PEER":
        return "Teman Sebaya";
      case "GROUP":
        return "Kelompok";
      default:
        return type;
    }
  };

  const getAssessmentFocusLabel = (focus: string) => {
    switch (focus) {
      case "COLLABORATION":
        return "Kolaborasi";
      case "COMMUNICATION":
        return "Komunikasi";
      case "CREATIVITY":
        return "Kreativitas";
      case "CRITICAL_THINKING":
        return "Berpikir Kritis";
      case "PARTICIPATION":
        return "Partisipasi";
      default:
        return focus;
    }
  };

  const getReviewStatusColor = (status: string) => {
    switch (status) {
      case "PENDING":
        return "warning";
      case "APPROVED":
        return "success";
      case "REJECTED":
        return "error";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Asesmen Mandiri & Teman Sebaya (SD)
        </Typography>
        <Button variant="contained" startIcon={<NiStar size="small" />} onClick={() => setOpenTemplateDialog(true)}>
          Template Baru
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Asesmen Mandiri & Teman Sebaya</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Sistem asesmen mandiri dan teman sebaya yang disederhanakan sesuai dengan kebutuhan SD.
      </Alert>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Box sx={{ borderBottom: 1, borderColor: "divider", mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Template Asesmen" />
          <Tab label="Asesmen Diri" />
          <Tab label="Asesmen Teman Sebaya" />
          <Tab label="Asesmen Kelompok" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Nama Template</TableCell>
                <TableCell className="font-bold">Tipe Asesmen</TableCell>
                <TableCell className="font-bold">Fase</TableCell>
                <TableCell className="font-bold">Fokus</TableCell>
                <TableCell className="font-bold">Deskripsi</TableCell>
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
              ) : templates.length > 0 ? (
                templates.map((template) => (
                  <TableRow key={template.id} hover>
                    <TableCell className="font-medium">{template.template_name}</TableCell>
                    <TableCell>
                      <Chip label={getAssessmentTypeLabel(template.assessment_type)} size="small" />
                    </TableCell>
                    <TableCell>{template.phase}</TableCell>
                    <TableCell>
                      <Chip label={getAssessmentFocusLabel(template.assessment_focus)} size="small" />
                    </TableCell>
                    <TableCell className="text-sm">{template.description}</TableCell>
                    <TableCell>
                      <Chip
                        label={template.is_active ? "Aktif" : "Nonaktif"}
                        color={template.is_active ? "success" : "default"}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    Tidak ada template asesmen.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box className="mb-4">
          <Button
            variant="outlined"
            startIcon={<NiStar size="small" />}
            onClick={() => setOpenSelfAssessmentDialog(true)}
          >
            Asesmen Diri Baru
          </Button>
        </Box>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Student ID</TableCell>
                <TableCell className="font-bold">Tanggal</TableCell>
                <TableCell className="font-bold">Konteks</TableCell>
                <TableCell className="font-bold">Confidence</TableCell>
                <TableCell className="font-bold">Feedback Guru</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {selfAssessments.length > 0 ? (
                selfAssessments.map((assessment) => (
                  <TableRow key={assessment.id} hover>
                    <TableCell className="text-sm">{assessment.student_id}</TableCell>
                    <TableCell className="text-sm">{assessment.assessment_date}</TableCell>
                    <TableCell className="text-sm">{assessment.context}</TableCell>
                    <TableCell>
                      <Chip
                        label={assessment.confidence_level}
                        color={assessment.confidence_level === "HIGH" ? "success" : "info"}
                        size="small"
                      />
                    </TableCell>
                    <TableCell className="text-sm">{assessment.teacher_feedback || "N/A"}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center" className="py-10">
                    Tidak ada asesmen diri.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box className="mb-4">
          <Button
            variant="outlined"
            startIcon={<NiStar size="small" />}
            onClick={() => setOpenPeerAssessmentDialog(true)}
          >
            Asesmen Teman Sebaya Baru
          </Button>
        </Box>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Penilai</TableCell>
                <TableCell className="font-bold">Dinilai</TableCell>
                <TableCell className="font-bold">Tanggal</TableCell>
                <TableCell className="font-bold">Konteks</TableCell>
                <TableCell className="font-bold">Relasi</TableCell>
                <TableCell className="font-bold">Status Review</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {peerAssessments.length > 0 ? (
                peerAssessments.map((assessment) => (
                  <TableRow key={assessment.id} hover>
                    <TableCell className="text-sm">{assessment.assessor_student_id}</TableCell>
                    <TableCell className="text-sm">{assessment.assessed_student_id}</TableCell>
                    <TableCell className="text-sm">{assessment.assessment_date}</TableCell>
                    <TableCell className="text-sm">{assessment.context}</TableCell>
                    <TableCell>
                      <Chip label={assessment.relationship_context} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={assessment.teacher_review_status}
                        color={getReviewStatusColor(assessment.teacher_review_status)}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    Tidak ada asesmen teman sebaya.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Nama Kelompok</TableCell>
                <TableCell className="font-bold">Tanggal</TableCell>
                <TableCell className="font-bold">Konteks</TableCell>
                <TableCell className="font-bold">Rating Kolaborasi</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {groupAssessments.length > 0 ? (
                groupAssessments.map((assessment) => (
                  <TableRow key={assessment.id} hover>
                    <TableCell className="font-medium">{assessment.group_name}</TableCell>
                    <TableCell className="text-sm">{assessment.assessment_date}</TableCell>
                    <TableCell className="text-sm">{assessment.context}</TableCell>
                    <TableCell>
                      <Chip
                        label={assessment.collaboration_rating}
                        color={assessment.collaboration_rating === "EXCELLENT" ? "success" : "info"}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} align="center" className="py-10">
                    Tidak ada asesmen kelompok.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Template Dialog */}
      <Dialog open={openTemplateDialog} onClose={() => setOpenTemplateDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Template Asesmen Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Nama Template"
              fullWidth
              value={templateFormData.template_name}
              onChange={(e) => setTemplateFormData({ ...templateFormData, template_name: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tipe Asesmen</InputLabel>
              <Select
                value={templateFormData.assessment_type}
                label="Tipe Asesmen"
                onChange={(e) => setTemplateFormData({ ...templateFormData, assessment_type: e.target.value })}
              >
                <MenuItem value="SELF">Diri Sendiri</MenuItem>
                <MenuItem value="PEER">Teman Sebaya</MenuItem>
                <MenuItem value="GROUP">Kelompok</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Subject ID"
              fullWidth
              value={templateFormData.subject_id}
              onChange={(e) => setTemplateFormData({ ...templateFormData, subject_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Fase</InputLabel>
              <Select
                value={templateFormData.phase}
                label="Fase"
                onChange={(e) => setTemplateFormData({ ...templateFormData, phase: e.target.value })}
              >
                <MenuItem value="FASE_A">Fase A (Kelas 1-2)</MenuItem>
                <MenuItem value="FASE_B">Fase B (Kelas 3-4)</MenuItem>
                <MenuItem value="FASE_C">Fase C (Kelas 5-6)</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Fokus Asesmen</InputLabel>
              <Select
                value={templateFormData.assessment_focus}
                label="Fokus Asesmen"
                onChange={(e) => setTemplateFormData({ ...templateFormData, assessment_focus: e.target.value })}
              >
                <MenuItem value="COLLABORATION">Kolaborasi</MenuItem>
                <MenuItem value="COMMUNICATION">Komunikasi</MenuItem>
                <MenuItem value="CREATIVITY">Kreativitas</MenuItem>
                <MenuItem value="CRITICAL_THINKING">Berpikir Kritis</MenuItem>
                <MenuItem value="PARTICIPATION">Partisipasi</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Deskripsi"
              fullWidth
              multiline
              rows={3}
              value={templateFormData.description}
              onChange={(e) => setTemplateFormData({ ...templateFormData, description: e.target.value })}
            />
            <TextField
              label="Kriteria (JSON)"
              fullWidth
              multiline
              rows={3}
              value={templateFormData.criteria}
              onChange={(e) => setTemplateFormData({ ...templateFormData, criteria: e.target.value })}
            />
            <TextField
              label="Skala Rating (JSON)"
              fullWidth
              multiline
              rows={2}
              value={templateFormData.rating_scale}
              onChange={(e) => setTemplateFormData({ ...templateFormData, rating_scale: e.target.value })}
            />
            <TextField
              label="Instruksi"
              fullWidth
              multiline
              rows={2}
              value={templateFormData.instructions}
              onChange={(e) => setTemplateFormData({ ...templateFormData, instructions: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenTemplateDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateTemplate}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Self Assessment Dialog */}
      <Dialog
        open={openSelfAssessmentDialog}
        onClose={() => setOpenSelfAssessmentDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Asesmen Diri Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Student ID"
              fullWidth
              value={selfAssessmentFormData.student_id}
              onChange={(e) => setSelfAssessmentFormData({ ...selfAssessmentFormData, student_id: e.target.value })}
            />
            <TextField
              label="Template ID"
              fullWidth
              value={selfAssessmentFormData.template_id}
              onChange={(e) => setSelfAssessmentFormData({ ...selfAssessmentFormData, template_id: e.target.value })}
            />
            <TextField
              label="Konteks"
              fullWidth
              value={selfAssessmentFormData.context}
              onChange={(e) => setSelfAssessmentFormData({ ...selfAssessmentFormData, context: e.target.value })}
            />
            <TextField
              label="Respons (JSON)"
              fullWidth
              multiline
              rows={3}
              value={selfAssessmentFormData.responses}
              onChange={(e) => setSelfAssessmentFormData({ ...selfAssessmentFormData, responses: e.target.value })}
            />
            <TextField
              label="Refleksi Diri"
              fullWidth
              multiline
              rows={3}
              value={selfAssessmentFormData.self_reflection}
              onChange={(e) =>
                setSelfAssessmentFormData({ ...selfAssessmentFormData, self_reflection: e.target.value })
              }
            />
            <TextField
              label="Goals Set (JSON array)"
              fullWidth
              value={selfAssessmentFormData.goals_set}
              onChange={(e) => setSelfAssessmentFormData({ ...selfAssessmentFormData, goals_set: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Confidence Level</InputLabel>
              <Select
                value={selfAssessmentFormData.confidence_level}
                label="Confidence Level"
                onChange={(e) =>
                  setSelfAssessmentFormData({ ...selfAssessmentFormData, confidence_level: e.target.value })
                }
              >
                <MenuItem value="LOW">Rendah</MenuItem>
                <MenuItem value="MEDIUM">Sedang</MenuItem>
                <MenuItem value="HIGH">Tinggi</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenSelfAssessmentDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateSelfAssessment}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Peer Assessment Dialog */}
      <Dialog
        open={openPeerAssessmentDialog}
        onClose={() => setOpenPeerAssessmentDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Asesmen Teman Sebaya Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Penilai Student ID"
              fullWidth
              value={peerAssessmentFormData.assessor_student_id}
              onChange={(e) =>
                setPeerAssessmentFormData({ ...peerAssessmentFormData, assessor_student_id: e.target.value })
              }
            />
            <TextField
              label="Dinilai Student ID"
              fullWidth
              value={peerAssessmentFormData.assessed_student_id}
              onChange={(e) =>
                setPeerAssessmentFormData({ ...peerAssessmentFormData, assessed_student_id: e.target.value })
              }
            />
            <TextField
              label="Template ID"
              fullWidth
              value={peerAssessmentFormData.template_id}
              onChange={(e) => setPeerAssessmentFormData({ ...peerAssessmentFormData, template_id: e.target.value })}
            />
            <TextField
              label="Konteks"
              fullWidth
              value={peerAssessmentFormData.context}
              onChange={(e) => setPeerAssessmentFormData({ ...peerAssessmentFormData, context: e.target.value })}
            />
            <TextField
              label="Respons (JSON)"
              fullWidth
              multiline
              rows={3}
              value={peerAssessmentFormData.responses}
              onChange={(e) => setPeerAssessmentFormData({ ...peerAssessmentFormData, responses: e.target.value })}
            />
            <TextField
              label="Feedback Positif"
              fullWidth
              multiline
              rows={2}
              value={peerAssessmentFormData.positive_feedback}
              onChange={(e) =>
                setPeerAssessmentFormData({ ...peerAssessmentFormData, positive_feedback: e.target.value })
              }
            />
            <TextField
              label="Feedback Konstruktif"
              fullWidth
              multiline
              rows={2}
              value={peerAssessmentFormData.constructive_feedback}
              onChange={(e) =>
                setPeerAssessmentFormData({ ...peerAssessmentFormData, constructive_feedback: e.target.value })
              }
            />
            <TextField
              label="Saran (JSON array)"
              fullWidth
              multiline
              rows={2}
              value={peerAssessmentFormData.suggestions}
              onChange={(e) => setPeerAssessmentFormData({ ...peerAssessmentFormData, suggestions: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Konteks Relasi</InputLabel>
              <Select
                value={peerAssessmentFormData.relationship_context}
                label="Konteks Relasi"
                onChange={(e) =>
                  setPeerAssessmentFormData({ ...peerAssessmentFormData, relationship_context: e.target.value })
                }
              >
                <MenuItem value="GROUP_MEMBER">Anggota Kelompok</MenuItem>
                <MenuItem value="CLASSMATE">Teman Kelas</MenuItem>
                <MenuItem value="PROJECT_PARTNER">Partner Proyek</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPeerAssessmentDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreatePeerAssessment}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
