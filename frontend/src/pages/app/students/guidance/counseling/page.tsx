/* eslint-disable @typescript-eslint/no-unused-vars, no-empty */
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
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSettings from "@/icons/nexture/ni-settings";

interface Classroom {
  id: string;
  classroom_name: string;
}

interface Enrollment {
  id: string;
  student: {
    id: string;
    full_name: string;
    nisn: string;
  };
}

interface EWSAlert {
  id: string;
  student_id: string;
  classroom_id: string;
  alert_type: string; // LITERACY_DELAY, ATTENDANCE_DROP, BEHAVIORAL_CONCERN
  severity_level: string; // LOW, MEDIUM, HIGH
  trigger_reason: string;
  status: string; // OPEN, INTERVENED, RESOLVED
  intervention_notes: string;
  detected_at: string;
}

interface ObservationTag {
  id: string;
  category: string;
  tag_name: string;
  sentiment: string;
}

export default function CounselingPage() {
  const { t } = useTranslation();
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [selectedClassroom, setSelectedClassroom] = useState<string>("");
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [alerts, setAlerts] = useState<EWSAlert[]>([]);
  const [tags, setTags] = useState<ObservationTag[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal States
  const [openInterventionDialog, setOpenInterventionDialog] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState<EWSAlert | null>(null);
  const [interventionNotes, setInterventionNotes] = useState("");
  const [interventionStatus, setInterventionStatus] = useState("RESOLVED");

  const [openObservationDialog, setOpenObservationDialog] = useState(false);
  const [obsStudent, setObsStudent] = useState("");
  const [obsContext, setObsContext] = useState("");
  const [obsNotes, setObsNotes] = useState("");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const token = localStorage.getItem("accessToken");

  const fetchClassrooms = async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setClassrooms(json.data);
        if (json.data.length > 0) {
          setSelectedClassroom(json.data[0].id);
        }
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchClassroomDetails = async (classId: string) => {
    if (!classId) return;
    try {
      setLoading(true);
      // Fetch enrollments
      const resEnr = await fetch(`${DEFAULTS.API_URL}/api/v1/classrooms/${classId}/enrollments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const jsonEnr = await resEnr.json();
      setEnrollments(jsonEnr.data || []);

      // Fetch EWS alerts
      const resAlerts = await fetch(`${DEFAULTS.API_URL}/api/v1/intelligence/alerts?classroom_id=${classId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const jsonAlerts = await resAlerts.json();
      setAlerts(jsonAlerts.data || []);
    } catch (err: any) {
      setError("Gagal menarik detail kelas");
    } finally {
      setLoading(false);
    }
  };

  const fetchTags = async () => {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intelligence/observation-tags`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      setTags(json.data || []);
    } catch (err) {}
  };

  useEffect(() => {
    fetchClassrooms();
    fetchTags();
  }, []);

  useEffect(() => {
    if (selectedClassroom) {
      fetchClassroomDetails(selectedClassroom);
    }
  }, [selectedClassroom]);

  const handleTriggerCron = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intelligence/alerts/trigger-cron`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        fetchClassroomDetails(selectedClassroom);
      }
    } catch (err) {
      setError("Gagal memicu cron analitik");
    } finally {
      setLoading(false);
    }
  };

  const handleInterventionSubmit = async () => {
    if (!selectedAlert) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intelligence/alerts/${selectedAlert.id}/intervene`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: interventionStatus,
          intervention_notes: interventionNotes,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenInterventionDialog(false);
        setInterventionNotes("");
        fetchClassroomDetails(selectedClassroom);
      }
    } catch (err) {
      setError("Gagal merekam intervensi");
    }
  };

  const handleObservationSubmit = async () => {
    if (!obsStudent || !obsNotes) return;
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/intelligence/anecdotal`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          student_id: obsStudent,
          context_activity: obsContext,
          notes: obsNotes,
          tag_ids: selectedTags,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenObservationDialog(false);
        setObsStudent("");
        setObsContext("");
        setObsNotes("");
        setSelectedTags([]);
        fetchClassroomDetails(selectedClassroom);
      }
    } catch (err) {
      setError("Gagal mengirim jurnal observasi anekdotal");
    }
  };

  const toggleTagSelection = (tagId: string) => {
    setSelectedTags((prev) => (prev.includes(tagId) ? prev.filter((id) => id !== tagId) : [...prev, tagId]));
  };

  const getStudentName = (studentId: string) => {
    const enr = enrollments.find((e) => e.student.id === studentId);
    return enr ? enr.student.full_name : t("counseling.unknown-student", "Siswa Tidak Dikenal");
  };

  return (
    <Box className="pb-10">
      <Grid container spacing={3} className="mb-6 items-center justify-between">
        <Grid size={{ xs: 12, md: 8 }}>
          <Typography variant="h1" component="h1" className="mb-0">
            {t("counseling.title")}
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home">
              {t("staff-form.breadcrumb-home")}
            </Link>
            <Typography variant="body2" className="text-text-secondary">
              {t("counseling.description")}
            </Typography>
          </Breadcrumbs>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }} className="flex justify-end gap-3">
          <Button
            variant="outlined"
            startIcon={<NiSettings size="small" />}
            onClick={handleTriggerCron}
            className="rounded-xl border-slate-200 bg-white"
          >
            {t("counseling.trigger-analytics")}
          </Button>
          <Button
            variant="contained"
            startIcon={<NiPlus size="small" />}
            onClick={() => setOpenObservationDialog(true)}
            className="rounded-xl"
          >
            {t("counseling.new-anecdotal")}
          </Button>
        </Grid>
      </Grid>

      {error && (
        <Alert severity="error" className="mb-6 rounded-2xl font-bold">
          {error}
        </Alert>
      )}

      {/* Classroom Filter Card */}
      <Card className="mb-8 rounded-3xl border-none shadow-sm">
        <CardContent className="p-6">
          <Grid container spacing={3} className="items-center">
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth size="small">
                <InputLabel>{t("counseling.select-classroom")}</InputLabel>
                <Select
                  value={selectedClassroom}
                  label={t("counseling.select-classroom")}
                  onChange={(e) => setSelectedClassroom(e.target.value)}
                >
                  {classrooms.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.classroom_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {loading ? (
        <Box className="flex justify-center py-20">
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={4}>
          {/* EWS alerts section */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Typography variant="h4" className="mb-4 font-black text-slate-800">
              {t("counseling.ews-alerts")}
            </Typography>
            {alerts.length === 0 ? (
              <Paper className="rounded-3xl border border-dashed border-slate-200 p-10 text-center text-slate-400">
                {t("counseling.no-alerts")}
              </Paper>
            ) : (
              <Box className="space-y-4">
                {alerts.map((alert) => (
                  <Card
                    key={alert.id}
                    className="rounded-3xl border border-slate-100 shadow-sm transition-all duration-300 hover:shadow-md"
                  >
                    <CardContent className="p-6">
                      <Box className="flex items-start justify-between">
                        <Box>
                          <Typography variant="h6" className="font-bold text-slate-900">
                            {getStudentName(alert.student_id)}
                          </Typography>
                          <Typography variant="body2" className="mb-3 font-mono text-xs text-slate-500">
                            {t("counseling.status")}: {alert.alert_type}
                          </Typography>
                        </Box>
                        <Chip
                          label={alert.severity_level}
                          color={
                            alert.severity_level === "HIGH"
                              ? "error"
                              : alert.severity_level === "MEDIUM"
                                ? "warning"
                                : "info"
                          }
                          size="small"
                          className="rounded-lg font-bold"
                        />
                      </Box>
                      <Typography
                        variant="body2"
                        className="mb-4 rounded-2xl border border-slate-100/50 bg-slate-50 p-4 text-slate-600"
                      >
                        {alert.trigger_reason}
                      </Typography>
                      <Box className="flex items-center justify-between">
                        <Chip
                          label={alert.status}
                          variant="outlined"
                          color={alert.status === "OPEN" ? "error" : "success"}
                          size="small"
                        />
                        {alert.status === "OPEN" && (
                          <Button
                            variant="text"
                            size="small"
                            onClick={() => {
                              setSelectedAlert(alert);
                              setOpenInterventionDialog(true);
                            }}
                            className="font-bold"
                          >
                            {t("counseling.record-intervention")}
                          </Button>
                        )}
                      </Box>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            )}
          </Grid>

          {/* Student baseline / style info section */}
          <Grid size={{ xs: 12, md: 6 }}>
            <Typography variant="h4" className="mb-4 font-black text-slate-800">
              {t("counseling.baseline-title")}
            </Typography>
            <Paper className="rounded-3xl border border-slate-100 p-6 shadow-sm">
              <Typography variant="body2" className="mb-4 text-slate-500">
                {t("counseling.baseline-desc")}
              </Typography>
              <Box className="space-y-4">
                {enrollments.map((enr) => (
                  <Box
                    key={enr.id}
                    className="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0 last:pb-0"
                  >
                    <Box>
                      <Typography variant="body1" className="font-bold text-slate-800">
                        {enr.student.full_name}
                      </Typography>
                      <Typography variant="body2" className="text-xs text-slate-400">
                        NISN: {enr.student.nisn}
                      </Typography>
                    </Box>
                    <Button
                      component={Link}
                      to={`/students/details?id=${enr.student.id}`}
                      variant="text"
                      size="small"
                      className="text-xs font-bold"
                    >
                      {t("counseling.view-profile-360")}
                    </Button>
                  </Box>
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* Intervention Dialog */}
      <Dialog open={openInterventionDialog} onClose={() => setOpenInterventionDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle className="font-bold">{t("counseling.intervention-dialog-title")}</DialogTitle>
        <DialogContent className="pt-2">
          <Typography variant="body2" className="mb-4 text-slate-500">
            {t("counseling.intervention-dialog-desc")}
          </Typography>
          <Grid container spacing={3}>
            <Grid size={{ xs: 12 }}>
              <FormControl fullWidth size="small">
                <InputLabel>{t("counseling.intervention-status-label")}</InputLabel>
                <Select
                  value={interventionStatus}
                  label={t("counseling.intervention-status-label")}
                  onChange={(e) => setInterventionStatus(e.target.value)}
                >
                  <MenuItem value="INTERVENED">{t("counseling.status-intervened")}</MenuItem>
                  <MenuItem value="RESOLVED">{t("counseling.status-resolved")}</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label={t("counseling.intervention-notes-label")}
                value={interventionNotes}
                onChange={(e) => setInterventionNotes(e.target.value)}
                required
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions className="p-4">
          <Button onClick={() => setOpenInterventionDialog(false)} color="inherit" className="font-bold">
            {t("counseling.button-cancel")}
          </Button>
          <Button
            onClick={handleInterventionSubmit}
            color="primary"
            variant="contained"
            className="rounded-xl font-bold shadow-md"
            disabled={!interventionNotes}
          >
            {t("counseling.button-save-intervention")}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Anecdotal Observation Dialog */}
      <Dialog open={openObservationDialog} onClose={() => setOpenObservationDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle className="font-bold">{t("counseling.anecdotal-dialog-title")}</DialogTitle>
        <DialogContent className="pt-2">
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth size="small">
                <InputLabel>{t("counseling.select-student")}</InputLabel>
                <Select
                  value={obsStudent}
                  label={t("counseling.select-student")}
                  onChange={(e) => setObsStudent(e.target.value)}
                >
                  {enrollments.map((enr) => (
                    <MenuItem key={enr.student.id} value={enr.student.id}>
                      {enr.student.full_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                size="small"
                label={t("counseling.context-activity")}
                value={obsContext}
                onChange={(e) => setObsContext(e.target.value)}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label={t("counseling.observation-notes")}
                value={obsNotes}
                onChange={(e) => setObsNotes(e.target.value)}
                required
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <Typography variant="body2" className="mb-2 font-bold text-slate-700">
                {t("counseling.behavior-tags")}
              </Typography>
              <Box className="flex flex-wrap gap-2">
                {tags.map((tag) => {
                  const isSelected = selectedTags.includes(tag.id);
                  return (
                    <Chip
                      key={tag.id}
                      label={`${tag.tag_name} (${tag.sentiment})`}
                      onClick={() => toggleTagSelection(tag.id)}
                      color={isSelected ? (tag.sentiment === "POSITIVE" ? "success" : "error") : "default"}
                      variant={isSelected ? "filled" : "outlined"}
                      className="cursor-pointer"
                    />
                  );
                })}
              </Box>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions className="p-4">
          <Button onClick={() => setOpenObservationDialog(false)} color="inherit" className="font-bold">
            {t("counseling.button-cancel")}
          </Button>
          <Button
            onClick={handleObservationSubmit}
            color="primary"
            variant="contained"
            className="rounded-xl font-bold shadow-md"
            disabled={!obsStudent || !obsNotes}
          >
            {t("counseling.button-save-journal")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
