# DOCUMENT INGESTION PIPELINE

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini menjelaskan arsitektur dan strategi Document Ingestion Pipeline pada Enterprise Educational AI Platform.

Pipeline ini bertanggung jawab untuk:

* menerima dokumen,
* memahami struktur dokumen,
* melakukan parsing,
* melakukan semantic chunking,
* enrichment metadata,
* embedding generation,
* indexing ke vector database.

---

# Core Philosophy

Document ingestion bukan sekadar:

```text id="wrong-ingestion"
upload PDF → embedding
```

Tetapi:

```text id="correct-ingestion"
document intelligence pipeline
```

yang memahami:

* struktur pendidikan,
* layout,
* tabel,
* formula,
* gambar,
* kompetensi,
* asesmen.

---

# Core Objectives

---

# 1. Educational Understanding

Pipeline harus memahami:

* CP,
* ATP,
* asesmen,
* aktivitas,
* inquiry,
* refleksi.

---

# 2. Multi-Modal Understanding

Pipeline harus mendukung:

* text,
* image,
* table,
* formula,
* diagram.

---

# 3. Retrieval Optimization

Output pipeline harus:

* retrieval-friendly,
* metadata-rich,
* explainable.

---

# 4. Enterprise Scalability

Pipeline harus:

* asynchronous,
* distributed,
* observable,
* replayable.

---

# High-Level Pipeline Architecture

```text id="high-level-ingestion-pipeline"
PDF Upload
     ↓
Upload Validation
     ↓
Storage Layer
     ↓
Document Analyzer
     ├── Text Extractor
     ├── OCR Engine
     ├── Table Extractor
     ├── Image Extractor
     └── Layout Detector
     ↓
Semantic Chunk Builder
     ↓
Metadata Enrichment
     ↓
Embedding Pipeline
     ↓
Vector Indexing
     ↓
Knowledge Store
```

---

# Pipeline Architecture Principles

---

# 1. Asynchronous by Default

Semua heavy processing:

* OCR,
* embeddings,
* indexing,
* image captioning,

harus asynchronous.

---

# 2. Event-Driven

Semua stage berkomunikasi menggunakan:

* queue,
* event contracts.

---

# 3. Replayable

Semua processing harus:

* reproducible,
* replayable,
* traceable.

---

# 4. Modular

Setiap stage:

* independent,
* scalable,
* isolated.

---

# Pipeline Stages

---

# STAGE 1 — Document Upload

## Purpose

Menerima dokumen dari:

* frontend,
* backend,
* bulk ingestion,
* admin upload.

---

# Supported Formats

## Mandatory

✅ PDF

---

# Optional

✅ DOCX

✅ PPTX

✅ image-based PDF

---

# Validation Rules

---

# Validate

✅ file size

✅ mime type

✅ malware scan

✅ corrupted file detection

---

# Reject

❌ executable file

❌ encrypted PDF tanpa izin

❌ malformed PDF

---

# Recommended Limits

| Type          | Max Size |
| ------------- | -------- |
| Standard PDF  | 100MB    |
| OCR-heavy PDF | 300MB    |

---

# Upload Metadata

## Required

```json id="upload-metadata"
{
  "document_id": "uuid",
  "document_type": "buku_guru",
  "subject": "IPA",
  "grade": 4,
  "phase": "B"
}
```

---

# Storage Strategy

---

# Raw File Storage

Gunakan:

* MinIO

---

# Folder Structure

```text id="storage-structure"
storage/
├── raw/
├── parsed/
├── OCR/
├── images/
└── embeddings/
```

---

# STAGE 2 — Upload Event

## Purpose

Memulai asynchronous ingestion pipeline.

---

# Event Example

```text id="upload-event"
DOCUMENT.UPLOAD.REQUESTED
```

---

# Payload Example

```json id="upload-payload"
{
  "document_id": "doc_001",
  "storage_path": "/raw/doc_001.pdf"
}
```

---

