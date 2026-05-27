Berikut struktur final yang disarankan untuk **production-ready enterprise educational AI platform** untuk Kurikulum Merdeka.

Ini bukan sekadar "folder rapi", tetapi sudah mempertimbangkan:

* scalability,
* observability,
* AI governance,
* async processing,
* multimodal document intelligence,
* retrieval engineering,
* educational intelligence,
* enterprise maintainability.

---

# FINAL STRUCTURE — AI PLATFORM

```text
ai-platform/
│
├── services/                          # 13 Microservices
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
│   ├── moderation-service/
│   ├── reranking-service/
│   ├── vision-service/
│   └── notification-service/
│
├── educational-intelligence/          # 7 Educational AI Engines
│   ├── curriculum-engine/
│   ├── pedagogy-engine/
│   ├── assessment-engine/
│   ├── learning-progression-engine/
│   ├── learning-graph-engine/
│   ├── adaptive-learning-engine/
│   └── recommendation-engine/
│
├── ai-agents/                         # 4 Specialized AI Agents
│   ├── teacher-agent/
│   ├── student-learning-agent/
│   ├── curriculum-agent/
│   └── assessment-agent/
│
├── hallucination-guard/               # 6 AI Validators
│   ├── curriculum-validator/
│   ├── pedagogy-validator/
│   ├── competency-validator/
│   ├── assessment-validator/
│   ├── phase-validator/
│   └── retrieval-grounding-validator/
│
├── educational-observability/         # 6 Monitoring Systems
│   ├── learning-analytics/
│   ├── competency-analytics/
│   ├── assessment-quality-monitoring/
│   ├── retrieval-quality-monitoring/
│   ├── pedagogy-effectiveness-monitoring/
│   └── hallucination-monitoring/
│
├── educational-ontology/               # 6 Knowledge Structures
│   ├── curriculum-ontology/
│   ├── pedagogy-ontology/
│   ├── competency-ontology/
│   ├── assessment-ontology/
│   ├── learning-objective-ontology/
│   └── concept-hierarchy/
│
├── retrieval-enhancement/             # 6 Specialized Retrieval Systems
│   ├── curriculum-aware-reranker/
│   ├── pedagogy-aware-retrieval/
│   ├── competency-aware-retrieval/
│   ├── assessment-aware-retrieval/
│   ├── contextual-retrieval/
│   └── learning-style-retrieval/
│
├── semantic-enrichment/               # 6 Tagging Systems
│   ├── competency-tagging/
│   ├── pedagogy-tagging/
│   ├── assessment-tagging/
│   ├── cognitive-level-tagging/
│   ├── learning-objective-tagging/
│   └── deep-learning-tagging/
│
├── shared/                            # Shared Components
│   ├── schemas/
│   ├── contracts/
│   ├── events/
│   ├── enums/
│   ├── exceptions/
│   ├── logging/
│   ├── telemetry/
│   ├── security/
│   ├── middleware/
│   ├── utils/
│   ├── configs/
│   ├── constants/
│   ├── grpc/
│   ├── models/
│   ├── observability/
│   ├── prompts/
│   └── telemetry/
│
├── knowledge/                         # 9 Domain Knowledge Repositories
│   ├── cp/                           # Capaian Pembelajaran
│   ├── atp/                          # Alur Tujuan Pembelajaran
│   ├── buku_guru/                    # Buku Panduan Guru
│   ├── buku_siswa/                   # Buku Siswa
│   ├── modul_ajar/                   # Modul Ajar
│   ├── asesmen/                      # Bank Asesmen
│   ├── p5/                           # Projek P5
│   ├── media/                        # Educational Media
│   ├── ontology/                     # Knowledge Graphs
│   └── temporary/                    # Temporary Storage
│
├── models/                            # 7 Model Categories
│   ├── embeddings/
│   ├── classifiers/
│   ├── rerankers/
│   ├── local-llm/
│   ├── OCR/
│   ├── vision/
│   └── moderation/
│
├── storage/                           # 11 Storage Layers
│   ├── raw/                          # Original Documents
│   ├── parsed/                       # Parsed Content
│   ├── OCR/                          # OCR Results
│   ├── chunks/                       # Semantic Chunks
│   ├── embeddings/                   # Vector Embeddings
│   ├── enriched/                     # Enriched Metadata
│   ├── tables/                       # Extracted Tables
│   ├── images/                       # Extracted Images
│   ├── formulas/                     # Mathematical Formulas
│   ├── normalized/                   # Normalized Content
│   └── snapshots/                    # System Snapshots
│
├── workers/                           # 7 Async Worker Types
│   ├── document-workers/
│   ├── OCR-workers/
│   ├── embedding-workers/
│   ├── enrichment-workers/
│   ├── indexing-workers/
│   ├── reranking-workers/
│   └── cleanup-workers/
│
├── pipelines/                         # 9 Processing Pipelines
│   ├── ingestion/
│   ├── parsing/
│   ├── chunking/
│   ├── embeddings/
│   ├── enrichment/
│   ├── retrieval/
│   ├── reranking/
│   ├── generation/
│   └── indexing/
│
├── scripts/                           # 20+ Automation Scripts
│   ├── backup/
│   ├── benchmark/
│   ├── bootstrap/
│   ├── cleanup/
│   ├── deployment/
│   ├── embedding/
│   ├── ingestion/
│   ├── maintenance/
│   ├── migration/
│   ├── migrations/
│   ├── monitoring/
│   ├── qdrant/
│   ├── recovery/
│   ├── reindex/
│   ├── repair/
│   ├── security/
│   ├── setup/
│   ├── testing/
│   └── utils/
│
├── infra/                             # 12 Infrastructure Components
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
├── deployment/                        # Multi-Environment Deployment
│   ├── dev/
│   ├── staging/
│   ├── production/
│   └── scripts/
│
├── docs/                              # 15 Documentation Categories
│   ├── API/
│   ├── architecture/
│   ├── chunking/
│   ├── deployment/
│   ├── engineering/
│   ├── governance/
│   ├── ingestion/
│   ├── knowledge/
│   ├── models/
│   ├── observability/
│   ├── prompts/
│   ├── retrieval/
│   ├── runbooks/
│   └── security/
│
├── tests/                             # 9 Testing Categories
│   ├── chunking/
│   ├── e2e/
│   ├── embeddings/
│   ├── generation/
│   ├── integration/
│   ├── load/
│   ├── parsing/
│   ├── reranking/
│   └── retrieval/
│
├── notebooks/                         # 9 R&D Notebook Categories
│   ├── benchmarks/
│   ├── embedding-tests/
│   ├── experiments/
│   ├── model-benchmarks/
│   ├── OCR/
│   ├── parsing/
│   ├── reranking/
│   └── retrieval-evals/
│
├── .github/
│
├── Makefile
├── pyproject.toml
├── requirements.txt
├── README.md
└── .env
```

