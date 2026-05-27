# gRPC Architecture Conversion Guide

## Overview

This document outlines the architectural change required to convert Fase 5, 6, 7, and 8 AI services from REST API JSON endpoints to gRPC services accessible only by the backend.

## Current Architecture

### Problem Statement
- AI services (Fase 5, 6, 7, 8) currently expose REST API JSON endpoints
- These endpoints are publicly accessible through FastAPI
- No proper internal communication protocol with backend
- Security risk of exposing AI services directly
- Performance limitations of HTTP/JSON for high-volume AI operations

### Current Services
- **Fase 7**: AI Agents Service (Port 8023)
- **Fase 8**: Hallucination Guard Service (Port 8024)
- **Fase 8**: Educational Observability Service (Port 8025)
- **Fase 5**: Educational Intelligence Services
- **Fase 6**: Advanced Enhancement Services

## Target Architecture

### gRPC Communication Model
```
Backend (Go) <---> gRPC Client <---> gRPC Server (Python Services)
```

### Service Ports
- AI Agents Service: gRPC Port 50072
- Hallucination Guard Service: gRPC Port 50073
- Educational Observability Service: gRPC Port 50074
- Educational Intelligence Services: Ports 50075-50082
- Advanced Enhancement Services: Ports 50083-50086

## Implementation Status

### ✅ Completed (Fase 7 & 8 Services)

The following services have been successfully converted to gRPC:

