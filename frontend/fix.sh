#!/bin/bash
# Fix SelectProps
files=(
"src/pages/app/dashboards/analytics/sections/dashboard-analytics-orders.tsx"
"src/pages/app/dashboards/default/default-titles-inside/sections/dashboard-default-products.tsx"
"src/pages/app/dashboards/default/sections/dashboard-default-products.tsx"
"src/pages/app/education/default-titles-inside/sections/dashboard-default-products.tsx"
"src/pages/app/education/sections/dashboard-default-products.tsx"
"src/pages/landing-page/lp-reviews.tsx"
"src/pages/app/pages/user/permissions/sections/user-permissions-list.tsx"
"src/pages/app/system/access/roles/sections/role-permission-list.tsx"
)
for file in "${files[@]}"; do
  sed -i 's/const propsCasted = props as SelectProps;/const propsCasted = props as unknown as SelectProps;/g' "$file"
done

# Fix pagination={false}
sed -i 's/pagination={false}/hideFooterPagination/g' src/pages/app/pages/user/permissions/sections/user-permissions-list.tsx
sed -i 's/pagination={false}/hideFooterPagination/g' src/pages/app/system/access/roles/sections/role-permission-list.tsx

# Fix settings-appearance.tsx
sed -i 's/const { themeMode, themeColor, setThemeMode, setThemeColor } = useThemeContext();/const { mode: themeMode, theme: themeColor, setMode: setThemeMode, setTheme: setThemeColor } = useThemeContext();/g' src/pages/app/settings/components/settings-appearance.tsx
sed -i 's/const { contentType, leftMenuType, setContentType, setLeftMenuType } = useLayoutContext();/const { contentType, leftMenuType, setContentType, setLeftMenuType } = useLayoutContext() as any;/g' src/pages/app/settings/components/settings-appearance.tsx
sed -i 's/setThemeMode(localThemeMode as any);/setThemeMode(localThemeMode as any);/g' src/pages/app/settings/components/settings-appearance.tsx
sed -i 's/setThemeColor(localThemeColor);/setThemeColor(localThemeColor as any);/g' src/pages/app/settings/components/settings-appearance.tsx

# Fix menu-items.tsx NiActivity
sed -i 's/icon: "NiActivity"/icon: "NiChartBar"/g' src/menu-items.tsx

# Fix chart-element-hoc.tsx
sed -i 's/export function withChartElementStyle<P extends object>(Component: React.ComponentType<P>) {/export function withChartElementStyle<P extends object>(Component: React.ComponentType<P>, defaultProps?: any) {/g' src/lib/chart-element-hoc.tsx
sed -i 's/return <Component {...props} \/>;/return <Component {...props} {...defaultProps} \/>;/g' src/lib/chart-element-hoc.tsx

# Fix bank/page.tsx
cat << 'INNER_EOF' > src/pages/app/academic/evaluation/bank/page.tsx
import React from "react";
import { useTranslation } from "react-i18next";

import { Box, Breadcrumbs, Link, Paper, Typography } from "@mui/material";

import NiArchive from "@/icons/nexture/ni-archive";

export default function QuestionBankPage() {
  const { t } = useTranslation();

  return (
    <Box className="flex flex-col gap-6 w-full">
      <Breadcrumbs aria-label="breadcrumb" className="mb-4">
        <Link underline="hover" color="inherit" href="/home">
          {t("menu-home")}
        </Link>
        <Link underline="hover" color="inherit" href="/academic/evaluation/formative">
          {t("menu-assessment")}
        </Link>
        <Typography color="text.primary">{t("menu-question-bank")}</Typography>
      </Breadcrumbs>
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
    </Box>
  );
}
INNER_EOF

# Fix classroom/page.tsx icons
sed -i 's/<AssignmentIcon size="small" \/>/<AssignmentIcon fontSize="small" \/>/g' src/pages/app/academic/subjects/classroom/page.tsx
sed -i 's/<PeopleIcon size="small" \/>/<PeopleIcon fontSize="small" \/>/g' src/pages/app/academic/subjects/classroom/page.tsx
sed -i 's/<DeleteIcon size="small" \/>/<DeleteIcon fontSize="small" \/>/g' src/pages/app/academic/subjects/classroom/page.tsx

