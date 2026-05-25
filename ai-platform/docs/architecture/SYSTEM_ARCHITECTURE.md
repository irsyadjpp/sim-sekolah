# SYSTEM ARCHITECTURE

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini menjelaskan arsitektur sistem secara menyeluruh untuk Enterprise Educational AI Platform.

Dokumen ini mencakup:

* high-level architecture,
* service boundaries,
* infrastructure topology,
* communication strategy,
* AI pipeline architecture,
* observability,
* governance.

---

# System Vision

Platform ini dirancang sebagai:

```text id="fr8szm"
Enterprise Educational Intelligence Platform
```

Bukan:

* chatbot sederhana,
* PDF QA app,
* LangChain demo,
* AI wrapper biasa.

---

# Core Objectives

## 1. Educational Intelligence

Mendukung:

* kurikulum,
* asesmen,
* ATP,
* CP,
* pembelajaran multimodal.

---

## 2. Enterprise Scalability

Mendukung:

* ribuan dokumen,
* concurrent users,
* distributed workers,
* GPU workloads.

---

## 3. AI Governance

Mendukung:

* auditability,
* traceability,
* moderation,
* observability.

---

# High-Level Architecture

```text id="high-level-architecture"
┌──────────────────────┐
│   React Frontend     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Golang Backend API  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   AI Adapter Layer   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│    Python AI Platform        │
└──────────┬───────────────────┘
           │
 ┌─────────┼─────────┐
 ▼         ▼         ▼
Parser   Retrieval  Generation
Svc      Svc        Svc

           │
           ▼
┌──────────────────────┐
│      Qdrant          │
└──────────────────────┘
```

---

# Architecture Principles

---

# 1. Separation of Concerns

## React

Hanya menangani:

* UI,
* UX,
* presentation layer.

---

## Golang Backend

Menangani:

* business logic,
* ERP,
* auth,
* transactional workflows.

---

## Python AI Platform

Menangani:

* AI,
* retrieval,
* parsing,
* orchestration,
* embeddings.

---

# 2. AI as Dedicated Infrastructure

AI Platform diperlakukan sebagai:

```text id="g4a9uj"
Internal AI Infrastructure
```

Bukan:

* frontend app,
* monolith backend.

---

# 3. Event-Driven Architecture

Heavy workloads berjalan asynchronous.

Contoh:

* OCR,
* embeddings,
* indexing,
* image processing.

---

# 4. Microservice-Based AI

Setiap service memiliki:

* responsibility tunggal,
* independent scaling,
* isolated deployment.

---

# Core System Components

---

# 1. React Frontend

## Responsibility

* user interface,
* dashboard,
* AI chat UI,
* document upload UI.

---

# Technology

* React

---

# Rules

Frontend:

* tidak boleh akses AI platform langsung,
* tidak boleh memanggil Qdrant,
* tidak boleh memegang AI credentials.

---

# 2. Golang Backend Platform

## Responsibility

* business logic,
* school ERP,
* user management,
* auth,
* API aggregation.

---

# Technology

* Go

---

# Core Modules

```text id="golang-core"
- auth service
- school service
- curriculum service
- AI adapter
```

---

# 3. AI Adapter Layer

## Purpose

Bridge antara:

* Golang backend,
* Python AI platform.

---

# Responsibilities

* request forwarding,
* auth propagation,
* policy enforcement,
* caching,
* timeout handling,
* retry handling.

---

# Rules

Frontend tidak boleh bypass adapter.

---

# 4. Python AI Platform

## Purpose

Dedicated enterprise AI infrastructure.

---

# Core Responsibilities

* document intelligence,
* retrieval,
* orchestration,
* embeddings,
* AI generation,
* governance.

---

# AI Platform Structure

```text id="ai-platform-structure"
services/
workers/
pipelines/
shared/
models/
storage/
knowledge/
infra/
```

---

# AI Service Architecture

---

# 1. gateway-service

## Responsibility

AI API entrypoint.

---

# Features

* auth validation,
* rate limiting,
* request routing,
* policy enforcement.

---

# 2. orchestration-service

## Responsibility

AI workflow coordination.

---

# Features

* planning,
* routing,
* orchestration,
* fallback strategy.

---

# 3. parser-service

## Responsibility

Document intelligence.

---

# Features

* PDF extraction,
* OCR,
* layout analysis,
* table extraction,
* image extraction.

---

# Core Tools

* PyMuPDF
* Unstructured
* Camelot

---

# 4. semantic-chunk-service

## Responsibility

Educational semantic chunking.

---

# Features

* curriculum-aware chunking,
* hierarchy preservation,
* pedagogy segmentation.

---

# 5. metadata-service

## Responsibility

AI enrichment.

---

# Features

* taxonomy tagging,
* difficulty classification,
* learning style tagging.

---

# 6. embedding-service

## Responsibility

Embedding generation.

---

# Features

* text embeddings,
* image embeddings,
* formula embeddings,
* vector indexing.

---

# 7. retrieval-service

## Responsibility

Semantic retrieval.

---

# Features

* hybrid retrieval,
* metadata filtering,
* query understanding,
* context building.

---

# 8. reranking-service

## Responsibility

Improve retrieval quality.

---

# Features

* cross-encoder reranking,
* relevance scoring.

---

# 9. generation-service

## Responsibility

LLM answer generation.

---

# Features

* prompt building,
* hallucination validation,
* citation generation.

