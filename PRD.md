Berikut adalah draf *Product Requirements Document* (PRD) dan Desain Database tingkat tinggi (High-Level Database Design) untuk membangun fitur tersebut.

---

# 📄 PRODUCT REQUIREMENTS DOCUMENT (PRD)

**Produk:** Fitur Analisis Karakteristik Digital (Modul Perencanaan Strategis SD)
**Status:** Draft / Proposed
**Fokus Utama:** Memfasilitasi Perencanaan Berbasis Data untuk Penyusunan Kurikulum Satuan Pendidikan (KSP).

## 1. Visi & Objektif

Membangun instrumen analitik digital yang intuitif bagi Kepala Sekolah dan Tim Kerja SD untuk memetakan kondisi internal/eksternal sekolah secara berbasis bukti (data-driven), sehingga menghasilkan visi, misi, program, dan Kurikulum Satuan Pendidikan (KSP) yang sangat kontekstual.

## 2. Aktor / User Roles

* **Kepala Sekolah:** Pemilik proyek (Project Owner), penyetuju draf, dan pengguna dashboard utama.
* **Tim Kerja (Guru/Staf):** Kontributor data, fasilitator FGD, analis masalah, dan penyusun KSP.
* **Responden (Murid, Orang Tua, Mitra):** Pengguna dengan akses terbatas hanya untuk mengisi kuesioner digital.

## 3. Kebutuhan Fungsional (Functional Requirements - FR)

### FR 1: Modul Pengumpulan Data Digital (Data Ingestion)

* **FR 1.1 Kuesioner Digital Dinamis:** Sistem memiliki pembuat *form* (seperti Google Forms) dengan templat bawaan untuk survei pemetaan sarpras, minat/bakat murid, dan masukan orang tua.
* **FR 1.2 Integrasi API Rapor Pendidikan:** Sistem dapat menarik data JSON/XML dari Rapor Pendidikan Kemdikbudristek (berdasarkan NPSN) untuk menampilkan indikator capaian literasi, numerasi, dan karakter secara otomatis.
* **FR 1.3 Modul FGD Virtual:** Fitur penjadwalan FGD, penyediaan *link* *conference*, dan kolaborasi *real-time* untuk mencatat notulensi, catatan anekdotal, serta sentimen warga sekolah.

### FR 2: Modul Pemetaan Karakteristik (Mapping Dashboard)

* **FR 2.1 Pemetaan Potensi Daerah:** Form isian terstruktur untuk menginventarisasi kekhasan daerah (sosial, budaya, industri, alam).
* **FR 2.2 Profiling Kebutuhan Murid:** Dasbor yang mengagregasi hasil kuesioner murid menjadi data statistik (contoh: *pie chart* persentase murid dengan intensitas penggunaan gawai tinggi untuk rekomendasi dimensi Penalaran Kritis).
* **FR 2.3 Inventarisasi Sarpras & IT:** *Checklist* kondisi fisik dan infrastruktur digital untuk menilai kesiapan sekolah dalam implementasi Pembelajaran Mendalam, Koding, dan Kecerdasan Artifisial (KA).

### FR 3: Modul Alat Analisis (Analytical Tools)

* **FR 3.1 SWOT Builder:** Papan kanvas interaktif dengan 4 kuadran (S, W, O, T) yang memungkinkan tim kerja melakukan *drag-and-drop* kartu data dari hasil pengumpulan (FR 1 & FR 2) ke dalam kuadran yang relevan.
* **FR 3.2 Root Cause Analyzer:** Antarmuka tabular yang menghubungkan metrik Rapor Pendidikan yang merah/kuning dengan 5-Whys atau analisis sebab-akibat, diakhiri dengan kolom penetapan "Kegiatan Benahi".
* **FR 3.3 Fishbone Diagram Visualizer:** Kanvas visual *diagram tulang ikan* interaktif. Kepala masalah (akibat) berada di kanan, sementara tulang (sebab) dikategorikan menjadi Manusia, Metode, Material/Fasilitas, Lingkungan, dll.

### FR 4: Generator Kurikulum Satuan Pendidikan (KSP)

* **FR 4.1 Ekspor Dokumen:** Mengompilasi seluruh hasil analisis (SWOT, Akar Masalah, Fishbone, Profil Murid) menjadi satu draf KSP berformat PDF atau Word yang siap di- *review*.

