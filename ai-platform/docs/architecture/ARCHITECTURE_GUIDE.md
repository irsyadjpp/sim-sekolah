# AI Platform Architecture Documentation

# Enterprise Educational AI Platform

Dokumen ini menjelaskan struktur final dari `ai-platform` yang digunakan sebagai dedicated AI infrastructure untuk sistem pendidikan enterprise.

---

# Tujuan Platform

Platform ini dirancang untuk:

- document intelligence,
- multimodal educational retrieval,
- semantic chunking,
- AI orchestration,
- enterprise governance,
- scalable AI processing,
- observability,
- educational knowledge engineering.

Platform ini **tidak menangani frontend** dan tidak menjadi business ERP utama.

Arsitektur utama:

```text
React Frontend
      ↓
Golang Backend Platform
      ↓
AI Adapter Layer
      ↓
Python AI Platform
```

---

# Prinsip Arsitektur

## 1. Headless AI Infrastructure

AI Platform hanya:
- memproses AI,
- retrieval,
- orchestration,
- document intelligence.

Tidak menangani:
- frontend rendering,
- SSR,
- UI session.

---

## 2. Event-Driven Architecture

Semua processing besar berjalan asynchronous menggunakan queue.

Contoh:

```text
PDF Upload
   ↓
DOCUMENT_UPLOADED
   ↓
parser-service
   ↓
DOCUMENT_PARSED
   ↓
semantic-chunk-service
```

---

## 3. Single Responsibility Services

Setiap service hanya memiliki satu domain responsibility.

---

# Folder Structure Overview

```text
ai-platform/
├── services/
├── workers/
├── pipelines/
├── shared/
├── models/
├── storage/
├── knowledge/
├── infra/
├── deployment/
├── tests/
├── docs/
├── notebooks/
└── scripts/
```

---

# 1. services/

Berisi seluruh dedicated AI microservices.

## Guideline

- Setiap service harus independent.
- Setiap service memiliki Dockerfile sendiri.
- Tidak boleh business logic lintas domain.
- Semua komunikasi menggunakan gRPC atau event.

---

# gateway-service/

## Fungsi

Entry point internal AI platform.

## Responsibility

- request validation
- authentication
- policy enforcement
- request routing
- rate limiting

## Tidak boleh

- retrieval logic
- parsing logic
- embedding generation

---

# orchestration-service/

## Fungsi

Otak workflow AI platform.

## Responsibility

- workflow orchestration
- routing
- planning
- fallback strategy
- AI coordination

## Contoh Flow

```text
Question
 ↓
Intent Detection
 ↓
Retrieval Strategy
 ↓
Generation Strategy
 ↓
Validation
```

## Guideline

- Tidak boleh menyimpan vector.
- Tidak boleh melakukan parsing langsung.
- Fokus pada orchestration.

---

# parser-service/

## Fungsi

Document intelligence foundation.

## Responsibility

- PDF parsing
- OCR
- layout analysis
- image extraction
- table extraction

## Tools

- PyMuPDF
- Unstructured
- Camelot
- Nougat

## Output

Normalized document JSON.

## Guideline

- Jangan langsung chunking di parser.
- Simpan bbox dan page metadata.
- Semua extraction harus reproducible.

---

# semantic-chunk-service/

## Fungsi

Membangun educational semantic chunks.

## Responsibility

- hierarchical chunking
- curriculum-aware chunking
- pedagogy segmentation
- semantic grouping

## Chunk Examples

- activity
- assessment
- competency
- reflection
- inquiry
- experiment

## Guideline

JANGAN gunakan:
- character splitting,
- naive chunking.

WAJIB:
- preserve hierarchy,
- preserve educational semantics.

---

# metadata-service/

## Fungsi

AI enrichment layer.

## Responsibility

- difficulty classification
- taxonomy enrichment
- pedagogy tagging
- learning style tagging

## Output Example

```json
{
  "difficulty": "easy",
  "taxonomy": "analyze"
}
```

## Guideline

Metadata harus:
- searchable,
- consistent,
- explainable.

---

# embedding-service/

## Fungsi

Generate embeddings dan indexing.

## Responsibility

- text embedding
- table embedding
- image embedding
- formula embedding

## Guideline

Gunakan multi-embedding strategy.

Jangan:
- satu embedding untuk semua tipe data.

---

# retrieval-service/

## Fungsi

Semantic retrieval engine.

## Responsibility

- vector retrieval
- metadata filtering
- hybrid retrieval
- context building

## Guideline

Retrieval harus:
- explainable,
- traceable,
- filterable.

Jangan hanya:
- top-k similarity.

---

# reranking-service/

## Fungsi

Improve retrieval relevance.

## Responsibility

- reranking
- relevance scoring
- cross-encoder scoring

## Guideline

