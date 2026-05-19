import { Suspense, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { BrowserRouter, useLocation } from "react-router-dom";

import { Box, StyledEngineProvider } from "@mui/material";

import BackgroundWrapper from "@/components/layout/containers/background-wrapper";
import SnackbarWrapper from "@/components/layout/containers/snackbar-wrapper";
import LayoutContextProvider from "@/components/layout/layout-context";
import { AlertProvider } from "@/hooks/use-alert";
import { ConfirmProvider } from "@/hooks/use-confirm";
import { uxAnalytics } from "@/lib/ux-analytics";
import Loading from "@/pages/loading";
import AppRoutes from "@/routes";
import ThemeProvider from "@/theme/theme-provider";

const UXAnalyticsTracker = () => {
  const location = useLocation();

  useEffect(() => {
    const startTime = performance.now();
    const handleLoad = () => {
      const duration = performance.now() - startTime;
      uxAnalytics.trackPageLoad(location.pathname, duration);
    };

    const timer = setTimeout(handleLoad, 100);
    return () => clearTimeout(timer);
  }, [location.pathname]);

  return null;
};

const App = () => {
  const { i18n } = useTranslation();
  const direction = i18n.language === "ar" ? "rtl" : "ltr";

  return (
    <BrowserRouter>
      <UXAnalyticsTracker />
      <StyledEngineProvider enableCssLayer>
        <Box
          lang={i18n.language}
          dir={direction}
          className="font-mulish font-urbanist relative overflow-hidden antialiased"
        >
          {/* Initial loader */}
          <div id="initial-loader">
            <div className="spinner"></div>
          </div>
          {/* Initial loader end */}

          <ThemeProvider>
            <LayoutContextProvider>
              <BackgroundWrapper />
              <SnackbarWrapper>
                <AlertProvider>
                  <ConfirmProvider>
                    <Suspense fallback={<Loading />}>
                      {/* Routes */}
                      <AppRoutes />
                    </Suspense>
                  </ConfirmProvider>
                </AlertProvider>
              </SnackbarWrapper>
            </LayoutContextProvider>
          </ThemeProvider>
        </Box>
      </StyledEngineProvider>
    </BrowserRouter>
  );
};

export default App;
