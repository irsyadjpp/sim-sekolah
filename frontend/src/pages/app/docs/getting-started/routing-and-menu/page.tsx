import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-routing-and-menu" />
    </Box>
  );
};

export default function DocsGettingStartedRoutingAndMenu() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const roles = [
    {
      role: "Pengelola Utama (Kepala Sekolah/Admin)",
      access: "Bisa melihat dan mengatur semua isi di halaman ini, mulai dari data guru, siswa, hingga aturan sekolah.",
    },
    {
      role: "Bapak & Ibu Guru",
      access: "Bisa membuka bagian Pengajaran untuk mengatur jadwal, nilai, dan rencana belajar siswa.",
    },
    {
      role: "Staf Tata Usaha",
      access: "Bisa membuka bagian pendaftaran siswa baru dan merapikan surat-surat atau berkas sekolah.",
    },
  ];

  return (
    <Grid container spacing={5} className="items-start">
      <Grid size={"auto"} className="hidden pe-8 lg:flex">
        <MenuContent />
      </Grid>
      <Grid size={"grow"} spacing={5} container>
        <Grid size={12} spacing={2.5} container>
          <Grid size={{ xs: 12, md: "grow" }}>
            <Typography variant="h1" component="h1" className="mb-0">
              Siapa Saja yang Bisa Membuka Halaman Ini?
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Hak Pengguna</Typography>
            </Breadcrumbs>
          </Grid>
          <Grid size={{ xs: 12, md: "auto" }} className="lg:hidden">
            <Tooltip title="Menu Bantuan">
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

        <Grid size={12}>
          <Card className="rounded-4xl border-none shadow-xl">
            <CardContent className="p-8 md:p-12">
              <Typography variant="h4" className="mb-6 font-black">
                Pembagian Tugas & Wewenang
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-10 text-lg leading-relaxed">
                Demi menjaga agar data di SDI Bonerate No 85 tidak berantakan, setiap orang diberikan pilihan menu yang
                berbeda sesuai dengan tugasnya masing-masing.
              </Typography>

              <Box className="flex flex-col gap-6">
                {roles.map((item, index) => (
                  <Box
                    key={index}
                    className="flex items-start gap-6 rounded-3xl border border-slate-100 bg-slate-50 p-6"
                  >
                    <Box className="bg-primary/10 text-primary flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl">
                      <Typography variant="h5" className="font-black">
                        {index + 1}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" className="mb-1 font-bold">
                        {item.role}
                      </Typography>
                      <Typography variant="body2" className="text-text-secondary leading-relaxed">
                        {item.access}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>

              <Divider className="my-10" />

              <Typography variant="h6" className="mb-4 font-bold">
                Cara Kerja yang Mudah
              </Typography>
              <Typography variant="body2" className="text-text-secondary mb-4 leading-relaxed">
                Halaman ini dibuat agar Bapak dan Ibu tidak pusing melihat terlalu banyak menu yang tidak perlu. Dengan
                begitu, Bapak dan Ibu bisa lebih fokus mengajar dan mendampingi siswa.
              </Typography>
              <Typography variant="body2" className="text-text-secondary leading-relaxed">
                Jika ada menu yang Bapak dan Ibu butuhkan tapi tidak muncul, silakan lapor ke Pengelola Utama agar
                dibukakan aksesnya.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Drawer open={openDrawer} anchor="right" onClose={toggleDrawer(false)}>
          <Box className="min-w-80 p-7">
            <MenuContent />
          </Box>
        </Drawer>
      </Grid>
    </Grid>
  );
}
