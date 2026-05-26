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
  CircularProgress,
  Grid,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface TeachingReflection {
  id: string;
  lesson_topic: string;
  reflection_date: string;
  reflection_type: string;
  status: string;
  self_rating: number | null;
}

interface ReflectionSummary {
  total_reflections: number;
  submitted_reflections: number;
  average_self_rating: number;
  most_used_type: string;
  recent_activity: number;
}

export default function TeacherReflectionPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Data states
  const [reflections, setReflections] = useState<TeachingReflection[]>([]);
  const [summary, setSummary] = useState<ReflectionSummary | null>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Fetch functions
  const fetchReflections = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      // Use a default teacher ID - in production this would come from user context
      const teacherId = "default-teacher-id";
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teaching-reflection/teacher/${teacherId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setReflections(json.data.reflections || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      // Use a default teacher ID - in production this would come from user context
      const teacherId = "default-teacher-id";
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teaching-reflection/teacher/${teacherId}/summary`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSummary(json.data);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (tabValue === 0) fetchReflections();
    if (tabValue === 3) fetchSummary();
  }, [tabValue]);

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("reflection.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("reflection.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/teachers">
            {t("reflection.breadcrumb-teachers")}
          </Link>
          <Typography variant="body2">{t("reflection.breadcrumb-reflection")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="reflection tabs">
            <Tab label={t("reflection.tab-reflections")} />
            <Tab label={t("reflection.tab-effectiveness")} />
            <Tab label={t("reflection.tab-quality")} />
            <Tab label={t("reflection.tab-trends")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">{t("reflection.reflections-title")}</Typography>
                <Button variant="contained" color="primary">
                  {t("reflection.create-reflection")}
                </Button>
              </Box>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("reflection.reflections-description")}
              </Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                  <CircularProgress />
                </Box>
              ) : reflections.length === 0 ? (
                <Alert severity="info" className="mt-4">
                  {t("reflection.no-reflections")}
                </Alert>
              ) : (
                <Grid container spacing={2} className="mt-4">
                  {reflections.map((reflection) => (
                    <Grid size={{ xs: 12, md: 6 }} key={reflection.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6">{reflection.lesson_topic || "No Topic"}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {new Date(reflection.reflection_date).toLocaleDateString()}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            Type: {reflection.reflection_type} | Status: {reflection.status}
                          </Typography>
                          {reflection.self_rating && (
                            <Typography variant="body2" color="textSecondary">
                              Self Rating: {reflection.self_rating}
                            </Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("reflection.effectiveness-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("reflection.effectiveness-description")}
              </Typography>
              <Alert severity="info" className="mt-4">
                {t("reflection.effectiveness-coming-soon")}
              </Alert>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("reflection.quality-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("reflection.quality-description")}
              </Typography>
              <Alert severity="info" className="mt-4">
                {t("reflection.quality-coming-soon")}
              </Alert>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("reflection.trends-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("reflection.trends-description")}
              </Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                  <CircularProgress />
                </Box>
              ) : summary ? (
                <Grid container spacing={2} className="mt-4">
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.total_reflections}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Total Reflections
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.submitted_reflections}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Submitted
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.average_self_rating.toFixed(1)}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Avg Rating
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.recent_activity}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Recent Activity
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Alert severity="info" className="mt-4">
                  {t("reflection.no-trends")}
                </Alert>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
