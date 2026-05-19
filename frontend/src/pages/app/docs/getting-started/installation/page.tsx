import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-installation" />
    </Box>
  );
};

export default function DocsGettingStartedInstallation() {
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
              Cara Masuk ke Halaman Sekolah
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Cara Masuk</Typography>
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
                Langkah Mudah Membuka Halaman SDI Bonerate No 85
              </Typography>

              <Typography variant="body1" className="text-text-secondary mb-10 leading-relaxed">
                Halaman ini adalah tempat resmi untuk seluruh Bapak dan Ibu Guru serta Staf di SDI Bonerate No 85.
                Silakan ikuti langkah-langkah di bawah ini:
              </Typography>

              <Box className="flex flex-col gap-8">
                <Box>
                  <Typography variant="h6" className="mb-2 flex items-center gap-3 font-bold">
                    <Box className="bg-primary flex h-8 w-8 items-center justify-center rounded-full text-sm text-white">
                      1
                    </Box>
                    Buka Aplikasi Internet
                  </Typography>
                  <Typography variant="body1" className="text-text-secondary pl-11">
                    Gunakan aplikasi untuk membuka internet yang ada di komputer atau laptop Bapak dan Ibu (biasanya
                    yang gambarnya bulat berwarna-warni).
                  </Typography>
                </Box>

                <Box>
                  <Typography variant="h6" className="mb-2 flex items-center gap-3 font-bold">
                    <Box className="bg-primary flex h-8 w-8 items-center justify-center rounded-full text-sm text-white">
                      2
                    </Box>
                    Ketik Alamat Website
                  </Typography>
                  <Typography variant="body1" className="text-text-secondary pl-11">
                    Ketik alamat website sekolah yang sudah dibagikan oleh pengelola di kotak bagian atas aplikasi
                    internet Anda.
                  </Typography>
                </Box>

                <Box>
                  <Typography variant="h6" className="mb-2 flex items-center gap-3 font-bold">
                    <Box className="bg-primary flex h-8 w-8 items-center justify-center rounded-full text-sm text-white">
                      3
                    </Box>
                    Masukkan Nama & Kata Sandi
                  </Typography>
                  <Typography variant="body1" className="text-text-secondary pl-11">
                    Gunakan **Nama Panggilan** atau **Nomor Pegawai** serta **Kata Sandi** yang sudah Bapak dan Ibu
                    miliki. Jika belum punya, silakan minta ke bagian Tata Usaha.
                  </Typography>
                </Box>
              </Box>

              <Divider className="my-10" />

              <Typography variant="h5" className="mb-6 font-black">
                Ada Masalah Saat Masuk?
              </Typography>

              <Grid container spacing={4}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="subtitle1" className="mb-1 font-bold text-red-500">
                    Gagal Masuk / Kata Sandi Salah
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary">
                    Pastikan huruf besar dan kecilnya sudah benar. Periksa juga apakah lampu tombol untuk huruf besar di
                    keyboard sedang menyala atau tidak.
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="subtitle1" className="mb-1 font-bold text-orange-500">
                    Halaman Tidak Muncul
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary">
                    Periksa apakah kabel internet atau sambungan internet Bapak dan Ibu sedang aktif. Jika masih tidak
                    bisa, cobalah tutup aplikasinya dan buka kembali dari awal.
                  </Typography>
                </Grid>
              </Grid>
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
