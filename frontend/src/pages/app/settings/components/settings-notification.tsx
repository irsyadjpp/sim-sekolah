import { useState } from "react";

import { Button, Card, CardContent, FormControlLabel, Grid, Switch, Typography } from "@mui/material";

import { DEFAULTS } from "@/config";
import type { MeData } from "@/types/me";

interface Props {
  meData: MeData;
  onUpdated: () => void;
}

export default function SettingsNotification({ meData, onUpdated }: Props) {
  // Read from meData, fallback to true if undefined
  const [emailNotifications, setEmailNotifications] = useState(meData.email_notifications ?? true);
  const [pushNotifications, setPushNotifications] = useState(meData.push_notifications ?? true);

  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<{ text: string; error: boolean } | null>(null);

  const handleSave = async () => {
    setSaving(true);
    setMsg(null);
    const token = localStorage.getItem("accessToken");

    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/me`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          email_notifications: emailNotifications,
          push_notifications: pushNotifications,
        }),
      });

      if (!res.ok) throw new Error("Gagal menyimpan preferensi notifikasi.");

      setMsg({ text: "Preferensi notifikasi berhasil diperbarui.", error: false });
      onUpdated();
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
            Preferensi Notifikasi
          </Typography>
          <Typography variant="body2" className="text-text-secondary mb-4">
            Pilih bagaimana Anda ingin menerima pembaruan dari sistem.
          </Typography>

          <Grid container direction="column" spacing={2} className="mb-4">
            <Grid>
              <FormControlLabel
                control={
                  <Switch
                    checked={emailNotifications}
                    onChange={(e) => setEmailNotifications(e.target.checked)}
                    color="primary"
                  />
                }
                label={
                  <div>
                    <Typography variant="body1">Notifikasi Email</Typography>
                    <Typography variant="body2" className="text-text-secondary">
                      Terima pembaruan penting via email (seperti reset password, pengumuman).
                    </Typography>
                  </div>
                }
              />
            </Grid>
            <Grid>
              <FormControlLabel
                control={
                  <Switch
                    checked={pushNotifications}
                    onChange={(e) => setPushNotifications(e.target.checked)}
                    color="primary"
                  />
                }
                label={
                  <div>
                    <Typography variant="body1">Notifikasi Push (Browser)</Typography>
                    <Typography variant="body2" className="text-text-secondary">
                      Tampilkan notifikasi di browser Anda saat aplikasi sedang dibuka.
                    </Typography>
                  </div>
                }
              />
            </Grid>
          </Grid>

          {msg && (
            <Typography variant="body2" color={msg.error ? "error" : "success.main"} className="mt-2">
              {msg.text}
            </Typography>
          )}

          <Button
            size="medium"
            color="primary"
            variant="outlined"
            onClick={handleSave}
            disabled={saving}
            className="mt-2"
          >
            {saving ? "Menyimpan..." : "Simpan Preferensi"}
          </Button>
        </CardContent>
      </Card>
    </Grid>
  );
}
