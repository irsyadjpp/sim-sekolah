import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-file-structure" />
    </Box>
  );
};

export default function DocsGettingStartedFileStructure() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const sections = [
    {
      title: "Halaman Utama",
      description:
        "Halaman pertama yang Bapak dan Ibu lihat. Isinya ringkasan jumlah siswa, jumlah guru, dan kabar terbaru dari sekolah.",
      subItems: ["Data Jumlah Siswa & Guru", "Kabar Sekolah", "Pemberitahuan Baru"],
    },
    {
      title: "Bagian Pengajaran",
      description: "Tempat untuk mengatur semua urusan belajar mengajar di sekolah.",
      subItems: [
        "Guru & Pegawai: Berisi daftar semua orang yang bekerja di sekolah.",
        "Cara Belajar: Tempat mengatur tujuan belajar siswa (Kurikulum Merdeka).",
        "Jadwal: Tempat mengatur pembagian waktu dan ruangan kelas.",
      ],
    },
    {
      title: "Bagian Siswa",
      description: "Tempat khusus untuk mengurus semua hal tentang siswa.",
      subItems: [
        "Pendaftaran: Tempat mendaftarkan siswa baru ke sekolah.",
        "Daftar Nama: Mencari dan merapikan data identitas siswa.",
        "Keadaan Siswa: Melihat siapa saja yang aktif, lulus, atau pindah sekolah.",
      ],
    },
    {
      title: "Pusat Bantuan",
      description: "Kumpulan tulisan dan petunjuk cara menggunakan halaman ini agar Bapak dan Ibu tidak bingung.",
      subItems: ["Petunjuk Pengguna", "Tanya Jawab", "Kabar Pembaruan"],
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
              Mengenal Menu Pilihan
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Daftar Menu</Typography>
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
                Memahami Bagian-Bagian Halaman
              </Typography>
              <Typography variant="body1" className="text-text-secondary mb-10 text-lg">
                Halaman ini dibuat sesederhana mungkin agar Bapak dan Ibu mudah menemukan apa yang dicari. Berikut
                adalah penjelasan isi dari setiap pilihan menu yang ada:
              </Typography>

              <Grid container spacing={4}>
                {sections.map((section, index) => (
                  <Grid key={index} size={{ xs: 12, md: 6 }}>
                    <Box className="h-full rounded-3xl border border-slate-100 bg-slate-50 p-6">
                      <Typography variant="h5" className="text-primary mb-3 font-bold">
                        {section.title}
                      </Typography>
                      <Typography variant="body2" className="text-text-secondary mb-4 leading-relaxed">
                        {section.description}
                      </Typography>
                      <Box className="flex flex-col gap-2">
                        {section.subItems.map((sub, i) => (
                          <Typography
                            key={i}
                            variant="caption"
                            className="flex items-center gap-2 font-bold text-slate-600"
                          >
                            <Box className="h-1.5 w-1.5 rounded-full bg-slate-300" />
                            {sub}
                          </Typography>
                        ))}
                      </Box>
                    </Box>
                  </Grid>
                ))}
              </Grid>

              <Divider className="my-10" />

              <Typography variant="h6" className="mb-4 font-bold">
                Tips Mencari Data
              </Typography>
              <Typography variant="body2" className="text-text-secondary">
                Gunakan pilihan yang ada di sebelah kiri untuk berpindah-pindah bagian. Bapak dan Ibu juga bisa
                mengetikkan nama siswa di kotak pencarian di bagian atas untuk menemukan data dengan cepat.
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
