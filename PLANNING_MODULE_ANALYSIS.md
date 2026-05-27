# Analisis Modul Perencanaan Strategis & Kurikulum (Planning)

## Ringkasan Eksekutif

Modul Perencanaan Strategis & Kurikulum (Planning) menjadi rujukan utama dalam penyelenggaraan pendidikan di satuan pendidikan. Berikut adalah analisis implementasi fitur-fitur modul ini di frontend, backend, dan ai-platform.

---

## Status Implementasi Fitur

### 1. Fitur Analisis Karakteristik Digital

**Deskripsi:** Alat untuk melakukan analisis SWOT, Root Cause, atau Fishbone diagram untuk memetakan potensi daerah, kebutuhan murid, dan kondisi sarana prasarana.

| Komponen | Frontend | Backend | AI Platform | Status |
|----------|----------|---------|-------------|--------|
| SWOT Analysis | ❌ Tidak ditemukan | ❌ Tidak ditemukan | ❌ Tidak ditemukan | **BELUM DIIMPLEMENTASI** |
| Root Cause Analysis | ❌ Tidak ditemukan | ❌ Tidak ditemukan | ❌ Tidak ditemukan | **BELUM DIIMPLEMENTASI** |
| Fishbone Diagram | ❌ Tidak ditemukan | ❌ Tidak ditemukan | ❌ Tidak ditemukan | **BELUM DIIMPLEMENTASI** |

**Rekomendasi:**
- Fitur ini sepenuhnya belum diimplementasi di ketiga platform
- Perlu pengembangan dari awal untuk analisis SWOT, Root Cause, dan Fishbone
- Bisa diintegrasikan dengan AI Platform untuk analisis berbasis AI

---

### 2. Inventory Akar Masalah (Integrasi Rapor Pendidikan)

**Deskripsi:** Fitur sinkronisasi data Rapor Pendidikan untuk identifikasi masalah literasi/numerasi dan penentuan "Kegiatan Benahi" secara otomatis.

| Komponen | Frontend | Backend | AI Platform | Status |
|----------|----------|---------|-------------|--------|
| Rapor Pendidikan Integration | ⚠️ Partial (gradebook) | ❌ Tidak ditemukan | ❌ Tidak ditemukan | **BELUM LENGKAP** |
| Literasi/Numerasi Issues | ⚠️ Partial (reading-literacy) | ✅ Ada (foundational skills) | ❌ Tidak ditemukan | **PARTIAL** |
| Kegiatan Benahi (Otomatis) | ❌ Tidak ditemukan | ❌ Tidak ditemukan | ❌ Tidak ditemukan | **BELUM DIIMPLEMENTASI** |

**Detail Implementasi:**

**Frontend:**
- `src/pages/app/reports/gradebook/scores/page.tsx` - Gradebook reports (55 matches)
- `src/pages/app/academic/reading-literacy/page.tsx` - Reading literacy page
- `src/pages/app/academic/reading-literacy/progression/page.tsx` - Literacy progression
- `src/pages/app/academic/foundational-skills/page.tsx` - Foundational skills

**Backend:**
- `internal/reading_literacy/handler.go` - Reading literacy handler (11 matches)
- `internal/foundational_skills/model.go` - Foundational skills model (14 matches)
- `migrations/000024_create_foundational_skills_tables.up.sql` - Database schema

**Rekomendasi:**
- Rapor Pendidikan integration belum lengkap
- Literasi/numerasi sudah ada tapi belum terintegrasi dengan Rapor Pendidikan
- Fitur "Kegiatan Benahi" otomatis belum diimplementasi
- Perlu integrasi dengan API Rapor Pendidikan Kemdikbud

---

### 3. Penyusun Kurikulum Satuan Pendidikan (KSP)

**Deskripsi:** Ruang kolaborasi untuk merumuskan visi, misi, dan tujuan yang selaras dengan 8 dimensi profil lulusan.

| Komponen | Frontend | Backend | AI Platform | Status |
|----------|----------|---------|-------------|--------|
| KSP Builder | ✅ Ada | ✅ Ada | ⚠️ Partial (docs) | **DIIMPLEMENTASI** |
| Vision/Mission/Goals | ✅ Ada | ✅ Ada | ❌ Tidak ditemukan | **DIIMPLEMENTASI** |
| 8 Dimensi Profil Lulusan | ✅ Ada | ✅ Ada | ❌ Tidak ditemukan | **DIIMPLEMENTASI** |

**Detail Implementasi:**

**Frontend:**
- `src/pages/app/academic/ksp/page.tsx` - KSP list page (82 matches)
- `src/pages/app/academic/ksp/details/page.tsx` - KSP details page (18 matches)
- `src/pages/app/academic/dimensions/page.tsx` - Profile dimensions page (2 matches)
- `src/pages/app/profile/vision/page.tsx` - Vision page
- `src/pages/app/profile/mission/page.tsx` - Mission page

