import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  Chip,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiBook from "@/icons/nexture/ni-book";

interface ReadingLevel {
  id: string;
  level_code: string;
  level_name: string;
  description: string;
  wpm_min: number;
  wpm_max: number;
}

export default function ReadingLiteracyPage() {
  const [levels, setLevels] = useState<ReadingLevel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLevels = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/reading-literacy/levels`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setLevels(json.data.levels || []);
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
    fetchLevels();
  }, []);

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Tingkat Literasi Membaca
        </Typography>
        <Box className="flex gap-2">
          <Button variant="outlined" component={Link} to="/academic/reading-literacy/progression">
            Lihat Progres Siswa
          </Button>
          <Button
            variant="contained"
            startIcon={<NiBook />}
            component={Link}
            to="/academic/reading-literacy/assessment"
          >
            Asesmen Membaca
          </Button>
        </Box>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Literasi Membaca</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Standar Literasi Membaca disesuaikan dengan Early Grade Reading Assessment (EGRA).
      </Alert>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <TableContainer component={Card}>
        <Table>
          <TableHead>
            <TableRow className="bg-action-hover">
              <TableCell className="font-bold">Kode</TableCell>
              <TableCell className="font-bold">Tingkat Membaca</TableCell>
              <TableCell className="font-bold">Standar Kelancaran (WPM)</TableCell>
              <TableCell className="font-bold">Deskripsi</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : levels.length > 0 ? (
              levels.map((lvl) => (
                <TableRow key={lvl.id} hover>
                  <TableCell>
                    <Chip label={lvl.level_code} color="primary" />
                  </TableCell>
                  <TableCell className="text-primary font-medium">{lvl.level_name}</TableCell>
                  <TableCell>
                    {lvl.wpm_max > 0 ? `${lvl.wpm_min} - ${lvl.wpm_max} WPM` : `> ${lvl.wpm_min} WPM`}
                  </TableCell>
                  <TableCell>{lvl.description}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center" className="py-10">
                  Tidak ada data tingkat membaca.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
