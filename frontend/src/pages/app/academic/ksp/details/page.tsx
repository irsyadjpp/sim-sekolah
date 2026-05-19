/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useSearchParams } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Paper,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useConfirm } from "@/hooks/use-confirm";
import NiBook from "@/icons/nexture/ni-book";
import NiCheckFull from "@/icons/nexture/ni-check-full";
import NiChevronRight from "@/icons/nexture/ni-chevron-right";
import NiSparkle from "@/icons/nexture/ni-sparkle";

interface Chapter {
  id: string;
  chapter_number: number;
  title: string;
  content: string;
}

interface KspDetail {
  id: string;
  academic_year: { year_name: string; semester: string };
  status: string;
  chapters: Chapter[];
}

export default function KspDetailsPage() {
  const confirm = useConfirm();
  const { t } = useTranslation();
  const [searchParams] = useSearchParams();
  const kspId = searchParams.get("id");

  const [data, setData] = useState<KspDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeChapter, setActiveChapter] = useState<number>(1);
  const [generating, setGenerating] = useState(false);

  const fetchData = async () => {
    if (!kspId) return;
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/curriculum-documents/${kspId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setData(json.data);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [kspId]);

  const handleGenerateChapter = async (num: number) => {
    setGenerating(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/curriculum-documents/chapters/trigger`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          curriculum_document_id: kspId,
          chapter_number: num,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        alert("Formulasi draf Bab " + num + " telah masuk antrean AI.");
        fetchData();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleFinalize = async () => {
    const ok = await confirm({
      title: "Finalisasi KSP",
      message: "Finalisasi akan membekukan dokumen dan mengarsipkannya ke RAG. Lanjutkan?",
      confirmText: "Finalisasi",
      cancelText: "Batal",
    });
    if (!ok) return;
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/curriculum-documents/${kspId}/finalize`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        alert(t("ksp-builder.final-success"));
        fetchData();
      } else {
        alert(json.message);
      }
    } catch (err: any) {
      alert(err.message);
    }
  };

  const currentChapter = data?.chapters.find((c) => c.chapter_number === activeChapter);
  const semesters = { 1: "Ganjil", 2: "Genap" };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Box>
          <Typography variant="h1" component="h1" className="mb-0 text-3xl font-bold">
            {loading ? "Memuat Dokumen..." : `KSP ${data?.academic_year.year_name} (${data?.academic_year.semester})`}
          </Typography>
          {!loading && data && (
            <Box className="mt-1 flex items-center gap-2">
              <Chip label={data.status} size="small" color={data.status === "FINAL" ? "success" : "default"} />
              <Typography variant="caption" color="textSecondary">
                ID: {data.id}
              </Typography>
            </Box>
          )}
        </Box>
        {!loading && data && data.status !== "FINAL" && (
          <Button variant="contained" color="success" startIcon={<NiCheckFull />} onClick={handleFinalize}>
            {t("ksp-builder.finalize")}
          </Button>
        )}
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">{t("ksp-builder.breadcrumb-home")}</Link>
        <Link to="/academic">{t("ksp-builder.breadcrumb-academic")}</Link>
        <Link to="/academic/ksp">{t("ksp-builder.breadcrumb-ksp")}</Link>
        <Typography variant="body2">Dokumen Detail</Typography>
      </Breadcrumbs>

      {loading ? (
        <Box className="flex h-64 items-center justify-center">
          <CircularProgress />
        </Box>
      ) : error || !data ? (
        <Alert severity="error">{error || "Data tidak ditemukan"}</Alert>
      ) : (
        <Grid container spacing={4}>
          {/* Sidebar Bab */}
          <Grid size={{ xs: 12, md: 3 }}>
            <Paper className="border-divider overflow-hidden rounded-2xl border shadow-none">
              <List component="nav" className="p-0">
                {[1, 2, 3, 4, 5].map((num) => {
                  const chapter = data.chapters.find((c) => c.chapter_number === num);
                  const isActive = activeChapter === num;
                  return (
                    <ListItemButton
                      key={num}
                      selected={isActive}
                      onClick={() => setActiveChapter(num)}
                      className={`border-divider border-b px-6 py-4 last:border-b-0 ${
                        isActive ? "bg-primary/5 text-primary" : ""
                      }`}
                    >
                      <ListItemIcon className={isActive ? "text-primary" : "text-slate-400"}>
                        <NiBook size="small" />
                      </ListItemIcon>
                      <ListItemText
                        primary={`Bab ${num}`}
                        secondary={chapter ? chapter.title : "Belum diisi"}
                        primaryTypographyProps={{ variant: "body2", className: "font-bold" }}
                        secondaryTypographyProps={{ variant: "caption", className: "truncate block w-40" }}
                      />
                      {chapter && <NiCheckFull size="small" className="text-success" />}
                      {!chapter && <NiChevronRight size="small" />}
                    </ListItemButton>
                  );
                })}
              </List>
            </Paper>
          </Grid>

          {/* Konten Bab */}
          <Grid size={{ xs: 12, md: 9 }}>
            <Card className="border-divider min-h-[500px] rounded-2xl border shadow-sm">
              <CardContent className="p-8">
                {currentChapter ? (
                  <Box>
                    <Box className="mb-6 flex items-center justify-between">
                      <Typography variant="h4" className="font-bold">
                        Bab {currentChapter.chapter_number}: {currentChapter.title}
                      </Typography>
                      {data.status !== "FINAL" && (
                        <Button
                          variant="outlined"
                          startIcon={<NiSparkle size="small" />}
                          onClick={() => handleGenerateChapter(activeChapter)}
                          disabled={generating}
                        >
                          {generating ? "Menyusun..." : "Regenerasi AI"}
                        </Button>
                      )}
                    </Box>
                    <Divider className="mb-6" />
                    {generating ? (
                      <Box className="py-20 text-center">
                        <CircularProgress className="mb-4" />
                        <Typography color="textSecondary">{t("ksp-builder.ai-orchestration")}</Typography>
                      </Box>
                    ) : (
                      <Box
                        className="prose prose-slate max-w-none"
                        dangerouslySetInnerHTML={{ __html: currentChapter.content }}
                      />
                    )}
                  </Box>
                ) : (
                  <Box className="py-20 text-center">
                    <Typography variant="h5" className="mb-4 font-bold text-slate-400">
                      Bab {activeChapter} Belum Tersedia
                    </Typography>
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<NiSparkle />}
                      onClick={() => handleGenerateChapter(activeChapter)}
                      disabled={generating}
                    >
                      {generating ? "Menyusun..." : t("ksp-builder.generate-ai")}
                    </Button>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}
