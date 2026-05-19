import { Link } from "react-router-dom";

import { Breadcrumbs, Grid, Typography } from "@mui/material";

export default function Page() {
  return (
    <Grid container spacing={5}>
      <Grid size={{ xs: 12 }} className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          Alam
        </Typography>
        <Breadcrumbs>
          <Link color="inherit" to="/dashboards/default">
            Home
          </Link>
          <Link color="inherit" to="/locality">
            Lokalitas
          </Link>
          <Link color="inherit" to="/locality/environment">
            Lingkungan
          </Link>
          <Typography variant="body2">Alam</Typography>
        </Breadcrumbs>
      </Grid>
      <Grid size={{ xs: 12 }}>
        <Typography variant="body1">Halaman untuk Alam masih dalam pengembangan.</Typography>
      </Grid>
    </Grid>
  );
}
