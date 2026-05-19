import SettingsAppearance from "./components/settings-appearance";
import SettingsContact from "./components/settings-contact";
import SettingsNotification from "./components/settings-notification";
import SettingsPublicInfo from "./components/settings-public-info";
import SettingsRole from "./components/settings-role";
import SettingsSecurity from "./components/settings-security";
import SettingsSecurityAccount from "./components/settings-security-account";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

import {
  Box,
  Breadcrumbs,
  Button,
  CircularProgress,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
  Typography,
} from "@mui/material";
import { Grid } from "@mui/material";

import { DEFAULTS } from "@/config";
import NiBell from "@/icons/nexture/ni-bell";
import NiBriefcase from "@/icons/nexture/ni-briefcase";
import NiListCircle from "@/icons/nexture/ni-list-circle";
import NiLock from "@/icons/nexture/ni-lock";
import NiPaintRoller from "@/icons/nexture/ni-paint-roller";
import NiPin from "@/icons/nexture/ni-pin";
import NiShield from "@/icons/nexture/ni-shield";
import NiUser from "@/icons/nexture/ni-user";
import type { MeData } from "@/types/me";

export type { MeData };

const MenuContent = () => {
  const location = useLocation();
  const path = location.pathname;

  const isSelected = (target: string) => path === target || (target === "/settings" && path === "/settings/");

  return (
    <Box className="flex flex-col gap-4">
      <List className="-mt-6">
        <ListItem disablePadding>
          <ListItemButton className="pointer-events-none mt-4">
            <ListItemText
              primary="Akun"
              slotProps={{
                primary: { className: "text-xs! font-semibold! opacity-40" },
              }}
            />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton href="/settings" LinkComponent={Link} selected={isSelected("/settings")}>
            <ListItemIcon>
              <NiUser size="medium" />
            </ListItemIcon>
            <ListItemText primary="Profil Saya" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton href="/settings/kontak" LinkComponent={Link} selected={isSelected("/settings/kontak")}>
            <ListItemIcon>
              <NiPin size="medium" />
            </ListItemIcon>
            <ListItemText primary="Kontak & Alamat" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton href="/settings/pekerjaan" LinkComponent={Link} selected={isSelected("/settings/pekerjaan")}>
            <ListItemIcon>
              <NiBriefcase size="medium" />
            </ListItemIcon>
            <ListItemText primary="Data Kepegawaian/Sekolah" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton className="pointer-events-none mt-4">
            <ListItemText
              primary="Keamanan"
              slotProps={{
                primary: { className: "text-xs! font-semibold! opacity-40" },
              }}
            />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton href="/settings/password" LinkComponent={Link} selected={isSelected("/settings/password")}>
            <ListItemIcon>
              <NiLock size="medium" />
            </ListItemIcon>
            <ListItemText primary="Ubah Password" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton href="/settings/keamanan" LinkComponent={Link} selected={isSelected("/settings/keamanan")}>
            <ListItemIcon>
              <NiShield size="medium" />
            </ListItemIcon>
            <ListItemText primary="Keamanan Akun" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton className="pointer-events-none mt-4">
            <ListItemText
              primary="Preferensi"
              slotProps={{
                primary: { className: "text-xs! font-semibold! opacity-40" },
              }}
            />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            href="/settings/notifikasi"
            LinkComponent={Link}
            selected={isSelected("/settings/notifikasi")}
          >
            <ListItemIcon>
              <NiBell size="medium" />
            </ListItemIcon>
            <ListItemText primary="Notifikasi" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton href="/settings/tampilan" LinkComponent={Link} selected={isSelected("/settings/tampilan")}>
            <ListItemIcon>
              <NiPaintRoller size="medium" />
            </ListItemIcon>
            <ListItemText primary="Tampilan" />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );
};

export default function Settings() {
  const [openDrawer, setOpenDrawer] = useState(false);
  const [meData, setMeData] = useState<MeData | null>(null);
  const [loading, setLoading] = useState(() => (!localStorage.getItem("accessToken") ? false : true));
  const [error, setError] = useState<string | null>(() =>
    !localStorage.getItem("accessToken") ? "Sesi telah berakhir. Silakan login kembali." : null,
  );

  const fetchMe = () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setError("Sesi telah berakhir. Silakan login kembali.");
      setLoading(false);
      return;
    }

    fetch(`${DEFAULTS.API_URL}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Gagal memuat profil.");
        return res.json();
      })
      .then((json) => {
        setMeData(json.data);
        // Sync to localStorage as well
        localStorage.setItem("-user-data", JSON.stringify(json.data));
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    if (localStorage.getItem("accessToken")) {
      Promise.resolve().then(() => fetchMe());
    }
  }, []);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const roleLabel = () => {
    if (!meData?.roles?.length) return "Pengguna";
    const roleMap: Record<string, string> = {
      SUPER_ADMIN: "Super Admin",
      ADMIN_SEKOLAH: "Admin Sekolah",
      GURU: "Guru",
      SISWA: "Siswa",
    };
    return meData.roles.map((r) => roleMap[r] ?? r).join(", ");
  };

  return (
    <Grid container spacing={5} className="items-start">
      <Grid size={"auto"} className="hidden pe-8 lg:flex">
        <MenuContent />
      </Grid>
      <Grid size={"grow"} spacing={5} container>
        <Grid size={12} spacing={2.5} container>
          <Grid size={{ xs: 12, md: "grow" }}>
            <Typography variant="h1" component="h1" className="mb-0">
              Pengaturan Akun
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/dashboards/default">
                Beranda
              </Link>
              <Typography variant="body2">Pengaturan</Typography>
            </Breadcrumbs>
          </Grid>
          <Grid size={{ xs: 12, md: "auto" }} className="lg:hidden">
            <Tooltip title="Daftar Menu">
              <Button
                className="icon-only surface-standard"
                color="grey"
                variant="surface"
                onClick={toggleDrawer(true)}
              >
                <NiListCircle size={"medium"} />
              </Button>
            </Tooltip>
          </Grid>
        </Grid>

        {loading && (
          <Grid size={12} className="flex justify-center py-10">
            <CircularProgress />
          </Grid>
        )}

        {error && (
          <Grid size={12}>
            <Typography color="error">{error}</Typography>
          </Grid>
        )}

        {!loading && !error && meData && (
          <Box className="flex w-full flex-col gap-5">
            {location.pathname === "/settings" || location.pathname === "/settings/" ? (
              <SettingsPublicInfo meData={meData} onUpdated={fetchMe} />
            ) : null}
            {location.pathname === "/settings/kontak" && <SettingsContact meData={meData} onUpdated={fetchMe} />}
            {location.pathname === "/settings/pekerjaan" && <SettingsRole meData={meData} roleLabel={roleLabel()} />}
            {location.pathname === "/settings/password" && <SettingsSecurity />}
            {location.pathname === "/settings/keamanan" && (
              <SettingsSecurityAccount meData={meData} onUpdated={fetchMe} />
            )}
            {location.pathname === "/settings/notifikasi" && (
              <SettingsNotification meData={meData} onUpdated={fetchMe} />
            )}
            {location.pathname === "/settings/tampilan" && <SettingsAppearance meData={meData} onUpdated={fetchMe} />}
          </Box>
        )}

        <Drawer open={openDrawer} anchor="right" onClose={toggleDrawer(false)}>
          <Box className="min-w-80 p-7">
            <MenuContent />
          </Box>
        </Drawer>
      </Grid>
    </Grid>
  );
}
