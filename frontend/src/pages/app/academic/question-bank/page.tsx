"use client";

import { useEffect, useState } from "react";

import {
  Add as AddIcon,
  CheckCircle as CheckCircleIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  FilterList as FilterIcon,
  Help as HelpIcon,
  Refresh as RefreshIcon,
  School as SchoolIcon,
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  Visibility as ViewIcon,
} from "@mui/icons-material";
import {
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

interface Question {
  id: string;
  question_text: string;
  question_type: string;
  subject_id?: string;
  difficulty: string;
  points: number;
  status: string;
  author_name: string;
  usage_count: number;
  correct_rate: number;
  created_at: string;
}

interface QuestionStatistics {
  total_questions: number;
  by_difficulty: Record<string, number>;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  total_usage: number;
  average_correct_rate: number;
}

interface QuestionCategory {
  id: string;
  name: string;
  description: string;
  color: string;
}

export default function QuestionBankPage() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [statistics, setStatistics] = useState<QuestionStatistics | null>(null);
  const [categories, setCategories] = useState<QuestionCategory[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchQuestions = async () => {
    setLoading(true);
    setError(null);
    try {
      // Mock data for now since backend might not be fully implemented
      const mockQuestions: Question[] = [
        {
          id: "1",
          question_text: "Apa ibukota Indonesia?",
          question_type: "MULTIPLE_CHOICE",
          difficulty: "EASY",
          points: 1,
          status: "PUBLISHED",
          author_name: "Guru A",
          usage_count: 150,
          correct_rate: 85.5,
          created_at: "2025-01-15T10:00:00Z",
        },
        {
          id: "2",
          question_text: "Jelaskan konsep fotosintesis",
          question_type: "ESSAY",
          difficulty: "HARD",
          points: 5,
          status: "PUBLISHED",
          author_name: "Guru B",
          usage_count: 75,
          correct_rate: 72.3,
          created_at: "2025-01-20T14:30:00Z",
        },
      ];
      setQuestions(mockQuestions);
    } catch (err) {
      setError("Failed to fetch questions");
      console.error("Error fetching questions:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      // Mock statistics
      const mockStats: QuestionStatistics = {
        total_questions: 150,
        by_difficulty: { EASY: 50, MEDIUM: 60, HARD: 30, EXPERT: 10 },
        by_type: {
          MULTIPLE_CHOICE: 80,
          TRUE_FALSE: 30,
          ESSAY: 20,
          SHORT_ANSWER: 15,
          FILL_IN_BLANK: 5,
        },
        by_status: { PUBLISHED: 120, DRAFT: 20, PENDING: 10 },
        total_usage: 5000,
        average_correct_rate: 78.5,
      };
      setStatistics(mockStats);
    } catch (err) {
      console.error("Error fetching statistics:", err);
    }
  };

  const fetchCategories = async () => {
    try {
      // Mock categories
      const mockCategories: QuestionCategory[] = [
        { id: "1", name: "Pengetahuan", description: "Soal pengetahuan dasar", color: "#3B82F6" },
        { id: "2", name: "Pemahaman", description: "Soal pemahaman konsep", color: "#10B981" },
        { id: "3", name: "Penerapan", description: "Soal penerapan konsep", color: "#F59E0B" },
        { id: "4", name: "Analisis", description: "Soal analisis", color: "#EF4444" },
        { id: "5", name: "Evaluasi", description: "Soal evaluasi", color: "#8B5CF6" },
        { id: "6", name: "Kreatifitas", description: "Soal kreatifitas", color: "#EC4899" },
      ];
      setCategories(mockCategories);
    } catch (err) {
      console.error("Error fetching categories:", err);
    }
  };

  useEffect(() => {
    fetchQuestions();
    fetchStatistics();
    fetchCategories();
  }, []);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleAddQuestion = () => {
    setAddDialogOpen(true);
  };

  const handleViewQuestion = (question: Question) => {
    setSelectedQuestion(question);
    setViewDialogOpen(true);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "EASY":
        return "success";
      case "MEDIUM":
        return "info";
      case "HARD":
        return "warning";
      case "EXPERT":
        return "error";
      default:
        return "default";
    }
  };

  const getTypeColor = (type: string) => {
    const colors: Record<string, any> = {
      MULTIPLE_CHOICE: "primary",
      TRUE_FALSE: "secondary",
      ESSAY: "warning",
      SHORT_ANSWER: "info",
      FILL_IN_BLANK: "success",
    };
    return colors[type] || "default";
  };

  const filteredQuestions = questions.filter((q) => {
    const matchesSearch = q.question_text.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDifficulty = !selectedDifficulty || q.difficulty === selectedDifficulty;
    const matchesType = !selectedType || q.question_type === selectedType;
    const matchesStatus = !selectedStatus || q.status === selectedStatus;
    return matchesSearch && matchesDifficulty && matchesType && matchesStatus;
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
          Bank Soal
        </Typography>
        <Box display="flex" gap={2}>
          <Button variant="outlined" startIcon={<RefreshIcon />} onClick={fetchQuestions}>
            Refresh
          </Button>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleAddQuestion}>
            Tambah Soal
          </Button>
        </Box>
      </Box>

      {error && (
        <Box sx={{ mb: 3, p: 2, bgcolor: "error.light", borderRadius: 1 }}>
          <Typography color="error.dark">{error}</Typography>
        </Box>
      )}

      <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Soal" />
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
                        Total Soal
                      </Typography>
                      <HelpIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.total_questions}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Total Penggunaan
                      </Typography>
                      <TrendingUpIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.total_usage}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Rata-rata Benar
                      </Typography>
                      <SchoolIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.average_correct_rate}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        Soal Published
                      </Typography>
                      <CheckCircleIcon color="action" />
                    </Box>
                    <Typography variant="h4" fontWeight="bold">
                      {statistics.by_status.PUBLISHED || 0}
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
                  placeholder="Cari soal..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  InputProps={{
                    startAdornment: <SearchIcon sx={{ mr: 1, color: "text.secondary" }} />,
                  }}
                />
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <FormControl fullWidth>
                  <InputLabel>Kesulitan</InputLabel>
                  <Select
                    value={selectedDifficulty}
                    onChange={(e) => setSelectedDifficulty(e.target.value)}
                    label="Kesulitan"
                  >
                    <MenuItem value="">Semua</MenuItem>
                    <MenuItem value="EASY">Mudah</MenuItem>
                    <MenuItem value="MEDIUM">Sedang</MenuItem>
                    <MenuItem value="HARD">Sulit</MenuItem>
                    <MenuItem value="EXPERT">Ahli</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <FormControl fullWidth>
                  <InputLabel>Tipe Soal</InputLabel>
                  <Select value={selectedType} onChange={(e) => setSelectedType(e.target.value)} label="Tipe Soal">
                    <MenuItem value="">Semua</MenuItem>
                    <MenuItem value="MULTIPLE_CHOICE">Pilihan Ganda</MenuItem>
                    <MenuItem value="TRUE_FALSE">Benar/Salah</MenuItem>
                    <MenuItem value="ESSAY">Esai</MenuItem>
                    <MenuItem value="SHORT_ANSWER">Jawaban Pendek</MenuItem>
                    <MenuItem value="FILL_IN_BLANK">Isi Tempat Kosong</MenuItem>
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
                    setSelectedDifficulty("");
                    setSelectedType("");
                    setSelectedStatus("");
                  }}
                >
                  Reset Filter
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {/* Questions Table */}
          <Paper>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Pertanyaan</TableCell>
                    <TableCell>Tipe</TableCell>
                    <TableCell>Kesulitan</TableCell>
                    <TableCell>Poin</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Penggunaan</TableCell>
                    <TableCell>% Benar</TableCell>
                    <TableCell>Aksi</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredQuestions.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={9} align="center">
                        <Typography variant="body2" color="text.secondary">
                          Tidak ada soal ditemukan
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredQuestions.map((question) => (
                      <TableRow key={question.id}>
                        <TableCell>
                          <Typography variant="body2" noWrap>
                            {question.question_text}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={question.question_type.replace("_", " ")}
                            size="small"
                            color={getTypeColor(question.question_type)}
                          />
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={question.difficulty}
                            size="small"
                            color={getDifficultyColor(question.difficulty)}
                          />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{question.points}</Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={question.status}
                            size="small"
                            color={question.status === "PUBLISHED" ? "success" : "default"}
                          />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{question.usage_count}</Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{question.correct_rate}%</Typography>
                        </TableCell>
                        <TableCell>
                          <Box display="flex" gap={1}>
                            <Tooltip title="View">
                              <IconButton size="small" onClick={() => handleViewQuestion(question)}>
                                <ViewIcon />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Edit">
                              <IconButton size="small">
                                <EditIcon />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Delete">
                              <IconButton size="small">
                                <DeleteIcon />
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
              <CardHeader title="Soal per Kesulitan" />
              <CardContent>
                {Object.entries(statistics.by_difficulty).map(([difficulty, count]) => (
                  <Box key={difficulty} display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2">{difficulty}</Typography>
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
              <CardHeader title="Soal per Tipe" />
              <CardContent>
                {Object.entries(statistics.by_type).map(([type, count]) => (
                  <Box key={type} display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2">{type.replace("_", " ")}</Typography>
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
                        borderRadius: 2,
                        backgroundColor: category.color,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <SchoolIcon sx={{ color: "white" }} />
                    </Box>
                    <Box>
                      <Typography variant="h6" fontWeight="bold">
                        {category.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {category.description}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Add Question Dialog */}
      <Dialog open={addDialogOpen} onClose={() => setAddDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Tambah Soal Baru</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Grid container spacing={2}>
              <Grid size={{ xs: 12 }}>
                <TextField fullWidth label="Pertanyaan" multiline rows={3} required />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Tipe Soal</InputLabel>
                  <Select label="Tipe Soal" required>
                    <MenuItem value="MULTIPLE_CHOICE">Pilihan Ganda</MenuItem>
                    <MenuItem value="TRUE_FALSE">Benar/Salah</MenuItem>
                    <MenuItem value="ESSAY">Esai</MenuItem>
                    <MenuItem value="SHORT_ANSWER">Jawaban Pendek</MenuItem>
                    <MenuItem value="FILL_IN_BLANK">Isi Tempat Kosong</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Kesulitan</InputLabel>
                  <Select label="Kesulitan" required>
                    <MenuItem value="EASY">Mudah</MenuItem>
                    <MenuItem value="MEDIUM">Sedang</MenuItem>
                    <MenuItem value="HARD">Sulit</MenuItem>
                    <MenuItem value="EXPERT">Ahli</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField fullWidth label="Poin" type="number" defaultValue={1} />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select label="Status" defaultValue="DRAFT">
                    <MenuItem value="DRAFT">Draft</MenuItem>
                    <MenuItem value="PUBLISHED">Published</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddDialogOpen(false)}>Batal</Button>
          <Button variant="contained">Simpan</Button>
        </DialogActions>
      </Dialog>

      {/* View Question Dialog */}
      <Dialog open={viewDialogOpen} onClose={() => setViewDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Detail Soal</DialogTitle>
        <DialogContent>
          {selectedQuestion && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                {selectedQuestion.question_text}
              </Typography>
              <Grid container spacing={2} sx={{ mt: 2 }}>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Tipe:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedQuestion.question_type.replace("_", " ")}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Kesulitan:
                  </Typography>
                  <Chip
                    label={selectedQuestion.difficulty}
                    size="small"
                    color={getDifficultyColor(selectedQuestion.difficulty)}
                  />
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Poin:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedQuestion.points}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Status:
                  </Typography>
                  <Chip
                    label={selectedQuestion.status}
                    size="small"
                    color={selectedQuestion.status === "PUBLISHED" ? "success" : "default"}
                  />
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    Penggunaan:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedQuestion.usage_count}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Typography variant="body2" color="text.secondary">
                    % Benar:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {selectedQuestion.correct_rate}%
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialogOpen(false)}>Tutup</Button>
          <Button variant="contained" startIcon={<EditIcon />}>
            Edit
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
