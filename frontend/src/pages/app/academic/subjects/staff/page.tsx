import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  FormControl,
  Grid,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import { useClientTable } from "@/hooks/use-client-table";
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiEyeOpen from "@/icons/nexture/ni-eye-open";
import NiPlus from "@/icons/nexture/ni-plus";
import NiSearch from "@/icons/nexture/ni-search";

export default function StaffListPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [staff, setStaff] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [filterGender, setFilterGender] = useState("Semua");
  const [filterStatus, setFilterStatus] = useState("Semua");

  useEffect(() => {
    const fetchStaff = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setError(t("common-errors.auth-error"));
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/teachers`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        if (json.status === "success") {
          setStaff(json.data || []);
        } else {
          setError(t("common-errors.fetch-error"));
        }
      } catch (err: any) {
        setError(t("common-errors.network-error"));
      } finally {
        setLoading(false);
      }
    };
    fetchStaff();
  }, []);

  const filteredData = useMemo(() => {
    return staff.filter((s) => {
      const matchSearch =
        (s.full_name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
        (s.nip || "").toLowerCase().includes(searchQuery.toLowerCase());
      const matchGender = filterGender === "Semua" || s.gender === filterGender;
      const matchStatus = filterStatus === "Semua" || s.employment_status === filterStatus;
      return matchSearch && matchGender && matchStatus;
    });
  }, [staff, searchQuery, filterGender, filterStatus]);

  const { paginatedData, page, limit, total, sortBy, sortDir, handlePageChange, handleLimitChange, handleSort } =
    useClientTable({ key: "staff", data: filteredData, defaultLimit: 10 });

  return (
    <Grid container spacing={4}>
      {/* Header */}
      <Grid size={{ xs: 12 }}>
        <Box className="mb-2 flex items-center justify-between">
          <Typography variant="h1" component="h1" className="mb-0">
            {t("staff-form.title")}
          </Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<NiPlus size="small" />}
            onClick={() => navigate("/academic/subjects/staff/create")}
          >
            {t("staff-form.breadcrumb-add")}
          </Button>
        </Box>
        <Breadcrumbs>
          <Link color="inherit" to="/home">
            Beranda
          </Link>
          <Link color="inherit" to="/academic">
            {t("staff-form.breadcrumb-academic")}
          </Link>
          <Link color="inherit" to="/academic/subjects">
            {t("staff-form.breadcrumb-subjects")}
          </Link>
          <Typography variant="body2">{t("staff-form.breadcrumb-staff")}</Typography>
        </Breadcrumbs>
        {error && (
          <Alert severity="error" className="mt-4 rounded-xl">
            {error}
          </Alert>
        )}
      </Grid>

      {/* Filters */}
      <Grid size={{ xs: 12 }}>
        <Card variant="outlined" className="border-divider bg-surface-standard rounded-2xl">
          <CardContent className="p-4">
            <Grid container spacing={3} alignItems="center">
              <Grid size={{ xs: 12, md: 4 }}>
                <TextField
                  fullWidth
                  placeholder="Cari nama atau NIP..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <NiSearch size="small" className="text-text-secondary" />
                      </InputAdornment>
                    ),
                  }}
                  size="small"
                />
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <FormControl fullWidth size="small">
                  <InputLabel id="filter-gender-label">Jenis Kelamin</InputLabel>
                  <Select
                    labelId="filter-gender-label"
                    value={filterGender}
                    label="Jenis Kelamin"
                    onChange={(e) => setFilterGender(e.target.value)}
                    IconComponent={NiChevronDownSmall}
                  >
                    <MenuItem value="Semua">Semua Jenis Kelamin</MenuItem>
                    <MenuItem value="L">Laki-laki</MenuItem>
                    <MenuItem value="P">Perempuan</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <FormControl fullWidth size="small">
                  <InputLabel id="filter-status-label">Status</InputLabel>
                  <Select
                    labelId="filter-status-label"
                    value={filterStatus}
                    label="Status"
                    onChange={(e) => setFilterStatus(e.target.value)}
                    IconComponent={NiChevronDownSmall}
                  >
                    <MenuItem value="Semua">Semua Status</MenuItem>
                    <MenuItem value="PNS">PNS</MenuItem>
                    <MenuItem value="PPPK">PPPK</MenuItem>
                    <MenuItem value="Honorer">Honorer</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>

      {/* Content - Table View */}
      <Grid size={{ xs: 12 }}>
        <Card variant="outlined" className="border-divider overflow-hidden rounded-2xl">
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow className="bg-action-hover">
                  <TableCell
                    className="py-4 pl-6 font-semibold"
                    sortDirection={sortBy === "full_name" ? sortDir : false}
                  >
                    <TableSortLabel
                      active={sortBy === "full_name"}
                      direction={sortBy === "full_name" ? sortDir : "asc"}
                      onClick={() => handleSort("full_name")}
                    >
                      {t("staff-form.label-full-name")}
                    </TableSortLabel>
                  </TableCell>
                  <TableCell className="py-4 font-semibold" sortDirection={sortBy === "nip" ? sortDir : false}>
                    <TableSortLabel
                      active={sortBy === "nip"}
                      direction={sortBy === "nip" ? sortDir : "asc"}
                      onClick={() => handleSort("nip")}
                    >
                      {t("staff-form.label-nip")}
                    </TableSortLabel>
                  </TableCell>
                  <TableCell className="py-4 font-semibold">{t("staff-form.label-teaching-subject")}</TableCell>
                  <TableCell
                    className="py-4 font-semibold"
                    sortDirection={sortBy === "employment_status" ? sortDir : false}
                  >
                    <TableSortLabel
                      active={sortBy === "employment_status"}
                      direction={sortBy === "employment_status" ? sortDir : "asc"}
                      onClick={() => handleSort("employment_status")}
                    >
                      Status
                    </TableSortLabel>
                  </TableCell>
                  <TableCell className="py-4 font-semibold" align="center">
                    Aksi
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center" className="py-20">
                      <CircularProgress size={30} />
                    </TableCell>
                  </TableRow>
                ) : paginatedData.length > 0 ? (
                  paginatedData.map((row) => (
                    <TableRow key={row.id} hover>
                      <TableCell className="pl-6 font-medium">
                        {row.full_name}
                        <Typography variant="caption" display="block" color="text.secondary">
                          {row.gender === "L" ? "Laki-laki" : "Perempuan"}
                        </Typography>
                      </TableCell>
                      <TableCell>{row.nip || "-"}</TableCell>
                      <TableCell>{row.teaching_subject || "-"}</TableCell>
                      <TableCell>
                        <Chip
                          label={row.employment_status || "N/A"}
                          size="small"
                          color="primary"
                          variant="outlined"
                          className="font-bold"
                        />
                      </TableCell>
                      <TableCell align="center">
                        <Button
                          variant="text"
                          size="small"
                          startIcon={<NiEyeOpen size="small" />}
                          onClick={() => navigate(`/academic/subjects/staff/details?id=${row.id}`)}
                        >
                          Detail
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={5}>
                      <Box className="py-20 text-center">
                        <Typography variant="body1" color="text.secondary">
                          Belum ada data staf yang sesuai.
                        </Typography>
                        <Button
                          variant="outlined"
                          color="primary"
                          className="mt-4 rounded-xl"
                          onClick={() => {
                            setSearchQuery("");
                            setFilterGender("Semua");
                            setFilterStatus("Semua");
                          }}
                        >
                          Reset Filter
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
        </Card>
      </Grid>
    </Grid>
  );
}
