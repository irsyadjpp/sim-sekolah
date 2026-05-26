import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Alert, Box, Breadcrumbs, Card, CardContent, CircularProgress, Tab, Tabs, Typography } from "@mui/material";

import { DEFAULTS } from "@/config";

interface LearningAnalytics {
  total_students: number;
  total_assessments: number;
  average_score: number;
  mastery_rate: number;
  by_subject: {
    subject_name: string;
    average_score: number;
    mastery_rate: number;
    assessment_count: number;
  }[];
  by_grade_level: {
    grade_level: string;
    student_count: number;
    average_score: number;
    mastery_rate: number;
  }[];
  recent_trends: {
    period: string;
    average_score: number;
    mastery_rate: number;
  }[];
}

export default function LearningAnalyticsPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [analytics, setAnalytics] = useState<LearningAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      // Try to get portfolio analytics as example
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/portfolio-analytics`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setAnalytics(json.data);
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
    fetchAnalytics();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("analytics.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("analytics.breadcrumb-home")}
          </Link>
          <Typography variant="body2">{t("analytics.breadcrumb-analytics")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="analytics tabs">
            <Tab label={t("analytics.tab-overview")} />
            <Tab label={t("analytics.tab-performance")} />
            <Tab label={t("analytics.tab-trends")} />
            <Tab label={t("analytics.tab-recommendations")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("analytics.overview-title")}</Typography>
              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : analytics ? (
                <Box className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-4">
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="textSecondary">
                        {t("analytics.total-students")}
                      </Typography>
                      <Typography variant="h4">{analytics.total_students || 0}</Typography>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="textSecondary">
                        {t("analytics.total-assessments")}
                      </Typography>
                      <Typography variant="h4">{analytics.total_assessments || 0}</Typography>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="textSecondary">
                        {t("analytics.average-score")}
                      </Typography>
                      <Typography variant="h4">{analytics.average_score?.toFixed(1) || 0}</Typography>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="textSecondary">
                        {t("analytics.mastery-rate")}
                      </Typography>
                      <Typography variant="h4">{analytics.mastery_rate?.toFixed(1) || 0}%</Typography>
                    </CardContent>
                  </Card>
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" className="mt-4">
                  {t("analytics.no-data")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("analytics.performance-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("analytics.performance-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("analytics.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("analytics.trends-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("analytics.trends-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("analytics.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("analytics.recommendations-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("analytics.recommendations-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("analytics.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
