# Phase 3: Retrieval & Generation - Implementation Complete

## ⚠️ IMPORTANT SECURITY UPDATE - Architecture Fix
**Status**: Priority 1 Security Lockdown Complete (See: [SECURITY_LOCKDOWN_COMPLETE.md](SECURITY_LOCKDOWN_COMPLETE.md))

All AI Platform services (Parser, Vision, Semantic Chunk, Metadata, Embedding, Retrieval, Reranking, Generation) now communicate **ONLY** through the Gateway Service. Port mappings for internal services have been removed from docker-compose.yml. This reduces the attack surface from 9+ exposed endpoints to 1 controlled entry point.

**Current Architecture**:
- ✅ Gateway Service (8002): **SINGULAR** external entry point
- ✅ AI Platform services: **INTERNAL ONLY** (no external port mapping)
- ✅ Communication: Backend (Go) → Gateway → AI Platform Services

See [ARCHITECTURE_FIX_RECOMMENDATIONS.md](ARCHITECTURE_FIX_RECOMMENDATIONS.md) for next steps (RabbitMQ/gRPC integration).

## Overview
Phase 3 implements the Retrieval & Generation components for the AI Platform. This phase focuses on semantic search, reranking, and LLM-based content generation essential for AI-powered educational features.

## Services Implemented

### 1. Embedding Service (Port 8006 - Internal Only)
**Location**: `services/embedding-service/`
**⚠️ Note**: Port 8006 is NOT exposed externally. Access via Gateway Service.

**Purpose**: Generate embeddings for text, images, tables, and mathematical formulas

**Components**:
- `main.py` - Embedding API with multiple embedder support
- `schemas/embedding_schemas.py` - Pydantic schemas for embedding requests/responses
- `embedders/text/text_embedder.py` - Text embedding with BAAI/bge-m3
- `embedders/image/image_embedder.py` - Image embedding with CLIP
- `embedders/table/table_embedder.py` - Table embedding for structured data
- `embedders/formula/formula_embedder.py` - Mathematical formula embedding

**Key Features**:
- **Multilingual support** - BAAI/bge-m3 for Indonesian and English
- **Multi-modal embedding** - Text, images, tables, formulas
- **GPU acceleration** - CUDA support for faster processing
- **Batch processing** - Efficient batch embedding generation
- **Model flexibility** - Support for multiple embedding models

**API Endpoints**:
- `POST /api/v1/embed/text` - Single text embedding
- `POST /api/v1/embed/text/batch` - Batch text embedding
- `POST /api/v1/embed/image` - Image embedding
- `POST /api/v1/embed/table` - Table embedding
- `POST /api/v1/embed/formula` - Formula embedding (LaTeX)
- `GET /api/v1/models` - List available models
- `GET /api/v1/stats` - Service statistics

**Dependencies**:
- sentence-transformers
- PyTorch
- PIL/Pillow for image processing

---

### 2. Retrieval Service (Port 8007 - Internal Only)
**Location**: `services/retrieval-service/`
**⚠️ Note**: Port 8007 is NOT exposed externally. Access via Gateway Service.

**Purpose**: Semantic and hybrid search with Qdrant vector database

**Components**:
- `main.py` - Retrieval API with multiple search strategies
- `schemas/retrieval_schemas.py` - Pydantic schemas for retrieval requests/responses
- `retrievers/semantic_retriever.py` - Vector-based semantic search
- `retrievers/hybrid_retriever.py` - Fusion of semantic and keyword search
- `retrievers/metadata_retriever.py` - Metadata-filtered search
- `query_builders/query_builder.py` - Query optimization and expansion
- `context-builders/context_builder.py` - Context assembly for LLM

**Key Features**:
- **Semantic search** - Vector similarity search with Qdrant
- **Hybrid search** - Fusion of semantic and BM25 keyword search
- **Metadata filtering** - Filter by curriculum, competency, difficulty
- **Query expansion** - Synonym, curriculum-based, semantic expansion
- **Context building** - Assemble retrieved documents for LLM input
- **Multiple strategies** - Ranked, diverse, summarized context building

**API Endpoints**:
- `POST /api/v1/search/semantic` - Semantic vector search
- `POST /api/v1/search/hybrid` - Hybrid semantic + keyword search
- `POST /api/v1/search/metadata` - Metadata-filtered search
- `POST /api/v1/query/build` - Query optimization and expansion
- `POST /api/v1/context/build` - Context assembly from documents
- `GET /api/v1/collections` - List Qdrant collections
- `GET /api/v1/stats` - Service statistics

