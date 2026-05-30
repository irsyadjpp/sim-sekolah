import { useState, useCallback } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Alert,
  CircularProgress,
  LinearProgress,
  Grid,
  Paper,
  Divider,
} from "@mui/material";
import {
  Upload as UploadIcon,
  CloudUpload,
  CheckCircle,
  Error,
  Warning,
  Description,
  Folder,
  Lock,
} from "@mui/icons-material";
import { documentApi, DOCUMENT_CATEGORIES, DOCUMENT_TYPES, ACCESS_LEVELS, validateFileForUpload, calculateFileHash } from "@/services/document-api";

interface DocumentUploadProps { }

export default function DocumentUpload({ }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");
  const [duplicateWarning, setDuplicateWarning] = useState<any>(null);

  // Form state
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    document_number: "",
    category: DOCUMENT_CATEGORIES.CURRICULUM,
    document_type: "",
    access_level: ACCESS_LEVELS.INTERNAL,
  });

  const [fileHash, setFileHash] = useState<string>("");
  const [checkingDuplicate, setCheckingDuplicate] = useState(false);

  // Handle file selection
  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    // Validate file
    const validation = validateFileForUpload(selectedFile, 100); // 100MB limit
    if (!validation.valid) {
      setError(validation.error || "Invalid file");
      return;
    }

    setError("");
    setFile(selectedFile);

    // Calculate file hash for duplicate detection
    try {
      const hash = await calculateFileHash(selectedFile);
      setFileHash(hash);

      // Auto-detect document type from MIME type
      const detectedType = documentApi.getDocumentTypeFromMimeType(selectedFile.type);
      setFormData(prev => ({
        ...prev,
        document_type: detectedType,
      }));

      // Check for duplicates
      await checkForDuplicates(hash, selectedFile.name);
    } catch (err) {
      console.error("Error calculating file hash:", err);
    }
  };

  // Check for duplicates
  const checkForDuplicates = async (hash: string, fileName: string) => {
    setCheckingDuplicate(true);
    setDuplicateWarning(null);

    try {
      const result = await documentApi.checkDuplicate({
        file_hash: hash,
        title: formData.title,
        document_number: formData.document_number,
      });

      if (result.isDuplicate && result.data) {
        setDuplicateWarning({
          message: `Duplicate document found: ${result.data.title}`,
          document: result.data,
        });
      }
    } catch (err) {
      console.error("Error checking duplicates:", err);
    } finally {
      setCheckingDuplicate(false);
    }
  };

  // Handle form input changes
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = event.target as HTMLInputElement;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));

    // Re-check duplicates when title or document number changes
    if ((name === "title" || name === "document_number") && fileHash) {
      checkForDuplicates(fileHash, file?.name || "");
    }
  };

  // Handle select changes
  const handleSelectChange = (name: string) => (event: unknown) => {
    const value = (event as React.ChangeEvent<{ value: unknown }>).target.value;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file");
      return;
    }

    if (!formData.title.trim()) {
      setError("Document title is required");
      return;
    }

    setError("");
    setSuccess("");
    setUploading(true);
    setUploadProgress(0);

    try {
      const uploadFormData = new FormData();
      uploadFormData.append("file", file);
      uploadFormData.append("title", formData.title);
      uploadFormData.append("description", formData.description);
      uploadFormData.append("document_number", formData.document_number);
      uploadFormData.append("category", formData.category);
      uploadFormData.append("document_type", formData.document_type);
      uploadFormData.append("access_level", formData.access_level);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      const response = await documentApi.uploadDocument(uploadFormData);

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.status === "success") {
        setSuccess("Document uploaded successfully!");
        setFile(null);
        setFormData({
          title: "",
          description: "",
          document_number: "",
          category: DOCUMENT_CATEGORIES.CURRICULUM,
          document_type: "",
          access_level: ACCESS_LEVELS.INTERNAL,
        });
        setFileHash("");
        setDuplicateWarning(null);
      } else {
        setError(response.message || "Upload failed");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Upload failed. Please try again.");
      setUploadProgress(0);
    } finally {
      setUploading(false);
    }
  };

  // Reset form
  const handleReset = () => {
    setFile(null);
    setError("");
    setSuccess("");
    setDuplicateWarning(null);
    setFileHash("");
    setFormData({
      title: "",
      description: "",
      document_number: "",
      category: DOCUMENT_CATEGORIES.CURRICULUM,
      document_type: "",
      access_level: ACCESS_LEVELS.INTERNAL,
    });
    setUploadProgress(0);
  };

  // Get folder path for display
  const getFolderDisplayName = (category: string): string => {
    const folderMap: Record<string, string> = {
      [DOCUMENT_CATEGORIES.CURRICULUM]: "📚 Buku Pelajaran",
      [DOCUMENT_CATEGORIES.ASSESSMENT]: "📝 Ujian dan Tugas",
      [DOCUMENT_CATEGORIES.GENERAL]: "📄 Dokumen Umum",
      [DOCUMENT_CATEGORIES.ACCREDITATION]: "🏆 Dokumen Akreditasi",
      [DOCUMENT_CATEGORIES.ADMINISTRATION]: "📋 Administrasi",
      [DOCUMENT_CATEGORIES.FINANCE]: "💰 Keuangan",
      [DOCUMENT_CATEGORIES.HR]: "👥 SDM",
      [DOCUMENT_CATEGORIES.LEGAL]: "⚖️ Dokumen Hukum",
      [DOCUMENT_CATEGORIES.STUDENT]: "🎓 Siswa",
      [DOCUMENT_CATEGORIES.TEACHER]: "👨‍🏫 Guru",
      [DOCUMENT_CATEGORIES.POLICY]: "📜 Kebijakan",
      [DOCUMENT_CATEGORIES.REPORT]: "📊 Laporan",
    };
    return folderMap[category] || category;
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Upload Dokumen
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Upload dokumen dengan validasi metadata untuk mencegah duplikasi berdasarkan hash file
      </Typography>

      <Grid container spacing={3}>
        {/* Upload Section */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Pilih File
              </Typography>

              {!file ? (
                <Box
                  sx={{
                    border: "2px dashed",
                    borderColor: "primary.main",
                    borderRadius: 2,
                    p: 4,
                    textAlign: "center",
                    cursor: "pointer",
                    "&:hover": {
                      backgroundColor: "primary.light",
                      opacity: 0.8,
                    },
                  }}
                  component="label"
                >
                  <input
                    type="file"
                    hidden
                    accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
                    onChange={handleFileChange}
                  />
                  <CloudUpload sx={{ fontSize: 48, color: "primary.main", mb: 2 }} />
                  <Typography variant="body1" color="primary">
                    Klik atau drag file ke sini
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX (Max 100MB)
                  </Typography>
                </Box>
              ) : (
                <Box>
                  <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                    <Description sx={{ mr: 2, color: "primary.main" }} />
                    <Typography variant="body1" noWrap>
                      {file.name}
                    </Typography>
                    <Button
                      size="small"
                      onClick={handleReset}
                      sx={{ ml: 2 }}
                    >
                      Ganti
                    </Button>
                  </Box>

                  <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 2 }}>
                    <Chip
                      icon={<Folder />}
                      label={documentApi.formatFileSize(file.size)}
                      size="small"
                    />
                    <Chip
                      label={file.type || "Unknown"}
                      size="small"
                      variant="outlined"
                    />
                    {fileHash && (
                      <Chip
                        label={`Hash: ${fileHash.substring(0, 8)}...`}
                        size="small"
                        color={checkingDuplicate ? "warning" : "success"}
                      />
                    )}
                  </Box>

                  {uploading && (
                    <Box sx={{ mt: 2 }}>
                      <LinearProgress variant="determinate" value={uploadProgress} />
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        {uploadProgress}%
                      </Typography>
                    </Box>
                  )}
                </Box>
              )}

              {error && (
                <Alert severity="error" sx={{ mt: 2 }} onClose={() => setError("")}>
                  {error}
                </Alert>
              )}

              {duplicateWarning && (
                <Alert
                  severity="warning"
                  sx={{ mt: 2 }}
                  action={
                    <Button color="inherit" size="small" onClick={() => setDuplicateWarning(null)}>
                      Abaikan
                    </Button>
                  }
                >
                  <Warning sx={{ mr: 1 }} />
                  {duplicateWarning.message}
                  {duplicateWarning.document && (
                    <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                      Dokumen existing: ID {duplicateWarning.document.id}, Status {duplicateWarning.document.status}
                    </Typography>
                  )}
                </Alert>
              )}

              {success && (
                <Alert
                  severity="success"
                  sx={{ mt: 2 }}
                  action={
                    <Button color="inherit" size="small" onClick={() => setSuccess("")}>
                      Tutup
                    </Button>
                  }
                >
                  <CheckCircle sx={{ mr: 1 }} />
                  {success}
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Metadata Section */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informasi Dokumen
              </Typography>

              <Grid container spacing={2}>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    fullWidth
                    label="Judul Dokumen *"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    disabled={uploading}
                    error={!formData.title.trim()}
                    helperText={!formData.title.trim() ? "Judul dokumen wajib diisi" : ""}
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Deskripsi"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    disabled={uploading}
                    multiline
                    rows={3}
                    placeholder="Deskripsi singkat tentang dokumen..."
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Nomor Dokumen"
                    name="document_number"
                    value={formData.document_number}
                    onChange={handleInputChange}
                    disabled={uploading}
                    placeholder="DOC-2024-001"
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Kategori Dokumen</InputLabel>
                    <Select
                      value={formData.category}
                      onChange={handleSelectChange("category")}
                      disabled={uploading}
                      label="Kategori Dokumen"
                    >
                      {Object.entries(DOCUMENT_CATEGORIES).map(([key, value]) => (
                        <MenuItem key={key} value={value}>
                          {getFolderDisplayName(value)}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Tipe Dokumen</InputLabel>
                    <Select
                      value={formData.document_type}
                      onChange={handleSelectChange("document_type")}
                      disabled={uploading || !!formData.document_type}
                      label="Tipe Dokumen"
                    >
                      {Object.values(DOCUMENT_TYPES).map((type) => (
                        <MenuItem key={type} value={type}>
                          {type}
                        </MenuItem>
                      ))}
                    </Select>
                    {formData.document_type && (
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                        Terdeteksi otomatis dari file
                      </Typography>
                    )}
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Level Akses</InputLabel>
                    <Select
                      value={formData.access_level}
                      onChange={handleSelectChange("access_level")}
                      disabled={uploading}
                      label="Level Akses"
                    >
                      <MenuItem value={ACCESS_LEVELS.PUBLIC}>🌐 Public</MenuItem>
                      <MenuItem value={ACCESS_LEVELS.INTERNAL}>🏢 Internal</MenuItem>
                      <MenuItem value={ACCESS_LEVELS.PRIVATE}>🔒 Private</MenuItem>
                      <MenuItem value={ACCESS_LEVELS.RESTRICTED}>🔐 Restricted</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <Typography variant="body2" color="text.secondary">
                      Folder penyimpanan: <strong>{getFolderDisplayName(formData.category)}</strong>
                    </Typography>
                    <Chip
                      icon={<Lock />}
                      label={formData.access_level}
                      size="small"
                      color={formData.access_level === ACCESS_LEVELS.PUBLIC ? "success" : "default"}
                    />
                  </Box>
                </Grid>

                <Grid item xs={12}>
                  <Box sx={{ display: "flex", gap: 2, mt: 2 }}>
                    <Button
                      variant="contained"
                      onClick={handleUpload}
                      disabled={!file || uploading || !formData.title.trim() || !!duplicateWarning}
                      startIcon={uploading ? <CircularProgress size={20} /> : <UploadIcon />}
                      fullWidth
                    >
                      {uploading ? "Mengupload..." : "Upload Dokumen"}
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={handleReset}
                      disabled={uploading}
                    >
                      Reset
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Info Section */}
      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3, bgcolor: "info.light", borderRadius: 2 }}>
          <Typography variant="h6" gutterBottom>
            ℹ️ Informasi Upload Dokumen
          </Typography>
          <Typography variant="body2" component="div">
            <ul>
              <li>File akan diupload ke SeaweedFS dengan folder berdasarkan kategori dokumen</li>
              <li>Validasi duplikat menggunakan hash file (SHA-256) bukan hanya nama file</li>
              <li>Dokumen dengan hash yang sama akan ditolak untuk mencegah duplikasi</li>
              <li>Metadata lengkap (judul, nomor, kategori) wajib diisi untuk organisasi yang baik</li>
              <li>Ukuran maksimum file adalah 100MB</li>
              <li>Format yang didukung: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX</li>
            </ul>
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}
