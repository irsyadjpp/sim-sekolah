/* eslint-disable @typescript-eslint/no-unused-vars */
import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import * as Yup from "yup";

import {
  ArrowBack as ArrowLeftIcon,
  ArrowForward as ArrowRightIcon,
  Check as CheckIcon,
  CheckCircleOutline as SuccessIcon,
  ContactPhone as PhoneIcon,
  LocationOn as LocationIcon,
  Person as PersonIcon,
  School as SchoolIcon,
} from "@mui/icons-material";
import {
  Alert,
  Box,
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

import Logo from "@/components/logo/logo";
import { DEFAULTS } from "@/config";

export default function SPMBRegisterPage() {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [admissionPaths, setAdmissionPaths] = useState<any[]>([]);
  const [academicYears, setAcademicYears] = useState<any[]>([]);
  const [successData, setSuccessData] = useState<any | null>(null);

  const selectedPath = admissionPaths.find((p) => p.id === formik.values.admission_path_id);
  const isDomisili = selectedPath?.name === "Domisili";

  const steps = [
    { label: "Jalur & Akademik", icon: <SchoolIcon /> },
    { label: "Identitas Murid", icon: <PersonIcon /> },
    { label: "Alamat Domisili", icon: <LocationIcon /> },
    { label: "Orang Tua & Kontak", icon: <PhoneIcon /> },
  ];

  const religions = ["Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Khonghucu", "Lainnya"];
  const genders = [
    { value: "L", label: "Laki-laki" },
    { value: "P", label: "Perempuan" },
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const pathRes = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/admission-paths`);
        const pathJson = await pathRes.json();
        if (pathJson.status === "success") {
          setAdmissionPaths(pathJson.data || []);
        }

        const yearRes = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/academic-years`);
        const yearJson = await yearRes.json();
        if (yearJson.status === "success") {
          setAcademicYears(yearJson.data || []);
        }
      } catch (err) {
        console.error("Gagal memuat data awal SPMB", err);
      }
    };
    fetchData();
  }, []);

  const formik = useFormik({
    initialValues: {
      admission_path_id: "",
      academic_year_id: "",
      full_name: "",
      nik: "",
      nisn: "",
      gender: "L",
      birth_place: "",
      birth_date: "",
      religion: "Islam",
      address: "",
      village: "",
      district: "",
      regency: "Kepulauan Selayar",
      province: "Sulawesi Selatan",
      postal_code: "",
      distance_to_school: 1.0,
      father_name: "",
      father_nik: "",
      father_occupation: "",
      mother_name: "",
      mother_nik: "",
      mother_occupation: "",
      phone_number: "",
      family_card_issue_date: "",
    },
    validationSchema: Yup.object({
      admission_path_id: Yup.string().required("Jalur masuk wajib dipilih"),
      academic_year_id: Yup.string().required("Tahun ajaran wajib dipilih"),
      full_name: Yup.string().required("Nama lengkap calon murid wajib diisi"),
      nik: Yup.string().length(16, "NIK harus terdiri dari 16 digit").required("NIK calon murid wajib diisi"),
      gender: Yup.string().required("Jenis kelamin wajib dipilih"),
      birth_place: Yup.string().required("Tempat lahir wajib diisi"),
      birth_date: Yup.string()
        .required("Tanggal lahir wajib diisi")
        .test("age-gate", "Usia calon murid kurang dari 5 tahun 6 bulan pada 1 Juli tahun berjalan", function (value) {
          if (!value) return true;
          const birth = new Date(value);
          const currentYear = new Date().getFullYear();
          const targetDate = new Date(currentYear, 6, 1);
          const ageDiffMs = targetDate.getTime() - birth.getTime();
          const ageDate = new Date(ageDiffMs);
          const ageYears = Math.abs(ageDate.getUTCFullYear() - 1970);
          const ageMonths = ageYears * 12 + ageDate.getUTCMonth();
          return ageMonths >= 66;
        }),
      religion: Yup.string().required("Agama wajib dipilih"),
      address: Yup.string().required("Alamat tempat tinggal wajib diisi"),
      village: Yup.string().required("Desa/Kelurahan wajib diisi"),
      district: Yup.string().required("Kecamatan wajib diisi"),
      phone_number: Yup.string().required("Nomor HP aktif wajib diisi untuk koordinasi"),
      family_card_issue_date: Yup.string().test(
        "kk-required",
        "Tanggal terbit Kartu Keluarga wajib diisi untuk Jalur Domisili",
        function (value) {
          const { admission_path_id } = this.parent;
          const path = admissionPaths.find((p) => p.id === admission_path_id);
          if (path?.name === "Domisili" && !value) return false;
          return true;
        },
      ),
    }),
    onSubmit: async (values) => {
      setError(null);
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/register`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            school_year_id: values.academic_year_id,
            admission_path_id: values.admission_path_id,
            full_name: values.full_name,
            nik: values.nik,
            nisn: values.nisn,
            gender: values.gender,
            birth_place: values.birth_place,
            birth_date: values.birth_date,
            religion: values.religion,
            family_card_issue_date: values.family_card_issue_date || undefined,
            address: values.address,
            village: values.village,
            district: values.district,
            regency: values.regency,
            province: values.province,
            postal_code: values.postal_code,
            distance_to_school_km: parseFloat(values.distance_to_school.toString()),
            father_name: values.father_name,
            father_nik: values.father_nik,
            father_occupation: values.father_occupation,
            mother_name: values.mother_name,
            mother_nik: values.mother_nik,
            mother_occupation: values.mother_occupation,
            phone_number: values.phone_number,
          }),
        });

        const json = await res.json();
        if (json.status === "success") {
          setSuccessData(json.data);
        } else {
          setError(json.message || "Gagal melakukan pendaftaran. Silakan periksa kembali data Anda.");
        }
      } catch (err) {
        setError("Terjadi kesalahan jaringan. Silakan coba beberapa saat lagi.");
      }
    },
  });

  const handleNext = async () => {
    if (activeStep === 0) {
      if (!formik.values.admission_path_id || !formik.values.academic_year_id) {
        formik.setTouched({ admission_path_id: true, academic_year_id: true });
        return;
      }
    }
    if (activeStep === 1) {
      const errors = await formik.validateForm();
      if (errors.full_name || errors.nik || errors.birth_place || errors.birth_date) {
        formik.setTouched({
          full_name: true,
          nik: true,
          birth_place: true,
          birth_date: true,
        });
        return;
      }
    }
    if (activeStep === 2) {
      const errors = await formik.validateForm();
      const path = admissionPaths.find((p) => p.id === formik.values.admission_path_id);
      if (
        errors.address ||
        errors.village ||
        errors.district ||
        (path?.path_name === "Domisili" && errors.family_card_issue_date)
      ) {
        formik.setTouched({
          address: true,
          village: true,
          district: true,
          family_card_issue_date: true,
        });
        return;
      }
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => setActiveStep((prev) => prev - 1);

  if (successData) {
    return (
      <Box className="bg-waves flex min-h-screen w-full items-center justify-center bg-cover bg-center p-4">
        <Paper elevation={3} className="bg-background-paper shadow-darker-xs w-2xl max-w-full rounded-[40px] py-14">
          <Box className="flex flex-col items-center gap-6 px-8 text-center sm:px-14">
            <Box className="mb-4">
              <Logo classNameMobile="hidden" />
            </Box>
            <SuccessIcon color="success" sx={{ fontSize: 90 }} className="animate-bounce" />
            <Box>
              <Typography variant="h2" className="mb-2 font-black text-green-600">
                Pendaftaran Berhasil!
              </Typography>
              <Typography variant="body1" className="text-text-secondary">
                Data calon murid baru telah sukses disimpan dalam sistem SPMB Online UPT SDI Bonerate No. 85.
              </Typography>
            </Box>

            <Card className="my-4 w-full rounded-3xl border border-slate-100 bg-slate-50 p-6 text-left">
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <Typography variant="body2" className="font-bold text-slate-400">
                    NAMA LENGKAP
                  </Typography>
                  <Typography variant="body1" className="font-black text-slate-800">
                    {successData.full_name}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <Typography variant="body2" className="font-bold text-slate-400">
                    NIK PENDAFTAR
                  </Typography>
                  <Typography variant="body1" className="font-mono font-black text-slate-800">
                    {successData.nik}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <Typography variant="body2" className="font-bold text-slate-400">
                    STATUS AWAL
                  </Typography>
                  <Typography variant="body1" className="font-bold text-amber-600">
                    Menunggu Verifikasi
                  </Typography>
                </Grid>
              </Grid>
            </Card>

            <Alert severity="warning" className="w-full rounded-2xl text-left font-semibold">
              <strong>PENTING:</strong> Catat dan simpan NIK di atas. Anda wajib melakukan upload dokumen pendukung (KK,
              Akta Kelahiran, Rekomendasi Psikolog/Disabilitas jika diperlukan) pada menu Cek Status Pendaftaran untuk
              menyelesaikan proses administrasi.
            </Alert>

            <Box className="flex w-full flex-col justify-center gap-4 sm:flex-row">
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate("/auth/spmb/status")}
                className="rounded-2xl px-8 py-4 font-black shadow-xl"
              >
                Upload Dokumen & Cek Status
              </Button>
              <Button
                variant="outlined"
                color="inherit"
                onClick={() => navigate("/auth/sign-in")}
                className="rounded-2xl px-8 py-4 font-bold"
              >
                Kembali ke Beranda
              </Button>
            </Box>
          </Box>
        </Paper>
      </Box>
    );
  }

  return (
    <Box className="bg-waves flex min-h-screen w-full items-center justify-center bg-cover bg-center p-4">
      <Paper elevation={3} className="bg-background-paper shadow-darker-xs w-4xl max-w-full rounded-[40px] py-10">
        <Box className="flex flex-col gap-6 px-8 sm:px-14">
          <Box className="flex items-center justify-between">
            <Logo classNameMobile="hidden" />
            <Button variant="text" color="primary" onClick={() => navigate("/auth/sign-in")} className="font-bold">
              Kembali
            </Button>
          </Box>

          <Box className="flex flex-col">
            <Typography variant="h1" className="mb-1">
              Pendaftaran Murid Baru (SPMB Online)
            </Typography>
            <Typography variant="body1" className="text-text-secondary">
              Lengkapi formulir pendaftaran calon murid baru UPT SDI Bonerate No. 85 Kepulauan Selayar.
            </Typography>
          </Box>

          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 3 }}>
              <Stepper activeStep={activeStep} orientation="vertical">
                {steps.map((step, index) => (
                  <Step key={step.label}>
                    <StepLabel
                      icon={
                        <Box
                          className={`flex h-10 w-10 items-center justify-center rounded-2xl transition-all duration-300 ${
                            activeStep === index
                              ? "bg-primary scale-110 text-white shadow-xl"
                              : activeStep > index
                                ? "bg-green-500 text-white"
                                : "bg-slate-100 text-slate-400"
                          }`}
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
            </Grid>

            <Grid size={{ xs: 12, md: 9 }}>
              <Card className="overflow-hidden rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
                <CardContent className="p-0">
                  {error && (
                    <Alert severity="error" className="mb-6 rounded-xl font-semibold">
                      {error}
                    </Alert>
                  )}

                  <Typography variant="h5" className="text-primary mb-6 font-black">
                    Langkah {activeStep + 1}: {steps[activeStep].label}
                  </Typography>

                  {activeStep === 0 && (
                    <Grid container spacing={3}>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <FormControl fullWidth variant="outlined">
                          <InputLabel>Jalur SPMB</InputLabel>
                          <Select
                            label="Jalur SPMB"
                            name="admission_path_id"
                            value={formik.values.admission_path_id}
                            onChange={formik.handleChange}
                            error={formik.touched.admission_path_id && Boolean(formik.errors.admission_path_id)}
                          >
                            {admissionPaths.map((path) => (
                              <MenuItem key={path.id} value={path.id}>
                                {path.name}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <FormControl fullWidth variant="outlined">
                          <InputLabel>Tahun Ajaran</InputLabel>
                          <Select
                            label="Tahun Ajaran"
                            name="academic_year_id"
                            value={formik.values.academic_year_id}
                            onChange={formik.handleChange}
                            error={formik.touched.academic_year_id && Boolean(formik.errors.academic_year_id)}
                          >
                            {academicYears.map((year) => (
                              <MenuItem key={year.id} value={year.id}>
                                {year.year_name} ({year.semester})
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                    </Grid>
                  )}

                  {activeStep === 1 && (
                    <Grid container spacing={3}>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Nama Lengkap Calon Murid"
                          name="full_name"
                          value={formik.values.full_name}
                          onChange={formik.handleChange}
                          error={formik.touched.full_name && Boolean(formik.errors.full_name)}
                          helperText={formik.touched.full_name && formik.errors.full_name}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="NIK Calon Murid"
                          name="nik"
                          value={formik.values.nik}
                          onChange={formik.handleChange}
                          error={formik.touched.nik && Boolean(formik.errors.nik)}
                          helperText={formik.touched.nik && formik.errors.nik}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="NISN (Opsional)"
                          name="nisn"
                          value={formik.values.nisn}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <FormControl fullWidth variant="outlined">
                          <InputLabel>Jenis Kelamin</InputLabel>
                          <Select
                            label="Jenis Kelamin"
                            name="gender"
                            value={formik.values.gender}
                            onChange={formik.handleChange}
                          >
                            {genders.map((g) => (
                              <MenuItem key={g.value} value={g.value}>
                                {g.label}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Tempat Lahir"
                          name="birth_place"
                          value={formik.values.birth_place}
                          onChange={formik.handleChange}
                          error={formik.touched.birth_place && Boolean(formik.errors.birth_place)}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          type="date"
                          label="Tanggal Lahir"
                          name="birth_date"
                          InputLabelProps={{ shrink: true }}
                          value={formik.values.birth_date}
                          onChange={formik.handleChange}
                          error={formik.touched.birth_date && Boolean(formik.errors.birth_date)}
                        />
                      </Grid>
                      <Grid size={{ xs: 12 }}>
                        <FormControl fullWidth variant="outlined">
                          <InputLabel>Agama</InputLabel>
                          <Select
                            label="Agama"
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
                  )}

                  {activeStep === 2 && (
                    <Grid container spacing={3}>
                      <Grid size={{ xs: 12 }}>
                        <TextField
                          fullWidth
                          multiline
                          rows={2}
                          label="Alamat Lengkap"
                          name="address"
                          value={formik.values.address}
                          onChange={formik.handleChange}
                          error={formik.touched.address && Boolean(formik.errors.address)}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Desa/Kelurahan"
                          name="village"
                          value={formik.values.village}
                          onChange={formik.handleChange}
                          error={formik.touched.village && Boolean(formik.errors.village)}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Kecamatan"
                          name="district"
                          value={formik.values.district}
                          onChange={formik.handleChange}
                          error={formik.touched.district && Boolean(formik.errors.district)}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField fullWidth label="Kabupaten" name="regency" disabled value={formik.values.regency} />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField fullWidth label="Provinsi" name="province" disabled value={formik.values.province} />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Kode Pos"
                          name="postal_code"
                          value={formik.values.postal_code}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          type="number"
                          label="Jarak ke Sekolah (km)"
                          name="distance_to_school"
                          value={formik.values.distance_to_school}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      {isDomisili && (
                        <Grid size={{ xs: 12, md: 6 }}>
                          <TextField
                            fullWidth
                            type="date"
                            label="Tanggal Terbit Kartu Keluarga"
                            name="family_card_issue_date"
                            InputLabelProps={{ shrink: true }}
                            value={formik.values.family_card_issue_date}
                            onChange={formik.handleChange}
                            error={
                              formik.touched.family_card_issue_date && Boolean(formik.errors.family_card_issue_date)
                            }
                            helperText={formik.touched.family_card_issue_date && formik.errors.family_card_issue_date}
                          />
                        </Grid>
                      )}
                    </Grid>
                  )}

                  {activeStep === 3 && (
                    <Grid container spacing={3}>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Nama Ayah Kandung"
                          name="father_name"
                          value={formik.values.father_name}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="NIK Ayah"
                          name="father_nik"
                          value={formik.values.father_nik}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 12 }}>
                        <TextField
                          fullWidth
                          label="Pekerjaan Ayah"
                          name="father_occupation"
                          value={formik.values.father_occupation}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="Nama Ibu Kandung"
                          name="mother_name"
                          value={formik.values.mother_name}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 6 }}>
                        <TextField
                          fullWidth
                          label="NIK Ibu"
                          name="mother_nik"
                          value={formik.values.mother_nik}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12, md: 12 }}>
                        <TextField
                          fullWidth
                          label="Pekerjaan Ibu"
                          name="mother_occupation"
                          value={formik.values.mother_occupation}
                          onChange={formik.handleChange}
                        />
                      </Grid>
                      <Grid size={{ xs: 12 }}>
                        <TextField
                          fullWidth
                          label="Nomor HP Aktif (WhatsApp)"
                          name="phone_number"
                          value={formik.values.phone_number}
                          onChange={formik.handleChange}
                          error={formik.touched.phone_number && Boolean(formik.errors.phone_number)}
                          helperText={formik.touched.phone_number && formik.errors.phone_number}
                        />
                      </Grid>
                    </Grid>
                  )}

                  <Divider className="my-6" />

                  <Box className="flex items-center justify-between">
                    <Button
                      variant="text"
                      color="inherit"
                      disabled={activeStep === 0}
                      onClick={handleBack}
                      startIcon={<ArrowLeftIcon />}
                      className="font-bold"
                    >
                      Kembali
                    </Button>

                    {activeStep < steps.length - 1 ? (
                      <Button
                        variant="contained"
                        onClick={handleNext}
                        endIcon={<ArrowRightIcon />}
                        className="rounded-2xl px-8 py-3 font-bold shadow-xl"
                      >
                        Lanjutkan
                      </Button>
                    ) : (
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={() => formik.handleSubmit()}
                        className="rounded-2xl px-8 py-3 font-black shadow-xl"
                      >
                        Kirim Pendaftaran
                      </Button>
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </Box>
  );
}