---

# 10. vision-service

## Responsibility

Multimodal visual intelligence.

---

# Features

* image captioning,
* OCR enhancement,
* diagram understanding.

---

# 11. moderation-service

## Responsibility

AI governance & safety.

---

# Features

* moderation,
* prompt filtering,
* hallucination policy.

---

# 12. audit-service

## Responsibility

Enterprise auditability.

---

# Features

* prompt logs,
* retrieval logs,
* answer logs,
* token tracking.

---

# 13. monitoring-service

## Responsibility

Observability.

---

# Features

* metrics,
* tracing,
* dashboards,
* health monitoring.

---

# Communication Architecture

---

# Sync Communication

## Recommended

Gunakan:

* gRPC

---

# Use Cases

* Go ↔ Python communication,
* internal AI service calls.

---

# Async Communication

## Recommended

Gunakan:

* RabbitMQ
  atau
* Apache Kafka

---

# Use Cases

* ingestion,
* OCR,
* embeddings,
* indexing,
* AI workflows.

---

# Event-Driven Pipeline

```text id="event-driven-pipeline"
PDF Upload
   ↓
DOCUMENT.UPLOAD.REQUESTED
   ↓
Parser Worker
   ↓
DOCUMENT.PARSE.COMPLETED
   ↓
Chunk Worker
   ↓
CHUNK.GENERATION.COMPLETED
   ↓
Embedding Worker
   ↓
EMBEDDING.INDEX.COMPLETED
```

---

# Storage Architecture

---

# 1. PostgreSQL

## Purpose

Relational data.

---

# Stores

* audit,
* metadata,
* jobs,
* AI requests.

---

# 2. Qdrant

## Purpose

Vector retrieval.

---

# Stores

* embeddings,
* semantic chunks,
* retrieval metadata.

---

# Technology

* Qdrant

---

# 3. MinIO

## Purpose

Object storage.

---

# Stores

* PDF,
* OCR result,
* extracted images,
* intermediate artifacts.

---

# Technology

* MinIO

---

# Knowledge Architecture

---

# Knowledge Namespace

```text id="knowledge-namespace"
knowledge/
├── cp/
├── atp/
├── buku_guru/
├── buku_siswa/
├── asesmen/
├── p5/
└── ontology/
```

---

# Purpose

Membuat:

* retrieval lebih akurat,
* metadata lebih konsisten,
* educational reasoning lebih baik.

---

# AI Pipeline Architecture

---

# Document Intelligence Pipeline

```text id="document-pipeline"
PDF
 ↓
Parser
 ├── Text Extraction
 ├── OCR
 ├── Layout Detection
 ├── Table Extraction
 └── Image Extraction
 ↓
Semantic Chunking
 ↓
Metadata Enrichment
 ↓
Embedding Generation
 ↓
Qdrant Indexing
```

---

# Retrieval Pipeline

```text id="retrieval-pipeline"
Question
 ↓
Intent Detection
 ↓
Metadata Filtering
 ↓
Vector Retrieval
 ↓
Hybrid Search
 ↓
Reranking
 ↓
Context Builder
 ↓
Generation
```

---

# Scalability Strategy

---

# Horizontal Scaling

Semua service harus:

* stateless,
* horizontally scalable.

---

# GPU Isolation

GPU-intensive workloads dipisah:

* reranking,
* vision,
* embeddings.

---

# Queue-Based Scaling

Workers dapat:

* autoscale,
* parallel processing.

---

# Security Architecture

---

# Rules

## Frontend tidak boleh akses AI langsung

---

## Semua request harus melalui backend

---

## Service-to-service auth wajib

---

# Security Components

* JWT validation,
* RBAC,
* API gateway,
* signed URLs,
* encrypted storage.

---

# Observability Architecture

---

# Stack

* Prometheus
* Grafana
* OpenTelemetry

---

# Required Metrics

```text id="metrics-list"
retrieval_latency
OCR_failure_rate
embedding_duration
queue_lag
hallucination_rate
token_usage
```

---

# Governance Architecture

---

# Required Features

* prompt logging,
* retrieval logging,
* moderation,
* auditability,
* explainability.

---

# Audit Requirements

Semua AI responses wajib:

* traceable,
* reproducible,
* auditable.

---

# Deployment Architecture

---

# Recommended Stack

* Docker
* Kubernetes

---

# Environment

```text id="deployment-env"
dev
staging
production
```

---

# CI/CD

## Recommended

* [GitHub Actions](https://github.com/features/actions?utm_source=chatgpt.com)
* [Argo CD](https://argo-cd.readthedocs.io/?utm_source=chatgpt.com)

---

# Core Engineering Priorities

## 1. Document Intelligence

Foundation system.

---

## 2. Semantic Chunking

Core retrieval quality.

---

## 3. Metadata Engineering

Core explainability.

---

## 4. Retrieval Engineering

Core AI accuracy.

---

## 5. Governance & Observability

Mandatory for enterprise AI.

---

# Most Important Architectural Insight

Enterprise educational AI systems berhasil bukan karena:

* model terbesar,
* GPU terbanyak,
* chatbot paling kompleks.

Tetapi karena:

* retrieval architecture,
* metadata engineering,
* semantic chunking,
* observability,
* governance,
* orchestration.

Karena itu:

* AI platform harus diperlakukan sebagai infrastructure system,
  bukan sekadar feature tambahan di backend.