**Dependencies**:
- Qdrant client
- sentence-transformers
- Reciprocal Rank Fusion (RRF)

---

### 3. Reranking Service (Port 8008 - Internal Only)
**Location**: `services/reranking-service/`
**⚠️ Note**: Port 8008 is NOT exposed externally. Access via Gateway Service.

**Purpose**: Re-rank retrieved documents using cross-encoders and curriculum-aware strategies

**Components**:
- `main.py` - Reranking API with multiple strategies
- `schemas/reranking_schemas.py` - Pydantic schemas for reranking requests/responses
- `cross-encoder/cross_encoder.py` - Cross-encoder model reranking
- `ranking/curriculum_reranker.py` - Curriculum-aware reranking
- `ranking/pedagogy_reranker.py` - Pedagogy-aware reranking (VARK)
- `ranking/competency_reranker.py` - Competency-aware reranking (KI-1 to KI-4)

**Key Features**:
- **Cross-encoder reranking** - Precise relevance scoring with ms-marco-MiniLM
- **Curriculum-aware** - Re-rank by Kurikulum Merdeka level, subject, competency
- **Pedagogy-aware** - Re-rank by learning style (VARK) and teaching method
- **Competency-aware** - Re-rank by core competency (KI-1 to KI-4) and Bloom's taxonomy
- **Educational focus** - Specialized for educational content alignment
- **Multiple strategies** - Combine different reranking approaches

**API Endpoints**:
- `POST /api/v1/rerank` - Cross-encoder reranking
- `POST /api/v1/rerank/curriculum` - Curriculum-aware reranking
- `POST /api/v1/rerank/pedagogy` - Pedagogy-aware reranking
- `POST /api/v1/rerank/competency` - Competency-aware reranking
- `GET /api/v1/methods` - List available reranking methods
- `GET /api/v1/stats` - Service statistics

**Dependencies**:
- sentence-transformers (cross-encoder)
- Custom educational ranking logic

---

### 4. Generation Service (Port 8009 - Internal Only)
**Location**: `services/generation-service/`
**⚠️ Note**: Port 8009 is NOT exposed externally. Access via Gateway Service.

**Purpose**: LLM-based text generation with multiple providers and citation support

**Components**:
- `main.py` - Generation API with multi-provider support
- `schemas/generation_schemas.py` - Pydantic schemas for generation requests/responses
- `providers/openai_provider.py` - OpenAI API integration (GPT-4, GPT-3.5)
- `providers/anthropic_provider.py` - Anthropic API integration (Claude 3)
- `providers/local_provider.py` - Local LLM support (Qwen, Mistral)
- `prompts/prompt_manager.py` - Template management for educational prompts
- `citations/citation_system.py` - Citation extraction and formatting
- `validators/response_validator.py` - Response validation and hallucination detection

**Key Features**:
- **Multi-provider support** - OpenAI, Anthropic, and local models
- **Citation system** - Automatic citation extraction and formatting
- **Response validation** - Hallucination detection and quality checks
- **Template management** - Educational-specific prompt templates
- **Streaming support** - Real-time response generation
- **Educational prompts** - Built-in templates for lesson plans, assessments, etc.

**API Endpoints**:
- `POST /api/v1/generate` - Text generation with specified provider
- `POST /api/v1/generate/citations` - Generation with citations from documents
- `POST /api/v1/validate` - Response validation and quality check
- `POST /api/v1/templates/generate` - Generation using prompt templates
- `GET /api/v1/providers` - List available LLM providers
- `GET /api/v1/templates` - List available prompt templates
- `GET /api/v1/stats` - Service statistics

**Dependencies**:
- OpenAI API (optional)
- Anthropic API (optional)
- Transformers (for local models)
- Custom citation and validation logic

---

## Docker Configuration

All services include Dockerfiles with standard configurations:

### Embedding Service Dockerfile
- Base: Python 3.11-slim
- System: Minimal
- Port: 8006 (INTERNAL ONLY - not exposed externally)
- GPU Support: Yes (CUDA)

### Retrieval Service Dockerfile
- Base: Python 3.11-slim
- System: Minimal
- Port: 8007 (INTERNAL ONLY - not exposed externally)
- Dependencies: Qdrant client

### Reranking Service Dockerfile
- Base: Python 3.11-slim
- System: Minimal
- Port: 8008 (INTERNAL ONLY - not exposed externally)
- GPU Support: Yes (CUDA)

