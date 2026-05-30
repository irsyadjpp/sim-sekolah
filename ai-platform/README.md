# AI-Native Curriculum & Deep Learning Intelligence Platform

Production-grade Educational Intelligence Platform for Kurikulum Merdeka and Pembelajaran Mendalam.

---

## Overview

AI-Native Curriculum & Deep Learning Intelligence Platform adalah platform AI khusus pendidikan yang dirancang untuk:

- curriculum-aware AI,
- pedagogy-aware retrieval,
- competency-aware learning,
- multimodal educational document intelligence,
- adaptive learning systems,
- assessment intelligence,
- educational governance,
- character development (Profil Pelajar Pancasila),
- deep learning pedagogy (Pembelajaran Mendalam).

Platform ini bukan sekadar:
- chatbot PDF,
- generic RAG,
- AI assistant biasa.

Tetapi dirancang sebagai:

> Educational Cognitive Infrastructure

yang memahami:
- kurikulum (Kurikulum Merdeka)
- pedagogi (Pembelajaran Mendalam)
- asesmen
- kompetensi
- learning progression
- character development
- school quality improvement

---

## Core Principles

### 1. Curriculum-Aware

AI memahami:
- CP
- ATP
- fase
- grade
- struktur Kurikulum Merdeka

---

### 2. Pedagogy-Aware

AI memahami:
- inquiry learning
- project-based learning
- differentiated learning
- deep learning

---

### 3. Competency-Aware

AI memahami:
- competency progression
- mastery learning
- remediation
- prerequisite relationship

---

### 4. Multimodal Intelligence

AI mampu memproses:
- text
- tables
- formulas
- diagrams
- educational images
- scanned documents

---

### 5. Governance-First

Platform memiliki:
- auditability
- traceability
- retrieval logging
- AI observability
- hallucination protection

---

## High-Level Architecture

```text
Frontend (ReactJS)
        ↓
Backend API (Go)
        ↓
AI Platform Monolith (Python - FastAPI)
        ↓
Domain-Driven Bounded Contexts
        ↓
Educational Intelligence Layer
        ↓
Retrieval + Vector Infrastructure
```

---

## Main Components

### Frontend

Frontend hanya menangani:

- UI
- dashboard
- user interaction

Tech:

- ReactJS

---

### Backend Core

Backend utama menangani:

- business logic
- authentication
- school management
- ERP features
- API orchestration

Tech:

- GoLang

---

### AI Platform

Dedicated AI infrastructure.

Tech:

- Python
- FastAPI
- Qdrant
- PyMuPDF
- Unstructured
- Transformers

---

## AI Platform Responsibilities

AI Platform menangani:

- document ingestion and parsing
- OCR and multimodal extraction
- semantic chunking
- embeddings and vector search
- retrieval and reranking
- assessment generation
- recommendation systems
- adaptive learning
- educational AI orchestration
- character development tracking
- school quality evaluation

---

## Main Architecture

