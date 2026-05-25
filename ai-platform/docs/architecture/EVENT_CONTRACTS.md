# EVENT CONTRACTS

## Purpose

Dokumen ini mendefinisikan standar event-driven architecture pada Enterprise Educational AI Platform.

Tujuan utama:

* memastikan komunikasi antar service konsisten,
* membuat pipeline scalable,
* mendukung asynchronous AI workloads,
* memastikan observability dan auditability,
* mempermudah retry dan recovery.

---

# Architecture Overview

AI Platform menggunakan:

* event-driven architecture,
* asynchronous processing,
* distributed workers,
* queue-based pipelines.

---

# Core Principles

## 1. Events are Immutable

Event tidak boleh diubah setelah dipublish.

Jika ada perubahan:

* buat event baru,
* jangan overwrite event lama.

---

## 2. Events Must Be Traceable

Setiap event wajib memiliki:

```json
{
  "event_id": "uuid",
  "trace_id": "uuid",
  "timestamp": "ISO8601"
}
```

---

## 3. Events Must Be Replayable

Event harus dapat:

* di-replay,
* di-reprocess,
* digunakan untuk recovery.

---

## 4. Services Must Be Loosely Coupled

Service tidak boleh:

* memanggil internal logic service lain,
* mengakses database service lain.

Komunikasi:

* via event,
* atau gRPC contract resmi.

---

# Event Bus Strategy

## Recommended Queue

Gunakan salah satu:

### Option A — RabbitMQ

Cocok untuk:

* task queue,
* ingestion pipeline,
* worker orchestration.

---

### Option B — Apache Kafka

Cocok untuk:

* high throughput,
* event streaming,
* replay event,
* observability.

---

# Recommended Architecture

## Hybrid Strategy

```text
RabbitMQ
→ task orchestration

Kafka
→ analytics + event stream
```

---

# Event Naming Convention

Gunakan format:

```text
DOMAIN.ACTION.STATUS
```

---

# Examples

```text
DOCUMENT.UPLOAD.REQUESTED
DOCUMENT.PARSE.COMPLETED
CHUNK.GENERATION.COMPLETED
EMBEDDING.INDEX.FAILED
RETRIEVAL.REQUESTED
GENERATION.COMPLETED
```

---

# Naming Rules

## Gunakan uppercase

✅ Benar:

```text
DOCUMENT.PARSE.COMPLETED
```

❌ Salah:

```text
document_parse_completed
```

---

# Event Payload Standard

Semua event wajib memiliki struktur berikut:

```json
{
  "event_id": "uuid",
  "trace_id": "uuid",
  "event_name": "DOCUMENT.PARSE.COMPLETED",
  "timestamp": "2026-05-25T10:00:00Z",
  "producer": "parser-service",
  "version": "1.0",
  "payload": {}
}
```

---

# Field Definitions

| Field      | Description              |
| ---------- | ------------------------ |
| event_id   | unique event identifier  |
| trace_id   | distributed tracing ID   |
| event_name | event type               |
| timestamp  | event creation timestamp |
| producer   | originating service      |
| version    | event schema version     |
| payload    | business payload         |

---

# Traceability Standard

Semua pipeline wajib membawa:

```text
trace_id
document_id
request_id
user_id
school_id
```

---

# Required Headers

## Queue Headers

```json
{
  "trace_id": "uuid",
  "retry_count": 0,
  "source_service": "parser-service"
}
```

---

# Event Versioning Strategy

## Rules

* jangan modify schema existing,
* gunakan semantic versioning,
* backward compatibility wajib dijaga.

---

# Example

```text
DOCUMENT.PARSE.COMPLETED.v1
DOCUMENT.PARSE.COMPLETED.v2
```

---

# Core Event Categories

---

# 1. Document Events

## Purpose

Mengatur seluruh document ingestion pipeline.

---

# Events

```text
DOCUMENT.UPLOAD.REQUESTED
DOCUMENT.UPLOAD.COMPLETED
DOCUMENT.PARSE.REQUESTED
DOCUMENT.PARSE.COMPLETED
DOCUMENT.PARSE.FAILED
```

---

# Example Payload

```json
{
  "document_id": "doc_001",
  "document_type": "buku_guru",
  "subject": "IPA",
  "grade": 4,
  "storage_path": "/raw/file.pdf"
}
```

---

# 2. OCR Events

## Purpose

Mengatur OCR processing.

---

# Events

```text
OCR.REQUESTED
OCR.COMPLETED
OCR.FAILED
```

---

# Payload Example

```json
{
  "document_id": "doc_001",
  "page": 12,
  "language": "id"
}
```

---

# 3. Chunking Events

## Purpose

Semantic chunk generation pipeline.

---

# Events

```text
CHUNK.GENERATION.REQUESTED
CHUNK.GENERATION.COMPLETED
CHUNK.GENERATION.FAILED
```

---

# Payload Example

```json
{
  "document_id": "doc_001",
  "chunk_strategy": "curriculum-aware",
  "total_chunks": 124
}
```

---

# 4. Metadata Events

## Purpose

AI enrichment pipeline.

---

# Events

```text
METADATA.ENRICHMENT.REQUESTED
METADATA.ENRICHMENT.COMPLETED
METADATA.ENRICHMENT.FAILED
```

---

# Payload Example

```json
{
  "chunk_id": "chunk_001",
  "taxonomy": "analyze",
  "difficulty": "medium"
}
```

---

# 5. Embedding Events

## Purpose

Embedding generation dan indexing.

---

# Events

```text
EMBEDDING.GENERATION.REQUESTED
EMBEDDING.GENERATION.COMPLETED
EMBEDDING.INDEX.REQUESTED
EMBEDDING.INDEX.COMPLETED
EMBEDDING.INDEX.FAILED
```

