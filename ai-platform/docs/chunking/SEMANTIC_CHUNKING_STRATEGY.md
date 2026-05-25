# SEMANTIC CHUNKING STRATEGY

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini menjelaskan strategi semantic chunking pada Enterprise Educational AI Platform.

Semantic chunking adalah:

```text id="semantic-definition"
core intelligence layer
```

yang menentukan:

* retrieval quality,
* context quality,
* AI accuracy,
* explainability,
* educational reasoning.

---

# Why Semantic Chunking Matters

Pada enterprise educational AI systems:

```text id="why-important"
retrieval quality > model size
```

Dan retrieval quality sangat ditentukan oleh:

* chunk boundaries,
* semantic preservation,
* metadata quality,
* educational hierarchy.

---

# Core Problem

Mayoritas RAG systems gagal karena menggunakan:

```text id="bad-chunking"
1000 character chunking
```

atau:

```text id="another-bad"
fixed token chunking
```

Akibatnya:

* konteks terpotong,
* competency rusak,
* tabel tidak utuh,
* asesmen tercampur,
* reasoning AI buruk.

---

# Core Principle

Chunking harus mengikuti:

```text id="educational-semantic"
educational semantics
```

bukan:

* jumlah karakter,
* jumlah token,
* page splitting.

---

# Chunking Goals

---

# 1. Preserve Educational Meaning

Chunk harus mempertahankan:

* tujuan pembelajaran,
* aktivitas,
* asesmen,
* inquiry,
* refleksi.

---

# 2. Preserve Hierarchy

Chunk harus menjaga:

* bab,
* subbab,
* topik,
* competency hierarchy.

---

# 3. Preserve Retrieval Relevance

Chunk harus:

* searchable,
* explainable,
* filterable.

---

# 4. Preserve Context Integrity

Jangan memotong:

* tabel,
* formula,
* rubrik,
* diagram explanation.

---

# Chunking Architecture

```text id="chunking-architecture"
Raw Document
     ↓
Layout Analysis
     ↓
Structural Segmentation
     ↓
Educational Segmentation
     ↓
Semantic Chunk Builder
     ↓
Metadata Enrichment
     ↓
Embedding Pipeline
```

---

# Chunking Stages

---

# STAGE 1 — Structural Segmentation

## Purpose

Memahami struktur dasar dokumen.

---

# Input

Dari:

* PyMuPDF
* Unstructured

---

# Detect

* title
* heading
* paragraph
* table
* figure
* formula
* list
* footer
* header

---

# Output Example

```json id="stage1-output"
{
  "type": "Heading",
  "text": "Energi Panas"
}
```

---

# STAGE 2 — Educational Segmentation

## Purpose

Mendeteksi struktur pendidikan.

---

# Detect

* competency
* activity
* experiment
* reflection
* assessment
* inquiry
* instruction
* explanation

---

# Output Example

```json id="stage2-output"
{
  "segment_type": "activity",
  "title": "Percobaan Energi Panas"
}
```

---

# STAGE 3 — Semantic Grouping

## Purpose

Menggabungkan content menjadi educational semantic units.

---

# Rules

Chunk harus:

* coherent,
* meaningful,
* self-contained.

---

# Example

## BAD

```text id="bad-example"
"...siswa mengamati..."
"...energi panas berasal..."
```

terpisah.

---

## GOOD

```text id="good-example"
Activity:
Siswa mengamati perpindahan panas...
```

utuh.

---

# STAGE 4 — Metadata Attachment

## Purpose

Menambahkan educational metadata.

---

# Metadata Examples

```json id="metadata-example"
{
  "subject": "IPA",
  "grade": 4,
  "phase": "B",
  "topic": "Energi",
  "chunk_type": "activity",
  "difficulty": "easy"
}
```

---

# Educational Chunk Types

---

# 1. Concept Chunk

## Purpose

Penjelasan konsep.

---

# Example

```text id="concept-example"
Energi panas adalah...
```

---

# Retrieval Priority

HIGH

---

# 2. Activity Chunk

## Purpose

Aktivitas pembelajaran.

---

# Example

```text id="activity-example"
Siswa melakukan percobaan...
```

---

# Retrieval Priority

VERY HIGH

Karena aktivitas sangat penting untuk:

* guru,
* lesson planning,
* inquiry learning.

---

# 3. Assessment Chunk

## Purpose

Evaluasi pembelajaran.

---

# Example

```text id="assessment-example"
Jawablah pertanyaan berikut...
```

---

# 4. Competency Chunk

## Purpose

CP / ATP / learning objective.

---

# Example

```text id="competency-example"
Peserta didik mampu memahami...
```

---

# 5. Reflection Chunk

## Purpose

Refleksi pembelajaran.

---

# 6. Experiment Chunk

## Purpose

Eksperimen atau praktikum.

---

# 7. Table Chunk

## Purpose

Preserve educational tables.

---

# Important Rule

Tabel tidak boleh dipotong.

---

# 8. Formula Chunk

## Purpose

Preserve mathematical semantics.

---

# 9. Diagram Chunk

## Purpose

