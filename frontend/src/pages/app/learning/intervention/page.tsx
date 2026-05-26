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

interface RemedialProgram {
  id: string;
  program_name: string;
  target_grade: string;
  description: string;
  is_active: boolean;
}

interface EnrichmentProgram {
  id: string;
  program_name: string;
  target_grade: string;
  description: string;
  is_active: boolean;
}

interface InterventionSummary {
  total_assignments: number;
  remedial_assignments: number;
  enrichment_assignments: number;
  active_interventions: number;
  completed_interventions: number;
  average_improvement: number;
  success_rate: number;
}

export default function InterventionPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Data states
  const [remedialPrograms, setRemedialPrograms] = useState<RemedialProgram[]>([]);
  const [enrichmentPrograms, setEnrichmentPrograms] = useState<EnrichmentProgram[]>([]);
  const [summary, setSummary] = useState<InterventionSummary | null>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Fetch functions
  const fetchRemedialPrograms = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intervention/remedial`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setRemedialPrograms(json.data.programs || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchEnrichmentPrograms = async () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intervention/enrichment`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setEnrichmentPrograms(json.data.programs || []);
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
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intervention/assignments/summary?school_id=${schoolId}`, {
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
    if (tabValue === 0) fetchRemedialPrograms();
    if (tabValue === 1) fetchEnrichmentPrograms();
    if (tabValue === 3) fetchSummary();
  }, [tabValue]);

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("intervention.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("intervention.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/learning">
            {t("intervention.breadcrumb-learning")}
          </Link>
          <Typography variant="body2">{t("intervention.breadcrumb-intervention")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="intervention tabs">
            <Tab label={t("intervention.tab-remedial")} />
            <Tab label={t("intervention.tab-enrichment")} />
            <Tab label={t("intervention.tab-workflows")} />
            <Tab label={t("intervention.tab-analytics")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">{t("intervention.remedial-title")}</Typography>
                <Button variant="contained" color="primary">
                  {t("intervention.create-remedial")}
                </Button>
              </Box>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("intervention.remedial-description")}
              </Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                  <CircularProgress />
                </Box>
              ) : remedialPrograms.length === 0 ? (
                <Alert severity="info" className="mt-4">
                  {t("intervention.no-remedial")}
                </Alert>
              ) : (
                <Grid container spacing={2} className="mt-4">
                  {remedialPrograms.map((program) => (
                    <Grid size={{ xs: 12, md: 6 }} key={program.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6">{program.program_name}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            Grade: {program.target_grade}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            Status: {program.is_active ? "Active" : "Inactive"}
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
                <Typography variant="h6">{t("intervention.enrichment-title")}</Typography>
                <Button variant="contained" color="primary">
                  {t("intervention.create-enrichment")}
                </Button>
              </Box>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("intervention.enrichment-description")}
              </Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                  <CircularProgress />
                </Box>
              ) : enrichmentPrograms.length === 0 ? (
                <Alert severity="info" className="mt-4">
                  {t("intervention.no-enrichment")}
                </Alert>
              ) : (
                <Grid container spacing={2} className="mt-4">
                  {enrichmentPrograms.map((program) => (
                    <Grid size={{ xs: 12, md: 6 }} key={program.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6">{program.program_name}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            Grade: {program.target_grade}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            Status: {program.is_active ? "Active" : "Inactive"}
                          </Typography>
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
              <Typography variant="h6">{t("intervention.workflows-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("intervention.workflows-description")}
              </Typography>
              <Alert severity="info" className="mt-4">
                {t("intervention.workflows-coming-soon")}
              </Alert>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("intervention.analytics-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("intervention.analytics-description")}
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
                        <Typography variant="h4">{summary.total_assignments}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Total Assignments
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.active_interventions}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Active Interventions
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.average_improvement.toFixed(1)}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Avg Improvement
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid size={{ xs: 12, md: 3 }}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h4">{summary.success_rate.toFixed(0)}%</Typography>
                        <Typography variant="body2" color="textSecondary">
                          Success Rate
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Alert severity="info" className="mt-4">
                  {t("intervention.no-analytics")}
                </Alert>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
