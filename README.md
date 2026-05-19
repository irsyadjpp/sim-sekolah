# SIM Sekolah - UPT SDI Bonerate No. 85

## Ringkasan Eksekutif (Executive Summary)
SIM Sekolah adalah Sistem Informasi Manajemen terpadu yang dirancang khusus untuk memenuhi kebutuhan operasional, akademik, dan administratif di **UPT SDI Bonerate No. 85, Kepulauan Selayar**. Sistem ini hadir sebagai solusi digitalisasi pendidikan yang komprehensif, menghubungkan seluruh pemangku kepentingan—mulai dari calon siswa, orang tua, guru, hingga manajemen sekolah—ke dalam satu ekosistem digital yang aman, cepat, dan terintegrasi penuh.

## Visi Bisnis & Objektif Utama
1. **Digitalisasi *End-to-End***: Mengubah proses manual institusi (pendaftaran siswa baru, pencatatan asesmen, hingga pencetakan rapor) menjadi alur kerja digital yang efisien dan serba otomatis.
2. **Kesesuaian dengan Standar Nasional**: Struktur data dan alur kerja didesain agar sangat kompatibel dengan standar Dapodik Kementerian Pendidikan.
3. **Observabilitas & Keamanan Tingkat Enterprise**: Dibangun dengan standar keamanan tinggi yang mencakup *Multi-Factor Authentication* (MFA), enkripsi data, perlindungan akses berbasis peran (RBAC), serta pemantauan log/performa sistem secara *real-time* via Grafana/OTel.
4. **Pendidikan Berbasis Data & AI**: Menerapkan konsep *Deep Learning* dan asisten Kecerdasan Buatan (AI) untuk membantu pendidik menyusun modul ajar, memberikan umpan balik (feedback) yang personal, dan mendeteksi dini kendala belajar siswa.

---

## Arsitektur Repositori (Monorepo)
Guna menjamin konsistensi versi dan kolaborasi lintas tim yang mulus, sistem ini dikelola dalam satu repositori terpusat (*Monorepo*) yang terdiri dari tiga pilar layanan utama:

* 📁 **`/frontend`**: Aplikasi antarmuka pengguna (UI) modern berbasis React dan TypeScript. Menyediakan *User Experience* (UX) kelas atas dengan estetika premium yang responsif untuk berbagai jenis pengguna (Portal Siswa, Dasbor Guru, Panel Admin).
* 📁 **`/backend`**: *Core service* super cepat berbasis Go (Golang). Bertanggung jawab atas logika bisnis, keamanan API, integrasi basis data (PostgreSQL), manajemen *cache* & antrean (Redis), dan sistem manajemen berkas terdistribusi (RustFS).
* 📁 **`/ai-worker`**: Layanan asinkron yang menangani beban kerja berat Kecerdasan Buatan (AI), seperti ekstraksi wawasan (*insights*), pembuatan narasi deskriptif, dan pengolahan bahasa alami (*Natural Language Processing*).

---

## Alur Kerja Bisnis Utama (Core Business Flows)

Sistem ini dirancang dengan pendekatan *Workflow-First*, memastikan kelancaran operasional sekolah dari hulu ke hilir.

### 1. Alur Penerimaan Peserta Didik Baru (PPDB) & *Onboarding*
Merupakan gerbang utama bagi peserta didik baru untuk bergabung ke dalam ekosistem sekolah.
* **Pendaftaran Mandiri**: Orang tua atau wali murid mengisi formulir pendaftaran digital dan mengunggah dokumen persyaratan dasar (Akte, KK) secara online.
* **Verifikasi & Validasi**: Panitia PPDB memvalidasi dokumen secara sistemik.
* **Enrollment & Aktivasi**: Setelah dinyatakan lulus, sistem secara otomatis menerbitkan Nomor Induk Siswa (NIS), mendistribusikan siswa ke rombongan belajar (Rombel), dan mencetak kredensial masuk (akun portal) untuk siswa dan orang tua.

### 2. Alur Akademik, Kurikulum & *Deep Learning*
Memfasilitasi siklus inti kegiatan belajar mengajar sehari-hari.
* **Perencanaan (Kurikulum)**: Guru menyusun Capaian Pembelajaran (CP) dan Alur Tujuan Pembelajaran (ATP). Sistem dilengkapi dengan Asisten AI untuk mempermudah penyusunan Modul Ajar dan Modul P5 (Projek Penguatan Profil Pelajar Pancasila).
* **Pelaksanaan Kegiatan**: Pencatatan presensi kehadiran harian terpadu, pengelolaan jadwal pelajaran, serta pencatatan Jurnal Anekdotal (catatan perilaku khusus siswa).
* **Evaluasi (Asesmen)**: Input nilai formatif dan sumatif secara terpusat, memungkinkan pemantauan distribusi kognitif siswa (pemahaman LOTS hingga penalaran HOTS).

### 3. Alur Intelligence & Early Warning System (EWS)
Fitur proaktif untuk meminimalisasi angka ketertinggalan siswa dan putus sekolah.
* **Pengumpulan Data Silang**: Sistem secara pasif mengumpulkan data riwayat absensi, sentimen Jurnal Anekdotal, dan tren nilai akademik.
* **Analisis Prediktif AI**: Mesin AI akan mendeteksi anomali. Contoh: Penurunan tajam tingkat kehadiran atau akumulasi tag sentimen negatif terkait keterlambatan literasi.
* **Intervensi Cepat**: Sistem menerbitkan peringatan dini (*Alert*) langsung ke dasbor Wali Kelas dan Guru Bimbingan Konseling (BK) untuk memberikan pendampingan yang tepat sasaran dan terukur.

### 4. Alur Pelaporan Akademik (E-Rapor Terpadu)
Menutup siklus semester dengan laporan yang komprehensif, cepat, dan minim beban administratif.
* **Agregasi Otomatis**: Sistem secara otomatis menarik rekapitulasi nilai akhir, presensi total, catatan ekstrakurikuler, dan perkembangan dimensi P5.
* **Generasi Narasi AI**: Modul kecerdasan buatan menyusun kalimat deskripsi capaian akademik dan karakter untuk setiap siswa secara unik, berdasarkan data mentah yang ada.
* **Finalisasi & Distribusi Eksekutif**: Setelah melalui gerbang validasi ketat dan pengesahan (*digital sign*) dari Kepala Sekolah, E-Rapor didistribusikan dalam format digital langsung ke genggaman orang tua melalui portal mereka.

---

> *Dokumen ini memberikan pandangan strategis (*helicopter view*) dari arsitektur bisnis SIM Sekolah. Untuk panduan teknis seperti petunjuk instalasi, manajemen *environment variables*, atau *guideline* kontribusi kode, silakan merujuk pada file `README.md` spesifik yang terdapat di dalam setiap sub-direktori layanan.*
