# AI Platform Monolith Architecture

## Overview

AI Platform telah dikonversi dari **Microservices Architecture** menjadi **Modular Monolith Architecture** untuk menyederhanakan deployment, mengurangi overhead infrastruktur, dan menghilangkan kompleksitas komunikasi antar-service. Arsitektur modular monolith mempertahankan batas yang jelas antar modul untuk memudahkan konversi kembali ke microservices di masa depan jika diperlukan.

---

## Architecture Changes

### Previous: Microservices Architecture
- 33+ microservices terpisah
- HTTP/gRPC communication antar services
- Multiple Docker containers
- Service discovery complexity
- Network latency antar services
- Complex orchestration

### Current: Modular Monolith Architecture
- Single unified application dengan modular boundaries
- Direct function calls antar components
- Single Docker container
- Simplified deployment
- Zero network latency
- Easy debugging
- Modular structure untuk future microservices extraction

---

## Monolith Structure

```
monolith/
├── app/
│   ├── main.py                 # Unified FastAPI application
│   ├── core/                   # Core configuration and utilities
│   │   ├── config.py         # Centralized settings
│   │   └── logging.py        # Logging configuration
│   ├── services/               # All services (direct function calls)
│   │   # Core Services
│   │   ├── parser_service.py
│   │   ├── semantic_chunk_service.py
│   │   ├── semantic_enrichment_service.py
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   │   ├── generation_service.py
│   │   ├── pipeline_tracker_service.py
│   │   └── ontology_validation_service.py
│   │   # Educational Services
│   │   ├── adaptive_learning_service.py
│   │   ├── assessment_service.py
│   │   ├── curriculum_service.py
│   │   ├── educational_intelligence_service.py
│   │   ├── pedagogy_service.py
│   │   └── learning_graph_service.py
│   │   # Governance Services
│   │   ├── governance_service.py
│   │   └── observability_service.py
│   │   # Enhancement Services
│   │   ├── retrieval_enhancement_service.py
│   │   ├── strategic_analysis_service.py
│   │   └── recommendation_service.py
│   │   # Infrastructure Services
│   │   ├── metadata_service.py
│   │   ├── monitoring_service.py
│   │   ├── notification_service.py
│   │   ├── orchestration_service.py
│   │   ├── vision_service.py
│   │   ├── ai_agents_service.py
│   │   └── gateway_service.py
│   ├── api/                    # API routes (unified endpoints)
│   │   # Core API Routes
│   │   ├── parser_routes.py
│   │   ├── chunk_routes.py
│   │   ├── enrichment_routes.py
│   │   ├── embedding_routes.py
│   │   ├── retrieval_routes.py
│   │   ├── generation_routes.py
│   │   └── ontology_routes.py
│   │   # Educational API Routes
│   │   ├── adaptive_learning_routes.py
│   │   ├── assessment_routes.py
│   │   ├── curriculum_routes.py
│   │   ├── educational_intelligence_routes.py
│   │   ├── pedagogy_routes.py
│   │   └── learning_graph_routes.py
│   │   # Governance API Routes
│   │   ├── governance_routes.py
│   │   └── observability_routes.py
│   │   # Enhancement API Routes
│   │   ├── retrieval_enhancement_routes.py
│   │   ├── strategic_analysis_routes.py
│   │   └── recommendation_routes.py
│   │   # Infrastructure API Routes
│   │   ├── metadata_routes.py
│   │   ├── monitoring_routes.py
│   │   ├── notification_routes.py
│   │   ├── orchestration_routes.py
│   │   ├── vision_routes.py
│   │   ├── ai_agents_routes.py
│   │   └── gateway_routes.py
│   ├── models/                 # Data models
│   └── utils/                  # Utility functions
├── requirements.txt            # Unified dependencies
├── Dockerfile                 # Single container build
├── docker-compose.yml         # Simplified orchestration
└── .env                       # Environment configuration
```

---

## Key Changes

### 1. Communication Pattern
**Before**: HTTP/gRPC calls between microservices
```python
# Microservices communication
response = httpx.post("http://parser-service:8001/parse", data=document)
```

**After**: Direct function calls within monolith
```python
# Monolith communication
parsed_doc = parser_service.parse_document(document_data)
```

### 2. Deployment
**Before**: 33+ containers, complex orchestration
```yaml
services:
  parser-service:
    build: ./services/parser-service
  chunk-service:
    build: ./services/semantic-chunk-service
  enrichment-service:
    build: ./services/semantic-enrichment-service
  # ... 30+ more services
```

**After**: Single container deployment
```yaml
services:
  ai-platform-monolith:
    build: ./monolith
```

### 3. Configuration
**Before**: Multiple .env files per service
```
services/parser-service/.env
services/chunk-service/.env
services/enrichment-service/.env
# ... 30+ more .env files
```

**After**: Single .env file
```
monolith/.env
```

### 4. Dependencies
**Before**: Multiple requirements.txt per service
```
services/parser-service/requirements.txt
services/chunk-service/requirements.txt
# ... 30+ more requirements.txt
```

**After**: Single requirements.txt
```
monolith/requirements.txt
```

---

## Benefits of Monolith Architecture

