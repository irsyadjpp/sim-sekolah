Berikut struktur final yang saya sarankan untuk **production-ready enterprise educational AI platform** Anda.

Ini bukan sekadar “folder rapi”, tetapi sudah mempertimbangkan:

* scalability,
* observability,
* AI governance,
* async processing,
* multimodal document intelligence,
* retrieval engineering,
* enterprise maintainability.

---

# FINAL STRUCTURE — AI PLATFORM

```text id="s2ux1f"
ai-platform/
│
├── services/
│   │
│   ├── gateway-service/
│   ├── orchestration-service/
│   ├── parser-service/
│   ├── semantic-chunk-service/
│   ├── metadata-service/
│   ├── embedding-service/
│   ├── retrieval-service/
│   ├── generation-service/
│   ├── audit-service/
│   ├── monitoring-service/
│   └── notification-service/
│
├── shared/
│   │
│   ├── schemas/
│   ├── contracts/
│   ├── events/
│   ├── enums/
│   ├── exceptions/
│   ├── logging/
│   ├── telemetry/
│   ├── security/
│   ├── utils/
│   ├── configs/
│   └── constants/
│
├── knowledge/
│   │
│   ├── cp/
│   ├── atp/
│   ├── buku_guru/
│   ├── buku_siswa/
│   ├── modul_ajar/
│   ├── asesmen/
│   ├── p5/
│   ├── media/
│   └── temporary/
│
├── infra/
│   │
│   ├── docker/
│   ├── kubernetes/
│   ├── kafka/
│   ├── rabbitmq/
│   ├── qdrant/
│   ├── postgres/
│   ├── minio/
│   ├── prometheus/
│   ├── grafana/
│   ├── tempo/
│   ├── loki/
│   └── nginx/
│
├── deployment/
│   │
│   ├── dev/
│   ├── staging/
│   ├── production/
│   └── scripts/
│
├── docs/
│   │
│   ├── architecture/
│   ├── api/
│   ├── prompts/
│   ├── retrieval/
│   ├── governance/
│   ├── chunking/
│   └── runbooks/
│
├── notebooks/
│   │
│   ├── experiments/
│   ├── embedding-tests/
│   ├── retrieval-evals/
│   ├── reranking/
│   └── model-benchmarks/
│
├── scripts/
│   │
│   ├── migration/
│   ├── reindex/
│   ├── repair/
│   ├── ingestion/
│   └── benchmark/
│
├── tests/
│   │
│   ├── integration/
│   ├── e2e/
│   ├── retrieval/
│   ├── parsing/
│   ├── chunking/
│   └── load/
│
├── .github/
│
├── Makefile
├── pyproject.toml
├── README.md
└── .env
```

---

# PENJELASAN TIAP SERVICE

---

# 1. gateway-service

API entrypoint untuk:

* frontend,
* ERP Spring Boot,
* mobile apps.

---

# Tugas

* auth validation,
* JWT validation,
* rate limiting,
* request routing,
* API aggregation.

---

# Stack

* FastAPI
* NGINX/API Gateway.

---

# 2. orchestration-service

INI OTAK AI SYSTEM.

---

# Tugas

* workflow orchestration,
* routing,
* policy,
* fallback,
* AI strategy.

---

# Contoh

