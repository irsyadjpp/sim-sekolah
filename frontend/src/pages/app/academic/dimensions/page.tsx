import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Box,
  Breadcrumbs,
  Card,
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

interface ProfileDimension {
  id: string;
  dimension_code: string;
  dimension_name: string;
  description: string;
  is_active: boolean;
}

export default function Page() {
  const [data, setData] = useState<ProfileDimension[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/profile-dimensions`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success") {
          setData(json.data || []);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "dimensions", data, defaultLimit: 10 });

  return (
    <Box>
      <Typography variant="h1" component="h1" className="text-primary mb-2 font-bold">
        Dimensi Profil Lulusan
      </Typography>
      <Breadcrumbs className="mb-6">
        <Link to="/home" className="hover:underline">
          Beranda
        </Link>
        <Link to="/academic" className="hover:underline">
          Akademik
        </Link>
        <Typography variant="body2" color="text.secondary">
          Dimensi Profil
        </Typography>
      </Breadcrumbs>

      <TableContainer component={Card} elevation={0} className="border-divider overflow-hidden rounded-xl border">
        <Table>
          <TableHead className="bg-slate-50">
            <TableRow>
              <TableCell
                className="py-4 font-bold"
                width="120"
                sortDirection={sortBy === "dimension_code" ? sortDir : false}
              >
                <TableSortLabel
                  active={sortBy === "dimension_code"}
                  direction={sortBy === "dimension_code" ? sortDir : "asc"}
                  onClick={() => handleSort("dimension_code")}
                >
                  Kode
                </TableSortLabel>
              </TableCell>
              <TableCell className="py-4 font-bold" sortDirection={sortBy === "dimension_name" ? sortDir : false}>
                <TableSortLabel
                  active={sortBy === "dimension_name"}
                  direction={sortBy === "dimension_name" ? sortDir : "asc"}
                  onClick={() => handleSort("dimension_name")}
                >
                  Nama Dimensi
                </TableSortLabel>
              </TableCell>
              <TableCell className="py-4 font-bold">Deskripsi</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-20">
                  <CircularProgress size={32} thickness={4} />
                  <Typography variant="body2" className="mt-4 text-slate-500">
                    Memuat data dimensi...
                  </Typography>
                </TableCell>
              </TableRow>
            ) : paginatedData.length > 0 ? (
              paginatedData.map((d) => (
                <TableRow key={d.id} hover>
                  <TableCell className="text-primary font-bold">{d.dimension_code}</TableCell>
                  <TableCell className="font-medium text-slate-800">{d.dimension_name}</TableCell>
                  <TableCell className="text-sm text-slate-600 italic">
                    {d.description || "Belum ada deskripsi."}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} align="center" className="py-20">
                  <Typography variant="body1" className="text-slate-400">
                    Tidak ada data dimensi profil.
                  </Typography>
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
