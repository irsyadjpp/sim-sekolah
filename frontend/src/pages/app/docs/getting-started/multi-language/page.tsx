import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Grid, Tooltip, Typography } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-multi-language" />
    </Box>
  );
};

export default function DocsGettingStartedMultiLanguage() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
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
              Pilihan Bahasa
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Bahasa</Typography>
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
                Dua Bahasa: Indonesia & Inggris
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-10 text-lg leading-relaxed">
                Halaman SDI Bonerate No 85 ini bisa tampil dalam dua bahasa. Bapak dan Ibu bisa memilih bahasa yang
                paling nyaman digunakan agar tidak ada kata-kata yang membingungkan.
              </Typography>

              <Grid container spacing={4}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Box className="rounded-3xl border border-blue-100 bg-blue-50 p-6">
                    <Typography variant="h6" className="mb-2 font-bold text-blue-700">
                      Bahasa Indonesia
                    </Typography>
                    <Typography variant="body2" className="text-blue-900/70">
                      Bahasa utama untuk semua tulisan, pengumuman, dan laporan sekolah.
                    </Typography>
                  </Box>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Box className="rounded-3xl border border-orange-100 bg-orange-50 p-6">
                    <Typography variant="h6" className="mb-2 font-bold text-orange-700">
                      English (Inggris)
                    </Typography>
                    <Typography variant="body2" className="text-orange-900/70">
                      Pilihan bahasa lain yang bisa Bapak dan Ibu coba untuk mengenal istilah pendidikan masa kini.
                    </Typography>
                  </Box>
                </Grid>
              </Grid>

              <Divider className="my-10" />

              <Typography variant="h6" className="mb-4 font-bold">
                Cara Mengganti Bahasa
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-6 leading-relaxed">
                Bapak dan Ibu bisa mengganti bahasa kapan saja. Caranya cukup tekan gambar bendera yang ada di bagian
                kanan atas layar. Seketika itu juga, semua tulisan di menu dan tombol akan berubah.
              </Typography>

              <Typography
                variant="body2"
                className="border-primary rounded-2xl border-l-4 bg-slate-100 p-4 text-slate-600 italic"
              >
                Penting: Mengganti bahasa hanya mengubah tulisan petunjuk saja, tidak akan mengubah data asli (seperti
                nama orang atau alamat rumah).
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
