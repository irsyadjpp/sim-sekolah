import React, { useEffect, useState } from "react";
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Button,
  Breadcrumbs,
  Link,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { DEFAULTS } from "@/config";
import { cn } from "@/lib/utils";
import StrategicPlanningErrorBoundary from "@/components/strategic-planning/StrategicPlanningErrorBoundary";
import SPCard from "@/components/strategic-planning/SPCard";
import SPLoading from "@/components/strategic-planning/SPLoading";
import PermissionGuard from "@/components/strategic-planning/PermissionGuard";
import PollIcon from "@mui/icons-material/Poll";
import BarChartIcon from "@mui/icons-material/BarChart";
import GroupsIcon from "@mui/icons-material/Groups";
import ChecklistIcon from "@mui/icons-material/Checklist";
import PsychologyIcon from "@mui/icons-material/Psychology";
import TimelineIcon from "@mui/icons-material/Timeline";
import SchoolIcon from "@mui/icons-material/School";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";

// Dashboard Statistics Interface
interface DashboardStats {
  totalSurveys: number;
  activeFGDSessions: number;
  swotAnalyses: number;
  rootCauseAnalyses: number;
  studentProfiles: number;
  kspIntegrations: number;
}

// Phase Progress Interface
interface PhaseProgress {
  phase: string;
  name: string;
  progress: number;
  status: "completed" | "in-progress" | "pending";
}

// Recent Activity Interface
interface RecentActivity {
  id: string;
  type: string;
  description: string;
  timestamp: string;
}