---

# 🗄️ DATABASE DESIGN (Arsitektur Relasional)

Untuk menangani arsitektur di atas, kita akan menggunakan *Relational Database Management System* (RDBMS) seperti PostgreSQL. Berikut adalah struktur tabel inti (Core Tables).

### 1. Tabel Inti & Pengguna

| Nama Tabel | Kolom | Tipe Data | Deskripsi |
| --- | --- | --- | --- |
| `schools` | `id` (PK), `npsn`, `name`, `address` | UUID, VARCHAR | Data master sekolah SD. |
| `users` | `id` (PK), `school_id` (FK), `role`, `name` | UUID, VARCHAR | `role`: 'kepsek', 'guru', 'responden'. |

### 2. Pengumpulan Data & Rapor

| Nama Tabel | Kolom | Tipe Data | Deskripsi |
| --- | --- | --- | --- |
| `rapor_pendidikan` | `id` (PK), `school_id` (FK), `year`, `literacy_score`, `numeracy_score`, `raw_data` | UUID, INT, FLOAT, JSONB | Menyimpan data tarikan API Rapor Pendidikan (*raw_data* untuk JSON utuh). |
| `surveys` | `id` (PK), `school_id` (FK), `target_audience`, `title`, `status` | UUID, VARCHAR | `target_audience`: 'murid', 'ortu', 'mitra'. |
| `survey_responses` | `id` (PK), `survey_id` (FK), `respondent_id`, `answers_json` | UUID, UUID, JSONB | Jawaban dari kuesioner. Menggunakan JSONB agar fleksibel. |
| `fgd_sessions` | `id` (PK), `school_id` (FK), `topic`, `date`, `conclusions` | UUID, VARCHAR, DATE, TEXT | Rekapitulasi hasil FGD. |

### 3. Pemetaan Karakteristik

| Nama Tabel | Kolom | Tipe Data | Deskripsi |
| --- | --- | --- | --- |
| `mapping_potensi` | `id` (PK), `school_id` (FK), `category`, `description`, `learning_potential` | UUID, VARCHAR, TEXT, TEXT | `category`: 'budaya', 'alam', 'industri'. |
| `mapping_sarpras` | `id` (PK), `school_id` (FK), `facility_name`, `condition`, `digital_ready` | UUID, VARCHAR, VARCHAR, BOOLEAN | Mendata kesiapan fisik & digital (Koding/KA). |
| `student_needs` | `id` (PK), `school_id` (FK), `profil_dimensi`, `current_status`, `action_plan` | UUID, VARCHAR, TEXT, TEXT | Pemetaan profil lulusan (misal: 'Penalaran Kritis'). |

### 4. Modul Alat Analisis

| Nama Tabel | Kolom | Tipe Data | Deskripsi |
| --- | --- | --- | --- |
| `swot_items` | `id` (PK), `school_id` (FK), `quadrant`, `statement`, `source_data_id` | UUID, ENUM, TEXT, UUID | `quadrant`: 'S','W','O','T'. |
| `root_causes` | `id` (PK), `school_id` (FK), `rapor_metric_id`, `identified_problem`, `root_cause`, `kegiatan_benahi` | UUID, UUID, TEXT, TEXT, TEXT | Menghubungkan masalah di rapor dengan kegiatan perbaikan. |
| `fishbone_diagrams` | `id` (PK), `school_id` (FK), `head_effect` | UUID, TEXT | Masalah utama yang dianalisis. |
| `fishbone_nodes` | `id` (PK), `diagram_id` (FK), `bone_category`, `cause_text` | UUID, UUID, VARCHAR, TEXT | `bone_category`: 'Manusia', 'Fasilitas', dll. |

### 5. Hasil Akhir (Output)

| Nama Tabel | Kolom | Tipe Data | Deskripsi |
| --- | --- | --- | --- |
| `ksp_documents` | `id` (PK), `school_id` (FK), `academic_year`, `generated_at`, `status`, `file_url` | UUID, VARCHAR, TIMESTAMP, VARCHAR, TEXT | Dokumen akhir yang siap diunduh/ditinjau. Status: 'draft', 'approved'. |

---
