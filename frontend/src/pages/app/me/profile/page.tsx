import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Avatar,
  Box,
  Breadcrumbs,
  Card,
  CardContent,
  Chip,
  Divider,
  FormControl,
  FormLabel,
  Grid,
  Input,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import type { MeData } from "@/types/me";

const ReadField = ({ label, value }: { label: string; value?: string | number | null }) => (
  <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
    <FormLabel component="label" className="min-w-60">
      {label}
    </FormLabel>
    <Input value={value ?? "-"} disabled className="w-full" />
  </FormControl>
);

export default function ProfilePage() {
  const [meData, setMeData] = useState<MeData | null>(() => {
    const cachedUser = localStorage.getItem("-user-data");
    if (cachedUser) {
      try {
        return JSON.parse(cachedUser);
      } catch (e) {
        console.error("Failed to parse cached user", e);
      }
    }
    return null;
  });
  const [loading, setLoading] = useState(() => (!localStorage.getItem("accessToken") ? false : true));
  const [error, setError] = useState<string | null>(() =>
    !localStorage.getItem("accessToken") ? "Sesi tidak valid. Silakan login kembali." : null,
  );

  useEffect(() => {
    // Fetch from API to update data
    const token = localStorage.getItem("accessToken");
    if (!token) return;
    fetch(`${DEFAULTS.API_URL}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r: Response) => {
        if (!r.ok) throw new Error("Gagal memuat profil.");
        return r.json();
      })
      .then((json) => {
        setMeData(json.data);
        localStorage.setItem("-user-data", JSON.stringify(json.data));
        setLoading(false);
      })
      .catch((e: Error) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  const profile = meData?.teacher ?? meData?.student ?? null;
  const isTeacher = !!meData?.teacher;
  const isStudent = !!meData?.student;

  const roleLabel: Record<string, string> = {
    SUPER_ADMIN: "Super Admin",
    ADMIN_SEKOLAH: "Admin Sekolah",
    GURU: "Guru",
    SISWA: "Siswa",
  };

  return (
    <Box>
      <Typography variant="h1" component="h1" className="mb-1">
        Profil Saya
      </Typography>
      <Breadcrumbs className="mb-6">
        <Link to="/dashboards/default">Beranda</Link>
        <Typography variant="body2">Profil</Typography>
      </Breadcrumbs>

      {loading && <Typography>Memuat profil...</Typography>}
      {error && <Typography color="error">{error}</Typography>}

      {meData && (
        <Grid container spacing={4} className="items-start">
          {/* ---- KARTU KIRI: Avatar + Nama ---- */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent className="flex flex-col items-center gap-3 py-8 text-center">
                <Avatar src={profile?.photo_url ?? ""} alt={meData.full_name} sx={{ width: 96, height: 96 }} />
                <Typography variant="h5" component="p">
                  {meData.full_name}
                </Typography>
                <Typography variant="body2" className="text-text-secondary">
                  {meData.email}
                </Typography>
                <Typography variant="body2" className="text-text-secondary">
                  @{meData.username}
                </Typography>
                <Box className="mt-1 flex flex-wrap justify-center gap-1">
                  {meData.roles.map((r) => (
                    <Chip
                      key={r}
                      label={roleLabel[r] ?? r}
                      size="small"
                      color={r === "GURU" ? "primary" : r === "SISWA" ? "success" : "default"}
                    />
                  ))}
                </Box>
                {isTeacher && meData.teacher && (
                  <Box className="mt-2 w-full text-left">
                    <Divider className="mb-3" />
                    <Typography variant="caption" className="text-text-secondary mb-1 block">
                      STATUS KEPEGAWAIAN
                    </Typography>
                    <Chip
                      label={meData.teacher.employment_status ?? "Tidak diketahui"}
                      size="small"
                      variant="outlined"
                    />
                    {meData.teacher.is_certified && (
                      <Chip label="Bersertifikasi" size="small" color="success" className="ml-1" />
                    )}
                    {meData.teacher.is_active ? (
                      <Chip label="Aktif" size="small" color="success" className="ml-1" />
                    ) : (
                      <Chip label="Tidak Aktif" size="small" color="error" className="ml-1" />
                    )}
                  </Box>
                )}
                {isStudent && meData.student && (
                  <Box className="mt-2 w-full text-left">
                    <Divider className="mb-3" />
                    <Typography variant="caption" className="text-text-secondary mb-1 block">
                      STATUS SISWA
                    </Typography>
                    <Chip
                      label={meData.student.student_status ?? "Aktif"}
                      size="small"
                      color={meData.student.student_status === "Aktif" ? "success" : "default"}
                    />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* ---- KARTU KANAN: Detail ---- */}
          <Grid size={{ xs: 12, md: 8 }} container spacing={3}>
            {/* Informasi Akun */}
            <Grid size={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" component="h6" className="card-title">
                    Informasi Akun
                  </Typography>
                  <ReadField label="Nama Lengkap" value={meData.full_name} />
                  <ReadField label="Username" value={meData.username} />
                  <ReadField label="Email" value={meData.email} />
                </CardContent>
              </Card>
            </Grid>

            {/* Identitas Diri */}
            {profile && (
              <Grid size={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" component="h6" className="card-title">
                      Identitas Diri
                    </Typography>
                    <ReadField
                      label="Jenis Kelamin"
                      value={
                        profile.gender === "L" ? "Laki-laki" : profile.gender === "P" ? "Perempuan" : profile.gender
                      }
                    />
                    <ReadField label="Tempat Lahir" value={profile.birth_place} />
                    <ReadField
                      label="Tanggal Lahir"
                      value={
                        profile.birth_date
                          ? new Date(profile.birth_date).toLocaleDateString("id-ID", {
                              day: "2-digit",
                              month: "long",
                              year: "numeric",
                            })
                          : undefined
                      }
                    />
                    <ReadField label="Agama" value={profile.religion} />
                    <ReadField label="Kewarganegaraan" value={profile.nationality} />
                  </CardContent>
                </Card>
              </Grid>
            )}

            {/* Kontak & Alamat */}
            {profile && (
              <Grid size={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" component="h6" className="card-title">
                      Kontak &amp; Alamat
                    </Typography>
                    {isTeacher && meData.teacher && <ReadField label="Telepon" value={meData.teacher.phone} />}
                    <ReadField label="Alamat" value={profile.full_address} />
                    <ReadField label="Desa/Kelurahan" value={profile.village} />
                    <ReadField label="Kecamatan" value={profile.district} />
                    <ReadField label="Kabupaten/Kota" value={profile.regency} />
                    <ReadField label="Provinsi" value={profile.province} />
                    <ReadField label="Kode Pos" value={profile.postal_code} />
                  </CardContent>
                </Card>
              </Grid>
            )}

            {/* Data Guru */}
            {isTeacher && meData.teacher && (
              <Grid size={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" component="h6" className="card-title">
                      Data Kepegawaian
                    </Typography>
                    <ReadField label="NIP" value={meData.teacher.nip} />
                    <ReadField label="NUPTK" value={meData.teacher.nuptk} />
                    <ReadField label="NIY / NIGK" value={meData.teacher.niy_nigk} />
                    <ReadField label="Status" value={meData.teacher.employment_status} />
                    <ReadField label="Mata Pelajaran" value={meData.teacher.teaching_subject} />
                    <ReadField label="Jabatan Tambahan" value={meData.teacher.additional_position} />
                    <ReadField label="Jam Mengajar" value={meData.teacher.teaching_hours} />
                    <ReadField label="Pendidikan Terakhir" value={meData.teacher.last_education} />
                    <ReadField label="Jurusan" value={meData.teacher.major} />
                    <ReadField label="Universitas" value={meData.teacher.university_name} />
                    <ReadField label="Tahun Lulus" value={meData.teacher.graduation_year} />
                    <ReadField label="No. Sertifikat" value={meData.teacher.certificate_number} />
                  </CardContent>
                </Card>
              </Grid>
            )}

            {/* Data Siswa */}
            {isStudent && meData.student && (
              <Grid size={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" component="h6" className="card-title">
                      Data Akademik
                    </Typography>
                    <ReadField label="NIS" value={meData.student.nis} />
                    <ReadField label="NISN" value={meData.student.nisn} />
                    <ReadField label="Tahun Masuk" value={meData.student.enrollment_year} />
                    <ReadField label="Kurikulum" value={meData.student.curriculum} />
                    <ReadField label="Status Siswa" value={meData.student.student_status} />
                    <ReadField label="Golongan Darah" value={meData.student.blood_type} />
                    <ReadField
                      label="Tinggi Badan"
                      value={meData.student.height ? `${meData.student.height} cm` : undefined}
                    />
                    <ReadField
                      label="Berat Badan"
                      value={meData.student.weight ? `${meData.student.weight} kg` : undefined}
                    />
                  </CardContent>
                </Card>
              </Grid>
            )}

            <Grid size={12}>
              <Typography variant="caption" className="text-text-secondary">
                Untuk memperbarui data profil, kunjungi halaman{" "}
                <Link to="/settings" className="text-primary">
                  Pengaturan
                </Link>
                .
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}
