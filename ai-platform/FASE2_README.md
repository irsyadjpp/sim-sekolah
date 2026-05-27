# Phase 2: Core Intelligence Engine - Implementation Complete

## Overview
Phase 2 implements the Core Intelligence Engine components for the AI Platform. This phase focuses on document processing, vision analysis, curriculum-aware chunking, and AI enrichment.

## Services Implemented

### 1. Parser Service (Port 8001)
**Location**: `services/parser-service/`

**Purpose**: Document intelligence for PDF, text, tables, images, and OCR processing

**Components**:
- `main.py` - Document intelligence API with parsing endpoints
- `parser_schemas.py` - Pydantic schemas for parsing requests/responses
- `extractors/` - Text, table, image, OCR, layout detection
- `normalizers/` - Content normalization
- `pipelines/` - Document processing pipeline

**Key Features**:
- PDF processing with text, table, and image extraction
- Tesseract OCR support for Indonesian and English
- Layout detection for structured content
- Content normalization for consistency

**Dependencies**:
- Tesseract OCR (Indonesian + English)
- PyPDF2, pdfplumber
- Pillow for image processing

---

### 2. Vision Service (Port 8002 internal, 8005 external)
**Location**: `services/vision-service/`

**Purpose**: Computer vision processing for educational content

**Components**:
- `main.py` - Vision processing API
- `vision_schemas.py` - Pydantic schemas for vision operations
- `OCR/` - OCR processing with Tesseract
- `VLM/` - Vision-language model integration
- `captioning/` - Image captioning
- `diagram_analysis/` - Diagram and chart analysis
- `embeddings/` - Image embeddings generation

**Key Features**:
- OCR with Indonesian and English support
- Image classification
- Image captioning
- Diagram analysis (charts, graphs, tables)
- Image embeddings for vector search

**Dependencies**:
- Tesseract OCR (Indonesian + English)
- OpenGL libraries for image processing
- PIL/Pillow

---

### 3. Semantic Chunk Service (Port 8003) ⭐ MOST IMPORTANT
**Location**: `services/semantic-chunk-service/`

**Purpose**: Curriculum-aware semantic chunking for Kurikulum Merdeka

**Components**:
- `main.py` - Curriculum-aware chunking API
- `chunking_schemas.py` - Pydantic schemas for chunking
- `chunkers/` - Competency, activity, assessment, inquiry, lesson plan chunkers
- `hierarchy/` - Hierarchy detection
- `pedagogy/` - Pedagogy classification
- `taxonomy/` - Taxonomy tagging
- `builders/` - Chunk construction
- `enrichers/` - Chunk enrichment

