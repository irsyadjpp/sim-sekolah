import { Box, Card, CardContent, Chip, FormControl, FormLabel, Grid, Input, Typography } from "@mui/material";

import type { MeData } from "@/types/me";

interface Props {
  meData: MeData;
  roleLabel: string;
}

export default function SettingsRole({ meData, roleLabel }: Props) {
  const isTeacher = !!meData.teacher;
  const isStudent = !!meData.student;
  const teacher = meData.teacher;
  const student = meData.student;

  return (
    <Grid size={12}>
      <Card>
        <CardContent>
          <Box className="mb-2 flex items-center justify-between">
            <Typography variant="h6" component="h6" className="card-title mb-0">
              {isTeacher ? "Data Kepegawaian" : isStudent ? "Data Akademik" : "Informasi Peran"}
            </Typography>
            <Chip label={roleLabel} color="primary" size="small" />
          </Box>

          {/* ========== TEACHER SECTION ========== */}
          {isTeacher && teacher && (
            <>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NIP
                </FormLabel>
                <Input value={teacher.nip ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NUPTK
                </FormLabel>
                <Input value={teacher.nuptk ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NIY / NIGK
                </FormLabel>
                <Input value={teacher.niy_nigk ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Status Kepegawaian
                </FormLabel>
                <Input value={teacher.employment_status ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Mata Pelajaran Diampu
                </FormLabel>
                <Input value={teacher.teaching_subject ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Jabatan Tambahan
                </FormLabel>
                <Input value={teacher.additional_position ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Jam Mengajar
                </FormLabel>
                <Input value={teacher.teaching_hours?.toString() ?? "0"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Pendidikan Terakhir
                </FormLabel>
                <Input value={teacher.last_education ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Jurusan
                </FormLabel>
                <Input value={teacher.major ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Universitas
                </FormLabel>
                <Input value={teacher.university_name ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Sertifikasi Guru
                </FormLabel>
                <Box className="flex items-center gap-2 pt-2">
                  <Chip
                    label={teacher.is_certified ? "Sudah Sertifikasi" : "Belum Sertifikasi"}
                    color={teacher.is_certified ? "success" : "default"}
                    size="small"
                  />
                  {teacher.is_certified && (
                    <Typography variant="body2" className="text-text-secondary">
                      No. {teacher.certificate_number}
                    </Typography>
                  )}
                </Box>
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Status Aktif
                </FormLabel>
                <Box className="pt-2">
                  <Chip
                    label={teacher.is_active ? "Aktif" : "Tidak Aktif"}
                    color={teacher.is_active ? "success" : "error"}
                    size="small"
                  />
                </Box>
              </FormControl>
            </>
          )}

          {/* ========== STUDENT SECTION ========== */}
          {isStudent && student && (
            <>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NIS
                </FormLabel>
                <Input value={student.nis ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NISN
                </FormLabel>
                <Input value={student.nisn ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Tahun Masuk
                </FormLabel>
                <Input value={student.enrollment_year?.toString() ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Kurikulum
                </FormLabel>
                <Input value={student.curriculum ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Status Siswa
                </FormLabel>
                <Box className="pt-2">
                  <Chip
                    label={student.student_status ?? "Tidak Diketahui"}
                    color={student.student_status === "Aktif" ? "success" : "default"}
                    size="small"
                  />
                </Box>
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Golongan Darah
                </FormLabel>
                <Input value={student.blood_type ?? "-"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Tinggi Badan (cm)
                </FormLabel>
                <Input value={student.height?.toString() ?? "0"} disabled className="w-full" />
              </FormControl>

              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Berat Badan (kg)
                </FormLabel>
                <Input value={student.weight?.toString() ?? "0"} disabled className="w-full" />
              </FormControl>
            </>
          )}

          {/* Jika akun belum terhubung ke profil manapun */}
          {!isTeacher && !isStudent && (
            <Typography variant="body2" className="text-text-secondary mt-2">
              Akun ini belum terhubung ke profil Guru atau Siswa. Hubungi administrator sekolah.
            </Typography>
          )}

          <Typography variant="caption" className="text-text-secondary mt-4 block">
            * Data kepegawaian/akademik hanya bisa diubah oleh administrator sekolah.
          </Typography>
        </CardContent>
      </Card>
    </Grid>
  );
}
