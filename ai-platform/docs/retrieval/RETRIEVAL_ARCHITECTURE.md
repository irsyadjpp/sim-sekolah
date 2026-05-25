# RETRIEVAL ARCHITECTURE

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan Retrieval Architecture untuk Enterprise Educational AI Platform.

Retrieval architecture adalah:

```text id="retrieval-architecture-definition"
knowledge retrieval intelligence system
```

yang bertanggung jawab untuk:

* menemukan context yang relevan,
* memahami intent pengguna,
* melakukan semantic retrieval,
* melakukan reranking,
* memberikan grounding untuk AI generation.

---

# Why Retrieval Matters

Dalam enterprise educational AI:

```text id="retrieval-core-principle"
retrieval quality > model size
```

Karena:
LLM terbaik sekalipun akan menghasilkan:

* hallucination,
* misinformation,
* curriculum mismatch,

jika retrieval buruk.

---

# Core Objectives

---

# 1. Curriculum-Aware Retrieval

Retrieval harus memahami:

* subject,
* phase,
* competency,
* educational context.

---

# 2. Explainable Retrieval

AI wajib dapat menjelaskan:

* kenapa context dipilih,
* source mana digunakan.

---

# 3. Multi-Modal Retrieval

Retrieval harus mendukung:

* text,
* formula,
* image,
* table,
* assessment.

---

# 4. Enterprise Scalability

Retrieval harus:

* low latency,
* horizontally scalable,
* observable.

---

# Core Principles

---

# 1. Retrieval Is Not Search

Retrieval modern bukan:

* keyword search,
* plain vector similarity.

Tetapi:

```text id="modern-retrieval"
semantic educational intelligence
```

---

# 2. Hybrid Retrieval Is Mandatory

Enterprise educational AI wajib menggunakan:

```text id="hybrid-retrieval"
Dense Retrieval
     +
Sparse Retrieval
     +
Metadata Filtering
     +
Reranking
```

---

# 3. Metadata Is First-Class

Metadata filtering lebih penting daripada:

* raw vector similarity.

---

# 4. Reranking Is Mandatory

Initial retrieval sering noisy.

Reranking diperlukan untuk:

* precision,
* curriculum relevance,
* answer quality.

---

# High-Level Retrieval Architecture

```text id="high-level-retrieval-architecture"
User Query
    ↓
Query Understanding
    ↓
Query Enrichment
    ↓
Hybrid Retrieval
 ├── Dense Retrieval
 ├── Sparse Retrieval
 └── Metadata Filtering
    ↓
Candidate Merging
    ↓
Reranking
    ↓
Context Builder
    ↓
Prompt Assembly
    ↓
LLM
```

---

# Retrieval Pipeline

---

# STAGE 1 — Query Understanding

## Purpose

Memahami:

* intent,
* educational context,
* curriculum relevance.

---

# Query Understanding Tasks

```text id="query-understanding-tasks"
intent detection
subject classification
grade classification
competency detection
language detection
```

---

# Example

## User Query

```text id="query-example"
jelaskan perpindahan panas
```

---

# Query Understanding Result

```json id="query-understanding-result"
{
  "subject": "IPA",
  "topic": "Perpindahan Panas",
  "language": "id"
}
```

---

# Query Understanding Models

## Recommended

* lightweight classifier
* local LLM
* embedding classifier

---

# Query Normalization

---

# Purpose

Membersihkan:

* typo,
* synonym,
* notation variation.

---

# Example

```text id="query-normalization-example"
“konduksi panas”
=
“perpindahan panas konduksi”
```

---

# Query Expansion

## Purpose

Menambahkan:

* synonym,
* curriculum terminology,
* ontology relationships.

---

# Example

```text id="query-expansion-example"
“kalor”
→
“energi panas”
```

---

# STAGE 2 — Hybrid Retrieval

## Purpose

Menggabungkan:

* semantic retrieval,
* keyword retrieval,
* metadata filtering.

---

