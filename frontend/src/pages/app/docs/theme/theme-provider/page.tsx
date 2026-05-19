import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-theme-provider" />
    </Box>
  );
};

export default function DocsThemeThemeProvider() {
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
              Pilihan Kesukaan
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Pilihan</Typography>
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
                Supaya Bapak & Ibu Nyaman Bekerja
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-10 text-lg leading-relaxed">
                Supaya Bapak dan Ibu tidak cepat lelah saat mengurus data sekolah, halaman ini bisa diatur mengikuti
                kebiasaan Bapak dan Ibu saat menggunakan komputer.
              </Typography>

              <Box className="flex flex-col gap-8">
                <Box className="rounded-3xl border border-slate-100 bg-slate-50 p-6">
                  <Typography variant="h6" className="mb-2 font-bold">
                    Berubah Sendiri Ikuti Waktu
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary leading-relaxed">
                    Halaman ini bisa berubah warnanya sendiri menjadi lebih redup jika Bapak dan Ibu bekerja di malam
                    hari, agar mata tetap nyaman dan tidak sakit terkena cahaya yang terlalu terang.
                  </Typography>
                </Box>

                <Box className="rounded-3xl border border-slate-100 bg-slate-50 p-6">
                  <Typography variant="h6" className="mb-2 font-bold">
                    Tanda Warna untuk Setiap Bagian
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary leading-relaxed">
                    Setiap bagian menu (seperti bagian Guru atau bagian Siswa) memiliki tanda warna yang berbeda.
                    Tujuannya agar Bapak dan Ibu tahu sedang berada di bagian mana hanya dengan melihat warnanya saja.
                  </Typography>
                </Box>
              </Box>

              <Divider className="my-10" />

              <Typography variant="h6" className="mb-4 font-bold">
                Janji Kami untuk Bapak & Ibu Guru
              </Typography>
              <Typography variant="body2" className="text-text-secondary leading-relaxed">
                Kami ingin Bapak dan Ibu lebih senang mengajar siswa-siswi kita di SDI Bonerate No 85 tanpa harus
                dipusingkan dengan cara kerja komputer yang sulit. Halaman ini hadir untuk membantu tugas mulia Bapak
                dan Ibu.
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