**Backend:**
- `internal/curriculum/handler.go` - Curriculum handler (1 match)
- `internal/curriculum/service.go` - Curriculum service
- `internal/curriculum/repository.go` - Curriculum repository
- `internal/curriculum/model.go` - Curriculum model
- `internal/profile_dimension/handler.go` - Profile dimension handler (2 matches)
- `internal/profile_dimension/service.go` - Profile dimension service (2 matches)
- `internal/profile_dimension/model.go` - Profile dimension model
- `migrations/000022_update_profile_dimensions.up.sql` - Profile dimensions migration (3 matches)

**AI Platform:**
- Documentation mentions KSP (50 matches in 13 files)
- No specific AI services for KSP generation

**Rekomendasi:**
- KSP sudah diimplementasi dengan baik di frontend dan backend
- 8 dimensi profil lulusan sudah ada
- Vision dan mission sudah ada
- Bisa diintegrasikan dengan AI Platform untuk generasi visi/misi otomatis

---

### 4. Manajemen Alur Tujuan Pembelajaran (ATP)

**Deskripsi:** Bank data untuk mengadaptasi dan memodifikasi ATP dan perangkat ajar dari pusat agar sesuai konteks sekolah.

| Komponen | Frontend | Backend | AI Platform | Status |
|----------|----------|---------|-------------|--------|
| ATP Builder | ✅ Ada | ✅ Ada | ✅ Ada | **DIIMPLEMENTASI** |
| ATP Adaptation | ✅ Ada | ✅ Ada | ✅ Ada | **DIIMPLEMENTASI** |
| Teaching Materials Bank | ⚠️ Partial | ✅ Ada | ✅ Ada | **PARTIAL** |

**Detail Implementasi:**

**Frontend:**
- `src/pages/app/academic/curriculum/flow/page.tsx` - ATP flow page (40 matches)
- `src/pages/app/academic/deep-learning/page.tsx` - Deep learning page (4 matches)
- `src/pages/app/learning/lesson-plans/page.tsx` - Lesson plans page (25 matches)

**Backend:**
- `internal/learning/handler.go` - Learning handler (23 matches)
- `internal/learning/service.go` - Learning service (28 matches)
- `internal/learning/model.go` - Learning model (22 matches)
- `internal/learning/dto.go` - Learning DTO (16 matches)
- `internal/learning/repository.go` - Learning repository (8 matches)
- `internal/lesson_planning/service.go` - Lesson planning service (7 matches)
- `migrations/000041_enhance_atp_table.up.sql` - ATP table migration (27 matches)
- `migrations/000043_create_lesson_planning_tables.up.sql` - Lesson planning tables

**AI Platform:**
- `services/curriculum-engine/app/main.py` - Curriculum engine (85 matches)
- `services/curriculum-engine/app/grpc_server.py` - Curriculum gRPC server (32 matches)
- `services/curriculum-engine/app/consumer.py` - Curriculum consumer (16 matches)
- CPStructure and ATPStructure models
- CP and ATP validation
- CP/ATP alignment checking

**Rekomendasi:**
- ATP sudah diimplementasi dengan sangat baik di ketiga platform
- AI Platform menyediakan validation dan alignment checking untuk CP/ATP
- Teaching materials bank perlu diperluas di frontend

---

### 5. Penjadwalan & Alokasi JP

**Deskripsi:** Pengaturan muatan kurikulum (Intrakurikuler, Kokurikuler, dan Ekstrakurikuler) serta manajemen beban belajar tahunan.

| Komponen | Frontend | Backend | AI Platform | Status |
|----------|----------|---------|-------------|--------|
| Intrakurikuler | ✅ Ada | ✅ Ada | ❌ Tidak ditemukan | **DIIMPLEMENTASI** |
| Kokurikuler | ✅ Ada | ✅ Ada | ❌ Tidak ditemukan | **DIIMPLEMENTASI** |
| Ekstrakurikuler | ✅ Ada | ✅ Ada | ❌ Tidak ditemukan | **DIIMPLEMENTASI** |
| Alokasi JP | ⚠️ Partial | ✅ Ada | ❌ Tidak ditemukan | **PARTIAL** |
| Beban Belajar Tahunan | ❌ Tidak ditemukan | ✅ Ada | ❌ Tidak ditemukan | **BELUM LENGKAP** |

**Detail Implementasi:**