---

# PENJELASAN STRUKTUR UTAMA

---

## 1. SERVICES - 13 Microservices

### Core AI Services

**gateway-service** (Port 8002)
- API entrypoint untuk frontend, ERP Spring Boot, mobile apps
- Auth validation, JWT validation, rate limiting, request routing, API aggregation

**orchestration-service** (Port 8007)
- OTAK AI SYSTEM
- Workflow orchestration, routing, policy, fallback, AI strategy

**parser-service** (Port 8008)
- Document intelligence foundation
- PDF processing, OCR, table extraction, layout detection
- Tooling: PyMuPDF, Unstructured, Camelot, Nougat, Tesseract

**semantic-chunk-service** (Port 8011)
- MOST IMPORTANT SERVICE
- Curriculum-aware semantic chunking
- Mengubah parsed document menjadi educational semantic chunks

**metadata-service** (Port 8004)
- AI enrichment untuk tagging dan classification
- Difficulty assessment, taxonomy classification, learning style detection

**embedding-service** (Port 8001)
- Multimodal embeddings (text, image, table, formula)
- Tooling: BAAI/bge-m3, intfloat/multilingual-e5-large

**retrieval-service** (Port 8010)
- Core retrieval intelligence
- Hybrid retrieval dengan metadata filtering
- Tooling: Qdrant

**generation-service** (Port 8003)
- LLM generation layer dengan multiple providers
- Cloud: GPT, Claude | Local: Qwen, Mistral, Llama

### Governance Services

**audit-service** (Port 8000)
- WAJIB enterprise AI
- Logging, compliance, traceability
- Menyimpan prompt, retrieval result, answer, latency, token usage, model version

**monitoring-service** (Port 8006)
- Observability dengan Prometheus/Grafana/OpenTelemetry
- Metrics: retrieval latency, chunk quality, OCR errors, token usage, hallucination rate

**moderation-service** (Port 8005)
- Content moderation dan safety
- Toxicity detection, bias checking, content filtering

**reranking-service** (Port 8009)
- Advanced reranking untuk retrieval quality
- Multiple reranking strategies and models

### Specialized Services

**vision-service** (Port 8012)
- Image processing, OCR, diagram analysis
- Tooling: Tesseract, computer vision models

**notification-service**
- Event-driven notifications
- Email, push, in-app notifications

---

## 2. EDUCATIONAL INTELLIGENCE - 7 AI Engines

**curriculum-engine**
- Validasi CP, ATP, phase alignment, grade alignment
- Curriculum structure validation

**pedagogy-engine**
- Analisis inquiry learning, differentiated learning, deep learning
- Pedagogical context analysis

