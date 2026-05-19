import { Link } from "react-router-dom";

import {
  AnchorOutlined,
  AutoGraphOutlined,
  ParkOutlined,
  StarsOutlined,
  VisibilityOutlined,
} from "@mui/icons-material";
import { Avatar, Box, Breadcrumbs, Card, CardContent, Grid, Typography } from "@mui/material";

export default function Page() {
  return (
    <Grid container spacing={4}>
      <Grid size={{ xs: 12 }}>
        <Typography variant="h1" component="h1" className="mb-2">
          Visi Sekolah
        </Typography>
        <Breadcrumbs>
          <Link color="inherit" to="/home">
            Beranda
          </Link>
          <Typography color="inherit">Profil</Typography>
          <Typography variant="body2">Visi</Typography>
        </Breadcrumbs>
      </Grid>

      <Grid size={{ xs: 12 }}>
        <Card className="border-divider mt-4 overflow-hidden rounded-[20px] border shadow-sm">
          <Box className="bg-primary/5 border-divider border-b p-8 text-center">
            <Avatar className="bg-primary mx-auto mb-4 h-16 w-16 text-white">
              <VisibilityOutlined fontSize="large" />
            </Avatar>
            <Typography variant="h4" className="text-primary mb-2 font-bold italic">
              "Terwujudnya Generasi yang Berakhlak Mulia, Cerdas, Tangguh, dan Berwawasan Lingkungan Bahari Berlandaskan
              Profil Pelajar Pancasila."
            </Typography>
          </Box>
          <CardContent className="p-8">
            <Typography variant="h5" className="mb-6 font-bold">
              Makna Visi
            </Typography>

            <Grid container spacing={4}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-success/10 text-success">
                    <StarsOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      Berakhlak Mulia
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Mengakar pada kuatnya nilai-nilai agama Islam dan tradisi luhur masyarakat Bonerate.
                    </Typography>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-info/10 text-info">
                    <AutoGraphOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      Cerdas
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Komitmen sekolah untuk terus meningkatkan literasi dan numerasi meski berada di wilayah kepulauan
                      yang terluar.
                    </Typography>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-warning/10 text-warning">
                    <AnchorOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      Tangguh
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Menggambarkan daya juang (resiliensi) siswa yang terbiasa menghadapi tantangan alam dan
                      keterbatasan infrastruktur.
                    </Typography>
                  </Box>
                </Box>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Box className="flex gap-4">
                  <Avatar className="bg-primary/10 text-primary">
                    <ParkOutlined />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" className="mb-1 font-bold">
                      Berwawasan Lingkungan Bahari
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Kesadaran bahwa siswa hidup di ekosistem pesisir/kepulauan, sehingga mereka harus mencintai dan
                      mampu menjaga potensi laut serta alam sekitarnya.
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
