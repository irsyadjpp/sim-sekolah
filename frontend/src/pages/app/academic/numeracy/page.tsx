import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Card, CardContent, Tab, Tabs, Typography } from "@mui/material";

import { DEFAULTS } from "@/config";

interface NumeracyAnalytics {
  total_assessments: number;
  average_score: number;
  mastery_rate: number;
  by_numeracy_type: {
    numeracy_type: string;
    type_name: string;
    total_assessments: number;
    average_score: number;
    mastery_rate: number;
  }[];
  by_mastery_level: {
    mastery_level: string;
    level_name: string;
    count: number;
    percentage: number;
  }[];
}

export default function NumeracyPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [analytics, setAnalytics] = useState<NumeracyAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/numeracy/analytics`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setAnalytics(json.data);
      }
    } catch (err) {
      console.error("Failed to fetch analytics:", err);
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
          {t("numeracy.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("numeracy.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/academic">
            {t("numeracy.breadcrumb-academic")}
          </Link>
          <Typography variant="body2">{t("numeracy.breadcrumb-numeracy")}</Typography>
        </Breadcrumbs>
      </Box>

      <Card className="mb-6">
        <CardContent>
          <Typography variant="h6" className="mb-4">
            {t("numeracy.analytics-title")}
          </Typography>
          {loading ? (
            <Typography>{t("numeracy.loading")}</Typography>
          ) : analytics ? (
            <Box className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <Card>
                <CardContent>
                  <Typography variant="body2" color="textSecondary">
                    {t("numeracy.total-assessments")}
                  </Typography>
                  <Typography variant="h4">{analytics.total_assessments}</Typography>
                </CardContent>
              </Card>
              <Card>
                <CardContent>
                  <Typography variant="body2" color="textSecondary">
                    {t("numeracy.average-score")}
                  </Typography>
                  <Typography variant="h4">{analytics.average_score.toFixed(1)}</Typography>
                </CardContent>
              </Card>
              <Card>
                <CardContent>
                  <Typography variant="body2" color="textSecondary">
                    {t("numeracy.mastery-rate")}
                  </Typography>
                  <Typography variant="h4">{analytics.mastery_rate.toFixed(1)}%</Typography>
                </CardContent>
              </Card>
            </Box>
          ) : (
            <Typography>{t("numeracy.no-data")}</Typography>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="numeracy tabs">
            <Tab label={t("numeracy.tab-indicators")} />
            <Tab label={t("numeracy.tab-assessments")} />
            <Tab label={t("numeracy.tab-growth")} />
            <Tab label={t("numeracy.tab-interventions")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("numeracy.indicators-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("numeracy.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("numeracy.assessments-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("numeracy.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("numeracy.growth-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("numeracy.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("numeracy.interventions-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("numeracy.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