```text
AI PLATFORM MONOLITH (Domain-Driven Bounded Contexts)
│
├── standards-domain/              # Foundation - Kurikulum Merdeka Standards
│   ├── kurikulum_merdeka/          # CP, ATP, Modul Ajar standards
│   ├── profil_pelajar_pancasila/    # 6 dimensions Profil Pelajar Pancasila
│   ├── capaian_pembelajaran/        # Learning objectives, competencies
│   ├── standards_repository/       # Standards database & validation
│   └── standards_api/              # National standards integration
│
├── curriculum-domain/            # Kurikulum Management
│   ├── cp_management/             # CP (Curriculum Program)
│   ├── atp_generation/            # ATP (Annual Teaching Plan)
│   ├── modul_ajar_creation/        # Modul Ajar generator
│   └── standards_alignment/         # Kurikulum Merdeka alignment validation
│
├── assessment-domain/             # Assessment & Evaluation
│   ├── assessment_generation/       # Task generation
│   ├── rubric_creation/            # Rubric creation & management
│   ├── evaluation/                  # Performance evaluation
│   └── progress_tracking/           # Student progress
│
├── learning-domain/               # Deep Learning Intelligence
│   ├── adaptive_learning/           # Personalized learning paths
│   ├── differentiated_learning/      # Differentiated instruction
│   ├── mastery_tracking/            # Learning mastery depth
│   ├── progression/                # Learning progression
│   └── deep_learning_pedagogy/      # Pembelajaran Mendalam Layer
│       ├── reflection_engine/        # Reflection & self-regulation
│       ├── metacognition_engine/      # Metacognitive analysis
│       └── project_based_learning/    # P5 & project learning
│
├── teacher-domain/                 # Teacher Primary User
│   ├── teacher_workflows/           # Teacher Workflow Layer
│   │   ├── modul_ajar_workflow/      # Modul Ajar creation workflow
│   │   ├── cp_atp_workflow/          # CP → ATP workflow
│   │   ├── assessment_workflow/      # Assessment workflow
│   │   └── remediation_workflow/    # Remediation workflow
│   ├── planning_assistant/           # AI planning assistant
│   └── resource_recommendation/      # Resource & activity recommendations
│
├── student-domain/                 # Student Learning Experience
│   ├── learning_journal/             # Learning journal & reflection
│   ├── progress_monitoring/         # Progress & mastery tracking
│   ├── reflection_engine/            # Reflection & self-regulation
│   ├── self_regulation/             # Self-regulation tracking
│   └── student_dashboard/           # Student dashboard
│
├── character-domain/               # Character Development
│   ├── character_assessment/         # Profil Pelajar Pancasila assessment
│   ├── character_reporting/          # Character development reporting
│   └── value_tracking/              # Value development tracking
│
├── learning_objectives/            # TP Intelligence Domain
│   ├── tp_parser.py                 # TP parsing
│   ├── tp_mapper.py                 # TP to ATP mapping
│   ├── tp_progression.py            # TP progression tracking
│   ├── tp_mastery.py                # TP mastery assessment
│   ├── tp_assessment_linker.py      # TP to assessment linking
│   ├── tp_activity_linker.py        # TP to activity linking
│   └── tp_validator.py              # TP validation
│
├── school_curriculum/              # KSP Intelligence
│   ├── context_analysis.py          # School context analysis
│   ├── swot_engine.py               # SWOT analysis
│   ├── school_profile_generator.py  # School profile generation
│   ├── vision_mission_generator.py  # Vision & mission generation
│   ├── curriculum_structure_generator.py  # Curriculum structure
│   └── annual_ksp_review.py         # Annual KSP review
│
├── reporting/                      # Reporting Intelligence
│   ├── report_card_generator.py     # Report card generation
│   ├── narrative_feedback_generator.py  # Narrative feedback
│   └── competency_summary_generator.py  # Competency summaries
│
├── school_quality/                 # School Quality Intelligence
│   ├── evaluation_engine.py         # School evaluation
│   ├── improvement_recommendation.py  # Improvement recommendations
│   ├── teacher_development_recommendation.py  # Teacher development
│   └── rapor_pendidikan_analytics.py  # Rapor Pendidikan analytics
│
├── ai_core/                        # AI Layer Separation
│   ├── llm/                        # LLM providers & management
│   ├── embeddings/                  # Embedding models & providers
│   ├── reranking/                   # Reranking strategies
│   ├── agents/                      # AI Agents (teacher, student, curriculum, assessment)
│   ├── reasoning/                   # Reasoning chains
│   ├── memory/                      # Memory systems (vector, episodic, semantic)
│   └── orchestration/                # AI orchestration
│
├── content_processing/              # Content Processing
│   ├── ingestion/                  # Document ingestion
│   ├── parsing/                     # Text, figure extraction
│   ├── chunking/                    # Semantic chunking
│   └── enrichment/                  # Content enrichment
│
├── support/                       # Support Services
│   ├── observability/               # Monitoring & analytics
│   ├── governance/                  # Audit & compliance
│   └── notification/               # Notifications
│
└── api/                            # API Layer (FastAPI)
    ├── content_processing/          # Content processing endpoints
    ├── document_ingestion/          # Document ingestion endpoints
    ├── intelligence/                # Educational intelligence endpoints
    └── support/                     # Support domain endpoints
```

---

## Educational Intelligence Layer

### standards-domain (Foundation)

Validasi:
- CP (Capaian Pembelajaran)
- ATP (Alur Tujuan Pembelajaran)
- phase alignment
- grade alignment
- Kurikulum Merdeka standards
- Profil Pelajar Pancasila dimensions

---

### curriculum-domain

Menganalisis:
- CP management
- ATP generation
- Modul Ajar creation
- standards alignment

---

### assessment-domain

