Berikut cara saya membangun **Dedicated AI Services (Python)** dari nol sampai production-ready untuk sistem Anda.

Saya akan buat pendekatan yang realistis untuk tim enterprise kecil–menengah:

* scalable,
* maintainable,
* async,
* observable,
* mudah di-debug,
* mudah diintegrasikan ke Spring Boot.

---

# TARGET AKHIR

Kita akan membangun:

```text id="u3d4o9"
ai-platform/
├── api-gateway/
├── parser-service/
├── embedding-service/
├── retrieval-service/
├── generation-service/
├── metadata-service/
├── orchestration-service/
├── shared/
├── infra/
└── deployment/
```

---

# PHASE 0 — Tentukan Filosofi Architecture

Sebelum coding:

## Jangan membuat:

* 1 service besar,
* 1 Python app monster,
* semua AI logic di satu tempat.

---

# Gunakan prinsip:

## “Single Responsibility AI Service”

Artinya:

| Service               | Tanggung Jawab  |
| --------------------- | --------------- |
| parser-service        | parsing PDF     |
| embedding-service     | embedding       |
| retrieval-service     | search          |
| generation-service    | generate answer |
| metadata-service      | enrichment      |
| orchestration-service | workflow AI     |

---

# PHASE 1 — Setup Foundation

---

# STEP 1 — Pilih Framework Python

Saya sarankan:

## Gunakan:

* FastAPI

Kenapa:

* async native,
* cepat,
* cocok microservices,
* OpenAPI otomatis,
* production proven.

---

# STEP 2 — Setup Monorepo

Buat:

```text id="m0wqcr"
ai-platform/
```

---

# STEP 3 — Struktur Awal

```text id="0u4h9z"
ai-platform/
├── services/
│   ├── parser-service/
│   ├── embedding-service/
│   ├── retrieval-service/
│   ├── generation-service/
│   └── orchestration-service/
│
├── shared/
│   ├── models/
│   ├── utils/
│   ├── logging/
│   └── configs/
│
├── infra/
│   ├── docker/
│   ├── kafka/
│   └── monitoring/
│
└── deployment/
```

---

# STEP 4 — Python Package Manager

Saya sarankan:

## Gunakan:

* uv

lebih modern daripada pip.

---

# STEP 5 — Standardisasi Semua Service

Semua service WAJIB punya:

```text id="tk0o9q"
app/
├── api/
├── core/
├── services/
├── workers/
├── models/
├── repositories/
└── main.py
```

---

# PHASE 2 — Parser Service

Ini service paling penting.

---

# STEP 6 — Parser Service Pertama

## Tujuan

Input:

* PDF

Output:

* structured document JSON.

---

# Install

Gunakan:

* PyMuPDF
* Unstructured

---

# STEP 7 — Buat Flow Parsing Dasar

```text id="jlwmgm"
PDF
 ↓
Extract pages
 ↓
Extract blocks
 ↓
Detect layout
 ↓
Normalize
 ↓
Store JSON
```

---

# STEP 8 — Raw Extraction Layer

Gunakan:

PyMuPDF

Extract:

* text,
* bbox,
* font,
* image refs.

---

# Output

```json id="t9ub8y"
{
  "page": 1,
  "blocks": [
    {
      "type": "text",
      "bbox": [0,0,100,100],
      "text": "Energi"
    }
  ]
}
```

---

# STEP 9 — Layout Intelligence

Gunakan:

Unstructured

Deteksi:

* Title,
* Header,
* Paragraph,
* Table,
* Figure.

---

# STEP 10 — Buat Unified Document Schema

KRITIKAL.

Jangan simpan hasil parsing mentah.

---

# Buat schema standar

Contoh:

```json id="px26hl"
{
  "document_id": "uuid",
  "page": 1,
  "element_type": "title",
  "content": "Energi",
  "metadata": {
    "subject": "IPA",
    "grade": 4
  }
}
```

---

# PHASE 3 — Queue System

---

# STEP 11 — Tambahkan Queue

Gunakan:

* RabbitMQ
  atau
* Apache Kafka

Saya sarankan awal:

* RabbitMQ lebih mudah.

---

# Flow

```text id="vrvkkx"
Upload PDF
   ↓
Queue
   ↓
Parser Worker
```

---

# STEP 12 — Worker Architecture

Jangan parsing di request HTTP.

SALAH BESAR.

---

# Yang benar:

```text id="7hdf25"
HTTP Upload
   ↓
Create Job
   ↓
Push Queue
   ↓
Background Worker
```

---

# PHASE 4 — Embedding Service

---

# STEP 13 — Buat Embedding Service

Service khusus embedding.

