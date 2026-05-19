import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import * as Yup from "yup";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CircularProgress,
  Divider,
  FormControl,
  FormHelperText,
  Grid,
  IconButton,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";

import ToastEditor from "@/components/ToastEditor";
import { DEFAULTS } from "@/config";
import NiArrowLeft from "@/icons/nexture/ni-arrow-left";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiBook from "@/icons/nexture/ni-book";
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiExclamationSquare from "@/icons/nexture/ni-exclamation-square";
import NiGraduation from "@/icons/nexture/ni-graduation";
import NiPlus from "@/icons/nexture/ni-plus";

export default function Page() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [phases, setPhases] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [elements, setElements] = useState<any[]>([]);
  const [apiError, setApiError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch initial data (Phases & Subjects)
  useEffect(() => {
    const fetchInitialData = async () => {
      const token = localStorage.getItem("accessToken");
      try {
        const [phaseRes, subjectRes] = await Promise.all([
          fetch(`${DEFAULTS.API_URL}/api/v1/phases`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${DEFAULTS.API_URL}/api/v1/subjects`, { headers: { Authorization: `Bearer ${token}` } }),
        ]);

        const phaseJson = await phaseRes.json();
        const subjectJson = await subjectRes.json();

        if (phaseJson.status === "success") setPhases(phaseJson.data || []);
        if (subjectJson.status === "success") setSubjects(subjectJson.data || []);
      } catch (err) {
        console.error("Failed to fetch initial data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchInitialData();
  }, []);

  const formik = useFormik({
    initialValues: {
      phase_id: "",
      subject_id: "",
      year_sk: "26",
      details: [] as { element_id: string; sub_code: string; detail_text: string; sequence_no: number }[],
    },
    validationSchema: Yup.object({
      phase_id: Yup.string().required(t("curriculum-validation.phase-required")),
      subject_id: Yup.string().required(t("curriculum-validation.subject-required")),
      year_sk: Yup.string().required(t("curriculum-validation.year-required")).max(10),
      details: Yup.array()
        .of(
          Yup.object({
            element_id: Yup.string().required(t("curriculum-validation.element-required")),
            detail_text: Yup.string().required(t("curriculum-validation.detail-required")),
          }),
        )
        .test("unique-elements", t("curriculum-validation.duplicate-element"), function (value) {
          if (!value) return true;
          const ids = value.map((v) => v.element_id).filter(Boolean);
          const hasDuplicates = ids.some((val, i) => ids.indexOf(val) !== i);
          return !hasDuplicates;
        }),
    }),
    onSubmit: async (values, { setSubmitting }) => {
      setApiError(null);
      try {
        const token = localStorage.getItem("accessToken");
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-outcomes`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(values),
        });

        const json = await res.json();
        if (json.status === "success") {
          navigate("/academic/curriculum");
        } else {
          setApiError(json.message || "Gagal menyimpan data CP");
        }
      } catch (err: any) {
        setApiError(err.message || "Terjadi kesalahan jaringan");
      } finally {
        setSubmitting(false);
      }
    },
  });

  // Fetch elements when subject changes
  useEffect(() => {
    if (!formik.values.subject_id) {
      setElements([]);
      return;
    }
    const fetchElements = async () => {
      const token = localStorage.getItem("accessToken");
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects/${formik.values.subject_id}/elements`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success") {
          setElements(json.data || []);
        }
      } catch (err) {
        console.error("Failed to fetch elements", err);
      }
    };
    fetchElements();
  }, [formik.values.subject_id]);

  return (
    <Box className="pb-10">
      <Box className="mb-4 flex items-center gap-4">
        <Button
          variant="outlined"
          size="small"
          onClick={() => navigate("/academic/curriculum")}
          className="min-w-0 p-2"
        >
          <NiArrowLeft size="small" />
        </Button>
        <Typography variant="h1" component="h1" className="mb-0">
          {t("curriculum-validation.add-title")}
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link color="inherit" to="/home">
          {t("curriculum-validation.breadcrumb-home")}
        </Link>
        <Link color="inherit" to="/academic">
          {t("curriculum-validation.breadcrumb-academic")}
        </Link>
        <Link color="inherit" to="/academic/curriculum">
          {t("curriculum-validation.breadcrumb-curriculum")}
        </Link>
        <Typography variant="body2">{t("curriculum-validation.breadcrumb-add")}</Typography>
      </Breadcrumbs>

      <Card variant="outlined" className="border-divider p-6">
        {loading ? (
          <Box className="flex h-64 flex-col items-center justify-center gap-4">
            <CircularProgress size={40} />
            <Typography variant="body2" color="textSecondary">
              {t("curriculum-validation.form-loading-data")}
            </Typography>
          </Box>
        ) : phases.length === 0 || subjects.length === 0 ? (
          <Box className="flex flex-col items-center justify-center py-10 text-center">
            <Box className="bg-warning/10 text-warning mb-6 rounded-2xl p-4">
              <NiExclamationSquare size={48} />
            </Box>
            <Typography variant="h4" component="h2" className="mb-2 font-bold">
              {t("curriculum-validation.support-data-empty")}
            </Typography>
            <Typography variant="body1" color="textSecondary" className="mb-8 max-w-md">
              {t("curriculum-validation.support-data-empty-desc")}
            </Typography>

            <Grid container spacing={3} className="max-w-2xl justify-center">
              {phases.length === 0 && (
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Card variant="outlined" className="border-primary/20 border p-5">
                    <Box className="mb-4 flex items-center gap-3">
                      <Box className="bg-primary/20 text-primary rounded-lg p-2">
                        <NiGraduation size={24} />
                      </Box>
                      <Typography variant="subtitle1" className="font-bold">
                        {t("curriculum-validation.support-phase-title")}
                      </Typography>
                    </Box>
                    <Typography variant="body2" className="text-text-secondary mb-4 text-left">
                      {t("curriculum-validation.support-phase-desc")}
                    </Typography>
                    <Button
                      fullWidth
                      variant="contained"
                      size="small"
                      onClick={() => navigate("/academic/phases")}
                      startIcon={<NiPlus size="small" />}
                    >
                      {t("curriculum-validation.support-phase-btn")}
                    </Button>
                  </Card>
                </Grid>
              )}
              {subjects.length === 0 && (
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Card variant="outlined" className="border-secondary/20 border p-5">
                    <Box className="mb-4 flex items-center gap-3">
                      <Box className="bg-secondary/20 text-secondary rounded-lg p-2">
                        <NiBook size={24} />
                      </Box>
                      <Typography variant="subtitle1" className="font-bold">
                        {t("curriculum-validation.support-subject-title")}
                      </Typography>
                    </Box>
                    <Typography variant="body2" className="text-text-secondary mb-4 text-left">
                      {t("curriculum-validation.support-subject-desc")}
                    </Typography>
                    <Button
                      fullWidth
                      variant="contained"
                      size="small"
                      color="secondary"
                      onClick={() => navigate("/academic/subjects")}
                      startIcon={<NiPlus size="small" />}
                    >
                      {t("curriculum-validation.support-subject-btn")}
                    </Button>
                  </Card>
                </Grid>
              )}
            </Grid>
          </Box>
        ) : (
          <form onSubmit={formik.handleSubmit}>
            {apiError && (
              <Alert severity="error" className="mb-6">
                {apiError}
              </Alert>
            )}

            <Grid container spacing={4}>
              <Grid size={{ xs: 12, md: 4 }}>
                <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                  {t("curriculum-validation.form-phase-label")}
                </Typography>
                <FormControl fullWidth size="small" error={formik.touched.phase_id && Boolean(formik.errors.phase_id)}>
                  <Select
                    name="phase_id"
                    value={formik.values.phase_id}
                    onChange={formik.handleChange}
                    IconComponent={NiChevronDownSmall}
                    displayEmpty
                  >
                    <MenuItem value="" disabled>
                      {t("curriculum-validation.form-phase-placeholder")}
                    </MenuItem>
                    {phases.map((p) => (
                      <MenuItem key={p.id} value={p.id}>
                        {p.phase_name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.phase_id && <FormHelperText>{formik.errors.phase_id}</FormHelperText>}
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 5 }}>
                <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                  {t("curriculum-validation.form-subject-label")}
                </Typography>
                <FormControl
                  fullWidth
                  size="small"
                  error={formik.touched.subject_id && Boolean(formik.errors.subject_id)}
                >
                  <Select
                    name="subject_id"
                    value={formik.values.subject_id}
                    onChange={(e) => {
                      formik.handleChange(e);
                      formik.setFieldValue("details", []); // Reset details when subject changes
                    }}
                    IconComponent={NiChevronDownSmall}
                    displayEmpty
                  >
                    <MenuItem value="" disabled>
                      {t("curriculum-validation.form-subject-placeholder")}
                    </MenuItem>
                    {subjects.map((s) => (
                      <MenuItem key={s.id} value={s.id}>
                        {s.subject_name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.subject_id && <FormHelperText>{formik.errors.subject_id}</FormHelperText>}
                </FormControl>
              </Grid>

              <Grid size={{ xs: 12, md: 3 }}>
                <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                  {t("curriculum-validation.form-year-label")}
                </Typography>
                <TextField
                  fullWidth
                  name="year_sk"
                  placeholder={t("curriculum-validation.form-year-placeholder")}
                  value={formik.values.year_sk}
                  onChange={formik.handleChange}
                  error={formik.touched.year_sk && Boolean(formik.errors.year_sk)}
                  helperText={formik.touched.year_sk && formik.errors.year_sk}
                  size="small"
                />
              </Grid>

              <Grid size={12}>
                <Divider className="my-4" />
                <Box className="mb-6 flex items-center justify-between">
                  <Box>
                    <Typography variant="h6" className="font-bold">
                      {t("curriculum-validation.form-elements-title")}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {t("curriculum-validation.form-elements-desc")}
                    </Typography>
                  </Box>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<NiPlus size="small" />}
                    onClick={() => {
                      const details = [...formik.values.details];
                      details.push({ element_id: "", sub_code: "", detail_text: "", sequence_no: details.length + 1 });
                      formik.setFieldValue("details", details);
                    }}
                    disabled={!formik.values.subject_id}
                  >
                    {t("curriculum-validation.form-add-element-btn")}
                  </Button>
                </Box>

                {typeof formik.errors.details === "string" && (
                  <Alert severity="error" className="mb-4">
                    {formik.errors.details}
                  </Alert>
                )}

                <Box className="flex flex-col gap-6">
                  {formik.values.details.map((detail, index) => (
                    <Card key={index} variant="outlined" className="border-divider border p-5">
                      <Box className="mb-4 flex items-center justify-between">
                        <Typography variant="subtitle2" className="text-primary font-bold">
                          {t("curriculum-validation.form-detail-element-title")} #{index + 1}
                        </Typography>
                        <IconButton
                          color="error"
                          size="small"
                          onClick={() => {
                            const details = [...formik.values.details];
                            details.splice(index, 1);
                            formik.setFieldValue("details", details);
                          }}
                        >
                          <NiBinEmpty size="small" />
                        </IconButton>
                      </Box>

                      <Grid container spacing={3}>
                        <Grid size={{ xs: 12, md: 5 }}>
                          <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                            {t("curriculum-validation.form-select-element-label")}
                          </Typography>
                          <FormControl
                            fullWidth
                            size="small"
                            error={Boolean((formik.errors.details as any)?.[index]?.element_id)}
                          >
                            <Select
                              value={detail.element_id}
                              onChange={(e) => formik.setFieldValue(`details.${index}.element_id`, e.target.value)}
                              IconComponent={NiChevronDownSmall}
                              displayEmpty
                            >
                              <MenuItem value="" disabled>
                                {t("curriculum-validation.form-select-element-placeholder")}
                              </MenuItem>
                              {elements.map((e) => {
                                const isAlreadySelected = formik.values.details.some(
                                  (d, idx) => d.element_id === e.id && idx !== index,
                                );
                                return (
                                  <MenuItem key={e.id} value={e.id} disabled={isAlreadySelected}>
                                    {e.element_name} ({e.abbreviation}){" "}
                                    {isAlreadySelected && `— ${t("curriculum-validation.form-select-element-already")}`}
                                  </MenuItem>
                                );
                              })}
                            </Select>
                          </FormControl>
                        </Grid>

                        <Grid size={12}>
                          <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                            {t("curriculum-validation.form-description-label")}
                          </Typography>
                          <ToastEditor
                            value={detail.detail_text}
                            onChange={(val) => formik.setFieldValue(`details.${index}.detail_text`, val)}
                          />
                        </Grid>
                      </Grid>
                    </Card>
                  ))}

                  {formik.values.details.length === 0 && (
                    <Box className="bg-surface-standard border-divider rounded-xl border border-dashed py-16 text-center">
                      <Box className="bg-primary/10 text-primary mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full">
                        <NiBook size="large" />
                      </Box>
                      <Typography variant="h6" className="font-bold">
                        {t("curriculum-validation.form-no-elements-title")}
                      </Typography>
                      <Typography variant="body2" color="textSecondary" className="mx-auto max-w-xs italic">
                        {!formik.values.subject_id
                          ? t("curriculum-validation.form-no-elements-phase-hint")
                          : t("curriculum-validation.form-no-elements-add-hint")}
                      </Typography>
                    </Box>
                  )}
                </Box>
              </Grid>

              <Grid size={12} className="mt-8 flex justify-end gap-3">
                <Button variant="outlined" onClick={() => navigate("/academic/curriculum")}>
                  {t("curriculum-validation.form-btn-cancel")}
                </Button>
                <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
                  {formik.isSubmitting ? <CircularProgress size={24} /> : t("curriculum-validation.form-btn-save")}
                </Button>
              </Grid>
            </Grid>
          </form>
        )}
      </Card>
    </Box>
  );
}
