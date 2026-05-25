# EMBEDDING STRATEGY

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan strategi embedding untuk Enterprise Educational AI Platform.

Embedding strategy adalah:

```text id="embedding-strategy-definition"
semantic representation architecture
```

yang digunakan untuk:

* semantic retrieval,
* curriculum-aware search,
* multimodal understanding,
* educational reasoning,
* vector indexing.

---

# Why Embeddings Matter

Dalam enterprise educational AI:

```text id="embedding-core-principle"
retrieval quality determines AI quality
```

Dan retrieval quality sangat bergantung pada:

* embedding quality,
* chunk quality,
* metadata quality.

---

# Embedding Objectives

---

# 1. Semantic Understanding

Embedding harus memahami:

* educational semantics,
* curriculum context,
* competency relationships.

---

# 2. Multilingual Support

Karena sistem menggunakan:

* Bahasa Indonesia,
* English,
* bilingual curriculum resources.

---

# 3. Multi-Modal Understanding

Embedding harus mendukung:

* text,
* table,
* formula,
* image,
* diagram.

---

# 4. Retrieval Optimization

Embedding harus:

* retrieval-friendly,
* scalable,
* filter-compatible.

---

# Core Principles

---

# 1. One Embedding Is Not Enough

Enterprise educational AI tidak boleh menggunakan:

```text id="single-embedding-anti-pattern"
1 embedding for everything
```

---

# Correct Strategy

Gunakan:

* text embedding,
* table embedding,
* formula embedding,
* image embedding.

---

# 2. Embeddings Must Be Metadata-Aware

Embedding saja tidak cukup.

Harus dikombinasikan dengan:

* metadata filtering,
* ontology,
* reranking.

---

# 3. Embeddings Must Be Reproducible

Semua embedding wajib:

* versioned,
* traceable,
* reproducible.

---

# Embedding Architecture

```text id="embedding-architecture"
Content
  ↓
Content-Type Detection
  ↓
Embedding Router
  ├── Text Embedding
  ├── Table Embedding
  ├── Formula Embedding
  └── Image Embedding
  ↓
Vector Store
```

---

# Embedding Categories

```text id="embedding-categories"
Text Embeddings
Multilingual Embeddings
Formula Embeddings
Image Embeddings
Table Embeddings
Hybrid Embeddings
```

---

# 1. Text Embeddings

## Purpose

Representasi semantic text.

---

# Used For

✅ concept retrieval

✅ educational QA

✅ lesson generation

✅ curriculum retrieval

---

# Recommended Models

## Primary Recommendation

* BGE-M3

---

# Why BGE-M3

Karena mendukung:

* multilingual,
* hybrid retrieval,
* dense + sparse retrieval.

---

# Alternative Models

* E5-large
* Instructor-xl

---

# Embedding Metadata Example

```json id="text-embedding-metadata"
{
  "embedding_type": "text",
  "model": "bge-m3",
  "dimension": 1024
}
```

---

# Text Embedding Rules

---

# DO

✅ semantic chunking

✅ curriculum-aware chunking

✅ metadata enrichment

---

# DON'T

❌ fixed 1000-char chunking

❌ embedding raw PDF pages

❌ embedding noisy OCR blindly

---

# 2. Multilingual Embeddings

## Purpose

Mendukung:

* Bahasa Indonesia,
* English,
* bilingual content.

---

# Recommended Model

* multilingual-e5-large

---

# Why Important

Karena educational content sering:

* campuran bahasa,
* istilah ilmiah Inggris,
* bilingual references.

---

# Example

```text id="multilingual-example"
“heat transfer”
=
“perpindahan panas”
```

---

# Multilingual Retrieval Goals

Embedding harus mampu:

* cross-language retrieval,
* semantic equivalence.

---

# Example Query

```text id="multilingual-query"
“konduksi”
```

harus dapat menemukan:

* “heat conduction”.

---

# Recommended Strategy

---

# Indonesian-First Retrieval

Gunakan:

* Indonesian-optimized prompts,
* multilingual embeddings.

---

# Hybrid Strategy

```text id="hybrid-multilingual-strategy"
Multilingual Embedding
     +
Metadata Filtering
```

---

# 3. Formula Embeddings

## Purpose

Representasi mathematical semantics.

---

# Why Important

Formula tidak bisa diperlakukan seperti:

* plain text,
* OCR biasa.

---

# Example

```text id="formula-example"
F = m × a
```

memiliki semantic structure.

---

# Formula Pipeline

```text id="formula-pipeline"
Formula Extraction
      ↓
Formula Normalization
      ↓
Formula Embedding
```

---

# Recommended Formula Extraction

* Nougat

---

# Formula Embedding Metadata

```json id="formula-embedding-metadata"
{
  "embedding_type": "formula",
  "formula_domain": "physics"
}
```

---

# Formula Retrieval Use Cases

✅ physics formulas

✅ chemistry equations

✅ mathematics concepts

---

# Formula Normalization Rules

---

# Normalize

✅ notation consistency

✅ spacing

✅ symbols

---

# Example

```text id="formula-normalization"
F=ma
→
F = m × a
```

---

# 4. Image Embeddings

## Purpose

Representasi semantic visual content.

---

# Used For

✅ diagrams

✅ experiments

✅ educational illustrations

✅ science images

---

# Example

```text id="image-example"
diagram perpindahan panas
```

---

# Vision Embedding Pipeline

```text id="vision-pipeline"
Image Extraction
      ↓
Caption Generation
      ↓
Vision Embedding
```