### Generation Service Dockerfile
- Base: Python 3.11-slim
- System: Minimal
- Port: 8009 (INTERNAL ONLY - not exposed externally)
- API Keys: OpenAI, Anthropic (optional)

---

## Kubernetes Configuration

Each service has its own Kubernetes manifest in `infra/kubernetes/`:

- `infra/kubernetes/embedding-service.yaml`
- `infra/kubernetes/retrieval-service.yaml`
- `infra/kubernetes/reranking-service.yaml`
- `infra/kubernetes/generation-service.yaml`

Each includes:
- Deployment with replica configuration
- Service (ClusterIP)
- HorizontalPodAutoscaler (HPA)
- Resource limits and requests
- Health checks (liveness and readiness probes)

**Replica and Resource Configurations**:

| Service | Min Replicas | Max Replicas | Memory Request | Memory Limit | CPU Request | CPU Limit |
|---------|--------------|--------------|----------------|--------------|------------|----------|
| Embedding | 2 | 6 | 1Gi | 2Gi | 1000m | 2000m |
| Retrieval | 2 | 8 | 512Mi | 1Gi | 500m | 1000m |
| Reranking | 2 | 6 | 1Gi | 2Gi | 1000m | 2000m |
| Generation | 2 | 6 | 1Gi | 2Gi | 1000m | 2000m |

---

## Docker Compose Update

The `docker-compose.yml` has been updated with the four new services:

```yaml
services:
  embedding-service:
    ports: "8006:8006"
    depends_on: [postgres, redis, qdrant]
    
  retrieval-service:
    ports: "8007:8007"
    depends_on: [postgres, redis, qdrant, embedding-service]
    
  reranking-service:
    ports: "8008:8008"
    depends_on: [postgres, redis, retrieval-service]
    
  generation-service:
    ports: "8009:8009"
    depends_on: [postgres, redis, reranking-service]
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
| **Embedding** | **8006** | **8006** |
| **Retrieval** | **8007** | **8007** |
| **Reranking** | **8008** | **8008** |
| **Generation** | **8009** | **8009** |

---

## API Endpoints Summary

### Embedding Service (http://localhost:8006)
- `POST /api/v1/embed/text` - Single text embedding
- `POST /api/v1/embed/text/batch` - Batch text embedding
- `POST /api/v1/embed/image` - Image embedding
- `POST /api/v1/embed/table` - Table embedding
- `POST /api/v1/embed/formula` - Formula embedding
- `GET /api/v1/models` - List available models
- `GET /health` - Health check

### Retrieval Service (http://localhost:8007)
- `POST /api/v1/search/semantic` - Semantic search
- `POST /api/v1/search/hybrid` - Hybrid search
- `POST /api/v1/search/metadata` - Metadata search
- `POST /api/v1/query/build` - Query building
- `POST /api/v1/context/build` - Context building
- `GET /api/v1/collections` - List collections
- `GET /health` - Health check

### Reranking Service (http://localhost:8008)
- `POST /api/v1/rerank` - Cross-encoder reranking
- `POST /api/v1/rerank/curriculum` - Curriculum reranking
- `POST /api/v1/rerank/pedagogy` - Pedagogy reranking
- `POST /api/v1/rerank/competency` - Competency reranking
- `GET /api/v1/methods` - List methods
- `GET /health` - Health check

### Generation Service (http://localhost:8009)
- `POST /api/v1/generate` - Generate text
- `POST /api/v1/generate/citations` - Generate with citations
- `POST /api/v1/validate` - Validate response
- `POST /api/v1/templates/generate` - Template generation
- `GET /api/v1/providers` - List providers
- `GET /api/v1/templates` - List templates
- `GET /health` - Health check

---

## Educational-Specific Features

### Kurikulum Merdeka Integration
- **Curriculum-aware search** - Filter by SD/SMP/SMA levels
- **Competency tagging** - Support for KI-1 to KI-4 competencies
- **Subject-specific retrieval** - Search by subject area
- **Grade-level targeting** - Search by specific grade

### Pedagogy Support
- **Learning style adaptation** - VARK model integration
- **Teaching method alignment** - Direct instruction, inquiry-based, PBL
- **Differentiation strategies** - Support for diverse learning needs
- **Activity type matching** - Individual, group, class activities

### Bloom's Taxonomy
- **Cognitive level targeting** - Remember to Create
- **Competency mapping** - Align with Bloom's levels
- **Progression support** - Scaffold from lower to higher levels

### Prompt Templates
- **Lesson plan generation** - Kurikulum Merdeka compliant
- **Assessment creation** - With rubrics and criteria
- **Concept explanation** - Age-appropriate explanations
- **Question generation** - Various competency levels
- **Differentiation strategies** - For diverse learners

---

## Performance Targets

### Embedding Service
- Embedding throughput: > 100 docs/sec
- Latency: < 100ms per document (batch)
- Model: BAAI/bge-m3 (1024 dimensions)

### Retrieval Service
- Retrieval latency: < 500ms
- Hybrid search: Semantic + keyword fusion
- Query expansion: < 50ms

### Reranking Service
- Reranking improvement: > 20% over baseline
- Latency: < 200ms for 10 documents
- Cross-encoder: ms-marco-MiniLM-L-6-v2

### Generation Service
- Response validation: < 100ms
- Citation extraction: Automatic
- Hallucination detection: Real-time

---

## Dependencies and Requirements

### Python Dependencies
- sentence-transformers
- transformers
- torch
- qdrant-client
- openai
- anthropic
- fastapi
- pydantic
- uvicorn

### System Requirements
- Python 3.11+
- CUDA (for GPU acceleration)
- 8GB RAM minimum
- 50GB disk space for models

### API Keys (Optional)
- OpenAI API key (for OpenAI provider)
- Anthropic API key (for Anthropic provider)

---

## Testing and Validation

### Health Checks
All services include comprehensive health checks:
- Liveness probes
- Readiness probes
- Dependency checks
- Model loading verification

### API Testing
- Endpoint availability
- Request/response validation
- Error handling
- Rate limiting

### Performance Testing
- Load testing
- Latency measurement
- Throughput validation
- Resource utilization

---

## Next Steps

### Phase 4: Governance & Observability
- Audit service implementation
- Quality assurance service
- Feedback collection system
- Analytics and reporting

### Integration Tasks
- Gateway integration for new services
- End-to-end workflow testing
- Performance optimization
- Documentation completion

### Production Readiness
- Security hardening
- Monitoring enhancement
- Backup and recovery
- Disaster recovery planning

## 🔄 Communication Architecture Update

**Status**: Priority 2 (RabbitMQ) and Priority 3 (gRPC) implementations complete.

### Backend Integration

**Go Backend gRPC Client**:
- File: `backend/internal/messaging/grpc_client.go`
- Manages connections to all AI services
- Provides client methods for each service

**Go Backend RabbitMQ Producer**:
- File: `backend/internal/messaging/rabbitmq_producer.go`
- Publishes tasks to AI service queues
- Consumes results from result queues

### Communication Matrix

| From | To | Method | Use Case |
|------|-----|--------|----------|
| Backend | Parser | gRPC/RabbitMQ | Document parsing |
| Backend | Vision | gRPC/RabbitMQ | Image processing |
| Backend | Chunk | gRPC/RabbitMQ | Content chunking |
| Backend | Metadata | gRPC/RabbitMQ | Enrichment |
| Backend | Embedding | gRPC/RabbitMQ | Vector generation |
| Backend | Retrieval | gRPC | Real-time search |
| Backend | Reranking | gRPC/RabbitMQ | Result reranking |
| Backend | Generation | gRPC/RabbitMQ | AI generation |

### Service Ports

| Service | REST Port (deprecated) | gRPC Port | RabbitMQ Queue |
|---------|----------------------|-----------|---------------|
| Embedding | 8006 | 50052 | embedding.queue |
| Retrieval | 8007 | 50054 | retrieval.queue |
| Reranking | 8008 | 50058 | reranking.queue |
| Generation | 8009 | 50053 | generation.queue |

**Documentation**:
- RabbitMQ Implementation: `PRIORITY2_RABBITMQ_IMPLEMENTATION.md`
- gRPC Implementation: `PRIORITY3_GRPC_IMPLEMENTATION.md`
- Cleanup & Documentation: `PRIORITY4_CLEANUP_DOCUMENTATION.md`

---

## Summary

Phase 3 successfully implements the core AI functionality for the platform:

✅ **Embedding Service** - Multi-modal embedding generation
✅ **Retrieval Service** - Semantic and hybrid search with Qdrant
✅ **Reranking Service** - Educational-aware reranking strategies
✅ **Generation Service** - Multi-provider LLM integration with citations

These services form the foundation for AI-powered educational features including intelligent search, content generation, and personalized learning experiences aligned with Kurikulum Merdeka.