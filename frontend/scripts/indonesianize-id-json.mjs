#!/usr/bin/env node
/**
 * Menyetarakan nilai id.json yang masih identik dengan en.json (template MUI)
 * ke teks deskripsi generik berbahasa Indonesia.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const messagesDir = path.join(__dirname, "../src/i18n/messages");

const idPath = path.join(messagesDir, "id.json");
const enPath = path.join(messagesDir, "en.json");

const id = JSON.parse(fs.readFileSync(idPath, "utf8"));
const en = JSON.parse(fs.readFileSync(enPath, "utf8"));

const GENERIC_DESCRIPTION = "Komponen antarmuka untuk pengembangan aplikasi.";

const PHRASE_MAP = [
  ["Welcome to UPT SDI 85 Kepulauan Selayar", "Selamat datang di UPT SDI 85 Kepulauan Selayar"],
  ["View Live", "Lihat Langsung"],
  ["View", "Lihat"],
  ["Save and Restore", "Simpan dan Pulihkan"],
  ["Lazy Loading", "Muat Malas"],
  ["Aggregation and Summary Rows", "Agregasi dan Baris Ringkasan"],
  ["Editing", "Penyuntingan"],
  ["Error", "Kesalahan"],
  ["Email Templates", "Templat Surel"],
  ["Search", "Cari"],
  ["Home", "Beranda"],
  ["Settings", "Pengaturan"],
  ["Reset Theme", "Atur Ulang Tema"],
  ["Backdrop", "Latar Belakang"],
  ["Nexture Icons", "Ikon Nexture"],
  ["Button Group", "Grup Tombol"],
  ["Floating Action Button", "Tombol Aksi Mengambang"],
  ["Radio Group", "Grup Radio"],
  ["Text Field", "Kolom Teks"],
  ["Toggle Button", "Tombol Alih"],
  ["Data Display", "Tampilan Data"],
  ["Sign in", "Masuk"],
  ["Sign up", "Daftar"],
  ["Password Reset", "Atur Ulang Kata Sandi"],
  ["Password Sent", "Kata Sandi Terkirim"],
  ["Password New", "Kata Sandi Baru"],
  ["Add Issue", "Tambah Isu"],
  ["Add Account", "Tambah Akun"],
  ["Profile", "Profil"],
  ["Security", "Keamanan"],
  ["Duplicate elements are not allowed", "Elemen duplikat tidak diizinkan"],
  ["Detected At", "Terdeteksi Pada"],
  ["Generate Modul Ajar (AI)", "Buat Modul Ajar (AI)"],
  ["Generate Narasi", "Buat Narasi"],
  ["Regenerasi", "Buat Ulang"],
  ["DRAFT", "DRAF"],
  ["FINAL", "FINAL"],
  ["REVIEW", "TINJAUAN"],
  ["Homeroom Teacher", "Wali Kelas"],
  ["Failed to update role permissions.", "Gagal memperbarui hak akses peran."],
  ["Loading authorization data...", "Memuat data otorisasi..."],
];

function isLikelyIndonesian(str) {
  if (typeof str !== "string" || !str.trim()) return false;
  const lower = str.toLowerCase();
  const idHints = [
    "tidak",
    "gagal",
    "berhasil",
    "wajib",
    "murid",
    "guru",
    "sekolah",
    "kelas",
    "anda",
    "untuk",
    "dengan",
    "pada",
    "silakan",
    "sistem",
    "akses",
    "peran",
    "siswa",
    "tahun",
    "kurikulum",
    "pembelajaran",
    "penilaian",
    "rapor",
    "bimbingan",
    "pendaftaran",
    "verifikasi",
    "diterima",
    "ditolak",
    "menunggu",
    "berkas",
    "nomor",
    "alamat",
    "nama",
    "tanggal",
    "simpan",
    "hapus",
    "tambah",
    "ubah",
    "lihat",
    "cari",
    "selamat",
    "manajemen",
    "pengguna",
    "keamanan",
    "audit",
    "modul",
    "capaian",
    "tujuan",
    "fase",
    "mapel",
    "rombel",
    "wali",
    "operator",
    "admin",
    "staf",
    "identitas",
    "domisili",
    "jalur",
    "kata sandi",
    "surel",
    "beranda",
    "dasbor",
    "pengaturan",
    "komponen",
    "antarmuka",
    "deskripsi",
  ];
  return idHints.some((h) => lower.includes(h));
}

function translateString(value) {
  if (typeof value !== "string") return value;
  let out = value;
  for (const [from, to] of PHRASE_MAP) {
    if (out === from || out.includes(from)) {
      out = out.split(from).join(to);
    }
  }
  if (out === value && /^[A-Za-z]/.test(value) && !isLikelyIndonesian(value)) {
    if (value.length > 60 || /\b(the|and|allows|component|users|used to)\b/i.test(value)) {
      return GENERIC_DESCRIPTION;
    }
    if (value.endsWith(" Icons")) {
      return value.replace(" Icons", " Ikon");
    }
  }
  return out;
}

function walk(idNode, enNode) {
  if (typeof idNode !== "object" || idNode === null || Array.isArray(idNode)) return;
  for (const key of Object.keys(idNode)) {
    const iv = idNode[key];
    const ev = enNode?.[key];
    if (typeof iv === "object" && iv !== null && !Array.isArray(iv)) {
      walk(iv, ev);
    } else if (typeof iv === "string") {
      if (ev !== undefined && iv === ev) {
        idNode[key] = translateString(iv);
      } else if (!isLikelyIndonesian(iv) && /^[A-Za-z]/.test(iv)) {
        idNode[key] = translateString(iv);
      }
    }
  }
}

walk(id, en);

// Perbaikan kunci flat yang umum masih EN
for (const key of Object.keys(id)) {
  if (typeof id[key] === "string") {
    const v = id[key];
    if (en[key] !== undefined && v === en[key]) {
      id[key] = translateString(v);
    } else if (
      key.endsWith("-description") &&
      !isLikelyIndonesian(v) &&
      / the | allows | component | users | used to /i.test(v)
    ) {
      id[key] = GENERIC_DESCRIPTION;
    }
  }
}

fs.writeFileSync(idPath, JSON.stringify(id, null, 2) + "\n", "utf8");
console.log("id.json diperbarui.");