---

# Recommended Vision Models

## Local Models

* Qwen-VL
* LLaVA

---

# Cloud Vision

* GPT-4o Vision

---

# Image Metadata Example

```json id="image-metadata-example"
{
  "image_type": "diagram",
  "caption": "Perpindahan panas melalui konduksi"
}
```

---

# Image Embedding Strategy

---

# Recommended

```text id="image-embedding-strategy"
caption embedding
     +
vision embedding
```

---

# Why Important

Karena educational diagrams:

* sering kompleks,
* membutuhkan contextual understanding.

---

# 5. Table Embeddings

## Purpose

Representasi semantic table structure.

---

# Why Important

Pendidikan penuh:

* rubrik,
* competency matrix,
* assessment table.

---

# Recommended Extraction

* Camelot

---

# Table Embedding Strategy

---

# Preserve

✅ row structure

✅ column relationship

✅ semantic meaning

---

# NEVER

❌ flatten tables into plain text.

---

# Table Embedding Example

```json id="table-embedding-example"
{
  "table_type": "rubric",
  "columns": ["indikator", "nilai"]
}
```

---

# 6. Hybrid Embeddings

## Purpose

Menggabungkan:

* dense retrieval,
* sparse retrieval,
* metadata filtering.

---

# Recommended Strategy

```text id="hybrid-retrieval-strategy"
Dense Embedding
    +
Sparse Retrieval
    +
Metadata Filtering
    +
Reranking
```

---

# Why Important

Dense embedding saja sering gagal untuk:

* exact curriculum code,
* competency identifier,
* formula notation.

---

# Embedding Storage Strategy

---

# Recommended Database

* Qdrant

---

# Why Qdrant

Karena mendukung:

* metadata filtering,
* hybrid search,
* scalable indexing.

---

# Embedding Collection Strategy

---

# Recommended Collections

```text id="embedding-collections"
text_embeddings
formula_embeddings
image_embeddings
table_embeddings
```

---

# Why Separate Collections

Karena:

* dimension bisa berbeda,
* retrieval strategy berbeda,
* optimization berbeda.

---

# Embedding Metadata Standard

## Required Fields

```json id="embedding-standard"
{
  "embedding_id": "uuid",
  "embedding_type": "text",
  "model_name": "bge-m3",
  "model_version": "v1"
}
```

---

# Additional Metadata

```json id="embedding-additional-metadata"
{
  "subject": "IPA",
  "grade": 4,
  "chunk_type": "activity"
}
```

---

# Embedding Versioning

---

# Mandatory

Semua embeddings wajib:

* reproducible,
* reindexable.

---

# Example

```json id="embedding-versioning"
{
  "embedding_version": "v2"
}
```

---

# Reindexing Strategy

---

# Reindex Required When

✅ embedding model berubah

✅ chunking strategy berubah

✅ metadata schema berubah

---

# Reindex Pipeline

```text id="reindex-pipeline"
Old Embeddings
      ↓
Re-Embedding
      ↓
Re-Indexing
```

---

# Embedding Quality Metrics

---

# Required Metrics

| Metric              | Purpose               |
| ------------------- | --------------------- |
| retrieval_precision | semantic quality      |
| recall              | retrieval coverage    |
| semantic_similarity | embedding consistency |
| latency             | performance           |

---

# Embedding Evaluation

---

# Mandatory Tests

✅ multilingual retrieval

✅ curriculum retrieval

✅ formula retrieval

✅ image retrieval

---

# Example Evaluation Query

```text id="evaluation-query"
“energi panas”
```

Expected:

* concept chunks,
* experiments,
* diagrams,
* assessments.

---

# Embedding Observability

---

# Required Metrics

```text id="embedding-observability"
embedding_duration
embedding_failure_rate
vector_dimension_validation
```

---

# Required Logs

* embedding logs,
* indexing logs,
* retrieval logs.

---

# GPU Strategy

---

# GPU Recommended For

✅ batch embeddings

✅ image embeddings

✅ reranking

---

# CPU-Compatible Workloads

✅ lightweight embeddings

✅ metadata classification

---

# Security Requirements

---

# Never Store

❌ raw secrets

❌ internal prompts

---

# Access Control

Embedding services harus:

* RBAC-aware,
* tenant-aware.

---

# Governance Requirements

---

# Every Embedding Must Be

✅ versioned

✅ traceable

✅ reproducible

---

# Audit Metadata Example

```json id="embedding-audit-metadata"
{
  "embedding_model": "bge-m3",
  "embedding_version": "v2"
}
```

---

# Anti-Patterns

---

# DO NOT

❌ one embedding for all content

❌ embedding raw PDF pages

❌ flattening tables

❌ ignoring metadata filtering

❌ storing embeddings in PostgreSQL only

❌ using embeddings without reranking

---

# Production Readiness Checklist

---

# Mandatory

✅ multilingual embeddings

✅ formula embeddings

✅ image embeddings

✅ hybrid retrieval

✅ metadata filtering

✅ embedding versioning

✅ observability

---

# Most Important Insight

Enterprise educational AI retrieval bukan tentang:

```text id="wrong-embedding-focus"
vector similarity only
```

Tetapi tentang:

```text id="correct-embedding-focus"
semantic educational intelligence retrieval
```

Karena:
retrieval quality ditentukan oleh:

* embeddings,
* metadata,
* ontology,
* chunking,
* reranking,
* educational structure.
