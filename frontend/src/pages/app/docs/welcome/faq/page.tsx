import DocsMenu from "../../sections/docs-menu";
import { useState } from "react";
import { Link } from "react-router-dom";

import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Breadcrumbs,
  Button,
  Drawer,
  Tooltip,
  Typography,
} from "@mui/material";
import { Grid } from "@mui/material";

import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiListCircle from "@/icons/nexture/ni-list-circle";

const MenuContent = () => {
  return (
    <Box className="flex flex-col gap-4">
      <DocsMenu selectedID="docs-faq" />
    </Box>
  );
};

export default function DocsWelcomeFaq() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenDrawer(newOpen);
  };

  const faqs = [
    {
      q: "Bagaimana cara mengatur Kurikulum Merdeka di halaman ini?",
      a: "Bapak dan Ibu dapat menggunakan bagian Akademik untuk mengatur apa yang harus dicapai siswa. Caranya sangat mudah dan bisa disesuaikan dengan kebutuhan kelas masing-masing.",
    },
    {
      q: "Apa yang dimaksud dengan Pembelajaran Mendalam?",
      a: "Ini adalah cara belajar yang dibantu oleh asisten pintar untuk mengenali kemampuan setiap siswa. Tujuannya agar siswa benar-benar paham materi, bukan hanya sekadar menghafal.",
    },
    {
      q: "Bagaimana cara mendaftarkan siswa baru?",
      a: "Buka menu 'Siswa' lalu pilih 'Tambah Siswa'. Masukkan data dari Kartu Keluarga dan KTP orang tua ke dalam kotak-kotak yang tersedia secara lengkap.",
    },
    {
      q: "Dapatkah guru memasukkan materi khas Bonerate?",
      a: "Tentu bisa. Di bagian pengajaran, Bapak dan Ibu dapat menambahkan materi ajar yang berkaitan dengan kehidupan sehari-hari di Bonerate dan Kepulauan Selayar.",
    },
    {
      q: "Apakah data sekolah sudah benar?",
      a: "Ya, halaman ini sudah disiapkan khusus untuk SDI Bonerate No. 85. Alamat dan nomor identitas sekolah (NPSN) sudah terisi secara otomatis sesuai data resmi.",
    },
    {
      q: "Bagaimana jika saya belum selesai mengisi data yang banyak?",
      a: "Jangan khawatir. Bapak dan Ibu bisa menekan tombol 'Simpan Sementara' di bagian bawah. Dengan begitu, pekerjaan bisa dilanjutkan besok tanpa harus mengulang dari awal.",
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
              Tanya Jawab (FAQ)
            </Typography>
            <Breadcrumbs>
              <Link color="inherit" to="/home">
                Beranda
              </Link>
              <Link color="inherit" to="/docs">
                Pusat Bantuan
              </Link>
              <Typography variant="body2">Tanya Jawab</Typography>
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
          <Box className="flex flex-col gap-4">
            {faqs.map((faq, index) => (
              <Accordion key={index} className="overflow-hidden rounded-3xl border-none shadow-sm before:hidden">
                <AccordionSummary
                  expandIcon={<NiChevronDownSmall />}
                  className="px-8 py-4 transition-colors hover:bg-slate-50"
                >
                  <Typography variant="h6" className="font-bold text-slate-800">
                    {faq.q}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails className="bg-slate-50/50 px-8 pb-6">
                  <Typography variant="body1" className="text-text-secondary leading-relaxed">
                    {faq.a}
                  </Typography>
                </AccordionDetails>
              </Accordion>
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