---

# Install model

Gunakan:

* BAAI/bge-m3

atau

* intfloat/multilingual-e5-large

---

# STEP 14 — Embedding Pipeline

```text id="d8y0nh"
Chunk
 ↓
Normalize text
 ↓
Generate embedding
 ↓
Store vector
```

---

# STEP 15 — Vector Store

Gunakan:

Qdrant

---

# Collection Strategy

Jangan satu collection besar.

Pisahkan:

```text id="6v4mh7"
curriculum_chunks
teacher_books
student_books
assessment_items
lesson_plans
```

---

# STEP 16 — Metadata Schema

WAJIB konsisten.

---

# Contoh metadata

```json id="hrp1zq"
{
  "subject": "IPA",
  "grade": 4,
  "phase": "B",
  "topic": "Energi",
  "chunk_type": "activity"
}
```

---

# PHASE 5 — Retrieval Service

---

# STEP 17 — Retrieval Service

Service khusus search.

---

# Tanggung jawab

* semantic search,
* metadata filter,
* reranking.

---

# STEP 18 — Hybrid Retrieval

Jangan hanya vector search.

Gabungkan:

* semantic,
* BM25,
* metadata filter.

---

# STEP 19 — Reranking

Tambahkan reranker.

Karena embedding saja tidak cukup.

---

# Flow

```text id="wb3bx8"
Top 50 retrieval
   ↓
Rerank
   ↓
Top 5 context
```

---

# PHASE 6 — Generation Service

---

# STEP 20 — Generation Service

Service khusus LLM.

---

# Tanggung jawab

* prompt building,
* answer generation,
* citation,
* hallucination guard.

---

# STEP 21 — Structured Prompting

Jangan prompt random.

Buat template system prompt.

---

# Contoh

```text id="vh6rdu"
You are curriculum assistant.
Only answer from retrieved context.
Always cite source.
```

---

# STEP 22 — Citation System

Setiap chunk WAJIB punya:

* source,
* page,
* chunk id.

---

# STEP 23 — Hallucination Guard

Jika retrieval confidence rendah:

* jangan jawab pasti.

---

# PHASE 7 — Orchestration Service

Ini “otak” AI system.

---

# STEP 24 — Buat Orchestrator

Gunakan:

* LangGraph
  atau custom orchestrator.

---

# Flow

```text id="k7uxmx"
Question
 ↓
Intent Detection
 ↓
Retrieval
 ↓
Reranking
 ↓
Prompt Build
 ↓
Generation
 ↓
Validation
```

---

# PHASE 8 — Observability

WAJIB.

---

# STEP 25 — Structured Logging

Gunakan JSON logging.

---

# STEP 26 — Monitoring

Gunakan:

* Prometheus
* Grafana

---

# STEP 27 — Tracing

Gunakan:

* OpenTelemetry

Trace:

* retrieval latency,
* LLM latency,
* parsing latency.

---

# PHASE 9 — Security

---

# STEP 28 — API Security

Gunakan:

* JWT,
* service-to-service auth,
* API gateway validation.

---

# STEP 29 — AI Governance

Simpan:

* prompt,
* response,
* retrieved chunks,
* model,
* token usage.

---

# PHASE 10 — Production Deployment

---

# STEP 30 — Dockerize Semua Service

Semua service:

* independent container,
* independent scaling.

---

# STEP 31 — Kubernetes

Gunakan:

* HPA,
* autoscaling worker,
* queue-based scaling.

---

# STEP 32 — CI/CD

Gunakan:

* GitHub Actions,
* GitLab CI,
* ArgoCD.

---

# REKOMENDASI PALING PENTING

---

# Jangan mulai dari:

```text id="yv3mfd"
chatbot UI
```

---

# Mulai dari:

```text id="kh9s2k"
1. parsing pipeline
2. metadata schema
3. retrieval quality
```

Karena:

> retrieval bagus + metadata bagus = AI bagus.

---

# Urutan Pengerjaan yang Benar

## Minggu 1–2

* parser-service
* queue
* MinIO
* PostgreSQL

---

## Minggu 3–4

* chunking
* embedding
* Qdrant

---

## Minggu 5–6

* retrieval
* reranking
* metadata filter

---

## Minggu 7–8

* generation service
* orchestration
* observability

---

# Saran Senior AI Engineer

Kalau project ini serius production enterprise:

## Jangan buru-buru ke:

* AI agent,
* multi-agent,
* autonomous AI.

---

# Prioritaskan dulu:

```text id="z7d8oo"
document intelligence
+
retrieval engineering
+
governance
```

Karena itu fondasi sebenarnya dari enterprise education AI.
