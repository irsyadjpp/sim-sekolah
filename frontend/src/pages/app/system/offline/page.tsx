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

interface SyncStatus {
  is_online: boolean;
  last_sync: string;
  pending_changes: number;
  sync_progress: number;
  conflicted_items: number;
}

export default function OfflinePage() {
  const { t } = useTranslation();
  const [syncStatus, setSyncStatus] = useState<SyncStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSyncStatus = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/offline/sync-status`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setSyncStatus(json.data);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async () => {
    setSyncing(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/offline/sync`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        await fetchSyncStatus();
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSyncing(false);
    }
  };

  useEffect(() => {
    fetchSyncStatus();
    // Check online status
    const handleOnline = () => {
      setSyncStatus((prev) => (prev ? { ...prev, is_online: true } : prev));
    };
    const handleOffline = () => {
      setSyncStatus((prev) => (prev ? { ...prev, is_online: false } : prev));
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("offline.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("offline.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/system">
            {t("offline.breadcrumb-system")}
          </Link>
          <Typography variant="body2">{t("offline.breadcrumb-offline")}</Typography>
        </Breadcrumbs>
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
      ) : (
        <Box className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                {t("offline.sync-status")}
              </Typography>
              <Box className="mb-4">
                <Chip
                  label={syncStatus?.is_online ? t("offline.online") : t("offline.offline")}
                  color={syncStatus?.is_online ? "success" : "error"}
                  className="mb-2"
                />
                {syncing && (
                  <Box className="mt-2">
                    <LinearProgress variant="indeterminate" />
                    <Typography variant="caption" display="block" className="mt-1">
                      {t("offline.syncing")}
                    </Typography>
                  </Box>
                )}
              </Box>
              <Box className="space-y-2">
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2">{t("offline.last-sync")}:</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {syncStatus?.last_sync
                      ? new Date(syncStatus.last_sync).toLocaleString("id-ID")
                      : t("offline.never")}
                  </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2">{t("offline.pending-changes")}:</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {syncStatus?.pending_changes || 0}
                  </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2">{t("offline.conflicted-items")}:</Typography>
                  <Typography variant="body2" fontWeight="bold" color="error">
                    {syncStatus?.conflicted_items || 0}
                  </Typography>
                </Box>
              </Box>
              <Button
                variant="contained"
                fullWidth
                className="mt-4"
                onClick={handleSync}
                disabled={!syncStatus?.is_online || syncing}
              >
                {syncing ? t("offline.syncing") : t("offline.sync-now")}
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                {t("offline.sync-queue")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mb-4">
                {t("offline.sync-queue-description")}
              </Typography>
              {syncStatus && syncStatus.pending_changes > 0 ? (
                <Alert severity="info" className="mb-2">
                  {t("offline.pending-items", { count: syncStatus.pending_changes })}
                </Alert>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  {t("offline.no-pending-items")}
                </Typography>
              )}
              {syncStatus && syncStatus.conflicted_items > 0 && (
                <Alert severity="warning" className="mt-2">
                  {t("offline.conflict-warning", { count: syncStatus.conflicted_items })}
                </Alert>
              )}
            </CardContent>
          </Card>

          <Card className="md:col-span-2">
            <CardContent>
              <Typography variant="h6" className="mb-4">
                {t("offline.offline-mode-info")}
              </Typography>
              <Typography variant="body2" className="mb-2">
                {t("offline.offline-mode-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {t("offline.offline-mode-note")}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      )}
    </Box>
  );
}
