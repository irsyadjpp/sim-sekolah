import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface Rubric {
  id: string;
  title: string;
  description: string;
  subject_id: string;
  subject_name?: string;
  assessment_type: string;
  grade_level: string;
  max_score: number;
  is_template: boolean;
  is_active: boolean;
  criteria_count: number;
  created_at: string;
}

export default function RubricPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [rubrics, setRubrics] = useState<Rubric[]>([]);
  const [templates, setTemplates] = useState<Rubric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRubrics = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/rubrics`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setRubrics(json.data || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchTemplates = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/rubrics/templates`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setTemplates(json.data || []);
      }
    } catch (err: any) {
      console.error("Failed to fetch templates:", err);
    }
  };

  useEffect(() => {
    fetchRubrics();
    fetchTemplates();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getAssessmentTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      PROJECT: "Proyek",
      PRESENTATION: "Presentasi",
      WRITTEN_WORK: "Karya Tulis",
      PRACTICAL: "Praktik",
      BEHAVIORAL: "Perilaku",
      ORAL: "Lisan",
      OBSERVATION: "Observasi",
    };
    return labels[type] || type;
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("rubric.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("rubric.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/academic">
            {t("rubric.breadcrumb-academic")}
          </Link>
          <Link color="inherit" to="/academic/evaluation">
            {t("rubric.breadcrumb-evaluation")}
          </Link>
          <Typography variant="body2">{t("rubric.breadcrumb-rubric")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="rubric tabs">
            <Tab label={t("rubric.tab-rubrics")} />
            <Tab label={t("rubric.tab-templates")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
                <Typography variant="h6">{t("rubric.manage-rubrics")}</Typography>
                <Button variant="contained" color="primary">
                  {t("rubric.create-rubric")}
                </Button>
              </Box>

              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : rubrics.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {rubrics.map((rubric) => (
                    <Card key={rubric.id} className="transition-shadow hover:shadow-lg">
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="start" className="mb-2">
                          <Typography variant="h6" className="mb-0">
                            {rubric.title}
                          </Typography>
                          <Chip
                            label={rubric.is_template ? "Template" : "Rubric"}
                            size="small"
                            color={rubric.is_template ? "info" : "primary"}
                          />
                        </Box>
                        {rubric.description && (
                          <Typography variant="body2" color="textSecondary" className="mb-2">
                            {rubric.description}
                          </Typography>
                        )}
                        <Box className="space-y-1">
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("rubric.type")}: {getAssessmentTypeLabel(rubric.assessment_type)}
                          </Typography>
                          {rubric.subject_name && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("rubric.subject")}: {rubric.subject_name}
                            </Typography>
                          )}
                          {rubric.grade_level && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("rubric.grade-level")}: {rubric.grade_level}
                            </Typography>
                          )}
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("rubric.criteria-count")}: {rubric.criteria_count}
                          </Typography>
                          {rubric.max_score > 0 && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("rubric.max-score")}: {rubric.max_score}
                            </Typography>
                          )}
                        </Box>
                        <Box display="flex" gap={1} className="mt-3">
                          <Chip
                            label={rubric.is_active ? t("rubric.active") : t("rubric.inactive")}
                            size="small"
                            color={rubric.is_active ? "success" : "default"}
                          />
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center" className="py-10">
                  {t("rubric.no-rubrics")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
                <Typography variant="h6">{t("rubric.manage-templates")}</Typography>
                <Button variant="contained" color="primary">
                  {t("rubric.create-template")}
                </Button>
              </Box>

              {templates.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {templates.map((template) => (
                    <Card key={template.id} className="transition-shadow hover:shadow-lg">
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="start" className="mb-2">
                          <Typography variant="h6" className="mb-0">
                            {template.title}
                          </Typography>
                          <Chip label="Template" size="small" color="info" />
                        </Box>
                        {template.description && (
                          <Typography variant="body2" color="textSecondary" className="mb-2">
                            {template.description}
                          </Typography>
                        )}
                        <Box className="space-y-1">
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("rubric.type")}: {getAssessmentTypeLabel(template.assessment_type)}
                          </Typography>
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("rubric.criteria-count")}: {template.criteria_count}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center" className="py-10">
                  {t("rubric.no-templates")}
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
