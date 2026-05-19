import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import * as Yup from "yup";

import {
  ArrowBack as ArrowLeftIcon,
  ArrowForward as ArrowRightIcon,
  Badge as BadgeIcon,
  Check as CheckIcon,
  Delete as DeleteIcon,
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
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Divider,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Step,
  StepLabel,
  Stepper,
  Switch,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";

export default function StaffDetailsPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const id = searchParams.get("id");

  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [initialData, setInitialData] = useState<any>(null);

  const steps = [
    { label: t("staff-form.step-identitas"), icon: <PersonIcon /> },
    { label: t("staff-form.step-lahir"), icon: <PersonIcon /> },
    { label: t("staff-form.step-kepegawaian"), icon: <BadgeIcon /> },
    { label: t("staff-form.step-kontak"), icon: <BadgeIcon /> },
    { label: t("staff-form.step-domisili"), icon: <LocationIcon /> },
    { label: t("staff-form.step-pendidikan"), icon: <BookIcon /> },
  ];

  const religions = [
    "Islam",
    "Kristen",
    "Katolik",
    "Hindu",
    "Buddha",
    "Khonghucu",
    t("staff-form.label-religion-other", "Lainnya"),
  ];

  useEffect(() => {
    if (!id) {
      navigate("/academic/subjects/staff");
      return;
    }

    const fetchTeacherDetails = async () => {
      const token = localStorage.getItem("accessToken");
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teachers/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success" && json.data) {
          const d = json.data;
          // Format dates to YYYY-MM-DD
          const formatDate = (dateStr: string) => {
            if (!dateStr) return "";
            return dateStr.split("T")[0];
          };

          setInitialData({
            school_id: d.school_id || "",
            full_name: d.full_name || "",
            gender: d.gender || "L",
            birth_place: d.birth_place || "",
            birth_date: formatDate(d.birth_date),
            nik: d.nik || "",
            nuptk: d.nuptk || "",
            niy_nigk: d.niy_nigk || "",
            religion: d.religion || "Islam",
            nationality: d.nationality || "WNI",
            photo_url: d.photo_url || "",
            full_address: d.full_address || "",
            hamlet: d.hamlet || "",
            rt_rw: d.rt_rw || "",
            village: d.village || "",
            district: d.district || "",
            regency: d.regency || "",
            province: d.province || "",
            postal_code: d.postal_code || "",
            phone: d.phone || "",
            email: d.email || "",
            nip: d.nip || "",
            employment_status: d.employment_status || "PNS",
            start_teaching_date: formatDate(d.start_teaching_date),
            appointment_decree: d.appointment_decree || "",
            salary_source: d.salary_source || "",
            teaching_subject: d.teaching_subject || "",
            additional_position: d.additional_position || "",
            teaching_hours: d.teaching_hours || 0,
            is_active: d.is_active ?? true,
            last_education: d.last_education || "",
            major: d.major || "",
            university_name: d.university_name || "",
            graduation_year: d.graduation_year || new Date().getFullYear(),
            is_certified: d.is_certified ?? false,
            certificate_number: d.certificate_number || "",
            teaching_preference: d.teaching_preference || "",
          });
        } else {
          setError(t("common-errors.fetch-error"));
        }
      } catch (err: any) {
        setError(t("common-errors.network-error"));
      } finally {
        setLoading(false);
      }
    };
    fetchTeacherDetails();
  }, [id, navigate, t]);

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: initialData || {
      school_id: "",
      full_name: "",
      gender: "L",
      birth_place: "",
      birth_date: "",
      nik: "",
      nuptk: "",
      niy_nigk: "",
      religion: "Islam",
      nationality: "WNI",
      photo_url: "",
      full_address: "",
      hamlet: "",
      rt_rw: "",
      village: "",
      district: "",
      regency: "",
      province: "",
      postal_code: "",
      phone: "",
      email: "",
      nip: "",
      employment_status: "PNS",
      start_teaching_date: "",
      appointment_decree: "",
      salary_source: "",
      teaching_subject: "",
      additional_position: "",
      teaching_hours: 0,
      is_active: true,
      last_education: "",
      major: "",
      university_name: "",
      graduation_year: new Date().getFullYear(),
      is_certified: false,
      certificate_number: "",
      teaching_preference: "",
    },
    validationSchema: Yup.object({
      full_name: Yup.string().required(t("staff-form.required")),
      nik: Yup.string().length(16, t("staff-form.invalid-nik")).required(t("staff-form.required")),
    }),
    onSubmit: async (values) => {
      await submitData(values);
    },
  });

  const submitData = async (values: any) => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setError(t("common-errors.auth-error"));
      return;
    }
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teachers/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(values),
      });
      const json = await res.json();
      if (json.status === "success") {
        navigate("/academic/subjects/staff");
      } else {
        setError(t("common-errors.save-error"));
      }
    } catch (err: any) {
      setError(t("common-errors.network-error"));
    }
  };

  const handleDelete = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teachers/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        navigate("/academic/subjects/staff");
      } else {
        setError("Gagal menghapus data guru.");
        setOpenDeleteDialog(false);
      }
    } catch (err) {
      setError(t("common-errors.network-error"));
      setOpenDeleteDialog(false);
    }
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
                label={t("staff-form.label-full-name")}
                name="full_name"
                variant="outlined"
                value={formik.values.full_name}
                onChange={formik.handleChange}
                error={formik.touched.full_name && Boolean(formik.errors.full_name)}
                helperText={formik.touched.full_name && (formik.errors.full_name as string)}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-nik")}
                name="nik"
                variant="outlined"
                value={formik.values.nik}
                onChange={formik.handleChange}
                error={formik.touched.nik && Boolean(formik.errors.nik)}
                helperText={formik.touched.nik && (formik.errors.nik as string)}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>{t("staff-form.label-gender")}</InputLabel>
                <Select
                  label={t("staff-form.label-gender")}
                  name="gender"
                  value={formik.values.gender}
                  onChange={formik.handleChange}
                >
                  <MenuItem value="L">Laki-laki</MenuItem>
                  <MenuItem value="P">Perempuan</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>{t("staff-form.label-religion")}</InputLabel>
                <Select
                  label={t("staff-form.label-religion")}
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
                label={t("staff-form.label-birth-place")}
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
                label={t("staff-form.label-birth-date")}
                name="birth_date"
                InputLabelProps={{ shrink: true }}
                variant="outlined"
                value={formik.values.birth_date}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-nip")}
                name="nip"
                variant="outlined"
                value={formik.values.nip}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>{t("staff-form.label-employment-status")}</InputLabel>
                <Select
                  label={t("staff-form.label-employment-status")}
                  name="employment_status"
                  value={formik.values.employment_status}
                  onChange={formik.handleChange}
                >
                  <MenuItem value="PNS">PNS</MenuItem>
                  <MenuItem value="PPPK">PPPK</MenuItem>
                  <MenuItem value="Honorer">Honorer</MenuItem>
                  <MenuItem value="GTY">GTY</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-teaching-subject")}
                name="teaching_subject"
                variant="outlined"
                value={formik.values.teaching_subject}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                type="number"
                label={t("staff-form.label-teaching-hours")}
                name="teaching_hours"
                variant="outlined"
                value={formik.values.teaching_hours}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-nuptk")}
                name="nuptk"
                variant="outlined"
                value={formik.values.nuptk}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                type="date"
                label={t("staff-form.label-tmt")}
                name="start_teaching_date"
                InputLabelProps={{ shrink: true }}
                variant="outlined"
                value={formik.values.start_teaching_date}
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
                label={t("staff-form.label-email")}
                name="email"
                variant="outlined"
                value={formik.values.email}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-phone")}
                name="phone"
                variant="outlined"
                value={formik.values.phone}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label={t("staff-form.label-address")}
                name="full_address"
                variant="outlined"
                value={formik.values.full_address}
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
                label={t("staff-form.label-village")}
                name="village"
                variant="outlined"
                value={formik.values.village}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-district")}
                name="district"
                variant="outlined"
                value={formik.values.district}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-regency")}
                name="regency"
                variant="outlined"
                value={formik.values.regency}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-postal-code")}
                name="postal_code"
                variant="outlined"
                value={formik.values.postal_code}
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
                label={t("staff-form.label-education")}
                name="last_education"
                variant="outlined"
                value={formik.values.last_education}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label={t("staff-form.label-university")}
                name="university_name"
                variant="outlined"
                value={formik.values.university_name}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                multiline
                rows={2}
                placeholder={t("staff-form.label-ai-pref")}
                label={t("staff-form.label-ai-pref")}
                name="teaching_preference"
                value={formik.values.teaching_preference}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={formik.values.is_certified}
                    onChange={(e) => formik.setFieldValue("is_certified", e.target.checked)}
                  />
                }
                label={t("staff-form.label-certified")}
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
      <Grid container spacing={2.5} className="mb-8 w-full items-center justify-between">
        <Grid size={{ xs: 12, md: 8 }}>
          <Typography variant="h1" component="h1" className="mb-0">
            {loading ? "Memuat Data Staf..." : "Detail Staf"}
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
              {t("staff-form.breadcrumb-home")}
            </Link>
            <Link color="inherit" to="/academic" className="hover:text-primary no-underline transition-colors">
              {t("staff-form.breadcrumb-academic")}
            </Link>
            <Link color="inherit" to="/academic/subjects" className="hover:text-primary no-underline transition-colors">
              {t("staff-form.breadcrumb-subjects")}
            </Link>
            <Link
              color="inherit"
              to="/academic/subjects/staff"
              className="hover:text-primary no-underline transition-colors"
            >
              {t("staff-form.breadcrumb-staff")}
            </Link>
            <Typography variant="body2" className="text-text-secondary">
              Detail
            </Typography>
          </Breadcrumbs>
        </Grid>
        {!loading && !error && (
          <Grid size={{ xs: 12, md: 4 }} className="mt-4 flex justify-end md:mt-0">
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={() => setOpenDeleteDialog(true)}
              className="rounded-xl bg-white shadow-sm"
            >
              Hapus Staf
            </Button>
          </Grid>
        )}
      </Grid>

      {loading ? (
        <Box className="flex justify-center py-20">
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" className="mb-8 rounded-2xl font-bold">
          {error}
        </Alert>
      ) : (
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
                <Box className="w-full">
                  <Typography variant="h5" className="text-primary mb-10 font-black">
                    Langkah {activeStep + 1}: {steps[activeStep].label}
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
                      {t("staff-form.button-back")}
                    </Button>

                    <Box className="flex gap-4">
                      {activeStep < steps.length - 1 ? (
                        <Button
                          variant="contained"
                          onClick={handleNext}
                          endIcon={<ArrowRightIcon />}
                          className="rounded-2xl px-10 py-4 font-bold shadow-xl"
                        >
                          {t("staff-form.button-next")}
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
                          Perbarui Data
                        </Button>
                      )}
                    </Box>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle className="font-bold">Konfirmasi Hapus</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Apakah Anda yakin ingin menghapus data staf ini? Tindakan ini tidak dapat dibatalkan.
          </DialogContentText>
        </DialogContent>
        <DialogActions className="p-4">
          <Button onClick={() => setOpenDeleteDialog(false)} color="inherit" variant="text" className="font-bold">
            Batal
          </Button>
          <Button onClick={handleDelete} color="error" variant="contained" className="rounded-xl font-bold shadow-md">
            Hapus
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
