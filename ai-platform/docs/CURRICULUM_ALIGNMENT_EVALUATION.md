# Evaluasi Alignment Kurikulum - AI Platform

## Ringkasan Eksekutif

AI Platform secara **umum align dengan Kurikulum Merdeka**, namun terdapat **2 isu legacy** yang perlu diperbaiki untuk menghilangkan referensi ke kurikulum lama (K13).

---

## Status Alignment

### ✅ Kurikulum Merdeka (Mayoritas Codebase)

**Terminologi Kurikulum Merdeka yang digunakan:**
- **CP** (Capaian Pembelajaran) - 96 referensi di 31 file
- **ATP** (Alur Tujuan Pembelajaran) - 96 referensi di 31 file
- **Phase/Fase** (A, B, C, D) - 301 referensi di 55 file
- **Capaian Pembelajaran** - 32 referensi di 11 file
- **Alur Tujuan Pembelajaran** - 32 referensi di 11 file

**Struktur Dokumen Kurikulum Merdeka:**
- `cp` - Capaian Pembelajaran
- `atp` - Alur Tujuan Pembelajaran
- `buku_guru` - Buku Guru
- `buku_siswa` - Buku Siswa
- `modul_ajar` - Modul Ajar
- `asesmen` - Asesmen
- `p5` - Projek Penguatan Profil Pelajar Pancasila

**Struktur Kompetensi Kurikulum Merdeka:**
```
CP (Capaian Pembelajaran)
  ↓
ATP (Alur Tujuan Pembelajaran)
  ↓
Learning Objective (Tujuan Pembelajaran)
  ↓
Activity (Aktivitas)
  ↓
Assessment (Asesmen)
```

**Struktur Fase Kurikulum Merdeka:**
- **Phase A**: Kelas 1-2 (Fase Fondasi)
- **Phase B**: Kelas 3-4 (Fase Pengembangan)
- **Phase C**: Kelas 5-6 (Fase Penerapan)
- **Phase D**: Kelas 7-9 (Fase Lanjutan)

---

### ❌ Isu Legacy K13 (Perlu Diperbaiki)

#### 1. Ontology File - Referensi K13

**File:** `knowledge/ontology/curriculum_ontology.json`
**Line 5:** `"description": "Ontology for Indonesian K-13 curriculum structure"`

**Masalah:**
- Deskripsi ontology menyebutkan "K-13 curriculum structure"
- Ini tidak akurat karena ontology sebenarnya menggunakan struktur Kurikulum Merdeka (CP, ATP, Phase)

**Rekomendasi Perbaikan:**
```json
{
  "ontology": {
    "name": "Indonesian Curriculum Ontology",
    "version": "1.0",
    "description": "Ontology for Indonesian Kurikulum Merdeka structure",
    ...
  }
}
```

---

#### 2. RabbitMQ Messages - Terminologi KI (Kompetensi Inti)

**File:** `shared/messaging/rabbitmq_messages.py`
**Line 115:** `competency_type: str  # KI-1, KI-2, KI-3, KI-4`

**Masalah:**
- KI (Kompetensi Inti) adalah terminologi K13
- Di Kurikulum Merdeka, tidak ada KI/KD, diganti dengan CP/ATP
- Comment ini menyesatkan dan tidak align dengan Kurikulum Merdeka

**Rekomendasi Perbaikan:**
```python
@dataclass
class ChunkCompetencyMessage(BaseMessage):
    """Message for competency-based chunking"""
    content_id: str
    content: str
    competency_type: str  # CP-based competency type
    metadata: Dict[str, Any]
```

Atau jika ingin lebih spesifik:
```python
competency_type: str  # CP code (e.g., CP-IPA-B-01)
```

---

## Detail Analisis

### Pencarian Terminologi Kurikulum

| Terminologi | Hasil Pencarian | Status |
|-------------|----------------|--------|
| KTSP | 0 hasil | ✅ Tidak ada referensi |
| K13 | 0 hasil di Python code | ✅ Tidak ada referensi di code |
| K13 | 1 hasil di JSON file | ❌ Perlu perbaikan |
| Kurikulum Merdeka | 0 hasil | ⚠️ Tidak ada referensi eksplisit |
| CP | 96 hasil di 31 file | ✅ Terminologi Kurikulum Merdeka |
| ATP | 96 hasil di 31 file | ✅ Terminologi Kurikulum Merdeka |
| Capaian Pembelajaran | 32 hasil di 11 file | ✅ Terminologi Kurikulum Merdeka |
| Alur Tujuan Pembelajaran | 32 hasil di 11 file | ✅ Terminologi Kurikulum Merdeka |
| Phase/Fase | 301 hasil di 55 file | ✅ Struktur Kurikulum Merdeka |
| KI (Kompetensi Inti) | 1 hasil di comment | ❌ Perlu perbaikan |
| KD (Kompetensi Dasar) | 0 hasil | ✅ Tidak ada referensi |

---

### Service yang Align dengan Kurikulum Merdeka

#### 1. Curriculum Engine
- **File:** `services/curriculum-engine/app/main.py`
- **Status:** ✅ Full align
- **Bukti:**
  - Menggunakan `CPStructure` dengan field `phase: str  # A, B, C, D`
  - Menggunakan `ATPStructure` dengan field `cp_id`, `phase`, `semester`
  - Validasi CP dan ATP
  - Check alignment antara CP dan ATP

