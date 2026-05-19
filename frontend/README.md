# SIM Sekolah Terpadu - SD Negeri (Frontend UI)

Antarmuka pengguna (UI) modern untuk Sistem Informasi Manajemen Sekolah Terpadu, dibangun dengan fokus pada pengalaman pengguna (UX) yang premium, super cepat (*Fast UX*), ramah aksesibilitas (*Accessible UI*), responsif, dan mendukung penuh standar **Kurikulum Merdeka 2026**.

---

## 🌟 Fitur Unggulan UI & Peningkatan UX Premium

Aplikasi ini telah dirancang ulang untuk mematuhi **Prinsip Utama Modern Enterprise UX**:

### 1. ⚡ Fast UX & Perceived Performance
- **Shimmering Skeleton Loader**: Menghilangkan spinner pemuatan yang mengganggu. Pemuatan data tabel presensi dan evaluasi kini dilengkapi dengan visualisasi shimmering skeleton yang presisi guna menjaga stabilitas tata letak visual saat memproses data.
- **Optimistic UI state updates**: Operasi simpan absensi dan nilai siswa diperbarui secara instan di sisi klien tanpa memaksa *page reload* penuh atau *spinner lock-screen*, sehingga proses kerja guru terasa sangat lancar dan cepat.
- **Snackbar Floating Toast Notifications**: Notifikasi browser standard `alert()` telah digantikan sepenuhnya dengan komponen Material-UI `<Snackbar>` melayang yang elegan dengan sudut membulat modern (`16px`).

### 2. 🖱️ Minimum Click Principle (MCP) - Zero-Click Loading
- **Cascade Auto-Selection**: Halaman absensi harian, nilai sumatif, nilai formatif, dan jadwal pelajaran secara otomatis mendeteksi rombel aktif guru dan langsung memilih kelas pertama secara default.
- **Instant Mounting**: Daftar siswa langsung tampil secara otomatis sejak detik pertama halaman terbuka (**0 klik untuk melihat data**). Guru hanya membutuhkan maksimum 1–3 klik untuk menyelesaikan tugas-tugas administratif utama mereka.

### 3. 📊 Clean Table UX (ERP Table Standards) 🆕
- **Sticky Table Headers**: Judul tabel menempel kuat di atas kontainer scroll saat daftar data digulir ke bawah, memudahkan penelusuran tabel berskala besar.
- **Column Visibility Toggles**: Guru/Admin dapat menyembunyikan atau menampilkan kolom tabel secara real-time via checkbox dropdown (misalnya menyembunyikan kolom IP Address atau Email pada log audit).
- **Client-Side CSV Data Export**: Tombol ekspor instan untuk mengunduh seluruh baris tabel aktif menjadi file `.csv` dengan pemformatan yang aman dan cepat.
- **Interactive Multi-Column Sorting**: Klik pada judul header kolom akan memicu pengurutan asinkron instan (diindikasikan dengan ikon Unicode `🔼` / `🔽` / `↕️`).

### 4. ♿ Universal Accessibility (A11y Compliance) 🆕
- **Screen-Reader Basic Support**: Seluruh tombol kehadiran dan text field catatan pada tabel absensi harian dan penilaian akademik telah dilengkapi dengan tag dinamis `aria-label` yang spesifik sesuai nama siswa (misalnya `aria-label="Tandai Ahmad Dahlan sebagai Sakit"`).
- **Logical Tab Order**: Mendukung navigasi keyboard penuh menggunakan tombol `Tab`, memudahkan guru melakukan input nilai ratusan siswa berturut-turut tanpa memegang mouse.
- **WCAG High-Contrast Ratio**: Penggunaan rasio kontras teks minimum `4.5:1` dan warna status terpadu yang ramah bagi pengguna dengan keterbatasan penglihatan warna (*color blindness*).

### 5. 📈 UX Analytics & Telemetry Engine 🆕
- **Waktu Muat Halaman**: Mengukur durasi render visual rute secara presisi menggunakan `performance.now()`.
- **Runtime Error Catcher**: Menangkap kegagalan API, unhandled promise rejections, dan runtime error secara otomatis di peramban klien lengkap dengan *stack trace* dan info browser.
- **Telemetry Sync**: Sinkronisasi log telemetri klien di latar belakang secara asinkron ke endpoint `/api/v1/system/client-logs` untuk dialirkan langsung ke Loki & Grafana Observability Dashboard.

---

## 🛠️ Tech Stack

* **Framework:** [React 18+](https://reactjs.org/)
* **Build Tool:** [Vite](https://vitejs.dev/)
* **UI Library:** [Material UI (MUI) v6](https://mui.com/) (menggunakan Grid v2 terpadu)
* **Styling:** [TailwindCSS](https://tailwindcss.com/)
* **Form Management:** [Formik](https://formik.org/) & [Yup](https://github.com/jquense/yup)
* **State & Routing:** [React Router Dom v6](https://reactrouter.com/)
* **Icons:** Nexture Custom Icons
* **Telemetry Service:** Custom UX Analytics Telemetry Client

---

## 📦 Instalasi & Pengembangan

### 1. Prasyarat
* **Node.js** (v18 ke atas disarankan)
* **npm** atau **yarn**

### 2. Setup Awal
```bash
# Install dependensi
npm install
```

### 3. Konfigurasi Environment
Buat file `.env` di root folder frontend:
```env
VITE_API_URL=http://localhost:8080
VITE_APP_NAME="SIM Sekolah Terpadu"
```

### 4. Jalankan Aplikasi
```bash
npm run dev
```
Akses aplikasi di: `http://localhost:3001` (atau port yang tertera di terminal).

---

## 🏗️ Struktur Proyek

```
frontend/
├── src/
│   ├── components/     # Komponen UI (Layout, DataGrid, Form)
│   ├── icons/          # Koleksi Icon Nexture
│   ├── i18n/           # Internasionalisasi (ID/EN)
│   ├── lib/            # Pustaka utilitas & Layanan Klien
│   │   └── ux-analytics.ts # UX Telemetry Engine 🆕
│   ├── pages/          # Halaman aplikasi (berbasis struktur route)
│   │   ├── app/        # Halaman setelah login
│   │   │   ├── academic/     # Kurikulum, Mapel, Fase, Evaluasi
│   │   │   ├── local-context/ # Konteks Lokal
│   │   │   └── ...
│   │   └── auth/       # Login, Reset Password, MFA verification
│   ├── routes.tsx      # Konfigurasi routing dinamis
│   └── theme/          # Kustomisasi tema MUI
└── tailwind.config.js  # Konfigurasi TailwindCSS
```

---

*Membangun masa depan pendidikan Indonesia dengan antarmuka yang cerdas, cepat, dan inklusif.* 🇮🇩