import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  AlertTitle,
  Box,
  Button,
  CircularProgress,
  Divider,
  FormControl,
  FormLabel,
  Input,
  Paper,
  Typography,
} from "@mui/material";

import Logo from "@/components/logo/logo";

export default function Page() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setApiError(null);
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8080/api/v1/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const result = await response.json();
      if (!response.ok || !result.success) {
        throw new Error(result.message || "Terjadi kesalahan, coba lagi.");
      }
      navigate("/auth/password-sent");
    } catch (err: any) {
      setApiError(err.message);
    } finally {
      setLoading(false);
    }
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
                  Reset Kata Sandi
                </Typography>
                <Typography variant="body1" className="text-text-primary">
                  Dapatkan email tentang cara mengatur ulang kata sandi Anda dengan aman.
                </Typography>
              </Box>

              <Box className="flex flex-col gap-5">
                <Box component={"form"} onSubmit={handleSubmit} className="flex flex-col">
                  <FormControl className="outlined" variant="standard" size="small">
                    <FormLabel component="label">Email</FormLabel>
                    <Input
                      placeholder="contoh@email.com"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </FormControl>

                  {apiError && (
                    <Alert severity="error" className="mb-4">
                      <AlertTitle variant="subtitle2">Gagal Mengirim</AlertTitle>
                      {apiError}
                    </Alert>
                  )}
                  <Box className="flex flex-col gap-2">
                    <Button type="submit" variant="contained" className="mb-4" disabled={loading}>
                      {loading ? <CircularProgress size={20} color="inherit" /> : "Lanjutkan"}
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
                  Masuk
                </Typography>
                <Typography variant="body1" className="text-text-secondary">
                  Jika Anda sudah memiliki akun, silakan{" "}
                  <Link to="/" className="link-primary link-underline-hover">
                    masuk
                  </Link>
                  .
                </Typography>
              </Box>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
