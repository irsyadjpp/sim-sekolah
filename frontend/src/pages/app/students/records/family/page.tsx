import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Breadcrumbs, Grid, Typography } from "@mui/material";

export default function Page() {
  const { t } = useTranslation();

  return (
    <Grid container spacing={5}>
      <Grid size={{ xs: 12 }} className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("students.records.family.title")}
        </Typography>
        <Breadcrumbs>
          <Link color="inherit" to="/dashboards/default">
            {t("common-ui.home")}
          </Link>
          <Link color="inherit" to="/students">
            {t("students.breadcrumb")}
          </Link>
          <Link color="inherit" to="/students/records">
            {t("students.records.breadcrumb")}
          </Link>
          <Typography variant="body2">{t("students.records.family.title")}</Typography>
        </Breadcrumbs>
      </Grid>
      <Grid size={{ xs: 12 }}>
        <Typography variant="body1">{t("students.records.under-development")}</Typography>
      </Grid>
    </Grid>
  );
}