1. **AI Agents Service (Fase 7)** - Port 50072
   - ✅ Proto file created (`proto/ai_agents.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Startup script created (`start_grpc.sh`)
   - ✅ README updated with gRPC documentation
   - ✅ 16 gRPC methods implemented (4 per agent)

2. **Hallucination Guard Service (Fase 8.1)** - Port 50073
   - ✅ Proto file created (`proto/hallucination_guard.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Startup script created (`start_grpc.sh`)
   - ✅ 7 gRPC methods implemented (6 validators + 1 detection)

3. **Educational Observability Service (Fase 8.2)** - Port 50074
   - ✅ Proto file created (`proto/educational_observability.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Startup script created (`start_grpc.sh`)
   - ✅ 6 gRPC methods implemented (6 monitoring dashboards)

4. **Backend gRPC Client Updated**
   - ✅ Service addresses added to grpc_client.go
   - ✅ Placeholder client implementations added
   - ✅ Connection manager configured for new services

### ✅ Completed (Fase 2 - Core Intelligence Services)

The following services have been successfully converted to gRPC:

2. **Parser Service (Fase 2.1)** - Port 50051
   - ✅ Proto file created (`proto/parser_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/parser_service.go`)
   - ✅ 6 gRPC methods (ParseDocument, ParseText, ExtractTables, ExtractImages, ExtractOCR, DetectLayout)

3. **Vision Service (Fase 2.2)** - Port 50055
   - ✅ Proto file created (`proto/vision_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/vision_service.go`)
   - ✅ 5 gRPC methods (ProcessOCR, AnalyzeDiagram, ExtractFormula, ClassifyImage, PreprocessImage)

4. **Semantic Chunk Service (Fase 2.3)** - Port 50056
   - ✅ Proto file created (`proto/semantic_chunk_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/semantic_chunk_service.go`)
   - ✅ 10 gRPC methods (ChunkCompetency, ChunkActivity, ChunkAssessment, ChunkInquiry, ChunkLessonPlan, DetectHierarchy, ClassifyPedagogy, ValidateQuality, EnrichMetadata, BuildChunks)

5. **Metadata Service (Fase 2.4)** - Port 50057
   - ✅ Proto file created (`proto/metadata_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/metadata_service.go`)
   - ✅ 7 gRPC methods (EnrichDifficulty, ClassifyTaxonomy, DetectLearningStyle, TagCompetency, TagPedagogy, TagAssessment, BatchEnrich)

### ✅ Completed (Fase 3 - Retrieval & Generation Services)

The following services have been successfully converted to gRPC:

6. **Embedding Service (Fase 3.1)** - Port 50052
   - ✅ Proto file created (`proto/embedding_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/embedding_service.go`)
   - ✅ 6 gRPC methods (EmbedText, EmbedImage, EmbedTable, EmbedFormula, BatchEmbedText, GetEmbeddingInfo)

7. **Retrieval Service (Fase 3.2)** - Port 50054
   - ✅ Proto file created (`proto/retrieval_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/retrieval_service.go`)
   - ✅ 6 gRPC methods (SemanticSearch, HybridSearch, FilterByMetadata, BuildContext, ExpandQuery, GetRelevanceScores)

8. **Generation Service (Fase 3.3)** - Port 50053
   - ✅ Proto file created (`proto/generation_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/generation_service.go`)
   - ✅ 6 gRPC methods (GenerateText, GenerateWithContext, StreamText, GenerateQuiz, GenerateLessonPlan, GenerateExplanation)

9. **Reranking Service (Fase 3.4)** - Port 50058
   - ✅ Proto file created (`proto/reranking_service.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Backend gRPC client implemented (`internal/ai/grpc/reranking_service.go`)
   - ✅ 6 gRPC methods (RerankCrossEncoder, RerankMonoEncoder, CurriculumAwareRerank, PedagogyAwareRerank, CompetencyAwareRerank, HybridRerank)

### ✅ Completed (Fase 5 - Educational Intelligence Services)

The following services have been successfully converted to gRPC:

4. **Educational Intelligence Services (Fase 5)** - Ports 50075-50081
   - ✅ Proto file created (`proto/educational_intelligence.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Startup script created (`start_grpc.sh`)
   - ✅ README updated with gRPC documentation
   - ✅ 14 gRPC methods implemented (2 per engine × 7 engines)
   - **Engines**:
     - Adaptive Learning Engine (Port 50075): GeneratePersonalizedLearningPath, AnalyzeStudentLearningPattern
     - Assessment Engine (Port 50076): GenerateAdaptiveAssessment, AnalyzeAssessmentResults
     - Curriculum Engine (Port 50077): GenerateCurriculumPlan, AlignContentWithStandards
     - Learning Graph Engine (Port 50078): BuildLearningGraph, AnalyzeLearningPath
     - Learning Progression Engine (Port 50079): TrackStudentProgression, PredictLearningOutcomes
     - Pedagogy Engine (Port 50080): RecommendPedagogyStrategy, EvaluateTeachingEffectiveness
     - Recommendation Engine (Port 50081): GenerateContentRecommendations, GenerateActivityRecommendations

### ✅ Completed (Fase 6 - Advanced Enhancement Services)

The following services have been successfully converted to gRPC:

5. **Advanced Enhancement Services (Fase 6)** - Ports 50083-50085
   - ✅ Proto file created (`proto/advanced_enhancement.proto`)
   - ✅ Python gRPC stub files generated
   - ✅ gRPC server implemented (`app/grpc_server.py`)
   - ✅ Dockerfile updated for gRPC support
   - ✅ Startup script created (`start_grpc.sh`)
   - ✅ README updated with gRPC documentation
   - ✅ 9 gRPC methods implemented (3 per service × 3 services)
   - **Services**:
     - Retrieval Enhancement Service (Port 50083): EnhanceQuery, ExpandQuery, RerankResults
     - Semantic Enrichment Service (Port 50084): EnrichContent, GenerateEmbeddings, ExtractKnowledge
     - Educational Ontology Service (Port 50085): QueryOntology, ValidateAlignment, GetRelatedConcepts

6. **Backend gRPC Client Updated**
   - ✅ Service addresses added to grpc_client.go for Fase 5 & 6 services
   - ✅ Placeholder client implementations added for all new services
   - ✅ Connection manager configured for new services

### ✅ Completed (Backend gRPC Client Implementation for Fase 2 & 3)

The backend gRPC client has been fully implemented for Fase 2 and Fase 3 services:

10. **Backend gRPC Client (Fase 2 & 3)**
   - ✅ Proto files copied to `backend/internal/ai/proto/`
   - ✅ Go client implementations created in `backend/internal/ai/grpc/`:
     - `parser_service.go` - Parser Service client with 6 methods
     - `vision_service.go` - Vision Service client with 5 methods
     - `semantic_chunk_service.go` - Semantic Chunk Service client with 10 methods
     - `metadata_service.go` - Metadata Service client with 7 methods
     - `embedding_service.go` - Embedding Service client with 6 methods
     - `retrieval_service.go` - Retrieval Service client with 6 methods
     - `generation_service.go` - Generation Service client with 6 methods
     - `reranking_service.go` - Reranking Service client with 6 methods
   - ✅ Main `grpc_client.go` updated to use new client implementations
   - ✅ Legacy compatibility methods maintained for backward compatibility
   - ✅ Client initialization and connection management implemented
   - ✅ Proper error handling and context propagation

## Implementation Plan
For each service, implement:

#### 1. Install Dependencies
```python
# Add to requirements.txt
grpcio==1.60.0
grpcio-tools==1.60.0
protobuf==4.25.1
```

#### 2. Generate Python gRPC Code
```bash
# For each proto file
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/ai_agents.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/hallucination_guard.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/educational_observability.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/educational_intelligence.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/advanced_enhancement.proto
```

#### 3. Implement gRPC Server
Create `app/grpc_server.py` for each service:

```python
import grpc
from concurrent import futures
import asyncio
from app.main import HallucinationGuardEngine
import ai_platform.hallucination_guard.hallucination_guard_pb2 as pb2
import ai_platform.hallucination_guard.hallucination_guard_pb2_grpc as pb2_grpc

class HallucinationGuardServicer(pb2_grpc.HallucinationGuardServiceServicer):
    def __init__(self):
        self.engine = HallucinationGuardEngine()
    
    def ValidateCurriculum(self, request, context):
        # Implement gRPC method
        pass
    
    # Implement other gRPC methods...

async def serve(port):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_HallucinationGuardServiceServicer_to_server(
        HallucinationGuardServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    await server.start()
    print(f"gRPC Server started on port {port}")
    await server.wait_for_termination()
```

#### 4. Update Main Application
Modify `app/main.py`:
- Remove or comment out FastAPI app and endpoints
- Keep the core engine classes
- Add gRPC server integration
- Update lifespan manager to start gRPC server

```python
# Remove FastAPI app
# app = FastAPI(...)

# Replace with gRPC server startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start gRPC server
    if ENABLE_GRPC_SERVER:
        from .grpc_server import serve
        import asyncio
        asyncio.create_task(serve(GRPC_PORT))
    yield
```

### Phase 3: Backend gRPC Client Implementation

#### 1. Generate Go gRPC Code
```bash
# From backend directory
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/ai_agents.proto
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/hallucination_guard.proto
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/educational_observability.proto
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/educational_intelligence.proto
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/advanced_enhancement.proto
```

#### 2. Update Backend gRPC Client
Modify `internal/messaging/grpc_client.go`:

```go
// Update services map
services: map[string]string{
    // Existing services
    "parser":         "parser-service:50051",
    "embedding":      "embedding-service:50052",
    "generation":     "generation-service:50053",
    "retrieval":      "retrieval-service:50054",
    "vision":         "vision-service:50055",
    "chunk":          "semantic-chunk-service:50056",
    "metadata":       "metadata-service:50057",
    "reranking":      "reranking-service:50058",
    
    // New Phase 7 services
    "ai_agents":              "ai-agents-service:50072",
    "hallucination_guard":      "hallucination-guard-service:50073",
    "educational_observability": "educational-observability-service:50074",
    
    // New Phase 5 services
    "adaptive_learning":       "adaptive-learning-engine:50075",
    "assessment_engine":        "assessment-engine:50076",
    "curriculum_engine":        "curriculum-engine:50077",
    "learning_graph":           "learning-graph-engine:50078",
    "learning_progression":     "learning-progression-engine:50079",
    "pedagogy_engine":          "pedagogy-engine:50080",
    "recommendation_engine":    "recommendation-engine:50081",
    
    // New Phase 6 services
    "retrieval_enhancement":     "retrieval-enhancement-service:50083",
    "semantic_enrichment":      "semantic-enrichment-service:50084",
    "educational_ontology":     "educational-ontology-service:50085",
}

// Add client types for new services
type AIAgentsServiceClient struct {
    conn *grpc.ClientConn
}

type HallucinationGuardServiceClient struct {
    conn *grpc.ClientConn
}

type EducationalObservabilityServiceClient struct {
    conn *grpc.ClientConn
}
```

### Phase 4: Docker Configuration Updates

#### 1. Update Dockerfile
Remove FastAPI startup, add gRPC server startup:

```dockerfile
# Run the gRPC server instead of FastAPI
CMD ["python", "app/grpc_server.py"]
```

#### 2. Update docker-compose.yml
Remove port exposures for HTTP, only expose gRPC ports:

```yaml
ai-agents-service:
  build: ./services/ai-agents-service
  ports:
    - "50072:50072"  # gRPC only
  environment:
    - ENABLE_GRPC_SERVER=true
    - ENABLE_REST_API=false
    - GRPC_PORT=50072
```

### Phase 5: Documentation Updates

#### 1. Update Service READMEs
Remove REST API documentation, add gRPC documentation:

```markdown
## gRPC Service

This service provides gRPC endpoints for AI functionality. 

### Port
- gRPC: 50072

### Proto Definition
See `proto/ai_agents.proto` for complete service definition.

### Client Implementation
See `backend/internal/messaging/grpc_client.go` for Go client example.
```

#### 2. Update IMPLEMENTATION_PHASES.md
Add note about gRPC architecture:

```markdown
## Architecture Note
All AI platform services communicate exclusively via gRPC with the backend.
No REST API JSON endpoints are exposed to ensure security and performance.
```

## Implementation Details

### Service-by-Service Conversion Plan

#### 1. AI Agents Service (Fase 7)
**Current Port**: 8023 (HTTP)
**Target Port**: 50072 (gRPC)
**Service Name**: `ai_agents`
**Proto File**: `proto/ai_agents.proto`

**Methods to Implement**:
- LessonPlanningAssistant
- AssessmentCreationAssistant
- StudentProgressAnalysis
- TeachingStrategyRecommendation
- PersonalizedGuidance
- QuestionAnswering
- LearningPathRecommendation
- AdaptiveInteraction
- CPGuidance
- ATPGuidance
- CurriculumAlignmentChecking
- CurriculumRecommendation
- ExpertKnowledgeIntegration
- AssessmentGenerationAssistant
- RubricCreationAssistant
- AssessmentAnalytics
- QualityValidation

#### 2. Hallucination Guard Service (Fase 8.1)
**Current Port**: 8024 (HTTP)
**Target Port**: 50073 (gRPC)
**Service Name**: `hallucination_guard`
**Proto File**: `proto/hallucination_guard.proto`

**Methods to Implement**:
- ValidateCurriculum
- ValidatePedagogy
- ValidateCompetency
- ValidateAssessment
- ValidatePhase
- ValidateRetrievalGrounding
- DetectHallucination

#### 3. Educational Observability Service (Fase 8.2)
**Current Port**: 8025 (HTTP)
**Target Port**: 50074 (gRPC)
**Service Name**: `educational_observability`
**Proto File**: `proto/educational_observability.proto`

**Methods to Implement**:
- GenerateLearningAnalytics
- GenerateCompetencyAnalytics
- MonitorAssessmentQuality
- MonitorRetrievalQuality
- MonitorPedagogyEffectiveness
- MonitorHallucinations

#### 4. Educational Intelligence Services (Fase 5)
**Services**: Adaptive Learning, Assessment, Curriculum, Learning Graph, Learning Progression, Pedagogy, Recommendation
**Target Ports**: 50075-50081 (gRPC)
**Proto File**: `proto/educational_intelligence.proto`

#### 5. Advanced Enhancement Services (Fase 6)
**Services**: Retrieval Enhancement, Semantic Enrichment, Educational Ontology
**Target Ports**: 50083-50085 (gRPC)
**Proto File**: `proto/advanced_enhancement.proto`

## Security Considerations

### Network Isolation
- gRPC services should run on internal network
- No public exposure of gRPC ports
- Backend acts as sole client to gRPC services

### Authentication
- Implement mutual TLS (mTLS) for gRPC communication
- Use service-to-service authentication
- Implement request validation and rate limiting

### Authorization
- Backend validates all requests to AI services
- Implement service-level authorization
- Audit all gRPC calls for compliance

## Performance Considerations

### gRPC Benefits
- Binary serialization (more efficient than JSON)
- HTTP/2 (multiplexing, header compression)
- Streaming support for large data transfers
- Built-in load balancing
- Strongly typed contracts

### Expected Performance Improvements
- **Latency**: 30-50% reduction vs HTTP/JSON
- **Throughput**: 2-3x increase vs HTTP/JSON
- **Bandwidth**: 50-70% reduction vs HTTP/JSON
- **Connection Reuse**: gRPC maintains persistent connections

## Testing Strategy

### 1. Unit Testing
- Test gRPC server implementation
- Test request/response conversion
- Test error handling

### 2. Integration Testing
- Test backend gRPC client communication
- Test end-to-end service interactions
- Test error scenarios

### 3. Performance Testing
- Benchmark gRPC vs HTTP performance
- Test under load conditions
- Validate SLA compliance

## Migration Path

### Option A: Big Bang (All services at once)
- Convert all services simultaneously
- Update backend to use new gRPC clients
- Deploy together
- **Risk**: Higher deployment complexity

### Option B: Gradual Migration (Recommended)
- Phase 1: Convert AI Agents Service (Fase 7) first
- Phase 2: Convert Hallucination Guard (Fase 8.1)
- Phase 3: Convert Educational Observability (Fase 8.2)
- Phase 4: Convert Fase 5 services
- Phase 5: Convert Fase 6 services
- **Risk**: Lower, easier to troubleshoot

## Rollback Plan

### If Issues Occur
1. Keep REST API as fallback initially
2. Use feature flags to switch between gRPC and REST
3. Monitor performance and error rates
4. Roll back to REST if critical issues occur

### Rollback Process
1. Switch backend to use HTTP clients
2. Restart services with REST API enabled
3. Investigate and fix issues
4. Attempt gRPC migration again

## Monitoring & Observability

### gRPC-Specific Metrics
- Request/response times per service
- Error rates per method
- Connection pool utilization
- gRPC specific metrics (streaming, compression)

### Logging
- Log all gRPC calls
- Include request/response metadata
- Log errors with full context
- Correlate logs with backend requests

## Next Steps

### Immediate Actions
1. Review and approve proto files
2. Implement gRPC server for AI Agents Service (first service)
3. Update backend gRPC client for AI Agents Service
4. Test end-to-end communication
5. Gradually migrate other services

### Long-term Actions
1. Implement mTLS for all gRPC communications
2. Add gRPC streaming for large data transfers
3. Implement gRPC load balancing
4. Add comprehensive gRPC monitoring

## Conclusion

Converting AI services from REST API to gRPC will provide significant security and performance benefits. The conversion should be done gradually, starting with the AI Agents Service (Fase 7) as the most critical user-facing component.

---

**Document Version**: 1.0  
**Created**: 2026-05-27  
**Status**: Architecture Definition Complete, Implementation Pending