#### 2. Semantic Chunk Service
- **File:** `services/semantic-chunk-service/app/chunkers/competency_chunker.py`
- **Status:** ✅ Full align
- **Bukti:**
  - Menggunakan competency indicators: 'kompetensi', 'tujuan pembelajaran', 'capaian pembelajaran'
  - Metadata termasuk `phase`, `grade`, `subject`
  - Chunk type: 'competency'

#### 3. Educational Metadata Standard
- **File:** `docs/knowledge/EDUCATIONAL_METADATA_STANDARD.md`
- **Status:** ✅ Full align
- **Bukti:**
  - Document types: cp, atp, buku_guru, buku_siswa, modul_ajar, asesmen, p5
  - Curriculum metadata: phase, grade, semester
  - Competency relationships: CP → ATP → Learning Objective → Activity → Assessment

#### 4. Knowledge Base Structure
- **File:** `knowledge/README.md`
- **Status:** ✅ Full align
- **Bukti:**
  - Direktori: cp/, atp/, buku_guru/, buku_siswa/, modul_ajar/, asesmen/, p5/
  - Semua adalah struktur Kurikulum Merdeka

---

## Perbandingan Kurikulum

### K13 vs Kurikulum Merdeka

| Aspek | K13 | Kurikulum Merdeka |
|-------|-----|-------------------|
| Kompetensi Inti | KI (4 jenis: KI-1, KI-2, KI-3, KI-4) | Tidak ada |
| Kompetensi Dasar | KD | Tidak ada |
| Capaian Pembelajaran | Tidak ada | CP (Capaian Pembelajaran) |
| Alur Tujuan Pembelajaran | Tidak ada | ATP (Alur Tujuan Pembelajaran) |
| Struktur Kelas | Per kelas | Per Fase (A, B, C, D) |
| Projek P5 | Tidak ada | P5 (Profil Pelajar Pancasila) |
| Modul Ajar | Ada tapi tidak wajib | Wajib |

---

## Rekomendasi Perbaikan

### Prioritas 1: Perbaiki Ontology File

**File:** `knowledge/ontology/curriculum_ontology.json`

**Perubahan:**
```diff
- "description": "Ontology for Indonesian K-13 curriculum structure",
+ "description": "Ontology for Indonesian Kurikulum Merdeka structure",
```

**Alasan:**
- Deskripsi saat ini tidak akurat
- Ontology menggunakan struktur Kurikulum Merdeka (CP, ATP, Phase)
- Menyebabkan kebingungan tentang kurikulum yang digunakan

---

### Prioritas 2: Perbaiki RabbitMQ Messages

**File:** `shared/messaging/rabbitmq_messages.py`

**Perubahan:**
```diff
- competency_type: str  # KI-1, KI-2, KI-3, KI-4
+ competency_type: str  # CP code (e.g., CP-IPA-B-01)
```

**Alasan:**
- KI adalah terminologi K13, tidak ada di Kurikulum Merdeka
- Comment menyesatkan developer
- Sebaiknya menggunakan CP code yang sesuai dengan Kurikulum Merdeka

---

## Kesimpulan

### Status Keseluruhan: **90% Align dengan Kurikulum Merdeka**

**Yang Sudah Align (✅):**
- Struktur CP dan ATP digunakan secara konsisten
- Struktur Fase (A, B, C, D) digunakan secara konsisten
- Tipe dokumen Kurikulum Merdeka (modul_ajar, p5) digunakan
- Tidak ada referensi ke KTSP
- Tidak ada referensi ke K13 di Python code (kecuali 2 isu legacy)
- Educational metadata standard align dengan Kurikulum Merdeka
- Knowledge base structure align dengan Kurikulum Merdeka

**Yang Perlu Diperbaiki (❌):**
1. Ontology file description - ganti "K-13" menjadi "Kurikulum Merdeka"
2. RabbitMQ messages comment - ganti referensi KI menjadi CP

### Rekomendasi Akhir

**AI Platform ini dirancang untuk Kurikulum Merdeka dan kurikulum masa depan, BUKAN untuk kurikulum lama (KTSP, K13).**

Setelah perbaikan 2 isu legacy di atas, platform akan **100% align dengan Kurikulum Merdeka** dan siap untuk digunakan dalam implementasi Kurikulum Merdeka.

---

## Action Items

### Immediate (High Priority)
- [ ] Update `knowledge/ontology/curriculum_ontology.json` line 5
- [ ] Update `shared/messaging/rabbitmq_messages.py` line 115

### Optional (Low Priority)
- [ ] Tambahkan dokumentasi eksplisit tentang Kurikulum Merdeka di README
- [ ] Tambahkan validasi untuk memastikan input menggunakan struktur Kurikulum Merdeka
- [ ] Update semua comment yang masih menggunakan terminologi generik menjadi spesifik Kurikulum Merdeka

---

## Referensi

- Kurikulum Merdeka: https://kurikulum.kemdikbud.go.id/
- Perbedaan K13 dan Kurikulum Merdeka: Dokumen resmi Kemdikbud
