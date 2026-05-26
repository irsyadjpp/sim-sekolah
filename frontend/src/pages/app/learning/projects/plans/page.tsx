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
  LinearProgress,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

interface P5Project {
  id: string;
  title: string;
  description: string;
  subject_id: string;
  subject_name?: string;
  classroom_id: string;
  classroom_name?: string;
  project_theme: string;
  academic_year_id: string;
  semester: number;
  start_date: string;
  end_date: string;
  total_weeks: number;
  project_type: string;
  max_team_size: number;
  status: string;
  progress: number;
  teams_count: number;
  milestones_count: number;
  created_at: string;
}

export default function P5ProjectsPage() {
  const { t } = useTranslation();
  const [projects, setProjects] = useState<P5Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/p5/projects`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setProjects(json.data || []);
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
    fetchProjects();
  }, []);

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      PERENCANAAN: "Perencanaan",
      BERJALAN: "Berjalan",
      DIHENTIKAN: "Dihentikan",
      SELESAI: "Selesai",
      DIBATALKAN: "Dibatalkan",
    };
    return labels[status] || status;
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, any> = {
      PERENCANAAN: "info",
      BERJALAN: "primary",
      DIHENTIKAN: "warning",
      SELESAI: "success",
      DIBATALKAN: "error",
    };
    return colors[status] || "default";
  };

  const getProjectTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      INDIVIDU: "Individu",
      KELOMPOK: "Kelompok",
      KELAS: "Kelas",
    };
    return labels[type] || type;
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("p5.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("p5.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/learning">
            {t("p5.breadcrumb-learning")}
          </Link>
          <Link color="inherit" to="/learning/projects">
            {t("p5.breadcrumb-projects")}
          </Link>
          <Typography variant="body2">{t("p5.breadcrumb-plans")}</Typography>
        </Breadcrumbs>
      </Box>

      <Box display="flex" justifyContent="space-between" alignItems="center" className="mb-4">
        <Typography variant="h6">{t("p5.manage-projects")}</Typography>
        <Button variant="contained" color="primary">
          {t("p5.create-project")}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      {loading ? (
        <Box display="flex" justifyContent="center" className="py-10">
          <CircularProgress size={24} />
        </Box>
      ) : projects.length > 0 ? (
        <Box className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <Card key={project.id} className="transition-shadow hover:shadow-lg">
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="start" className="mb-2">
                  <Typography variant="h6" className="mb-0">
                    {project.title}
                  </Typography>
                  <Chip label={getStatusLabel(project.status)} size="small" color={getStatusColor(project.status)} />
                </Box>
                {project.description && (
                  <Typography variant="body2" color="textSecondary" className="mb-2">
                    {project.description}
                  </Typography>
                )}
                <Box className="space-y-1">
                  <Typography variant="caption" display="block" color="textSecondary">
                    {t("p5.theme")}: {project.project_theme}
                  </Typography>
                  {project.subject_name && (
                    <Typography variant="caption" display="block" color="textSecondary">
                      {t("p5.subject")}: {project.subject_name}
                    </Typography>
                  )}
                  {project.classroom_name && (
                    <Typography variant="caption" display="block" color="textSecondary">
                      {t("p5.classroom")}: {project.classroom_name}
                    </Typography>
                  )}
                  <Typography variant="caption" display="block" color="textSecondary">
                    {t("p5.type")}: {getProjectTypeLabel(project.project_type)}
                  </Typography>
                  {project.start_date && (
                    <Typography variant="caption" display="block" color="textSecondary">
                      {t("p5.duration")}: {project.total_weeks} minggu
                    </Typography>
                  )}
                  <Typography variant="caption" display="block" color="textSecondary">
                    {t("p5.teams")}: {project.teams_count}
                  </Typography>
                  <Typography variant="caption" display="block" color="textSecondary">
                    {t("p5.milestones")}: {project.milestones_count}
                  </Typography>
                </Box>
                <Box className="mt-3">
                  <Box display="flex" justifyContent="space-between" className="mb-1">
                    <Typography variant="caption">{t("p5.progress")}</Typography>
                    <Typography variant="caption">{project.progress}%</Typography>
                  </Box>
                  <LinearProgress variant="determinate" value={project.progress} />
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      ) : (
        <Typography variant="body2" color="textSecondary" align="center" className="py-10">
          {t("p5.no-projects")}
        </Typography>
      )}
    </Box>
  );
}
