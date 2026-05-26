import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Card, CardContent, Tab, Tabs, Typography } from "@mui/material";

export default function CharacterGrowthPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("character-growth.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("character-growth.breadcrumb-home")}
          </Link>
          <Link color="inherit" to="/students">
            {t("character-growth.breadcrumb-students")}
          </Link>
          <Typography variant="body2">{t("character-growth.breadcrumb-character-growth")}</Typography>
        </Breadcrumbs>
      </Box>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="character-growth tabs">
            <Tab label={t("character-growth.tab-growth-tracking")} />
            <Tab label={t("character-growth.tab-assessments")} />
            <Tab label={t("character-growth.tab-dimensions")} />
            <Tab label={t("character-growth.tab-milestones")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("character-growth.growth-tracking-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.growth-tracking-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("character-growth.assessments-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.assessments-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("character-growth.dimensions-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.dimensions-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.coming-soon")}
              </Typography>
            </Box>
          )}

          {tabValue === 3 && (
            <Box className="mt-4">
              <Typography variant="h6">{t("character-growth.milestones-title")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.milestones-description")}
              </Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("character-growth.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
