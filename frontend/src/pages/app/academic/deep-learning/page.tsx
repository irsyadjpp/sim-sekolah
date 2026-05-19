/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Box,
  Breadcrumbs,
  Card,
  CircularProgress,
  Grid,
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

interface DesignElement {
  id: string;
  design_element_name: string;
  description: string;
}

interface CognitiveStage {
  id: string;
  stage_order: number;
  stage_name: string;
  operational_verbs: string;
}

interface AssessmentLevel {
  id: string;
  level_code: string;
  description: string;
  pisa_level: string;
}

export default function Page() {
  const [tab, setTab] = useState(0);
  const [elemen, setElemen] = useState<DesignElement[]>([]);
  const [tahapan, setTahapan] = useState<CognitiveStage[]>([]);
  const [tingkat, setTingkat] = useState<AssessmentLevel[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        const headers = { Authorization: `Bearer ${token}` };

        const [resEd, resTk, resTa] = await Promise.all([
          fetch(`${DEFAULTS.API_URL}/api/v1/deep-learning/design-element`, { headers }),
          fetch(`${DEFAULTS.API_URL}/api/v1/deep-learning/cognitive-stage`, { headers }),
          fetch(`${DEFAULTS.API_URL}/api/v1/deep-learning/assessment-level`, { headers }),
        ]);

        const [jsonEd, jsonTk, jsonTa] = await Promise.all([resEd.json(), resTk.json(), resTa.json()]);

        if (jsonEd.status === "success") setElemen(jsonEd.data || []);
        if (jsonTk.status === "success") setTahapan(jsonTk.data || []);
        if (jsonTa.status === "success") setTingkat(jsonTa.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const {
    paginatedData: paginatedElemen,
    page: elemenPage,
    limit: elemenLimit,
    total: elemenTotal,
    handlePageChange: setElemenPage,
    handleLimitChange: setElemenLimit,
  } = useClientTable({ key: "deep_elemen", data: elemen, defaultLimit: 10 });

  const {
    paginatedData: paginatedTahapan,
    page: tahapanPage,
    limit: tahapanLimit,
    total: tahapanTotal,
    handlePageChange: setTahapanPage,
    handleLimitChange: setTahapanLimit,
  } = useClientTable({ key: "deep_tahapan", data: tahapan, defaultLimit: 10 });

  const {
    paginatedData: paginatedTingkat,
    page: tingkatPage,
    limit: tingkatLimit,
    total: tingkatTotal,
    handlePageChange: setTingkatPage,
    handleLimitChange: setTingkatLimit,
  } = useClientTable({ key: "deep_tingkat", data: tingkat, defaultLimit: 10 });

  return (
    <Box>
      <Typography variant="h1" component="h1" className="text-primary mb-2 font-bold">
        Referensi Deep Learning
      </Typography>
      <Breadcrumbs className="mb-6">
        <Link to="/home" className="hover:underline">
          Beranda
        </Link>
        <Link to="/academic" className="hover:underline">
          Akademik
        </Link>
        <Typography variant="body2" color="text.secondary">
          Ref Deep Learning
        </Typography>
      </Breadcrumbs>

      <Card elevation={0} className="border-divider mb-6 overflow-hidden rounded-xl border">
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          className="border-divider border-b bg-slate-50"
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label="Elemen Desain" className="py-4 font-bold" />
          <Tab label="Tahapan Kognitif" className="py-4 font-bold" />
          <Tab label="Tingkat Asesmen" className="py-4 font-bold" />
        </Tabs>

        <Box className="p-0">
          {loading ? (
            <Box className="flex flex-col items-center justify-center py-20">
              <CircularProgress size={32} thickness={4} />
              <Typography variant="body2" className="mt-4 text-slate-500">
                Memuat parameter deep learning...
              </Typography>
            </Box>
          ) : (
            <>
              {tab === 0 && (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell className="bg-slate-50/50 font-bold" width="250">
                          Nama Elemen
                        </TableCell>
                        <TableCell className="bg-slate-50/50 font-bold">Deskripsi / Panduan</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {paginatedElemen.map((e) => (
                        <TableRow key={e.id} hover>
                          <TableCell className="text-primary font-bold">{e.design_element_name}</TableCell>
                          <TableCell className="text-sm text-slate-600 italic">
                            {e.description || "Belum ada panduan."}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <TablePagination
                    component="div"
                    count={elemenTotal}
                    page={elemenPage - 1}
                    onPageChange={(_, newPage) => setElemenPage(newPage + 1)}
                    rowsPerPage={elemenLimit}
                    onRowsPerPageChange={(e) => setElemenLimit(parseInt(e.target.value, 10))}
                    labelRowsPerPage="Baris:"
                  />
                </TableContainer>
              )}

              {tab === 1 && (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell className="bg-slate-50/50 font-bold" width="80">
                          Urutan
                        </TableCell>
                        <TableCell className="bg-slate-50/50 font-bold" width="200">
                          Nama Tahapan
                        </TableCell>
                        <TableCell className="bg-slate-50/50 font-bold">Kata Kerja Operasional (KKO)</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {paginatedTahapan.map((t) => (
                        <TableRow key={t.id} hover>
                          <TableCell align="center">
                            <Box className="bg-primary flex h-8 w-8 items-center justify-center rounded-full font-bold text-white">
                              {t.stage_order}
                            </Box>
                          </TableCell>
                          <TableCell className="font-bold text-slate-800">{t.stage_name}</TableCell>
                          <TableCell className="text-sm text-slate-600">
                            {t.operational_verbs || "Belum ada referensi KKO."}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <TablePagination
                    component="div"
                    count={tahapanTotal}
                    page={tahapanPage - 1}
                    onPageChange={(_, newPage) => setTahapanPage(newPage + 1)}
                    rowsPerPage={tahapanLimit}
                    onRowsPerPageChange={(e) => setTahapanLimit(parseInt(e.target.value, 10))}
                    labelRowsPerPage="Baris:"
                  />
                </TableContainer>
              )}

              {tab === 2 && (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell className="bg-slate-50/50 font-bold" width="120">
                          Kode
                        </TableCell>
                        <TableCell className="bg-slate-50/50 font-bold">Keterangan</TableCell>
                        <TableCell className="bg-slate-50/50 font-bold" width="150">
                          Level PISA
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {paginatedTingkat.map((t) => (
                        <TableRow key={t.id} hover>
                          <TableCell>
                            <Box
                              className={`rounded px-3 py-1 text-center font-bold ${t.level_code === "HOTS" ? "bg-orange-100 text-orange-700" : "bg-blue-100 text-blue-700"}`}
                            >
                              {t.level_code}
                            </Box>
                          </TableCell>
                          <TableCell className="font-medium text-slate-800">{t.description}</TableCell>
                          <TableCell className="text-center font-mono text-xs text-slate-600">
                            {t.pisa_level || "-"}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <TablePagination
                    component="div"
                    count={tingkatTotal}
                    page={tingkatPage - 1}
                    onPageChange={(_, newPage) => setTingkatPage(newPage + 1)}
                    rowsPerPage={tingkatLimit}
                    onRowsPerPageChange={(e) => setTingkatLimit(parseInt(e.target.value, 10))}
                    labelRowsPerPage="Baris:"
                  />
                </TableContainer>
              )}
            </>
          )}
        </Box>
      </Card>
    </Box>
  );
}
