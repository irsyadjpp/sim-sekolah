"use client";

import { useEffect, useState } from "react";

import {
  Cancel as CancelIcon,
  CheckCircle as CheckIcon,
  CloudUpload as UploadIcon,
  Description as DescriptionIcon,
  Download as DownloadIcon,
  FilterList as FilterIcon,
  Folder as FolderIcon,
  History as HistoryIcon,
  Pending as PendingIcon,
  Refresh as RefreshIcon,
  Search as SearchIcon,
  Share as ShareIcon,
  Visibility as ViewIcon,
} from "@mui/icons-material";
import {
  Alert,
  AlertTitle,
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Paper,
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
  Tooltip,
  Typography,
} from "@mui/material";

interface Document {
  id: string;
  title: string;
  description: string;
  document_number: string;
  category: string;
  document_type: string;
  status: string;
  access_level: string;
  file_name: string;
  file_size: number;
  author_name: string;
  version: number;
  download_count: number;
  view_count: number;
  created_at: string;
  is_confidential: boolean;
}

interface DocumentStatistics {
  total_documents: number;
  by_category: Record<string, number>;
  by_status: Record<string, number>;
  total_downloads: number;
  total_views: number;
  recent_uploads: number;
  pending_approvals: number;
  storage_used: number;
  storage_used_formatted: string;
}

interface DocumentCategory {
  id: string;
  name: string;
  description: string;
  color: string;
  icon: string;
  document_count: number;
}

