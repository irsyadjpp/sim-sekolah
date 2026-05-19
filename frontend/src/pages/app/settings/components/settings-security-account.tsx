import { useState } from "react";
import { useTranslation } from "react-i18next";

import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  Grid,
  Input,
  Switch,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import type { MeData } from "@/types/me";

interface Props {
  meData: MeData;
  onUpdated: () => void;
}

export default function SettingsSecurityAccount({ meData, onUpdated }: Props) {
  const { t } = useTranslation();
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(meData.two_factor_enabled ?? false);

  // Setup Modal States
  const [showSetup, setShowSetup] = useState(false);
  const [loadingSetup, setLoadingSetup] = useState(false);
  const [setupData, setSetupData] = useState<{ secret: string; qr_code_url: string } | null>(null);
  const [verificationCode, setVerificationCode] = useState("");
  const [verifying, setVerifying] = useState(false);
  const [setupError, setSetupError] = useState<string | null>(null);

  // Disable Modal States
  const [showDisable, setShowDisable] = useState(false);
  const [disableCode, setDisableCode] = useState("");
  const [disabling, setDisabling] = useState(false);
  const [disableError, setDisableError] = useState<string | null>(null);

  const handleToggle = (e: React.ChangeEvent<HTMLInputElement>) => {
    const checked = e.target.checked;
    if (checked) {
      // Trigger 2FA setup flow
      initiate2FASetup();
    } else {
      // Trigger 2FA disable flow
      setShowDisable(true);
      setDisableCode("");
      setDisableError(null);
    }
  };

  const initiate2FASetup = async () => {
    setLoadingSetup(true);
    setSetupError(null);
    setShowSetup(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/2fa/setup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      const result = await res.json();
      if (!res.ok || result.status !== "success") {
        throw new Error(result.message || "Gagal menginisiasi setup 2FA");
      }
      setSetupData(result.data);
    } catch (err: any) {
      setSetupError(err.message);
    } finally {
      setLoadingSetup(false);
    }
  };

  const handleVerifyEnable = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!verificationCode || verificationCode.length !== 6) {
      setSetupError(t("mfa.settings-invalid-code"));
      return;
    }
    setVerifying(true);
    setSetupError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/2fa/enable`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ code: verificationCode }),
      });
      const result = await res.json();
      if (!res.ok || result.status !== "success") {
        throw new Error(result.message || t("mfa.settings-invalid-code"));
      }
      setTwoFactorEnabled(true);
      setShowSetup(false);
      onUpdated();
    } catch (err: any) {
      setSetupError(err.message);
    } finally {
      setVerifying(false);
    }
  };

  const handleVerifyDisable = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!disableCode || disableCode.length !== 6) {
      setDisableError(t("mfa.settings-invalid-code"));
      return;
    }
    setDisabling(true);
    setDisableError(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/2fa/disable`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ code: disableCode }),
      });
      const result = await res.json();
      if (!res.ok || result.status !== "success") {
        throw new Error(result.message || t("mfa.settings-invalid-code"));
      }
      setTwoFactorEnabled(false);
      setShowDisable(false);
      onUpdated();
    } catch (err: any) {
      setDisableError(err.message);
    } finally {
      setDisabling(false);
    }
  };

  return (
    <Grid size={{ xs: 12 }}>
      <Card>
        <CardContent>
          <Typography variant="h6" component="h6" className="card-title">
            {t("mfa.settings-title")}
          </Typography>
          <Typography variant="body2" className="text-text-secondary mb-4">
            {t("mfa.settings-desc")}
          </Typography>

          <Grid container direction="column" spacing={2} className="mb-4">
            <Grid size={{ xs: 12 }}>
              <FormControlLabel
                control={<Switch checked={twoFactorEnabled} onChange={handleToggle} color="primary" />}
                label={
                  <div>
                    <Typography variant="body1">{t("mfa.settings-title")}</Typography>
                    <Typography variant="body2" className="text-text-secondary">
                      {t("mfa.settings-desc")}
                    </Typography>
                  </div>
                }
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Setup 2FA Dialog */}
      <Dialog
        open={showSetup}
        onClose={() => {
          if (!verifying) {
            setShowSetup(false);
            setVerificationCode("");
            setSetupData(null);
          }
        }}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>{t("mfa.settings-setup-title")}</DialogTitle>
        <DialogContent dividers>
          {loadingSetup ? (
            <Box className="flex flex-col items-center justify-center gap-4 py-8">
              <CircularProgress />
              <Typography variant="body2" className="text-text-secondary">
                Menyiapkan konfigurasi keamanan...
              </Typography>
            </Box>
          ) : setupError && !setupData ? (
            <Alert severity="error" className="mb-4">
              {setupError}
            </Alert>
          ) : (
            setupData && (
              <Box className="flex flex-col gap-6 py-2">
                <Typography variant="body2">{t("mfa.settings-setup-scan")}</Typography>

                <Box className="mx-auto my-2 flex max-w-[240px] justify-center rounded-lg border border-slate-100 bg-white p-4 shadow-sm">
                  <img
                    src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(
                      setupData.qr_code_url,
                    )}`}
                    alt="2FA QR Code"
                    style={{ width: "200px", height: "200px" }}
                  />
                </Box>

                <Typography variant="body2" className="text-text-secondary mt-2">
                  {t("mfa.settings-setup-key")}{" "}
                  <strong className="text-primary mt-1 block rounded bg-slate-50 p-1.5 text-center font-mono tracking-wider select-all dark:bg-slate-800">
                    {setupData.secret}
                  </strong>
                </Typography>

                <Typography variant="body2" className="mt-4">
                  {t("mfa.settings-setup-verify")}
                </Typography>

                <Box component="form" onSubmit={handleVerifyEnable} className="flex flex-col gap-4">
                  <Input
                    placeholder={t("mfa.settings-setup-placeholder")}
                    value={verificationCode}
                    onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                    inputProps={{
                      style: { textAlign: "center", fontSize: "1.25rem", letterSpacing: "0.25rem", fontWeight: 700 },
                    }}
                    fullWidth
                    autoFocus
                  />

                  {setupError && (
                    <Alert severity="error" className="mt-2">
                      {setupError}
                    </Alert>
                  )}
                </Box>
              </Box>
            )
          )}
        </DialogContent>
        <DialogActions>
          <Button
            color="secondary"
            onClick={() => {
              setShowSetup(false);
              setVerificationCode("");
              setSetupData(null);
            }}
            disabled={verifying}
          >
            {t("mfa.settings-setup-canceling")}
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleVerifyEnable}
            disabled={verifying || verificationCode.length !== 6 || !setupData}
          >
            {verifying ? "Mengaktifkan..." : t("mfa.settings-setup-button")}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Disable 2FA Dialog */}
      <Dialog
        open={showDisable}
        onClose={() => {
          if (!disabling) {
            setShowDisable(false);
            setDisableCode("");
            setDisableError(null);
          }
        }}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>{t("mfa.settings-disable-title")}</DialogTitle>
        <DialogContent dividers>
          <Box component="form" onSubmit={handleVerifyDisable} className="flex flex-col gap-4 py-2">
            <Typography variant="body2">{t("mfa.settings-disable-desc")}</Typography>

            <Input
              placeholder={t("mfa.settings-setup-placeholder")}
              value={disableCode}
              onChange={(e) => setDisableCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
              inputProps={{
                style: { textAlign: "center", fontSize: "1.25rem", letterSpacing: "0.25rem", fontWeight: 700 },
              }}
              fullWidth
              autoFocus
            />

            {disableError && (
              <Alert severity="error" className="mt-2">
                {disableError}
              </Alert>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button
            color="secondary"
            onClick={() => {
              setShowDisable(false);
              setDisableCode("");
              setDisableError(null);
            }}
            disabled={disabling}
          >
            {t("mfa.settings-setup-canceling")}
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={handleVerifyDisable}
            disabled={disabling || disableCode.length !== 6}
          >
            {disabling ? "Menonaktifkan..." : t("mfa.settings-disable-button")}
          </Button>
        </DialogActions>
      </Dialog>
    </Grid>
  );
}