Membangun:
- formative assessment
- HOTS questions
- rubric generation
- competency evaluation
- performance evaluation
- progress tracking

---

### learning-domain

Mendeteksi:
- mastery progression
- prerequisite gaps
- remediation needs
- adaptive learning paths
- differentiated learning
- deep learning pedagogy (Pembelajaran Mendalam)
- reflection & self-regulation
- metacognition
- project-based learning (P5)

---

### teacher-domain

Workflow orchestration:
- Modul Ajar creation workflow
- CP → ATP workflow
- Assessment workflow
- Remediation workflow
- Planning assistant
- Resource recommendations

---

### student-domain

Student experience:
- Learning journal
- Progress monitoring
- Reflection & self-regulation
- Self-assessment
- Student dashboard

---

### character-domain

Character development:
- Profil Pelajar Pancasila assessment
- Character reporting
- Value tracking

---

### learning_objectives (TP Intelligence)

TP management:
- TP parsing
- TP to ATP mapping
- TP progression tracking
- TP mastery assessment
- TP to assessment linking
- TP to activity linking
- TP validation

---

### school_curriculum (KSP Intelligence)

School curriculum:
- School context analysis
- SWOT analysis
- School profile generation
- Vision & mission generation
- Curriculum structure
- Annual KSP review

---

### reporting

Reporting intelligence:
- Report card generation
- Narrative feedback generation
- Competency summary generation

---

### school_quality

School quality:
- School evaluation
- Improvement recommendations
- Teacher development recommendations
- Rapor Pendidikan analytics

---

## Document Intelligence Pipeline

```text
PDF
 ↓
Document Analyzer
 ├── Text Extractor
 ├── Table Extractor
 ├── Image Extractor
 ├── OCR Engine
 └── Layout Detector
 ↓
Semantic Chunk Builder
 ↓
Embedding Pipeline
 ↓
Vector Database
```

---

## Parsing Stack

### PDF Processing

- PyMuPDF

---

### Layout Intelligence

- Unstructured

---

### Table Extraction

- Camelot

---

### OCR

- Tesseract OCR

---

### Formula Extraction

- Nougat OCR

---

## Knowledge Structure

```text
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

## Semantic Chunking Strategy

Platform menggunakan:

### Curriculum-Aware Semantic Chunking

Bukan:

- fixed chunk size
- naive splitting

---

### Chunking Based On

- competency
- activity
- assessment
- inquiry
- reflection
- learning objective
- cognitive level

---

### Example Chunk Metadata

```json
{
  "subject": "IPA",
  "grade": 4,
  "phase": "B",
  "competency": "memahami perpindahan panas",
  "pedagogy_type": "inquiry",
  "cognitive_level": "analysis",
  "assessment_type": "formatif"
}
```

---

## Retrieval Architecture

### Hybrid Retrieval

```text
semantic similarity
+
metadata filtering
+
pedagogy filtering
+
competency filtering
+
reranking
```

---

## Vector Database

### Qdrant

Digunakan untuk:

- semantic retrieval
- metadata filtering
- multimodal retrieval

---

## Database Strategy

### PostgreSQL

Untuk:

- relational business data
- metadata
- governance

---

### Qdrant

Untuk:

- vector search
- retrieval infrastructure

---

### MinIO

Untuk:

- PDFs
- images
- extracted assets
- snapshots

---

## AI Model Strategy

### Cloud Models

Digunakan untuk:

- reasoning
- generation

Examples:

- GPT-4.1
- Claude

---

### Local Models

Digunakan untuk:

- metadata extraction
- classification
- lightweight NLP

Examples:

- Qwen
- Mistral
- Llama

---

## Embedding Strategy

### Text Embedding

- BAAI/bge-m3
- multilingual-e5-large

---

### Formula Embedding

Dedicated formula embedding pipeline

---

### Image Embedding

Multimodal embedding pipeline

---

## Queue Architecture

Semua processing bersifat asynchronous.

### Pipeline

```text
PDF Upload
   ↓
Queue
   ↓
Parsing Worker
   ↓
Embedding Worker
   ↓
