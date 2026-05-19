import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-settings" />
    </Box>
  );
};

export default function DocsThemeSettings() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const settings = [
    {
      title: "Ganti Bahasa",
      description:
        "Halaman ini bisa diatur dalam bahasa Indonesia atau Inggris. Caranya tekan gambar bendera yang ada di bagian atas.",
      details: "Semua petunjuk dan tulisan akan otomatis berubah mengikuti bahasa yang dipilih.",
    },
    {
      title: "Gaya Warna Layar",
      description:
        "Bapak dan Ibu bisa memilih layar yang terang atau yang agak gelap agar mata tidak cepat lelah saat bekerja. Tekan gambar bulan atau matahari di bagian atas.",
      details: "Bisa juga diatur agar berubah sendiri mengikuti waktu siang dan malam.",
    },
    {
      title: "Warna Utama",
      description:
        "Pilih warna kesukaan Bapak dan Ibu untuk tombol-tombol di layar (ada Biru, Oranye, Ungu, atau Hijau).",
      details: "Pilihannya ada di bagian tombol gambar gir di sebelah kanan.",
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
              Mengatur Tampilan
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Aturan Layar</Typography>
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
                Menyesuaikan Kenyamanan Bapak & Ibu
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-10 text-lg leading-relaxed">
                Halaman ini bisa diatur tampilannya agar Bapak dan Ibu lebih nyaman saat menggunakannya sehari-hari.
                Berikut adalah beberapa hal yang bisa diubah:
              </Typography>

              <Box className="flex flex-col gap-6">
                {settings.map((item, index) => (
                  <Box key={index} className="rounded-[32px] border border-slate-100 bg-slate-50 p-8">
                    <Typography variant="h5" className="text-primary mb-3 font-bold">
                      {item.title}
                    </Typography>
                    <Typography variant="body1" className="mb-2 leading-relaxed text-slate-700">
                      {item.description}
                    </Typography>
                    <Typography variant="caption" className="text-text-secondary italic">
                      * {item.details}
                    </Typography>
                  </Box>
                ))}
              </Box>

              <Divider className="my-10" />

              <Typography variant="h6" className="mb-4 font-bold">
                Penting untuk Diingat
              </Typography>
              <Typography variant="body2" className="text-text-secondary leading-relaxed">
                Pilihan ini hanya berlaku di komputer yang sedang Bapak dan Ibu gunakan sekarang. Jika Bapak dan Ibu
                pindah ke komputer lain, mungkin perlu mengatur ulang kembali warnanya.
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
