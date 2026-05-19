# SIM Sekolah Terpadu - SD Negeri (Backend API)

Sistem Informasi Manajemen (SIM) Sekolah Terpadu adalah backend layanan mandiri (API) enterprise yang dibangun khusus untuk mengelola operasional SD Negeri (tanpa modul pembayaran). Sistem ini didesain agar sangat kompatibel dengan sinkronisasi **Dapodik**, mendukung standar rapor **Kurikulum Merdeka 2026** (termasuk Kurikulum Satuan Pendidikan - KSP), dan dilengkapi kecerdasan buatan (**AI**) berbasis **Google Gemini API** serta kapabilitas **Deep Learning** untuk membantu beban kerja administratif guru.

Aplikasi ini dibangun menggunakan bahasa pemrograman Go (Golang) versi **1.26** dengan framework **Fiber v2** yang sangat cepat dan ringan, serta didukung oleh stack enterprise modern untuk skalabilitas, caching, pengolah graf, pengolah antrean, pencarian vektor (RAG), dan *observability pipeline*.

---

## 🌟 Fitur Utama & Arsitektur Modul

Sistem ini didukung oleh arsitektur modular yang kuat:

1. **Modul Institusi & Aktor**
   - Manajemen Tahun Ajaran, Sekolah, Fase, dan Tingkat Kelas.
   - Manajemen entitas Guru (berikut auto-create User), Siswa, dan Orang Tua Siswa.

2. **Modul Manajemen Kelas & KBM**
   - Manajemen Rombongan Belajar (Classrooms) dan Wali Kelas.
   - *Enrollments* (fitur pendaftaran siswa ke rombel secara massal/Bulk).
   - *Teaching Assignments* (Penugasan Guru Mata Pelajaran per kelas).

3. **Modul Kurikulum Merdeka (KSP & Capaian Pembelajaran)**
   - Manajemen Kurikulum Satuan Pendidikan (KSP), Capaian Pembelajaran (CP), Fase, Mata Pelajaran, dan Dimensi Profil Pelajar Pancasila.

4. **Modul Konteks Lokal (Local Context Engine)**
   - Mendukung **Pembelajaran Mendalam (Deep Learning)**.
   - Manajemen konteks lingkungan, realitas sosial, budaya, potensi daerah, hingga pengalaman nyata siswa.
   - Data terstruktur untuk rekomendasi AI dan penyusunan Modul Ajar/P5 yang kontekstual.

5. **Modul Asesmen & Penilaian**
   - Pembuatan Asesmen (Formatif/Sumatif).
   - Penginputan nilai harian/ujian menggunakan metode *Bulk Upsert*.

6. **Modul Manajemen Keamanan & Autentikasi (Enterprise Grade Security) 🆕**
   - Autentikasi JWT dan HttpOnly Cookie.
   - Hak Akses Terpusat (RBAC): Super Admin, Admin Sekolah, dan Guru.
   - **MFA Engine (Multi-Factor Authentication)**: Setup TOTP (`MFA_ENABLE`) menggunakan Auth App (seperti Google Authenticator) dan verifikasi token 6-digit saat login untuk melindungi akun sekolah.
   - **Kebijakan Token Aktif**: Token otomatis kadaluarsa secara ketat di akhir pekan (*weekend*) atau hari libur guna memperkecil celah eksploitasi data luar jam kerja.

