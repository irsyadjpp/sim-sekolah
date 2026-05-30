# AI Platform Architecture Documentation - Domain-Driven Curriculum & Deep Learning Intelligence

**Project**: Indonesian Education AI Platform  
**Version**: 2.0 (Architecture Revision)  
**Last Updated**: 2026-05-30  
**Architecture Type**: Domain-Driven Monolith with Bounded Contexts  
**Focus**: AI-Native Curriculum & Deep Learning Intelligence Platform untuk Kurikulum Merdeka dan Pembelajaran Mendalam

---

## ⚠️ CRITICAL ARCHITECTURE PROBLEMS IDENTIFIED

Recent CTO-level architecture review identified **8 critical problems**:
1. Service/Engine explosion causing ambiguity and circular dependencies
2. Domain intelligence tercampur perlu bounded context evolution
3. shared/ folder berisiko menjadi "God folder"
4. Missing teacher workflow layer (platform masih AI-centric, bukan workflow-centric)
5. AI layer tidak jelas dipisah
6. Missing Deep Learning Pedagogy Layer untuk Pembelajaran Mendalam
7. Missing Standards Core sebagai foundation
8. Architecture over-engineered dengan premature enterprise patterns

**Status**: 🚨 **CRITICAL ARCHITECTURE REVISION REQUIRED**

---

## Executive Summary

AI Platform adalah **AI-Native Curriculum & Deep Learning Intelligence Platform** yang dirancang khusus untuk mendukung Kurikulum Merdeka Indonesia dan framework "Pembelajaran Mendalam" dari pemerintah. Platform menggunakan **domain-driven monolith architecture dengan bounded contexts** untuk optimal separation of concerns, scalability, dan alignment dengan teacher workflows.

**Critical Architecture Revision Required**: CTO-level review identified 8 critical problems yang perlu segera diatasi untuk menghindari technical debt explosion dan maintainability issues.

---

## 🎯 REVISED ARCHITECTURE STRATEGY

### New Architecture Focus (STOP/FOCUS)
**STOP**: 
- ❌ Over-engineering abstractions
- ❌ Premature microservice decomposition
- ❌ Future-proofing patterns
- ❌ Service/Engine explosion

**FOCUS**:
- ✅ Domain-driven bounded contexts
- ✅ Teacher-workflow centric design
- ✅ User-value first
- ✅ Simple before scaling

---

## 🏗️ REVISED DOMAIN-DRIVEN ARCHITECTURE

### 🎯 Recommended Bounded Context Structure

