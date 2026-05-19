/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CircularProgress,
  Divider,
  Grid,
  Skeleton,
  Typography,
} from "@mui/material";

import ToastViewer from "@/components/ToastViewer";
import { DEFAULTS } from "@/config";
import NiArrowLeft from "@/icons/nexture/ni-arrow-left";

export default function ViewSubjectPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const id = searchParams.get("id");

  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);
  const [subject, setSubject] = useState<any>(null);

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
        if (json.status === "success") {
          setSubject(json.data);
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
            Detail Mata Pelajaran
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
        <Typography variant="body2">Detail</Typography>
      </Breadcrumbs>

      <Card variant="outlined" className="border-divider p-6">
        {apiError && (
          <Alert severity="error" className="mb-6">
            {apiError}
          </Alert>
        )}

        <Grid container spacing={4}>
          <Grid size={{ xs: 12, md: 6 }}>
            <Typography variant="caption" color="textSecondary" className="mb-1 block font-bold">
              Kode Mata Pelajaran
            </Typography>
            {loading || !subject ? (
              <Skeleton variant="text" width="60%" height={24} />
            ) : (
              <Typography variant="body1" className="font-medium">
                {subject?.subject_code}
              </Typography>
            )}
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <Typography variant="caption" color="textSecondary" className="mb-1 block font-bold">
              Nama Mata Pelajaran
            </Typography>
            {loading || !subject ? (
              <Skeleton variant="text" width="80%" height={24} />
            ) : (
              <Typography variant="body1" className="font-medium">
                {subject?.subject_name}
              </Typography>
            )}
          </Grid>

          <Grid size={12}>
            <Divider />
          </Grid>

          <Grid size={12}>
            <Typography variant="subtitle2" className="mb-2 font-bold">
              Rasional
            </Typography>
            {loading || !subject ? (
              <Skeleton variant="rectangular" height={100} className="rounded-lg" />
            ) : (
              <Box className="bg-surface-standard rounded-lg border p-4">
                <ToastViewer value={subject?.rational} />
              </Box>
            )}
          </Grid>

          <Grid size={12}>
            <Typography variant="subtitle2" className="mb-2 font-bold">
              Tujuan
            </Typography>
            {loading || !subject ? (
              <Skeleton variant="rectangular" height={100} className="rounded-lg" />
            ) : (
              <Box className="bg-surface-standard rounded-lg border p-4">
                <ToastViewer value={subject?.goals} />
              </Box>
            )}
          </Grid>

          <Grid size={12}>
            <Typography variant="subtitle2" className="mb-2 font-bold">
              Karakteristik (Umum)
            </Typography>
            {loading || !subject ? (
              <Skeleton variant="rectangular" height={100} className="rounded-lg" />
            ) : (
              <Box className="bg-surface-standard rounded-lg border p-4">
                <ToastViewer value={subject?.characteristics} />
              </Box>
            )}
          </Grid>

          <Grid size={12}>
            <Divider className="my-4" />
            <Typography variant="h6" className="mb-4 font-bold">
              Poin Karakteristik & Elemen
            </Typography>
            <Box className="flex flex-col gap-6">
              {loading || !subject ? (
                <>
                  <Skeleton variant="rectangular" height={150} className="rounded-lg" />
                  <Skeleton variant="rectangular" height={150} className="rounded-lg" />
                </>
              ) : (
                subject?.characteristic_points?.map((point: any, pIndex: number) => (
                  <Card key={pIndex} variant="outlined" className="border-divider border p-5">
                    <Typography variant="subtitle2" className="text-primary mb-4 font-bold">
                      Poin {pIndex + 1}
                    </Typography>
                    <Box className="bg-surface-standard mb-6 rounded-lg border p-4">
                      <ToastViewer value={point.description} />
                    </Box>

                    <Typography
                      variant="caption"
                      color="textSecondary"
                      className="mb-3 block font-bold tracking-wider uppercase"
                    >
                      Elemen-elemen:
                    </Typography>
                    <Box className="flex flex-col gap-4">
                      {point.elements?.map((element: any, eIndex: number) => (
                        <Card key={eIndex} variant="outlined" className="bg-background-paper border-dashed p-4">
                          <Typography variant="body2" className="text-secondary mb-2 font-bold">
                            {element.element_name} ({element.abbreviation})
                          </Typography>
                          <Box className="bg-surface-standard rounded-lg border p-4">
                            <ToastViewer value={element.description} />
                          </Box>
                        </Card>
                      ))}
                    </Box>
                  </Card>
                ))
              )}
            </Box>
          </Grid>
        </Grid>
      </Card>
    </Box>
  );
}
