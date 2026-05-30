import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  Stack,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import NiPlus from "@/icons/nexture/ni-plus";
import NiFile from "@/icons/nexture/ni-file";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiCopy from "@/icons/nexture/ni-copy";

interface SurveyTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  question_count: number;
  is_system_template: boolean;
  created_at: string;
}

function SurveyTemplatesPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [templates, setTemplates] = useState<SurveyTemplate[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("all");

  const CATEGORIES = [
    { value: "all", label: "Semua" },
    { value: "satisfaction", label: "Kepuasan" },
    { value: "assessment", label: "Penilaian" },
    { value: "feedback", label: "Masukan" },
    { value: "research", label: "Penelitian" },
  ];

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/survey-templates`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        setTemplates(json.data || []);
      } else {
        setError(json.message || "Failed to load templates");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTemplates();
  }, []);

  const useTemplate = async (templateId: string) => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/survey-templates/${templateId}/use`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        navigate(`/strategic-planning/data-collection/surveys/${json.data.id}/edit`);
      } else {
        setError(json.message || "Failed to use template");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const previewTemplate = (templateId: string) => {
    navigate(`/strategic-planning/data-collection/surveys/templates/${templateId}`);
  };

  const copyTemplate = async (templateId: string) => {
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/survey-templates/${templateId}/copy`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchTemplates();
      } else {
        setError(json.message || "Failed to copy template");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    }
  };

  const filteredTemplates = selectedCategory === "all"
    ? templates
    : templates.filter((t) => t.category === selectedCategory);

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Template Kuesioner
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => navigate("/strategic-planning/data-collection/surveys/create")}
        >
          Buat Kuesioner Baru
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/strategic-planning">Perencanaan Strategis</Link>
        <Link to="/strategic-planning/data-collection">Pengumpulan Data</Link>
        <Link to="/strategic-planning/data-collection/surveys">Kuesioner</Link>
        <Typography variant="body2">Template</Typography>
      </Breadcrumbs>

      <Grid container spacing={2} className="mb-6">
        {CATEGORIES.map((category) => (
          <Grid key={category.value}>
            <Button
              variant={selectedCategory === category.value ? "contained" : "outlined"}
              onClick={() => setSelectedCategory(category.value)}
            >
              {category.label}
            </Button>
          </Grid>
        ))}
      </Grid>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {loading ? (
        <Box className="flex justify-center items-center py-12">
          <CircularProgress size={48} />
        </Box>
      ) : filteredTemplates.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <NiFile size={64} className="text-text-secondary mx-auto mb-4" />
            <Typography variant="h6" className="mb-2">
              Tidak ada template yang tersedia
            </Typography>
            <Typography variant="body2" className="text-text-secondary mb-4">
              Mulai dari template sistem atau buat template kustom Anda sendiri
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {filteredTemplates.map((template) => (
            <Grid key={template.id} size={{ xs: 12, md: 4 }}>
              <Card className="h-full hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <Box className="flex justify-between items-start mb-4">
                    <Box className="flex-1">
                      {template.is_system_template && (
                        <Typography variant="caption" color="primary" className="mb-1 block">
                          Template Sistem
                        </Typography>
                      )}
                      <Typography variant="h6" className="font-bold mb-2">
                        {template.name}
                      </Typography>
                    </Box>
                    <NiFile className="text-primary" size={32} />
                  </Box>

                  <Typography variant="body2" className="text-text-secondary mb-4 line-clamp-2">
                    {template.description}
                  </Typography>

                  <Box className="flex items-center gap-4 mb-4">
                    <Typography variant="caption" className="text-text-secondary">
                      {template.question_count} pertanyaan
                    </Typography>
                    <Typography variant="caption" className="text-text-secondary">
                      {template.category}
                    </Typography>
                  </Box>

                  <Stack spacing={2}>
                    <Button
                      variant="contained"
                      fullWidth
                      onClick={() => useTemplate(template.id)}
                    >
                      Gunakan Template
                    </Button>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<NiEyeOpen size="small" />}
                      onClick={() => previewTemplate(template.id)}
                    >
                      Preview
                    </Button>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<NiCopy size="small" />}
                      onClick={() => copyTemplate(template.id)}
                    >
                      Duplikat
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

export default function SurveyTemplatesPageWithGuard() {
  return (
    <PermissionGuard allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR"]}>
      <SurveyTemplatesPage />
    </PermissionGuard>
  );
}