**Frontend:**
- `src/pages/app/academic/curriculum/intrakurikuler/page.tsx` - Intrakurikuler page (3 matches)
- `src/pages/app/academic/curriculum/kokurikuler/page.tsx` - Kokurikuler page (3 matches)
- `src/pages/app/academic/curriculum/ekstrakurikuler/page.tsx` - Ekstrakurikuler page
- `src/pages/app/academic/curriculum/data.ts` - Curriculum data (2 matches)
- `src/pages/app/learning/lesson-plans/page.tsx` - Lesson plans with JP allocation (25 matches)

**Backend:**
- `internal/curriculum/handler.go` - Curriculum handler (55 matches for curriculum types)
- `internal/curriculum/service.go` - Curriculum service (36 matches)
- `internal/curriculum/repository.go` - Curriculum repository (26 matches)
- `internal/curriculum/model.go` - Curriculum model (19 matches)
- `internal/lesson_planning/service.go` - Lesson planning service (7 matches)
- `internal/lesson_planning/model.go` - Lesson planning model
- `migrations/000027_add_curriculum_type_classification.up.sql` - Curriculum type classification (28 matches)

**AI Platform:**
- Tidak ada implementasi spesifik untuk penjadwalan dan alokasi JP

**Rekomendasi:**
- Intrakurikuler, Kokurikuler, Ekstrakurikuler sudah diimplementasi
- Alokasi JP perlu diperluas di frontend
- Beban belajar tahunan belum ada di frontend
- AI Platform belum terlibat dalam penjadwalan

---

## Matriks Implementasi Lengkap

| Fitur | Frontend | Backend | AI Platform | Status Keseluruhan |
|-------|----------|---------|-------------|-------------------|
| Analisis SWOT | ❌ | ❌ | ❌ | **BELUM DIIMPLEMENTASI** |
| Root Cause Analysis | ❌ | ❌ | ❌ | **BELUM DIIMPLEMENTASI** |
| Fishbone Diagram | ❌ | ❌ | ❌ | **BELUM DIIMPLEMENTASI** |
| Rapor Pendidikan Integration | ⚠️ Partial | ❌ | ❌ | **BELUM LENGKAP** |
| Literasi/Numerasi Issues | ⚠️ Partial | ✅ | ❌ | **PARTIAL** |
| Kegiatan Benahi Otomatis | ❌ | ❌ | ❌ | **BELUM DIIMPLEMENTASI** |
| KSP Builder | ✅ | ✅ | ⚠️ Partial | **DIIMPLEMENTASI** |
| Vision/Mission/Goals | ✅ | ✅ | ❌ | **DIIMPLEMENTASI** |
| 8 Dimensi Profil Lulusan | ✅ | ✅ | ❌ | **DIIMPLEMENTASI** |
| ATP Builder | ✅ | ✅ | ✅ | **DIIMPLEMENTASI** |
| ATP Adaptation | ✅ | ✅ | ✅ | **DIIMPLEMENTASI** |
| Teaching Materials Bank | ⚠️ Partial | ✅ | ✅ | **PARTIAL** |
| Intrakurikuler | ✅ | ✅ | ❌ | **DIIMPLEMENTASI** |
| Kokurikuler | ✅ | ✅ | ❌ | **DIIMPLEMENTASI** |
| Ekstrakurikuler | ✅ | ✅ | ❌ | **DIIMPLEMENTASI** |
| Alokasi JP | ⚠️ Partial | ✅ | ❌ | **PARTIAL** |
| Beban Belajar Tahunan | ❌ | ✅ | ❌ | **BELUM LENGKAP** |

---

## Gap Analysis

### Fitur yang Belum Diimplementasi (0%)

1. **Analisis SWOT** - Tidak ada di ketiga platform
2. **Root Cause Analysis** - Tidak ada di ketiga platform
3. **Fishbone Diagram** - Tidak ada di ketiga platform
4. **Kegiatan Benahi Otomatis** - Tidak ada di ketiga platform

### Fitur yang Belum Lengkap (Partial)

1. **Rapor Pendidikan Integration** - Hanya gradebook, belum integrasi API
2. **Literasi/Numerasi Issues** - Ada tapi belum terintegrasi dengan Rapor Pendidikan
3. **Teaching Materials Bank** - Backend dan AI Platform ada, frontend perlu diperluas
4. **Alokasi JP** - Backend ada, frontend perlu diperluas
5. **Beban Belajar Tahunan** - Backend ada, frontend belum ada

### Fitur yang Sudah Diimplementasi (100%)

1. **KSP Builder** - Frontend dan Backend lengkap
2. **Vision/Mission/Goals** - Frontend dan Backend lengkap
3. **8 Dimensi Profil Lulusan** - Frontend dan Backend lengkap
4. **ATP Builder** - Ketiga platform lengkap
5. **ATP Adaptation** - Ketiga platform lengkap
6. **Intrakurikuler** - Frontend dan Backend lengkap
7. **Kokurikuler** - Frontend dan Backend lengkap
8. **Ekstrakurikuler** - Frontend dan Backend lengkap

