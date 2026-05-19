/* eslint-disable @typescript-eslint/no-unused-vars */
import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
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
  Grid,
  IconButton,
  MenuItem,
  Select,
  Skeleton,
  Snackbar,
  TextField,
  Typography,
} from "@mui/material";

import ToastEditor from "@/components/ToastEditor";
import { DEFAULTS } from "@/config";
import NiArrowLeft from "@/icons/nexture/ni-arrow-left";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiPlus from "@/icons/nexture/ni-plus";

export default function EditSubjectPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const id = searchParams.get("id");

  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [subject, setSubject] = useState<any>(null);

  const formik = useFormik({
    initialValues: {
      subject_code: subject?.subject_code || "",
      subject_name: subject?.subject_name || "",
      rational: subject?.rational || "",
      goals: subject?.goals || "",
      characteristics: subject?.characteristics || "",
      is_active: subject?.is_active ?? true,
      characteristic_points: (subject?.characteristic_points || []).map((p: any) => ({
        id: p.id,
        description: p.description,
        elements: (p.elements || []).map((e: any) => ({
          id: e.id,
          element_name: e.element_name,
          abbreviation: e.abbreviation || "",
          description: e.description,
        })),
      })) as {
        id?: string;
        description: string;
        elements: { id?: string; element_name: string; abbreviation: string; description: string }[];
      }[],
    },
    enableReinitialize: true,
    validationSchema: Yup.object({
      subject_name: Yup.string().required("Nama mata pelajaran wajib diisi"),
      characteristic_points: Yup.array().of(
        Yup.object({
          description: Yup.string().required("Deskripsi poin wajib diisi"),
          elements: Yup.array().of(
            Yup.object({
              element_name: Yup.string().required("Nama elemen wajib diisi"),
              description: Yup.string().required("Deskripsi elemen wajib diisi"),
            }),
          ),
        }),
      ),
    }),
    onSubmit: async (values, { setSubmitting }) => {
      setApiError(null);
      setSuccessMessage(null);
      try {
        const token = localStorage.getItem("accessToken");
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(values),
        });

        const json = await res.json();
        if (json.status === "success") {
          setSuccessMessage("Mata pelajaran berhasil diperbarui! / Subject successfully updated!");

          // Re-fetch or update subject state to sync any newly generated IDs
          if (json.data) {
            setSubject(json.data);
          }
        } else {
          setApiError(json.message || "Gagal memperbarui data mata pelajaran");
        }
      } catch (err: any) {
        setApiError(err.message || "Terjadi kesalahan jaringan");
      } finally {
        setSubmitting(false);
      }
    },
  });

  useEffect(() => {
    if (!id) {
      navigate("/academic/subjects");
      return;
    }

    const fetchSubject = async () => {
      const token = localStorage.getItem("accessToken");
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success" && json.data) {
          setSubject(json.data);

          // Explicitly set formik values to ensure sync
          const data = json.data;
          formik.setValues({
            subject_code: data.subject_code || "",
            subject_name: data.subject_name || "",
            rational: data.rational || "",
            goals: data.goals || "",
            characteristics: data.characteristics || "",
            is_active: data.is_active ?? true,
            characteristic_points: (data.characteristic_points || []).map((p: any) => ({
              id: p.id,
              description: p.description || "",
              elements: (p.elements || []).map((e: any) => ({
                id: e.id,
                element_name: e.element_name || "",
                abbreviation: e.abbreviation || "",
                description: e.description || "",
              })),
            })),
          });
        } else {
          setApiError(json.message);
        }
      } catch (err: any) {
        setApiError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSubject();
  }, [id, navigate]);

  return (
    <Box>
      <Box className="mb-2 flex items-center gap-4">
        <Button
          variant="outlined"
          color="primary"
          onClick={() => navigate("/academic/subjects")}
          className="min-w-0 p-2"
        >
          <NiArrowLeft size="small" />
        </Button>
        <Box>
          <Typography variant="h1" component="h1" className="mb-0">
            Edit Mata Pelajaran
          </Typography>
        </Box>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link color="inherit" to="/home">
          Beranda
        </Link>
        <Link color="inherit" to="/academic">
          Akademik
        </Link>
        <Link color="inherit" to="/academic/subjects">
          Mata Pelajaran
        </Link>
        <Typography variant="body2">Edit</Typography>
      </Breadcrumbs>
      <Card variant="outlined" className="border-divider p-6">
        {apiError && (
          <Alert severity="error" className="mb-6">
            {apiError}
          </Alert>
        )}

        <form onSubmit={formik.handleSubmit}>
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 4 }}>
              <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                Kode Mata Pelajaran
              </Typography>
              {loading || !subject ? (
                <Skeleton variant="rectangular" height={40} className="rounded" />
              ) : (
                <TextField fullWidth name="subject_code" value={formik.values.subject_code} disabled size="small" />
              )}
            </Grid>
            <Grid size={{ xs: 12, md: 5 }}>
              <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                Nama Mata Pelajaran
              </Typography>
              {loading || !subject ? (
                <Skeleton variant="rectangular" height={40} className="rounded" />
              ) : (
                <TextField
                  fullWidth
                  name="subject_name"
                  value={formik.values.subject_name}
                  onChange={formik.handleChange}
                  size="small"
                />
              )}
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                Status
              </Typography>
              {loading || !subject ? (
                <Skeleton variant="rectangular" height={40} className="rounded" />
              ) : (
                <FormControl fullWidth size="small">
                  <Select name="is_active" value={formik.values.is_active} onChange={formik.handleChange}>
                    <MenuItem value={true as any}>Aktif</MenuItem>
                    <MenuItem value={false as any}>Non-aktif</MenuItem>
                  </Select>
                </FormControl>
              )}
            </Grid>

            <Grid size={12}>
              <Typography variant="subtitle2" className="mb-2 font-bold">
                Rasional
              </Typography>
              <Box>
                {loading || !subject ? (
                  <Skeleton variant="rectangular" height={300} className="rounded-lg" />
                ) : (
                  <ToastEditor
                    key={`rational-${id}-${loading}`}
                    value={formik.values.rational}
                    onChange={(val) => formik.setFieldValue("rational", val)}
                  />
                )}
              </Box>
            </Grid>

            <Grid size={12} className="mt-4">
              <Typography variant="subtitle2" className="mb-2 font-bold">
                Tujuan
              </Typography>
              <Box>
                {loading || !subject ? (
                  <Skeleton variant="rectangular" height={300} className="rounded-lg" />
                ) : (
                  <ToastEditor
                    key={`goals-${id}-${loading}`}
                    value={formik.values.goals}
                    onChange={(val) => formik.setFieldValue("goals", val)}
                  />
                )}
              </Box>
            </Grid>

            <Grid size={12} className="mt-4">
              <Typography variant="subtitle2" className="mb-2 font-bold">
                Karakteristik (Umum)
              </Typography>
              <Box>
                {loading || !subject ? (
                  <Skeleton variant="rectangular" height={300} className="rounded-lg" />
                ) : (
                  <ToastEditor
                    key={`characteristics-${id}-${loading}`}
                    value={formik.values.characteristics}
                    onChange={(val) => formik.setFieldValue("characteristics", val)}
                  />
                )}
              </Box>
            </Grid>

            {/* Poin Karakteristik & Elemen */}
            <Grid size={12} className="mt-8">
              <Divider className="mb-6" />
              <Box className="mb-6 flex items-center justify-between">
                <Box>
                  <Typography variant="h6" className="font-bold">
                    Poin Karakteristik & Elemen
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Tambahkan poin-poin karakteristik beserta elemen-elemennya.
                  </Typography>
                </Box>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<NiPlus size="small" />}
                  onClick={() => {
                    const points = [...formik.values.characteristic_points];
                    points.push({ description: "", elements: [] });
                    formik.setFieldValue("characteristic_points", points);
                  }}
                >
                  Tambah Poin
                </Button>
              </Box>

              <Box className="flex flex-col gap-6">
                {loading || !subject ? (
                  <>
                    <Skeleton variant="rectangular" height={150} className="rounded-lg" />
                    <Skeleton variant="rectangular" height={150} className="rounded-lg" />
                  </>
                ) : (
                  formik.values.characteristic_points.map((point, pIndex) => (
                    <Card key={pIndex} variant="outlined" className="border-divider border p-5">
                      <Box className="mb-4 flex items-center justify-between">
                        <Typography variant="subtitle2" className="text-primary font-bold">
                          Poin Karakteristik {pIndex + 1}
                        </Typography>
                        <IconButton
                          color="error"
                          size="small"
                          onClick={() => {
                            const points = [...formik.values.characteristic_points];
                            points.splice(pIndex, 1);
                            formik.setFieldValue("characteristic_points", points);
                          }}
                        >
                          <NiBinEmpty size="small" />
                        </IconButton>
                      </Box>

                      <Box className="mb-6">
                        <Typography
                          variant="caption"
                          color="textSecondary"
                          className="mb-2 block font-bold tracking-wider uppercase"
                        >
                          Deskripsi Poin
                        </Typography>
                        <ToastEditor
                          key={`point-${pIndex}-${id}-${loading}`}
                          value={point.description}
                          onChange={(val) => formik.setFieldValue(`characteristic_points[${pIndex}].description`, val)}
                        />
                      </Box>

                      <Box className="ml-8">
                        <Box className="mb-4 flex items-center justify-between">
                          <Typography variant="subtitle2" className="text-primary font-bold">
                            Elemen pada Poin Ini
                          </Typography>
                          <Button
                            variant="text"
                            size="small"
                            color="primary"
                            startIcon={<NiPlus size="small" />}
                            onClick={() => {
                              const points = [...formik.values.characteristic_points];
                              points[pIndex].elements.push({ element_name: "", abbreviation: "", description: "" });
                              formik.setFieldValue("characteristic_points", points);
                            }}
                          >
                            Tambah Elemen
                          </Button>
                        </Box>

                        <Box className="flex flex-col gap-4">
                          {point.elements.map((element, eIndex) => (
                            <Card key={eIndex} variant="outlined" className="border-dashed bg-white/50 p-4">
                              <Grid container spacing={3}>
                                <Grid size={{ xs: 12, md: 11 }}>
                                  <TextField
                                    fullWidth
                                    size="small"
                                    label="Nama Elemen"
                                    name={`characteristic_points[${pIndex}].elements[${eIndex}].element_name`}
                                    value={element.element_name}
                                    onChange={formik.handleChange}
                                    error={
                                      (formik.touched.characteristic_points?.[pIndex] as any)?.elements?.[eIndex]
                                        ?.element_name &&
                                      Boolean(
                                        (formik.errors.characteristic_points?.[pIndex] as any)?.elements?.[eIndex]
                                          ?.element_name,
                                      )
                                    }
                                  />
                                </Grid>
                                <Grid size={{ xs: 12, md: 1 }} className="flex items-center justify-center">
                                  <IconButton
                                    color="error"
                                    size="small"
                                    onClick={() => {
                                      const points = [...formik.values.characteristic_points];
                                      points[pIndex].elements.splice(eIndex, 1);
                                      formik.setFieldValue("characteristic_points", points);
                                    }}
                                  >
                                    <NiBinEmpty size="small" />
                                  </IconButton>
                                </Grid>
                                <Grid size={12}>
                                  <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                                    Deskripsi Elemen
                                  </Typography>
                                  <ToastEditor
                                    key={`element-${pIndex}-${eIndex}-${id}-${loading}`}
                                    value={element.description}
                                    onChange={(val) =>
                                      formik.setFieldValue(
                                        `characteristic_points[${pIndex}].elements[${eIndex}].description`,
                                        val,
                                      )
                                    }
                                  />
                                </Grid>
                              </Grid>
                            </Card>
                          ))}
                        </Box>
                      </Box>
                    </Card>
                  ))
                )}
              </Box>
            </Grid>

            <Grid size={12} className="mt-8 flex justify-end gap-3">
              <Button variant="outlined" onClick={() => navigate("/academic/subjects")}>
                Batal
              </Button>
              <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
                Simpan Perubahan
              </Button>
            </Grid>
          </Grid>
        </form>
      </Card>

      <Snackbar
        open={Boolean(successMessage)}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage(null)}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert onClose={() => setSuccessMessage(null)} severity="success" variant="filled">
          {successMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
}
