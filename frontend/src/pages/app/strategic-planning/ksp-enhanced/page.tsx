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
  Alert,
  Snackbar,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Tabs,
  Tab,
  Checkbox,
  FormGroup,
  FormControlLabel,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  AppBar,
  Toolbar,
  Tooltip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Switch,
  Slider,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Download as DownloadIcon,
  Save as SaveIcon,
  Close as CloseIcon,
  Description as DocumentIcon,
  Dashboard as TemplateIcon,
  Assessment as AnalyticsIcon,
  Preview as PreviewIcon,
  Check as CheckIcon,
  ExpandMore as ExpandMoreIcon,
  Visibility as ViewIcon,
  School as SchoolIcon,
  AutoFixHigh as AutoFixIcon,
} from "@mui/material";

interface KSPTemplate {
  id: string;
  template_name: string;
  template_category: string;
  template_description: string;
  integration_structure: any;
  is_public: boolean;
  is_active: boolean;
  usage_count: number;
  created_by: string;
  created_at: string;
  updated_at: string;
}

interface KSPIntegration {
  id: string;
  curriculum_document_id: string;
  school_id: string;
  integration_type: string;
  selected_data_points: DataPointSelection[];
  custom_sections: CustomSection[];
  include_charts: boolean;
  include_recommendations: boolean;
  integration_status: string;
  created_at: string;
  updated_at: string;
}

interface DataPointSelection {
  data_type: string;
  data_id: string;
  section: string;
  priority: number;
  notes: string;
}

interface CustomSection {
  section_title: string;
  section_order: number;
  content: string;
  include_in_toc: boolean;
}

interface AnalysisSnapshot {
  integration_id: string;
  swot_data: any;
  root_cause_data: any;
  fishbone_data: any;
  student_needs_data: any;
  survey_data: any;
  rapor_data: any;
  captured_at: string;
}

const KSPEnhancedPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [templates, setTemplates] = useState<KSPTemplate[]>([]);
  const [integrations, setIntegrations] = useState<KSPIntegration[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<KSPTemplate | null>(null);
  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [openIntegrationDialog, setOpenIntegrationDialog] = useState(false);
  const [openPreviewDialog, setOpenPreviewDialog] = useState(false);
  const [analysisSnapshot, setAnalysisSnapshot] = useState<AnalysisSnapshot | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedDataPoints, setSelectedDataPoints] = useState<DataPointSelection[]>([]);
  const [customSections, setCustomSections] = useState<CustomSection[]>([]);
  const [includeCharts, setIncludeCharts] = useState(true);
  const [includeRecommendations, setIncludeRecommendations] = useState(true);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });

  useEffect(() => {
    loadTemplates();
    loadIntegrations();
  }, []);

  const loadTemplates = async () => {
    // Simulate loading templates
    setTemplates([
      {
        id: "00000000-0000-0000-0000-000000000010",
        template_name: "Comprehensive Strategic Planning",
        template_category: "STRATEGIC",
        template_description: "Template lengkap untuk perencanaan strategis dengan semua analisis",
        integration_structure: {
          include_swot: true,
          include_root_cause: true,
          include_fishbone: true,
          include_student_needs: true,
          sections: ["EXECUTIVE_SUMMARY", "ANALISIS_SWOT", "ANALISIS_AKAR_MASALAH", "DIAGRAM_FISHBONE", "KEBUTUHAN_SISWA", "RENCANA_TINDAKAN", "MONITORING_EVALUASI"],
        },
        is_public: true,
        is_active: true,
        usage_count: 15,
        created_by: "system",
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
      {
        id: "00000000-0000-0000-0000-000000000011",
        template_name: "SWOT Focus Analysis",
        template_category: "SWOT",
        template_description: "Template fokus analisis SWOT untuk perencanaan cepat",
        integration_structure: {
          include_swot: true,
          include_root_cause: false,
          include_fishbone: false,
          include_student_needs: false,
          sections: ["EXECUTIVE_SUMMARY", "ANALISIS_SWOT", "RENCANA_TINDAKAN"],
        },
        is_public: true,
        is_active: true,
        usage_count: 8,
        created_by: "system",
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
      {
        id: "00000000-0000-0000-0000-000000000012",
        template_name: "Problem Solving Focus",
        template_category: "PROBLEM_SOLVING",
        template_description: "Template fokus pemecahan masalah dengan root cause dan fishbone",
        integration_structure: {
          include_swot: false,
          include_root_cause: true,
          include_fishbone: true,
          include_student_needs: false,
          sections: ["EXECUTIVE_SUMMARY", "IDENTIFIKASI_MASALAH", "ANALISIS_AKAR_MASALAH", "DIAGRAM_FISHBONE", "RENCANA_PERBAIKAN"],
        },
        is_public: true,
        is_active: true,
        usage_count: 5,
        created_by: "system",
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
    ]);
  };

  const loadIntegrations = async () => {
    // Simulate loading integrations
    setIntegrations([
      {
        id: "1",
        curriculum_document_id: "doc-1",
        school_id: "school-1",
        integration_type: "COMPREHENSIVE",
        selected_data_points: [],
        custom_sections: [],
        include_charts: true,
        include_recommendations: true,
        integration_status: "COMPLETED",
        created_at: "2025-01-15T10:00:00Z",
        updated_at: "2025-01-20T14:30:00Z",
      },
    ]);
  };

  const handleUseTemplate = (template: KSPTemplate) => {
    setSelectedTemplate(template);
    setCurrentStep(0);
    setSelectedDataPoints([]);
    setCustomSections([]);
    setIncludeCharts(true);
    setIncludeRecommendations(true);
    setOpenIntegrationDialog(true);
    setOpenTemplateDialog(false);
  };

  const handleAddDataPoint = () => {
    const newPoint: DataPointSelection = {
      data_type: "SWOT",
      data_id: "",
      section: "ANALISIS",
      priority: 1,
      notes: "",
    };
    setSelectedDataPoints([...selectedDataPoints, newPoint]);
  };

  const handleRemoveDataPoint = (index: number) => {
    setSelectedDataPoints(selectedDataPoints.filter((_, i) => i !== index));
  };

  const handleAddCustomSection = () => {
    const newSection: CustomSection = {
      section_title: "",
      section_order: customSections.length + 1,
      content: "",
      include_in_toc: true,
    };
    setCustomSections([...customSections, newSection]);
  };

  const handleRemoveCustomSection = (index: number) => {
    setCustomSections(customSections.filter((_, i) => i !== index));
  };

  const handleGenerateDocument = () => {
    // Simulate document generation
    setSnackbar({
      open: true,
      message: "Dokumen KSP sedang dibuat...",
      severity: "info",
    });

    setTimeout(() => {
      setSnackbar({
        open: true,
        message: "Dokumen KSP berhasil dibuat",
        severity: "success",
      });
      setOpenIntegrationDialog(false);
    }, 2000);
  };

  const handlePreviewDocument = (integration: KSPIntegration) => {
    // Simulate generating analysis snapshot
    setAnalysisSnapshot({
      integration_id: integration.id,
      swot_data: {
        total_items: {
          strengths: 5,
          weaknesses: 3,
          opportunities: 4,
          threats: 2,
        },
        priority_items: ["Kompetensi guru kurang", "Keterbatasan peralatan ICT"],
      },
      root_cause_data: {
        total_root_causes: 3,
        resolved: 1,
        in_progress: 2,
        top_issues: ["Hasil belajar menurun", "Kehadiran guru tidak stabil"],
      },
      fishbone_data: {
        total_diagrams: 2,
        total_nodes: 10,
        category_distribution: {
          MAN: 2,
          METHOD: 3,
          MACHINE: 2,
          MATERIAL: 2,
          ENVIRONMENT: 1,
        },
      },
      student_needs_data: {
        total_profiles: 50,
        critical_needs: 5,
        priority_areas: ["BERIMAN", "MANDIRI"],
      },
      survey_data: {},
      rapor_data: {},
      captured_at: new Date().toISOString(),
    });
    setOpenPreviewDialog(true);
  };

  const renderTemplateCard = (template: KSPTemplate) => (
    <Card
      key={template.id}
      sx={{
        cursor: "pointer",
        border: selectedTemplate?.id === template.id ? "2px solid #1976d2" : "1px solid #e0e0e0",
        "&:hover": {
          boxShadow: 3,
        },
      }}
      onClick={() => setSelectedTemplate(template)}
    >
      <CardContent>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 1 }}>
          <Typography variant="h6" gutterBottom>
            {template.template_name}
          </Typography>
          <Chip label={`${template.usage_count}x`} size="small" variant="outlined" />
        </Box>
        <Typography variant="body2" color="text.secondary" paragraph>
          {template.template_description}
        </Typography>
        <Box sx={{ display: "flex", gap: 1, mb: 1 }}>
          <Chip label={template.template_category} size="small" variant="outlined" />
          {template.is_public && (
            <Chip label="Public" size="small" color="primary" variant="outlined" />
          )}
        </Box>
        <Typography variant="caption" color="text.secondary">
          Sections: {template.integration_structure.sections?.length || 0}
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Button
            variant="contained"
            size="small"
            fullWidth
            startIcon={<AutoFixIcon />}
            onClick={() => handleUseTemplate(template)}
          >
            Gunakan Template
          </Button>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="xl">
      <Box sx={{ mt: 4, mb: 4 }}>
        <AppBar position="static" color="default" elevation={0} sx={{ mb: 3 }}>
          <Toolbar>
            <Typography variant="h5" component="h1" sx={{ flexGrow: 1 }}>
              KSP Enhanced Generator
            </Typography>
            <Button
              variant="contained"
              startIcon={<TemplateIcon />}
              onClick={() => setOpenTemplateDialog(true)}
            >
              Buat dari Template
            </Button>
          </Toolbar>
        </AppBar>

        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
          <Tab label="Template KSP" />
          <Tab label="Integrasi Analisis" />
        </Tabs>

        {activeTab === 0 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Template KSP yang Tersedia
            </Typography>
            <Grid container spacing={3}>
              {templates.map((template) => (
                <Grid item xs={12} md={6} lg={4} key={template.id}>
                  {renderTemplateCard(template)}
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {activeTab === 1 && (
          <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
              <Typography variant="h6">
                Integrasi Analisis KSP
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setOpenTemplateDialog(true)}
              >
                Buat Integrasi Baru
              </Button>
            </Box>

            <Grid container spacing={3}>
              {integrations.map((integration) => (
                <Grid item xs={12} md={6} key={integration.id}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 2 }}>
                        <Typography variant="h6" gutterBottom>
                          Integrasi #{integration.id}
                        </Typography>
                        <Chip
                          label={integration.integration_status}
                          size="small"
                          color={integration.integration_status === "COMPLETED" ? "success" : "warning"}
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        Type: {integration.integration_type}
                      </Typography>
                      <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
                        <Button
                          size="small"
                          variant="outlined"
                          startIcon={<PreviewIcon />}
                          onClick={() => handlePreviewDocument(integration)}
                        >
                          Preview
                        </Button>
                        <Button
                          size="small"
                          variant="outlined"
                          startIcon={<DownloadIcon />}
                        >
                          Download
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* Template Selection Dialog */}
        <Dialog open={openTemplateDialog} onClose={() => setOpenTemplateDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <TemplateIcon color="primary" />
              <Typography variant="h6">Pilih Template KSP</Typography>
            </Box>
          </DialogTitle>
          <DialogContent>
            <Alert severity="info" sx={{ mb: 2 }}>
              Pilih template untuk memulai pembuatan dokumen KSP dengan struktur yang sudah disiapkan
            </Alert>
            <Grid container spacing={2}>
              {templates.map((template) => (
                <Grid item xs={12} md={6} key={template.id}>
                  {renderTemplateCard(template)}
                </Grid>
              ))}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenTemplateDialog(false)}>Batal</Button>
          </DialogActions>
        </Dialog>

        {/* Integration Wizard Dialog */}
        <Dialog open={openIntegrationDialog} onClose={() => setOpenIntegrationDialog(false)} maxWidth="lg" fullWidth>
          <DialogTitle>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <AutoFixIcon color="primary" />
              <Typography variant="h6">
                {selectedTemplate?.template_name} - Konfigurasi Integrasi
              </Typography>
            </Box>
          </DialogTitle>
          <DialogContent>
            <Stepper activeStep={currentStep} orientation="vertical">
              <Step>
                <StepLabel>Pilih Data Analisis</StepLabel>
                <StepContent>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    Pilih data analisis yang ingin disertakan dalam dokumen KSP
                  </Alert>
                  <Box sx={{ mb: 2 }}>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<AddIcon />}
                      onClick={handleAddDataPoint}
                    >
                      Tambah Data Point
                    </Button>
                  </Box>
                  {selectedDataPoints.map((point, index) => (
                    <Paper key={index} sx={{ p: 2, mb: 1, display: "flex", alignItems: "center", gap: 1 }}>
                      <FormControl size="small" sx={{ minWidth: 120 }}>
                        <Select
                          value={point.data_type}
                          onChange={(e) => {
                            const updated = [...selectedDataPoints];
                            updated[index].data_type = e.target.value;
                            setSelectedDataPoints(updated);
                          }}
                        >
                          <MenuItem value="SWOT">SWOT</MenuItem>
                          <MenuItem value="ROOT_CAUSE">Root Cause</MenuItem>
                          <MenuItem value="FISHBONE">Fishbone</MenuItem>
                          <MenuItem value="STUDENT_NEEDS">Student Needs</MenuItem>
                        </Select>
                      </FormControl>
                      <TextField
                        size="small"
                        placeholder="Data ID"
                        value={point.data_id}
                        onChange={(e) => {
                          const updated = [...selectedDataPoints];
                          updated[index].data_id = e.target.value;
                          setSelectedDataPoints(updated);
                        }}
                      />
                      <IconButton size="small" onClick={() => handleRemoveDataPoint(index)}>
                        <DeleteIcon />
                      </IconButton>
                    </Paper>
                  ))}
                  <Box sx={{ mt: 2 }}>
                    <Button onClick={() => setCurrentStep(currentStep + 1)} disabled={selectedDataPoints.length === 0}>
                      Lanjut
                    </Button>
                  </Box>
                </StepContent>
              </Step>

              <Step>
                <StepLabel>Custom Sections</StepLabel>
                <StepContent>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    Tambah section kustom untuk dokumen KSP
                  </Alert>
                  <Box sx={{ mb: 2 }}>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<AddIcon />}
                      onClick={handleAddCustomSection}
                    >
                      Tambah Section
                    </Button>
                  </Box>
                  {customSections.map((section, index) => (
                    <Paper key={index} sx={{ p: 2, mb: 1 }}>
                      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
                        <TextField
                          size="small"
                          label="Judul Section"
                          value={section.section_title}
                          onChange={(e) => {
                            const updated = [...customSections];
                            updated[index].section_title = e.target.value;
                            setCustomSections(updated);
                          }}
                        />
                        <IconButton size="small" onClick={() => handleRemoveCustomSection(index)}>
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                      <TextField
                        size="small"
                        multiline
                        rows={2}
                        label="Konten"
                        value={section.content}
                        onChange={(e) => {
                          const updated = [...customSections];
                          updated[index].content = e.target.value;
                          setCustomSections(updated);
                        }}
                      />
                      <FormControlLabel
                        control={<Checkbox checked={section.include_in_toc} onChange={(e) => {
                          const updated = [...customSections];
                          updated[index].include_in_toc = e.target.checked;
                          setCustomSections(updated);
                        }} />}
                        label="Include in Table of Contents"
                      />
                    </Paper>
                  ))}
                  <Box sx={{ mt: 2 }}>
                    <Button onClick={() => setCurrentStep(currentStep + 1)}>
                      Lanjut
                    </Button>
                    <Button onClick={() => setCurrentStep(currentStep - 1)} sx={{ ml: 1 }}>
                      Kembali
                    </Button>
                  </Box>
                </StepContent>
              </Step>

              <Step>
                <StepLabel>Options</StepLabel>
                <StepContent>
                  <FormGroup sx={{ mb: 2 }}>
                    <FormControlLabel
                      control={<Checkbox checked={includeCharts} onChange={(e) => setIncludeCharts(e.target.checked)} />}
                      label="Include Charts"
                    />
                    <FormControlLabel
                      control={<Checkbox checked={includeRecommendations} onChange={(e) => setIncludeRecommendations(e.target.checked)} />}
                      label="Include Recommendations"
                    />
                  </FormGroup>
                  <Box sx={{ mt: 2 }}>
                    <Button
                      variant="contained"
                      onClick={handleGenerateDocument}
                      startIcon={<AutoFixIcon />}
                    >
                      Generate Dokumen
                    </Button>
                    <Button onClick={() => setCurrentStep(currentStep - 1)} sx={{ ml: 1 }}>
                      Kembali
                    </Button>
                  </Box>
                </StepContent>
              </Step>
            </Stepper>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenIntegrationDialog(false)}>Batal</Button>
          </DialogActions>
        </Dialog>

        {/* Preview Dialog */}
        <Dialog open={openPreviewDialog} onClose={() => setOpenPreviewDialog(false)} maxWidth="lg" fullWidth>
          <DialogTitle>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <PreviewIcon color="primary" />
              <Typography variant="h6">Preview Dokumen KSP</Typography>
            </Box>
          </DialogTitle>
          <DialogContent>
            {analysisSnapshot && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Executive Summary
                </Typography>
                <Paper sx={{ p: 2, mb: 3 }}>
                  <Typography variant="body2">
                    Dokumen ini berisi analisis komprehensif untuk perencanaan strategis pendidikan,
                    mengintegrasikan berbagai data analisis dari modul Strategic Planning.
                  </Typography>
                </Paper>

                {analysisSnapshot.swot_data && (
                  <Accordion defaultExpanded>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography variant="h6">Analisis SWOT</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Card sx={{ backgroundColor: "#4CAF50", color: "white" }}>
                            <CardContent>
                              <Typography variant="h3">{analysisSnapshot.swot_data.total_items?.strengths || 0}</Typography>
                              <Typography variant="body2">Strengths</Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                        <Grid item xs={6}>
                          <Card sx={{ backgroundColor: "#F44336", color: "white" }}>
                            <CardContent>
                              <Typography variant="h3">{analysisSnapshot.swot_data.total_items?.weaknesses || 0}</Typography>
                              <Typography variant="body2">Weaknesses</Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                        <Grid item xs={6}>
                          <Card sx={{ backgroundColor: "#2196F3", color: "white" }}>
                            <CardContent>
                              <Typography variant="h3">{analysisSnapshot.swot_data.total_items?.opportunities || 0}</Typography>
                              <Typography variant="body2">Opportunities</Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                        <Grid item xs={6}>
                          <Card sx={{ backgroundColor: "#FF9800", color: "white" }}>
                            <CardContent>
                              <Typography variant="h3">{analysisSnapshot.swot_data.total_items?.threats || 0}</Typography>
                              <Typography variant="body2">Threats</Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                      </Grid>
                    </AccordionDetails>
                  </Accordion>
                )}

                {analysisSnapshot.root_cause_data && (
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography variant="h6">Analisis Root Cause</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2">
                        Total Root Causes: {analysisSnapshot.root_cause_data.total_root_causes}
                      </Typography>
                      <Typography variant="body2">
                        Resolved: {analysisSnapshot.root_cause_data.resolved}
                      </Typography>
                      <Typography variant="body2">
                        In Progress: {analysisSnapshot.root_cause_data.in_progress}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                )}

                {analysisSnapshot.fishbone_data && (
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography variant="h6">Diagram Fishbone</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2">
                        Total Diagrams: {analysisSnapshot.fishbone_data.total_diagrams}
                      </Typography>
                      <Typography variant="body2">
                        Total Nodes: {analysisSnapshot.fishbone_data.total_nodes}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                )}
              </Box>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenPreviewDialog(false)}>Tutup</Button>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={() => {
                setSnackbar({
                  open: true,
                  message: "Dokumen berhasil didownload",
                  severity: "success",
                });
                setOpenPreviewDialog(false);
              }}
            >
              Download
            </Button>
          </DialogActions>
        </Dialog>

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

export default KSPEnhancedPage;