# Queue Recommendation

Gunakan:

* RabbitMQ
  atau
* Apache Kafka

---

# STAGE 3 — Document Analyzer

## Purpose

Memahami struktur dokumen.

---

# Architecture

```text id="document-analyzer"
Document Analyzer
 ├── Text Extractor
 ├── OCR Engine
 ├── Table Extractor
 ├── Image Extractor
 └── Layout Detector
```

---

# 3.1 Text Extractor

## Purpose

Extract:

* raw text,
* page blocks,
* coordinates.

---

# Recommended Tool

* PyMuPDF

---

# Extracted Information

```json id="text-extraction-example"
{
  "page": 1,
  "blocks": [],
  "coordinates": []
}
```

---

# 3.2 OCR Engine

## Purpose

Menangani:

* scanned PDF,
* image PDF,
* handwritten content.

---

# Recommended Tools

* Tesseract OCR
* PaddleOCR

---

# OCR Strategy

## OCR hanya jika diperlukan

Jangan OCR semua PDF.

---

# OCR Detection

Gunakan:

* text density,
* extractability score.

---

# 3.3 Table Extractor

## Purpose

Preserve:

* rubrik,
* competency matrix,
* assessment table.

---

# Recommended Tool

* Camelot

---

# Rules

Tabel tidak boleh:

* dipotong,
* di-flatten menjadi plain text.

---

# Table Output Example

```json id="table-output"
{
  "table_id": "tbl_001",
  "headers": [],
  "rows": []
}
```

---

# 3.4 Image Extractor

## Purpose

Extract:

* diagrams,
* illustrations,
* experiments,
* educational images.

---

# Recommended Tool

* PyMuPDF

---

# Output Example

```json id="image-output"
{
  "image_id": "img_001",
  "page": 5
}
```

---

# 3.5 Layout Detector

## Purpose

Memahami semantic layout.

---

# Recommended Tool

* Unstructured

---

# Detect

* title
* heading
* paragraph
* list
* table
* figure
* footer

---

# Example Output

```json id="layout-output"
{
  "type": "Title",
  "text": "Energi"
}
```

---

# STAGE 4 — Formula Extraction

## Purpose

Preserve mathematical semantics.

---

# Recommended Tool

* Nougat

---

# Why Important

Formula PDF biasa sering:

* rusak,
* kehilangan notation,
* kehilangan structure.

---

# Example Output

```json id="formula-output"
{
  "formula": "F = m × a"
}
```

---

# STAGE 5 — Semantic Chunk Builder

## Purpose

Membentuk educational semantic chunks.

---

# Chunking Must Be

✅ curriculum-aware

✅ semantic-aware

✅ hierarchy-aware

---

# Chunk Types

```text id="chunk-types"
concept
activity
assessment
reflection
experiment
table
formula
diagram
```

---

# Chunk Example

```json id="chunk-example"
{
  "chunk_type": "activity",
  "content": "Siswa melakukan percobaan..."
}
```

---

# STAGE 6 — Metadata Enrichment

## Purpose

Menambahkan educational intelligence.

---

# Enrichment Examples

```json id="metadata-enrichment"
{
  "difficulty": "easy",
  "learning_style": ["visual"],
  "taxonomy": "analyze"
}
```

---

# Metadata Categories

---

# Curriculum Metadata

* subject
* phase
* grade
* competency

---

# Pedagogical Metadata

* inquiry
* reflection
* experiment

---

# AI Metadata

* difficulty
* semantic category
* confidence score

---

# STAGE 7 — Embedding Pipeline

## Purpose

Generate embeddings.

---

# Multi-Embedding Strategy

---

# Text Embedding

Untuk:

* concepts,
* explanations.

---

# Table Embedding

Untuk:

* assessment matrix,
* competency mapping.

---

# Image Embedding

Untuk:

* diagrams,
* educational images.

---

# Formula Embedding

Untuk:

* equations,
* scientific notation.

---

