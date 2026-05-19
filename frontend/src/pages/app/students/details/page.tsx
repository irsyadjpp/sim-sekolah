import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import * as Yup from "yup";

import {
  Add as AddIcon,
  ArrowBack as ArrowLeftIcon,
  ArrowForward as ArrowRightIcon,
  Check as CheckIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
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
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Divider,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Step,
  StepLabel,
  Stepper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useConfirm } from "@/hooks/use-confirm";

export default function StudentDetailsPage() {
  const confirm = useConfirm();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const id = searchParams.get("id");

  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [initialData, setInitialData] = useState<any>(null);

  // Parent State
  const [parents, setParents] = useState<any[]>([]);
  const [openParentDialog, setOpenParentDialog] = useState(false);
  const [parentError, setParentError] = useState<string | null>(null);
  const [parentForm, setParentForm] = useState({
    id: "",
    parent_type: "FATHER",
    full_name: "",
    nik: "",
    education: "",
    occupation: "",
    income: 0,
    phone: "",
  });

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
    "Islam",
    "Kristen",
    "Katolik",
    "Hindu",
    "Buddha",
    "Khonghucu",
    t("student-form.label-religion-other", "Lainnya"),
  ];

  const fetchStudentDetails = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success" && json.data) {
        const d = json.data;
        setParents(d.parents || []);

        const formatDate = (dateStr: string) => {
          if (!dateStr) return "";
          return dateStr.split("T")[0];
        };

        setInitialData({
          school_id: d.school_id || "",
          full_name: d.full_name || "",
          nis: d.nis || "",
          nisn: d.nisn || "",
          gender: d.gender || "L",
          birth_place: d.birth_place || "",
          birth_date: formatDate(d.birth_date),
          religion: d.religion || "Islam",
          nationality: d.nationality || "WNI",
          child_order: d.child_order || 1,
          siblings: d.siblings || 0,
          photo_url: d.photo_url || "",
          nik: d.nik || "",
          family_card_number: d.family_card_number || "",
          birth_certificate: d.birth_certificate || "",
          kip_number: d.kip_number || "",
          full_address: d.full_address || "",
          rt_rw: d.rt_rw || "",
          village: d.village || "",
          district: d.district || "",
          regency: d.regency || "",
          province: d.province || "",
          postal_code: d.postal_code || "",
          coordinates: d.coordinates || "",
          enrollment_year: d.enrollment_year || new Date().getFullYear(),
          curriculum: d.curriculum || "Kurikulum Merdeka",
          student_status: d.student_status || "Aktif",
          entry_path: d.entry_path || "Zonasi",
          previous_school: d.previous_school || "",
          exam_number: d.exam_number || "",
          blood_type: d.blood_type || "",
          height: d.height || 0,
          weight: d.weight || 0,
          medical_history: d.medical_history || "",
          disability: d.disability || "",
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

  useEffect(() => {
    if (!id) {
      navigate("/students");
      return;
    }
    fetchStudentDetails();
  }, [id, navigate, t]);

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: initialData || {
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

  const submitData = async (values: any) => {
    const token = localStorage.getItem("accessToken");
    if (!token) return setError(t("common-errors.auth-error"));
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students/${id}`, {
        method: "PUT",
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
      }
    } catch (err: any) {
      setError(t("common-errors.network-error"));
    }
  };

  const handleDelete = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        navigate("/students");
      } else {
        setError("Gagal menghapus data siswa.");
        setOpenDeleteDialog(false);
      }
    } catch (err) {
      setError(t("common-errors.network-error"));
      setOpenDeleteDialog(false);
    }
  };

  const handleParentSubmit = async () => {
    if (!parentForm.full_name) {
      setParentError("Nama wajib diisi.");
      return;
    }
    const token = localStorage.getItem("accessToken");
    try {
      setParentError(null);
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students/${id}/parents`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          parent_type: parentForm.parent_type,
          full_name: parentForm.full_name,
          nik: parentForm.nik,
          education: parentForm.education,
          occupation: parentForm.occupation,
          income: Number(parentForm.income),
          phone: parentForm.phone,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenParentDialog(false);
        fetchStudentDetails(); // Refresh parents
      } else {
        setParentError("Gagal menyimpan data orang tua.");
      }
    } catch (err) {
      setParentError(t("common-errors.network-error"));
    }
  };

  const handleParentDelete = async (parentId: string) => {
    const ok = await confirm({
      title: "Hapus Data Orang Tua",
      message: "Hapus data orang tua ini?",
      confirmText: "Hapus",
      cancelText: "Batal",
    });
    if (!ok) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/students/${id}/parents/${parentId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        fetchStudentDetails();
      } else {
        setError("Gagal menghapus data orang tua.");
      }
    } catch (err) {
      setError(t("common-errors.network-error"));
    }
  };

  const openEditParent = (p: any) => {
    setParentForm({
      id: p.id,
      parent_type: p.parent_type,
      full_name: p.full_name,
      nik: p.nik,
      education: p.education,
      occupation: p.occupation,
      income: p.income,
      phone: p.phone,
    });
    setParentError(null);
    setOpenParentDialog(true);
  };

  const openAddParent = () => {
    setParentForm({
      id: "",
      parent_type: "FATHER",
      full_name: "",
      nik: "",
      education: "",
      occupation: "",
      income: 0,
      phone: "",
    });
    setParentError(null);
    setOpenParentDialog(true);
  };

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
                helperText={
                  formik.touched.full_name && formik.errors.full_name ? String(formik.errors.full_name) : undefined
                }
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
                helperText={formik.touched.nik && formik.errors.nik ? String(formik.errors.nik) : undefined}
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
                  <MenuItem value="L">Laki-laki</MenuItem>
                  <MenuItem value="P">Perempuan</MenuItem>
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
            <Grid size={{ xs: 12, md: 6 }}>
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
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>Status Siswa (Lifecycle)</InputLabel>
                <Select
                  label="Status Siswa (Lifecycle)"
                  name="student_status"
                  value={formik.values.student_status}
                  onChange={formik.handleChange}
                >
                  <MenuItem value="active">Active (Aktif)</MenuItem>
                  <MenuItem value="graduated">Graduated (Lulus)</MenuItem>
                  <MenuItem value="withdrawn">Withdrawn (Keluar)</MenuItem>
                  <MenuItem value="alumni">Alumni</MenuItem>
                  <MenuItem value="applicant">Applicant (Calon Siswa)</MenuItem>
                  <MenuItem value="accepted">Accepted (Diterima)</MenuItem>
                  <MenuItem value="enrolled">Enrolled (Terdaftar)</MenuItem>
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

  return (
    <Box className="pb-10">
      <Grid container spacing={2.5} className="mb-8 w-full items-center justify-between">
        <Grid size={{ xs: 12, md: 8 }}>
          <Typography variant="h1" component="h1" className="mb-0">
            {loading ? t("student-form.loading-details") : t("student-form.detail-title")}
          </Typography>
          <Breadcrumbs>
            <Link color="inherit" to="/home" className="hover:text-primary no-underline transition-colors">
              {t("student-form.breadcrumb-home")}
            </Link>
            <Link color="inherit" to="/students" className="hover:text-primary no-underline transition-colors">
              {t("student-form.students-list")}
            </Link>
            <Typography variant="body2" className="text-text-secondary">
              {t("student-form.detail-word")}
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
              {t("student-form.delete-student")}
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
          <Grid size={{ xs: 12, md: 4, lg: 3 }} className="space-y-4">
            <Paper className="rounded-3xl border border-slate-100 bg-slate-50/50 p-6 shadow-sm">
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
            <Card className="mb-6 overflow-hidden rounded-[40px] border-none bg-white shadow-2xl">
              <CardContent className="p-10 md:p-14">
                <Box className="w-full">
                  <Typography variant="h5" className="text-primary mb-10 font-black">
                    {t("student-form.step-label")} {activeStep + 1}: {steps[activeStep].label}
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
                          {t("student-form.button-update")}
                        </Button>
                      )}
                    </Box>
                  </Box>
                </Box>
              </CardContent>
            </Card>

            {/* PARENT SECTION */}
            <Card className="rounded-[40px] border-none bg-white shadow-2xl">
              <CardContent className="p-10 md:p-14">
                <Box className="mb-6 flex items-center justify-between">
                  <Typography variant="h5" className="text-primary font-black">
                    Data Orang Tua / Wali
                  </Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={openAddParent}
                    className="rounded-xl font-bold"
                  >
                    Tambah
                  </Button>
                </Box>

                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow className="bg-slate-50">
                        <TableCell className="font-bold">Hubungan</TableCell>
                        <TableCell className="font-bold">Nama Lengkap</TableCell>
                        <TableCell className="font-bold">Pekerjaan</TableCell>
                        <TableCell className="font-bold">No. HP</TableCell>
                        <TableCell align="right" className="font-bold">
                          Aksi
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {parents.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={5} align="center" className="py-8 text-slate-400">
                            Belum ada data orang tua/wali.
                          </TableCell>
                        </TableRow>
                      ) : (
                        parents.map((p) => (
                          <TableRow key={p.id}>
                            <TableCell className="font-medium">
                              {p.parent_type === "FATHER"
                                ? t("student-form.parent-father")
                                : p.parent_type === "MOTHER"
                                  ? t("student-form.parent-mother")
                                  : t("student-form.parent-guardian")}
                            </TableCell>
                            <TableCell>{p.full_name}</TableCell>
                            <TableCell>{p.occupation || "-"}</TableCell>
                            <TableCell>{p.phone || "-"}</TableCell>
                            <TableCell align="right">
                              <IconButton size="small" onClick={() => openEditParent(p)} color="primary">
                                <EditIcon fontSize="small" />
                              </IconButton>
                              <IconButton size="small" onClick={() => handleParentDelete(p.id)} color="error">
                                <DeleteIcon fontSize="small" />
                              </IconButton>
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Delete Confirmation Dialog */}
      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle className="font-bold">{t("student-form.button-delete")}</DialogTitle>
        <DialogContent>
          <DialogContentText>{t("student-form.delete-confirm")}</DialogContentText>
        </DialogContent>
        <DialogActions className="p-4">
          <Button onClick={() => setOpenDeleteDialog(false)} color="inherit" variant="text" className="font-bold">
            {t("student-form.button-back")}
          </Button>
          <Button onClick={handleDelete} color="error" variant="contained" className="rounded-xl font-bold shadow-md">
            {t("student-form.button-delete")}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add/Edit Parent Dialog */}
      <Dialog open={openParentDialog} onClose={() => setOpenParentDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle className="font-bold">
          {parentForm.id ? t("student-form.parent-edit") : t("student-form.parent-add")}
        </DialogTitle>
        <DialogContent>
          {parentError && (
            <Alert severity="error" className="mt-2 mb-4 rounded-xl">
              {parentError}
            </Alert>
          )}
          <Grid container spacing={3} className="mt-1">
            <Grid size={{ xs: 12 }}>
              <FormControl fullWidth size="small">
                <InputLabel>{t("student-form.parent-relation")}</InputLabel>
                <Select
                  value={parentForm.parent_type}
                  label={t("student-form.parent-relation")}
                  onChange={(e) => setParentForm({ ...parentForm, parent_type: e.target.value })}
                >
                  <MenuItem value="FATHER">{t("student-form.parent-father")}</MenuItem>
                  <MenuItem value="MOTHER">{t("student-form.parent-mother")}</MenuItem>
                  <MenuItem value="GUARDIAN">{t("student-form.parent-guardian")}</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                size="small"
                label={t("student-form.parent-name")}
                value={parentForm.full_name}
                onChange={(e) => setParentForm({ ...parentForm, full_name: e.target.value })}
                required
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                size="small"
                label={t("student-form.label-nik")}
                value={parentForm.nik}
                onChange={(e) => setParentForm({ ...parentForm, nik: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                size="small"
                label={t("student-form.parent-phone")}
                value={parentForm.phone}
                onChange={(e) => setParentForm({ ...parentForm, phone: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                size="small"
                label={t("student-form.parent-education")}
                value={parentForm.education}
                onChange={(e) => setParentForm({ ...parentForm, education: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                size="small"
                label={t("student-form.parent-occupation")}
                value={parentForm.occupation}
                onChange={(e) => setParentForm({ ...parentForm, occupation: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                size="small"
                type="number"
                label={t("student-form.parent-income")}
                value={parentForm.income}
                onChange={(e) => setParentForm({ ...parentForm, income: Number(e.target.value) })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions className="p-4">
          <Button onClick={() => setOpenParentDialog(false)} color="inherit" variant="text" className="font-bold">
            {t("student-form.button-back")}
          </Button>
          <Button
            onClick={handleParentSubmit}
            color="primary"
            variant="contained"
            className="rounded-xl font-bold shadow-md"
          >
            {t("student-form.button-save-parent")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
