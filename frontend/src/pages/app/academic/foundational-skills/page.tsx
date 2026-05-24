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
import NiStar from "@/icons/nexture/ni-star";

interface FoundationalSkillStandard {
  id: string;
  skill_type: string;
  skill_code: string;
  skill_name: string;
  description: string;
  indicators: string;
}

export default function FoundationalSkillsPage() {
  const [standards, setStandards] = useState<FoundationalSkillStandard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStandards = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/foundational-skills/standards`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setStandards(json.data.standards || []);
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
    fetchStandards();
  }, []);

  const parseIndicators = (indicatorsStr: string) => {
    try {
      return JSON.parse(indicatorsStr) as string[];
    } catch {
      return [];
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Standar Keterampilan Dasar
        </Typography>
        <Box className="flex gap-2">
          <Button variant="outlined" component={Link} to="/academic/foundational-skills/progress">
            Lihat Progres Siswa
          </Button>
          <Button
            variant="contained"
            startIcon={<NiStar size="small" />}
            component={Link}
            to="/academic/foundational-skills/assessment"
          >
            Asesmen Baru
          </Button>
        </Box>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Keterampilan Dasar</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Standar keterampilan dasar Literasi dan Numerasi difokuskan untuk Fase A (Kelas 1-2).
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
              <TableCell className="font-bold">Tipe</TableCell>
              <TableCell className="font-bold">Kode</TableCell>
              <TableCell className="font-bold">Nama Keterampilan</TableCell>
              <TableCell className="font-bold">Deskripsi</TableCell>
              <TableCell className="font-bold">Indikator</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : standards.length > 0 ? (
              standards.map((s) => (
                <TableRow key={s.id} hover>
                  <TableCell>
                    <Chip
                      label={s.skill_type}
                      color={s.skill_type === "LITERASI" ? "primary" : "secondary"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell className="text-primary font-medium">{s.skill_code}</TableCell>
                  <TableCell className="font-medium">{s.skill_name}</TableCell>
                  <TableCell>{s.description}</TableCell>
                  <TableCell>
                    <ul className="m-0 pl-4">
                      {parseIndicators(s.indicators).map((ind, i) => (
                        <li key={i} className="text-sm">
                          {ind}
                        </li>
                      ))}
                    </ul>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="py-10">
                  Tidak ada data standar keterampilan dasar.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
