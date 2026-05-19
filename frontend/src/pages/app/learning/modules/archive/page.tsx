import { Link } from "react-router-dom";

import { Breadcrumbs, Grid, Typography } from "@mui/material";

export default function Page() {
  return (
    <Grid container spacing={5}>
      <Grid size={{ xs: 12 }} className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          Arsip
        </Typography>
        <Breadcrumbs>
          <Link color="inherit" to="/dashboards/default">
            Home
          </Link>
          <Link color="inherit" to="/learning">
            Pembelajaran
          </Link>
          <Link color="inherit" to="/learning/modules">
            Modul
          </Link>
          <Typography variant="body2">Arsip</Typography>
        </Breadcrumbs>
      </Grid>
      <Grid size={{ xs: 12 }}>
        <Typography variant="body1">Halaman untuk Arsip masih dalam pengembangan.</Typography>
      </Grid>
    </Grid>
  );
}