# Recommended Models

## Text

* BGE-M3

---

# Multilingual

* multilingual-e5-large

---

# Embedding Output Example

```json id="embedding-output"
{
  "chunk_id": "chunk_001",
  "embedding_model": "bge-m3",
  "dimension": 1024
}
```

---

# STAGE 8 — Vector Indexing

## Purpose

Store embeddings untuk retrieval.

---

# Recommended Database

* Qdrant

---

# Metadata Filtering Example

```json id="metadata-filtering"
{
  "subject": "IPA",
  "grade": 4,
  "chunk_type": "activity"
}
```

---

# Knowledge Organization Strategy

---

# Knowledge Namespace

```text id="knowledge-namespace-structure"
knowledge/
├── cp/
├── atp/
├── buku_guru/
├── buku_siswa/
├── modul_ajar/
├── asesmen/
└── p5/
```

---

# Purpose

Meningkatkan:

* retrieval precision,
* filtering,
* explainability.

---

# Event-Driven Pipeline

---

# Example Flow

```text id="event-driven-example"
DOCUMENT.UPLOAD.REQUESTED
      ↓
DOCUMENT.PARSE.COMPLETED
      ↓
CHUNK.GENERATION.COMPLETED
      ↓
EMBEDDING.INDEX.COMPLETED
```

---

# Queue Strategy

---

# Recommended Queues

```text id="queue-strategy"
document.queue
OCR.queue
chunk.queue
embedding.queue
indexing.queue
```

---

# Retry Strategy

---

# Retryable

✅ temporary network failure

✅ queue timeout

---

# Non-Retryable

❌ corrupted PDF

❌ malformed schema

---

# Dead Letter Queue (DLQ)

## Required

```text id="dlq-required"
dlq.document.parse
dlq.embedding
```

---

# Observability Requirements

---

# Mandatory Metrics

```text id="mandatory-metrics"
OCR_latency
parse_failure_rate
embedding_duration
chunk_quality
queue_lag
```

---

# Required Logs

* ingestion logs,
* extraction logs,
* chunk logs,
* embedding logs.

---

# OpenTelemetry

Semua stage wajib:

* traceable,
* correlated.

---

# Security Requirements

---

# Mandatory

✅ malware scan

✅ encrypted storage

✅ RBAC

✅ signed URLs

---

# Never Store

❌ raw credentials

❌ secrets in metadata

---

# Scalability Strategy

---

# Horizontal Scaling

Workers harus:

* stateless,
* autoscalable.

---

# GPU Isolation

GPU workloads dipisah:

* OCR acceleration,
* embeddings,
* vision inference.

---

# Pipeline Failure Handling

---

# Example

```text id="failure-handling"
OCR failure
   ↓
retry
   ↓
fallback OCR
   ↓
DLQ
```

---

# Governance Requirements

---

# Every Document Must Be

✅ traceable

✅ reproducible

✅ auditable

---

# Audit Metadata

```json id="audit-metadata-example"
{
  "document_id": "doc_001",
  "pipeline_version": "v2",
  "embedding_model": "bge-m3"
}
```

---

# Anti-Patterns

---

# DO NOT

❌ fixed-character chunking

❌ OCR all documents blindly

❌ flatten tables into plain text

❌ store embeddings in relational DB

❌ synchronous OCR processing

❌ upload directly to vector DB

---

# Production Readiness Checklist

---

# Mandatory

✅ async processing

✅ queue orchestration

✅ observability

✅ retries

✅ DLQ

✅ metadata enrichment

✅ semantic chunking

✅ vector indexing

---

# Most Important Insight

Enterprise document ingestion bukan tentang:

```text id="wrong-focus-ingestion"
extracting text from PDF
```

Tetapi tentang:

```text id="correct-focus-ingestion"
building educational knowledge intelligence
```

Karena:
quality retrieval,
AI reasoning,
dan explainability

semuanya ditentukan oleh kualitas ingestion pipeline.