---

## Rekomendasi Prioritas

### Prioritas 1 (High) - Fitur Analisis Karakteristik Digital

**Action Items:**
- [ ] Implementasi SWOT Analysis di frontend
- [ ] Implementasi Root Cause Analysis di frontend
- [ ] Implementasi Fishbone Diagram di frontend
- [ ] Integrasi dengan AI Platform untuk analisis berbasis AI
- [ ] Backend API untuk menyimpan dan mengambil hasil analisis

**Estimasi:** 4-6 minggu

---

### Prioritas 2 (High) - Inventory Akar Masalah

**Action Items:**
- [ ] Integrasi API Rapor Pendidikan Kemdikbud
- [ ] Implementasi fitur "Kegiatan Benahi" otomatis
- [ ] Integrasi literasi/numerasi dengan Rapor Pendidikan
- [ ] Dashboard untuk monitoring akar masalah

**Estimasi:** 3-4 minggu

---

### Prioritas 3 (Medium) - Penyempurnaan Fitur Eksisting

**Action Items:**
- [ ] Perluas Teaching Materials Bank di frontend
- [ ] Implementasi Alokasi JP di frontend
- [ ] Implementasi Beban Belajar Tahunan di frontend
- [ ] Integrasi KSP dengan AI Platform untuk generasi visi/misi otomatis

**Estimasi:** 2-3 minggu

---

## Integrasi AI Platform

### Potensi Integrasi AI Platform untuk Modul Planning

1. **Analisis Karakteristik Digital**
   - Gunakan AI Agents Service untuk analisis SWOT
   - Gunakan Generation Service untuk rekomendasi strategi
   - Gunakan Retrieval Service untuk best practices

2. **Inventory Akar Masalah**
   - Gunakan AI Platform untuk analisis literasi/numerasi
   - Gunakan Recommendation Engine untuk "Kegiatan Benahi"
   - Gunakan Hallucination Guard untuk validasi rekomendasi

3. **KSP Builder**
   - Gunakan AI Platform untuk generasi visi/misi otomatis
   - Gunakan Curriculum Engine untuk validasi KSP
   - Gunakan Educational Intelligence untuk rekomendasi

4. **ATP Management**
   - Sudah terintegrasi dengan Curriculum Engine
   - Bisa ditambahkan AI untuk adaptasi ATP otomatis
   - Gunakan Semantic Chunking untuk perangkat ajar

5. **Penjadwalan & Alokasi JP**
   - Gunakan AI Platform untuk optimasi alokasi JP
   - Gunakan Recommendation Engine untuk distribusi beban
   - Gunakan Learning Progression untuk personalisasi

---

## Kesimpulan

**Status Keseluruhan: 60% Diimplementasi**

**Yang Sudah Diimplementasi (✅):**
- KSP Builder dengan Vision/Mission/Goals
- 8 Dimensi Profil Lulusan
- ATP Builder dan Adaptation
- Intrakurikuler, Kokurikuler, Ekstrakurikuler
- Partial: Literasi/Numerasi, Teaching Materials Bank, Alokasi JP

**Yang Belum Diimplementasi (❌):**
- Analisis SWOT, Root Cause, Fishbone
- Rapor Pendidikan Integration
- Kegiatan Benahi Otomatis
- Beban Belajar Tahunan di frontend

**Rekomendasi Utama:**
1. Prioritaskan implementasi Fitur Analisis Karakteristik Digital (SWOT, Root Cause, Fishbone)
2. Integrasi API Rapor Pendidikan untuk Inventory Akar Masalah
3. Perluas integrasi AI Platform untuk fitur-fitur planning
4. Implementasi fitur yang masih partial untuk kelengkapan

---

## Action Items Summary

### Immediate (1-2 bulan)
- [ ] Implementasi SWOT Analysis
- [ ] Implementasi Root Cause Analysis
- [ ] Implementasi Fishbone Diagram
- [ ] Integrasi API Rapor Pendidikan
- [ ] Implementasi Kegiatan Benahi Otomatis

### Short-term (2-3 bulan)
- [ ] Perluas Teaching Materials Bank di frontend
- [ ] Implementasi Alokasi JP di frontend
- [ ] Implementasi Beban Belajar Tahunan di frontend
- [ ] Integrasi KSP dengan AI Platform

### Long-term (3-6 bulan)
- [ ] Integrasi AI Platform untuk semua fitur planning
- [ ] Dashboard analisis karakteristik digital
- [ ] Monitoring dan reporting akar masalah
- [ ] Optimasi penjadwalan dengan AI