Preserve image explanation.

---

# Hierarchical Chunking

---

# Purpose

Menjaga struktur kurikulum.

---

# Example Hierarchy

```text id="hierarchy-example"
Subject
 └── Chapter
      └── Topic
           └── Activity
                └── Assessment
```

---

# Required Metadata

Semua chunk wajib memiliki:

```json id="required-metadata"
{
  "chunk_id": "uuid",
  "document_id": "uuid",
  "subject": "IPA",
  "grade": 4,
  "phase": "B",
  "topic": "Energi",
  "chunk_type": "activity"
}
```

---

# Chunk Size Strategy

---

# Rules

Chunk size mengikuti:

* semantic boundary,
* educational meaning.

Bukan:

* fixed token.

---

# Recommended Size

| Chunk Type | Recommended Size     |
| ---------- | -------------------- |
| Concept    | 300–800 tokens       |
| Activity   | 500–1200 tokens      |
| Assessment | 200–600 tokens       |
| Table      | full table           |
| Formula    | full formula context |

---

# Chunk Overlap Strategy

---

# Purpose

Menjaga continuity context.

---

# Rules

Gunakan overlap:

* antar paragraph,
* antar activity,
* antar concept.

---

# Recommended Overlap

| Content Type | Overlap |
| ------------ | ------- |
| Concept      | 10–15%  |
| Activity     | 15–20%  |
| Assessment   | 5–10%   |

---

# Table Chunking Rules

---

# DO NOT

❌ split row

❌ split rubric

❌ split competency matrix

---

# DO

✅ preserve full table

✅ preserve headers

✅ preserve relationships

---

# Formula Chunking Rules

---

# Rules

Formula harus:

* preserve notation,
* preserve explanation,
* preserve surrounding context.

---

# Example

```text id="formula-example"
F = m × a
```

harus include:

* explanation,
* unit,
* context.

---

# Image & Diagram Chunking

---

# Rules

Image harus punya:

* caption,
* semantic explanation,
* surrounding context.

---

# Example Metadata

```json id="image-metadata"
{
  "image_type": "diagram",
  "caption": "Perpindahan panas"
}
```

---

# Curriculum-Aware Chunking

---

# Purpose

Membuat retrieval sesuai kurikulum.

---

# Detect

* CP
* ATP
* subject
* phase
* grade
* topic
* subtopic

---

# Example

```json id="curriculum-aware"
{
  "phase": "B",
  "grade": 4,
  "subject": "IPA"
}
```

---

# Chunk Relationships

---

# Purpose

Membuat educational graph.

---

# Relationships

```text id="chunk-relationships"
activity → competency
assessment → topic
experiment → concept
reflection → activity
```

---

# Multi-Modal Chunking

---

# Supported Types

* text
* table
* image
* formula
* diagram

---

# Multi-Embedding Strategy

Setiap chunk dapat memiliki:

* text embedding,
* image embedding,
* formula embedding.

---

# Chunk Storage Schema

## Recommended Structure

```json id="storage-schema"
{
  "chunk_id": "uuid",
  "chunk_type": "activity",
  "content": "...",
  "metadata": {},
  "relationships": [],
  "embeddings": {}
}
```

---

# Chunking Quality Metrics

---

# Required Metrics

| Metric               | Purpose              |
| -------------------- | -------------------- |
| chunk_coherence      | semantic integrity   |
| retrieval_relevance  | retrieval quality    |
| context_completeness | context preservation |
| overlap_quality      | continuity quality   |

---

# Chunking Failure Examples

---

# BAD — Fixed Character Split

```text id="failure-example-1"
"...energi panas dapat..."
```

terpotong.

---

# BAD — Table Split

Rubrik assessment rusak.

---

# BAD — Formula Isolation

Formula tanpa explanation.

---

# GOOD Chunk Characteristics

---

# Good Chunk Should Be

✅ self-contained

✅ semantically coherent

✅ educationally meaningful

✅ retrieval-friendly

✅ metadata-rich

---

# Recommended Technologies

---

# Structural Parsing

* PyMuPDF
* Unstructured

---

# Table Extraction

* Camelot

---

# Formula OCR

* Nougat

---

# Embeddings

* BGE-M3
* multilingual-e5-large

---

# Retrieval Integration

Chunk metadata wajib compatible dengan:

* Qdrant filters,
* retrieval pipelines,
* reranking systems.

---

# Observability Requirements

Chunk pipeline wajib:

* traceable,
* replayable,
* monitorable.

---

# Required Logs

* chunk generation logs,
* chunk failure logs,
* chunk quality metrics.

---

# Governance Requirements

Chunk wajib:

* explainable,
* traceable ke source,
* reproducible.

---

# Most Important Insight

Semantic chunking bukan preprocessing biasa.

Semantic chunking adalah:

```text id="most-important-insight"
knowledge engineering layer
```

yang menentukan:

* retrieval intelligence,
* AI reasoning quality,
* educational understanding.

Dan pada enterprise educational AI systems:

```text id="final-insight"
semantic chunking lebih penting daripada model AI paling mahal
```
