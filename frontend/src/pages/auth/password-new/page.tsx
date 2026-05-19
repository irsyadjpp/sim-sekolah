import { useFormik } from "formik";
import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import * as yup from "yup";

import {
  Alert,
  AlertTitle,
  Box,
  Button,
  capitalize,
  CircularProgress,
  Divider,
  FormControl,
  FormLabel,
  Input,
  Paper,
  Tooltip,
  Typography,
} from "@mui/material";

import Logo from "@/components/logo/logo";
import NiCheck from "@/icons/nexture/ni-check";
import NiCross from "@/icons/nexture/ni-cross";
import NiCrossSquare from "@/icons/nexture/ni-cross-square";
import { cn } from "@/lib/utils";

const validationSchema = yup.object({
  password: yup
    .string()
    .required("Bagian ini wajib diisi")
    .min(8, "Harus minimal 8 karakter")
    .test("uppercase", "Harus mengandung huruf besar dan kecil", (value) => {
      const hasUpperCase = /[A-Z]/.test(value);
      const hasLowerCase = /[a-z]/.test(value);
      return hasUpperCase && hasLowerCase;
    })
    .test("symbol", "Harus mengandung karakter spesial", (value) => {
      const hasSymbol = /[^A-Za-z 0-9]/g.test(value);
      return hasSymbol;
    }),
});

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
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const [submitted, setSubmitted] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      password: "",
    },
    validationSchema,
    onSubmit: async (values) => {
      setApiError(null);
      try {
        const response = await fetch("http://localhost:8080/api/v1/auth/reset-password", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token, password: values.password }),
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.message || "Gagal mereset kata sandi.");
        }
        navigate("/");
      } catch (err: any) {
        setApiError(err.message);
      }
    },
    validateOnBlur: false,
    validateOnMount: false,
  });

  const isPasswordLengthValid = () => {
    return formik.values.password.length >= 8;
  };

  const isPasswordCaseValid = () => {
    const hasUpperCase = /[A-Z]/.test(formik.values.password);
    const hasLowerCase = /[a-z]/.test(formik.values.password);
    return hasUpperCase && hasLowerCase;
  };

  const isPasswordSymbolValid = () => {
    const hasSymbol = /[^A-Za-z 0-9]/g.test(formik.values.password);
    return hasSymbol;
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
                  Buat kata sandi baru untuk akun Anda dengan aman.
                </Typography>
              </Box>

              <Box className="flex flex-col gap-5">
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
                      Kata Sandi{" "}
                      {formik.touched.password && formik.errors.password && (
                        <InputErrorTooltip title={formik.errors.password} />
                      )}
                    </FormLabel>
                    <Input
                      id="password"
                      name="password"
                      placeholder=""
                      autoComplete="off"
                      value={formik.values.password}
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                    />
                    <Typography variant="body2" className="text-text-secondary mt-2 inline-block align-middle">
                      <span className="inline">Harus</span>
                      <span
                        className={cn(
                          "mx-1 inline-block h-4 w-4 rounded-md align-text-bottom",
                          isPasswordLengthValid() ? "bg-success text-text-contrast" : "bg-grey-100 text-text-secondary",
                        )}
                      >
                        {isPasswordLengthValid() ? (
                          <NiCheck size={"tiny"}></NiCheck>
                        ) : (
                          <NiCross size={"tiny"}></NiCross>
                        )}
                      </span>
                      <span className={cn("inline font-semibold", isPasswordLengthValid() && "text-success")}>
                        minimal 8 karakter,{" "}
                      </span>
                      <span className="inline">harus mengandung</span>
                      <span
                        className={cn(
                          "mx-1 inline-block h-4 w-4 rounded-md align-text-bottom",
                          isPasswordCaseValid() ? "bg-success text-text-contrast" : "bg-grey-100 text-text-secondary",
                        )}
                      >
                        {isPasswordCaseValid() ? <NiCheck size={"tiny"}></NiCheck> : <NiCross size={"tiny"}></NiCross>}
                      </span>
                      <span className={cn("inline font-semibold", isPasswordCaseValid() && "text-success")}>
                        huruf kecil dan huruf besar,{" "}
                      </span>
                      <span className="inline">harus memiliki setidaknya</span>
                      <span
                        className={cn(
                          "mx-1 inline-block h-4 w-4 rounded-md align-text-bottom",
                          isPasswordSymbolValid() ? "bg-success text-text-contrast" : "bg-grey-100 text-text-secondary",
                        )}
                      >
                        {isPasswordSymbolValid() ? (
                          <NiCheck size={"tiny"}></NiCheck>
                        ) : (
                          <NiCross size={"tiny"}></NiCross>
                        )}
                      </span>
                      <span className={cn("inline font-semibold", isPasswordSymbolValid() && "text-success")}>
                        satu karakter spesial.
                      </span>
                    </Typography>
                  </FormControl>

                  {submitted && !formik.isValid && (
                    <Alert severity="error" icon={<NiCrossSquare />} className="neutral bg-background-paper/60! mb-4">
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
                    <Alert severity="error" icon={<NiCrossSquare />} className="neutral bg-background-paper/60! mb-4">
                      <AlertTitle variant="subtitle2">Gagal Reset Kata Sandi</AlertTitle>
                      <Typography variant="body2" className="text-text-primary">
                        {apiError}
                      </Typography>
                    </Alert>
                  )}

                  <Box className="flex flex-col gap-2">
                    <Button type="submit" variant="contained" className="mb-4" disabled={formik.isSubmitting}>
                      {formik.isSubmitting ? <CircularProgress size={20} color="inherit" /> : "Lanjutkan"}
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
