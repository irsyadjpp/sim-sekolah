import React, { useState, useEffect, useRef } from "react";
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
  Menu,
  ListItemText,
  ListItemIcon,
  AppBar,
  Toolbar,
  Tooltip,
  Divider,
  List,
  ListItem,
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  PanTool as PanIcon,
  CenterFocusStrong as CenterIcon,
  Check as CheckIcon,
  Warning as WarningIcon,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Download as DownloadIcon,
  Save as SaveIcon,
  Close as CloseIcon,
  Category as CategoryIcon,
  Assessment as AnalyticsIcon,
  Verified as VerifiedIcon,
  Dashboard as TemplateIcon,
  AutoFixHigh as AutoFixIcon,
} from "@mui/material";

interface FishboneNode {
  id: string;
  causeText: string;
  boneCategory: string;
  parentNodeId?: string;
  positionX: number;
  positionY: number;
  sequenceNo: number;
}

interface FishboneDiagram {
  id: string;
  headEffect: string;
  description: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

interface FishboneCategory {
  category_id: string;
  category_name: string;
  description: string;
  icon: string;
  color: string;
  is_preset: boolean;
}

interface FishboneAnalytics {
  diagram_id: string;
  total_nodes: number;
  total_edges: number;
  category_stats: Array<{ category: string; node_count: number }>;
  depth_analysis: Array<{ depth: number; count: number }>;
  created_at: string;
  updated_at: string;
}

interface ValidationResult {
  diagram_id: string;
  is_valid: boolean;
  issues: string[];
  warnings: string[];
  suggestions: string[];
}

interface FishboneTemplate {
  id: string;
  template_name: string;
  template_category: string;
  template_description: string;
  head_effect: string;
  preset_nodes: PresetNode[];
  is_public: boolean;
  is_active: boolean;
  usage_count: number;
  created_by: string;
  created_at: string;
  updated_at: string;
}

interface PresetNode {
  cause_text: string;
  bone_category: string;
  position_x: number;
  position_y: number;
  sequence_no: number;
}

const FishbonePage: React.FC = () => {
  const [diagrams, setDiagrams] = useState<FishboneDiagram[]>([]);
  const [currentDiagram, setCurrentDiagram] = useState<FishboneDiagram | null>(null);
  const [nodes, setNodes] = useState<FishboneNode[]>([]);
  const [categories, setCategories] = useState<FishboneCategory[]>([]);
  const [analytics, setAnalytics] = useState<FishboneAnalytics | null>(null);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [templates, setTemplates] = useState<FishboneTemplate[]>([]);
  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<FishboneTemplate | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [openNodeDialog, setOpenNodeDialog] = useState(false);
  const [openAnalytics, setOpenAnalytics] = useState(false);
  const [openValidation, setOpenValidation] = useState(false);
  const [editingDiagram, setEditingDiagram] = useState<FishboneDiagram | null>(null);
  const [editingNode, setEditingNode] = useState<FishboneNode | null>(null);
  const [newDiagram, setNewDiagram] = useState<Partial<FishboneDiagram>>({});
  const [newNode, setNewNode] = useState<Partial<FishboneNode>>({
    boneCategory: "MAN",
    positionX: 0,
    positionY: 0,
    sequenceNo: 0,
  });
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  const canvasRef = useRef<HTMLDivElement>(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });
  const [exportMenuAnchor, setExportMenuAnchor] = useState<null | HTMLElement>(null);

  useEffect(() => {
    loadDiagrams();
    loadCategories();
    loadTemplates();
  }, []);

  useEffect(() => {
    if (currentDiagram) {
      loadNodes();
      loadAnalytics();
      validateDiagram();
    }
  }, [currentDiagram]);

  const loadDiagrams = async () => {
    // Simulate loading diagrams
    setDiagrams([
      {
        id: "1",
        headEffect: "Penurunan Kualitas Pembelajaran",
        description: "Analisis sebab-akibat penurunan kualitas pembelajaran",
        schoolId: "school-1",
        createdAt: "2025-01-15T10:00:00Z",
        updatedAt: "2025-01-20T14:30:00Z",
      },
    ]);
  };