// Dashboard Component
const StrategicPlanningDashboardContent: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [stats, setStats] = useState<DashboardStats>({
    totalSurveys: 0,
    activeFGDSessions: 0,
    swotAnalyses: 0,
    rootCauseAnalyses: 0,
    studentProfiles: 0,
    kspIntegrations: 0,
  });

  const [phaseProgress] = useState<PhaseProgress[]>([
    { phase: "1", name: "Database Setup & Backend Foundation", progress: 100, status: "completed" },
    { phase: "2", name: "Frontend Foundation & Navigation", progress: 84, status: "in-progress" },
    { phase: "3", name: "FR 1 - Modul Pengumpulan Data Digital", progress: 0, status: "pending" },
    { phase: "4", name: "FR 3 - Alat Analisis", progress: 0, status: "pending" },
    { phase: "5", name: "FR 2.2 - Profiling Kebutuhan Murid", progress: 0, status: "pending" },
    { phase: "6", name: "FR 4 - KSP Enhanced Generator", progress: 0, status: "pending" },
  ]);

  const [recentActivities] = useState<RecentActivity[]>([
    {
      id: "1",
      type: "system",
      description: "Backend API berhasil diimplementasikan untuk semua modul",
      timestamp: "2 jam yang lalu",
    },
    {
      id: "2",
      type: "system",
      description: "Database migration selesai untuk 18 tabel",
      timestamp: "1 hari yang lalu",
    },
    {
      id: "3",
      type: "system",
      description: "Fase 1 (Backend Foundation) selesai 100%",
      timestamp: "1 hari yang lalu",
    },
  ]);

  useEffect(() => {
    // Simulate loading initial data
    const loadDashboardData = async () => {
      try {
        setLoading(true);

        // Simulate API calls with mock data for now
        // In production, this would be actual API calls using the existing pattern
        await new Promise(resolve => setTimeout(resolve, 1000));

        setStats({
          totalSurveys: 0,
          activeFGDSessions: 0,
          swotAnalyses: 0,
          rootCauseAnalyses: 0,
          studentProfiles: 0,
          kspIntegrations: 0,
        });
      } catch (err: any) {
        setError(err.message || "Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "success";
      case "in-progress":
        return "warning";
      default:
        return "default";
    }
  };

  const quickAccessCards = [
    {
      title: "Kuesioner Digital",
      description: "Buat dan kelola kuesioner untuk pengumpulan data",
      icon: <PollIcon sx={{ fontSize: 32 }} className="text-primary" />,
      path: "/strategic-planning/data-collection/surveys",
      count: stats.totalSurveys,
      label: "Total Survey",
    },
    {
      title: "Integrasi Rapor",
      description: "Integrasi data rapor pendidikan dari Kemdikbud",
      icon: <BarChartIcon sx={{ fontSize: 32 }} className="text-secondary" />,
      path: "/strategic-planning/data-collection/rapor-integration",
      count: 0,
      label: "Data Import",
    },
    {
      title: "FGD Digital",
      description: "Kelola sesi Focus Group Discussion",
      icon: <GroupsIcon sx={{ fontSize: 32 }} className="text-info" />,
      path: "/strategic-planning/data-collection/fgd",
      count: stats.activeFGDSessions,
      label: "Sesi Aktif",
    },
    {
      title: "Analisis SWOT",
      description: "Analisis Strengths, Weaknesses, Opportunities, Threats",
      icon: <ChecklistIcon sx={{ fontSize: 32 }} className="text-success" />,
      path: "/strategic-planning/analysis/swot",
      count: stats.swotAnalyses,
      label: "Analisis",
    },
    {
      title: "Root Cause",
      description: "Identifikasi akar masalah dengan metode sistematis",
      icon: <PsychologyIcon sx={{ fontSize: 32 }} className="text-warning" />,
      path: "/strategic-planning/analysis/root-cause",
      count: stats.rootCauseAnalyses,
      label: "Analisis",
    },
    {
      title: "Fishbone",
      description: "Visualisasi sebab-akibat dengan diagram Ishikawa",
      icon: <TimelineIcon sx={{ fontSize: 32 }} className="text-error" />,
      path: "/strategic-planning/analysis/fishbone",
      count: 0,
      label: "Diagram",
    },
    {
      title: "Profiling Murid",
      description: "Profil kebutuhan murid yang ditingkatkan",
      icon: <SchoolIcon sx={{ fontSize: 32 }} className="text-purple" />,
      path: "/strategic-planning/student-needs",
      count: stats.studentProfiles,
      label: "Profil",
    },
    {
      title: "KSP Enhanced",
      description: "Generator KSP dengan integrasi analisis",
      icon: <TrendingUpIcon sx={{ fontSize: 32 }} className="text-teal" />,
      path: "/strategic-planning/ksp-enhanced",
      count: stats.kspIntegrations,
      label: "Integrasi",
    },
  ];

  if (loading) {
    return <SPLoading message="Memuat dashboard..." fullScreen />;
  }

  return (
    <Container maxWidth="xl" className="py-4">
      {/* Header */}
      <Box className="mb-4">
        <Typography variant="h4" component="h1" className="mb-2">
          Perencanaan Strategis Sekolah
        </Typography>
        <Typography variant="body1" className="text-text-secondary">
          Dashboard berbasis data untuk perencanaan strategis dan penyusunan Kurikulum Satuan Pendidikan (KSP)
        </Typography>
      </Box>

      {/* Breadcrumbs */}
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Typography variant="body2">Perencanaan Strategis</Typography>
      </Breadcrumbs>

      {error && (
        <Box className="mb-4 p-4 bg-error-light rounded-lg">
          <Typography variant="body2" className="text-error">{error}</Typography>
        </Box>
      )}

      {/* Statistics Overview */}
      <Grid container spacing={3} className="mb-4">
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box className="flex items-center justify-between">
                <Box>
                  <Typography variant="h6" className="text-text-secondary">
                    Total Survey
                  </Typography>
                  <Typography variant="h4">{stats.totalSurveys}</Typography>
                </Box>
                <PollIcon sx={{ fontSize: 32 }} className="text-primary opacity-30" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box className="flex items-center justify-between">
                <Box>
                  <Typography variant="h6" className="text-text-secondary">
                    FGD Aktif
                  </Typography>
                  <Typography variant="h4">{stats.activeFGDSessions}</Typography>
                </Box>
                <GroupsIcon sx={{ fontSize: 32 }} className="text-info opacity-30" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box className="flex items-center justify-between">
                <Box>
                  <Typography variant="h6" className="text-text-secondary">
                    Analisis SWOT
                  </Typography>
                  <Typography variant="h4">{stats.swotAnalyses}</Typography>
                </Box>
                <ChecklistIcon sx={{ fontSize: 32 }} className="text-success opacity-30" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box className="flex items-center justify-between">
                <Box>
                  <Typography variant="h6" className="text-text-secondary">
                    Profil Murid
                  </Typography>
                  <Typography variant="h4">{stats.studentProfiles}</Typography>
                </Box>
                <SchoolIcon sx={{ fontSize: 32 }} className="text-purple opacity-30" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Access Cards */}
      <Typography variant="h5" component="h2" className="mb-2">
        Akses Cepat
      </Typography>
      <Grid container spacing={3} className="mb-4">
        {quickAccessCards.map((card, index) => (
          <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={index}>
            <SPCard
              title={card.title}
              subtitle={card.count > 0 ? `${card.label}: ${card.count}` : card.label}
              onClick={() => navigate(card.path)}
              hover
              elevation={2}
            >
              <Box className="flex justify-center mb-2">
                {card.icon}
              </Box>
              <Typography variant="body2" className="text-text-secondary text-center">
                {card.description}
              </Typography>
            </SPCard>
          </Grid>
        ))}
      </Grid>

      {/* Phase Progress */}
      <Typography variant="h5" component="h2" className="mb-2">
        Progress Implementasi
      </Typography>
      <Card className="mb-4">
        <CardContent>
          {phaseProgress.map((phase) => (
            <Box key={phase.phase} className="mb-2">
              <Box className="flex justify-between mb-1">
                <Typography variant="body2">
                  Fase {phase.phase}: {phase.name}
                </Typography>
                <Box className="flex items-center gap-1">
                  <Typography variant="body2">{phase.progress}%</Typography>
                  <Chip
                    label={phase.status === "completed" ? "Selesai" : phase.status === "in-progress" ? "Dalam Progres" : "Pending"}
                    size="small"
                    color={getStatusColor(phase.status) as any}
                  />
                </Box>
              </Box>
              <LinearProgress
                variant="determinate"
                value={phase.progress}
                className="h-2 rounded-full"
              />
            </Box>
          ))}
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Typography variant="h5" component="h2" className="mb-2">
        Aktivitas Terbaru
      </Typography>
      <Card>
        <CardContent>
          {recentActivities.length === 0 ? (
            <Typography variant="body2" className="text-text-secondary text-center py-2">
              Belum ada aktivitas terbaru
            </Typography>
          ) : (
            <Box>
              {recentActivities.map((activity) => (
                <Box
                  key={activity.id}
                  className="flex items-center py-2 border-b border-line last:border-0"
                >
                  <Box className="w-2 h-2 rounded-full bg-primary mr-2" />
                  <Box className="flex-grow">
                    <Typography variant="body2">{activity.description}</Typography>
                    <Typography variant="caption" className="text-text-secondary">
                      {activity.timestamp}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};

// Main Page Component with Providers
const StrategicPlanningPage: React.FC = () => {
  return (
    <StrategicPlanningErrorBoundary>
      <PermissionGuard
        allowedRoles={["ADMIN", "KEPALA_SEKOLAH", "GURU", "OPERATOR", "WALI_KELAS"]}
      >
        <StrategicPlanningDashboardContent />
      </PermissionGuard>
    </StrategicPlanningErrorBoundary>
  );
};

export default StrategicPlanningPage;