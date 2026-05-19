import axios from "axios";

import { DEFAULTS } from "@/config";

export const apiClient = axios.create({
  baseURL: DEFAULTS.API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export function translateUrl(url: string): string {
  if (!url) return url;

  let translated = url;

  // List of regex patterns to translate old English endpoints to new Indonesian ones
  const replacements: [RegExp, string][] = [
    // Auth sub-paths
    [/\/api\/v1\/auth\/sign-in/g, "/api/v1/otentikasi/masuk"],
    [/\/api\/v1\/auth\/login/g, "/api/v1/otentikasi/masuk"],
    [/\/api\/v1\/auth\/register/g, "/api/v1/otentikasi/daftar"],
    [/\/api\/v1\/auth\/refresh/g, "/api/v1/otentikasi/segarkan"],
    [/\/api\/v1\/auth\/logout/g, "/api/v1/otentikasi/keluar"],
    [/\/api\/v1\/auth\/forgot-password/g, "/api/v1/otentikasi/lupa-kata-sandi"],
    [/\/api\/v1\/auth\/reset-password/g, "/api/v1/otentikasi/atur-ulang-kata-sandi"],
    [/\/api\/v1\/auth\/verify-2fa/g, "/api/v1/otentikasi/verifikasi-2fa"],
    [/\/api\/v1\/auth\/me\/photo/g, "/api/v1/otentikasi/saya/foto"],
    [/\/api\/v1\/auth\/me/g, "/api/v1/otentikasi/saya"],
    [/\/api\/v1\/auth\/change-password/g, "/api/v1/otentikasi/ubah-kata-sandi"],
    [/\/api\/v1\/auth\/2fa\/setup/g, "/api/v1/otentikasi/2fa/atur"],
    [/\/api\/v1\/auth\/2fa\/enable/g, "/api/v1/otentikasi/2fa/aktifkan"],
    [/\/api\/v1\/auth\/2fa\/disable/g, "/api/v1/otentikasi/2fa/nonaktifkan"],
    [/\/api\/v1\/auth\/impersonate/g, "/api/v1/otentikasi/penyamaran"],
    [/\/api\/v1\/auth\/stop-impersonation/g, "/api/v1/otentikasi/berhenti-penyamaran"],
    [/\/api\/v1\/auth/g, "/api/v1/otentikasi"],

    // Nested Classrooms endpoints
    [/\/api\/v1\/classrooms\/([^/]+)\/enrollments/g, "/api/v1/kelas/$1/anggota"],
    [/\/api\/v1\/classrooms\/([^/]+)\/assignments/g, "/api/v1/kelas/$1/tugas-mengajar"],
    [/\/api\/v1\/classrooms\/([^/]+)\/attendances/g, "/api/v1/kelas/$1/kehadiran"],
    [/\/api\/v1\/classrooms\/([^/]+)\/reports/g, "/api/v1/kelas/$1/rapor"],
    [/\/api\/v1\/classrooms/g, "/api/v1/kelas"],

    // Nested Teaching Assignments & Assessments
    [/\/api\/v1\/teaching-assignments\/([^/]+)\/assessments/g, "/api/v1/tugas-mengajar/$1/penilaian"],
    [/\/api\/v1\/teaching-assignments/g, "/api/v1/tugas-mengajar"],
    [/\/api\/v1\/schedules/g, "/api/v1/jadwal"],
    [/\/api\/v1\/assessments\/([^/]+)\/scores/g, "/api/v1/penilaian/$1/nilai"],
    [/\/api\/v1\/assessments/g, "/api/v1/penilaian"],

    // Nested Reports endpoints
    [/\/api\/v1\/reports\/([^/]+)\/notes/g, "/api/v1/rapor/$1/catatan"],
    [/\/api\/v1\/reports\/([^/]+)\/scores/g, "/api/v1/rapor/$1/nilai"],
    [/\/api\/v1\/reports\/([^/]+)\/deep-learning/g, "/api/v1/rapor/$1/pembelajaran-mendalam"],
    [/\/api\/v1\/reports\/([^/]+)\/extracurricular/g, "/api/v1/rapor/$1/ekstrakurikuler"],
    [/\/api\/v1\/reports\/([^/]+)\/attendance/g, "/api/v1/rapor/$1/kehadiran"],
    [/\/api\/v1\/reports\/([^/]+)\/generate-ai-description/g, "/api/v1/rapor/$1/buat-deskripsi-ai"],
    [/\/api\/v1\/reports\/([^/]+)\/finalize/g, "/api/v1/rapor/$1/finalisasi"],
    [/\/api\/v1\/reports/g, "/api/v1/rapor"],

    // Nested Learning endpoints
    [/\/api\/v1\/learning\/atp\/([^/]+)\/generate-module/g, "/api/v1/pembelajaran/atp/$1/buat-modul"],
    [/\/api\/v1\/learning\/modules/g, "/api/v1/pembelajaran/modul"],
    [/\/api\/v1\/learning/g, "/api/v1/pembelajaran"],

    // Nested Local Contexts
    [/\/api\/v1\/local-contexts\/categories/g, "/api/v1/konteks-lokal/kategori"],
    [/\/api\/v1\/local-contexts/g, "/api/v1/konteks-lokal"],

    // Nested Deep Learning
    [/\/api\/v1\/deep-learning\/design-element/g, "/api/v1/pembelajaran-mendalam/elemen-desain"],
    [/\/api\/v1\/deep-learning\/cognitive-stage/g, "/api/v1/pembelajaran-mendalam/tahapan-kognitif"],
    [/\/api\/v1\/deep-learning\/assessment-level/g, "/api/v1/pembelajaran-mendalam/tingkat-asesmen"],
    [/\/api\/v1\/deep-learning/g, "/api/v1/pembelajaran-mendalam"],

    // Academic Years
    [/\/api\/v1\/academic-years\/([^/]+)\/activate/g, "/api/v1/tahun-ajaran/$1/aktifkan"],
    [/\/api\/v1\/academic-years/g, "/api/v1/tahun-ajaran"],

    // Curriculum Documents
    [/\/api\/v1\/curriculum-documents\/readiness/g, "/api/v1/dokumen-kurikulum/kesiapan"],
    [/\/api\/v1\/curriculum-documents\/chapters\/trigger/g, "/api/v1/dokumen-kurikulum/bab/pemicu"],
    [/\/api\/v1\/curriculum-documents\/([^/]+)\/chapters\/([^/]+)/g, "/api/v1/dokumen-kurikulum/$1/bab/$2"],
    [/\/api\/v1\/curriculum-documents\/chapters\/([^/]+)/g, "/api/v1/dokumen-kurikulum/bab/$1"],
    [/\/api\/v1\/curriculum-documents\/([^/]+)\/finalize/g, "/api/v1/dokumen-kurikulum/$1/finalisasi"],
    [/\/api\/v1\/curriculum-documents\/([^/]+)\/export/g, "/api/v1/dokumen-kurikulum/$1/ekspor"],
    [/\/api\/v1\/curriculum-documents/g, "/api/v1/dokumen-kurikulum"],

    // Learning Outcomes / CP
    [/\/api\/v1\/learning-outcomes\/([^/]+)\/details\/([^/]+)/g, "/api/v1/capaian-pembelajaran/$1/detail/$2"],
    [/\/api\/v1\/learning-outcomes\/([^/]+)\/details/g, "/api/v1/capaian-pembelajaran/$1/detail"],
    [
      /\/api\/v1\/learning-outcomes\/([^/]+)\/objectives\/([^/]+)/g,
      "/api/v1/capaian-pembelajaran/$1/tujuan-pembelajaran/$2",
    ],
    [/\/api\/v1\/learning-outcomes\/([^/]+)\/objectives/g, "/api/v1/capaian-pembelajaran/$1/tujuan-pembelajaran"],
    [/\/api\/v1\/learning-outcomes/g, "/api/v1/capaian-pembelajaran"],

    // Subjects Elements
    [/\/api\/v1\/subjects\/([^/]+)\/elements\/([^/]+)/g, "/api/v1/mata-pelajaran/$1/elemen/$2"],
    [/\/api\/v1\/subjects\/([^/]+)\/elements/g, "/api/v1/mata-pelajaran/$1/elemen"],
    [/\/api\/v1\/subjects/g, "/api/v1/mata-pelajaran"],

    // Dimensions
    [/\/api\/v1\/profile-dimensions/g, "/api/v1/dimensi-profil"],

    // Intelligence
    [/\/api\/v1\/intelligence\/students\/([^/]+)\/360/g, "/api/v1/kecerdasan-sistem/murid/$1/360"],
    [/\/api\/v1\/intelligence\/students\/([^/]+)\/profile-ext/g, "/api/v1/kecerdasan-sistem/murid/$1/profil-eksternal"],
    [/\/api\/v1\/intelligence\/anecdotal/g, "/api/v1/kecerdasan-sistem/anekdot"],
    [/\/api\/v1\/intelligence\/observation-tags/g, "/api/v1/kecerdasan-sistem/tag-observasi"],
    [
      /\/api\/v1\/intelligence\/assessment-instruments\/([^/]+)\/results/g,
      "/api/v1/kecerdasan-sistem/instrumen-penilaian/$1/hasil",
    ],
    [/\/api\/v1\/intelligence\/assessment-instruments/g, "/api/v1/kecerdasan-sistem/instrumen-penilaian"],
    [/\/api\/v1\/intelligence\/alerts\/([^/]+)\/intervene/g, "/api/v1/kecerdasan-sistem/peringatan/$1/intervensi"],
    [/\/api\/v1\/intelligence\/alerts\/trigger-cron/g, "/api/v1/kecerdasan-sistem/peringatan/pemicu-cron"],
    [/\/api\/v1\/intelligence\/alerts/g, "/api/v1/kecerdasan-sistem/peringatan"],
    [/\/api\/v1\/intelligence/g, "/api/v1/kecerdasan-sistem"],

    // Users & Roles
    [/\/api\/v1\/users\/roles/g, "/api/v1/pengguna/peran"],
    [/\/api\/v1\/users\/([^/]+)\/status/g, "/api/v1/pengguna/$1/status"],
    [/\/api\/v1\/users\/([^/]+)\/roles/g, "/api/v1/pengguna/$1/peran"],
    [/\/api\/v1\/users\/([^/]+)\/reset-password/g, "/api/v1/pengguna/$1/atur-ulang-kata-sandi"],
    [/\/api\/v1\/users/g, "/api/v1/pengguna"],

    // Permissions
    [/\/api\/v1\/permissions\/roles\/([^/]+)/g, "/api/v1/hak-akses/peran/$1"],
    [/\/api\/v1\/permissions/g, "/api/v1/hak-akses"],

    // System
    [/\/api\/v1\/system\/audit-logs/g, "/api/v1/sistem/catatan-audit"],
    [/\/api\/v1\/system/g, "/api/v1/sistem"],

    // Academic Promotion & Graduation
    [/\/api\/v1\/academic\/promotion/g, "/api/v1/akademik/kenaikan-kelas"],
    [/\/api\/v1\/academic\/graduation/g, "/api/v1/akademik/kelulusan"],
    [/\/api\/v1\/academic/g, "/api/v1/akademik"],

    // Classrooms & Teachers Schedules
    [/\/api\/v1\/classrooms\/([^/]+)\/schedules/g, "/api/v1/kelas/$1/jadwal"],
    [/\/api\/v1\/teachers\/([^/]+)\/schedules/g, "/api/v1/guru/$1/jadwal"],
    [/\/api\/v1\/schedules/g, "/api/v1/jadwal"],

    // Basic Resources
    [/\/api\/v1\/students\/([^/]+)\/parents\/([^/]+)/g, "/api/v1/murid/$1/orang-tua/$2"],
    [/\/api\/v1\/students\/([^/]+)\/parents/g, "/api/v1/murid/$1/orang-tua"],
    [/\/api\/v1\/students\/school\/([^/]+)/g, "/api/v1/murid/sekolah/$1"],
    [/\/api\/v1\/students/g, "/api/v1/murid"],
    [/\/api\/v1\/teachers\/school\/([^/]+)/g, "/api/v1/guru/sekolah/$1"],
    [/\/api\/v1\/teachers/g, "/api/v1/guru"],
    [/\/api\/v1\/grades\/phase\/([^/]+)/g, "/api/v1/tingkat-kelas/fase/$1"],
    [/\/api\/v1\/grades/g, "/api/v1/tingkat-kelas"],
    [/\/api\/v1\/phases/g, "/api/v1/fase"],
    [/\/api\/v1\/schools/g, "/api/v1/sekolah"],

    // AI
    [/\/api\/v1\/ai\/generate-narrative/g, "/api/v1/kecerdasan-buatan/buat-narasi"],
    [/\/api\/v1\/ai/g, "/api/v1/kecerdasan-buatan"],

    // Enrollment
    [/\/api\/v1\/enrollment/g, "/api/v1/pendaftaran"],

    // SPMB (Penerimaan Mahasiswa Baru)
    [/\/api\/v1\/ppdb\/applicants/g, "/api/v1/spmb/pelamar"],
    [/\/api\/v1\/ppdb\/applicants\/([^/]+)/g, "/api/v1/spmb/pelamar/$1"],
    [/\/api\/v1\/ppdb\/regulations/g, "/api/v1/spmb/peraturan"],
    [/\/api\/v1\/ppdb\/regulations\/([^/]+)/g, "/api/v1/spmb/peraturan/$1"],
    [/\/api\/v1\/ppdb/g, "/api/v1/spmb"],
  ];

  for (const [regex, replacement] of replacements) {
    if (regex.test(translated)) {
      translated = translated.replace(regex, replacement);
    }
  }

  return translated;
}
