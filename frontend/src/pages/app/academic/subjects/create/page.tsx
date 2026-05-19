/* eslint-disable @typescript-eslint/no-unused-vars */
import { useFormik } from "formik";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import * as Yup from "yup";

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
import NiPlus from "@/icons/nexture/ni-plus";

export default function CreateSubjectPage() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      subject_name: "",
      rational: "",
      goals: "",
      characteristics: "",
      is_active: true,
      characteristic_points: [] as {
        description: string;
        elements: { element_name: string; abbreviation: string; description: string }[];
      }[],
    },
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
      try {
        const token = localStorage.getItem("accessToken");
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/subjects`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(values),
        });

        const json = await res.json();
        if (json.status === "success") {
          navigate("/academic/subjects");
        } else {
          setApiError(json.message || "Gagal menyimpan data mata pelajaran");
        }
      } catch (err: any) {
        setApiError(err.message || "Terjadi kesalahan jaringan");
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <Box className="pb-10">
      <Box className="mb-4 flex items-center gap-4">
        <Button variant="outlined" size="small" onClick={() => navigate("/academic/subjects")} className="min-w-0 p-2">
          <NiArrowLeft size="small" />
        </Button>
        <Box>
          <Typography variant="h1" component="h1" className="mb-0">
            Tambah Mata Pelajaran
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
        <Typography variant="body2">Tambah</Typography>
      </Breadcrumbs>

      <Card variant="outlined" className="border-divider p-6">
        {apiError && (
          <Alert severity="error" className="mb-6">
            {apiError}
          </Alert>
        )}

        <form onSubmit={formik.handleSubmit}>
          <Grid container spacing={4}>
            <Grid size={{ xs: 12, md: 9 }}>
              <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                Nama Mata Pelajaran
              </Typography>
              <TextField
                fullWidth
                name="subject_name"
                placeholder="Masukkan nama mata pelajaran"
                value={formik.values.subject_name}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                error={formik.touched.subject_name && Boolean(formik.errors.subject_name)}
                helperText={formik.touched.subject_name && formik.errors.subject_name}
                size="small"
              />
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <Typography variant="caption" color="textSecondary" className="mb-2 block font-bold">
                Status
              </Typography>
              <FormControl fullWidth size="small">
                <Select name="is_active" value={formik.values.is_active} onChange={formik.handleChange}>
                  <MenuItem value={true as any}>Aktif</MenuItem>
                  <MenuItem value={false as any}>Non-aktif</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid size={12}>
              <Typography variant="subtitle2" className="mb-2 font-bold">
                Rasional
              </Typography>
              <ToastEditor value={formik.values.rational} onChange={(val) => formik.setFieldValue("rational", val)} />
            </Grid>

            <Grid size={12} className="mt-4">
              <Typography variant="subtitle2" className="mb-2 font-bold">
                Tujuan
              </Typography>
              <ToastEditor value={formik.values.goals} onChange={(val) => formik.setFieldValue("goals", val)} />
            </Grid>

            <Grid size={12} className="mt-4">
              <Typography variant="subtitle2" className="mb-2 font-bold">
                Karakteristik (Umum)
              </Typography>
              <ToastEditor
                value={formik.values.characteristics}
                onChange={(val) => formik.setFieldValue("characteristics", val)}
              />
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
                {formik.values.characteristic_points.map((point, pIndex) => (
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
                        {point.elements.length === 0 && (
                          <Typography
                            variant="body2"
                            color="textSecondary"
                            className="rounded-lg border border-dashed bg-gray-50/50 py-4 text-center italic"
                          >
                            Belum ada elemen. Klik "Tambah Elemen" untuk menambahkan.
                          </Typography>
                        )}
                      </Box>
                    </Box>
                  </Card>
                ))}

                {formik.values.characteristic_points.length === 0 && (
                  <Box className="border-divider flex flex-col items-center justify-center rounded-xl border-2 border-dashed bg-gray-50/30 py-12">
                    <Typography variant="body1" color="textSecondary" className="mb-4">
                      Belum ada poin karakteristik terstruktur.
                    </Typography>
                    <Button
                      variant="outlined"
                      startIcon={<NiPlus size="small" />}
                      onClick={() => {
                        const points = [...formik.values.characteristic_points];
                        points.push({ description: "", elements: [] });
                        formik.setFieldValue("characteristic_points", points);
                      }}
                    >
                      Mulai Tambahkan Poin
                    </Button>
                  </Box>
                )}
              </Box>
            </Grid>

            <Grid size={12} className="mt-8 flex justify-end gap-3">
              <Button variant="outlined" onClick={() => navigate("/academic/subjects")}>
                Batal
              </Button>
              <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
                Simpan Mata Pelajaran
              </Button>
            </Grid>
          </Grid>
        </form>
      </Card>
    </Box>
  );
}
