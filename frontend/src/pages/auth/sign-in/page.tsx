import { useFormik } from "formik";
import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import * as yup from "yup";

import {
  Alert,
  AlertTitle,
  Box,
  Button,
  capitalize,
  Divider,
  FormControl,
  FormLabel,
  IconButton,
  Input,
  InputAdornment,
  Paper,
  Tooltip,
  Typography,
} from "@mui/material";

import Logo from "@/components/logo/logo";
import { DEFAULTS } from "@/config";
import NiCrossSquare from "@/icons/nexture/ni-cross-square";
import NiEyeClose from "@/icons/nexture/ni-eye-close";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import { apiClient } from "@/lib/api-client";

type InputErrorProps = {
  title: string;
};

const InputErrorTooltip = ({ title }: InputErrorProps) => {
  return (
    <Box className="relative">
      <Tooltip title={title} arrow className="absolute -top-1.5">
        <Button
          startIcon={<NiCrossSquare size="small" />}
          color="error"
          size="small"
          className="group icon-only bg-transparent! outline-0!"
        ></Button>
      </Tooltip>
    </Box>
  );
};

export default function Page() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const validationSchema = useMemo(
    () =>
      yup.object({
        email: yup.string().required(t("validation.required")).email(t("validation.email")),
        password: yup.string().required(t("validation.required")),
      }),
    [t],
  );
  const [submitted, setSubmitted] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // MFA states
  const [showMfa, setShowMfa] = useState(false);
  const [mfaPendingToken, setMfaPendingToken] = useState<string | null>(null);
  const [mfaSetup, setMfaSetup] = useState(false);
  const [mfaSecret, setMfaSecret] = useState("");
  const [mfaQrCodeUrl, setMfaQrCodeUrl] = useState("");
  const [otpCode, setOtpCode] = useState("");
  const [verifyingOtp, setVerifyingOtp] = useState(false);

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema,
    onSubmit: async (values) => {
      setApiError(null);
      try {
        const response = await apiClient.post("/api/v1/auth/login", {
          email: values.email,
          password: values.password,
        });

        const result = response.data;

        if (result.status !== "success") {
          throw new Error(result.message || t("auth.email-password-wrong"));
        }

        // Check if 2FA verification is required
        if (result.data && result.data.mfa_required) {
          setMfaPendingToken(result.data.temp_token);
          setMfaSetup(!!result.data.mfa_setup);
          setMfaSecret(result.data.secret || "");
          setMfaQrCodeUrl(result.data.qr_code_url || "");
          setShowMfa(true);
          return;
        }

        // Store token and user data in localStorage
        if (result.data) {
          const d = result.data;
          if (d.token) localStorage.setItem("accessToken", d.token);
          if (d.user) {
            localStorage.setItem("-user-data", JSON.stringify(d.user));

            // Immediately persist appearance settings
            if (d.user.theme_color) localStorage.setItem("-theme-color", d.user.theme_color);
            if (d.user.theme_mode) localStorage.setItem("-theme-mode", d.user.theme_mode);
            if (d.user.content_type) localStorage.setItem("-content-type", d.user.content_type);
            if (d.user.left_menu_type) localStorage.setItem("-left-menu-type", d.user.left_menu_type);
          }
        }

        navigate(DEFAULTS.appRoot);
      } catch (err: any) {
        const errMsg = err.response?.data?.message || err.message || t("auth.email-password-wrong");
        setApiError(errMsg);
      }
    },
    validateOnBlur: false,
    validateOnMount: false,
  });

  const handleVerifyMfa = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!otpCode || otpCode.length !== 6) {
      setApiError(t("mfa.login-error"));
      return;
    }
    setVerifyingOtp(true);
    setApiError(null);
    try {
      const response = await apiClient.post("/api/v1/auth/verify-2fa", {
        temp_token: mfaPendingToken,
        code: otpCode,
      });

      const result = response.data;

      if (result.status !== "success") {
        throw new Error(result.message || t("mfa.login-error"));
      }

      if (result.data) {
        const d = result.data;
        if (d.token) localStorage.setItem("accessToken", d.token);
        if (d.user) {
          localStorage.setItem("-user-data", JSON.stringify(d.user));
          if (d.user.theme_color) localStorage.setItem("-theme-color", d.user.theme_color);
          if (d.user.theme_mode) localStorage.setItem("-theme-mode", d.user.theme_mode);
          if (d.user.content_type) localStorage.setItem("-content-type", d.user.content_type);
          if (d.user.left_menu_type) localStorage.setItem("-left-menu-type", d.user.left_menu_type);
        }
      }

      navigate(DEFAULTS.appRoot);
    } catch (err: any) {
      const errMsg = err.response?.data?.message || err.message || t("mfa.login-error");
      setApiError(errMsg);
    } finally {
      setVerifyingOtp(false);
    }
  };

  const [showPassword, setShowPassword] = useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  const googleSVG = () => {
    return (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M19.6169 10.2876C19.6169 9.60932 19.5561 8.95714 19.443 8.33105H10.4343V12.0354H15.5822C15.3561 13.2267 14.6778 14.2354 13.6604 14.9137V17.3224H16.7648C18.5735 15.6528 19.6169 13.2006 19.6169 10.2876Z"
          fill="#4285F4"
        />
        <path
          d="M10.4346 19.6346C13.0172 19.6346 15.1825 18.7825 16.7651 17.3216L13.6607 14.9129C12.8086 15.4868 11.7216 15.8346 10.4346 15.8346C7.94768 15.8346 5.83464 14.1564 5.07812 11.8955H1.89551V14.3651C3.46942 17.4868 6.69551 19.6346 10.4346 19.6346Z"
          fill="#34A853"
        />
        <path
          d="M5.07832 11.8866C4.88702 11.3127 4.77398 10.704 4.77398 10.0692C4.77398 9.4344 4.88702 8.8257 5.07832 8.25179V5.78223H1.89572C1.24354 7.06918 0.869629 8.52136 0.869629 10.0692C0.869629 11.617 1.24354 13.0692 1.89572 14.3561L4.37398 12.4257L5.07832 11.8866Z"
          fill="#FBBC05"
        />
        <path
          d="M10.4346 4.31358C11.8433 4.31358 13.0955 4.80054 14.0955 5.73967L16.8346 3.00054C15.1738 1.45271 13.0172 0.504883 10.4346 0.504883C6.69551 0.504883 3.46942 2.65271 1.89551 5.78314L5.07812 8.25271C5.83464 5.99184 7.94768 4.31358 10.4346 4.31358Z"
          fill="#EA4335"
        />
      </svg>
    );
  };

  return (
    <Box className="bg-waves flex min-h-screen w-full items-center justify-center bg-cover bg-center p-4">
      <Paper elevation={3} className="bg-background-paper shadow-darker-xs w-lg max-w-full rounded-4xl py-14">
        <Box className="flex flex-col gap-4 px-8 sm:px-14">
          <Box className="flex flex-col">
            <Box className="mb-14 flex justify-center">
              <Logo classNameMobile="hidden" />
            </Box>

            <Box className="flex flex-col gap-10">
              {showMfa ? (
                <Box className="flex flex-col gap-6">
                  {mfaSetup ? (
                    <Box className="flex flex-col">
                      <Typography variant="h1" component="h1" className="text-primary mb-2 text-center font-bold">
                        Setup Keamanan 2FA
                      </Typography>
                      <Typography variant="body2" className="text-text-secondary mb-4 text-center leading-relaxed">
                        Akun Anda memerlukan verifikasi Dua Faktor (MFA). Silakan pindai QR code berikut menggunakan
                        aplikasi Authenticator Anda (seperti Google Authenticator, Microsoft Authenticator, dll).
                      </Typography>
                      {mfaQrCodeUrl && (
                        <Box className="mb-4 flex flex-col items-center justify-center rounded-3xl border border-slate-100 bg-white p-5 shadow-sm">
                          <img
                            src={`https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(mfaQrCodeUrl)}`}
                            alt="MFA QR Code"
                            className="mb-3 h-44 w-44 rounded-xl border border-slate-100 bg-white p-1"
                          />
                          <Typography
                            variant="caption"
                            className="text-text-secondary rounded-lg border border-slate-100 bg-slate-50 px-3 py-1.5 text-center font-mono select-all"
                          >
                            Kunci Manual: <strong>{mfaSecret}</strong>
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  ) : (
                    <Box className="flex flex-col">
                      <Typography variant="h1" component="h1" className="text-primary mb-2 text-center font-bold">
                        {t("mfa.login-title")}
                      </Typography>
                      <Typography variant="body1" className="text-text-secondary mb-4 text-center leading-relaxed">
                        {t("mfa.login-desc")}
                      </Typography>
                    </Box>
                  )}

                  <Box component="form" onSubmit={handleVerifyMfa} className="flex flex-col gap-5">
                    <FormControl variant="standard" size="small">
                      <FormLabel component="label" className="mb-2 flex flex-row justify-center font-medium">
                        {t("mfa.login-placeholder")}
                      </FormLabel>
                      <Input
                        id="otp"
                        name="otp"
                        placeholder="000000"
                        autoFocus
                        value={otpCode}
                        onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                        inputProps={{
                          style: { textAlign: "center", fontSize: "1.75rem", letterSpacing: "0.5rem", fontWeight: 700 },
                        }}
                      />
                    </FormControl>

                    {apiError && (
                      <Alert severity="error" icon={<NiCrossSquare />} className="neutral bg-background-paper/60! mb-2">
                        <AlertTitle variant="subtitle2">Verifikasi Gagal</AlertTitle>
                        <Typography variant="body2" className="text-text-primary">
                          {apiError}
                        </Typography>
                      </Alert>
                    )}

                    <Box className="flex flex-col gap-2">
                      <Button type="submit" variant="contained" disabled={verifyingOtp || otpCode.length !== 6}>
                        {verifyingOtp ? "Memverifikasi..." : "Verifikasi & Lanjutkan"}
                      </Button>
                      <Button
                        variant="outlined"
                        color="secondary"
                        onClick={() => {
                          setShowMfa(false);
                          setMfaPendingToken(null);
                          setMfaSetup(false);
                          setOtpCode("");
                          setApiError(null);
                        }}
                      >
                        Batal
                      </Button>
                    </Box>
                  </Box>
                </Box>
              ) : (
                <>
                  <Box className="flex flex-col">
                    <Typography variant="h1" component="h1" className="mb-2">
                      Masuk
                    </Typography>
                    <Typography variant="body1" className="text-text-primary">
                      Akses akun Anda dengan cepat dan aman untuk memulai.
                    </Typography>
                  </Box>

                  <Box className="flex flex-col gap-5">
                    <Box className="flex flex-col gap-2">
                      <Button variant="outlined" color="grey" className="w-full">
                        <Box className="me-2">{googleSVG()}</Box>Masuk dengan Google
                      </Button>
                    </Box>

                    <Divider className="text-text-secondary my-0 text-sm">ATAU</Divider>

                    <Box
                      component={"form"}
                      onSubmit={(event) => {
                        setSubmitted(true);
                        formik.handleSubmit(event);
                      }}
                      className="flex flex-col"
                    >
                      <FormControl className="outlined" variant="standard" size="small">
                        <FormLabel component="label" className="flex flex-row">
                          Email
                          {formik.touched.email && formik.errors.email && (
                            <InputErrorTooltip title={formik.errors.email} />
                          )}
                        </FormLabel>
                        <Input
                          id="email"
                          name="email"
                          placeholder="Masukkan alamat email anda"
                          value={formik.values.email}
                          onChange={formik.handleChange}
                          onBlur={formik.handleBlur}
                        />
                      </FormControl>

                      <FormControl className="outlined" variant="standard" size="small">
                        <FormLabel component="label" className="flex flex-row">
                          Kata Sandi
                          {formik.touched.password && formik.errors.password && (
                            <InputErrorTooltip title={formik.errors.password} />
                          )}
                        </FormLabel>
                        <Input
                          size="small"
                          id="password"
                          name="password"
                          placeholder="Masukkan kata sandi anda"
                          autoComplete="off"
                          value={formik.values.password}
                          onChange={formik.handleChange}
                          onBlur={formik.handleBlur}
                          type={showPassword ? "text" : "password"}
                          endAdornment={
                            <InputAdornment position="end">
                              <IconButton
                                onClick={handleClickShowPassword}
                                onMouseDown={handleMouseDownPassword}
                                onMouseUp={handleMouseUpPassword}
                              >
                                {showPassword ? (
                                  <NiEyeClose size="medium" className="text-text-secondary" />
                                ) : (
                                  <NiEyeOpen size="medium" className="text-text-secondary" />
                                )}
                              </IconButton>
                            </InputAdornment>
                          }
                        />
                      </FormControl>

                      {submitted && !formik.isValid && (
                        <Alert
                          severity="error"
                          icon={<NiCrossSquare />}
                          className="neutral bg-background-paper/60! mb-4"
                        >
                          <AlertTitle variant="subtitle2">Masukan berikut memiliki kesalahan!</AlertTitle>
                          {Object.entries(formik.errors).map(([key, value]) => {
                            return (
                              <Box className="flex flex-row gap-0.5" key={crypto.randomUUID()}>
                                <Typography variant="body2" className="text-error">
                                  {capitalize(key)}:
                                </Typography>
                                <Typography variant="body2" className="text-text-primary">
                                  {value}
                                </Typography>
                              </Box>
                            );
                          })}
                        </Alert>
                      )}
                      {apiError && (
                        <Alert
                          severity="error"
                          icon={<NiCrossSquare />}
                          className="neutral bg-background-paper/60! mb-4"
                        >
                          <AlertTitle variant="subtitle2">Gagal Masuk</AlertTitle>
                          <Typography variant="body2" className="text-text-primary">
                            {apiError}
                          </Typography>
                        </Alert>
                      )}
                      <Box className="flex flex-col gap-2">
                        <Link
                          to="/auth/password-reset"
                          className="link-text-secondary link-underline-hover text-center text-sm font-semibold"
                        >
                          Reset Kata Sandi
                        </Link>
                        <Button type="submit" variant="contained" className="mb-4">
                          Lanjutkan
                        </Button>
                      </Box>

                      <Divider className="text-text-secondary my-4 text-sm">PORTAL SPMB ONLINE</Divider>
                      <Box className="mb-4 flex flex-col gap-2">
                        <Button
                          variant="outlined"
                          color="primary"
                          onClick={() => navigate("/auth/spmb/register")}
                          className="w-full font-bold"
                        >
                          Pendaftaran Murid Baru (SPMB)
                        </Button>
                        <Button
                          variant="outlined"
                          color="secondary"
                          onClick={() => navigate("/auth/spmb/status")}
                          className="w-full font-bold"
                        >
                          Cek Status Pendaftaran & Upload Berkas
                        </Button>
                      </Box>

                      <Typography variant="body2" className="text-text-secondary">
                        Dengan mengklik Lanjutkan atau Masuk dengan Google, Anda menyetujui{" "}
                        <Link
                          target="_blank"
                          to="/auth/terms-and-conditions"
                          className="link-primary link-underline-hover"
                        >
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
                </>
              )}
            </Box>
            {/* <Divider className="text-text-secondary my-0 text-sm"></Divider>
              <Box className="flex flex-col">
                <Typography variant="h6" component="h6">
                  Get Started
                </Typography>
                <Typography variant="body1" className="text-text-secondary">
                  New to Gogo? Please use your email to{" "}
                  <Link to="/auth/sign-up" className="link-primary link-underline-hover">
                    sign up
                  </Link>
                  .
                </Typography>
              </Box> */}
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
