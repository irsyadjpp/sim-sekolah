import React from "react";
import { useTranslation } from "react-i18next";

import { Box, Breadcrumbs, Link, Paper, Typography } from "@mui/material";

import ListingPageContent from "@/components/layout/listing-page-content";
import NiArchive from "@/icons/nexture/ni-archive";

export default function QuestionBankPage() {
  const { t } = useTranslation();

  return (
    <ListingPageContent
      title={t("menu-question-bank")}
      breadcrumb={
        <Breadcrumbs aria-label="breadcrumb">
          <Link underline="hover" color="inherit" href="/home">
            {t("menu-home")}
          </Link>
          <Link underline="hover" color="inherit" href="/academic/evaluation/formative">
            {t("menu-assessment")}
          </Link>
          <Typography color="text.primary">{t("menu-question-bank")}</Typography>
        </Breadcrumbs>
      }
    >
      <Box className="flex flex-col gap-6">
        <Paper
          elevation={0}
          className="flex flex-col items-center justify-center rounded-4xl border-2 border-dashed border-slate-200 bg-slate-50/50 p-12"
        >
          <Box className="bg-primary/10 mb-6 flex h-20 w-20 items-center justify-center rounded-full">
            <NiArchive size={40} className="text-primary" />
          </Box>
          <Typography variant="h4" className="mb-2 font-bold text-slate-800">
            {t("menu-question-bank")}
          </Typography>
          <Typography variant="body1" className="max-w-md text-center text-slate-500">
            Fitur Manajemen Soal (LOTS/HOTS) sedang dalam pengembangan. Halaman ini akan menjadi pusat bank soal untuk
            mendukung asesmen sekolah.
          </Typography>
        </Paper>
      </Box>
    </ListingPageContent>
  );
}