Indexing Worker
```

---

### Queue Technologies

- Kafka
- RabbitMQ

---

## AI Governance

### Mandatory Features

- audit log
- retrieval log
- prompt log
- AI traceability
- hallucination monitoring

---

## Hallucination Guard

Validasi:

- curriculum alignment
- competency alignment
- phase alignment
- assessment validity

---

## Security

### Authentication

- JWT

---

### Authorization

- RBAC

---

### Internal Security

- mTLS
- service authentication

---

### Encryption

- TLS
- encrypted storage

---

## Observability

### Monitoring Stack

- Prometheus
- Grafana
- OpenTelemetry

---

### Metrics

- retrieval latency
- hallucination rate
- embedding latency
- OCR failures
- retrieval precision

---

## Deployment Strategy

### Recommended

- Kubernetes
- Docker
- Helm

---

### Environment Separation

- local
- development
- staging
- production

---

## Recommended Tech Stack

| Layer          | Technology           |
| -------------- | -------------------- |
| Frontend       | ReactJS              |
| Backend        | GoLang               |
| AI Platform    | Python               |
| API            | FastAPI              |
| Queue          | Kafka / RabbitMQ     |
| Database       | PostgreSQL           |
| Vector DB      | Qdrant               |
| Object Storage | MinIO                |
| Monitoring     | Prometheus + Grafana |

---

## Folder Structure

```text
ai-platform/
├── docs/                          # Documentation (all markdown files)
├── monolith/                      # Main application code (monolith mode)
│   ├── app/
│   │   ├── standards-domain/      # Kurikulum Merdeka standards foundation
│   │   ├── curriculum-domain/      # Curriculum management
│   │   ├── assessment-domain/     # Assessment & evaluation
│   │   ├── learning-domain/       # Deep learning pedagogy
│   │   ├── teacher-domain/        # Teacher workflows & tools
│   │   ├── student-domain/        # Student learning experience
│   │   ├── character-domain/      # Character development
│   │   ├── learning_objectives/    # TP intelligence
│   │   ├── school_curriculum/     # KSP intelligence
│   │   ├── reporting/             # Reporting intelligence
│   │   ├── school_quality/        # School quality intelligence
│   │   ├── ai_core/               # AI layer (LLM, embeddings, agents)
│   │   ├── api/                   # FastAPI routes
│   │   ├── services/              # Business logic services
│   │   ├── chunkers/              # Semantic chunking
│   │   ├── extractors/            # Data extraction
│   │   ├── validators/            # Validation logic

infrastructure/                    # Centralized infrastructure configuration
├── docker/                        # Docker configurations
│   ├── base/                     # Base Dockerfiles
│   └── services/                 # Service-specific Dockerfiles
├── compose/                       # Docker Compose files
│   ├── sim-sekolah/              # SIM Sekolah stack
│   ├── ai-platform/              # AI Platform stacks
│   │   ├── docker-compose.yml    # Base microservices
│   │   ├── docker-compose.monolith.yml # Monolith
│   │   ├── dev/                 # Development overrides
│   │   ├── staging/              # Staging overrides
│   │   └── production/           # Production overrides
│   └── shared/                   # Shared infrastructure services
├── kubernetes/                    # Kubernetes manifests
│   ├── sim-sekolah/              # SIM Sekolah K8s
│   ├── ai-platform/              # AI Platform K8s
│   └── shared/                   # Shared K8s resources
├── monitoring/                    # Monitoring configurations
│   ├── grafana/                  # Grafana dashboards
│   ├── prometheus/               # Prometheus config
│   ├── loki/                     # Loki log aggregation
│   └── tempo/                    # Tempo distributed tracing
├── services/                      # Service configurations
│   ├── postgres/                 # PostgreSQL config
│   ├── redis/                    # Redis config
│   ├── rabbitmq/                 # RabbitMQ config
│   ├── qdrant/                   # Qdrant config
│   ├── minio/                    # MinIO config
│   └── nginx/                    # Nginx config
└── scripts/                       # Infrastructure scripts
    ├── setup/                    # Setup scripts
    ├── backup/                   # Backup scripts
    └── migration/                # Migration scripts