export default function DocumentRepositoryPage() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [statistics, setStatistics] = useState<DocumentStatistics | null>(null);
  const [categories, setCategories] = useState<DocumentCategory[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/documents");
      const data = await response.json();
      if (data.success) {
        setDocuments(data.data);
      }
    } catch (err) {
      setError("Failed to fetch documents");
      console.error("Error fetching documents:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await fetch("/api/documents/statistics");
      const data = await response.json();
      if (data.success) {
        setStatistics(data.data);
      }
    } catch (err) {
      console.error("Error fetching statistics:", err);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch("/api/documents/categories");
      const data = await response.json();
      if (data.success) {
        setCategories(data.data);
      }
    } catch (err) {
      console.error("Error fetching categories:", err);
    }
  };

  useEffect(() => {
    fetchDocuments();
    fetchStatistics();
    fetchCategories();
  }, []);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleUploadClick = () => {
    setUploadDialogOpen(true);
  };

  const handleViewDocument = (document: Document) => {
    setSelectedDocument(document);
    setViewDialogOpen(true);
  };

  const handleDownload = async (document: Document) => {
    try {
      const response = await fetch(`/api/documents/${document.id}/download`);
      if (response.ok) {
        const data = await response.json();
        // In a real implementation, this would trigger file download
        console.log("Download initiated:", data);
      }
    } catch (err) {
      console.error("Error downloading document:", err);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "APPROVED":
      case "PUBLISHED":
        return "success";
      case "PENDING":
        return "warning";
      case "REJECTED":
        return "error";
      case "DRAFT":
        return "default";
      default:
        return "default";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "APPROVED":
      case "PUBLISHED":
        return <CheckIcon />;
      case "PENDING":
        return <PendingIcon />;
      case "REJECTED":
        return <CancelIcon />;
      default:
        return null;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
  };

  const filteredDocuments = documents.filter((doc) => {
    const matchesSearch =
      doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || doc.category === selectedCategory;
    const matchesStatus = !selectedStatus || doc.status === selectedStatus;
    return matchesSearch && matchesCategory && matchesStatus;
  });

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" fontWeight="bold">
          Repository Dokumen
        </Typography>
        <Box display="flex" gap={2}>
          <Button variant="outlined" startIcon={<RefreshIcon />} onClick={fetchDocuments}>
            Refresh
          </Button>
          <Button variant="contained" startIcon={<UploadIcon />} onClick={handleUploadClick}>
            Upload Dokumen
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <AlertTitle>Error</AlertTitle>
          {error}
        </Alert>
      )}

      <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Dokumen" />
        <Tab label="Statistik" />
        <Tab label="Kategori" />
      </Tabs>

      {activeTab === 0 && (
        <>
          {/* Statistics Cards */}
          {statistics && (
            <Grid container spacing={3} sx={{ mb: 3 }}>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Total Dokumen
                      </Typography>
                      <FolderIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.total_documents}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Total Download
                      </Typography>
                      <DownloadIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.total_downloads}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Pending Approval
                      </Typography>
                      <PendingIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.pending_approvals}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Storage Used
                      </Typography>
                      <DescriptionIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.storage_used_formatted}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}

          {/* Filters */}
          <Paper sx={{ p: 2, mb: 3 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <TextField
                  fullWidth
                  placeholder="Cari dokumen..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  InputProps={{
                    startAdornment: <SearchIcon sx={{ mr: 1, color: "text.secondary" }} />,
                  }}
                />
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <FormControl fullWidth>
                  <InputLabel>Kategori</InputLabel>
                  <Select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    label="Kategori"
                  >
                    <MenuItem value="">Semua</MenuItem>
                    {categories.map((cat) => (
                      <MenuItem key={cat.id} value={cat.name}>
                        {cat.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)} label="Status">
                    <MenuItem value="">Semua</MenuItem>
                    <MenuItem value="DRAFT">Draft</MenuItem>
                    <MenuItem value="PENDING">Pending</MenuItem>
                    <MenuItem value="APPROVED">Approved</MenuItem>
                    <MenuItem value="PUBLISHED">Published</MenuItem>
                    <MenuItem value="REJECTED">Rejected</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 2 }}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<FilterIcon />}
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedCategory("");
                    setSelectedStatus("");
                  }}
                >
                  Reset Filter
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {/* Documents Table */}
          <Paper>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Judul</TableCell>
                    <TableCell>Kategori</TableCell>
                    <TableCell>Tipe</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Ukuran</TableCell>
                    <TableCell>Penulis</TableCell>
                    <TableCell>Download/View</TableCell>
                    <TableCell>Aksi</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredDocuments.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={9} align="center">
                        <Typography variant="body2" color="text.secondary">
                          Tidak ada dokumen ditemukan
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredDocuments.map((doc) => (
                      <TableRow key={doc.id}>
                        <TableCell>
                          <Box>
                            <Typography variant="body2" fontWeight="medium">
                              {doc.title}
                            </Typography>
                            {doc.document_number && (
                              <Typography variant="caption" color="text.secondary">
                                {doc.document_number}
                              </Typography>
                            )}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip label={doc.category} size="small" color="default" />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{doc.document_type}</Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={doc.status}
                            size="small"
                            color={getStatusColor(doc.status) as any}
                            icon={getStatusIcon(doc.status)}
                          />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{formatFileSize(doc.file_size)}</Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{doc.author_name}</Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {doc.download_count} / {doc.view_count}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Box display="flex" gap={1}>
                            <Tooltip title="View">
                              <IconButton size="small" onClick={() => handleViewDocument(doc)}>
                                <ViewIcon />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Download">
                              <IconButton size="small" onClick={() => handleDownload(doc)}>
                                <DownloadIcon />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Share">
                              <IconButton size="small">
                                <ShareIcon />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="History">
                              <IconButton size="small">
                                <HistoryIcon />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </>
      )}

      {activeTab === 1 && statistics && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardHeader title="Dokumen per Kategori" />
              <CardContent>
                {Object.entries(statistics.by_category).map(([category, count]) => (
                  <Box key={category} display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2">{category}</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {count}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardHeader title="Dokumen per Status" />
              <CardContent>
                {Object.entries(statistics.by_status).map(([status, count]) => (
                  <Box key={status} display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2">{status}</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {count}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 2 && (
        <Grid container spacing={2}>
          {categories.map((category) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={category.id}>
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Box
                      sx={{
                        width: 40,
                        height: 40,
                        borderRadius: "50%",
                        backgroundColor: category.color,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <FolderIcon sx={{ color: "white" }} />
                    </Box>
                    <Box>
                      <Typography variant="h6" fontWeight="bold">
                        {category.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {category.document_count} dokumen
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Upload Dialog */}
      <Dialog open={uploadDialogOpen} onClose={() => setUploadDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Upload Dokumen Baru</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Grid container spacing={2}>
              <Grid size={{ xs: 12 }}>
                <TextField fullWidth label="Judul Dokumen" required />
              </Grid>
              <Grid size={{ xs: 12 }}>
                <TextField fullWidth label="Deskripsi" multiline rows={3} />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Kategori</InputLabel>
                  <Select label="Kategori" required>
                    {categories.map((cat) => (
                      <MenuItem key={cat.id} value={cat.name}>
                        {cat.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Tipe Dokumen</InputLabel>
                  <Select label="Tipe Dokumen" required>
                    <MenuItem value="PDF">PDF</MenuItem>
                    <MenuItem value="DOCX">Word Document</MenuItem>
                    <MenuItem value="XLSX">Excel</MenuItem>
                    <MenuItem value="PPTX">PowerPoint</MenuItem>
                    <MenuItem value="IMAGE">Gambar</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12 }}>
                <Button variant="outlined" component="label" startIcon={<UploadIcon />} fullWidth>
                  Pilih File
                  <input type="file" hidden accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg,.png" />
                </Button>
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Batal</Button>
          <Button variant="contained">Upload</Button>
        </DialogActions>
      </Dialog>

      {/* View Document Dialog */}
      <Dialog open={viewDialogOpen} onClose={() => setViewDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Detail Dokumen</DialogTitle>
        <DialogContent>
          {selectedDocument && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                {selectedDocument.title}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {selectedDocument.description}
              </Typography>
              <Grid container spacing={2} sx={{ mt: 2 }}>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Kategori:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedDocument.category}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Tipe:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedDocument.document_type}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Status:
                  </Typography>
                  <Chip
                    label={selectedDocument.status}
                    size="small"
                    color={getStatusColor(selectedDocument.status) as any}
                  />
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Versi:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedDocument.version}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Ukuran:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {formatFileSize(selectedDocument.file_size)}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Penulis:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedDocument.author_name}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialogOpen(false)}>Tutup</Button>
          <Button variant="contained" startIcon={<DownloadIcon />}>
            Download
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
