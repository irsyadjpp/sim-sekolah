import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Card, CardContent, Tab, Tabs, Typography } from "@mui/material";

export default function TeacherWorkloadPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("workload.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("workload.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/academic">
            {t("workload.breadcrumb-academic")}
          </Link>
          <Typography variant="body2">{t("workload.breadcrumb-workload")}</Typography>
        </Breadcrumbs>
      </Box>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="workload tabs">
            <Tab label={t("workload.tab-overview")} />
            <Tab label={t("workload.tab-teaching-load")} />
            <Tab label={t("workload.tab-assessment")} />
            <Tab label={t("workload.tab-interventions")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("workload.overview-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.overview-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("workload.teaching-load-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.teaching-load-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("workload.assessment-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.assessment-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("workload.interventions-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.interventions-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("workload.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
