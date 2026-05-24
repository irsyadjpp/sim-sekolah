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

interface LearningExperience {
  id: string;
  experience_code: string;
  experience_name: string;
  description: string;
  sequence_order: number;
  key_indicators: string;
  is_active: boolean;
}

export default function LearningExperiencesPage() {
  const [experiences, setExperiences] = useState<LearningExperience[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchExperiences = async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/learning-experiences`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.success === true) {
        setExperiences(json.data.experiences || []);
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
    fetchExperiences();
  }, []);

  const parseIndicators = (indicatorsStr: string) => {
    try {
      return JSON.parse(indicatorsStr) as string[];
    } catch {
      return [];
    }
  };

  const getExperienceColor = (code: string) => {
    switch (code) {
      case "MEMAHAMI":
        return "primary";
      case "MENAPLIKASI":
        return "secondary";
      case "MEREFEKSI":
        return "success";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Tahap Pengalaman Belajar
        </Typography>
        <Box className="flex gap-2">
          <Button variant="outlined" component={Link} to="/academic/learning-experiences/progression">
            Lihat Progres Siswa
          </Button>
        </Box>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        <Link to="/academic">Akademik</Link>
        <Typography variant="body2">Tahap Pengalaman Belajar</Typography>
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Tahap pengalaman belajar terdiri dari 3 fase: Memahami, Mengaplikasi, dan Merefleksi. Setiap fase
        merepresentasikan progres kognitif siswa dalam pembelajaran.
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
              <TableCell className="font-bold">Nama Tahap</TableCell>
              <TableCell className="font-bold">Deskripsi</TableCell>
              <TableCell className="font-bold">Urutan</TableCell>
              <TableCell className="font-bold">Indikator</TableCell>
              <TableCell className="font-bold">Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : experiences.length > 0 ? (
              experiences
                .sort((a, b) => a.sequence_order - b.sequence_order)
                .map((exp) => (
                  <TableRow key={exp.id} hover>
                    <TableCell className="text-primary font-medium">{exp.experience_code}</TableCell>
                    <TableCell className="font-medium">{exp.experience_name}</TableCell>
                    <TableCell>{exp.description}</TableCell>
                    <TableCell>
                      <Chip
                        label={`Urutan ${exp.sequence_order}`}
                        size="small"
                        color={getExperienceColor(exp.experience_code) as any}
                      />
                    </TableCell>
                    <TableCell>
                      <ul className="m-0 pl-4">
                        {parseIndicators(exp.key_indicators).map((ind, i) => (
                          <li key={i} className="text-sm">
                            {ind}
                          </li>
                        ))}
                      </ul>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={exp.is_active ? "Aktif" : "Tidak Aktif"}
                        color={exp.is_active ? "success" : "default"}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center" className="py-10">
                  Tidak ada data tahap pengalaman belajar.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
