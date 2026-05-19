/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import {
  Box,
  Breadcrumbs,
  Button,
  Card,
  Chip,
  CircularProgress,
  Grid,
  List,
  ListItem,
  ListItemText,
  Paper,
  Skeleton,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  Tabs,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import NiArrowLeft from "@/icons/nexture/ni-arrow-left";
import NiBook from "@/icons/nexture/ni-book";

interface CPDetail {
  id: string;
  sub_code: string;
  detail_text: string;
  sequence_no: number;
  element: { element_name: string; description: string };
}

interface LearningOutcomeDetail {
  id: string;
  cp_code: string;
  outcome_text?: string;
  phase: { phase_name: string };
  subject: {
    subject_name: string;
    rational?: string;
    goals?: string;
    characteristics?: string;
  };
  details: CPDetail[];
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`cp-tabpanel-${index}`}
      aria-labelledby={`cp-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 10, px: 3, pb: 3 }}>{children}</Box>}
    </div>
  );
}

export default function Page() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const id = searchParams.get("id");
  const [data, setData] = useState<LearningOutcomeDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-outcomes/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success") {
          setData(json.data);
        } else {
          setError(json.message || "Failed to fetch details");
        }
      } catch (err: any) {
        setError(err.message || "Network error");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "cp_details", data: data?.details || [], defaultLimit: 10 });

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
          Detail Capaian Pembelajaran
        </Typography>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link color="inherit" to="/home">
          Beranda
        </Link>
        <Link color="inherit" to="/academic">
          Akademik
        </Link>
        <Link color="inherit" to="/academic/curriculum">
          Capaian Pembelajaran
        </Link>
        <Typography variant="body2">Detail</Typography>
      </Breadcrumbs>

      {error ? (
        <Box className="py-20 text-center">
          <Typography variant="h5" color="text.secondary">
            {error}
          </Typography>
          <Button
            variant="outlined"
            startIcon={<NiArrowLeft size="small" />}
            className="mt-4"
            onClick={() => navigate("/academic/curriculum")}
          >
            Kembali ke Daftar
          </Button>
        </Box>
      ) : (
        <Grid size={{ xs: 12 }}>
          {/* Card and Tabs */}
          <Card variant="outlined" className="border-divider overflow-hidden">
            <Box className="bg-surface-standard border-divider flex items-center justify-between border-b px-5 py-4">
              <Box className="flex items-center gap-3">
                <Box className="bg-primary/10 text-primary rounded-lg p-2">
                  <NiBook size="large" />
                </Box>
                <Box>
                  <Typography variant="h5" component="h3" className="font-bold">
                    {loading ? <Skeleton width={200} height={28} /> : data?.subject?.subject_name || "Mata Pelajaran"}
                  </Typography>
                  <Box className="mt-1 flex items-center gap-2">
                    {loading ? (
                      <>
                        <Skeleton width={80} height={20} />
                        <Skeleton width={120} height={20} />
                      </>
                    ) : (
                      <>
                        <Chip size="small" label={data?.phase?.phase_name} color="primary" variant="outlined" />
                        <Chip size="small" label={`Kode: ${data?.cp_code}`} variant="outlined" />
                      </>
                    )}
                  </Box>
                </Box>
              </Box>
              <Button
                variant="outlined"
                size="small"
                disabled={loading}
                onClick={() => data && navigate(`/academic/curriculum/edit?id=${data.id}`)}
              >
                Edit CP
              </Button>
            </Box>

            <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
              <Tabs value={tabValue} onChange={handleTabChange} aria-label="cp tabs" className="px-5">
                <Tab label="Capaian per Elemen" />
                <Tab label="Rasional" />
                <Tab label="Tujuan" />
                <Tab label="Karakteristik" />
              </Tabs>
            </Box>

            {/* Capaian per Elemen */}
            <CustomTabPanel value={tabValue} index={0}>
              {loading ? (
                <Box className="flex flex-col gap-4 py-4">
                  <Skeleton height={40} />
                  <Skeleton height={60} />
                  <Skeleton height={60} />
                </Box>
              ) : data?.details && data.details.length > 0 ? (
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell
                          className="bg-slate-50 font-bold"
                          width="200"
                          sortDirection={sortBy === "element.element_name" ? sortDir : false}
                        >
                          <TableSortLabel
                            active={sortBy === "element.element_name"}
                            direction={sortBy === "element.element_name" ? sortDir : "asc"}
                            onClick={() => handleSort("element.element_name")}
                          >
                            Elemen
                          </TableSortLabel>
                        </TableCell>
                        <TableCell
                          className="bg-slate-50 font-bold"
                          sortDirection={sortBy === "detail_text" ? sortDir : false}
                        >
                          <TableSortLabel
                            active={sortBy === "detail_text"}
                            direction={sortBy === "detail_text" ? sortDir : "asc"}
                            onClick={() => handleSort("detail_text")}
                          >
                            Deskripsi Capaian Pembelajaran
                          </TableSortLabel>
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {paginatedData.map((c) => (
                        <TableRow key={c.id}>
                          <TableCell className="align-top font-medium">{c.element?.element_name}</TableCell>
                          <TableCell className="align-top">
                            <div
                              className="ds-markdown text-text-secondary leading-relaxed"
                              dangerouslySetInnerHTML={{ __html: c.detail_text || "-" }}
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <TablePagination
                    component="div"
                    count={total}
                    page={page - 1}
                    onPageChange={(_, newPage) => handlePageChange(newPage + 1)}
                    rowsPerPage={limit}
                    onRowsPerPageChange={(e) => handleLimitChange(parseInt(e.target.value, 10))}
                    labelRowsPerPage="Baris per halaman:"
                  />
                </TableContainer>
              ) : (
                <Typography variant="body2" color="text.secondary" className="py-4 text-center italic">
                  Belum ada detail capaian per elemen.
                </Typography>
              )}
            </CustomTabPanel>

            {/* Rasional */}
            <CustomTabPanel value={tabValue} index={1}>
              {loading ? (
                <Box className="flex flex-col gap-3 py-4">
                  <Skeleton height={20} />
                  <Skeleton height={20} />
                  <Skeleton height={20} width="80%" />
                </Box>
              ) : (
                <div
                  className="ds-markdown text-text-secondary leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: data?.subject?.rational || "Tidak ada data rasional." }}
                />
              )}
            </CustomTabPanel>

            {/* Tujuan */}
            <CustomTabPanel value={tabValue} index={2}>
              {loading ? (
                <Box className="flex flex-col gap-3 py-4">
                  <Skeleton height={20} />
                  <Skeleton height={20} />
                  <Skeleton height={20} width="80%" />
                </Box>
              ) : (
                <div
                  className="ds-markdown text-text-secondary leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: data?.subject?.goals || "Tidak ada data tujuan." }}
                />
              )}
            </CustomTabPanel>

            {/* Karakteristik */}
            <CustomTabPanel value={tabValue} index={3}>
              {loading ? (
                <Box className="flex flex-col gap-3 py-4">
                  <Skeleton height={20} />
                  <Skeleton height={20} />
                  <Skeleton height={20} width="80%" />
                </Box>
              ) : (
                <div
                  className="ds-markdown text-text-secondary leading-relaxed"
                  dangerouslySetInnerHTML={{
                    __html: data?.subject?.characteristics || "Tidak ada data karakteristik.",
                  }}
                />
              )}
            </CustomTabPanel>
          </Card>
        </Grid>
      )}
    </Box>
  );
}
