import dayjs from "dayjs";
import { useState } from "react";
import { useDropzone } from "react-dropzone";

import {
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  FormControl,
  FormLabel,
  Grid,
  Input,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

import { DEFAULTS } from "@/config";
import NiCalendar from "@/icons/nexture/ni-calendar";
import NiChevronDownSmall from "@/icons/nexture/ni-chevron-down-small";
import NiChevronLeftSmall from "@/icons/nexture/ni-chevron-left-small";
import NiChevronRightSmall from "@/icons/nexture/ni-chevron-right-small";
import NiPen from "@/icons/nexture/ni-pen";
import NiPlus from "@/icons/nexture/ni-plus";
import { cn } from "@/lib/utils";
import type { MeData } from "@/types/me";

interface Props {
  meData: MeData;
  onUpdated: () => void;
}

const GENDER_OPTIONS = [
  { value: "L", label: "Laki-laki" },
  { value: "P", label: "Perempuan" },
];

export default function SettingsPublicInfo({ meData, onUpdated }: Props) {
  const profile = meData.teacher ?? meData.student;
  const isTeacher = !!meData.teacher;

  const [fullName, setFullName] = useState(meData.full_name ?? "");
  const [username, setUsername] = useState(meData.username ?? "");
  const [gender, setGender] = useState(profile?.gender ?? "");
  const [birthPlace, setBirthPlace] = useState(profile?.birth_place ?? "");
  const [birthDate, setBirthDate] = useState<string>(profile?.birth_date ?? "");
  const [religion, setReligion] = useState(profile?.religion ?? "");
  const [nationality, setNationality] = useState(profile?.nationality ?? "WNI");
  const [previewUrl, setPreviewUrl] = useState<string>(profile?.photo_url ?? "");
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);

  const { getRootProps, getInputProps, open } = useDropzone({
    noClick: true,
    noKeyboard: true,
    accept: { "image/*": [] },
    maxFiles: 1,
    multiple: false,
    onDrop: async (files) => {
      const file = files[0];
      if (!file) return;

      setPreviewUrl(URL.createObjectURL(file));

      // Auto upload on selection
      const token = localStorage.getItem("accessToken");
      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/me/photo`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });
        if (res.ok) {
          const json = await res.json();
          setPreviewUrl(json.data.photo_url);
          onUpdated();
        }
      } catch (err) {
        console.error("Gagal upload foto:", err);
      }
    },
  });

  const handleSave = async () => {
    setSaving(true);
    setSaveMsg(null);
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/auth/me`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ full_name: fullName, username }),
      });
      if (!res.ok) throw new Error("Gagal menyimpan perubahan.");
      setSaveMsg("Profil berhasil disimpan.");
      onUpdated();
    } catch (e: unknown) {
      setSaveMsg(e instanceof Error ? e.message : "Terjadi kesalahan.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Grid size={12}>
      <Card>
        <CardContent>
          <Box className="mb-2 flex items-center justify-between">
            <Typography variant="h6" component="h6" className="card-title mb-0">
              Informasi Publik
            </Typography>
            <Box className="flex gap-2">
              {meData.roles.map((r) => (
                <Chip
                  key={r}
                  label={r}
                  size="small"
                  color={r === "GURU" ? "primary" : r === "SISWA" ? "success" : "default"}
                />
              ))}
            </Box>
          </Box>

          {/* Foto Profil */}
          <FormControl
            variant="standard"
            size="small"
            fullWidth
            {...getRootProps({ className: "dropzone outlined lg:flex-row lg:gap-2.5 relative items-start" })}
          >
            <FormLabel component="label" className="min-w-60">
              Foto Profil
            </FormLabel>
            <Box className="relative">
              <Avatar alt="avatar" src={previewUrl} className="h-20 w-20 rounded-4xl" />
              <input {...getInputProps()} />
              <Button
                className="icon-only bg-background-paper hover:text-primary hover:bg-background-paper absolute -end-1 -bottom-1"
                size="small"
                color="grey"
                variant="outlined"
                startIcon={previewUrl ? <NiPen size={"small"} /> : <NiPlus size={"small"} />}
                onClick={open}
              />
            </Box>
          </FormControl>

          {/* Nama Lengkap */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Nama Lengkap
            </FormLabel>
            <Input value={fullName} onChange={(e) => setFullName(e.target.value)} className="w-full" />
          </FormControl>

          {/* Username */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Username
            </FormLabel>
            <Input value={username} onChange={(e) => setUsername(e.target.value)} className="w-full" />
          </FormControl>

          {/* Email (readonly) */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Email
            </FormLabel>
            <Input value={meData.email} disabled className="w-full" />
          </FormControl>

          {/* Jenis Kelamin */}
          {profile && (
            <FormControl fullWidth size="small" variant="standard" className="outlined lg:flex-row lg:gap-2.5">
              <FormLabel component="label" className="min-w-60">
                Jenis Kelamin
              </FormLabel>
              <Select
                className="w-full"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                IconComponent={NiChevronDownSmall}
                MenuProps={{ className: "outlined" }}
              >
                {GENDER_OPTIONS.map((o) => (
                  <MenuItem key={o.value} value={o.value}>
                    {o.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}

          {/* Tempat Lahir */}
          {profile && (
            <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
              <FormLabel component="label" className="min-w-60">
                Tempat Lahir
              </FormLabel>
              <Input value={birthPlace} onChange={(e) => setBirthPlace(e.target.value)} className="w-full" />
            </FormControl>
          )}

          {/* Tanggal Lahir */}
          {profile && (
            <FormControl fullWidth variant="standard" className="outlined lg:flex-row lg:gap-2.5">
              <FormLabel component="label" className="min-w-60">
                Tanggal Lahir
              </FormLabel>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DatePicker
                  className="mb-0 w-full"
                  slots={{
                    openPickerIcon: (props) => (
                      <NiCalendar {...props} className={cn(props.className, "text-text-secondary")} />
                    ),
                    switchViewIcon: (props) => (
                      <NiChevronDownSmall {...props} className={cn(props.className, "text-text-secondary")} />
                    ),
                    leftArrowIcon: (props) => (
                      <NiChevronLeftSmall {...props} className={cn(props.className, "text-text-secondary")} />
                    ),
                    rightArrowIcon: (props) => (
                      <NiChevronRightSmall {...props} className={cn(props.className, "text-text-secondary")} />
                    ),
                  }}
                  slotProps={{
                    textField: { size: "small", variant: "standard" },
                    desktopPaper: { className: "outlined" },
                  }}
                  value={birthDate ? dayjs(birthDate) : null}
                  onChange={(v) => setBirthDate(v ? v.format("YYYY-MM-DD") : "")}
                />
              </LocalizationProvider>
            </FormControl>
          )}

          {/* Agama */}
          {profile && (
            <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
              <FormLabel component="label" className="min-w-60">
                Agama
              </FormLabel>
              <Input value={religion} onChange={(e) => setReligion(e.target.value)} className="w-full" />
            </FormControl>
          )}

          {/* Kewarganegaraan */}
          {profile && (
            <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
              <FormLabel component="label" className="min-w-60">
                Kewarganegaraan
              </FormLabel>
              <Input value={nationality} onChange={(e) => setNationality(e.target.value)} className="w-full" />
            </FormControl>
          )}

          {/* Teacher-specific: NIP, NUPTK */}
          {isTeacher && meData.teacher && (
            <>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NIP
                </FormLabel>
                <Input value={meData.teacher.nip ?? ""} disabled className="w-full" />
              </FormControl>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NUPTK
                </FormLabel>
                <Input value={meData.teacher.nuptk ?? ""} disabled className="w-full" />
              </FormControl>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Mata Pelajaran
                </FormLabel>
                <Input value={meData.teacher.teaching_subject ?? ""} disabled className="w-full" />
              </FormControl>
            </>
          )}

          {/* Student-specific: NIS, NISN */}
          {!isTeacher && meData.student && (
            <>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NIS
                </FormLabel>
                <Input value={meData.student.nis ?? ""} disabled className="w-full" />
              </FormControl>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  NISN
                </FormLabel>
                <Input value={meData.student.nisn ?? ""} disabled className="w-full" />
              </FormControl>
              <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
                <FormLabel component="label" className="min-w-60">
                  Status
                </FormLabel>
                <Input value={meData.student.student_status ?? ""} disabled className="w-full" />
              </FormControl>
            </>
          )}

          {saveMsg && (
            <Typography variant="body2" color={saveMsg.includes("Gagal") ? "error" : "success.main"} className="mt-2">
              {saveMsg}
            </Typography>
          )}

          <Button
            size="medium"
            color="primary"
            variant="outlined"
            onClick={handleSave}
            disabled={saving}
            className="mt-2"
          >
            {saving ? "Menyimpan..." : "Simpan Perubahan"}
          </Button>
        </CardContent>
      </Card>
    </Grid>
  );
}
