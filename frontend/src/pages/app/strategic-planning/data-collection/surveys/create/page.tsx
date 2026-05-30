import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  Stack,
  Switch,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiChevronLeft from "@/icons/nexture/ni-chevron-left";
import NiPlus from "@/icons/nexture/ni-plus";
import NiTrash from "@/icons/nexture/ni-trash";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiGripVertical from "@/icons/nexture/ni-grip-vertical";

interface Question {
  id: string;
  question_type: string;
  question_text: string;
  description?: string;
  required: boolean;
  options?: string[];
  validation_rules?: {
    min_length?: number;
    max_length?: number;
    pattern?: string;
  };
}

interface SurveyFormData {
  title: string;
  description: string;
  survey_type: string;
  target_audience: string;
  status: string;
  start_date: string;
  end_date: string;
  questions: Question[];
}

const QUESTION_TYPES = [
  { value: "text", label: "Teks Pendek", icon: "T" },
  { value: "textarea", label: "Teks Panjang", icon: "¶" },
  { value: "number", label: "Angka", icon: "#" },
  { value: "email", label: "Email", icon: "@" },
  { value: "date", label: "Tanggal", icon: "📅" },
  { value: "single_choice", label: "Pilihan Ganda", icon: "○" },
  { value: "multiple_choice", label: "Checklist", icon: "☑" },
  { value: "rating", label: "Rating 1-5", icon: "★" },
  { value: "dropdown", label: "Dropdown", icon: "▼" },
];

const SURVEY_TYPES = [
  { value: "general", label: "Umum" },
  { value: "satisfaction", label: "Kepuasan" },
  { value: "feedback", label: "Masukan" },
  { value: "assessment", label: "Penilaian" },
  { value: "research", label: "Penelitian" },
];

const TARGET_AUDIENCES = [
  { value: "students", label: "Siswa" },
  { value: "teachers", label: "Guru" },
  { value: "parents", label: "Orang Tua" },
  { value: "staff", label: "Staff" },
  { value: "community", label: "Masyarakat" },
  { value: "mixed", label: "Campuran" },
];