```text id="rvbyb9"
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

---

# Struktur

```text id="2vf0h2"
orchestration-service/
├── workflows/
├── routers/
├── coordinators/
├── planners/
├── evaluators/
└── policies/
```

---

# 3. parser-service

Document intelligence foundation.

---

# Struktur

```text id="4jml8j"
parser-service/
├── extractors/
│   ├── text/
│   ├── table/
│   ├── image/
│   ├── ocr/
│   └── layout/
│
├── pipelines/
├── workers/
├── schemas/
└── normalizers/
```

---

# Tooling

* PyMuPDF
* Unstructured
* Camelot
* Nougat

---

# 4. semantic-chunk-service

MOST IMPORTANT SERVICE.

---

# Tugas

Mengubah:

* parsed document
  menjadi:
* educational semantic chunks.

---

# Struktur

```text id="l9k1m4"
semantic-chunk-service/
├── chunkers/
├── hierarchy/
├── classifiers/
├── pedagogy/
├── taxonomy/
└── builders/
```

---

# Jenis chunk

```text id="ed1x7h"
- competency
- activity
- assessment
- inquiry
- reflection
- experiment
- lesson_plan
```

---

# 5. metadata-service

AI enrichment.

---

# Struktur

```text id="jlwm2e"
metadata-service/
├── enrichers/
├── classifiers/
├── taxonomy/
├── difficulty/
└── standards/
```

---

# Output

```json id="jlwm3f"
{
  "difficulty": "easy",
  "taxonomy": "analyze",
  "learning_style": ["visual"]
}
```

---

# 6. embedding-service

---

# Struktur

```text id="jlwm4g"
embedding-service/
├── embedders/
│   ├── text/
│   ├── image/
│   ├── table/
│   └── formula/
│
├── vectorizers/
├── indexers/
└── workers/
```

---

# Tooling

* BAAI/bge-m3
* intfloat/multilingual-e5-large

---

# 7. retrieval-service

Core retrieval intelligence.

---

# Struktur

```text id="jlwm5h"
retrieval-service/
├── retrievers/
├── hybrid/
├── rerankers/
├── filters/
├── query-builders/
└── context-builders/
```

---

# Tooling

* Qdrant

---

# Retrieval Strategy

```text id="jlwm6i"
semantic
+
metadata filter
+
hybrid search
+
reranking
```

---

# 8. generation-service

LLM generation layer.

---

# Struktur

```text id="jlwm7j"
generation-service/
├── prompts/
├── templates/
├── citations/
├── validators/
├── hallucination/
└── providers/
```

---

# Model Strategy

## Cloud

* GPT,
* Claude.

## Local

* Qwen,
* Mistral,
* Llama.

---

# 9. audit-service

WAJIB enterprise AI.

---

# Menyimpan

* prompt,
* retrieval result,
* answer,
* latency,
* token usage,
* model version.

---

# Struktur

```text id="jlwm8k"
audit-service/
├── prompt-logs/
├── retrieval-logs/
├── answer-logs/
└── compliance/
```

---

# 10. monitoring-service

---

# Stack

* Prometheus
* Grafana
* OpenTelemetry

---

# Metrics

```text id="jlwm9l"
- retrieval latency
- chunk quality
- OCR errors
- token usage
- hallucination rate
```

---

# KNOWLEDGE STRUCTURE

Ini bukan sekadar folder storage.

Ini domain knowledge namespace.

---

# FINAL KNOWLEDGE STRUCTURE

```text id="jlwm0m"
knowledge/
├── cp/
│   ├── ipa/
│   ├── ips/
│   └── matematika/
│
├── atp/
├── buku_guru/
├── buku_siswa/
├── modul_ajar/
├── asesmen/
├── p5/
│
├── media/
│   ├── images/
│   ├── tables/
│   └── formulas/
│
└── temporary/
```

---

# EVENT ARCHITECTURE

KRITIKAL.

---

# Semua service berbasis event

```text id="jlwm1n"
DOCUMENT_UPLOADED
DOCUMENT_PARSED
CHUNKS_CREATED
METADATA_ENRICHED
EMBEDDINGS_CREATED
INDEXING_COMPLETED
```

---

# Queue

Gunakan:

* RabbitMQ
  atau
* Apache Kafka

---

# OBJECT STORAGE

Gunakan:

MinIO

---

# Simpan

```text id="jlwm2o"
- original PDF
- extracted images
- OCR output
- chunk snapshot
- embeddings snapshot
```

---

# DATABASE STRATEGY

---

# PostgreSQL

Untuk:

* business data,
* metadata relational,
* audit,
* jobs.

---

# Qdrant

Untuk:

* vector retrieval.

---

# RECOMMENDED DEPLOYMENT

---

# Container

* Docker

---

# Orchestration

* Kubernetes

---

# CI/CD

* GitHub Actions
* ArgoCD.

---

# PALING PENTING

Kalau saya lead engineer:

Saya akan memprioritaskan:

```text id="jlwm3p"
1. document intelligence
2. semantic chunking
3. metadata engineering
4. retrieval engineering
5. observability
```

Bukan:

* agent,
* chatbot UI,
* AI gimmick.

Karena untuk enterprise educational AI:

> retrieval architecture adalah core product sebenarnya.
