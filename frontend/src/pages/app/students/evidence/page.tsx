import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
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

interface LearningEvidence {
  id: string;
  student_id: string;
  student_name?: string;
  artifact_id: string;
  artifact_title?: string;
  competency_id: string;
  competency_type: string;
  evidence_date: string;
  mastery_level: string;
  teacher_id: string;
  teacher_name?: string;
  validation_status: string;
  validation_notes: string;
  created_at: string;
}

export default function LearningEvidencePage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [evidence, setEvidence] = useState<LearningEvidence[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchEvidence = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-evidence`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setEvidence(json.data || []);
      }
    } catch (err: any) {
      console.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvidence();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getCompetencyTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      CP: "Capaian Pembelajaran",
      TP: "Tujuan Pembelajaran",
      PROJECT: "Proyek",
    };
    return labels[type] || type;
  };

  const getMasteryLevelLabel = (level: string) => {
    const labels: Record<string, string> = {
      BELUM: "Belum",
      SEDANG: "Sedang",
      MENGUASAI: "Menguasai",
    };
    return labels[level] || level;
  };

  const getValidationStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      PENDING: "Menunggu",
      APPROVED: "Disetujui",
      REJECTED: "Ditolak",
    };
    return labels[status] || status;
  };

  const getValidationStatusColor = (status: string) => {
    const colors: Record<string, any> = {
      PENDING: "warning",
      APPROVED: "success",
      REJECTED: "error",
    };
    return colors[status] || "default";
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("evidence.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("evidence.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/students">
            {t("evidence.breadcrumb-students")}
          </Link>
          <Typography variant="body2">{t("evidence.breadcrumb-evidence")}</Typography>
        </Breadcrumbs>
      </Box>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="evidence tabs">
            <Tab label={t("evidence.tab-evidence")} />
            <Tab label={t("evidence.tab-validation")} />
            <Tab label={t("evidence.tab-analytics")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
                <Typography variant="h6">{t("evidence.manage-evidence")}</Typography>
                <Button variant="contained" color="primary">
                  {t("evidence.create-evidence")}
                </Button>
              </Box>

              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : evidence.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {evidence.map((item) => (
                    <Card key={item.id} className="transition-shadow hover:shadow-lg">
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="start" className="mb-2">
                          <Typography variant="h6" className="mb-0">
                            {item.artifact_title || "Evidence"}
                          </Typography>
                          <Chip
                            label={getValidationStatusLabel(item.validation_status)}
                            size="small"
                            color={getValidationStatusColor(item.validation_status)}
                          />
                        </Box>
                        <Box className="space-y-1">
                          {item.student_name && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("evidence.student")}: {item.student_name}
                            </Typography>
                          )}
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("evidence.competency-type")}: {getCompetencyTypeLabel(item.competency_type)}
                          </Typography>
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("evidence.evidence-date")}: {new Date(item.evidence_date).toLocaleDateString("id-ID")}
                          </Typography>
                          <Typography variant="caption" display="block" color="textSecondary">
                            {t("evidence.mastery-level")}: {getMasteryLevelLabel(item.mastery_level)}
                          </Typography>
                          {item.teacher_name && (
                            <Typography variant="caption" display="block" color="textSecondary">
                              {t("evidence.teacher")}: {item.teacher_name}
                            </Typography>
                          )}
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center" className="py-10">
                  {t("evidence.no-evidence")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("evidence.validation-queue")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("evidence.validation-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("evidence.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("evidence.evidence-analytics")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("evidence.analytics-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("evidence.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