  const loadCategories = async () => {
    // Simulate loading categories
    setCategories([
      {
        category_id: "MAN",
        category_name: "Manusia",
        description: "Faktor terkait SDM (guru, staff, siswa)",
        icon: "users",
        color: "#3B82F6",
        is_preset: true,
      },
      {
        category_id: "METHOD",
        category_name: "Metode",
        description: "Faktor terkait proses dan metode pembelajaran",
        icon: "clipboard",
        color: "#10B981",
        is_preset: true,
      },
      {
        category_id: "MACHINE",
        category_name: "Mesin",
        description: "Faktor terkait peralatan dan teknologi",
        icon: "cpu",
        color: "#8B5CF6",
        is_preset: true,
      },
      {
        category_id: "MATERIAL",
        category_name: "Material",
        description: "Faktor terkait bahan dan sumber belajar",
        icon: "book",
        color: "#F59E0B",
        is_preset: true,
      },
      {
        category_id: "ENVIRONMENT",
        category_name: "Lingkungan",
        description: "Faktor terkait lingkungan fisik dan sosial",
        icon: "globe",
        color: "#EF4444",
        is_preset: true,
      },
    ]);
  };

  const loadTemplates = async () => {
    // Simulate loading templates
    setTemplates([
      {
        id: "00000000-0000-0000-0000-000000000001",
        template_name: "Penurunan Kualitas Pembelajaran",
        template_category: "PENDIDIKAN",
        template_description: "Template untuk menganalisis penyebab penurunan kualitas pembelajaran",
        head_effect: "Penurunan Kualitas Pembelajaran",
        preset_nodes: [
          {
            cause_text: "Kompetensi guru kurang",
            bone_category: "MAN",
            position_x: 200,
            position_y: 100,
            sequence_no: 1,
          },
          {
            cause_text: "Metode pembelajaran tradisional",
            bone_category: "METHOD",
            position_x: 200,
            position_y: 200,
            sequence_no: 1,
          },
          {
            cause_text: "Keterbatasan peralatan ICT",
            bone_category: "MACHINE",
            position_x: 200,
            position_y: 300,
            sequence_no: 1,
          },
          {
            cause_text: "Buku ajar kurang relevan",
            bone_category: "MATERIAL",
            position_x: 200,
            position_y: 400,
            sequence_no: 1,
          },
          {
            cause_text: "Lingkungan kelas kurang kondusif",
            bone_category: "ENVIRONMENT",
            position_x: 200,
            position_y: 500,
            sequence_no: 1,
          },
        ],
        is_public: true,
        is_active: true,
        usage_count: 0,
        created_by: "system",
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
      {
        id: "00000000-0000-0000-0000-000000000002",
        template_name: "Masalah Kehadiran Siswa",
        template_category: "PENDIDIKAN",
        template_description: "Template untuk menganalisis penyebab masalah kehadiran siswa",
        head_effect: "Masalah Kehadiran Siswa",
        preset_nodes: [
          {
            cause_text: "Kondisi kesehatan siswa",
            bone_category: "MAN",
            position_x: 200,
            position_y: 100,
            sequence_no: 1,
          },
          {
            cause_text: "Kondisi ekonomi keluarga",
            bone_category: "ENVIRONMENT",
            position_x: 200,
            position_y: 200,
            sequence_no: 1,
          },
          {
            cause_text: "Transportasi ke sekolah",
            bone_category: "MACHINE",
            position_x: 200,
            position_y: 300,
            sequence_no: 1,
          },
          {
            cause_text: "Kurikulum terlalu berat",
            bone_category: "METHOD",
            position_x: 200,
            position_y: 400,
            sequence_no: 1,
          },
          {
            cause_text: "Fasilitas sekolah kurang menarik",
            bone_category: "MATERIAL",
            position_x: 200,
            position_y: 500,
            sequence_no: 1,
          },
        ],
        is_public: true,
        is_active: true,
        usage_count: 0,
        created_by: "system",
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
      {
        id: "00000000-0000-0000-0000-000000000003",
        template_name: "Masalah Disiplin Siswa",
        template_category: "PENDIDIKAN",
        template_description: "Template untuk menganalisis penyebab masalah disiplin siswa",
        head_effect: "Masalah Disiplin Siswa",
        preset_nodes: [
          {
            cause_text: "Pengawasan guru kurang",
            bone_category: "MAN",
            position_x: 200,
            position_y: 100,
            sequence_no: 1,
          },
          {
            cause_text: "Sistem penghargaan kurang",
            bone_category: "METHOD",
            position_x: 200,
            position_y: 200,
            sequence_no: 1,
          },
          {
            cause_text: "Aturan sekolah tidak jelas",
            bone_category: "MATERIAL",
            position_x: 200,
            position_y: 300,
            sequence_no: 1,
          },
          {
            cause_text: "Pengaruh lingkungan sosial",
            bone_category: "ENVIRONMENT",
            position_x: 200,
            position_y: 400,
            sequence_no: 1,
          },
          {
            cause_text: "Kurangnya kegiatan ekstrakurikuler",
            bone_category: "METHOD",
            position_x: 200,
            position_y: 500,
            sequence_no: 1,
          },
        ],
        is_public: true,
        is_active: true,
        usage_count: 0,
        created_by: "system",
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
    ]);
  };

  const loadNodes = async () => {
    if (!currentDiagram) return;
    // Simulate loading nodes
    setNodes([
      {
        id: "1",
        causeText: "Kompetensi guru kurang",
        boneCategory: "MAN",
        positionX: 200,
        positionY: 100,
        sequenceNo: 1,
      },
      {
        id: "2",
        causeText: "Metode pembelajaran tradisional",
        boneCategory: "METHOD",
        positionX: 200,
        positionY: 200,
        sequenceNo: 1,
      },
      {
        id: "3",
        causeText: "Keterbatasan peralatan ICT",
        boneCategory: "MACHINE",
        positionX: 200,
        positionY: 300,
        sequenceNo: 1,
      },
      {
        id: "4",
        causeText: "Buku ajar kurang relevan",
        boneCategory: "MATERIAL",
        positionX: 200,
        positionY: 400,
        sequenceNo: 1,
      },
      {
        id: "5",
        causeText: "Lingkungan kelas kurang kondusif",
        boneCategory: "ENVIRONMENT",
        positionX: 200,
        positionY: 500,
        sequenceNo: 1,
      },
    ]);
  };

  const loadAnalytics = async () => {
    if (!currentDiagram) return;
    // Simulate loading analytics
    setAnalytics({
      diagram_id: currentDiagram.id,
      total_nodes: nodes.length,
      total_edges: nodes.length,
      category_stats: categories.map((cat) => ({
        category: cat.category_name,
        node_count: nodes.filter((n) => n.boneCategory === cat.category_id).length,
      })),
      depth_analysis: [
        { depth: 0, count: 1 },
        { depth: 1, count: nodes.length },
      ],
      created_at: currentDiagram.createdAt,
      updated_at: currentDiagram.updatedAt,
    });
  };

  const validateDiagram = async () => {
    if (!currentDiagram) return;
    // Simulate validation
    setValidation({
      diagram_id: currentDiagram.id,
      is_valid: nodes.length > 0,
      issues: nodes.length === 0 ? ["Diagram tidak memiliki node"] : [],
      warnings: [],
      suggestions: nodes.length < 5 ? ["Tambahkan lebih banyak node untuk analisis yang lebih komprehensif"] : [],
    });
  };

  const handleAddDiagram = () => {
    setEditingDiagram(null);
    setNewDiagram({});
    setOpenDialog(true);
  };

  const handleEditDiagram = (diagram: FishboneDiagram) => {
    setEditingDiagram(diagram);
    setNewDiagram({ ...diagram });
    setOpenDialog(true);
  };

  const handleSaveDiagram = () => {
    if (!newDiagram.headEffect) {
      setSnackbar({
        open: true,
        message: "Head effect harus diisi",
        severity: "error",
      });
      return;
    }

    if (editingDiagram) {
      setDiagrams(
        diagrams.map((d) => (d.id === editingDiagram.id ? { ...d, ...newDiagram } : d))
      );
      setSnackbar({
        open: true,
        message: "Diagram berhasil diperbarui",
        severity: "success",
      });
    } else {
      const newDiagramWithId: FishboneDiagram = {
        id: Date.now().toString(),
        headEffect: newDiagram.headEffect!,
        description: newDiagram.description || "",
        schoolId: "school-1",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      setDiagrams([...diagrams, newDiagramWithId]);
      setSnackbar({
        open: true,
        message: "Diagram berhasil ditambahkan",
        severity: "success",
      });
    }

    setOpenDialog(false);
    setEditingDiagram(null);
    setNewDiagram({});
  };

  const handleAddNode = () => {
    setEditingNode(null);
    setNewNode({
      boneCategory: "MAN",
      positionX: 200,
      positionY: 100,
      sequenceNo: nodes.length + 1,
    });
    setOpenNodeDialog(true);
  };

  const handleEditNode = (node: FishboneNode) => {
    setEditingNode(node);
    setNewNode({ ...node });
    setOpenNodeDialog(true);
  };

  const handleSaveNode = () => {
    if (!newNode.causeText) {
      setSnackbar({
        open: true,
        message: "Cause text harus diisi",
        severity: "error",
      });
      return;
    }

    if (editingNode) {
      setNodes(nodes.map((n) => (n.id === editingNode.id ? { ...n, ...newNode } : n)));
      setSnackbar({
        open: true,
        message: "Node berhasil diperbarui",
        severity: "success",
      });
    } else {
      const newNodeWithId: FishboneNode = {
        id: Date.now().toString(),
        causeText: newNode.causeText!,
        boneCategory: newNode.boneCategory!,
        positionX: newNode.positionX || 200,
        positionY: newNode.positionY || 100,
        sequenceNo: newNode.sequenceNo || nodes.length + 1,
      };
      setNodes([...nodes, newNodeWithId]);
      setSnackbar({
        open: true,
        message: "Node berhasil ditambahkan",
        severity: "success",
      });
    }

    setOpenNodeDialog(false);
    setEditingNode(null);
    setNewNode({});
  };

  const handleDeleteNode = (nodeId: string) => {
    setNodes(nodes.filter((n) => n.id !== nodeId));
    setSnackbar({
      open: true,
      message: "Node berhasil dihapus",
      severity: "success",
    });
  };

  const handleZoomIn = () => {
    setZoom(Math.min(zoom + 0.1, 2));
  };

  const handleZoomOut = () => {
    setZoom(Math.max(zoom - 0.1, 0.5));
  };

  const handleResetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  const handleCanvasMouseDown = (e: React.MouseEvent) => {
    if (e.button === 1 || (e.button === 0 && e.altKey)) {
      setIsPanning(true);
      setPanStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleCanvasMouseMove = (e: React.MouseEvent) => {
    if (isPanning) {
      setPan({
        x: e.clientX - panStart.x,
        y: e.clientY - panStart.y,
      });
    }
  };

  const handleCanvasMouseUp = () => {
    setIsPanning(false);
  };

  const handleExport = async (format: "json" | "csv") => {
    if (!currentDiagram) return;

    try {
      const exportData = {
        diagram: currentDiagram,
        nodes: nodes,
        categories: categories,
        exported_at: new Date().toISOString(),
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `fishbone_diagram_${currentDiagram.id}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setSnackbar({
        open: true,
        message: `Diagram fishbone berhasil diekspor sebagai ${format.toUpperCase()}`,
        severity: "success",
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Gagal mengekspor diagram fishbone",
        severity: "error",
      });
    }

    setExportMenuAnchor(null);
  };

  const handleApplyTemplate = (template: FishboneTemplate) => {
    setSelectedTemplate(template);

    if (!currentDiagram) {
      // Create new diagram from template
      const newDiagram: FishboneDiagram = {
        id: Date.now().toString(),
        headEffect: template.head_effect,
        description: template.template_description,
        schoolId: "school-1",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      setCurrentDiagram(newDiagram);
    } else {
      // Update existing diagram with template data
      const updatedDiagram = {
        ...currentDiagram,
        headEffect: template.head_effect,
      };
      setCurrentDiagram(updatedDiagram);
    }

    // Convert preset nodes to fishbone nodes
    const templateNodes: FishboneNode[] = template.preset_nodes.map((presetNode, index) => ({
      id: `template-${Date.now()}-${index}`,
      causeText: presetNode.cause_text,
      boneCategory: presetNode.bone_category,
      positionX: presetNode.position_x,
      positionY: presetNode.position_y,
      sequenceNo: presetNode.sequence_no,
    }));

    setNodes(templateNodes);

    setOpenTemplateDialog(false);
    setSnackbar({
      open: true,
      message: `Template "${template.template_name}" berhasil diterapkan`,
      severity: "success",
    });
  };

  const getCategoryColor = (categoryId: string) => {
    const category = categories.find((c) => c.category_id === categoryId);
    return category?.color || "#9E9E9E";
  };

  const renderCanvas = () => {
    if (!currentDiagram) return null;

    return (
      <Paper
        ref={canvasRef}
        elevation={2}
        sx={{
          height: 600,
          position: "relative",
          overflow: "hidden",
          cursor: isPanning ? "grabbing" : "grab",
          backgroundColor: "#f5f5f5",
        }}
        onMouseDown={handleCanvasMouseDown}
        onMouseMove={handleCanvasMouseMove}
        onMouseUp={handleCanvasMouseUp}
        onMouseLeave={handleCanvasMouseUp}
      >
        <Box
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            transformOrigin: "0 0",
          }}
        >
          {/* Main spine */}
          <Box
            sx={{
              position: "absolute",
              left: 100,
              top: 50,
              width: 600,
              height: 4,
              backgroundColor: "#333",
            }}
          />

          {/* Head effect */}
          <Box
            sx={{
              position: "absolute",
              left: 650,
              top: 30,
              padding: 2,
              backgroundColor: "#FF5722",
              color: "white",
              borderRadius: 1,
              fontWeight: "bold",
              minWidth: 200,
              textAlign: "center",
            }}
          >
            <Typography variant="h6">{currentDiagram.headEffect}</Typography>
          </Box>

          {/* Category bones */}
          {categories.map((category, index) => {
            const categoryNodes = nodes.filter((n) => n.boneCategory === category.category_id);
            const yOffset = 100 + index * 100;

            return (
              <React.Fragment key={category.category_id}>
                {/* Bone line */}
                <Box
                  sx={{
                    position: "absolute",
                    left: 100,
                    top: yOffset,
                    width: 400,
                    height: 2,
                    backgroundColor: category.color,
                  }}
                />

                {/* Category label */}
                <Chip
                  label={category.category_name}
                  sx={{
                    position: "absolute",
                    left: 20,
                    top: yOffset - 12,
                    backgroundColor: category.color,
                    color: "white",
                    fontWeight: "bold",
                  }}
                />

                {/* Nodes */}
                {categoryNodes.map((node, nodeIndex) => (
                  <Box
                    key={node.id}
                    sx={{
                      position: "absolute",
                      left: 150 + nodeIndex * 80,
                      top: yOffset - 20,
                      padding: 1,
                      backgroundColor: "white",
                      border: `2px solid ${category.color}`,
                      borderRadius: 1,
                      minWidth: 150,
                      cursor: "pointer",
                      "&:hover": {
                        boxShadow: 3,
                      },
                    }}
                    onClick={() => handleEditNode(node)}
                  >
                    <Typography variant="body2" noWrap>
                      {node.causeText}
                    </Typography>
                  </Box>
                ))}
              </React.Fragment>
            );
          })}
        </Box>

        {/* Zoom controls */}
        <Box
          sx={{
            position: "absolute",
            bottom: 16,
            right: 16,
            display: "flex",
            gap: 1,
          }}
        >
          <Tooltip title="Zoom In">
            <IconButton size="small" onClick={handleZoomIn}>
              <ZoomInIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Zoom Out">
            <IconButton size="small" onClick={handleZoomOut}>
              <ZoomOutIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Reset View">
            <IconButton size="small" onClick={handleResetView}>
              <CenterIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Pan (Alt + Drag)">
            <IconButton size="small">
              <PanIcon />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Validation indicator */}
        {validation && (
          <Box
            sx={{
              position: "absolute",
              top: 16,
              right: 16,
            }}
          >
            {validation.is_valid ? (
              <Chip
                icon={<VerifiedIcon />}
                label="Valid"
                color="success"
                variant="outlined"
              />
            ) : (
              <Chip
                icon={<WarningIcon />}
                label="Invalid"
                color="error"
                variant="outlined"
              />
            )}
          </Box>
        )}
      </Paper>
    );
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ mt: 4, mb: 4 }}>
        <AppBar position="static" color="default" elevation={0} sx={{ mb: 3 }}>
          <Toolbar>
            <Typography variant="h5" component="h1" sx={{ flexGrow: 1 }}>
              Diagram Fishbone
            </Typography>
            <Box sx={{ display: "flex", gap: 1 }}>
              <Button
                variant="outlined"
                startIcon={<TemplateIcon />}
                onClick={() => {
                  setCurrentDiagram(null);
                  setOpenTemplateDialog(true);
                }}
              >
                Buat dari Template
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddDiagram}
              >
                Buat Diagram Baru
              </Button>
            </Box>
          </Toolbar>
        </AppBar>

        {!currentDiagram ? (
          <Box>
            <Typography variant="h6" gutterBottom>
              Daftar Diagram Fishbone
            </Typography>
            <Grid container spacing={3}>
              {diagrams.map((diagram) => (
                <Grid item xs={12} md={6} lg={4} key={diagram.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {diagram.headEffect}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {diagram.description}
                      </Typography>
                      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(diagram.updatedAt).toLocaleDateString("id-ID")}
                        </Typography>
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => setCurrentDiagram(diagram)}
                        >
                          Buka
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        ) : (
          <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
              <Box>
                <Typography variant="h6">{currentDiagram.headEffect}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {currentDiagram.description}
                </Typography>
              </Box>
              <Box sx={{ display: "flex", gap: 1 }}>
                <Button
                  variant="outlined"
                  startIcon={<TemplateIcon />}
                  onClick={() => setOpenTemplateDialog(true)}
                >
                  Template
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<AnalyticsIcon />}
                  onClick={() => setOpenAnalytics(true)}
                >
                  Analitik
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<VerifiedIcon />}
                  onClick={() => setOpenValidation(true)}
                >
                  Validasi
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={(e) => setExportMenuAnchor(e.currentTarget)}
                >
                  Ekspor
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<AddIcon />}
                  onClick={handleAddNode}
                >
                  Tambah Node
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setCurrentDiagram(null)}
                >
                  Kembali
                </Button>
              </Box>
            </Box>

            {renderCanvas()}

            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Node ({nodes.length})
              </Typography>
              <Grid container spacing={2}>
                {nodes.map((node) => (
                  <Grid item xs={12} md={6} lg={4} key={node.id}>
                    <Card
                      sx={{
                        borderLeft: `4px solid ${getCategoryColor(node.boneCategory)}`,
                      }}
                    >
                      <CardContent>
                        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                          <Box sx={{ flex: 1 }}>
                            <Chip
                              label={node.boneCategory}
                              size="small"
                              sx={{
                                backgroundColor: getCategoryColor(node.boneCategory),
                                color: "white",
                                mb: 1,
                              }}
                            />
                            <Typography variant="body1">{node.causeText}</Typography>
                          </Box>
                          <Box>
                            <IconButton size="small" onClick={() => handleEditNode(node)}>
                              <EditIcon fontSize="small" />
                            </IconButton>
                            <IconButton size="small" onClick={() => handleDeleteNode(node.id)}>
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Box>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Box>
        )}

        <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>{editingDiagram ? "Edit Diagram" : "Buat Diagram Baru"}</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              label="Head Effect"
              multiline
              rows={2}
              value={newDiagram.headEffect || ""}
              onChange={(e) => setNewDiagram({ ...newDiagram, headEffect: e.target.value })}
              sx={{ mt: 2, mb: 2 }}
            />

            <TextField
              fullWidth
              label="Deskripsi"
              multiline
              rows={3}
              value={newDiagram.description || ""}
              onChange={(e) => setNewDiagram({ ...newDiagram, description: e.target.value })}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Batal</Button>
            <Button onClick={handleSaveDiagram} variant="contained" startIcon={<SaveIcon />}>
              Simpan
            </Button>
          </DialogActions>
        </Dialog>

        <Dialog open={openNodeDialog} onClose={() => setOpenNodeDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>{editingNode ? "Edit Node" : "Tambah Node"}</DialogTitle>
          <DialogContent>
            <FormControl fullWidth sx={{ mt: 2, mb: 2 }}>
              <InputLabel>Kategori</InputLabel>
              <Select
                value={newNode.boneCategory || "MAN"}
                onChange={(e) => setNewNode({ ...newNode, boneCategory: e.target.value })}
                label="Kategori"
              >
                {categories.map((cat) => (
                  <MenuItem key={cat.category_id} value={cat.category_id}>
                    {cat.category_name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Cause Text"
              multiline
              rows={2}
              value={newNode.causeText || ""}
              onChange={(e) => setNewNode({ ...newNode, causeText: e.target.value })}
              sx={{ mb: 2 }}
            />

            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Position X"
                  type="number"
                  value={newNode.positionX || 200}
                  onChange={(e) => setNewNode({ ...newNode, positionX: Number(e.target.value) })}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Position Y"
                  type="number"
                  value={newNode.positionY || 100}
                  onChange={(e) => setNewNode({ ...newNode, positionY: Number(e.target.value) })}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenNodeDialog(false)}>Batal</Button>
            <Button onClick={handleSaveNode} variant="contained" startIcon={<SaveIcon />}>
              Simpan
            </Button>
          </DialogActions>
        </Dialog>

        <Dialog open={openAnalytics} onClose={() => setOpenAnalytics(false)} maxWidth="md" fullWidth>
          <DialogTitle>Analitik Diagram</DialogTitle>
          <DialogContent>
            {analytics && (
              <Box sx={{ mt: 2 }}>
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h3">{analytics.total_nodes}</Typography>
                        <Typography variant="body2">Total Nodes</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h3">{analytics.total_edges}</Typography>
                        <Typography variant="body2">Total Edges</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>

                <Typography variant="h6" gutterBottom>
                  Breakdown Kategori
                </Typography>
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, mb: 3 }}>
                  {analytics.category_stats.map((stat) => (
                    <Chip
                      key={stat.category}
                      label={`${stat.category}: ${stat.node_count}`}
                      variant="outlined"
                    />
                  ))}
                </Box>

                <Typography variant="h6" gutterBottom>
                  Analisis Depth
                </Typography>
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                  {analytics.depth_analysis.map((stat) => (
                    <Chip
                      key={stat.depth}
                      label={`Depth ${stat.depth}: ${stat.count}`}
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Box>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenAnalytics(false)}>Tutup</Button>
          </DialogActions>
        </Dialog>

        <Dialog open={openValidation} onClose={() => setOpenValidation(false)} maxWidth="md" fullWidth>
          <DialogTitle>Validasi Diagram</DialogTitle>
          <DialogContent>
            {validation && (
              <Box sx={{ mt: 2 }}>
                <Alert severity={validation.is_valid ? "success" : "error"} sx={{ mb: 2 }}>
                  {validation.is_valid ? "Diagram valid" : "Diagram tidak valid"}
                </Alert>

                {validation.issues.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="h6" color="error">
                      Issues:
                    </Typography>
                    <List>
                      {validation.issues.map((issue, index) => (
                        <ListItem key={index}>
                          <MuiListItemText primary={issue} />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}

                {validation.warnings.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="h6" color="warning">
                      Warnings:
                    </Typography>
                    <List>
                      {validation.warnings.map((warning, index) => (
                        <ListItem key={index}>
                          <MuiListItemText primary={warning} />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}

                {validation.suggestions.length > 0 && (
                  <Box>
                    <Typography variant="h6" color="info">
                      Suggestions:
                    </Typography>
                    <List>
                      {validation.suggestions.map((suggestion, index) => (
                        <ListItem key={index}>
                          <MuiListItemText primary={suggestion} />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
              </Box>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenValidation(false)}>Tutup</Button>
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

        <Dialog open={openTemplateDialog} onClose={() => setOpenTemplateDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <TemplateIcon color="primary" />
              <Typography variant="h6">Pilih Template Fishbone</Typography>
            </Box>
          </DialogTitle>
          <DialogContent>
            <Alert severity="info" sx={{ mb: 2 }}>
              Pilih template untuk memulai diagram fishbone dengan struktur yang sudah disiapkan
            </Alert>
            <Grid container spacing={2}>
              {templates.map((template) => (
                <Grid item xs={12} md={6} key={template.id}>
                  <Card
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
                        Head Effect: {template.head_effect}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="caption" color="text.secondary">
                          {template.preset_nodes.length} preset nodes
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenTemplateDialog(false)}>Batal</Button>
            <Button
              variant="contained"
              onClick={() => selectedTemplate && handleApplyTemplate(selectedTemplate)}
              disabled={!selectedTemplate}
              startIcon={<AutoFixIcon />}
            >
              Terapkan Template
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

export default FishbonePage;