function SurveyCreatePage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = !!id;

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [selectedQuestion, setSelectedQuestion] = useState<string | null>(null);

  const [formData, setFormData] = useState<SurveyFormData>({
    title: "",
    description: "",
    survey_type: "general",
    target_audience: "students",
    status: "draft",
    start_date: "",
    end_date: "",
    questions: [],
  });

  const loadSurvey = async () => {
    if (!id) return;

    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        const survey = json.data;
        setFormData({
          title: survey.title || "",
          description: survey.description || "",
          survey_type: survey.survey_type || "general",
          target_audience: survey.target_audience || "students",
          status: survey.status || "draft",
          start_date: survey.start_date ? survey.start_date.split("T")[0] : "",
          end_date: survey.end_date ? survey.end_date.split("T")[0] : "",
          questions: survey.questions || [],
        });
      } else {
        setError(json.message || "Failed to load survey");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isEdit) {
      loadSurvey();
    }
  }, [id]);

  const handleInputChange = (field: keyof SurveyFormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const addQuestion = (type: string) => {
    const newQuestion: Question = {
      id: `q-${Date.now()}`,
      question_type: type,
      question_text: "",
      description: "",
      required: false,
      options: ["single_choice", "multiple_choice", "dropdown"].includes(type) ? ["", ""] : undefined,
    };
    setFormData((prev) => ({
      ...prev,
      questions: [...prev.questions, newQuestion],
    }));
    setSelectedQuestion(newQuestion.id);
  };

  const updateQuestion = (questionId: string, updates: Partial<Question>) => {
    setFormData((prev) => ({
      ...prev,
      questions: prev.questions.map((q) => (q.id === questionId ? { ...q, ...updates } : q)),
    }));
  };

  const deleteQuestion = (questionId: string) => {
    setFormData((prev) => ({
      ...prev,
      questions: prev.questions.filter((q) => q.id !== questionId),
    }));
    if (selectedQuestion === questionId) {
      setSelectedQuestion(null);
    }
  };

  const moveQuestion = (index: number, direction: "up" | "down") => {
    const newQuestions = [...formData.questions];
    const newIndex = direction === "up" ? index - 1 : index + 1;

    if (newIndex < 0 || newIndex >= newQuestions.length) return;

    [newQuestions[index], newQuestions[newIndex]] = [newQuestions[newIndex], newQuestions[index]];
    setFormData((prev) => ({ ...prev, questions: newQuestions }));
  };

  const addOption = (questionId: string) => {
    setFormData((prev) => ({
      ...prev,
      questions: prev.questions.map((q) =>
        q.id === questionId && q.options ? { ...q, options: [...q.options, ""] } : q
      ),
    }));
  };

  const updateOption = (questionId: string, optionIndex: number, value: string) => {
    setFormData((prev) => ({
      ...prev,
      questions: prev.questions.map((q) =>
        q.id === questionId && q.options
          ? { ...q, options: q.options.map((opt, i) => (i === optionIndex ? value : opt)) }
          : q
      ),
    }));
  };

  const deleteOption = (questionId: string, optionIndex: number) => {
    setFormData((prev) => ({
      ...prev,
      questions: prev.questions.map((q) =>
        q.id === questionId && q.options
          ? { ...q, options: q.options.filter((_, i) => i !== optionIndex) }
          : q
      ),
    }));
  };

  const handleSubmit = async (publish = false) => {
    setSaving(true);
    setError(null);

    try {
      const token = localStorage.getItem("accessToken");
      const submitData = {
        ...formData,
        status: publish ? "active" : formData.status,
      };

      const url = isEdit
        ? `${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys/${id}`
        : `${DEFAULTS.API_URL}/api/v1/strategic-planning/surveys`;

      const method = isEdit ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(submitData),
      });

      const json = await res.json();

      if (json.status === "success") {
        navigate("/strategic-planning/data-collection/surveys");
      } else {
        setError(json.message || "Failed to save survey");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setSaving(false);
    }
  };

  const selectedQuestionData = formData.questions.find((q) => q.id === selectedQuestion);

  if (loading) {
    return (
      <Box className="flex justify-center items-center py-12">
        <CircularProgress size={48} />
      </Box>
    );
  }

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Box className="flex items-center gap-2">
          <IconButton onClick={() => navigate("/strategic-planning/data-collection/surveys")}>
            <NiChevronLeft />
          </IconButton>
          <Typography variant="h1" component="h1" className="mb-0">
            {isEdit ? "Edit Kuesioner" : "Buat Kuesioner Baru"}
          </Typography>
        </Box>
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            onClick={() => handleSubmit(false)}
            disabled={saving}
          >
            {saving ? "Menyimpan..." : "Simpan Draft"}
          </Button>
          <Button
            variant="contained"
            onClick={() => handleSubmit(true)}
            disabled={saving}
          >
            {saving ? "Memproses..." : "Terbitkan"}
          </Button>
        </Stack>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Link to="/strategic-planning/data-collection/surveys">Kuesioner</Link>
        <Typography variant="body2">{isEdit ? "Edit" : "Buat Baru"}</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} className="mb-4">
        <Tab label="Informasi Dasar" />
        <Tab label="Form Builder" />
        <Tab label="Preview" />
      </Tabs>

      {activeTab === 0 && (
        <Card>
          <CardContent className="p-6">
            <Grid container spacing={3}>
              <Grid size={{ xs: 12 }}>
                <FormControl fullWidth>
                  <InputLabel>Judul Kuesioner *</InputLabel>
                  <TextField
                    fullWidth
                    label="Judul Kuesioner *"
                    value={formData.title}
                    onChange={(e) => handleInputChange("title", e.target.value)}
                    required
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12 }}>
                <FormControl fullWidth>
                  <InputLabel>Deskripsi</InputLabel>
                  <TextField
                    fullWidth
                    label="Deskripsi"
                    value={formData.description}
                    onChange={(e) => handleInputChange("description", e.target.value)}
                    multiline
                    rows={3}
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Tipe Kuesioner</InputLabel>
                  <Select
                    label="Tipe Kuesioner"
                    value={formData.survey_type}
                    onChange={(e) => handleInputChange("survey_type", e.target.value)}
                  >
                    {SURVEY_TYPES.map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        {type.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Target Audiens</InputLabel>
                  <Select
                    label="Target Audiens"
                    value={formData.target_audience}
                    onChange={(e) => handleInputChange("target_audience", e.target.value)}
                  >
                    {TARGET_AUDIENCES.map((audience) => (
                      <MenuItem key={audience.value} value={audience.value}>
                        {audience.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Tanggal Mulai</InputLabel>
                  <TextField
                    fullWidth
                    label="Tanggal Mulai"
                    type="date"
                    value={formData.start_date}
                    onChange={(e) => handleInputChange("start_date", e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Tanggal Selesai</InputLabel>
                  <TextField
                    fullWidth
                    label="Tanggal Selesai"
                    type="date"
                    value={formData.end_date}
                    onChange={(e) => handleInputChange("end_date", e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </FormControl>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {activeTab === 1 && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-4">
                <Typography variant="h6" className="mb-4 font-bold">
                  Komponen Pertanyaan
                </Typography>
                <Stack spacing={2}>
                  {QUESTION_TYPES.map((type) => (
                    <Button
                      key={type.value}
                      variant="outlined"
                      fullWidth
                      onClick={() => addQuestion(type.value)}
                      startIcon={<span className="text-lg">{type.icon}</span>}
                    >
                      {type.label}
                    </Button>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-4">
                <Typography variant="h6" className="mb-4 font-bold">
                  Daftar Pertanyaan ({formData.questions.length})
                </Typography>
                {formData.questions.length === 0 ? (
                  <Typography variant="body2" className="text-text-secondary text-center py-4">
                    Belum ada pertanyaan. Tambahkan dari panel kiri.
                  </Typography>
                ) : (
                  <Stack spacing={2}>
                    {formData.questions.map((question, index) => (
                      <Card
                        key={question.id}
                        className={`cursor-pointer border ${selectedQuestion === question.id ? "border-blue-500 bg-blue-50" : ""
                          }`}
                        onClick={() => setSelectedQuestion(question.id)}
                      >
                        <CardContent className="p-3">
                          <Stack direction="row" alignItems="center" spacing={1}>
                            <IconButton
                              size="small"
                              onClick={(e) => {
                                e.stopPropagation();
                                moveQuestion(index, "up");
                              }}
                              disabled={index === 0}
                            >
                              <NiGripVertical size="small" />
                            </IconButton>
                            <Typography variant="body2" className="flex-1 truncate">
                              {index + 1}. {question.question_text || "Tanpa judul"}
                            </Typography>
                            {question.required && (
                              <Typography variant="caption" color="error">
                                *
                              </Typography>
                            )}
                            <IconButton
                              size="small"
                              onClick={(e) => {
                                e.stopPropagation();
                                deleteQuestion(question.id);
                              }}
                            >
                              <NiTrash size="small" />
                            </IconButton>
                          </Stack>
                        </CardContent>
                      </Card>
                    ))}
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="p-4">
                {selectedQuestionData ? (
                  <Stack spacing={3}>
                    <Typography variant="h6" className="font-bold">
                      Edit Pertanyaan
                    </Typography>

                    <FormControl fullWidth>
                      <TextField
                        fullWidth
                        label="Pertanyaan *"
                        value={selectedQuestionData.question_text}
                        onChange={(e) =>
                          updateQuestion(selectedQuestionData.id, { question_text: e.target.value })
                        }
                        required
                      />
                    </FormControl>

                    <FormControl fullWidth>
                      <TextField
                        fullWidth
                        label="Deskripsi"
                        value={selectedQuestionData.description || ""}
                        onChange={(e) =>
                          updateQuestion(selectedQuestionData.id, { description: e.target.value })
                        }
                        multiline
                        rows={2}
                      />
                    </FormControl>

                    {selectedQuestionData.options && (
                      <Box>
                        <Typography variant="subtitle2" className="mb-2">
                          Opsi Jawaban
                        </Typography>
                        <Stack spacing={1}>
                          {selectedQuestionData.options.map((opt, idx) => (
                            <Stack key={idx} direction="row" spacing={1} alignItems="center">
                              <TextField
                                fullWidth
                                size="small"
                                value={opt}
                                onChange={(e) => updateOption(selectedQuestionData.id, idx, e.target.value)}
                              />
                              <IconButton
                                size="small"
                                onClick={() => deleteOption(selectedQuestionData.id, idx)}
                              >
                                <NiTrash size="small" />
                              </IconButton>
                            </Stack>
                          ))}
                          <Button
                            size="small"
                            variant="outlined"
                            startIcon={<NiPlus size="small" />}
                            onClick={() => addOption(selectedQuestionData.id)}
                          >
                            Tambah Opsi
                          </Button>
                        </Stack>
                      </Box>
                    )}

                    <FormControlLabel
                      control={
                        <Switch
                          checked={selectedQuestionData.required}
                          onChange={(e) =>
                            updateQuestion(selectedQuestionData.id, { required: e.target.checked })
                          }
                        />
                      }
                      label="Wajib diisi"
                    />
                  </Stack>
                ) : (
                  <Typography variant="body2" className="text-text-secondary text-center py-4">
                    Pilih pertanyaan untuk mengedit
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 2 && (
        <Card>
          <CardContent className="p-6">
            <Typography variant="h5" className="mb-4 font-bold">
              Preview: {formData.title || "Tanpa Judul"}
            </Typography>
            {formData.description && (
              <Typography variant="body2" className="mb-4 text-text-secondary">
                {formData.description}
              </Typography>
            )}
            <Divider className="my-4" />
            <Stack spacing={3}>
              {formData.questions.length === 0 ? (
                <Typography variant="body2" className="text-text-secondary text-center py-4">
                  Belum ada pertanyaan untuk ditampilkan.
                </Typography>
              ) : (
                formData.questions.map((question, index) => (
                  <Box key={question.id}>
                    <Typography variant="subtitle1" className="font-bold mb-1">
                      {index + 1}. {question.question_text} {question.required && <span className="text-error">*</span>}
                    </Typography>
                    {question.description && (
                      <Typography variant="body2" className="text-text-secondary mb-2">
                        {question.description}
                      </Typography>
                    )}
                    <Typography variant="body2" className="text-text-secondary">
                      {question.question_type === "text" && "Input teks pendek"}
                      {question.question_type === "textarea" && "Input teks panjang"}
                      {question.question_type === "number" && "Input angka"}
                      {question.question_type === "email" && "Input email"}
                      {question.question_type === "date" && "Pilih tanggal"}
                      {question.question_type === "rating" && "⭐⭐⭐⭐⭐"}
                      {(question.question_type === "single_choice" ||
                        question.question_type === "multiple_choice" ||
                        question.question_type === "dropdown") && (
                          <Box className="pl-4">
                            {question.options?.map((opt, idx) => (
                              <Typography key={idx} variant="body2">
                                {question.question_type === "multiple_choice" ? "☐" : "○"} {opt || `Opsi ${idx + 1}`}
                              </Typography>
                            ))}
                          </Box>
                        )}
                    </Typography>
                  </Box>
                ))
              )}
            </Stack>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default function SurveyCreatePageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR"]}>
      <SurveyCreatePage />
    </PermissionGuard>
  );
}