```
monolith/app/
├── standards-domain/              # FOUNDATION - Kurikulum Merdeka Standards
│   ├── kurikulum_merdeka/          # CP, ATP, Modul Ajar standards
│   ├── profil_pelajar_pancasila/    # 6 dimensi Profil Pelajar Pancasila
│   ├── capaian_pembelajaran/        # Learning objectives, competencies
│   ├── standards_repository/       # Standards database & validation
│   └── standards_api/              # National standards integration
│
├── curriculum-domain/            # Bounded Context - Kurikulum Management
│   ├── cp_management/             # CP (Curriculum Program)
│   ├── atp_generation/            # ATP (Annual Teaching Plan)
│   ├── modul_ajar_creation/        # Modul Ajar generator
│   ├── standards_alignment/         # Kurikulum Merdeka alignment validation
│   └── curriculum_service.py      # Public API for curriculum operations
│
├── assessment-domain/             # Bounded Context - Assessment & Evaluation
│   ├── assessment_generation/       # Task generation
│   ├── rubric_creation/            # Rubric creation & management
│   ├── evaluation/                  # Performance evaluation
│   ├── progress_tracking/           # Student progress
│   └── assessment_service.py       # Public API for assessment operations
│
├── learning-domain/               # Bounded Context - Deep Learning Intelligence
│   ├── adaptive_learning/           # Personalized learning paths
│   ├── differentiated_learning/      # Differentiated instruction
│   ├── mastery_tracking/            # Learning mastery depth
│   ├── progression/                # Learning progression
│   ├── deep_learning_pedagogy/      # PEMBELAJAR MENDAL LAYER
│   │   ├── reflection_engine/        # Reflection & self-regulation
│   │   ├── metacognition_engine/      # Metacognitive analysis
│   │   └── project_based_learning/    # P5 & project learning
│   └── learning_service.py          # Public API for learning operations
│
├── teacher-domain/                 # Bounded Context - TEACHER PRIMARY USER
│   ├── teacher_workflows/           # CRITICAL - Teacher Workflow Layer
│   │   ├── modul_ajar_workflow/      # Modul Ajar creation workflow
│   │   ├── cp_atp_workflow/          # CP → ATP workflow
│   │   ├── assessment_workflow/      # Assessment workflow
│   │   └── remediation_workflow/    # Remediation workflow
│   ├── planning_assistant/           # AI planning assistant
│   ├── resource_recommendation/      # Resource & activity recommendations
│   └── teacher_service.py          # Public API for teacher operations
│
├── student-domain/                 # Bounded Context - Student Learning Experience
│   ├── learning_journal/             # Learning journal & reflection
│   ├── progress_monitoring/         # Progress & mastery tracking
│   ├── reflection_engine/            # Reflection & self-regulation
│   ├── self_regulation/             # Self-regulation tracking
│   └── student_service.py          # Public API for student operations
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
├── content_processing/              # Content Processing Domain
│   ├── ingestion/                  # Document ingestion
│   ├── parsing/                     # Text, figure extraction
│   ├── chunking/                    # Semantic chunking
│   ├── enrichment/                  # Content enrichment
│   └── processing_service.py      # Public API for content operations
│
├── support/                       # Support Domain
│   ├── observability/               # Monitoring & analytics
│   ├── governance/                  # Audit & compliance
│   ├── notification/               # Notifications
│   └── support_service.py          # Public API for support operations
│
├── common/                         # TRUE SHARED ONLY (NOT GOD FOLDER)
│   ├── utils/                      # Cross-cutting utilities ONLY
│   └── constants/                  # Shared constants
│
├── api/                            # API Layer (FastAPI)
│   ├── curriculum/                 # Curriculum domain APIs
│   ├── assessment/                 # Assessment domain APIs
│   ├── learning/                    # Learning domain APIs
│   ├── teacher/                     # Teacher domain APIs
│   ├── student/                     # Student domain APIs
│   └── support/                     # Support domain APIs
│
└── models/                         # Data Models & Schemas

### 🏗️ Architecture Overview

```
AI Platform
├── Monolith (Unified Deployment)
│   ├── Application Layer (FastAPI)
│   ├── Business Logic Layer (Services)
│   ├── Data Processing Layer (Extractors, Chunkers, etc.)
│   └── Integration Layer (gRPC, RabbitMQ)
├── Infrastructure (Docker, Kubernetes)
├── Shared Libraries (SDK, Common Utils)
├── Documentation
└── Testing Framework
```

### 🔄 Deployment Patterns

**Monolith Mode**: All services run in single FastAPI application  
**Microservice Mode**: Individual services can be deployed as separate microservices  
**Hybrid Mode**: Critical services as microservices, others in monolith

---

## Directory Structure

### 📁 Root Level Structure

```
ai-platform/
├── monolith/          # Main application code (monolith mode)
├── infra/             # Infrastructure configuration
├── sdk/               # Client SDK for external integration
├── shared/            # Shared libraries and utilities
├── docs/              # Documentation
├── tests/             # Test suites
├── pipelines/         # CI/CD pipelines
├── scripts/           # Utility scripts
├── workers/           # Background job workers
├── models/            # ML model storage
├── knowledge/         # Knowledge base and reference materials
├── legacy/            # Legacy code (deprecated)
└── storage/           # Storage configurations
```

---

## Monolith Application Structure

### 🎯 Core Application Layers

```
monolith/app/
├── main.py                    # FastAPI application entry point
├── api/                       # REST API routes
│   ├── content_processing/    # Content processing endpoints
│   ├── document_ingestion/    # Document ingestion endpoints
│   ├── intelligence/          # Educational intelligence endpoints
│   └── support/               # Support service endpoints
├── services/                  # Business logic services
│   ├── content_processing/    # Content processing services
│   ├── document_ingestion/    # Document ingestion services
│   ├── intelligence/          # Educational intelligence services
│   └── support/               # Support services
├── builders/                  # Builder pattern implementations
├── chunkers/                  # Text chunking algorithms
├── classifiers/               # Content classification models
├── config/                    # Configuration management
├── core/                      # Core utilities and base classes
├── embedders/                 # Text embedding generators
├── enrichers/                 # Content enrichment services
├── enrichment/                # Enrichment orchestration
├── extractors/                # Data extraction from documents
├── hierarchy/                 # Hierarchical data structures
├── integrations/              # External service integrations
├── messaging/                 # Messaging and event handling
├── models/                    # Data models and schemas
├── normalizers/               # Data normalization utilities
├── pedagogy/                  # Pedagogical models and logic
├── pipelines/                 # Processing pipelines
├── processors/                # Data processing utilities
├── providers/                 # Provider implementations (OpenAI, etc.)
├── retrievers/                # Information retrieval systems
├── schemas/                   # Data validation schemas
├── taggers/                   # Content tagging services
├── taxonomy/                  # Educational taxonomy definitions
├── validators/                # Data validation utilities
└── __init__.py
```

---

## Service Architecture

### 🎯 Services Organization by Domain

#### 1. Intelligence Services (Educational Intelligence Layer)
**Purpose**: Educational intelligence and personalized learning

**Files Outside Folders** (Monolith Service Instances):
- `adaptive_learning_service.py` - Personalized learning path generation
- `assessment_service.py` - Assessment creation and analytics
- `curriculum_service.py` - Curriculum planning and alignment
- `learning_graph_service.py` - Learning graph construction
- `learning_progression_service.py` - Learning progression tracking
- `pedagogy_service.py` - Pedagogical recommendations
- `recommendation_service.py` - Learning recommendations
- `strategic_analysis_service.py` - Strategic educational analysis
- `ai_agents_service.py` - AI agents orchestration (wrapper)
- `educational_intelligence_service.py` - General educational intelligence (wrapper)
- `educational_ontology_service.py` - Educational ontology management (wrapper)

**Folder-Based Microservice Implementations**:
- `ai_agents_service/` - AI Agents microservice (FastAPI, gRPC, consumer)
- `adaptive_learning_engine/` - Adaptive Learning Engine microservice
- `assessment_engine/` - Assessment Engine microservice
- `curriculum_engine/` - Curriculum Engine microservice
- `educational_intelligence_service/` - Educational Intelligence microservice
- `educational_ontology_service/` - Educational Ontology microservice
- `learning_graph_engine/` - Learning Graph Engine microservice
- `learning_progression_engine/` - Learning Progression Engine microservice
- `ontology_validation_service/` - Ontology Validation microservice
- `pedagogy_engine/` - Pedagogy Engine microservice
- `recommendation_engine/` - Recommendation Engine microservice

**Architecture Pattern**: Hybrid - Monolith instances for main.py integration, microservice folders for standalone deployment

#### 2. Support Services (Infrastructure Layer)
**Purpose**: Platform support and operational services

**Files Outside Folders** (Monolith Service Instances):
- `audit_service.py` - Audit and compliance tracking
- `educational_observability_service.py` - Educational observability
- `gateway_service.py` - API gateway and routing
- `governance_service.py` - Governance and policy enforcement
- `moderation_service.py` - Content moderation
- `monitoring_service.py` - System monitoring and metrics
- `notification_service.py` - Notification management
- `observability_service.py` - System observability
- `orchestration_service.py` - Service orchestration

**Folder-Based Microservice Implementations**:
- `audit_service/` - Audit microservice with compliance, logs
- `educational_observability_service/` - Educational observability microservice
- `gateway_service/` - Gateway microservice with adapters, auth, policies
- `moderation_service/` - Moderation microservice with content filters
- `monitoring_service/` - Monitoring microservice with dashboards, metrics
- `notification_service/` - Notification microservice
- `orchestration_service/` - Orchestration microservice with workflows
- `metadata_service/` - Metadata enrichment microservice

**Architecture Pattern**: Hybrid - Monolith instances for main.py integration, microservice folders for standalone deployment

#### 3. Content Processing Services (Core Processing Layer)
**Purpose**: Document content processing and enrichment

**Files Outside Folders** (Monolith Service Instances):
- `embedding_service.py` - Text embedding generation
- `generation_service.py` - Content generation
- `hallucination_guard_service.py` - Hallucination detection and prevention
- `metadata_service.py` - Metadata extraction and enrichment
- `minio_chunking_service.py` - Chunking with MinIO storage
- `ontology_validation_service.py` - Ontology-based validation
- `reranking_service.py` - Search result reranking
- `retrieval_enhancement_service.py` - Enhanced retrieval
- `retrieval_service.py` - Information retrieval
- `semantic_chunk_service.py` - Semantic text chunking
- `semantic_enrichment_service.py` - Semantic enrichment
- `vision_service.py` - Computer vision processing

**Folder-Based Microservice Implementations**:
- `advanced_enhancement/` - Advanced enhancement microservice
- `chunk_helpers/` - Chunking utility helpers (newly created)
- `embedding_service/` - Embedding microservice with embedders, vectorizers
- `hallucination_guard_service/` - Hallucination guard microservice
- `reranking_service/` - Reranking microservice with ranking algorithms
- `retrieval_enhancement_service/` - Retrieval enhancement microservice

**Architecture Pattern**: Hybrid - Monolith instances for main.py integration, microservice folders for specialized processing

#### 4. Document Ingestion Services (Ingestion Layer)
**Purpose**: Document ingestion and processing

**Files Outside Folders** (Monolith Service Instances):
- `parser_service.py` - Document parsing
- `pipeline_tracker_service.py` - Pipeline tracking

**Folder-Based Microservice Implementations**:
- `pipeline_tracker_service/` - Pipeline tracking microservice

**Architecture Pattern**: Hybrid - Monolith instances for main.py integration, microservice folders for advanced tracking

---

## Hybrid Architecture Pattern

### 🎯 Design Rationale

**Files Outside Folders**: Provide monolith service instances that are imported and used by `main.py` for unified deployment. These contain business logic classes that can be instantiated directly.

**Folder-Based Microservices**: Complete microservice implementations with:
- `main.py` - FastAPI application entry point
- `grpc_server.py` - gRPC server implementation
- `consumer.py` - RabbitMQ consumer for async processing
- Additional subdirectories for specialized functionality

### 🔄 Deployment Modes

#### Monolith Mode (Current Default)
```python
# main.py imports and instantiates services
from app.services.intelligence.adaptive_learning_service import AdaptiveLearningService
from app.services.intelligence.assessment_service import AssessmentService

