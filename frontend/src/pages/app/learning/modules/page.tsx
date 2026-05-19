/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CircularProgress,
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
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiFlash from "@/icons/nexture/ni-flash";
import NiPlus from "@/icons/nexture/ni-plus";

interface TeachingModule {
  id: string;
  atp_id: string;
  title: string;
  status: string;
}

export default function TeachingModulesPage() {
  const navigate = useNavigate();
  const [data, setData] = useState<TeachingModule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      // For now, listing all modules. In a real app, this would be filtered by user context.
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning/modules`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setData(json.data || []);
      } else {
        // If 404/not implemented yet, just show empty
        setData([]);
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

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "learning_modules", data, defaultLimit: 10 });

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Modul Ajar (RPP)
        </Typography>
        <Button
          variant="contained"
          startIcon={<NiPlus size="small" />}
          onClick={() => navigate("/academic/curriculum/flow")}
        >
          Buat dari ATP
        </Button>
      </Box>

      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Modul Ajar</Typography>
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
              <TableCell className="font-bold" sortDirection={sortBy === "title" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "title"}
                  direction={sortBy === "title" ? sortDir : "asc"}
                  onClick={() => handleSort("title")}
                >
                  Judul Modul
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" sortDirection={sortBy === "status" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "status"}
                  direction={sortBy === "status" ? sortDir : "asc"}
                  onClick={() => handleSort("status")}
                >
                  Status
                </TableSortLabel>
              </TableCell>
              <TableCell className="font-bold" align="center">
                Aksi
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((item) => (
                <TableRow key={item.id} hover>
                  <TableCell>
                    <Typography className="font-medium">{item.title}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{item.status}</Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<NiEyeOpen size="small" />}
                      onClick={() => navigate(`/learning/modules/details?id=${item.id}`)}
                    >
                      Buka
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-20 text-gray-500">
                  <Box className="flex flex-col items-center gap-4">
                    <Typography>Belum ada modul ajar yang dibuat.</Typography>
                    <Button
                      variant="contained"
                      color="secondary"
                      startIcon={<NiFlash size="small" />}
                      onClick={() => navigate("/academic/curriculum/flow")}
                    >
                      Generate dari ATP dengan AI
                    </Button>
                  </Box>
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
    </Box>
  );
}