# Architecture

```text id="hybrid-retrieval-architecture-detail"
Hybrid Retrieval
 ├── Dense Retrieval
 ├── Sparse Retrieval
 └── Metadata Filtering
```

---

# 2.1 Dense Retrieval

## Purpose

Semantic similarity search.

---

# Recommended Database

* Qdrant

---

# Recommended Embedding Models

* BGE-M3
* multilingual-e5-large

---

# Dense Retrieval Strengths

✅ semantic understanding

✅ multilingual retrieval

✅ contextual retrieval

---

# Dense Retrieval Weaknesses

❌ exact keyword matching

❌ curriculum code retrieval

❌ notation precision

---

# 2.2 Sparse Retrieval

## Purpose

Keyword & lexical retrieval.

---

# Recommended Engines

* BM25
* Elasticsearch
* OpenSearch

---

# Sparse Retrieval Strengths

✅ exact match

✅ curriculum code retrieval

✅ formula notation

---

# Sparse Retrieval Weaknesses

❌ semantic limitations

---

# Example

## Query

```text id="sparse-query-example"
CP-IPA-B-01
```

Sparse retrieval lebih efektif dibanding vector similarity.

---

# 2.3 Metadata Filtering

## Purpose

Educational precision filtering.

---

# Example Filters

```json id="metadata-filter-example"
{
  "subject": "IPA",
  "grade": 4,
  "phase": "B",
  "chunk_type": "activity"
}
```

---

# Why Important

Karena educational retrieval membutuhkan:

* curriculum alignment,
* educational relevance.

---

# Required Metadata Filters

```text id="required-metadata-filters"
subject
grade
phase
document_type
chunk_type
taxonomy_level
```

---

# STAGE 3 — Candidate Merging

## Purpose

Menggabungkan hasil:

* dense retrieval,
* sparse retrieval,
* metadata-filtered retrieval.

---

# Strategy

```text id="candidate-merging"
Dense Candidates
    +
Sparse Candidates
    +
Filtered Candidates
```

---

# Deduplication Rules

Candidates wajib:

* deduplicated,
* normalized.

---

# STAGE 4 — Reranking

## Purpose

Meningkatkan precision retrieval.

---

# Why Reranking Matters

Initial retrieval sering:

* noisy,
* partially relevant.

Reranking membantu:

* relevance scoring,
* curriculum alignment,
* semantic precision.

---

# Recommended Models

* bge-reranker
* cross-encoder reranker

---

# Reranking Inputs

```text id="reranking-inputs"
query
candidate chunk
metadata
ontology score
```

---

# Reranking Criteria

| Criteria             | Purpose                |
| -------------------- | ---------------------- |
| semantic relevance   | contextual match       |
| curriculum alignment | educational fit        |
| metadata match       | filtering quality      |
| ontology relevance   | knowledge relationship |

---

# Example

```text id="reranking-example"
Candidate A:
semantic score 0.82
curriculum score 0.95

→ higher final rank
```

---

# STAGE 5 — Context Builder

## Purpose

Menyusun context untuk LLM.

---

# Context Builder Rules

Context harus:

* concise,
* relevant,
* citation-aware.

---

# Recommended Context Structure

```text id="context-structure"
Source
Metadata
Content
Relevance Score
```

---

# Example

```text id="context-builder-example"
[SOURCE]
Buku Guru IPA Kelas 4
[/SOURCE]

[CONTENT]
Perpindahan panas terjadi...
```

---

# Context Window Strategy

---

# Prioritize

✅ highest relevance

✅ educational diversity

✅ curriculum alignment

---

# Avoid

❌ duplicate chunks

❌ unrelated chunks

❌ noisy OCR chunks

---

# Query Understanding Strategy

---

# Query Types

```text id="query-types"
factual question
concept explanation
assessment generation
lesson planning
remediation request
```

---

# Query Intent Example

## User Query

```text id="query-intent-example"
buat soal energi panas
```

Intent:

* assessment generation.

