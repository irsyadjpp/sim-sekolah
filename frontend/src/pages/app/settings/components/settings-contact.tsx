import { useState } from "react";

import { Button, Card, CardContent, FormControl, FormLabel, Grid, Input, Typography } from "@mui/material";

import { DEFAULTS } from "@/config";
import type { MeData } from "@/types/me";

interface Props {
  meData: MeData;
  onUpdated: () => void;
}

export default function SettingsContact({ meData, onUpdated }: Props) {
  const profile = meData.teacher ?? meData.student;

  const isTeacher = !!meData.teacher;
  const [phone, setPhone] = useState(meData.teacher?.phone ?? "");
  const [fullAddress, setFullAddress] = useState(profile?.full_address ?? "");
  const [village, setVillage] = useState(profile?.village ?? "");
  const [district, setDistrict] = useState(profile?.district ?? "");
  const [regency, setRegency] = useState(profile?.regency ?? "");
  const [province, setProvince] = useState(profile?.province ?? "");
  const [postalCode, setPostalCode] = useState(profile?.postal_code ?? "");
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);

  const handleSave = async () => {
    if (!profile) return;
    setSaving(true);
    setSaveMsg(null);
    const token = localStorage.getItem("accessToken");
    const endpoint = isTeacher
      ? `${DEFAULTS.API_URL}/api/v1/teachers/${profile.id}`
      : `${DEFAULTS.API_URL}/api/v1/students/${profile.id}`;

    try {
      const res = await fetch(endpoint, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          phone,
          full_address: fullAddress,
          village,
          district,
          regency,
          province,
          postal_code: postalCode,
        }),
      });
      if (!res.ok) throw new Error("Gagal menyimpan data kontak.");
      setSaveMsg("Kontak berhasil diperbarui.");
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
          <Typography variant="h6" component="h6" className="card-title">
            Kontak &amp; Alamat
          </Typography>

          {/* Email (readonly dari akun) */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Email Akun
            </FormLabel>
            <Input value={meData.email} disabled className="w-full" />
          </FormControl>

          {/* Email profil (guru/siswa) */}
          {profile && "email" in profile && (
            <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
              <FormLabel component="label" className="min-w-60">
                Email Profil
              </FormLabel>
              <Input value={(profile as { email?: string }).email ?? ""} disabled className="w-full" />
            </FormControl>
          )}

          {/* Nomor Telepon */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Nomor Telepon
            </FormLabel>
            <Input
              placeholder="Masukkan nomor telepon"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full"
            />
          </FormControl>

          {/* Alamat lengkap */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Alamat Lengkap
            </FormLabel>
            <Input
              placeholder="Jl. ..."
              value={fullAddress}
              onChange={(e) => setFullAddress(e.target.value)}
              className="w-full"
            />
          </FormControl>

          {/* Desa */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Desa/Kelurahan
            </FormLabel>
            <Input value={village} onChange={(e) => setVillage(e.target.value)} className="w-full" />
          </FormControl>

          {/* Kecamatan */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Kecamatan
            </FormLabel>
            <Input value={district} onChange={(e) => setDistrict(e.target.value)} className="w-full" />
          </FormControl>

          {/* Kabupaten */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Kabupaten/Kota
            </FormLabel>
            <Input value={regency} onChange={(e) => setRegency(e.target.value)} className="w-full" />
          </FormControl>

          {/* Provinsi */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Provinsi
            </FormLabel>
            <Input value={province} onChange={(e) => setProvince(e.target.value)} className="w-full" />
          </FormControl>

          {/* Kode Pos */}
          <FormControl className="outlined lg:flex-row lg:gap-2.5" variant="standard" size="small" fullWidth>
            <FormLabel component="label" className="min-w-60">
              Kode Pos
            </FormLabel>
            <Input value={postalCode} onChange={(e) => setPostalCode(e.target.value)} className="w-full" />
          </FormControl>

          {saveMsg && (
            <Typography variant="body2" color={saveMsg.includes("Gagal") ? "error" : "success.main"} className="mt-2">
              {saveMsg}
            </Typography>
          )}

          {profile && (
            <Button
              size="medium"
              color="primary"
              variant="outlined"
              onClick={handleSave}
              disabled={saving}
              className="mt-2"
            >
              {saving ? "Menyimpan..." : "Simpan Kontak"}
            </Button>
          )}
        </CardContent>
      </Card>
    </Grid>
  );
}
