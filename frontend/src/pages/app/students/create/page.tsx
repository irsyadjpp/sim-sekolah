import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import * as Yup from "yup";

import {
  ArrowBack as ArrowLeftIcon,
  ArrowForward as ArrowRightIcon,
  Check as CheckIcon,
  Drafts as DraftIcon,
  FitnessCenter as HealthIcon,
  LocationOn as LocationIcon,
  MenuBook as BookIcon,
  Person as PersonIcon,
  Save as SaveIcon,
} from "@mui/icons-material";
import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Step,
  StepLabel,
  Stepper,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

export default function CreateStudentPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const steps = [
    { label: t("student-form.step-identitas"), icon: <PersonIcon /> },
    { label: t("student-form.step-lahir"), icon: <PersonIcon /> },
    { label: t("student-form.step-domisili"), icon: <LocationIcon /> },
    { label: t("student-form.step-wilayah"), icon: <LocationIcon /> },
    { label: t("student-form.step-kk"), icon: <LocationIcon /> },
    { label: t("student-form.step-akademik"), icon: <BookIcon /> },
    { label: t("student-form.step-nis"), icon: <BookIcon /> },
    { label: t("student-form.step-kesehatan"), icon: <HealthIcon /> },
  ];

  const religions = [
    t("students.religion-islam"),
    t("students.religion-kristen"),
    t("students.religion-katolik"),
    t("students.religion-hindu"),
    t("students.religion-buddha"),
    t("students.religion-khonghucu"),
    t("student-form.label-religion-other", "Lainnya"),
  ];

  const formik = useFormik({
    initialValues: {
      school_id: "",
      full_name: "",
      nis: "",
      nisn: "",
      gender: "L",
      birth_place: "",
      birth_date: "",
      religion: "Islam",
      nationality: "WNI",
      child_order: 1,
      siblings: 0,
      photo_url: "",
      nik: "",
      family_card_number: "",
      birth_certificate: "",
      kip_number: "",
      full_address: "",
      rt_rw: "",
      village: "",
      district: "",
      regency: "",
      province: "",
      postal_code: "",
      coordinates: "",
      enrollment_year: new Date().getFullYear(),
      curriculum: "Kurikulum Merdeka",
      student_status: "Aktif",
      entry_path: "Zonasi",
      previous_school: "",
      exam_number: "",
      blood_type: "",
      height: 0,
      weight: 0,
      medical_history: "",
      disability: "",
    },
    validationSchema: Yup.object({
      full_name: Yup.string().required(t("student-form.required")),
      nik: Yup.string().length(16, t("student-form.invalid-nik")).required(t("student-form.required")),
    }),
    onSubmit: async (values) => {
      await submitData(values);
    },
  });

  useEffect(() => {
    const fetchSchools = async () => {
      const token = localStorage.getItem("accessToken");
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/schools`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success" && json.data?.length > 0) {
          // Hanya set jika belum ada school_id
          if (!formik.values.school_id) {
            formik.setFieldValue("school_id", json.data[0].id);
          }
        }
      } catch (err: any) {
        setError(t("common-errors.sync-error"));
      }
    };
    fetchSchools();
  }, [t]);

  const submitData = async (values: any) => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setError(t("common-errors.auth-error"));
      return;
    }
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(values),
      });
      const json = await res.json();
      if (json.status === "success") {
        navigate("/students");
      } else {
        setError(t("common-errors.save-error"));
        setActiveStep(0);
      }
    } catch (err: any) {
      setError(t("common-errors.network-error"));
    }
  };

  const handleSaveDraft = async () => {
    const values = { ...formik.values, student_status: "Draft" };
    await submitData(values);
  };

  const handleNext = async () => {
    if (activeStep === 0) {
      const errors = await formik.validateForm();
      if (errors.full_name || errors.nik) {
        formik.setTouched({ full_name: true, nik: true });
        return;
      }
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => setActiveStep((prev) => prev - 1);

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-full-name")}
                name="full_name"
                variant="outlined"
                value={formik.values.full_name}
                onChange={formik.handleChange}
                error={formik.touched.full_name && Boolean(formik.errors.full_name)}
                helperText={formik.touched.full_name && formik.errors.full_name}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-nik")}
                name="nik"
                variant="outlined"
                value={formik.values.nik}
                onChange={formik.handleChange}
                error={formik.touched.nik && Boolean(formik.errors.nik)}
                helperText={formik.touched.nik && formik.errors.nik}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>{t("student-form.label-gender")}</InputLabel>
                <Select
                  label={t("student-form.label-gender")}
                  name="gender"
                  value={formik.values.gender}
                  onChange={formik.handleChange}
                >
                  <MenuItem value="L">{t("students.gender-male")}</MenuItem>
                  <MenuItem value="P">{t("students.gender-female")}</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>{t("student-form.label-religion")}</InputLabel>
                <Select
                  label={t("student-form.label-religion")}
                  name="religion"
                  value={formik.values.religion}
                  onChange={formik.handleChange}
                >
                  {religions.map((r) => (
                    <MenuItem key={r} value={r}>
                      {r}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-birth-place")}
                name="birth_place"
                variant="outlined"
                value={formik.values.birth_place}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                type="date"
                label={t("student-form.label-birth-date")}
                name="birth_date"
                InputLabelProps={{ shrink: true }}
                variant="outlined"
                value={formik.values.birth_date}
                onChange={formik.handleChange}
              />
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label={t("student-form.label-address")}
                name="full_address"
                variant="outlined"
                value={formik.values.full_address}
                onChange={formik.handleChange}
              />
            </Grid>
          </Grid>
        );
      case 3:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-village")}
                name="village"
                variant="outlined"
                value={formik.values.village}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-district")}
                name="district"
                variant="outlined"
                value={formik.values.district}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-regency")}
                name="regency"
                variant="outlined"
                value={formik.values.regency}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-postal-code")}
                name="postal_code"
                variant="outlined"
                value={formik.values.postal_code}
                onChange={formik.handleChange}
              />
            </Grid>
          </Grid>
        );
      case 4:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-kk")}
                name="family_card_number"
                variant="outlined"
                value={formik.values.family_card_number}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-akta")}
                name="birth_certificate"
                variant="outlined"
                value={formik.values.birth_certificate}
                onChange={formik.handleChange}
              />
            </Grid>
          </Grid>
        );
      case 5:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                type="number"
                label={t("student-form.label-enrollment-year")}
                name="enrollment_year"
                variant="outlined"
                value={formik.values.enrollment_year}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-previous-school")}
                name="previous_school"
                variant="outlined"
                value={formik.values.previous_school}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>{t("student-form.label-entry-path")}</InputLabel>
                <Select
                  label={t("student-form.label-entry-path")}
                  name="entry_path"
                  value={formik.values.entry_path}
                  onChange={formik.handleChange}
                >
                  <MenuItem value="Zonasi">Zonasi</MenuItem>
                  <MenuItem value="Afirmasi">Afirmasi</MenuItem>
                  <MenuItem value="Prestasi">Prestasi</MenuItem>
                  <MenuItem value="Perpindahan Orang Tua">Perpindahan Orang Tua</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );
      case 6:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-nis")}
                name="nis"
                variant="outlined"
                value={formik.values.nis}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-nisn")}
                name="nisn"
                variant="outlined"
                value={formik.values.nisn}
                onChange={formik.handleChange}
              />
            </Grid>
          </Grid>
        );
      case 7:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-height")}
                name="height"
                variant="outlined"
                value={formik.values.height}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("student-form.label-weight")}
                name="weight"
                variant="outlined"
                value={formik.values.weight}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label={t("student-form.label-medical")}
                variant="outlined"
                name="medical_history"
                value={formik.values.medical_history}
                onChange={formik.handleChange}
              />
            </Grid>
          </Grid>
        );
      default:
        return null;
    }
  };

  return (
    <Box className="pb-10">
      <Grid container spacing={2.5} className="mb-8 w-full">
        <Grid size={{ xs: 12 }}>
          <Typography variant="h1" component="h1" className="mb-0">
            {t("student-form.title")}
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
              {t("student-form.breadcrumb-home")}
            </Link>
            <Link color="inherit" to="/students" className="hover:text-primary no-underline transition-colors">
              {t("student-form.breadcrumb-students")}
            </Link>
            <Typography variant="body2" className="text-text-secondary">
              {t("student-form.breadcrumb-add")}
            </Typography>
          </Breadcrumbs>
        </Grid>
      </Grid>

      <Grid container spacing={4}>
        <Grid size={{ xs: 12, md: 4, lg: 3 }}>
          <Paper className="sticky top-10 rounded-3xl border border-slate-100 bg-slate-50/50 p-6 shadow-sm">
            <Stepper activeStep={activeStep} orientation="vertical">
              {steps.map((step, index) => (
                <Step key={step.label}>
                  <StepLabel
                    icon={
                      <Box
                        className={`flex h-10 w-10 items-center justify-center rounded-2xl transition-all duration-300 ${activeStep === index ? "bg-primary scale-110 text-white shadow-xl" : activeStep > index ? "bg-green-500 text-white" : "bg-slate-100 text-slate-400"}`}
                      >
                        {activeStep > index ? <CheckIcon fontSize="small" /> : step.icon}
                      </Box>
                    }
                  >
                    <Typography
                      variant="body2"
                      className={`font-black ${activeStep === index ? "text-slate-900" : "text-slate-400"}`}
                    >
                      {step.label}
                    </Typography>
                  </StepLabel>
                </Step>
              ))}
            </Stepper>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8, lg: 9 }}>
          <Card className="overflow-hidden rounded-[40px] border-none bg-white shadow-2xl">
            <CardContent className="p-10 md:p-14">
              {error && (
                <Alert severity="error" className="mb-8 rounded-2xl font-bold">
                  {error}
                </Alert>
              )}

              <Box className="w-full">
                <Typography variant="h5" className="text-primary mb-10 font-black">
                  {t("Step")} {activeStep + 1}: {steps[activeStep].label}
                </Typography>

                {renderStepContent(activeStep)}

                <Divider className="my-10" />

                <Box className="flex items-center justify-between">
                  <Button
                    variant="text"
                    color="inherit"
                    disabled={activeStep === 0}
                    onClick={handleBack}
                    startIcon={<ArrowLeftIcon />}
                    className="font-bold"
                  >
                    {t("student-form.button-back")}
                  </Button>

                  <Box className="flex gap-4">
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={handleSaveDraft}
                      disabled={formik.isSubmitting}
                      startIcon={<DraftIcon />}
                      className="rounded-2xl px-6 py-4 font-bold"
                    >
                      {t("student-form.button-draft")}
                    </Button>

                    {activeStep < steps.length - 1 ? (
                      <Button
                        variant="contained"
                        onClick={handleNext}
                        endIcon={<ArrowRightIcon />}
                        className="rounded-2xl px-10 py-4 font-bold shadow-xl"
                      >
                        {t("student-form.button-next")}
                      </Button>
                    ) : (
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={() => formik.handleSubmit()}
                        disabled={formik.isSubmitting}
                        startIcon={<SaveIcon />}
                        className="rounded-2xl px-10 py-4 font-black shadow-xl"
                      >
                        {t("student-form.button-save")}
                      </Button>
                    )}
                  </Box>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
