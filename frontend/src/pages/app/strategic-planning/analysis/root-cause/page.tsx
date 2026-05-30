import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Paper,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Alert,
  Snackbar,
  Menu,
  ListItemText,
  ListItemIcon,
  AppBar,
  Toolbar,
  Tooltip,
  Divider,
  List,
  ListItem,
  ListItemText as MuiListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Download as DownloadIcon,
  Lightbulb as LightbulbIcon,
  Link as LinkIcon,
  Save as SaveIcon,
  Close as CloseIcon,
  NavigateNext as NextIcon,
  Check as CheckIcon,
  ExpandMore as ExpandMoreIcon,
  Psychology as PsychologyIcon,
  TrendingUp as TrendingUpIcon,
} from "@mui/icons-material";

interface RootCause {
  id: string;
  problem: string;
  rootCause: string;
  kegiatanBenahi: string;
  status: string;
  priority: string;
  description: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

interface FiveWhysNode {
  level: number;
  question: string;
  answer: string;
  evidence: string[];
  children: FiveWhysNode[];
}

interface FiveWhysResponse {
  root_cause_id: string;
  problem: string;
  analysis_tree: FiveWhysNode[];
  conclusion: string;
  confidence: number;
  created_at: string;
}

interface Suggestion {
  suggestion_id: string;
  root_cause_id: string;
  title: string;
  description: string;
  evidence: string[];
  priority: string;
  source: string;
  relevance: number;
}

const RootCausePage: React.FC = () => {
  const [rootCauses, setRootCauses] = useState<RootCause[]>([]);
  const [selectedRootCause, setSelectedRootCause] = useState<RootCause | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [openFiveWhysWizard, setOpenFiveWhysWizard] = useState(false);
  const [openSuggestions, setOpenSuggestions] = useState(false);
  const [openRaporLink, setOpenRaporLink] = useState(false);
  const [editingRootCause, setEditingRootCause] = useState<RootCause | null>(null);
  const [newRootCause, setNewRootCause] = useState<Partial<RootCause>>({
    status: "OPEN",
    priority: "MEDIUM",
  });
  const [fiveWhysStep, setFiveWhysStep] = useState(0);
  const [fiveWhysProblem, setFiveWhysProblem] = useState("");
  const [fiveWhysAnswers, setFiveWhysAnswers] = useState<string[]>([]);
  const [fiveWhysResult, setFiveWhysResult] = useState<FiveWhysResponse | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });
  const [exportMenuAnchor, setExportMenuAnchor] = useState<null | HTMLElement>(null);

  useEffect(() => {
    loadRootCauses();
  }, []);

  const loadRootCauses = async () => {
    // Simulate loading root causes
    setRootCauses([
      {
        id: "1",
        problem: "Hasil belajar siswa menurun",
        rootCause: "Metode pembelajaran kurang variatif",
        kegiatanBenahi: "Pelatihan guru metode pembelajaran aktif",
        status: "OPEN",
        priority: "HIGH",
        description: "Penurunan hasil belajar terdeteksi pada semester ini",
        schoolId: "school-1",
        createdAt: "2025-01-15T10:00:00Z",
        updatedAt: "2025-01-20T14:30:00Z",
      },
      {
        id: "2",
        problem: "Kehadiran guru tidak stabil",
        rootCause: "Kondisi kesehatan dan transportasi",
        kegiatanBenahi: "Program kesehatan guru dan fasilitas transportasi",
        status: "IN_PROGRESS",
        priority: "MEDIUM",
        description: "Fluktuasi kehadiran guru mempengaruhi proses belajar",
        schoolId: "school-1",
        createdAt: "2025-01-10T08:00:00Z",
        updatedAt: "2025-01-18T16:00:00Z",
      },
    ]);
  };

  const handleAddRootCause = () => {
    setEditingRootCause(null);
    setNewRootCause({
      status: "OPEN",
      priority: "MEDIUM",
    });
    setOpenDialog(true);
  };

  const handleEditRootCause = (rootCause: RootCause) => {
    setEditingRootCause(rootCause);
    setNewRootCause({ ...rootCause });
    setOpenDialog(true);
  };

  const handleSaveRootCause = () => {
    if (!newRootCause.problem || !newRootCause.rootCause) {
      setSnackbar({
        open: true,
        message: "Masalah dan akar masalah harus diisi",
        severity: "error",
      });
      return;
    }

    if (editingRootCause) {
      setRootCauses(
        rootCauses.map((rc) => (rc.id === editingRootCause.id ? { ...rc, ...newRootCause } : rc))
      );
      setSnackbar({
        open: true,
        message: "Akar masalah berhasil diperbarui",
        severity: "success",
      });
    } else {
      const newRC: RootCause = {
        id: Date.now().toString(),
        problem: newRootCause.problem!,
        rootCause: newRootCause.rootCause!,
        kegiatanBenahi: newRootCause.kegiatanBenahi || "",
        status: newRootCause.status || "OPEN",
        priority: newRootCause.priority || "MEDIUM",
        description: newRootCause.description || "",
        schoolId: "school-1",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      setRootCauses([...rootCauses, newRC]);
      setSnackbar({
        open: true,
        message: "Akar masalah berhasil ditambahkan",
        severity: "success",
      });
    }

    setOpenDialog(false);
    setEditingRootCause(null);
    setNewRootCause({});
  };

  const handleDeleteRootCause = (id: string) => {
    setRootCauses(rootCauses.filter((rc) => rc.id !== id));
    setSnackbar({
      open: true,
      message: "Akar masalah berhasil dihapus",
      severity: "success",
    });
  };

  const handleStartFiveWhys = (rootCause: RootCause) => {
    setSelectedRootCause(rootCause);
    setFiveWhysProblem(rootCause.problem);
    setFiveWhysAnswers([]);
    setFiveWhysStep(0);
    setFiveWhysResult(null);
    setOpenFiveWhysWizard(true);
  };

  const handleFiveWhysNext = () => {
    if (fiveWhysAnswers[fiveWhysStep]) {
      if (fiveWhysStep < 4) {
        setFiveWhysStep(fiveWhysStep + 1);
      } else {
        // Complete 5-Whys analysis
        performFiveWhysAnalysis();
      }
    } else {
      setSnackbar({
        open: true,
        message: "Silakan jawab pertanyaan terlebih dahulu",
        severity: "warning",
      });
    }
  };

  const performFiveWhysAnalysis = async () => {
    // Simulate 5-Whys analysis
    const mockResult: FiveWhysResponse = {
      root_cause_id: selectedRootCause!.id,
      problem: fiveWhysProblem,
      analysis_tree: [
        {
          level: 1,
          question: `Mengapa ${fiveWhysProblem}?`,
          answer: fiveWhysAnswers[0],
          evidence: [],
          children: [
            {
              level: 2,
              question: "Mengapa " + fiveWhysAnswers[0] + "?",
              answer: fiveWhysAnswers[1] || "Tidak ada jawaban",
              evidence: [],
              children: [],
            },
          ],
        },
      ],
      conclusion: "Akar masalah utama: " + (fiveWhysAnswers[4] || fiveWhysAnswers[0]),
      confidence: 0.75,
      created_at: new Date().toISOString(),
    };

    setFiveWhysResult(mockResult);
  };

  const handleShowSuggestions = async (rootCause: RootCause) => {
    setSelectedRootCause(rootCause);
    // Simulate loading suggestions
    setSuggestions([
      {
        suggestion_id: "1",
        root_cause_id: rootCause.id,
        title: "Program pembinaan guru",
        description: "Laksanakan pelatihan berkelanjutan untuk meningkatkan kompetensi guru",
        evidence: [rootCause.problem],
        priority: "HIGH",
        source: "SYSTEM",
        relevance: 0.85,
      },
      {
        suggestion_id: "2",
        root_cause_id: rootCause.id,
        title: "Peningkatan sarana prasarana",
        description: "Perbaiki dan lengkapi fasilitas pembelajaran yang kurang memadai",
        evidence: [rootCause.rootCause],
        priority: "MEDIUM",
        source: "SYSTEM",
        relevance: 0.70,
      },
    ]);
    setOpenSuggestions(true);
  };

  const handleExport = async (format: "json" | "csv") => {
    if (!selectedRootCause) return;

    try {
      const exportData = {
        root_cause: selectedRootCause,
        five_whys_result: fiveWhysResult,
        suggestions: suggestions,
        exported_at: new Date().toISOString(),
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `root_cause_${selectedRootCause.id}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setSnackbar({
        open: true,
        message: `Analisis akar masalah berhasil diekspor sebagai ${format.toUpperCase()}`,
        severity: "success",
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Gagal mengekspor analisis akar masalah",
        severity: "error",
      });
    }

    setExportMenuAnchor(null);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "OPEN":
        return "#FF9800";
      case "IN_PROGRESS":
        return "#2196F3";
      case "RESOLVED":
        return "#4CAF50";
      default:
        return "#9E9E9E";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "HIGH":
        return "#F44336";
      case "MEDIUM":
        return "#FF9800";
      case "LOW":
        return "#4CAF50";
      default:
        return "#9E9E9E";
    }
  };

  const renderFiveWhysWizard = () => {
    const questions = [
      `Mengapa ${fiveWhysProblem}?`,
      `Mengapa ${fiveWhysAnswers[0] || "..."}?`,
      `Mengapa ${fiveWhysAnswers[1] || "..."}?`,
      `Mengapa ${fiveWhysAnswers[2] || "..."}?`,
      `Mengapa ${fiveWhysAnswers[3] || "..."}?`,
    ];

    return (
      <Dialog open={openFiveWhysWizard} onClose={() => setOpenFiveWhysWizard(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <PsychologyIcon color="primary" />
            <Typography variant="h6">Analisis 5-Whys</Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          {fiveWhysResult ? (
            <Box sx={{ mt: 2 }}>
              <Alert severity="success" sx={{ mb: 2 }}>
                Analisis 5-Whys selesai!
              </Alert>
              <Typography variant="h6" gutterBottom>
                Kesimpulan:
              </Typography>
              <Typography variant="body1" paragraph>
                {fiveWhysResult.conclusion}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Confidence: {(fiveWhysResult.confidence * 100).toFixed(0)}%
              </Typography>
            </Box>
          ) : (
            <Box sx={{ mt: 2 }}>
              <Stepper activeStep={fiveWhysStep} orientation="vertical">
                {[0, 1, 2, 3, 4].map((step) => (
                  <Step key={step}>
                    <StepLabel>
                      <Typography variant="subtitle1">{questions[step]}</Typography>
                    </StepLabel>
                    <StepContent>
                      <TextField
                        fullWidth
                        multiline
                        rows={3}
                        placeholder="Jawaban Anda..."
                        value={fiveWhysAnswers[step] || ""}
                        onChange={(e) => {
                          const newAnswers = [...fiveWhysAnswers];
                          newAnswers[step] = e.target.value;
                          setFiveWhysAnswers(newAnswers);
                        }}
                        sx={{ mt: 1, mb: 2 }}
                      />
                      <Box sx={{ mb: 2 }}>
                        <Button
                          variant="contained"
                          onClick={handleFiveWhysNext}
                          disabled={!fiveWhysAnswers[step]}
                          endIcon={step < 4 ? <NextIcon /> : <CheckIcon />}
                        >
                          {step < 4 ? "Lanjut" : "Selesai"}
                        </Button>
                        {step > 0 && (
                          <Button onClick={() => setFiveWhysStep(step - 1)} sx={{ ml: 1 }}>
                            Kembali
                          </Button>
                        )}
                      </Box>
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenFiveWhysWizard(false)}>
            {fiveWhysResult ? "Tutup" : "Batal"}
          </Button>
          {fiveWhysResult && (
            <Button
              variant="contained"
              onClick={() => {
                setOpenFiveWhysWizard(false);
                setSnackbar({
                  open: true,
                  message: "Hasil analisis 5-Whys berhasil disimpan",
                  severity: "success",
                });
              }}
            >
              Simpan Hasil
            </Button>
          )}
        </DialogActions>
      </Dialog>
    );
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ mt: 4, mb: 4 }}>
        <AppBar position="static" color="default" elevation={0} sx={{ mb: 3 }}>
          <Toolbar>
            <Typography variant="h5" component="h1" sx={{ flexGrow: 1 }}>
              Analisis Root Cause
            </Typography>
            <Box sx={{ display: "flex", gap: 1 }}>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddRootCause}
              >
                Tambah Root Cause
              </Button>
            </Box>
          </Toolbar>
        </AppBar>

        <Grid container spacing={3}>
          {rootCauses.map((rootCause) => (
            <Grid item xs={12} md={6} lg={4} key={rootCause.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      {rootCause.problem}
                    </Typography>
                    <Box>
                      <IconButton size="small" onClick={() => handleEditRootCause(rootCause)}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleDeleteRootCause(rootCause.id)}>
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" paragraph>
                    {rootCause.description}
                  </Typography>

                  <Divider sx={{ my: 2 }} />

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Akar Masalah:
                    </Typography>
                    <Typography variant="body2">{rootCause.rootCause}</Typography>
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Kegiatan Perbaikan:
                    </Typography>
                    <Typography variant="body2">{rootCause.kegiatanBenahi}</Typography>
                  </Box>

                  <Box sx={{ display: "flex", gap: 1, mb: 2, flexWrap: "wrap" }}>
                    <Chip
                      label={rootCause.status}
                      size="small"
                      sx={{ backgroundColor: getStatusColor(rootCause.status), color: "white" }}
                    />
                    <Chip
                      label={rootCause.priority}
                      size="small"
                      sx={{ backgroundColor: getPriorityColor(rootCause.priority), color: "white" }}
                    />
                  </Box>

                  <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<PsychologyIcon />}
                      onClick={() => handleStartFiveWhys(rootCause)}
                    >
                      5-Whys
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<LightbulbIcon />}
                      onClick={() => handleShowSuggestions(rootCause)}
                    >
                      Saran
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<LinkIcon />}
                      onClick={() => {
                        setSelectedRootCause(rootCause);
                        setOpenRaporLink(true);
                      }}
                    >
                      Link Rapor
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<DownloadIcon />}
                      onClick={(e) => {
                        setSelectedRootCause(rootCause);
                        setExportMenuAnchor(e.currentTarget);
                      }}
                    >
                      Ekspor
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>{editingRootCause ? "Edit Root Cause" : "Tambah Root Cause"}</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              label="Masalah"
              multiline
              rows={2}
              value={newRootCause.problem || ""}
              onChange={(e) => setNewRootCause({ ...newRootCause, problem: e.target.value })}
              sx={{ mt: 2, mb: 2 }}
            />

            <TextField
              fullWidth
              label="Deskripsi"
              multiline
              rows={3}
              value={newRootCause.description || ""}
              onChange={(e) => setNewRootCause({ ...newRootCause, description: e.target.value })}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Akar Masalah"
              multiline
              rows={2}
              value={newRootCause.rootCause || ""}
              onChange={(e) => setNewRootCause({ ...newRootCause, rootCause: e.target.value })}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Kegiatan Perbaikan"
              multiline
              rows={2}
              value={newRootCause.kegiatanBenahi || ""}
              onChange={(e) => setNewRootCause({ ...newRootCause, kegiatanBenahi: e.target.value })}
              sx={{ mb: 2 }}
            />

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Status</InputLabel>
              <Select
                value={newRootCause.status || "OPEN"}
                onChange={(e) => setNewRootCause({ ...newRootCause, status: e.target.value })}
                label="Status"
              >
                <MenuItem value="OPEN">Open</MenuItem>
                <MenuItem value="IN_PROGRESS">In Progress</MenuItem>
                <MenuItem value="RESOLVED">Resolved</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Prioritas</InputLabel>
              <Select
                value={newRootCause.priority || "MEDIUM"}
                onChange={(e) => setNewRootCause({ ...newRootCause, priority: e.target.value })}
                label="Prioritas"
              >
                <MenuItem value="HIGH">High</MenuItem>
                <MenuItem value="MEDIUM">Medium</MenuItem>
                <MenuItem value="LOW">Low</MenuItem>
              </Select>
            </FormControl>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Batal</Button>
            <Button onClick={handleSaveRootCause} variant="contained" startIcon={<SaveIcon />}>
              Simpan
            </Button>
          </DialogActions>
        </Dialog>

        {renderFiveWhysWizard()}

        <Dialog open={openSuggestions} onClose={() => setOpenSuggestions(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <LightbulbIcon color="primary" />
              <Typography variant="h6">Saran Perbaikan</Typography>
            </Box>
          </DialogTitle>
          <DialogContent>
            <List>
              {suggestions.map((suggestion) => (
                <ListItem key={suggestion.suggestion_id}>
                  <Card sx={{ width: "100%" }}>
                    <CardContent>
                      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                        <Typography variant="h6" gutterBottom>
                          {suggestion.title}
                        </Typography>
                        <Chip
                          label={suggestion.priority}
                          size="small"
                          sx={{ backgroundColor: getPriorityColor(suggestion.priority), color: "white" }}
                        />
                      </Box>
                      <Typography variant="body2" paragraph>
                        {suggestion.description}
                      </Typography>
                      <Box sx={{ display: "flex", gap: 1, alignItems: "center" }}>
                        <Typography variant="caption" color="text.secondary">
                          Relevance: {(suggestion.relevance * 100).toFixed(0)}%
                        </Typography>
                        <Chip label={suggestion.source} size="small" variant="outlined" />
                      </Box>
                    </CardContent>
                  </Card>
                </ListItem>
              ))}
            </List>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenSuggestions(false)}>Tutup</Button>
          </DialogActions>
        </Dialog>

        <Dialog open={openRaporLink} onClose={() => setOpenRaporLink(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Link ke Metrik Rapor</DialogTitle>
          <DialogContent>
            <Alert severity="info" sx={{ mb: 2 }}>
              Fitur ini akan menghubungkan akar masalah dengan metrik Rapor Pendidikan Digital
            </Alert>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Tipe Link</InputLabel>
              <Select label="Tipe Link" defaultValue="CAUSE">
                <MenuItem value="CAUSE">Cause (Penyebab)</MenuItem>
                <MenuItem value="EFFECT">Effect (Efek)</MenuItem>
                <MenuItem value="CORRELATION">Correlation (Korelasi)</MenuItem>
              </Select>
            </FormControl>
            <TextField fullWidth label="ID Metrik Rapor" placeholder="Masukkan ID metrik" />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenRaporLink(false)}>Batal</Button>
            <Button variant="contained" onClick={() => setOpenRaporLink(false)}>
              Simpan Link
            </Button>
          </DialogActions>
        </Dialog>

        <Menu
          anchorEl={exportMenuAnchor}
          open={Boolean(exportMenuAnchor)}
          onClose={() => setExportMenuAnchor(null)}
        >
          <MenuItem onClick={() => handleExport("json")}>
            <ListItemIcon>
              <DownloadIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Ekspor JSON</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => handleExport("csv")}>
            <ListItemIcon>
              <DownloadIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Ekspor CSV</ListItemText>
          </MenuItem>
        </Menu>

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
};

export default RootCausePage;