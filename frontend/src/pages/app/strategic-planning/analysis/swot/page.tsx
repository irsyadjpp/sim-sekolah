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
  Divider,
  Tabs,
  Tab,
  Alert,
  Snackbar,
  Menu,
  ListItemText,
  ListItemIcon,
  AppBar,
  Toolbar,
  Tooltip,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  DragIndicator as DragIcon,
  Download as DownloadIcon,
  Analytics as AnalyticsIcon,
  Link as LinkIcon,
  Save as SaveIcon,
  Close as CloseIcon,
  Visibility as ViewIcon,
} from "@mui/icons-material";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

interface SWOTItem {
  id: string;
  title: string;
  description: string;
  quadrant: "STRENGTHS" | "WEAKNESSES" | "OPPORTUNITIES" | "THREATS";
  category?: string;
  priority: string;
  notes?: string;
  dataMapping?: {
    sourceType: string;
    sourceId: string;
    sourceField: string;
    confidence: number;
  };
}

interface SWOTSession {
  id: string;
  title: string;
  description: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

interface SWOTAnalytics {
  session_id: string;
  total_items: {
    strengths: number;
    weaknesses: number;
    opportunities: number;
    threats: number;
  };
  data_mapping_count: {
    strengths: number;
    weaknesses: number;
    opportunities: number;
    threats: number;
  };
  category_breakdown: Array<{ category: string; count: number }>;
  data_source_breakdown: Array<{ source_type: string; count: number }>;
  created_at: string;
  updated_at: string;
}

const SWOTPage: React.FC = () => {
  const [sessions, setSessions] = useState<SWOTSession[]>([]);
  const [currentSession, setCurrentSession] = useState<SWOTSession | null>(null);
  const [items, setItems] = useState<SWOTItem[]>([]);
  const [analytics, setAnalytics] = useState<SWOTAnalytics | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [openAnalytics, setOpenAnalytics] = useState(false);
  const [openDataMapping, setOpenDataMapping] = useState(false);
  const [editingItem, setEditingItem] = useState<SWOTItem | null>(null);
  const [newItem, setNewItem] = useState<Partial<SWOTItem>>({
    quadrant: "STRENGTHS",
    priority: "MEDIUM",
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });
  const [exportMenuAnchor, setExportMenuAnchor] = useState<null | HTMLElement>(null);

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (currentSession) {
      loadSessionItems();
      loadAnalytics();
    }
  }, [currentSession]);

  const loadSessions = async () => {
    // Simulate loading sessions
    setSessions([
      {
        id: "1",
        title: "Analisis SWOT Semester 1",
        description: "Analisis SWOT untuk semester ganjil 2025/2026",
        schoolId: "school-1",
        createdAt: "2025-01-15T10:00:00Z",
        updatedAt: "2025-01-20T14:30:00Z",
      },
    ]);
  };

  const loadSessionItems = async () => {
    // Simulate loading items
    setItems([
      {
        id: "1",
        title: "Guru Berkompeten",
        description: "Guru memiliki sertifikasi dan pengalaman yang memadai",
        quadrant: "STRENGTHS",
        category: "SDM",
        priority: "HIGH",
      },
      {
        id: "2",
        title: "Fasilitas Terbatas",
        description: "Keterbatasan sarana prasarana laboratorium",
        quadrant: "WEAKNESSES",
        category: "INFRASTRUKTUR",
        priority: "HIGH",
      },
      {
        id: "3",
        title: "Dana BOS",
        description: "Ketersediaan dana BOS untuk pengembangan",
        quadrant: "OPPORTUNITIES",
        category: "KEUANGAN",
        priority: "MEDIUM",
      },
      {
        id: "4",
        title: "Perubahan Kurikulum",
        description: "Adaptasi terhadap perubahan kurikulum nasional",
        quadrant: "THREATS",
        category: "KEBIJAKAN",
        priority: "HIGH",
      },
    ]);
  };

  const loadAnalytics = async () => {
    if (!currentSession) return;
    // Simulate loading analytics
    setAnalytics({
      session_id: currentSession.id,
      total_items: {
        strengths: 1,
        weaknesses: 1,
        opportunities: 1,
        threats: 1,
      },
      data_mapping_count: {
        strengths: 0,
        weaknesses: 0,
        opportunities: 0,
        threats: 0,
      },
      category_breakdown: [
        { category: "SDM", count: 1 },
        { category: "INFRASTRUKTUR", count: 1 },
        { category: "KEUANGAN", count: 1 },
        { category: "KEBIJAKAN", count: 1 },
      ],
      data_source_breakdown: [],
      created_at: currentSession.createdAt,
      updated_at: currentSession.updatedAt,
    });
  };

  const handleDragEnd = (result: any) => {
    if (!result.destination) return;

    const itemsCopy = [...items];
    const [reorderedItem] = itemsCopy.splice(result.source.index, 1);
    itemsCopy.splice(result.destination.index, 0, reorderedItem);
    setItems(itemsCopy);
  };

  const handleAddItem = () => {
    setEditingItem(null);
    setNewItem({
      quadrant: "STRENGTHS",
      priority: "MEDIUM",
    });
    setOpenDialog(true);
  };

  const handleEditItem = (item: SWOTItem) => {
    setEditingItem(item);
    setNewItem({ ...item });
    setOpenDialog(true);
  };

  const handleSaveItem = () => {
    if (!newItem.title || !newItem.description) {
      setSnackbar({
        open: true,
        message: "Judul dan deskripsi harus diisi",
        severity: "error",
      });
      return;
    }

    if (editingItem) {
      setItems(items.map((item) => (item.id === editingItem.id ? { ...item, ...newItem } : item)));
      setSnackbar({
        open: true,
        message: "Item berhasil diperbarui",
        severity: "success",
      });
    } else {
      const newItemWithId: SWOTItem = {
        id: Date.now().toString(),
        title: newItem.title!,
        description: newItem.description!,
        quadrant: newItem.quadrant!,
        priority: newItem.priority!,
        category: newItem.category,
        notes: newItem.notes,
      };
      setItems([...items, newItemWithId]);
      setSnackbar({
        open: true,
        message: "Item berhasil ditambahkan",
        severity: "success",
      });
    }

    setOpenDialog(false);
    setEditingItem(null);
    setNewItem({});
  };

  const handleDeleteItem = (itemId: string) => {
    setItems(items.filter((item) => item.id !== itemId));
    setSnackbar({
      open: true,
      message: "Item berhasil dihapus",
      severity: "success",
    });
  };

  const handleExport = async (format: "json" | "csv") => {
    if (!currentSession) return;

    try {
      // Simulate export API call
      const exportData = {
        session: currentSession,
        items: items,
        exported_at: new Date().toISOString(),
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `swot_analysis_${currentSession.id}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setSnackbar({
        open: true,
        message: `Analisis SWOT berhasil diekspor sebagai ${format.toUpperCase()}`,
        severity: "success",
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Gagal mengekspor analisis SWOT",
        severity: "error",
      });
    }

    setExportMenuAnchor(null);
  };

  const getQuadrantColor = (quadrant: string) => {
    switch (quadrant) {
      case "STRENGTHS":
        return "#4CAF50";
      case "WEAKNESSES":
        return "#F44336";
      case "OPPORTUNITIES":
        return "#2196F3";
      case "THREATS":
        return "#FF9800";
      default:
        return "#9E9E9E";
    }
  };

  const getQuadrantLabel = (quadrant: string) => {
    switch (quadrant) {
      case "STRENGTHS":
        return "Strengths (Kekuatan)";
      case "WEAKNESSES":
        return "Weaknesses (Kelemahan)";
      case "OPPORTUNITIES":
        return "Opportunities (Peluang)";
      case "THREATS":
        return "Threats (Ancaman)";
      default:
        return quadrant;
    }
  };

  const renderQuadrant = (quadrant: "STRENGTHS" | "WEAKNESSES" | "OPPORTUNITIES" | "THREATS") => {
    const quadrantItems = items.filter((item) => item.quadrant === quadrant);

    return (
      <Paper
        elevation={2}
        sx={{
          p: 2,
          height: "100%",
          minHeight: 400,
          backgroundColor: `${getQuadrantColor(quadrant)}10`,
          border: `2px solid ${getQuadrantColor(quadrant)}`,
        }}
      >
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
          <Typography variant="h6" sx={{ color: getQuadrantColor(quadrant), fontWeight: "bold" }}>
            {getQuadrantLabel(quadrant)}
          </Typography>
          <Chip label={quadrantItems.length} size="small" sx={{ backgroundColor: getQuadrantColor(quadrant), color: "white" }} />
        </Box>

        <Droppable droppableId={quadrant}>
          {(provided) => (
            <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ minHeight: 300 }}>
              {quadrantItems.map((item, index) => (
                <Draggable key={item.id} draggableId={item.id} index={index}>
                  {(provided) => (
                    <Card
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      sx={{ mb: 2, cursor: "move" }}
                      elevation={1}
                    >
                      <CardContent>
                        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                          <Box sx={{ flex: 1 }}>
                            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                              <IconButton {...provided.dragHandleProps} size="small" sx={{ mr: 1, cursor: "grab" }}>
                                <DragIcon fontSize="small" />
                              </IconButton>
                              <Typography variant="subtitle1" fontWeight="bold">
                                {item.title}
                              </Typography>
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                              {item.description}
                            </Typography>
                            {item.category && (
                              <Chip label={item.category} size="small" sx={{ mt: 1, mr: 1 }} />
                            )}
                            <Chip label={item.priority} size="small" sx={{ mt: 1 }} />
                            {item.dataMapping && (
                              <Tooltip title="Data mapping tersedia">
                                <LinkIcon fontSize="small" sx={{ ml: 1, verticalAlign: "middle", color: "primary.main" }} />
                              </Tooltip>
                            )}
                          </Box>
                          <Box>
                            <IconButton size="small" onClick={() => handleEditItem(item)}>
                              <EditIcon fontSize="small" />
                            </IconButton>
                            <IconButton size="small" onClick={() => handleDeleteItem(item.id)}>
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Box>
                        </Box>
                      </CardContent>
                    </Card>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </Box>
          )}
        </Droppable>

        <Button
          fullWidth
          variant="outlined"
          startIcon={<AddIcon />}
          onClick={() => {
            setNewItem({ ...newItem, quadrant });
            handleAddItem();
          }}
          sx={{ mt: 2 }}
        >
          Tambah Item
        </Button>
      </Paper>
    );
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ mt: 4, mb: 4 }}>
        <AppBar position="static" color="default" elevation={0} sx={{ mb: 3 }}>
          <Toolbar>
            <Typography variant="h5" component="h1" sx={{ flexGrow: 1 }}>
              Analisis SWOT
            </Typography>
            <Box sx={{ display: "flex", gap: 1 }}>
              <Button
                variant="contained"
                startIcon={<AnalyticsIcon />}
                onClick={() => setOpenAnalytics(true)}
                disabled={!currentSession}
              >
                Analitik
              </Button>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                onClick={(e) => setExportMenuAnchor(e.currentTarget)}
                disabled={!currentSession}
              >
                Ekspor
              </Button>
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
            </Box>
          </Toolbar>
        </AppBar>

        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
          <Tab label="Sesi Analisis" />
          <Tab label="Canvas SWOT" disabled={!currentSession} />
        </Tabs>

        {activeTab === 0 && (
          <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
              <Typography variant="h6">Sesi Analisis SWOT</Typography>
              <Button variant="contained" startIcon={<AddIcon />} onClick={() => { }}>
                Buat Sesi Baru
              </Button>
            </Box>

            <Grid container spacing={2}>
              {sessions.map((session) => (
                <Grid item xs={12} md={6} lg={4} key={session.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {session.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {session.description}
                      </Typography>
                      <Box sx={{ mt: 2, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(session.updatedAt).toLocaleDateString("id-ID")}
                        </Typography>
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => setCurrentSession(session)}
                          startIcon={<ViewIcon />}
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
        )}

        {activeTab === 1 && currentSession && (
          <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
              <Typography variant="h6">{currentSession.title}</Typography>
              <Typography variant="body2" color="text.secondary">
                {currentSession.description}
              </Typography>
            </Box>

            <DragDropContext onDragEnd={handleDragEnd}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  {renderQuadrant("STRENGTHS")}
                </Grid>
                <Grid item xs={12} md={6}>
                  {renderQuadrant("WEAKNESSES")}
                </Grid>
                <Grid item xs={12} md={6}>
                  {renderQuadrant("OPPORTUNITIES")}
                </Grid>
                <Grid item xs={12} md={6}>
                  {renderQuadrant("THREATS")}
                </Grid>
              </Grid>
            </DragDropContext>
          </Box>
        )}

        <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>{editingItem ? "Edit Item SWOT" : "Tambah Item SWOT"}</DialogTitle>
          <DialogContent>
            <FormControl fullWidth sx={{ mt: 2, mb: 2 }}>
              <InputLabel>Kuadran</InputLabel>
              <Select
                value={newItem.quadrant || "STRENGTHS"}
                onChange={(e) => setNewItem({ ...newItem, quadrant: e.target.value as any })}
                label="Kuadran"
              >
                <MenuItem value="STRENGTHS">Strengths (Kekuatan)</MenuItem>
                <MenuItem value="WEAKNESSES">Weaknesses (Kelemahan)</MenuItem>
                <MenuItem value="OPPORTUNITIES">Opportunities (Peluang)</MenuItem>
                <MenuItem value="THREATS">Threats (Ancaman)</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Judul"
              value={newItem.title || ""}
              onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Deskripsi"
              multiline
              rows={4}
              value={newItem.description || ""}
              onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Kategori"
              value={newItem.category || ""}
              onChange={(e) => setNewItem({ ...newItem, category: e.target.value })}
              sx={{ mb: 2 }}
            />

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Prioritas</InputLabel>
              <Select
                value={newItem.priority || "MEDIUM"}
                onChange={(e) => setNewItem({ ...newItem, priority: e.target.value })}
                label="Prioritas"
              >
                <MenuItem value="HIGH">High</MenuItem>
                <MenuItem value="MEDIUM">Medium</MenuItem>
                <MenuItem value="LOW">Low</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Catatan"
              multiline
              rows={2}
              value={newItem.notes || ""}
              onChange={(e) => setNewItem({ ...newItem, notes: e.target.value })}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Batal</Button>
            <Button onClick={handleSaveItem} variant="contained" startIcon={<SaveIcon />}>
              Simpan
            </Button>
          </DialogActions>
        </Dialog>

        <Dialog open={openAnalytics} onClose={() => setOpenAnalytics(false)} maxWidth="md" fullWidth>
          <DialogTitle>Analitik SWOT</DialogTitle>
          <DialogContent>
            {analytics && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Total Item per Kuadran
                </Typography>
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={6} md={3}>
                    <Card sx={{ backgroundColor: "#4CAF50", color: "white" }}>
                      <CardContent>
                        <Typography variant="h3">{analytics.total_items.strengths}</Typography>
                        <Typography variant="body2">Strengths</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Card sx={{ backgroundColor: "#F44336", color: "white" }}>
                      <CardContent>
                        <Typography variant="h3">{analytics.total_items.weaknesses}</Typography>
                        <Typography variant="body2">Weaknesses</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Card sx={{ backgroundColor: "#2196F3", color: "white" }}>
                      <CardContent>
                        <Typography variant="h3">{analytics.total_items.opportunities}</Typography>
                        <Typography variant="body2">Opportunities</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Card sx={{ backgroundColor: "#FF9800", color: "white" }}>
                      <CardContent>
                        <Typography variant="h3">{analytics.total_items.threats}</Typography>
                        <Typography variant="body2">Threats</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>

                <Typography variant="h6" gutterBottom>
                  Breakdown Kategori
                </Typography>
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                  {analytics.category_breakdown.map((cat) => (
                    <Chip key={cat.category} label={`${cat.category}: ${cat.count}`} variant="outlined" />
                  ))}
                </Box>
              </Box>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenAnalytics(false)}>Tutup</Button>
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

export default SWOTPage;