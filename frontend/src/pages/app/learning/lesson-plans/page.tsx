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

interface LessonPlan {
  id: string;
  title: string;
  subject_id: string;
  subject_name?: string;
  classroom_id: string;
  classroom_name?: string;
  atp_id: string;
  meeting_date: string;
  meeting_number: number;
  duration_minutes: number;
  status: string;
  academic_year_id: string;
  semester: number;
  sections_count: number;
  resources_count: number;
  created_at: string;
}

interface LessonPlanTemplate {
  id: string;
  title: string;
  description: string;
  subject_id: string;
  subject_name?: string;
  grade_level: string;
  category: string;
  default_duration_minutes: number;
  is_active: boolean;
  created_at: string;
}

export default function LessonPlansPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [lessonPlans, setLessonPlans] = useState<LessonPlan[]>([]);
  const [templates, setTemplates] = useState<LessonPlanTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLessonPlans = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/lesson-plans`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setLessonPlans(json.data || []);
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
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/lesson-plan-templates`, {
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
    fetchLessonPlans();
    fetchTemplates();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      DRAFT: "Draft",
      REVIEW: "Review",
      APPROVED: "Disetujui",
      PUBLISHED: "Terbit",
    };
    return labels[status] || status;
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, any> = {
      DRAFT: "default",
      REVIEW: "warning",
      APPROVED: "info",
      PUBLISHED: "success",
    };
    return colors[status] || "default";
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("lesson-planning.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("lesson-planning.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/learning">
            {t("lesson-planning.breadcrumb-learning")}
          </Link>
          <Typography variant="body2">{t("lesson-planning.breadcrumb-lesson-plans")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="lesson planning tabs">
            <Tab label={t("lesson-planning.tab-lesson-plans")} />
            <Tab label={t("lesson-planning.tab-templates")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
                <Typography variant="h6">{t("lesson-planning.manage-lesson-plans")}</Typography>
                <Button variant="contained" color="primary">
                  {t("lesson-planning.create-lesson-plan")}
                </Button>
              </Box>

              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : lessonPlans.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {lessonPlans.map((lessonPlan) => (
                    <Card key={lessonPlan.id} className="transition-shadow hover:shadow-lg">
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="start" className="mb-2">
                          <Typography variant="h6" className="mb-0">
                            {lessonPlan.title}
                          </Typography>
                          <Chip
                            label={getStatusLabel(lessonPlan.status)}
                            size="small"
                            color={getStatusColor(lessonPlan.status)}
                          />
                        </Box>
                        <Box className="space-y-1">
                          {lessonPlan.subject_name && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("lesson-planning.subject")}: {lessonPlan.subject_name}
                            </Typography>
                          )}
                          {lessonPlan.classroom_name && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("lesson-planning.classroom")}: {lessonPlan.classroom_name}
                            </Typography>
                          )}
                          {lessonPlan.meeting_date && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("lesson-planning.meeting-date")}:{" "}
                              {new Date(lessonPlan.meeting_date).toLocaleDateString("id-ID")}
                            </Typography>
                          )}
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("lesson-planning.meeting-number")}: {lessonPlan.meeting_number}
                          </Typography>
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("lesson-planning.duration")}: {lessonPlan.duration_minutes} menit
                          </Typography>
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("lesson-planning.sections")}: {lessonPlan.sections_count}
                          </Typography>
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("lesson-planning.resources")}: {lessonPlan.resources_count}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center" className="py-10">
                  {t("lesson-planning.no-lesson-plans")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
                <Typography variant="h6">{t("lesson-planning.manage-templates")}</Typography>
                <Button variant="contained" color="primary">
                  {t("lesson-planning.create-template")}
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
                          <Chip
                            label={template.is_active ? t("lesson-planning.active") : t("lesson-planning.inactive")}
                            size="small"
                            color={template.is_active ? "success" : "default"}
                          />
                        </Box>
                        {template.description && (
                          <Typography variant="body2" color="textSecondary" className="mb-2">
                            {template.description}
                          </Typography>
                        )}
                        <Box className="space-y-1">
                          {template.subject_name && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("lesson-planning.subject")}: {template.subject_name}
                            </Typography>
                          )}
                          {template.grade_level && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("lesson-planning.grade-level")}: {template.grade_level}
                            </Typography>
                          )}
                          {template.category && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("lesson-planning.category")}: {template.category}
                            </Typography>
                          )}
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("lesson-planning.default-duration")}: {template.default_duration_minutes} menit
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center" className="py-10">
                  {t("lesson-planning.no-templates")}
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
