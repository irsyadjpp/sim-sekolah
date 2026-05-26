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

interface StudentGrowth {
  id: string;
  student_id: string;
  student_name?: string;
  period: string;
  period_name?: string;
  academic_year_id: string;
  academic_year?: string;
  overall_score: number;
  mastery_rate: number;
  growth_rate: number;
  percentile: number;
  teacher_id: string;
  teacher_name?: string;
  notes: string;
  created_at: string;
}

export default function StudentGrowthPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [growthData, setGrowthData] = useState<StudentGrowth[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchGrowthData = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      // Try to get numeracy growth data as example
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/numeracy/growths`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setGrowthData(json.data || []);
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
    fetchGrowthData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getPeriodLabel = (period: string) => {
    const labels: Record<string, string> = {
      SEMESTER_1: "Semester 1",
      SEMESTER_2: "Semester 2",
    };
    return labels[period] || period;
  };

  const getGrowthTrend = (growthRate: number) => {
    if (growthRate > 0) return { label: "Naik", color: "success" as const };
    if (growthRate < 0) return { label: "Turun", color: "error" as const };
    return { label: "Stabil", color: "info" as const };
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("growth.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("growth.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/students">
            {t("growth.breadcrumb-students")}
          </Link>
          <Typography variant="body2">{t("growth.breadcrumb-growth")}</Typography>
        </Breadcrumbs>
      </Box>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="growth tabs">
            <Tab label={t("growth.tab-overview")} />
            <Tab label={t("growth.tab-competency")} />
            <Tab label={t("growth.tab-comparison")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
                <Typography variant="h6">{t("growth.growth-overview")}</Typography>
                <Button variant="contained" color="primary">
                  {t("growth.generate-report")}
                </Button>
              </Box>

              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : error ? (
                <Alert severity="error">{error}</Alert>
              ) : growthData.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {growthData.map((growth) => {
                    const trend = getGrowthTrend(growth.growth_rate);
                    return (
                      <Card key={growth.id} className="transition-shadow hover:shadow-lg">
                        <CardContent>
                          <Box display="flex" justifyContent="space-between" alignItems="start" className="mb-2">
                            <Typography variant="h6" className="mb-0">
                              {growth.student_name || "Student"}
                            </Typography>
                            <Chip label={trend.label} size="small" color={trend.color} />
                          </Box>
                          <Box className="space-y-1">
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("growth.period")}: {getPeriodLabel(growth.period)}
                            </Typography>
                            {growth.academic_year && (
                              <Typography variant="caption" display="block" color="textSecondary">
                                {t("growth.academic-year")}: {growth.academic_year}
                              </Typography>
                            )}
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("growth.overall-score")}: {growth.overall_score.toFixed(1)}
                            </Typography>
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("growth.mastery-rate")}: {growth.mastery_rate.toFixed(1)}%
                            </Typography>
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("growth.growth-rate")}: {growth.growth_rate > 0 ? "+" : ""}
                              {growth.growth_rate.toFixed(1)}%
                            </Typography>
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("growth.percentile")}: {growth.percentile}th
                            </Typography>
                          </Box>
                        </CardContent>
                      </Card>
                    );
                  })}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center" className="py-10">
                  {t("growth.no-growth-data")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("growth.competency-progression")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("growth.competency-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("growth.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("growth.comparison-analysis")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("growth.comparison-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("growth.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
