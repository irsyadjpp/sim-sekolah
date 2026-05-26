import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Alert, Box, Breadcrumbs, Card, CardContent, CircularProgress, Tab, Tabs, Typography } from "@mui/material";

import { DEFAULTS } from "@/config";

interface Portfolio {
  id: string;
  student_id: string;
  student_name: string;
  title: string;
  description: string;
  artifact_count: number;
  created_at: string;
}

export default function PortfolioPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPortfolios = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/portfolio/portfolios`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setPortfolios(json.data || []);
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
    fetchPortfolios();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("portfolio.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("portfolio.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/academic">
            {t("portfolio.breadcrumb-academic")}
          </Link>
          <Link color="inherit" to="/academic/evaluation">
            {t("portfolio.breadcrumb-evaluation")}
          </Link>
          <Typography variant="body2">{t("portfolio.breadcrumb-portfolio")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="portfolio tabs">
            <Tab label={t("portfolio.tab-portfolios")} />
            <Tab label={t("portfolio.tab-artifacts")} />
            <Tab label={t("portfolio.tab-evidence")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : portfolios.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {portfolios.map((portfolio) => (
                    <Card key={portfolio.id}>
                      <CardContent>
                        <Typography variant="h6" className="mb-2">
                          {portfolio.title}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" className="mb-2">
                          {portfolio.student_name}
                        </Typography>
                        <Typography variant="body2" className="mb-2">
                          {portfolio.description}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {portfolio.artifact_count} artefak
                        </Typography>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  {t("portfolio.no-portfolios")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("portfolio.artifacts-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("portfolio.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("portfolio.evidence-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("portfolio.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
