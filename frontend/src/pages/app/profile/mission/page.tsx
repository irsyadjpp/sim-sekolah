import { Link } from "react-router-dom";

import {
  EmojiFlagsOutlined,
  HandshakeOutlined,
  LightbulbOutlined,
  LocalLibraryOutlined,
  SailingOutlined,
  SchoolOutlined,
  StarsOutlined,
} from "@mui/icons-material";
import { Avatar, Box, Breadcrumbs, Card, CardContent, Divider, Grid, Typography } from "@mui/material";

export default function Page() {
  return (
    <Grid container spacing={4}>
      <Grid size={{ xs: 12 }}>
        <Typography variant="h1" component="h1" className="mb-2">
          Misi & Tujuan Sekolah
        </Typography>
        <Breadcrumbs>
          <Link color="inherit" to="/home">
            Beranda
          </Link>
          <Typography color="inherit">Profil</Typography>
          <Typography variant="body2">Misi</Typography>
        </Breadcrumbs>
      </Grid>

      <Grid size={{ xs: 12 }}>
        <Card className="border-divider mt-4 overflow-hidden rounded-[20px] border shadow-sm">
          <Box className="bg-primary flex items-center gap-4 p-6 text-white">
            <Avatar className="h-14 w-14 bg-white/20 text-white">
              <EmojiFlagsOutlined fontSize="large" />
            </Avatar>
            <Typography variant="h4" className="mb-0 font-bold">
              Misi UPT SDI Bonerate No. 85
            </Typography>
          </Box>
          <CardContent className="p-8">
            <Typography variant="body1" className="text-text-secondary mb-8">
              Untuk mewujudkan Visi sekolah, UPT SDI Bonerate No. 85 Kepulauan Selayar menetapkan Misi sebagai berikut:
            </Typography>

            <Grid container spacing={4}>
              <Grid size={{ xs: 12 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-success/10 text-success mt-1 shrink-0">
                    <StarsOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      1. Pembentukan Karakter dan Nilai Agama
                    </Typography>
                    <ul className="text-text-secondary list-disc space-y-1 pl-5">
                      <li>
                        Menanamkan keimanan dan ketakwaan kepada Tuhan Yang Maha Esa melalui pembiasaan ibadah rutin di
                        sekolah (seperti salat dhuha/dhuhur berjamaah dan perayaan hari besar Islam).
                      </li>
                      <li>
                        Mengintegrasikan kearifan lokal (seperti semangat gotong royong dan nilai kesopanan santun) ke
                        dalam perilaku keseharian siswa di sekolah.
                      </li>
                    </ul>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-info/10 text-info mt-1 shrink-0">
                    <LocalLibraryOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      2. Peningkatan Kualitas Pembelajaran (Kecerdasan)
                    </Typography>
                    <ul className="text-text-secondary list-disc space-y-1 pl-5">
                      <li>
                        Menyelenggarakan proses pembelajaran yang Aktif, Inovatif, Kreatif, Efektif, dan Menyenangkan
                        (PAIKEM) yang berpusat pada siswa.
                      </li>
                      <li>
                        Mengoptimalkan ketersediaan fasilitas sekolah untuk memacu kemampuan literasi (membaca/menulis)
                        dan numerasi siswa agar mampu bersaing dengan siswa di daratan utama kabupaten.
                      </li>
                    </ul>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-warning/10 text-warning mt-1 shrink-0">
                    <SchoolOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      3. Pengembangan Ketangguhan dan Kemandirian
                    </Typography>
                    <ul className="text-text-secondary list-disc space-y-1 pl-5">
                      <li>
                        Melatih kedisiplinan, kemandirian, dan keterampilan memecahkan masalah melalui kegiatan
                        kepramukaan dan ekstrakurikuler lainnya.
                      </li>
                      <li>
                        Membekali siswa dengan kecakapan hidup (life skills) dasar yang relevan dengan kondisi alam dan
                        dunia kerja lokal di masa depan.
                      </li>
                    </ul>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-primary/10 text-primary mt-1 shrink-0">
                    <SailingOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      4. Penanaman Wawasan Lingkungan Bahari
                    </Typography>
                    <ul className="text-text-secondary list-disc space-y-1 pl-5">
                      <li>
                        Mengintegrasikan pendidikan lingkungan hidup, khususnya pelestarian ekosistem pesisir dan laut,
                        ke dalam mata pelajaran muatan lokal atau proyek profil pelajar Pancasila.
                      </li>
                      <li>
                        Membiasakan gerakan kebersihan lingkungan sekolah dan aksi peduli pesisir (seperti menjaga
                        kebersihan pantai di sekitar Desa Bonerate).
                      </li>
                    </ul>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-secondary/10 text-secondary mt-1 shrink-0">
                    <HandshakeOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      5. Sinergi dengan Ekosistem Masyarakat
                    </Typography>
                    <ul className="text-text-secondary list-disc space-y-1 pl-5">
                      <li>
                        Membangun kemitraan yang kuat dan harmonis antara pihak sekolah, orang tua wali, tokoh
                        masyarakat, dan pemerintah desa (Desa Bonerate) untuk mendukung suksesnya program pendidikan.
                      </li>
                    </ul>
                  </Box>
                </Box>
              </Grid>
            </Grid>

            <Divider className="my-8" />

            <Box className="bg-action-hover border-divider rounded-xl border p-6">
              <Box className="mb-3 flex items-center gap-2">
                <LightbulbOutlined color="primary" />
                <Typography variant="h5" className="font-bold">
                  Tujuan Sekolah (Output yang Diharapkan)
                </Typography>
              </Box>
              <Typography variant="body1" className="text-text-secondary leading-relaxed">
                Rumusan visi dan misi ini dirancang agar lulusan UPT SDI Bonerate No. 85 tidak hanya memiliki nilai
                akademik yang baik, tetapi juga memiliki mental yang pantang menyerah, bangga akan identitas mereka
                sebagai masyarakat kepulauan Selayar, serta siap beradaptasi dengan kemajuan zaman tanpa meninggalkan
                nilai-nilai luhur budaya pesisir.
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
