import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiArrowRight from "@/icons/nexture/ni-arrow-right";
import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-introduction" />
    </Box>
  );
};

export default function DocsWelcomeIntroduction() {
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
              Kenali Lebih Dekat SIM Sekolah
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Tentang Sekolah</Typography>
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
              <Typography variant="h3" className="text-primary mb-4 font-black">
                UPT SDI BONERATE NO 85 KEPULAUAN SELAYAR
              </Typography>
              <Typography variant="h6" className="text-text-secondary mb-8">
                Halaman Pengelolaan Sekolah Berbasis Kurikulum Merdeka
              </Typography>

              <Box className="mb-10 rounded-3xl border border-slate-100 bg-slate-50 p-6">
                <Grid container spacing={2}>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="caption" className="block font-bold tracking-wider text-slate-400 uppercase">
                      Nomor Induk Sekolah (NPSN)
                    </Typography>
                    <Typography variant="body1" className="font-bold">
                      40304877
                    </Typography>
                  </Grid>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="caption" className="block font-bold tracking-wider text-slate-400 uppercase">
                      Jenis Sekolah
                    </Typography>
                    <Typography variant="body1" className="font-bold">
                      Sekolah Dasar Negeri
                    </Typography>
                  </Grid>
                  <Grid size={12}>
                    <Typography variant="caption" className="block font-bold tracking-wider text-slate-400 uppercase">
                      Lokasi Sekolah
                    </Typography>
                    <Typography variant="body1" className="font-bold">
                      Jalan Majapahit No. 312, Desa Bonerate, Kec. Pasimarannu, Kab. Kepulauan Selayar, Prov. Sulawesi
                      Selatan
                    </Typography>
                  </Grid>
                </Grid>
              </Box>

              <Typography variant="body1" className="text-text-secondary mb-8 text-lg leading-relaxed">
                Halaman ini dibuat khusus untuk membantu Bapak dan Ibu Guru dalam mengelola kegiatan sekolah sesuai
                dengan **Kurikulum Merdeka**. Melalui cara **Pembelajaran Mendalam**, kita ingin memastikan setiap siswa
                mendapatkan perhatian belajar yang tepat dan bermakna.
              </Typography>

              <Divider className="my-10" />

              <Grid container spacing={6}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="h5" className="mb-4 font-bold">
                    Kurikulum Merdeka
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary leading-relaxed">
                    Membantu mengatur langkah-langkah belajar siswa yang lebih luwes. Bapak dan Ibu bisa menyesuaikan
                    apa yang ingin dicapai siswa sesuai dengan kemampuan mereka masing-masing.
                  </Typography>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="h5" className="mb-4 font-bold">
                    Pembelajaran Mendalam
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary leading-relaxed">
                    Tersedia asisten pintar yang membantu menganalisis cara belajar siswa, sehingga pembelajaran tidak
                    hanya sekadar menghafal, tapi benar-benar dipahami.
                  </Typography>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="h5" className="mb-4 font-bold">
                    Pusat Data Warga Sekolah
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary leading-relaxed">
                    Semua informasi tentang siswa dan rekan kerja tersimpan rapi dan aman dalam satu tempat. Mencari
                    data pun menjadi lebih cepat dan mudah.
                  </Typography>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="h5" className="mb-4 font-bold">
                    Budaya Lokal Bonerate
                  </Typography>
                  <Typography variant="body2" className="text-text-secondary leading-relaxed">
                    Tetap mengedepankan nilai-nilai luhur Kepulauan Selayar dalam setiap materi ajar, agar siswa tetap
                    mencintai budayanya sendiri di tengah perkembangan zaman.
                  </Typography>
                </Grid>
              </Grid>

              <Box className="mt-12">
                <Button
                  variant="contained"
                  color="primary"
                  size="large"
                  endIcon={<NiArrowRight />}
                  to="/home"
                  component={Link}
                  className="rounded-2xl px-10 py-4 font-black shadow-xl"
                >
                  Mulai Gunakan Halaman Ini
                </Button>
              </Box>
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