adaptive_learning_service = AdaptiveLearningService()
assessment_service = AssessmentService()
```

#### Microservice Mode
Each folder can be deployed independently as a standalone microservice with its own FastAPI server, gRPC server, and message consumer.

#### Hybrid Mode
Critical services deployed as microservices, others run in monolith for resource optimization.

---

## Key Components

### 📊 Extractors (Data Extraction)
- `formula_extractor.py` - Mathematical formula extraction
- `figure_extractor.py` - Pedagogical figure interpretation
- `image_extractor.py` - Image data extraction
- `ocr_extractor.py` - OCR text extraction
- `text_extractor.py` - Text content extraction
- `table_extractor.py` - Table data extraction

### 🧠 Classifiers (Content Classification)
- `chunk_classifier.py` - Content chunk classification
- `pedagogical_classifier.py` - Pedagogical intent classification
- `bloom_semantic_classifier.py` - Bloom's taxonomy classification

### 🔧 Builders & Chunkers
- Various builder pattern implementations
- Multiple chunking algorithms for different content types

### 🎯 Models & Schemas
- Comprehensive data models for all domains
- Validation schemas for API inputs/outputs
- Educational taxonomy definitions

---

## File Organization Analysis

### ✅ Current Structure Status

**Total Files Analyzed**: 147 directories, 34 service files outside folders

**Pattern Identified**: Intentional hybrid architecture for deployment flexibility

**Wrapper Files Identified** (3 total):
1. `ai_agents_service.py` - Wrapper with dependencies (routes depend on it)
2. `educational_intelligence_service.py` - Safe wrapper (no active dependencies)
3. `educational_ontology_service.py` - Wrapper with critical dependencies

**Recommendation**: Keep current hybrid structure as it's designed for deployment flexibility

---

## Technology Stack

### 🛠️ Core Technologies
- **Language**: Python 3.x
- **Web Framework**: FastAPI
- **RPC**: gRPC
- **Message Queue**: RabbitMQ
- **Container**: Docker
- **Orchestration**: Kubernetes (optional)

### 🎯 AI/ML Libraries
- OpenAI API
- Anthropic API
- Various embedding models
- Computer vision libraries

### 💾 Storage
- PostgreSQL
- Vector Database
- MinIO (S3-compatible)
- Redis (caching)

---

## Integration Points

### 🔄 External Integrations
- **AI Providers**: OpenAI, Anthropic
- **Storage**: MinIO, S3
- **Messaging**: RabbitMQ
- **Database**: PostgreSQL, vector DB
- **Monitoring**: Observability services

### 📡 Communication Protocols
- **REST**: FastAPI endpoints
- **gRPC**: High-performance RPC
- **AMQP**: RabbitMQ messaging
- **WebSocket**: Real-time updates (future)

---

## Deployment Architecture

### 🚀 Deployment Options

#### Option 1: Full Monolith (Simplest)
- Single Docker container
- All services in one FastAPI app
- Ideal for development and small deployments

#### Option 2: Critical Microservices (Recommended)
- Core services as microservices
- Support services in monolith
- Balance of scalability and simplicity

#### Option 3: Full Microservices (Most Complex)
- Each service as independent microservice
- Maximum scalability and resilience
- Higher operational complexity

---

## Security & Governance

### 🔐 Security Features
- API Gateway with authentication
- Content moderation service
- Audit and compliance tracking
- Governance service for policy enforcement

### 📊 Observability
- Monitoring service with dashboards
- Educational observability service
- System metrics and health checks
- Distributed tracing

---

## Development Workflow

### 🛠️ Development Process
1. **Feature Development**: Add business logic to service files
2. **Microservice Enhancement**: Extend folder-based microservices as needed
3. **Testing**: Comprehensive test coverage
4. **Documentation**: Update architecture docs
5. **Deployment**: Choose appropriate deployment mode

### 🧪 Testing Strategy
- Unit tests for individual components
- Integration tests for service interactions
- End-to-end tests for full workflows
- Performance tests for scalability

---

## Performance Considerations

### ⚡ Performance Optimization
- Async processing with RabbitMQ
- Caching with Redis
- Vector database for efficient retrieval
- Load balancing for microservices

### 📈 Scalability
- Horizontal scaling of microservices
- Database sharding for large datasets
- CDN for static content delivery
- Optimized algorithms for content processing

---

## Maintenance & Operations

### 🔧 Maintenance Strategy
- Regular code quality reviews
- Dependency updates and security patches
- Performance monitoring and optimization
- Architecture evolution based on requirements

### 📊 Monitoring & Alerting
- Service health monitoring
- Performance metrics tracking
- Error logging and alerting
- Capacity planning

---

## Future Roadmap

### 🎯 Planned Enhancements
1. **AI Capabilities**: More sophisticated AI agents
2. **Real-time Features**: WebSocket-based real-time updates
3. **Advanced Analytics**: Enhanced educational analytics
4. **Mobile Support**: Mobile-first UI/UX
5. **Multi-language**: Support for regional languages

### 🏗️ Architecture Evolution
- Event-driven architecture implementation
- GraphQL API support
- Advanced microservice patterns (service mesh)
- Cloud-native optimization

---

## Conclusion

AI Platform uses intentional hybrid architecture that provides deployment flexibility while maintaining code organization clarity. The structure supports both monolith and microservice deployment patterns, allowing the platform to scale from development to production with minimal architectural changes.

**Key Strengths**:
- Deployment flexibility (monolith/microservice/hybrid)
- Clear separation of concerns by domain
- Comprehensive educational AI capabilities
- Robust support and governance layer
- Extensible and maintainable structure

**Architecture Decision**: Keep current hybrid structure as it provides optimal balance of simplicity and scalability for educational technology deployment.

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-30  
**Maintained By**: AI Platform Development Team