**assessment-engine**
- Formative assessment, HOTS questions, rubric generation
- Competency evaluation

**learning-progression-engine**
- Mastery progression detection
- Prerequisite gaps detection, remediation needs

**learning-graph-engine**
- Knowledge graph construction
- Competency graph, prerequisite graph, concept relationship

**adaptive-learning-engine**
- Personalized learning paths
- Adaptive content recommendation

**recommendation-engine**
- Content recommendation
- Learning resource suggestion

---

## 3. AI AGENTS - 4 Specialized Agents

**teacher-agent**
- Assistant untuk guru
- Lesson planning, assessment creation, student progress analysis

**student-learning-agent**
- Personalized learning companion
- Learning guidance, progress tracking, personalized support

**curriculum-agent**
- Curriculum expertise
- CP/ATP guidance, curriculum alignment checking

**assessment-agent**
- Assessment generation dan evaluation
- Question generation, rubric creation, assessment analytics

---

## 4. HALLUCINATION GUARD - 6 Validators

**curriculum-validator**
- Validasi kurikulum alignment
- CP/ATP compliance checking

**pedagogy-validator**
- Validasi pedagogical approach
- Teaching method appropriateness

**competency-validator**
- Validasi competency progression
- Mastery level verification

**assessment-validator**
- Validasi assessment quality
- HOTS verification, difficulty calibration

**phase-validator**
- Validasi phase appropriateness
- Phase alignment checking

**retrieval-grounding-validator**
- Validasi retrieval grounding
- Source verification, citation checking

---

## 5. EDUCATIONAL OBSERVABILITY - 6 Monitoring Systems

**learning-analytics**
- Student learning progress tracking
- Performance metrics, engagement analytics

**competency-analytics**
- Competency mastery analytics
- Progress tracking, gap analysis

**assessment-quality-monitoring**
- Assessment effectiveness monitoring
- Question quality analysis, difficulty calibration

**retrieval-quality-monitoring**
- Retrieval system performance
- Relevance scores, precision/recall tracking

**pedagogy-effectiveness-monitoring**
- Teaching method effectiveness
- Pedagogical approach analytics

**hallucination-monitoring**
- AI hallucination rate tracking
- Grounding verification, quality metrics

---

## 6. EDUCATIONAL ONTOLOGY - 6 Knowledge Structures

**curriculum-ontology**
- Struktur kurikulum
- CP/ATP hierarchy, subject organization

**pedagogy-ontology**
- Konsep pedagogis
- Teaching methods, learning strategies

**competency-ontology**
- Kompetensi hierarchy
- Skill progression, prerequisite relationships

**assessment-ontology**
- Tipe dan struktur asesmen
- Assessment categories, HOTS taxonomy

**learning-objective-ontology**
- Tujuan pembelajaran
- Objective hierarchy, cognitive levels

**concept-hierarchy**
- Hubungan konsep
- Knowledge graph, concept relationships

---

## 7. RETRIEVAL ENHANCEMENT - 6 Specialized Retrieval Systems

**curriculum-aware-reranker**
- Curriculum-based reranking
- CP/ATP alignment scoring

**pedagogy-aware-retrieval**
- Pedagogy-filtered retrieval
- Teaching method context

**competency-aware-retrieval**
- Competency-grounded retrieval
- Skill-based filtering

**assessment-aware-retrieval**
- Assessment-targeted retrieval
- Assessment type optimization

**contextual-retrieval**
- Context-aware search
- Learning context integration

**learning-style-retrieval**
- Learning style adaptive retrieval
- Personalized search results

---

## 8. SEMANTIC ENRICHMENT - 6 Tagging Systems

**competency-tagging**
- Auto-tag kompetensi
- Skill identification, competency mapping

**pedagogy-tagging**
- Tag pedagogical approach
- Teaching method classification

**assessment-tagging**
- Tag assessment type
- Assessment categorization

**cognitive-level-tagging**
- Tag taksonomi Bloom
- Cognitive level identification

**learning-objective-tagging**
- Tag tujuan pembelajaran
- Objective alignment

**deep-learning-tagging**
- Tag deep learning elements
- Higher-order thinking identification

---

## 9. MODELS - 7 Model Categories

**embeddings**
- Text, image, table, formula embedding models
- BAAI/bge-m3, multilingual-e5-large

**classifiers**
- Content classification models
- Educational content categorization

**rerankers**
- Reranking models
- Cross-encoders, mono-encoders

**local-llm**
- Local LLM models
- Qwen, Mistral, Llama

**OCR**
- OCR models
- Tesseract, specialized OCR

**vision**
- Computer vision models
- Image classification, diagram analysis

**moderation**
- Content moderation models
- Toxicity detection, bias checking

---

## 10. STORAGE - 11 Storage Layers

