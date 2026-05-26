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

interface SupervisionCycle {
  id: string;
  cycle_name: string;
  start_date: string;
  end_date: string;
  status: string;
  description: string;
}

interface TeacherObservation {
  id: string;
  teacher_id: string;
  observation_date: string;
  observation_type: string;
  status: string;
  lesson_topic: string;
  score: number | null;
}

interface SupervisionSummary {
  total_cycles: number;
  active_cycles: number;
  total_observations: number;
  pending_observations: number;
  completed_observations: number;
  average_score: number;
  teachers_supervised: number;
}

export default function AcademicSupervisionPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Data states
  const [cycles, setCycles] = useState<SupervisionCycle[]>([]);
  const [observations, setObservations] = useState<TeacherObservation[]>([]);
  const [summary, setSummary] = useState<SupervisionSummary | null>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Fetch functions
  const fetchCycles = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/supervision/cycles`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setCycles(json.data.cycles || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchObservations = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/supervision/observations`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setObservations(json.data.observations || []);
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
      // Use a default school ID - in production this would come from user context
      const schoolId = "default-school-id";
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/supervision/cycles/summary?school_id=${schoolId}`, {
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
    if (tabValue === 0) fetchCycles();
    if (tabValue === 1) fetchObservations();
    if (tabValue === 3) fetchSummary();
  }, [tabValue]);

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("supervision.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("supervision.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/academic">
            {t("supervision.breadcrumb-academic")}
          </Link>
          <Typography variant="body2">{t("supervision.breadcrumb-supervision")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="supervision tabs">
            <Tab label={t("supervision.tab-cycles")} />
            <Tab label={t("supervision.tab-observations")} />
            <Tab label={t("supervision.tab-feedback")} />
            <Tab label={t("supervision.tab-analytics")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">{t("supervision.cycles-title")}</Typography>
                <Button variant="contained" color="primary">
                  {t("supervision.create-cycle")}
                </Button>
              </Box>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("supervision.cycles-description")}
              </Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                  <CircularProgress />
                </Box>
              ) : cycles.length === 0 ? (
                <Alert severity="info" className="mt-4">
                  {t("supervision.no-cycles")}
                </Alert>
              ) : (
                <Grid container spacing={2} className="mt-4">
                  {cycles.map((cycle) => (
                    <Grid size={{ xs: 12, md: 6 }} key={cycle.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6">{cycle.cycle_name}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {new Date(cycle.start_date).toLocaleDateString()} -{" "}
                            {new Date(cycle.end_date).toLocaleDateString()}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            Status: {cycle.status}
                          </Typography>
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
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">{t("supervision.observations-title")}</Typography>
                <Button variant="contained" color="primary">
                  {t("supervision.create-observation")}
                </Button>
              </Box>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("supervision.observations-description")}
              </Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                  <CircularProgress />
                </Box>
              ) : observations.length === 0 ? (
                <Alert severity="info" className="mt-4">
                  {t("supervision.no-observations")}
                </Alert>
              ) : (
                <Grid container spacing={2} className="mt-4">
                  {observations.map((observation) => (
                    <Grid size={{ xs: 12, md: 6 }} key={observation.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6">{observation.lesson_topic || "No Topic"}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {new Date(observation.observation_date).toLocaleDateString()}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            Type: {observation.observation_type} | Status: {observation.status}
                          </Typography>
                          {observation.score && (
                            <Typography variant="body2" color="textSecondary">
                              Score: {observation.score}
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

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("supervision.feedback-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("supervision.feedback-description")}
              </Typography>
              <Alert severity="info" className="mt-4">
                {t("supervision.feedback-coming-soon")}
              </Alert>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("supervision.analytics-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("supervision.analytics-description")}
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
                        <Typography variant="h4">{summary.total_cycles}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Total Cycles
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.total_observations}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Total Observations
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.average_score.toFixed(1)}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Average Score
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.teachers_supervised}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Teachers Supervised
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Alert severity="info" className="mt-4">
                  {t("supervision.no-analytics")}
                </Alert>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
