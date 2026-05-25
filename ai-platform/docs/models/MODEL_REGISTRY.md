# MODEL REGISTRY

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan Model Registry untuk Enterprise Educational AI Platform.

Model Registry adalah:

```text id="model-registry-definition"
centralized AI model management system
```

yang digunakan untuk:

* model governance,
* version tracking,
* deployment management,
* hardware planning,
* model observability,
* AI reproducibility.

---

# Why Model Registry Matters

Enterprise AI systems tidak boleh:

❌ menggunakan model tanpa tracking

❌ deploy model tanpa benchmark

❌ mengganti model tanpa audit

❌ menggunakan embedding model random

---

# Model Registry Enables

✅ traceability

✅ reproducibility

✅ governance

✅ rollback

✅ benchmarking

✅ deployment consistency

---

# Core Principles

---

# 1. Every Model Must Be Registered

Tidak boleh ada:

* hidden model,
* unmanaged model,
* local random model.

---

# 2. Every Model Must Be Versioned

Semua model wajib:

* semantic versioning,
* immutable version history.

---

# 3. Every Model Must Be Observable

Semua model wajib memiliki:

* metrics,
* logs,
* latency tracking,
* quality tracking.

---

# 4. Every Model Must Be Governed

Semua model wajib:

* approved,
* benchmarked,
* documented.

---

# Model Registry Architecture

```text id="model-registry-architecture"
Model Registry
├── LLM Models
├── Embedding Models
├── OCR Models
├── Vision Models
├── Reranker Models
├── Classification Models
└── Experimental Models
```

---

# Registry Metadata Standard

## Required Fields

```json id="registry-required-fields"
{
  "model_id": "uuid",
  "model_name": "bge-m3",
  "model_version": "v1.0.0",
  "status": "production"
}
```

---

# Standard Fields

| Field             | Description               |
| ----------------- | ------------------------- |
| model_id          | unique identifier         |
| model_name        | model name                |
| model_version     | semantic version          |
| provider          | provider/vendor           |
| model_type        | embedding/LLM/OCR/etc     |
| status            | experimental/staging/prod |
| deployment_target | CPU/GPU                   |
| created_at        | registration timestamp    |

---

# Model Categories

---

# 1. LLM Models

## Purpose

Digunakan untuk:

* reasoning,
* generation,
* summarization,
* tutoring.

---

# Example Registry

```json id="llm-registry-example"
{
  "model_name": "gpt-4.1",
  "provider": "OpenAI",
  "model_type": "LLM"
}
```

---

# Recommended Models

## Cloud Models

* GPT-4.1
* Claude

---

# Local Models

* Mistral
* Qwen
* Llama

---

# Recommended Usage

| Use Case                   | Model Type |
| -------------------------- | ---------- |
| reasoning                  | cloud LLM  |
| metadata extraction        | local LLM  |
| lightweight classification | local LLM  |
| summarization              | hybrid     |

---

# 2. Embedding Models

## Purpose

Generate semantic embeddings.

---

# Recommended Models

## Primary

* BGE-M3

---

# Multilingual

* multilingual-e5-large

---

# Registry Example

```json id="embedding-registry-example"
{
  "model_name": "bge-m3",
  "dimension": 1024,
  "language_support": ["id", "en"]
}
```

---

# Embedding Model Metadata

| Field           | Description      |
| --------------- | ---------------- |
| dimension       | vector dimension |
| multilingual    | language support |
| max_tokens      | input capacity   |
| retrieval_score | benchmark score  |

---

# Embedding Strategy

---

# Multi-Embedding Architecture

```text id="multi-embedding-architecture"
Text Embedding
Table Embedding
Image Embedding
Formula Embedding
```

---

# Why Important

Karena:
educational AI bersifat:

* multimodal,
* curriculum-aware.

---

# 3. OCR Models

## Purpose

OCR extraction untuk:

* scanned PDF,
* image-based documents,
* formulas.

---

# Recommended OCR Models

* Tesseract OCR
* PaddleOCR

---

# Formula OCR

* Nougat

---

# OCR Registry Example

```json id="ocr-registry-example"
{
  "model_name": "PaddleOCR",
  "language_support": ["id", "en"]
}
```

---

# OCR Evaluation Metrics

| Metric           | Purpose            |
| ---------------- | ------------------ |
| OCR accuracy     | extraction quality |
| formula accuracy | math extraction    |
| table accuracy   | table parsing      |

---

# 4. Vision Models

## Purpose

Memahami:

* diagrams,
* educational images,
* experiments.

---

# Recommended Models

## Local Vision Models

* Qwen-VL
* LLaVA

---

# Cloud Vision

* GPT-4o Vision

---

# Registry Example

```json id="vision-registry-example"
{
  "model_name": "Qwen-VL",
  "vision_support": true
}
```

---

# 5. Reranker Models

## Purpose

Improve retrieval precision.

---

# Example Models

* bge-reranker
* cross-encoder reranker

---

# Why Important

Karena:
retrieval quality lebih penting daripada:

* model terbesar,
* prompt terbaik.

---

# 6. Classification Models

## Purpose

Digunakan untuk:

* metadata classification,
* pedagogy classification,
* taxonomy detection.

---

# Example Tasks

```text id="classification-tasks"
difficulty classification
taxonomy classification
chunk classification
```

---

# Model Status Lifecycle

---

# Supported Status

```text id="model-status-lifecycle"
experimental
staging
production
deprecated
archived
```

---

# Lifecycle Rules

## Experimental

* testing only,
* non-production.

---

# Staging

* benchmarked,
* pre-production validation.

---

# Production

* approved,
* monitored,
* stable.

---

# Deprecated

* migration required.

---

# GPU Requirements

---

# Purpose

Hardware planning.

---

# Registry Example

```json id="gpu-requirement-example"
{
  "gpu_required": true,
  "gpu_type": "L4",
  "vram_requirement": "24GB"
}
```

---

# GPU Recommendations

| Workload         | GPU     |
| ---------------- | ------- |
| embeddings       | T4 / L4 |
| reranking        | L4      |
| VLM              | A100    |
| OCR acceleration | T4      |

---

# CPU-Compatible Models

## Recommended For

* lightweight metadata extraction,
* simple classification.

---

# Example

```json id="cpu-compatible-example"
{
  "cpu_compatible": true
}
```

---

# Model Versioning Standard

---

# Rules

Gunakan:

```text id="semantic-versioning"
MAJOR.MINOR.PATCH
```

---

# Example

```text id="model-version-example"
v1.2.0
```

---

# Version Change Rules

| Type  | Meaning                 |
| ----- | ----------------------- |
| MAJOR | architecture change     |
| MINOR | performance improvement |
| PATCH | bug fix                 |

---

# Model Benchmarking

---

# Mandatory Before Production

✅ latency benchmark

✅ hallucination evaluation

✅ retrieval evaluation

✅ OCR evaluation

✅ multilingual evaluation

---

# Example Benchmark Metadata

```json id="benchmark-metadata"
{
  "retrieval_accuracy": 0.91,
  "hallucination_rate": 0.03
}
```

---

# Model Evaluation Categories

---

# Required

| Category          | Purpose            |
| ----------------- | ------------------ |
| retrieval quality | RAG quality        |
| latency           | performance        |
| hallucination     | reliability        |
| multilingual      | Indonesian support |
| cost              | operational cost   |

---

# Model Governance

---

# Approval Workflow

```text id="approval-workflow"
Experimental
   ↓
Benchmark
   ↓
Governance Review
   ↓
Staging
   ↓
Production
```

---

# Mandatory Governance Metadata

```json id="governance-registry-metadata"
{
  "approved_by": "AI Governance Team",
  "approval_date": "2026-05-25"
}
```

---

# Model Deployment Metadata

---

# Required Fields

```json id="deployment-metadata"
{
  "deployment_environment": "production",
  "deployment_cluster": "gpu-ai"
}
```

---

# Observability Requirements

---

# Every Model Must Have

✅ latency metrics

✅ token usage metrics

✅ GPU utilization

✅ failure metrics

---

# Example Metrics

```text id="model-metrics"
model_latency
token_usage
embedding_duration
GPU_utilization
```

---

# Audit Requirements

---

# Every AI Response Must Include

```json id="audit-requirements"
{
  "model_name": "gpt-4.1",
  "model_version": "v1.2.0"
}
```

---

# Rollback Strategy

---

# Rules

Semua model deployment wajib:

* rollback-ready,
* reproducible.

---

# Example

```text id="rollback-strategy"
v1.3.0 failure
   ↓
rollback → v1.2.0
```

---

# Registry Storage Strategy

---

# Recommended Database

## Metadata Storage

* PostgreSQL

---

# Artifact Storage

* MinIO

---

# Optional Model Registry Tools

Jika skala besar:

* MLflow

---

# Registry API Example

---

# Example Endpoint

```text id="registry-api-example"
GET /v1/models
GET /v1/models/{id}
POST /v1/models/register
```

---

# Security Requirements

---

# Rules

Model registry harus:

* RBAC-aware,
* audit-logged,
* immutable.

---

# Restricted Access

❌ production model overwrite

❌ unapproved model deployment

---

# Anti-Patterns

---

# DO NOT

❌ hardcoded model selection

❌ hidden local models

❌ deploying unbenchmarked models

❌ non-versioned prompts/models

❌ direct production model replacement

---

# Production Readiness Checklist

---

# Mandatory

✅ model versioning

✅ benchmark metadata

✅ GPU metadata

✅ observability

✅ governance approval

✅ rollback support

✅ audit logs

---

# Most Important Insight

Enterprise AI systems bukan tentang:

```text id="wrong-model-focus"
using the newest model
```

Tetapi tentang:

```text id="correct-model-focus"
operating models reliably at scale
```

Karena:
model terbaik sekalipun akan gagal di production tanpa:

* governance,
* observability,
* versioning,
* deployment discipline.