**Key Features**:
- **Curriculum-aware chunking** - NOT naive fixed-size splitting
- Chunking based on: competency, activity, assessment, inquiry, lesson plan
- Hierarchy detection for curriculum structure
- Pedagogy classification for learning approach
- Taxonomy tagging (Bloom's taxonomy)
- Chunk enrichment with metadata

**Why This is MOST IMPORTANT**:
- This is the bridge between raw content and educational intelligence
- Enables curriculum-aligned content processing
- Foundation for all downstream AI services (retrieval, generation, assessment)

---

### 4. Metadata Service (Port 8004)
**Location**: `services/metadata-service/`

**Purpose**: AI enrichment and tagging for educational content

**Components**:
- `main.py` - Enrichment API with orchestrator
- `schemas/metadata_schemas.py` - Pydantic schemas for enrichment
- `enrichers/` - All enrichment components:
  - `difficulty_classifier.py` - Easy/Medium/Hard classification
  - `taxonomy_classifier.py` - Bloom's taxonomy levels
  - `learning_style_detector.py` - Visual/Auditory/Reading/Kinesthetic
  - `competency_tagger.py` - KI-1 to KI-4 competencies
  - `pedagogy_tagger.py` - Pedagogical approaches
  - `assessment_tagger.py` - Assessment types

**Key Features**:
- Difficulty classification (Easy/Medium/Hard)
- Bloom's taxonomy classification (Remember to Create)
- Learning style detection (VARK model)
- Competency tagging (Kurikulum Merdeka KI-1 to KI-4)
- Pedagogy tagging (direct instruction, inquiry-based, project-based, etc.)
- Assessment tagging (diagnostic, formative, summative, performance-based)
- Batch enrichment support

**Enrichment Categories**:
- **Difficulty**: Based on cognitive complexity and language
- **Taxonomy**: Bloom's taxonomy cognitive levels
- **Learning Style**: VARK (Visual, Auditory, Reading, Kinesthetic)
- **Competency**: Kurikulum Merdeka core competencies (KI-1 to KI-4)
- **Pedagogy**: Teaching approaches (direct instruction, PBL, collaborative)
- **Assessment**: Assessment types (diagnostic, formative, summative)

---

## Docker Configuration

All services include Dockerfiles:

### Parser Service Dockerfile
- Base: Python 3.11-slim
- System: Tesseract OCR (Indonesian + English)
- Port: 8001

### Vision Service Dockerfile
- Base: Python 3.11-slim
- System: Tesseract OCR + OpenGL libraries
- Port: 8002 (internal), 8005 (external in docker-compose)

### Semantic Chunk Service Dockerfile
- Base: Python 3.11-slim
- System: Minimal
- Port: 8003

### Metadata Service Dockerfile
- Base: Python 3.11-slim
- System: Minimal
- Port: 8004

---

## Kubernetes Configuration

Each service has its own Kubernetes manifest:

- `infra/kubernetes/parser-service.yaml`
- `infra/kubernetes/vision-service.yaml`
- `infra/kubernetes/semantic-chunk-service.yaml`
- `infra/kubernetes/metadata-service.yaml`

Each includes:
- Deployment with replica configuration
- Service (ClusterIP)
- HorizontalPodAutoscaler (HPA)
- Resource limits and requests
- Health checks (liveness and readiness probes)

**Replica and Resource Configurations**:

| Service | Min Replicas | Max Replicas | Memory Request | Memory Limit |
|---------|--------------|--------------|----------------|--------------|
| Parser | 2 | 8 | 512Mi | 1Gi |
| Vision | 2 | 6 | 1Gi | 2Gi |
| Semantic Chunk | 3 | 10 | 512Mi | 1Gi |
| Metadata | 2 | 8 | 512Mi | 1Gi |

---

## Docker Compose Update

The `docker-compose.yml` has been updated with the four new services:

```yaml
services:
  parser-service:
    ports: "8001:8001"
    depends_on: [postgres, redis, rabbitmq, qdrant]
    
  vision-service:
    ports: "8005:8002"  # External:Internal to avoid conflict
    depends_on: [postgres, redis, rabbitmq, qdrant]
    
  semantic-chunk-service:
    ports: "8003:8003"
    depends_on: [postgres, redis, rabbitmq, qdrant]
    
  metadata-service:
    ports: "8004:8004"
    depends_on: [postgres, redis, rabbitmq, qdrant]
```

---

## Port Assignments

| Service | Internal Port | External Port |
|---------|---------------|---------------|
| Gateway | 8002 | 8002 |
| Parser | 8001 | 8001 |
| Vision | 8002 | 8005 |
| Semantic Chunk | 8003 | 8003 |
| Metadata | 8004 | 8004 |
| Monitoring | 8006 | 8006 |

---

## API Endpoints

### Parser Service (http://localhost:8001)
- `POST /api/v1/parse/document` - Parse document
- `POST /api/v1/parse/text` - Parse text
- `POST /api/v1/parse/tables` - Extract tables
- `POST /api/v1/parse/images` - Extract images
- `POST /api/v1/parse/ocr` - OCR processing
- `POST /api/v1/parse/layout` - Detect layout
- `POST /api/v1/parse/pipeline` - Full pipeline

### Vision Service (http://localhost:8005)
- `POST /api/v1/vision/ocr` - OCR processing
- `POST /api/v1/vision/classify` - Image classification
- `POST /api/v1/vision/caption` - Image captioning
- `POST /api/v1/vision/diagram` - Diagram analysis
- `POST /api/v1/vision/embeddings` - Image embeddings

### Semantic Chunk Service (http://localhost:8003)
- `POST /api/v1/chunk/competency` - Competency-based chunking
- `POST /api/v1/chunk/activity` - Activity-based chunking
- `POST /api/v1/chunk/assessment` - Assessment-based chunking
- `POST /api/v1/chunk/inquiry` - Inquiry-based chunking
- `POST /api/v1/chunk/lesson-plan` - Lesson plan chunking
- `POST /api/v1/chunk/auto` - Auto-detect and chunk

### Metadata Service (http://localhost:8004)
- `POST /api/v1/enrich` - Full enrichment orchestrator
- `POST /api/v1/enrich/difficulty` - Difficulty classification
- `POST /api/v1/enrich/taxonomy` - Bloom's taxonomy
- `POST /api/v1/enrich/learning-style` - Learning style detection
- `POST /api/v1/enrich/competency` - Competency tagging
- `POST /api/v1/enrich/pedagogy` - Pedagogy tagging
- `POST /api/v1/enrich/assessment` - Assessment tagging
- `POST /api/v1/enrich/batch` - Batch enrichment

---

## Architecture Flow

```
Raw Content (PDF, Text, Images)
    ↓
Parser Service
    ↓ [Parsed Content]
Vision Service
    ↓ [OCR, Image Features]
Semantic Chunk Service ⭐ (Most Important)
    ↓ [Curriculum-Aware Chunks]
Metadata Service
    ↓ [Enriched Chunks]
↓
Vector Database (Qdrant)
↓
Retrieval & Generation Services (Phase 3+)
```

---

## Next Steps (Phase 3)

According to `IMPLEMENTATION_PHASES.md`, Phase 3 covers:
- Embedding Service
- Retrieval Service
- Reranking Service

These services will build on the Core Intelligence Engine implemented in Phase 2.

## 🔄 Communication Architecture Update

**Status**: Priority 2 (RabbitMQ) and Priority 3 (gRPC) implementations complete.

### Architecture Transition

**Previous Architecture**:
- Direct REST API access to AI services
- Multiple external ports exposed
- Tight coupling between services

**Current Architecture**:
- Gateway Service as single entry point
- Backend (Go) handles business logic
- AI services communicate via gRPC/RabbitMQ
- Internal services no longer expose REST endpoints

### Communication Flow
```
External Client → Gateway (REST) → Backend (Go)
                                          ↓
                                    gRPC / RabbitMQ
                                          ↓
                                  AI Platform Services
```

### Service Communication

Each Phase 2 service now has:

**gRPC Server**:
- File: `app/grpc_server.py`
- Port: Service-specific (50051-50058)
- Methods: Defined in proto files

**RabbitMQ Consumer**:
- File: `app/consumer.py`
- Queue: Service-specific queue
- Message Types: Defined in rabbitmq_messages.py

**Service Ports**:
| Service | REST Port (deprecated) | gRPC Port | RabbitMQ Queue |
|---------|----------------------|-----------|---------------|
| Parser | 8001 | 50051 | parser.queue |
| Vision | 8005 | 50055 | vision.queue |
| Chunk | 8003 | 50056 | chunk.queue |
| Metadata | 8004 | 50057 | metadata.queue |

**Documentation**:
- RabbitMQ Implementation: `PRIORITY2_RABBITMQ_IMPLEMENTATION.md`
- gRPC Implementation: `PRIORITY3_GRPC_IMPLEMENTATION.md`
- Cleanup & Documentation: `PRIORITY4_CLEANUP_DOCUMENTATION.md`

---

## Usage

### Build and Run
```bash
# Build all services
docker-compose build

# Run all services
docker-compose up -d

# Check logs
docker-compose logs -f parser-service
docker-compose logs -f vision-service
docker-compose logs -f semantic-chunk-service
docker-compose logs -f metadata-service
```

### Test Services
```bash
# Health checks
curl http://localhost:8001/health  # Parser
curl http://localhost:8005/health  # Vision
curl http://localhost:8003/health  # Semantic Chunk
curl http://localhost:8004/health  # Metadata

# Example: Parse a document
curl -X POST http://localhost:8001/api/v1/parse/document \
  -H "Content-Type: application/json" \
  -d '{"document_id": "doc1", "file_path": "/path/to/file.pdf"}'

# Example: Enrich content
curl -X POST http://localhost:8004/api/v1/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "content1",
    "text": "Sample text for enrichment",
    "options": {
      "difficulty": true,
      "taxonomy": true,
      "competency": true
    }
  }'
```

---

## Notes

1. **Semantic Chunk Service is the MOST IMPORTANT component** - it does curriculum-aware chunking based on competency, activity, assessment, inquiry, and lesson plans. This is NOT naive fixed-size splitting.

2. **Vision Service port conflict resolved** - External port 8005 maps to internal port 8002 to avoid conflict with Gateway Service.

3. **All services use shared components** from the `shared/` directory for consistency.

4. **Resource allocations** are configured based on expected workload - Vision Service gets more resources for image processing.

5. **Health checks** are configured with appropriate initial delays - Vision Service has longer delay due to OCR initialization.

---

## Phase Status

✅ **COMPLETED** - All Phase 2 objectives achieved:
- Parser Service implemented
- Vision Service implemented
- Semantic Chunk Service implemented (Most Important)
- Metadata Service implemented
- Docker configurations created
- Kubernetes manifests created
- Docker Compose updated

**Ready for Phase 3: Retrieval & Generation Engine**