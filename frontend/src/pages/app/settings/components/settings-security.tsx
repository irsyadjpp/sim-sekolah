import { useState } from "react";

import {
  Button,
  Card,
  CardContent,
  FormControl,
  FormLabel,
  Grid,
  IconButton,
  Input,
  InputAdornment,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiEyeClose from "@/icons/nexture/ni-eye-close";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";

export default function SettingsSecurity() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showCurrent, setShowCurrent] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<{ text: string; error: boolean } | null>(null);

  const handleChangePassword = async () => {
    setMsg(null);
    if (!currentPassword || !newPassword || !confirmPassword) {
      setMsg({ text: "Semua field harus diisi.", error: true });
      return;
    }
    if (newPassword !== confirmPassword) {
      setMsg({ text: "Password baru dan konfirmasi tidak cocok.", error: true });
      return;
    }
    if (newPassword.length < 8) {
      setMsg({ text: "Password baru minimal 8 karakter.", error: true });
      return;
    }

    setSaving(true);
    const token = localStorage.getItem("accessToken");
    try {
      // We use the forgot-password / reset flow or a dedicated change-password endpoint
      // For now call a general endpoint
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/change-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.message ?? "Gagal mengubah password.");
      }
      setMsg({ text: "Password berhasil diubah.", error: false });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (e: unknown) {
      setMsg({ text: e instanceof Error ? e.message : "Terjadi kesalahan.", error: true });
    } finally {
      setSaving(false);
    }
  };

  return (
    <Grid size={12}>
      <Card>
        <CardContent>
          <Typography variant="h6" component="h6" className="card-title">
            Ubah Password
          </Typography>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Password Saat Ini
            </FormLabel>
            <Input
              type={showCurrent ? "text" : "password"}
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full"
              endAdornment={
                <InputAdornment position="end">
                  <IconButton size="small" onClick={() => setShowCurrent(!showCurrent)}>
                    {showCurrent ? <NiEyeClose size="small" /> : <NiEyeOpen size="small" />}
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Password Baru
            </FormLabel>
            <Input
              type={showNew ? "text" : "password"}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full"
              endAdornment={
                <InputAdornment position="end">
                  <IconButton size="small" onClick={() => setShowNew(!showNew)}>
                    {showNew ? <NiEyeClose size="small" /> : <NiEyeOpen size="small" />}
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Konfirmasi Password
            </FormLabel>
            <Input
              type={showConfirm ? "text" : "password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full"
              endAdornment={
                <InputAdornment position="end">
                  <IconButton size="small" onClick={() => setShowConfirm(!showConfirm)}>
                    {showConfirm ? <NiEyeClose size="small" /> : <NiEyeOpen size="small" />}
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>

          {msg && (
            <Typography variant="body2" color={msg.error ? "error" : "success.main"} className="mt-2">
              {msg.text}
            </Typography>
          )}

          <Button
            size="medium"
            color="primary"
            variant="outlined"
            onClick={handleChangePassword}
            disabled={saving}
            className="mt-2"
          >
            {saving ? "Memproses..." : "Ubah Password"}
          </Button>
        </CardContent>
      </Card>
    </Grid>
  );
}