---

# Ontology-Aware Retrieval

## Purpose

Menggunakan:

* concept relationships,
* prerequisite graph,
* competency hierarchy.

---

# Example

## Query

```text id="ontology-query-example"
materi sebelum kalor
```

---

# Retrieval Enhancement

Ontology membantu menemukan:

* prerequisite concepts.

---

# Multi-Modal Retrieval

---

# Purpose

Retrieval untuk:

* image,
* table,
* formula.

---

# Example

```text id="multimodal-query-example"
diagram perpindahan panas
```

---

# Retrieval Strategy

```text id="multimodal-retrieval-strategy"
Text Retrieval
    +
Image Retrieval
    +
Caption Retrieval
```

---

# Formula Retrieval

---

# Purpose

Scientific & mathematical understanding.

---

# Example

```text id="formula-retrieval-example"
rumus gaya
```

---

# Formula Retrieval Pipeline

```text id="formula-retrieval-pipeline"
Formula Query
      ↓
Formula Embedding
      ↓
Formula Retrieval
```

---

# Educational Retrieval Strategy

---

# Retrieval Priorities

```text id="educational-retrieval-priority"
1. curriculum relevance
2. competency relevance
3. semantic relevance
4. recency
```

---

# Retrieval Scoring Formula

## Example

FinalScore = 0.4(Semantic) + 0.3(Curriculum) + 0.2(Metadata) + 0.1(Ontology)

---

# Retrieval Metadata Standard

## Required Fields

```json id="retrieval-metadata"
{
  "retrieval_id": "uuid",
  "retrieval_strategy": "hybrid",
  "embedding_model": "bge-m3"
}
```

---

# Retrieval Observability

---

# Required Metrics

```text id="retrieval-observability"
retrieval_latency
retrieval_precision
reranking_duration
context_hit_rate
```

---

# Additional Metrics

```text id="retrieval-additional-metrics"
hallucination_rate
retrieval_confidence
metadata_filter_accuracy
```

---

# Retrieval Logging

## Mandatory

* query logs,
* reranking logs,
* metadata filter logs,
* retrieval scores.

---

# Example Retrieval Log

```json id="retrieval-log-example"
{
  "query": "energi panas",
  "retrieved_chunks": 12,
  "reranked_chunks": 5
}
```

---

# Retrieval Governance

---

# Required

✅ explainability

✅ traceability

✅ auditability

---

# Explainability Example

```json id="retrieval-explainability"
{
  "reason_selected": [
    "subject match",
    "high semantic relevance",
    "ontology relationship"
  ]
}
```

---

# Security Requirements

---

# Retrieval Must Prevent

❌ unauthorized data retrieval

❌ tenant leakage

❌ prompt injection context poisoning

---

# Required Protections

✅ RBAC-aware filtering

✅ tenant isolation

✅ query validation

---

# Scalability Strategy

---

# Retrieval Services Must Be

✅ stateless

✅ horizontally scalable

✅ cache-aware

---

# Recommended Cache

* Redis

---

# Retrieval Cache Targets

```text id="retrieval-cache-targets"
embedding cache
reranking cache
query cache
```

---

# Anti-Patterns

---

# DO NOT

❌ vector search only

❌ no reranking

❌ ignoring metadata filtering

❌ embedding raw PDF pages

❌ keyword search only

❌ no ontology integration

---

# Production Readiness Checklist

---

# Mandatory

✅ hybrid retrieval

✅ metadata filtering

✅ reranking

✅ query understanding

✅ ontology integration

✅ observability

✅ explainability

---

# Most Important Insight

Enterprise educational retrieval bukan tentang:

```text id="wrong-retrieval-thinking"
finding similar text
```

Tetapi tentang:

```text id="correct-retrieval-thinking"
finding the most educationally relevant knowledge
```

Karena:
AI reasoning quality ditentukan oleh:

* retrieval precision,
* curriculum alignment,
* ontology understanding,
* metadata intelligence.
