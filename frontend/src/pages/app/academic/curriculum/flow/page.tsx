import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  IconButton,
  Skeleton,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import { useConfirm } from "@/hooks/use-confirm";
import NiBinEmpty from "@/icons/nexture/ni-bin-empty";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPlus from "@/icons/nexture/ni-plus";

interface ATP {
  id: string;
  classroom_id: string;
  subject_id: string;
  subject?: { subject_name: string };
  classroom?: { name: string };
}

export default function ATPListPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const confirm = useConfirm();

  const [data, setData] = useState<ATP[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: "success" | "error" }>({
    open: false,
    message: "",
    severity: "success",
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning/atp?limit=10000`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setData(json.data || []);
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
  }, []);

  const handleDelete = async (id: string) => {
    const isConfirmed = await confirm({
      title: t("atp-builder.confirm-delete-title"),
      message: t("atp-builder.confirm-delete-desc"),
      confirmText: t("atp-builder.confirm-btn-delete"),
      cancelText: t("atp-builder.confirm-btn-cancel"),
    });

    if (!isConfirmed) return;

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning/atp/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();

      if (json.status === "success") {
        // Optimistic UI Update
        setData((prev) => prev.filter((item) => item.id !== id));
        setSnackbar({ open: true, message: t("atp-builder.delete-success"), severity: "success" });
      } else {
        setSnackbar({ open: true, message: json.message, severity: "error" });
      }
    } catch (err: any) {
      setSnackbar({ open: true, message: err.message, severity: "error" });
    }
  };

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "curriculum_flow", data, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("atp-builder.title")}
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => navigate("/academic/curriculum/flow/create")}
        >
          {t("atp-builder.create-flow")}
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">{t("atp-builder.breadcrumb-home")}</Link>
        <Link to="/academic">{t("atp-builder.breadcrumb-academic")}</Link>
        <Typography variant="body2">{t("atp-builder.breadcrumb-atp")}</Typography>
      </Breadcrumbs>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold" sortDirection={sortBy === "subject.subject_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "subject.subject_name"}
                  direction={sortBy === "subject.subject_name" ? sortDir : "asc"}
                  onClick={() => handleSort("subject.subject_name")}
                >
                  {t("atp-builder.subject")}
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "classroom.name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "classroom.name"}
                  direction={sortBy === "classroom.name" ? sortDir : "asc"}
                  onClick={() => handleSort("classroom.name")}
                >
                  {t("atp-builder.classroom")}
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" align="center">
                Aksi
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              Array.from(new Array(3)).map((_, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <Skeleton width="60%" />
                  </TableCell>
                  <TableCell>
                    <Skeleton width="40%" />
                  </TableCell>
                  <TableCell align="center">
                    <Skeleton width={80} height={40} className="inline-block" />
                    <Skeleton width={40} height={40} className="ml-2 inline-block" />
                  </TableCell>
                </TableRow>
              ))
            ) : paginatedData.length > 0 ? (
              paginatedData.map((item) => (
                <TableRow key={item.id} hover>
                  <TableCell>
                    <Typography className="font-medium">{item.subject?.subject_name || "Tanpa Nama"}</Typography>
                  </TableCell>
                  <TableCell>{item.classroom?.name || "Tanpa Kelas"}</TableCell>
                  <TableCell align="center">
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<NiEyeOpen size="small" />}
                      onClick={() => navigate(`/academic/curriculum/flow/details?id=${item.id}`)}
                      className="mr-2"
                    >
                      {t("atp-builder.manage-atp")}
                    </Button>
                    <IconButton size="small" color="error" onClick={() => handleDelete(item.id)}>
                      <NiBinEmpty size="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-10 text-gray-500 italic">
                  {t("atp-builder.no-data")}
                </TableCell>
              </TableRow>
            )}
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

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          variant="filled"
          sx={{ borderRadius: 2, fontWeight: 500 }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
