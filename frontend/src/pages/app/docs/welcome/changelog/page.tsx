import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Button, Card, CardContent, Divider, Drawer, Tooltip, Typography } from "@mui/material";
import { Grid } from "@mui/material";

import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-changelog" />
    </Box>
  );
};

export default function DocsWelcomeChangelog() {
  const [openDrawer, setOpenDrawer] = useState(false);
  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const updates = [
    {
      version: "Pembaruan Mei 2026 - Merapikan Daftar Guru",
      date: "Mei 2026",
      items: [
        "Semua data Guru dan Pegawai kini disatukan dalam satu tempat agar lebih rapi.",
        "Kotak isian saat mendaftarkan guru baru dibuat lebih lapang dan hanya menjadi 2 kolom supaya mudah dibaca.",
        "Tombol 'Simpan Sementara' dan 'Simpan Data' kini selalu muncul di setiap langkah pengisian.",
        "Pilihan bahasa (Indonesia & Inggris) sudah tersedia lengkap di semua kotak isian.",
        "Pesan jika ada kesalahan pengisian kini menggunakan bahasa yang lebih santun dan mudah dimengerti.",
      ],
    },
    {
      version: "Pembaruan April 2026 - Penataan Cara Belajar",
      date: "April 2026",
      items: [
        "Mulai disiapkan bagian untuk mengatur tujuan belajar siswa (Kurikulum Merdeka).",
        "Penataan jadwal pelajaran dan pembagian ruangan kelas untuk siswa.",
        "Penyelarasan data sekolah dengan pusat data pendidikan.",
        "Peningkatan keamanan agar data sekolah tidak bisa dibuka oleh orang sembarangan.",
      ],
    },
    {
      version: "Pembaruan Maret 2026 - Peresmian Halaman Sekolah",
      date: "Maret 2026",
      items: [
        "Halaman utama yang menampilkan ringkasan data sekolah sudah bisa digunakan.",
        "Bagian pendaftaran siswa baru secara mandiri mulai dibuka.",
        "Pengisian data profil lengkap UPT SDI Bonerate No 85.",
        "Tempat penyimpanan dokumen sekolah sudah disiapkan agar tidak tercecer.",
      ],
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
              Kabar Terbaru SDI Bonerate No 85
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Kabar Terbaru</Typography>
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
          <Box className="flex flex-col gap-6">
            {updates.map((update, index) => (
              <Card key={index} className="rounded-3xl border-none shadow-sm">
                <CardContent className="p-8">
                  <Box className="mb-4 flex flex-row items-start justify-between">
                    <Typography variant="h5" className="text-primary font-black">
                      {update.version}
                    </Typography>
                    <Typography
                      variant="body2"
                      className="rounded-full bg-slate-100 px-4 py-1 font-bold text-slate-500"
                    >
                      {update.date}
                    </Typography>
                  </Box>
                  <Divider className="mb-6 opacity-50" />
                  <ul className="m-0 flex list-none flex-col gap-3 p-0">
                    {update.items.map((item, i) => (
                      <li key={i} className="text-text-secondary flex items-start gap-3">
                        <Box className="bg-primary mt-2 h-2 w-2 shrink-0 rounded-full" />
                        <Typography variant="body1">{item}</Typography>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </Box>
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
