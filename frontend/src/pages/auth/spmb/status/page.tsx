/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

import {
  ArrowBack as BackIcon,
  Cancel as ErrorIcon,
  CheckCircle as ValidIcon,
  CloudUpload as UploadIcon,
  HelpOutline as PendingIcon,
  Search as SearchIcon,
} from "@mui/icons-material";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import Logo from "@/components/logo/logo";
import { DEFAULTS } from "@/config";
import { spmbStatusLabel } from "@/i18n/spmb-status";

export default function SPMBStatusPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [nik, setNik] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [applicant, setApplicant] = useState<any | null>(null);
  const [uploadMsg, setUploadMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  const handleSearch = async () => {
    if (!nik || nik.length < 16) {
      setError(t("spmb.status-page.nik-invalid"));
      return;
    }
    setLoading(true);
    setError(null);
    setUploadMsg(null);
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/check-status?nik=${nik}`);
      const json = await res.json();
      if (json.status === "success" && json.data) {
        setApplicant(json.data);
      } else {
        setApplicant(null);
        setError(json.message || t("spmb.status-page.check-not-found"));
      }
    } catch (err) {
      setError(t("spmb.status-page.check-server-error"));
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (docType: string, file: File) => {
    if (!applicant) return;
    setUploadMsg(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("document_type", docType);

    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/applicants/${applicant.id}/documents`, {
        method: "POST",
        body: formData,
      });

      const json = await res.json();
      if (json.status === "success") {
        setUploadMsg({ type: "success", text: t("spmb.status-page.upload-success", { type: docType }) });
        // Refresh applicant data
        const refreshRes = await fetch(`${DEFAULTS.API_URL}/api/v1/spmb/check-status?nik=${nik}`);
        const refreshJson = await refreshRes.json();
        if (refreshJson.status === "success") {
          setApplicant(refreshJson.data);
        }
      } else {
        setUploadMsg({ type: "error", text: json.message || t("spmb.status-page.upload-error") });
      }
    } catch (err) {
      setUploadMsg({ type: "error", text: t("spmb.status-page.upload-connection-error") });
    }
  };

  const getStatusChip = (status: string) => {
    const label = spmbStatusLabel(status);
    const color =
      status === "Submitted"
        ? "warning"
        : status === "Verified"
          ? "info"
          : status === "Accepted"
            ? "success"
            : status === "Rejected"
              ? "error"
              : "default";
    return <Chip label={label} color={color} className="rounded-xl font-bold" />;
  };

  const getDocumentTypes = () => {
    const list = [
      { code: "KK", label: t("spmb.status-page.doc-kk"), desc: t("spmb.status-page.doc-kk-desc") },
      { code: "AKTA", label: t("spmb.status-page.doc-akta"), desc: t("spmb.status-page.doc-akta-desc") },
    ];

    if (applicant) {
      if (applicant.birth_date) {
        const birth = new Date(applicant.birth_date);
        const currentYear = new Date().getFullYear();
        const targetDate = new Date(currentYear, 6, 1);
        const ageDiffMs = targetDate.getTime() - birth.getTime();
        const ageDate = new Date(ageDiffMs);
        const ageYears = Math.abs(ageDate.getUTCFullYear() - 1970);
        const ageMonths = ageYears * 12 + ageDate.getUTCMonth();

        if (ageMonths >= 66 && ageMonths < 72) {
          list.push({
            code: "REKOMENDASI_PSIKOLOG",
            label: "Surat Rekomendasi Psikolog / Dewan Guru",
            desc: t("spmb.status-page.age-requirement"),
          });
        }
      }

      if (applicant.admission_path?.name === "Afirmasi") {
        list.push({
          code: "KARTU_AFIRMASI",
          label: "Kartu Penanganan Kemiskinan / Disabilitas",
          desc: "Scan Kartu KIP / PKH / KKS / Kartu Disabilitas resmi (SKTM / KIS Ditolak)",
        });
      } else {
        list.push({
          code: "IJAZAH",
          label: "Ijazah / SKL",
          desc: "Scan Ijazah atau Surat Keterangan Lulus TK/PAUD (jika ada)",
        });
      }
    } else {
      list.push({
        code: "IJAZAH",
        label: "Ijazah / SKL",
        desc: "Scan Ijazah atau Surat Keterangan Lulus TK/PAUD (jika ada)",
      });
    }

    return list;
  };

  const getDocStatus = (code: string) => {
    if (!applicant?.documents) return { uploaded: false, path: "" };
    const doc = applicant.documents.find((d: any) => d.document_type === code);
    return doc ? { uploaded: true, path: doc.file_path } : { uploaded: false, path: "" };
  };

  return (
    <Box className="bg-waves flex min-h-screen w-full items-center justify-center bg-cover bg-center p-4">
      <Paper elevation={3} className="bg-background-paper shadow-darker-xs w-3xl max-w-full rounded-[40px] py-10">
        <Box className="flex flex-col gap-6 px-8 sm:px-14">
          <Box className="flex items-center justify-between">
            <Logo classNameMobile="hidden" />
            <Button
              variant="text"
              color="primary"
              onClick={() => navigate("/auth/sign-in")}
              startIcon={<BackIcon />}
              className="font-bold"
            >
              Kembali ke Login
            </Button>
          </Box>

          <Box className="flex flex-col">
            <Typography variant="h1" className="mb-1">
              Status Pendaftaran & Berkas
            </Typography>
            <Typography variant="body1" className="text-text-secondary">
              Periksa status kelulusan seleksi dan lengkapi berkas persyaratan administrasi Anda.
            </Typography>
          </Box>

          <Card className="rounded-3xl border border-slate-100 bg-slate-50/50 p-4 shadow-sm">
            <Box className="flex items-center gap-4">
              <TextField
                fullWidth
                label="Masukkan 16 Digit NIK Calon Murid"
                placeholder="Contoh: 7306xxxxxxxxxxxx"
                value={nik}
                onChange={(e) => setNik(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              />
              <Button
                variant="contained"
                onClick={handleSearch}
                disabled={loading}
                startIcon={<SearchIcon />}
                className="rounded-2xl px-6 py-4 font-black shadow-xl"
              >
                Cari
              </Button>
            </Box>
          </Card>

          {error && (
            <Alert severity="error" className="rounded-2xl font-semibold">
              {error}
            </Alert>
          )}

          {applicant && (
            <Box className="animate-fade-in flex flex-col gap-6">
              <Card className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
                <Typography variant="h5" className="text-primary mb-4 font-black">
                  Hasil Pencarian
                </Typography>
                <Grid container spacing={3}>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="body2" className="font-bold text-slate-400">
                      NAMA LENGKAP
                    </Typography>
                    <Typography variant="body1" className="font-black text-slate-800">
                      {applicant.full_name}
                    </Typography>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="body2" className="font-bold text-slate-400">
                      JALUR SELEKSI
                    </Typography>
                    <Typography variant="body1" className="font-bold text-slate-800">
                      {applicant.admission_path?.name}
                    </Typography>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="body2" className="font-bold text-slate-400">
                      NIK
                    </Typography>
                    <Typography variant="body1" className="font-mono text-slate-800">
                      {applicant.nik}
                    </Typography>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="body2" className="font-bold text-slate-400">
                      STATUS PENDAFTARAN
                    </Typography>
                    <Box className="mt-1">{getStatusChip(applicant.status)}</Box>
                  </Grid>
                </Grid>
              </Card>

              {applicant.status === "Accepted" && (
                <Alert severity="success" className="rounded-2xl font-bold">
                  Selamat! Calon murid telah dinyatakan DITERIMA di UPT SDI Bonerate No. 85. Data murid aktif telah
                  di-generate otomatis oleh sistem.
                </Alert>
              )}

              <Card className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
                <Typography variant="h5" className="text-primary mb-2 font-black">
                  Dokumen Persyaratan
                </Typography>
                <Typography variant="body2" className="text-text-secondary mb-4">
                  Unggah berkas asli dalam bentuk scan/foto berkualitas tinggi.
                </Typography>

                {uploadMsg && (
                  <Alert severity={uploadMsg.type} className="mb-4 rounded-xl font-semibold">
                    {uploadMsg.text}
                  </Alert>
                )}

                <Box className="flex flex-col gap-4">
                  {getDocumentTypes().map((doc) => {
                    const status = getDocStatus(doc.code);
                    return (
                      <Paper
                        key={doc.code}
                        className="flex items-center justify-between rounded-2xl border border-slate-100 p-4"
                      >
                        <Box className="flex items-center gap-4">
                          {status.uploaded ? <ValidIcon color="success" /> : <PendingIcon className="text-slate-300" />}
                          <Box>
                            <Typography variant="body1" className="font-bold text-slate-800">
                              {doc.label}
                            </Typography>
                            <Typography variant="caption" className="text-slate-400">
                              {doc.desc}
                            </Typography>
                          </Box>
                        </Box>

                        <Box>
                          {status.uploaded ? (
                            <Box className="flex items-center gap-2">
                              <Button
                                size="small"
                                variant="text"
                                color="primary"
                                href={`${DEFAULTS.API_URL}${status.path}`}
                                target="_blank"
                                className="font-bold"
                              >
                                Lihat Berkas
                              </Button>
                              <Button
                                component="label"
                                size="small"
                                variant="outlined"
                                color="grey"
                                className="rounded-xl font-bold"
                              >
                                Ganti
                                <input
                                  type="file"
                                  hidden
                                  accept="image/*,application/pdf"
                                  onChange={(e) => e.target.files?.[0] && handleFileUpload(doc.code, e.target.files[0])}
                                />
                              </Button>
                            </Box>
                          ) : (
                            <Button
                              component="label"
                              variant="contained"
                              color="primary"
                              startIcon={<UploadIcon />}
                              className="rounded-xl px-4 py-2 font-bold"
                            >
                              Unggah
                              <input
                                type="file"
                                hidden
                                accept="image/*,application/pdf"
                                onChange={(e) => e.target.files?.[0] && handleFileUpload(doc.code, e.target.files[0])}
                              />
                            </Button>
                          )}
                        </Box>
                      </Paper>
                    );
                  })}
                </Box>
              </Card>
            </Box>
          )}
        </Box>
      </Paper>
    </Box>
  );
}