**raw/** - Original documents
**parsed/** - Parsed content
**OCR/** - OCR results
**chunks/** - Semantic chunks
**embeddings/** - Vector embeddings
**enriched/** - Enriched metadata
**tables/** - Extracted tables
**images/** - Extracted images
**formulas/** - Mathematical formulas
**normalized/** - Normalized content
**snapshots/** - System snapshots

---

## 11. WORKERS - 7 Async Worker Types

**document-workers** - Document processing
**OCR-workers** - OCR processing
**embedding-workers** - Embedding generation
**enrichment-workers** - Metadata enrichment
**indexing-workers** - Vector indexing
**reranking-workers** - Reranking jobs
**cleanup-workers** - Data maintenance

---

## 12. PIPELINES - 9 Processing Pipelines

**ingestion/** - Document ingestion pipeline
**parsing/** - Document parsing pipeline
**chunking/** - Semantic chunking pipeline
**embeddings/** - Embedding generation pipeline
**enrichment/** - Metadata enrichment pipeline
**retrieval/** - Retrieval pipeline
**reranking/** - Reranking pipeline
**generation/** - Content generation pipeline
**indexing/** - Vector indexing pipeline

---

## 13. INFRASTRUCTURE - 12 Components

**docker/** - Container configuration
**kubernetes/** - K8s manifests
**kafka/** - Event streaming
**rabbitmq/** - Message queuing
**qdrant/** - Vector database
**postgres/** - Relational database
**minio/** - Object storage
**prometheus/** - Metrics collection
**grafana/** - Visualization
**tempo/** - Distributed tracing
**loki/** - Log aggregation
**nginx/** - Reverse proxy/load balancer

---

## 14. KNOWLEDGE STRUCTURE - 9 Domain Repositories

**cp/** - Capaian Pembelajaran per mata pelajaran
**atp/** - Alur Tujuan Pembelajaran
**buku_guru/** - Buku panduan guru
**buku_siswa/** - Buku siswa
**modul_ajar/** - Modul ajar
**asesmen/** - Bank soal dan asesmen
**p5/** - Projek Penguatan Profil Pelajar Pancasila
**media/** - Educational media (images, videos, audio)
**ontology/** - Knowledge graphs dan semantic structures

---

## 15. SHARED COMPONENTS - 17 Categories

**schemas/** - Pydantic schemas
**contracts/** - Service contracts/interfaces
**events/** - Event definitions
**enums/** - Enumeration types
**exceptions/** - Custom exceptions
**logging/** - Logging configuration
**telemetry/** - OpenTelemetry setup
**security/** - Security utilities
**middleware/** - FastAPI middleware
**utils/** - Utility functions
**configs/** - Configuration management
**constants/** - Application constants
**grpc/** - gRPC definitions
**models/** - Shared data models
**observability/** - Observability utilities
**prompts/** - Prompt templates
**prompts/** - AI prompt management

---

# EVENT ARCHITECTURE

KRITIKAL untuk async processing.

```text
DOCUMENT_UPLOADED
DOCUMENT_PARSED
CHUNKS_CREATED
METADATA_ENRICHED
EMBEDDINGS_CREATED
INDEXING_COMPLETED
RETRIEVAL_EXECUTED
GENERATION_COMPLETED
VALIDATION_PASSED
```

---

# DEPLOYMENT STRATEGY

## Container
- Docker untuk containerization

## Orchestration
- Kubernetes untuk production orchestration

## CI/CD
- GitHub Actions
- ArgoCD untuk GitOps

## Environments
- dev, staging, production

---

# PRIORITAS PENGEMBANGAN

Kalau lead engineer, prioritas:

```text
1. document intelligence (parser-service, vision-service)
2. semantic chunking (semantic-chunk-service)
3. metadata engineering (metadata-service)
4. retrieval engineering (retrieval-service, reranking-service)
5. observability (monitoring-service, audit-service)
6. educational intelligence (curriculum-engine, pedagogy-engine)
7. AI governance (hallucination-guard, educational-observability)
```

Bukan:
- agent bells & whistles,
- chatbot UI,
- AI gimmick.

Karena untuk enterprise educational AI:

> retrieval architecture + educational intelligence adalah core product sebenarnya.

---

# KEY INSIGHTS

Platform ini dirancang sebagai **Educational Cognitive Infrastructure** yang:

1. **Memahami Kurikulum Merdeka** - bukan generic AI
2. **Curriculum-Aware** - CP, ATP, phase, grade alignment
3. **Pedagogy-Aware** - inquiry, differentiated, deep learning
4. **Competency-Aware** - mastery progression, prerequisite
5. **Multimodal** - text, tables, formulas, diagrams, images
6. **Governance-First** - auditability, traceability, observability
7. **Production-Ready** - scalable, observable, maintainable

Bukan sekadar chatbot PDF atau generic RAG system.