---

# Payload Example

```json
{
  "chunk_id": "chunk_001",
  "embedding_model": "bge-m3",
  "vector_dimension": 1024
}
```

---

# 6. Retrieval Events

## Purpose

Tracking retrieval pipeline.

---

# Events

```text
RETRIEVAL.REQUESTED
RETRIEVAL.COMPLETED
RETRIEVAL.RERANKED
```

---

# Payload Example

```json
{
  "query": "apa itu energi panas",
  "top_k": 10,
  "filters": {
    "grade": 4,
    "subject": "IPA"
  }
}
```

---

# 7. Generation Events

## Purpose

Tracking AI generation pipeline.

---

# Events

```text
GENERATION.REQUESTED
GENERATION.COMPLETED
GENERATION.FAILED
```

---

# Payload Example

```json
{
  "model": "gpt-4.1",
  "token_usage": 1200,
  "context_chunks": 5
}
```

---

# 8. Moderation Events

## Purpose

AI safety tracking.

---

# Events

```text
MODERATION.REQUESTED
MODERATION.FLAGGED
MODERATION.APPROVED
```

---

# Retry Strategy

## Rules

Retry hanya untuk:

* transient errors,
* network issues,
* timeout.

---

# Jangan Retry

* invalid schema,
* malformed payload,
* corrupted document.

---

# Retry Policy

| Retry | Delay |
| ----- | ----- |
| 1     | 5s    |
| 2     | 30s   |
| 3     | 2m    |
| 4     | 10m   |

---

# Dead Letter Queue (DLQ)

## Purpose

Menampung failed events.

---

# Queue Naming

```text
dlq.document.parse
dlq.embedding.index
dlq.ocr.processing
```

---

# DLQ Rules

Semua DLQ wajib:

* observable,
* searchable,
* replayable.

---

# Idempotency Rules

Semua consumer wajib idempotent.

---

# Example

Jika:

```text
DOCUMENT.PARSE.COMPLETED
```

diproses 2 kali,
hasil harus tetap konsisten.

---

# Correlation ID Strategy

## Purpose

Distributed tracing.

---

# Rules

Gunakan:

* trace_id
* request_id
* correlation_id

di seluruh pipeline.

---

# Example Flow

```text
DOCUMENT.UPLOAD.REQUESTED
      ↓
DOCUMENT.PARSE.COMPLETED
      ↓
CHUNK.GENERATION.COMPLETED
      ↓
EMBEDDING.INDEX.COMPLETED
```

Semua event harus punya:

```text
trace_id sama
```

---

# Event Ordering Rules

## Critical Events

Harus ordered:

```text
DOCUMENT.PARSE.COMPLETED
↓
CHUNK.GENERATION.REQUESTED
```

---

# Non-Critical Events

Boleh asynchronous parallel:

* OCR,
* image extraction,
* metadata enrichment.

---

# Event Size Policy

## Rules

Event payload harus kecil.

---

# Jangan Kirim

❌ Full PDF

❌ Full image binary

❌ Large embedding vectors

---

# Gunakan Reference

✅ Benar:

```json
{
  "storage_path": "/parsed/doc_001.json"
}
```

---

# Security Policy

## Rules

Event tidak boleh mengandung:

* raw JWT,
* API keys,
* secrets,
* credentials.

---

# Sensitive Data Handling

Gunakan:

* encrypted storage,
* secure references,
* signed URLs.

---

# Observability Requirements

Semua event wajib:

* logged,
* traceable,
* monitorable.

---

# Metrics

## Required Metrics

```text
event_publish_rate
event_failure_rate
consumer_lag
retry_count
DLQ_count
```

---

# OpenTelemetry Integration

Semua producer & consumer wajib:

* inject trace_id,
* support distributed tracing.

---

# Queue Topology Recommendation

## RabbitMQ

```text
document.exchange
embedding.exchange
retrieval.exchange
generation.exchange
```

---

# Kafka Topics

```text
document-events
embedding-events
retrieval-events
generation-events
audit-events
```

---

# Event Consumer Guidelines

## Consumer Rules

### 1. Idempotent

### 2. Retry-safe

### 3. Stateless

### 4. Observable

### 5. Timeout-aware

---

# Event Producer Guidelines

## Producer Rules

### 1. Validate payload

### 2. Include metadata

### 3. Include trace_id

### 4. Use versioning

### 5. Avoid oversized payload

---

# Failure Handling Strategy

## Parsing Failure

```text
DOCUMENT.PARSE.FAILED
↓
DLQ
↓
manual inspection
```

---

# Embedding Failure

```text
retry
↓
fallback model
↓
DLQ
```

---

# Governance Requirements

Semua event wajib:

* auditable,
* reproducible,
* traceable.

---

# Compliance Rules

## Wajib menyimpan:

* event logs,
* timestamps,
* producer identity,
* retry history.

---

# Recommended Event Lifecycle

```text
REQUESTED
↓
PROCESSING
↓
COMPLETED
```

atau:

```text
REQUESTED
↓
FAILED
↓
RETRY
↓
DLQ
```

---

# Final Recommendations

## Prioritize

### 1. Traceability

### 2. Replayability

### 3. Idempotency

### 4. Observability

### 5. Loose coupling

---

# Most Important Insight

Event-driven AI systems gagal biasanya karena:

* event tidak konsisten,
* retry chaos,
* tidak ada tracing,
* payload terlalu besar,
* coupling antar service terlalu tinggi.

Karena itu:

* event contract,
* schema governance,
* observability,

adalah core engineering foundation untuk enterprise AI platform.
