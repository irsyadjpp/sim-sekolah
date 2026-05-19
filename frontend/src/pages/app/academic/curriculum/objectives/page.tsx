import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useSearchParams } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Skeleton,
  Snackbar,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useConfirm } from "@/hooks/use-confirm";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiPlus from "@/icons/nexture/ni-plus";

interface LearningObjective {
  id: string;
  description: string;
}

export default function ObjectivesPage() {
  const { t } = useTranslation();
  const [searchParams] = useSearchParams();
  const cpId = searchParams.get("cpId");
  const confirm = useConfirm();

  const [objectives, setObjectives] = useState<LearningObjective[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newObjective, setNewObjective] = useState("");
  const [saving, setSaving] = useState(false);

  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: "success" | "error" }>({
    open: false,
    message: "",
    severity: "success",
  });

  const fetchData = async () => {
    if (!cpId) return;
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-outcomes/${cpId}/objectives`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setObjectives(json.data || []);
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
    fetchData();
  }, [cpId]);

  const handleAdd = async () => {
    if (!newObjective.trim() || !cpId) return;
    setSaving(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-outcomes/${cpId}/objectives`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ description: newObjective }),
      });
      const json = await res.json();
      if (json.status === "success") {
        // Optimistic UI Update
        setObjectives((prev) => [...prev, json.data]);
        setNewObjective("");
        setSnackbar({ open: true, message: t("tp-validation.add-success"), severity: "success" });
      } else {
        setSnackbar({ open: true, message: json.message, severity: "error" });
      }
    } catch (err: any) {
      setSnackbar({ open: true, message: err.message, severity: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!cpId) return;

    const isConfirmed = await confirm({
      title: t("tp-validation.confirm-delete-title"),
      message: t("tp-validation.confirm-delete-desc"),
      confirmText: t("tp-validation.confirm-btn-delete"),
      cancelText: t("tp-validation.confirm-btn-cancel"),
    });

    if (!isConfirmed) return;

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-outcomes/${cpId}/objectives/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        // Optimistic UI Update
        setObjectives((prev) => prev.filter((obj) => obj.id !== id));
        setSnackbar({ open: true, message: t("tp-validation.delete-success"), severity: "success" });
      } else {
        setSnackbar({ open: true, message: json.message, severity: "error" });
      }
    } catch (err: any) {
      setSnackbar({ open: true, message: err.message, severity: "error" });
    }
  };

  return (
    <Box>
      <Typography variant="h1" component="h1" className="mb-2">
        {t("tp-validation.title")}
      </Typography>
      <Breadcrumbs className="mb-6">
        <Link to="/home">{t("tp-validation.breadcrumb-home")}</Link>
        <Link to="/academic">{t("tp-validation.breadcrumb-academic")}</Link>
        <Link to="/academic/curriculum">{t("tp-validation.breadcrumb-curriculum")}</Link>
        <Typography variant="body2">{t("tp-validation.breadcrumb-tp")}</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Card className="mb-6">
        <CardContent className="flex gap-2">
          <TextField
            fullWidth
            size="small"
            placeholder={t("tp-validation.input-placeholder")}
            value={newObjective}
            onChange={(e) => setNewObjective(e.target.value)}
            disabled={saving}
          />
          <Button
            variant="contained"
            startIcon={saving ? <CircularProgress size={16} color="inherit" /> : <NiPlus size="small" />}
            onClick={handleAdd}
            disabled={saving || !newObjective.trim()}
          >
            {t("tp-validation.btn-add")}
          </Button>
        </CardContent>
      </Card>

      <Card>
        {loading ? (
          <List>
            {[1, 2, 3].map((item) => (
              <ListItem key={item} divider={item < 3}>
                <ListItemText primary={<Skeleton width="15%" />} secondary={<Skeleton width="80%" />} />
              </ListItem>
            ))}
          </List>
        ) : (
          <List>
            {objectives.length > 0 ? (
              objectives.map((obj, index) => (
                <ListItem
                  key={obj.id}
                  divider={index < objectives.length - 1}
                  secondaryAction={
                    <IconButton edge="end" color="error" onClick={() => handleDelete(obj.id)}>
                      <NiBinEmpty size="small" />
                    </IconButton>
                  }
                >
                  <ListItemText
                    primary={`TP.${index + 1}`}
                    secondary={obj.description}
                    primaryTypographyProps={{ variant: "caption", color: "textSecondary", className: "font-bold" }}
                    secondaryTypographyProps={{ variant: "body1", color: "textPrimary", className: "mt-1" }}
                  />
                </ListItem>
              ))
            ) : (
              <Box className="py-10 text-center text-gray-500 italic">{t("tp-validation.list-empty")}</Box>
            )}
          </List>
        )}
      </Card>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          variant="filled"
          sx={{ borderRadius: 2, fontWeight: 500 }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