7. **Audit Log & Security Telemetry (SANGAT PENTING) 🆕**
   - **GORM Hook Trigger System**: Setiap aksi buka data, tambah, ubah, dan hapus (`READ`, `CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `MFA_ENABLE`) oleh aktor mana pun akan direkam secara otomatis oleh backend hook.
   - **Struktur Audit Logs**: Menyimpan `user_id`, `action`, `entity`, `entity_id`, `ip_address`, dan `created_at`.
   - **API Endpoint**: Menyediakan `/api/v1/system/audit-logs` untuk keperluan audit dan investigasi keamanan oleh pimpinan sekolah.

8. **Modul Rapor Kurikulum Merdeka + Deep Learning**
   - Rapor holistik: Nilai Intrakurikuler, Projek Penguatan Profil Pelajar Pancasila (P5), dan Observasi Deep Learning.

9. **Modul Integrasi AI (Google Gemini)**
   - Penulisan narasi otomatis (Catatan Wali Kelas/Deskripsi Capaian) berbasis data riil siswa menggunakan model `gemini-1.5-flash` via Google Gemini REST API.

10. **Modul PPDB SD Negeri**
    - Alur pendaftaran lengkap hingga auto-generate data siswa aktif dan NIS lokal.

11. **Modul System & Dashboard Telemetry**
    - Menyediakan endpoint telemetry dashboard khusus untuk tiga tipe user: Pimpinan, Guru, dan Operator.
    - Menghitung statistik sekolah, aktivitas rombel, serta data kesehatan hardware dan telemetri sistem.

---

## 🛠️ Stack Teknologi (Enterprise Stack)

Untuk menjamin performa tinggi dan keandalan sistem berskala produksi, backend ini dilengkapi stack modern berikut:

- **Bahasa Utama:** Go (Golang) **1.26**
- **Framework Web:** [Fiber v2](https://gofiber.io/) - untuk performa API ultra cepat dan konsumsi memori rendah.
- **Database Utama:** PostgreSQL **16.5** - DBMS Relasional tangguh untuk menyimpan data master dan operasional.
- **Object Storage:** [RustFS](https://github.com/rustfs/rustfs) - server penyimpanan file berbasis HTTP mandiri untuk menangani file dokumen & media (S3-compatible).
- **Caching & Queue:** Redis **v9** - digunakan untuk global rate limiting (menghindari serangan DDoS/abuse) serta backend *Asynchronous Queue Worker* menggunakan mekanisme List `BRPOP` untuk menangani antrean tugas latar belakang.
- **Graph Database:** Neo4j **v5** - menyimpan relasi materi pelajaran, peta kompetensi, dan graf akademik siswa.
- **Message Broker:** RabbitMQ - untuk manajemen event-driven communication dan pub-sub messages.
- **Vector Search (RAG Context):** Qdrant - database vektor untuk menunjang pencarian semantik (Semantic Search) dan context chunking data sekolah (untuk RAG modul ajar AI mendatang).
- **Observability Stack (Enterprise Monitoring) 🆕:** Integrasi penuh **OpenTelemetry (OTel)** dan terstruktur JSON logging. Alur log dialirkan secara terpusat melalui OTel Collector menuju Loki, Tempo, dan dashboard Grafana untuk melacak performa, trace database, dan query bermasalah (*Slow Queries*).
- **Database Migrator:** `golang-migrate/migrate/v4` - mengelola migrasi skema database secara terstruktur, sekuensial, dan versioned.

---

## 🚀 Panduan Instalasi & Menjalankan Aplikasi

### 1. Prasyarat Sistem
Pastikan servis-servis berikut terpasang atau dapat diakses:
- **Go** versi 1.26 atau lebih tinggi.
- **PostgreSQL 16+**
- **Redis v9**
- **Neo4j v5** (Community Edition)
- **RabbitMQ**
- **RustFS** (untuk media storage)
- **OpenTelemetry Collector** (jika ingin melacak trace/logs di Grafana Cloud)

> [!TIP]
> Seluruh database pendukung (PostgreSQL, Neo4j, Qdrant, RustFS, OTel Collector) dapat dijalankan dengan sangat mudah menggunakan Docker Compose yang telah disediakan di root workspace:
> ```bash
> docker-compose up -d
> ```

### 2. Kloning Repositori & Install Dependensi
Buka terminal pada direktori `backend` lalu jalankan perintah berikut:
```bash
go mod tidy
```

### 3. Konfigurasi Environment (File `.env`)
Salin file `.env.example` menjadi `.env` di folder `backend`:
```bash
cp .env.example .env
```
Sesuaikan nilai variabel berikut dengan kebutuhan lingkungan Anda. Berikut adalah isi konfigurasi standarnya:

```env
# APP & SERVER
APP_NAME="SIM Sekolah Terpadu"
APP_ENV=development
APP_PORT=8080
APP_DEBUG=true
SERVER_HOST=0.0.0.0
SERVER_PORT=8080

# DATABASE - POSTGRESQL
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=password123
DB_NAME=sim_sekolah_terpadu
DB_SSLMODE=disable
DB_TIMEZONE=Asia/Jakarta
DATABASE_URL=postgres://admin:password123@localhost:5432/sim_sekolah_terpadu?sslmode=disable

# JWT AUTHENTICATION & SECURITY
JWT_SECRET=4f9d7c2b1a8e6f5d9c3b7e1a2f4c8d6e9b1f3a7c5d8e2f6a1b9c4d7e8f2a6c1
JWT_EXPIRE_HOUR=72
BCRYPT_COST=12
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:5173,http://localhost:5174

# REDIS CACHE & QUEUE
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=password123
REDIS_DB=0

# RABBITMQ BROKER
RABBITMQ_URL=amqp://user:password123@localhost:5672/

# NEO4J GRAPH DB
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123

# RUSTFS STORAGE
RUSTFS_URL=http://localhost:9000

# LOGGING
LOG_LEVEL=debug
```

### 4. Eksekusi Database Migration
Aplikasi SIM Sekolah telah beralih sepenuhnya ke **Versioned Migrations** terotomatisasi. 

> [!IMPORTANT]
> **Tidak perlu lagi menjalankan `ddl.sql` secara manual!** 
> Saat backend server pertama kali dinyalakan, modul migrasi Go akan otomatis membaca file migration yang ada di folder `/migrations` dan mengaplikasikannya secara aman dan *idempotent* ke database PostgreSQL.
>
> Selain itu, aplikasi juga otomatis menjalankan inisialisasi system views dan dynamic seed data saat startup.

### 5. Generate Swagger (Jika melakukan perubahan rute)
Untuk memperbarui dokumentasi API terintegrasi setelah memodifikasi routing atau dokumentasi Swagger annotations:
```bash
swag init -g cmd/main.go --parseDependency --parseInternal
```

### 6. Jalankan Server!
Untuk menjalankan server secara lokal:
```bash
go run cmd/main.go
```
Saat berhasil berjalan:
- API Server akan mendengarkan di: `http://localhost:8080`
- Background Redis Queue Worker akan otomatis menyala untuk mengolah async jobs secara paralel.

---

## 📚 Dokumentasi API Terintegrasi

Backend didukung dokumentasi Swagger interaktif yang diperbarui otomatis. Setelah server berjalan, buka browser dan kunjungi:

👉 **[http://localhost:8080/swagger/index.html](http://localhost:8080/swagger/index.html)**

**Fitur Swagger:**
- Mengetes langsung seluruh endpoint (*Try it out*).
- Menyediakan otentikasi JWT Bearer token via tombol **Authorize** di pojok kanan atas. Format input: `Bearer <token_jwt_anda>`.

---

## 🏗️ Struktur Direktori (*Clean Architecture*)

Aplikasi dirancang dengan struktur bersih dan modular untuk memudahkan pemeliharaan jangka panjang:

```
backend/
├── cmd/
│   └── main.go                 # Entry point aplikasi utama (Setup database, redis, worker, & routing)
├── config/
│   ├── config.yaml             # Konfigurasi default aplikasi (Viper)
│   ├── database.go             # Konektor Postgresql (GORM)
│   ├── migrate.go              # Runner golang-migrate
│   ├── redis.go                # Konektor Redis Client
│   ├── neo4j.go                # Konektor Neo4j Driver
│   ├── rabbitmq.go             # Konektor RabbitMQ
│   └── viper.go                # Loader konfigurasi dinamis (Viper + Env Bind)
├── internal/                   # Direktori modul-modul bisnis (Domain Logic)
│   ├── academic_year/          # Manajemen Tahun Ajaran
│   ├── ai/                     # Integrasi AI Google Gemini
│   ├── assessment/             # Manajemen Asesmen & Nilai
│   ├── auth/                   # Autentikasi JWT, MFA & Role Check
│   ├── classroom/              # Manajemen Rombel (Kelas)
│   ├── cp/                     # Capaian Pembelajaran (Kurikulum Merdeka)
│   ├── deep_learning/          # Observasi & Deep Learning siswa
│   ├── enrollment/             # Pendaftaran murid massal ke Rombel
│   ├── ksp/                    # Kurikulum Satuan Pendidikan
│   ├── learning/               # Rencana & Aktivitas Pembelajaran
│   ├── local_context/          # Konteks Lokal engine
│   ├── ppdb/                   # Penerimaan Peserta Didik Baru (PPDB)
│   ├── report/                 # Modul Rapor Kurikulum Merdeka
│   ├── school/                 # Profil Sekolah & Embedding Trigger
│   ├── student/                # Manajemen Siswa & RAG context
│   ├── system/                 # Telemetry Dashboard, Audit Logs, Seeder & Redis Async Queue
│   ├── teacher/                # Manajemen Guru & Penugasan
│   └── user/                   # Manajemen Admin User
├── migrations/                 # File migrasi terstruktur (golang-migrate sql files)
│   ├── 000001_init_schema.up.sql
│   ├── 000002_seed_master_data.up.sql
│   └── 000003_seed_auth.up.sql
├── pkg/                        # Utility & Global Packages (Reusable helper)
│   ├── logger/                 # Enterprise OpenTelemetry Logger & Tracing Middleware
│   └── middleware/             # HTTP Route Protections (JWT auth)
├── routes/
│   └── routes.go               # Router aggregator yang menggabungkan seluruh modul
├── go.mod                      # File definisi module Go (Go 1.26)
├── ddl.sql                     # [DEPRECATED] Skema DDL legacy (sebagai referensi schema awal)
└── Dockerfile                  # Konstruksi container production
```

---

*Dikembangkan khusus untuk mendukung majunya pendidikan Indonesia berbasis teknologi modern skala enterprise.* 🇮🇩
