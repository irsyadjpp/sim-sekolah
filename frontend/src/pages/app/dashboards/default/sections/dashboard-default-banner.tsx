import { Box, Button, Card, CardContent, Typography } from "@mui/material";

import IllustrationConfigure from "@/icons/illustrations/illustration-configure";
import NiBasket from "@/icons/nexture/ni-basket";
import NiPalette from "@/icons/nexture/ni-palette";

export default function DashboardDefaultBanner() {
  const handleConfigureButtonClick = () => {
    const themeCustomizationButton = document.getElementById("themeCustomization");
    if (themeCustomizationButton) {
      themeCustomizationButton.click();
    }
  };
  return (
    <>
      <Typography variant="h6" component="h6" className="mb-3">
        Pengaturan Cepat
      </Typography>

      <Card>
        <CardContent className="flex h-full flex-col items-start justify-between">
          <Box className="flex w-full flex-col md:flex-row">
            <Box className="w-full md:w-6/12 xl:w-8/12">
              <Typography variant="h4" component="h4" className="card-title">
                Sesuaikan Tampilan
              </Typography>
              <Typography
                variant="body1"
                component="p"
                className="text-text-secondary text-center md:text-start xl:max-w-md"
              >
                Atur warna tema dan pilihan latar belakang untuk mempersonalisasi sistem ini. Anda juga bisa mengubah
                jenis menu, serta berpindah antara tata letak kotak (boxed) dan layar penuh (fluid).
              </Typography>
            </Box>
            <Box className="flex w-full justify-center md:w-6/12 md:justify-end xl:w-4/12">
              <IllustrationConfigure className="text-primary h-64 w-full max-w-xs object-contain" />
            </Box>
          </Box>
          <Box className="flex flex-row gap-1">
            <Button
              className="mx-auto md:mx-0"
              size="medium"
              color="primary"
              variant="contained"
              startIcon={<NiPalette size={"medium"} />}
              onClick={handleConfigureButtonClick}
            >
              Atur Tampilan
            </Button>

            <Button
              className="mx-auto md:mx-0"
              size="medium"
              color="primary"
              variant="outlined"
              startIcon={<NiBasket size={"medium"} />}
              href="/docs/welcome/introduction"
            >
              Bantuan
            </Button>
          </Box>
        </CardContent>
      </Card>
    </>
  );
}
