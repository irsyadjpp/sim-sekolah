import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-styling" />
    </Box>
  );
};

export default function DocsThemeStyling() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const personalization = [
    {
      title: "Gaya Menu Samping",
      description:
        "Bapak dan Ibu bisa memilih bentuk menu di sebelah kiri, apakah mau yang kecil saja atau yang lebar lengkap dengan tulisan.",
      details: "Menu yang kecil memberikan ruang baca yang lebih luas di tengah layar.",
    },
    {
      title: "Lebar Kotak Halaman",
      description: "Atur apakah isi halaman mau di tengah kotak saja atau memenuhi seluruh lebar layar komputer.",
      details:
        "Pilihan layar penuh sangat bagus digunakan saat Bapak dan Ibu melihat daftar nama siswa yang sangat banyak.",
    },
    {
      title: "Gerakan Halus Layar",
      description: "Layar akan bergerak dengan halus saat Bapak dan Ibu berpindah dari satu bagian ke bagian lainnya.",
      details: "Dibuat agar mata Bapak dan Ibu tetap nyaman meskipun lama menggunakan halaman ini.",
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
              Mengatur Gaya Halaman
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Gaya Halaman</Typography>
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
                Merapikan Bentuk Layar
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-10 text-lg leading-relaxed">
                Selain warna, Bapak dan Ibu juga bisa mengatur bagaimana bentuk menu dan kotak tulisan tampil di layar.
                Pilihannya ada di bagian pengaturan sebelah kanan:
              </Typography>

              <Grid container spacing={4}>
                {personalization.map((item, index) => (
                  <Grid key={index} size={{ xs: 12, md: 6 }}>
                    <Box className="h-full rounded-[32px] border border-slate-100 bg-slate-50 p-6">
                      <Typography variant="h5" className="text-primary mb-3 font-bold">
                        {item.title}
                      </Typography>
                      <Typography variant="body2" className="mb-3 leading-relaxed text-slate-700">
                        {item.description}
                      </Typography>
                      <Typography variant="caption" className="text-text-secondary block italic">
                        Tip: {item.details}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>

              <Divider className="my-10" />

              <Typography variant="h6" className="mb-4 text-center font-bold">
                Dibuat Khusus untuk SDI Bonerate
              </Typography>
              <Typography variant="body2" className="text-text-secondary text-center leading-relaxed">
                Semua pilihan ini disiapkan agar Bapak dan Ibu betah dan tidak pusing saat mengerjakan laporan atau
                melihat data di sekolah kita tercinta UPT SDI Bonerate No 85.
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