### 1. Simplified Deployment
- Single deployment artifact
- Single Docker image
- Single configuration file
- Single database connection pool

### 2. Reduced Complexity
- No service discovery needed
- No API gateway routing
- No inter-service networking
- No distributed transaction handling

### 3. Performance
- Zero network latency
- Direct function calls
- Shared memory access
- Unified caching

### 4. Easier Development
- Simple debugging
- Single codebase navigation
- Easy testing
- No inter-service mocking needed

### 5. Cost Efficiency
- Reduced infrastructure overhead
- Fewer containers to manage
- Simplified monitoring
- Lower maintenance costs

---

## Service Integration

### Parser Service Integration
- Direct access to document processing logic
- No HTTP layer overhead
- Shared document state

### Semantic Chunk Service Integration  
- Direct function calls from parser
- Immediate chunk access
- No queue delays

### Semantic Enrichment Service Integration
- Direct tagging of chunks
- Shared context across services
- Real-time enrichment

### Embedding Service Integration
- Direct vector generation
- Shared model instances
- Reduced memory footprint

### Retrieval Service Integration
- Direct database access
- No network latency
- Shared caching

---

## API Endpoints

All services accessible through unified API on port 8000:

### Core Services
- `/api/v1/parser` - Document parsing
- `/api/v1/chunk` - Semantic chunking  
- `/api/v1/enrichment` - Semantic enrichment
- `/api/v1/embedding` - Embedding generation
- `/api/v1/retrieval` - Document retrieval
- `/api/v1/generation` - Content generation
- `/api/v1/ontology` - Ontology validation

### Educational Services
- `/api/v1/adaptive-learning` - Adaptive learning analysis
- `/api/v1/assessment` - Assessment creation and evaluation
- `/api/v1/curriculum` - Curriculum management
- `/api/v1/educational-intelligence` - Educational insights
- `/api/v1/pedagogy` - Pedagogical recommendations
- `/api/v1/learning-graph` - Learning graph construction

### Governance Services
- `/api/v1/governance` - Audit, moderation, and hallucination detection
- `/api/v1/observability` - Event tracking and reporting

### Enhancement Services
- `/api/v1/retrieval-enhancement` - Query enhancement and reranking
- `/api/v1/strategic-analysis` - Strategic planning and analysis
- `/api/v1/recommendation` - Content recommendations

### Infrastructure Services
- `/api/v1/metadata` - Metadata extraction and management
- `/api/v1/monitoring` - System monitoring and health
- `/api/v1/notification` - Notification management
- `/api/v1/orchestration` - Pipeline orchestration
- `/api/v1/vision` - Image analysis and OCR
- `/api/v1/ai-agents` - AI agent management
- `/api/v1/gateway` - Request routing and authentication

---

## Scaling Strategy

### Monolith Scaling Options:
1. **Horizontal Scaling**: Multiple instances behind load balancer
2. **Vertical Scaling**: Increase resources per instance
3. **Service Boundaries**: Future extraction if needed

### When to Consider Microservices:
- Team size > 50 developers
- Transaction volume > 10M/day
- Service-specific scaling requirements
- Organizational boundaries

---

## Migration Strategy

### Phase 1: Core Services Integration ✅
- ✅ Parser Service
- ✅ Semantic Chunk Service  
- ✅ Semantic Enrichment Service
- ✅ Embedding Service
- ✅ Retrieval Service
- ✅ Generation Service
- ✅ Pipeline Tracker Service
- ✅ Ontology Validation Service

### Phase 2: Educational Services Integration ✅
- ✅ Adaptive Learning Service
- ✅ Assessment Service
- ✅ Curriculum Service
- ✅ Educational Intelligence Service
- ✅ Pedagogy Service
- ✅ Learning Graph Service

### Phase 3: Governance Services Integration ✅
- ✅ Governance Service (Audit, Moderation, Hallucination Guard)
- ✅ Observability Service

### Phase 4: Enhancement Services Integration ✅
- ✅ Retrieval Enhancement Service (Reranking, Advanced Enhancement)
- ✅ Strategic Analysis Service
- ✅ Recommendation Service

### Phase 5: Infrastructure Services Integration ✅
- ✅ Metadata Service
- ✅ Monitoring Service
- ✅ Notification Service
- ✅ Orchestration Service
- ✅ Vision Service
- ✅ AI Agents Service
- ✅ Gateway Service

### Migration Complete ✅
All 33+ microservices have been successfully migrated to the modular monolith architecture with clear service boundaries maintained for future microservices extraction if needed.

---

## Maintenance

### Code Changes
- All changes in single codebase
- Simple version control
- No inter-service version compatibility

### Testing
- Single test suite
- Integration tests simplified
- No network mocking needed

### Monitoring
- Single application metrics
- Simplified logging
- Unified error tracking

---

## Conclusion

Monolith architecture provides:
- **Simplicity**: Single application to manage
- **Performance**: Zero network latency
- **Efficiency**: Reduced infrastructure costs
- **Flexibility**: Easy to refactor and evolve

This architecture is ideal for:
- Small to medium teams
- Lower transaction volumes
- Rapid development cycles
- Simplified operational requirements

For future scaling needs, services can be extracted incrementally from the monolith based on clear business boundaries.