├── sdk/                           # Client SDK for external integration
├── shared/                        # Shared libraries and utilities
├── scripts/                       # Utility scripts
├── pipelines/                     # CI/CD pipelines
├── tests/                         # Test suites
├── workers/                       # Background job workers
├── models/                        # ML model storage
├── knowledge/                     # Knowledge base and reference materials
├── storage/                       # Storage configurations
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt                # Python dependencies
├── pyproject.toml                 # Project configuration
├── Makefile                       # Build automation
└── README.md                      # This file
```

---

## Design Philosophy

Platform ini dirancang berdasarkan prinsip:

```text
retrieval quality
>
model size
```

Karena dalam educational AI:

- grounding,
- pedagogy,
- curriculum alignment,
- competency structure

lebih penting daripada:

- model AI terbesar.

---

## Implementation Status

### Completed Domains (100%)

Based on GAP_ANALYSIS_PROGRESS.md (2026-05-30):

| Domain | Status | Progress |
|--------|--------|----------|
| TP Intelligence Domain | ✅ Completed | 100% |
| Standards & Regulation Engine | ✅ Completed | 100% |
| KSP Intelligence | ✅ Completed | 100% |
| Reflection Intelligence | ✅ Completed | 100% |
| Deep Learning Intelligence | ✅ Completed | 100% |
| Reporting Intelligence | ✅ Completed | 100% |
| School Quality Intelligence | ✅ Completed | 100% |

**Overall Progress: 100%**

All GAP_ANALYSIS.md items have been successfully implemented.

### Phase Completion

- Phase 1 (Critical Foundations): ✅ Completed (76%)
- Phase 2 (Domain Decomposition & Core Components): ✅ Completed (80%)
- Phase 3 (Integration & Architecture Cleanup): In Progress

---

## Architecture Evolution

### From Microservices to Domain-Driven Monolith

The platform has evolved from a microservice architecture to a **domain-driven monolith with bounded contexts** to address critical architecture problems:

- Service/Engine explosion causing ambiguity
- Domain intelligence scattered across services
- Missing teacher workflow layer
- AI layer not clearly separated
- Missing Deep Learning Pedagogy Layer
- Missing Standards Core as foundation

### Current Architecture Benefits

- **Domain-Driven Bounded Contexts**: Clear separation of concerns
- **Teacher-Workflow Centric**: Aligned with actual teacher workflows
- **User-Value First**: Focus on delivering value to users
- **Simple Before Scaling**: Start simple, scale when needed
- **Monolith Mode**: All services run in single FastAPI application
- **Hybrid Capability**: Can deploy as microservices when needed

---

## What This Platform Is NOT

❌ generic chatbot

❌ simple RAG

❌ PDF QA system

❌ MVP AI stack

❌ hackathon architecture

---

## What This Platform IS

✅ AI-Native Curriculum & Deep Learning Intelligence Platform

✅ Domain-Driven Monolith with Bounded Contexts

✅ Kurikulum Merdeka-Aligned

✅ Pembelajaran Mendalam-Compliant

✅ Educational Cognitive Infrastructure

✅ Adaptive Learning System

✅ Assessment Intelligence Platform

✅ Character Development Platform (Profil Pelajar Pancasila)

✅ School Quality Intelligence Platform

✅ Enterprise AI Architecture

---

## Long-Term Vision

Platform ini dirancang untuk mendukung:

- adaptive learning,
- competency tracing,
- personalized education,
- AI-powered curriculum systems,
- educational analytics,
- school intelligence infrastructure,
- character development tracking,
- deep learning pedagogy implementation,
- school quality improvement,
- comprehensive educational governance.

---

## Production Readiness

Platform ini dirancang dengan:

- scalability,
- observability,
- governance,
- maintainability,
- enterprise reliability,
- domain-driven architecture,
- bounded context separation,
- comprehensive testing,
- CI/CD pipelines.

---

## Most Important Insight

Educational AI bukan tentang:

```text
chatting with documents
```

Tetapi tentang:

```text
understanding learning systems
```

Karena inti pendidikan bukan:

- retrieval,

melainkan:

- pembelajaran,
- kompetensi,
- perkembangan,
- asesmen,
- pedagogi,
- karakter,
- kualitas sekolah,
- kurikulum yang selaras.

---

## Documentation

For detailed documentation, see the `docs/` folder:

- `GAP_ANALYSIS.md` - Gap analysis and implementation priorities
- `GAP_ANALYSIS_PROGRESS.md` - Implementation progress (100% completed)
- `AI_PLATFORM_ARCHITECTURE.md` - Detailed architecture documentation
- `IMPLEMENTATION_ACTION_ITEMS.md` - Implementation roadmap
- `NAMING_CONVENTIONS.md` - Naming conventions
- `PHASE_1_2_COMPREHENSIVE_OVERVIEW.md` - Phase 1 & 2 completion summary
- And more...

---

## Getting Started

See `docs/README.md` for detailed setup and deployment instructions.

---

## License

[Add license information here]