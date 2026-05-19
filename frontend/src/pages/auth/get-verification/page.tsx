import { Link, useNavigate } from "react-router-dom";

import {
  Box,
  Button,
  Divider,
  FormControl,
  FormControlLabel,
  Paper,
  Radio,
  RadioGroup,
  Typography,
} from "@mui/material";

import Logo from "@/components/logo/logo";
import { RadiobuttonSmallChecked, RadiobuttonSmallEmptyOutlined } from "@/icons/form/mui-radiobutton";

export default function Page() {
  const navigate = useNavigate();
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    navigate("/");
  };

  return (
    <Box className="bg-waves flex min-h-screen w-full items-center justify-center bg-cover bg-center p-4">
      <Paper elevation={3} className="bg-background-paper shadow-darker-xs w-[32rem] max-w-full rounded-4xl py-14">
        <Box className="flex flex-col gap-4 px-8 sm:px-14">
          <Box className="flex flex-col">
            <Box className="mb-14 flex justify-center">
              <Logo classNameMobile="hidden" />
            </Box>

            <Box className="flex flex-col gap-10">
              <Box className="flex flex-col">
                <Typography variant="h1" component="h1" className="mb-2">
                  Verifikasi
                </Typography>
                <Typography variant="body1" className="text-text-primary">
                  Silakan pilih bagaimana Anda ingin mendapatkan kode verifikasi.
                </Typography>
              </Box>

              <Box className="flex flex-col gap-5">
                <Box component={"form"} onSubmit={handleSubmit} className="flex flex-col">
                  <RadioGroup name="row-radio-buttons-group">
                    <FormControl className="mb-2">
                      <FormControlLabel
                        value="phone"
                        control={
                          <Radio
                            size="small"
                            icon={<RadiobuttonSmallEmptyOutlined />}
                            checkedIcon={<RadiobuttonSmallChecked />}
                          />
                        }
                        label="Kirim ke nomor telepon saya: ****8714"
                      />
                    </FormControl>
                    <FormControl className="mb-2">
                      <FormControlLabel
                        value="email"
                        control={
                          <Radio
                            size="small"
                            icon={<RadiobuttonSmallEmptyOutlined />}
                            checkedIcon={<RadiobuttonSmallChecked />}
                          />
                        }
                        label="Kirim ke alamat email saya: ne****@gmail.com"
                      />
                    </FormControl>
                  </RadioGroup>

                  <Box className="flex flex-col gap-2">
                    <Button type="submit" variant="contained" className="mb-4">
                      Lanjutkan
                    </Button>
                  </Box>

                  <Typography variant="body2" className="text-text-secondary">
                    Dengan mengklik Lanjutkan atau Masuk dengan Google, Anda menyetujui{" "}
                    <Link target="_blank" to="/auth/terms-and-conditions" className="link-primary link-underline-hover">
                      Syarat dan Ketentuan
                    </Link>{" "}
                    dan{" "}
                    <Link target="_blank" to="/auth/privacy-policy" className="link-primary link-underline-hover">
                      Kebijakan Privasi
                    </Link>
                    .
                  </Typography>
                </Box>
              </Box>
              <Divider className="text-text-secondary my-0 text-sm"></Divider>
              <Box className="flex flex-col">
                <Typography variant="h6" component="h6">
                  Sudah memiliki kode?
                </Typography>
                <Typography variant="body1" className="text-text-secondary">
                  Jika Anda memiliki kode, silakan{" "}
                  <Link to="/auth/set-verification" className="link-primary link-underline-hover">
                    kirim
                  </Link>{" "}
                  di sini.
                </Typography>
              </Box>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
