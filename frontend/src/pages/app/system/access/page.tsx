import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Box, Breadcrumbs, Card, CardContent, Grid, Typography } from "@mui/material";

export default function AccessHubPage() {
  const { t } = useTranslation();

  const cards = [
    {
      titleKey: "access-hub.card-users-title",
      descKey: "access-hub.card-users-desc",
      href: "/system/access/users",
      icon: (
        <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
          />
        </svg>
      ),
      color: "#3b82f6",
      bgColor: "rgba(59, 130, 246, 0.08)",
    },
    {
      titleKey: "access-hub.card-roles-title",
      descKey: "access-hub.card-roles-desc",
      href: "/system/access/roles",
      icon: (
        <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
          />
        </svg>
      ),
      color: "#10b981",
      bgColor: "rgba(16, 185, 129, 0.08)",
    },
    {
      titleKey: "access-hub.card-audit-title",
      descKey: "access-hub.card-audit-desc",
      href: "/system/access/security",
      icon: (
        <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
          />
        </svg>
      ),
      color: "#8b5cf6",
      bgColor: "rgba(139, 92, 246, 0.08)",
    },
  ];

  return (
    <Box sx={{ pb: 6 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h1" component="h1" sx={{ fontWeight: "bold", mb: 1, fontSize: "2rem" }}>
          {t("access-hub.title")}
        </Typography>
        <Breadcrumbs>
          <Link to="/dashboards/default" style={{ textDecoration: "none", color: "inherit" }}>
            {t("common-ui.home")}
          </Link>
          <Link to="/system" style={{ textDecoration: "none", color: "inherit" }}>
            {t("common-ui.system")}
          </Link>
          <Typography color="text.secondary" variant="body2">
            {t("menu-access-rights")}
          </Typography>
        </Breadcrumbs>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2, maxWidth: "700px" }}>
          {t("access-hub.welcome")}
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {cards.map((card) => (
          <Grid key={card.href} size={{ xs: 12, md: 4 }}>
            <Link to={card.href} style={{ textDecoration: "none", color: "inherit" }}>
              <Card
                sx={{
                  borderRadius: "20px",
                  boxShadow: "0 4px 20px 0 rgba(0,0,0,0.04)",
                  border: "1px solid rgba(0,0,0,0.08)",
                  transition: "all 0.3s ease-in-out",
                  height: "100%",
                  cursor: "pointer",
                  display: "flex",
                  flexDirection: "column",
                  position: "relative",
                  overflow: "hidden",
                  "&:hover": {
                    transform: "translateY(-6px)",
                    boxShadow: "0 12px 30px 0 rgba(0,0,0,0.1)",
                    borderColor: card.color,
                    "& .action-btn": {
                      color: card.color,
                      transform: "translateX(4px)",
                    },
                  },
                }}
              >
                <Box
                  sx={{ position: "absolute", top: 0, left: 0, height: "4px", width: "100%", bgcolor: card.color }}
                />

                <CardContent sx={{ p: 4, display: "flex", flexDirection: "column", flexGrow: 1 }}>
                  <Box
                    sx={{
                      width: "60px",
                      height: "60px",
                      borderRadius: "16px",
                      bgcolor: card.bgColor,
                      color: card.color,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      mb: 3,
                    }}
                  >
                    {card.icon}
                  </Box>

                  <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1.5, color: "text.primary" }}>
                    {t(card.titleKey)}
                  </Typography>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 4, lineHeight: 1.6, flexGrow: 1 }}>
                    {t(card.descKey)}
                  </Typography>

                  <Box
                    className="action-btn"
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      fontWeight: "bold",
                      color: "text.secondary",
                      fontSize: "0.9rem",
                      transition: "all 0.2s ease-in-out",
                    }}
                  >
                    {t("common-ui.open-settings")}
                    <svg
                      width="18"
                      height="18"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth="2.5"
                      style={{ marginLeft: "6px" }}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </Box>
                </CardContent>
              </Card>
            </Link>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