Pisahkan dari retrieval karena:
- GPU intensive,
- scaling berbeda.

---

# generation-service/

## Fungsi

LLM answer generation.

## Responsibility

- prompt building
- answer generation
- citation generation
- hallucination validation

## Guideline

Jawaban harus:
- memiliki source,
- traceable,
- grounded retrieval.

---

# vision-service/

## Fungsi

Multimodal visual intelligence.

## Responsibility

- image captioning
- diagram understanding
- OCR enhancement
- VLM integration

## Guideline

Semua image:
- harus punya metadata,
- harus traceable ke source document.

---

# moderation-service/

## Fungsi

AI safety dan governance.

## Responsibility

- content filtering
- hallucination policies
- prompt validation
- safety enforcement

---

# audit-service/

## Fungsi

Enterprise AI auditability.

## Responsibility

- prompt logs
- retrieval logs
- response logs
- token tracking
- compliance

## Guideline

Audit logs:
- immutable,
- searchable,
- timestamped.

---

# monitoring-service/

## Fungsi

Observability platform.

## Responsibility

- metrics
- tracing
- health monitoring
- dashboards

## Stack

- Prometheus
- Grafana
- OpenTelemetry

---

# 2. workers/

Berisi background asynchronous workers.

## Examples

- document-workers
- OCR-workers
- indexing-workers

## Guideline

Workers:
- stateless,
- retryable,
- queue-driven.

---

# 3. pipelines/

Berisi workflow orchestration pipeline.

## Examples

- ingestion
- retrieval
- chunking
- generation

## Guideline

Pipelines:
- deterministic,
- observable,
- replayable.

---

# 4. shared/

Berisi reusable shared components.

## Jangan masukkan

- business logic,
- service-specific logic.

## Contoh

- grpc contracts
- telemetry
- schemas
- prompts
- security

---

# 5. models/

Berisi AI models dan wrappers.

## Examples

- embeddings
- rerankers
- OCR
- vision
- local-llm

## Guideline

Pisahkan:
- inference layer,
- orchestration layer.

---

# 6. storage/

Berisi intermediate processing artifacts.

## Examples

- parsed
- chunks
- OCR
- embeddings

## Guideline

Storage digunakan untuk:
- replay pipeline,
- debugging,
- recovery,
- reindexing.

---

# 7. knowledge/

Knowledge namespace pendidikan.

## Examples

```text
knowledge/
├── cp/
├── atp/
├── buku_guru/
├── asesmen/
```

## Guideline

Knowledge harus:
- domain-aware,
- versioned,
- traceable.

---

# 8. infra/

Infrastructure configuration.

## Examples

- Kubernetes
- RabbitMQ
- Kafka
- Qdrant
- MinIO
- Prometheus

## Guideline

Semua infra:
- containerized,
- reproducible,
- environment-based.

---

# 9. deployment/

Deployment manifests.

## Environment

- dev
- staging
- production

## Guideline

Jangan deploy manual ke production.

Gunakan:
- CI/CD,
- GitOps.

---

# 10. tests/

Testing strategy.

## Types

- integration
- e2e
- retrieval
- load test

## Guideline

AI system wajib punya:
- retrieval evaluation,
- hallucination testing,
- benchmark dataset.

---

# 11. docs/

Berisi seluruh technical documentation.

## Wajib ada

- architecture
- governance
- prompts
- retrieval strategy
- chunking strategy

---

# 12. notebooks/

Research dan experimentation.

## Jangan digunakan untuk production logic.

---

# 13. scripts/

Operational utilities.

## Examples

- reindex
- migration
- benchmark
- cleanup

---

# Core Engineering Principles

# 1. Retrieval Quality > Model Size

Kualitas retrieval lebih penting daripada model terbesar.

---

# 2. Metadata Engineering is Critical

Metadata menentukan:
- filtering,
- explainability,
- governance.

---

# 3. Semantic Chunking is Core Intelligence

Chunking menentukan:
- retrieval quality,
- context quality,
- generation quality.

---

# 4. Observability is Mandatory

AI systems sulit di-debug tanpa:
- tracing,
- metrics,
- audit logs.

---

# 5. Governance is Required

Semua AI output harus:
- traceable,
- explainable,
- auditable.

---

# Recommended Communication Strategy

## Sync

Gunakan:
- gRPC

untuk:
- Go ↔ Python communication.

---

## Async

Gunakan:
- RabbitMQ atau Kafka

untuk:
- ingestion,
- embedding,
- indexing.

---

# Final Notes

Platform ini bukan:
- simple chatbot,
- LangChain demo,
- PDF QA app biasa.

Tetapi:

```text
Enterprise Educational Intelligence Platform
```

Fokus utama platform:

1. document intelligence
2. semantic chunking
3. metadata engineering
4. retrieval engineering
5. governance
6. observability
