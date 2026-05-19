import { useState } from "react";

import { Button, Card, CardContent, FormControl, FormLabel, Grid, MenuItem, Select, Typography } from "@mui/material";

import { useLayoutContext } from "@/components/layout/layout-context";
import { DEFAULTS } from "@/config";
import { useThemeContext } from "@/theme/theme-provider";
import type { MeData } from "@/types/me";

interface Props {
  meData: MeData;
  onUpdated: () => void;
}

export default function SettingsAppearance({ meData, onUpdated }: Props) {
  const { themeMode, themeColor, setThemeMode, setThemeColor } = useThemeContext();
  const { contentType, leftMenuType, setContentType, setLeftMenuType } = useLayoutContext();

  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<{ text: string; error: boolean } | null>(null);

  const [localThemeMode, setLocalThemeMode] = useState(meData.theme_mode ?? themeMode);
  const [localThemeColor, setLocalThemeColor] = useState(meData.theme_color ?? themeColor);
  const [localContentType, setLocalContentType] = useState(meData.content_type ?? contentType);
  const [localLeftMenuType, setLocalLeftMenuType] = useState(meData.left_menu_type ?? leftMenuType);

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
          theme_mode: localThemeMode,
          theme_color: localThemeColor,
          content_type: localContentType,
          left_menu_type: localLeftMenuType,
        }),
      });

      if (!res.ok) throw new Error("Gagal menyimpan preferensi tampilan.");

      // Update global context directly
      setThemeMode(localThemeMode as any);
      setThemeColor(localThemeColor);
      setContentType(localContentType as any);
      setLeftMenuType(localLeftMenuType as any);

      setMsg({ text: "Tampilan berhasil diperbarui.", error: false });
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
            Tampilan & Layout
          </Typography>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Tema Warna
            </FormLabel>
            <Select value={localThemeColor} onChange={(e) => setLocalThemeColor(e.target.value)} className="w-full">
              <MenuItem value="theme-purple">Purple (Default)</MenuItem>
              <MenuItem value="theme-blue">Blue</MenuItem>
              <MenuItem value="theme-green">Green</MenuItem>
              <MenuItem value="theme-rose">Rose</MenuItem>
              <MenuItem value="theme-orange">Orange</MenuItem>
            </Select>
          </FormControl>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Mode Tampilan
            </FormLabel>
            <Select value={localThemeMode} onChange={(e) => setLocalThemeMode(e.target.value)} className="w-full">
              <MenuItem value="light">Terang</MenuItem>
              <MenuItem value="dark">Gelap</MenuItem>
              <MenuItem value="system">Mengikuti Sistem</MenuItem>
            </Select>
          </FormControl>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Tata Letak Konten
            </FormLabel>
            <Select value={localContentType} onChange={(e) => setLocalContentType(e.target.value)} className="w-full">
              <MenuItem value="fluid">Fluid (Penuh)</MenuItem>
              <MenuItem value="boxed">Boxed (Terpusat)</MenuItem>
            </Select>
          </FormControl>

          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Jenis Menu Navigasi
            </FormLabel>
            <Select value={localLeftMenuType} onChange={(e) => setLocalLeftMenuType(e.target.value)} className="w-full">
              <MenuItem value="comfort">Kenyamanan (Comfort)</MenuItem>
              <MenuItem value="compact">Kompak (Compact)</MenuItem>
            </Select>
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
            onClick={handleSave}
            disabled={saving}
            className="mt-2"
          >
            {saving ? "Menyimpan..." : "Simpan Tampilan"}
          </Button>
        </CardContent>
      </Card>
    </Grid>
  );
}
