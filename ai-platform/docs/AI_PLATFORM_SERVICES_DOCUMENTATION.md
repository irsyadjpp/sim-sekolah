# AI Platform Services - Comprehensive Feature Documentation

## Overview

The AI Platform is a microservices-based educational AI system built with Python, providing 26 gRPC services for various AI-powered educational functionalities including embedding, vision processing, retrieval, generation, parsing, semantic chunking, reranking, metadata enrichment, and more.

---

## Services Directory (26 gRPC Services)

### 1. Embedding Service (Port 50052)

**Features:**
- Text Embedding: Generate embeddings for text content
- Image Embedding: Generate embeddings for images
- Table Embedding: Generate embeddings for tables
- Formula Embedding: Generate embeddings for mathematical formulas
- Batch Text Embedding: Process multiple texts in a single request
- Model Information: Retrieve embedding model details

**Components:**
- TextEmbedder
- ImageEmbedder
- TableEmbedder
- FormulaEmbedder

---

### 2. Vision Service (Port 50055)

**Features:**
- OCR Processing: Extract text from images using OCR
- Diagram Analysis: Analyze diagrams and charts
- Formula Extraction: Extract mathematical formulas from images
- Image Classification: Classify images into categories
- Image Preprocessing: Preprocess images for better analysis

**Components:**
- OCRProcessor
- ImageClassifier
- ImageCaptioning
- DiagramAnalyzer
- ImageEmbeddings

---

### 3. Retrieval Service (Port 50054)

**Features:**
- Semantic Search: Vector-based semantic search
- Hybrid Search: Combined semantic and keyword search
- Metadata Filtering: Filter results by metadata
- Context Building: Build context from retrieved documents
- Query Expansion: Expand queries for better retrieval
- Relevance Scoring: Score document relevance

**Components:**
- SemanticRetriever
- HybridRetriever
- MetadataFilter
- ContextBuilder
- QueryExpander
- RelevanceScorer

---

### 4. Generation Service (Port 50053)

**Features:**
- Text Generation: Generate text from prompts
- Context-Aware Generation: Generate text with provided context
- Streaming Text: Stream text generation in real-time
- Quiz Generation: Generate quiz questions
- Lesson Plan Generation: Generate lesson plans
- Explanation Generation: Generate explanations

**Components:**
- TextGenerator
- QuizGenerator
- LessonPlanGenerator
- ExplanationGenerator

---

### 5. Parser Service (Port 50051)

**Features:**
- Document Parsing: Parse various document formats
- Text Extraction: Extract text from documents
- Table Extraction: Extract tables from documents
- Image Extraction: Extract images from documents
- OCR Processing: Perform OCR on document images
- Layout Detection: Detect document layout structure

**Components:**
- TextExtractor
- TableExtractor
- ImageExtractor
- OCRExtractor
- LayoutDetector
- ContentNormalizer
- DocumentPipeline

---

### 6. Semantic Chunk Service (Port 50056)

**Features:**
- Competency-Based Chunking: Chunk content by competency (KI-1, KI-2, KI-3, KI-4)
- Activity-Based Chunking: Chunk content by learning activities
- Assessment-Based Chunking: Chunk content by assessment items
- Inquiry-Based Chunking: Chunk content for inquiry learning
- Lesson Plan-Based Chunking: Chunk content by lesson plan structure
- Hierarchy Detection: Detect content hierarchy
- Pedagogy Classification: Classify pedagogical approaches
- Quality Validation: Validate chunk quality
- Metadata Enrichment: Enrich chunks with metadata

**Components:**
- CompetencyChunker
- ActivityChunker
- AssessmentChunker
- InquiryChunker
- LessonPlanChunker
- ChunkEnricher

---

### 7. Reranking Service (Port 50058)

**Features:**
- Cross-Encoder Reranking: Rerank using cross-encoder models
- Mono-Encoder Reranking: Rerank using mono-encoder models
- Curriculum-Aware Reranking: Rerank based on curriculum alignment
- Pedagogy-Aware Reranking: Rerank based on pedagogical relevance
- Competency-Aware Reranking: Rerank based on competency matching
- Hybrid Reranking: Combine multiple reranking strategies

**Components:**
- CrossEncoderReranker
- MonoEncoderReranker
- CurriculumAwareReranker
- PedagogyAwareReranker
- CompetencyAwareReranker
- HybridReranker

---

### 8. Metadata Service (Port 50057)

**Features:**
- Difficulty Enrichment: Enrich content with difficulty levels
- Taxonomy Classification: Classify content by taxonomy framework (Bloom's)
- Learning Style Detection: Detect student learning styles
- Competency Tagging: Tag content with competency information
- Pedagogy Tagging: Tag content with pedagogical information
- Assessment Tagging: Tag content with assessment metadata
- Batch Enrichment: Enrich multiple content items at once

**Components:**
- DifficultyEnricher
- TaxonomyClassifier
- LearningStyleDetector
- CompetencyTagger
- PedagogyTagger
- AssessmentTagger

---

### 9. Moderation Service (Port 50060)

**Features:**
- Content Moderation: Moderate content for safety
- Batch Moderation: Moderate multiple contents
- Toxicity Detection: Detect toxic content
- Bias Detection: Detect biased content

**Components:**
- ModerationEngine

---

### 10. Orchestration Service (Port 50061)

**Features:**
- Workflow Execution: Execute complex workflows
- Intent Detection: Detect user intent from queries
- Strategy Selection: Select retrieval and generation strategies

**Components:**
- WorkflowEngine

---

### 11. Pedagogy Engine (Port 50063)

**Features:**
- Pedagogy Analysis: Analyze pedagogical approaches
- Pedagogy Type Detection: Detect pedagogy types

**Components:**
- PedagogyEngine

---

### 12. Curriculum Engine (Port 50062)

**Features:**
- CP Validation: Validate Curriculum Programs
- ATP Validation: Validate Annual Teaching Plans
- Alignment Checking: Check CP/ATP alignment

**Components:**
- CurriculumEngine

---

### 13. Assessment Engine (Port 50064)

**Features:**
- Assessment Generation: Generate assessments
- HOTS Questions: Generate Higher Order Thinking Skills questions
- Rubric Generation: Generate assessment rubrics

**Components:**
- AssessmentEngine

---

### 14. Learning Progression Engine (Port 50065)

**Features:**
- Mastery Tracking: Track competency mastery progression
- Gap Detection: Detect prerequisite knowledge gaps

**Components:**
- LearningProgressionEngine

---

### 15. Recommendation Engine (Port 50068)

**Features:**
- Content Recommendations: Generate content recommendations

**Components:**
- RecommendationEngine

---

### 16. Adaptive Learning Engine (Port 50067)

**Features:**
- Personalized Learning Paths: Generate personalized learning paths
- Adaptive Content Selection: Select content adaptively

**Components:**
- AdaptiveLearningEngine

---

### 17. Learning Graph Engine (Port 50066)

**Features:**
- Graph Construction: Construct knowledge graphs
- Graph Querying: Query knowledge graphs

**Components:**
- LearningGraphEngine

---

### 18. Educational Ontology Service (Port 50071)

**Features:**
- Ontology Query: Query educational ontology
- Add/Update/Delete Nodes: Manage ontology nodes

**Components:**
- EducationalOntologyService

---

### 19. AI Agents Service (Port 50072)

**Teacher Agent (4 methods):**
- Lesson Planning Assistant
- Assessment Creation Assistant
- Student Progress Analysis
- Teaching Strategy Recommendation

**Student Learning Agent (4 methods):**
- Personalized Guidance
- Question Answering
- Learning Path Recommendation
- Adaptive Interaction

**Curriculum Agent (5 methods):**
- CP Guidance
- ATP Guidance
- Curriculum Alignment Checking
- Curriculum Recommendation
- Expert Knowledge Integration

**Assessment Agent (4 methods):**
- Assessment Generation Assistant
- Rubric Creation Assistant
- Assessment Analytics
- Quality Validation

**Components:**
- AIAgentsEngine
- TeacherAgent
- StudentLearningAgent
- CurriculumAgent
- AssessmentAgent

---

### 20. Educational Intelligence Service (Ports 50075-50081)

**Adaptive Learning Engine (2 methods):**
- Generate Personalized Learning Path
- Analyze Student Learning Pattern

**Assessment Engine (2 methods):**
- Generate Adaptive Assessment
- Analyze Assessment Results

**Curriculum Engine (2 methods):**
- Generate Curriculum Plan
- Align Content with Standards

**Learning Graph Engine (2 methods):**
- Build Learning Graph
- Analyze Learning Path

**Learning Progression Engine (2 methods):**
- Track Student Progression
- Predict Learning Outcomes

**Pedagogy Engine (2 methods):**
- Recommend Pedagogy Strategy
- Evaluate Teaching Effectiveness

**Recommendation Engine (2 methods):**
- Generate Content Recommendations
- Generate Activity Recommendations

**Components:**
- EducationalIntelligenceEngine

---

### 21. Hallucination Guard Service (Port 50073)

**Features:**
- Curriculum Validator: Validate curriculum content
- Pedagogy Validator: Validate pedagogical content
- Competency Validator: Validate competency alignment
- Assessment Validator: Validate assessment content
- Phase Validator: Validate phase-appropriate content
- Retrieval Grounding Validator: Validate retrieval grounding
- Hallucination Detection: Detect hallucinations in generated content

**Components:**
- HallucinationGuardEngine

---

### 22. Advanced Enhancement Service (Ports 50083-50085)

**Retrieval Enhancement Service (3 methods):**
- Enhance Query
- Expand Query
- Rerank Results

**Semantic Enrichment Service (3 methods):**
- Enrich Content
- Generate Embeddings
- Extract Knowledge

**Educational Ontology Service (3 methods):**
- Query Ontology
- Validate Alignment
- Get Related Concepts

**Components:**
- AdvancedEnhancementEngine

---

### 23. Retrieval Enhancement Service (Port 50069)

**Features:**
- Curriculum-Aware Rerank: Curriculum-aware reranking
- Pedagogy-Aware Retrieve: Pedagogy-aware retrieval
- Competency-Aware Retrieve: Competency-aware retrieval
- Assessment-Aware Retrieve: Assessment-aware retrieval
- Contextual Retrieve: Contextual retrieval
- Learning Style Retrieve: Learning style-based retrieval

---

### 24. Semantic Enrichment Service (Port 50070)

**Features:**
- Tag Competencies: Tag content with competencies
- Tag Pedagogy: Tag content with pedagogical information
- Tag Assessment: Tag content with assessment metadata
- Tag Cognitive Level: Tag content with cognitive levels
- Tag Learning Objective: Tag content with learning objectives
- Tag Deep Learning: Tag content with deep learning concepts

---

### 25. Audit Service (Port 50059)

**Features:**
- Log Event: Log audit events to database
- Query Logs: Query audit logs with filters
- Check Compliance: Check event compliance

**Components:**
- AuditServicer with PostgreSQL integration

---

### 26. Educational Observability Service (Port 50074)

**Features:**
- Learning Analytics: Learning analytics dashboard
- Competency Analytics: Competency analytics dashboard
- Assessment Quality Monitoring: Assessment quality monitoring dashboard
- Retrieval Quality Monitoring: Retrieval quality monitoring dashboard
- Pedagogy Effectiveness Monitoring: Pedagogy effectiveness monitoring dashboard
- Hallucination Monitoring: Hallucination monitoring dashboard

**Components:**
- EducationalObservabilityEngine

---

## Shared Directory

### Security Module

**Encryption Service (`encryption.py`):**
- AES-256-GCM symmetric encryption for strings and bytes
- PBKDF2-based password hashing with configurable iterations
- Secure token generation using `secrets` module

**Authentication Service (`auth.py`):**
- JWT token creation, verification, and refresh
- User authentication and session management
- Token payload dataclass with user information

**Authorization Service (`authorization.py`):**
- Role-based access control
- Permission checking

---

### Events Module

**Document Events (`document_events.py`):**
- DocumentUploadedEvent: Emitted when document is uploaded
- DocumentProcessedEvent: Emitted when document processing completes
- DocumentFailedEvent: Emitted when document processing fails
- DocumentDeletedEvent: Emitted when document is deleted

**Base Event (`base.py`):**
- Base event class with common fields

---

### Telemetry Module

**Performance Monitoring (`performance.py`):**
- PerformanceMonitor class for tracking operation metrics
- Metric recording with success/failure tracking
- Statistics calculation (avg, min, max, median, p95, p99)
- Decorator and context manager for performance tracking

**Health Monitoring (`health.py`):**
- Health check endpoints

**Resource Monitoring (`resource.py`):**
- CPU, memory, and disk resource monitoring

---

### Observability Module

**Metrics Collection (`metrics.py`):**
- Prometheus-style metrics (Counter, Gauge, Histogram)
- MetricsCollector for centralized metrics management
- Thread-safe metric operations
- Decorator for timing function calls

**Logging (`logger.py`):**
- Structured logging configuration

**Tracing (`tracing.py`):**
- Distributed tracing support

---

### Messaging Module

**RabbitMQ Messages (`rabbitmq_messages.py`):**
- Message types: PARSE_DOCUMENT, CHUNK_COMPETENCY, EMBED_TEXT, SEMANTIC_SEARCH, GENERATE_TEXT
- Message priorities: LOW, MEDIUM, HIGH, CRITICAL
- Queue definitions with TTL and max-length
- Exchange definitions (topic and direct)
- Exchange-queue bindings

**RabbitMQ Consumer (`rabbitmq_consumer.py`):**
- Async consumer for processing messages

---

### gRPC Module

**Client Factory (`client_factory.py`):**
- Factory for creating gRPC clients
- Connection pooling and reuse
- Service configuration with default addresses
- Global factory instance management

**Channel Management (`channel.py`):**
- Channel lifecycle management
- Connection health monitoring

---

### Configs Module

**Settings (`settings.py`):**
- Pydantic-based settings from environment variables
- Database, Redis, RabbitMQ, Qdrant, MinIO configuration
- JWT, monitoring, OpenTelemetry configuration
- AI model API keys and embedding settings
- Rate limiting, file upload, CORS, cache configuration
- Security headers and HTTPS settings

---

### Middleware Module

- **Authentication Middleware (`auth.py`):** JWT authentication
- **CORS Middleware (`cors.py`):** Cross-Origin Resource Sharing
- **Error Middleware (`error.py`):** Error handling
- **Logging Middleware (`logging.py`):** Request/response logging

---

### Utils Module

**Helpers (`helpers.py`):**
- Utility functions

---

### Schemas Module

**Common Schemas (`common.py`):**
- Shared Pydantic schemas

---

### Exceptions Module

**Custom Exceptions (`exceptions.py`):**
- Platform-specific exceptions

---

## Pipelines Directory

### Knowledge Ingestion Pipeline

**Features:**
- KnowledgeLoader: Discover and load knowledge assets from filesystem
- KnowledgeIngestionPipeline: Ingest assets into vector store and knowledge graph
- Asset Types: cp, atp, buku_guru, buku_siswa, modul_ajar, asesmen, p5, media
- File Formats: JSON, MD, TXT, CSV
- Vector Indexing: Index content to vector store
- Graph Edge Creation: Create edges for knowledge graph

---

### Generation Pipeline

**Features:**
- RetrievalStage: Fetch relevant documents
- ContextBuilderStage: Build context from retrieved documents
- LLMGenerationStage: Generate answer using LLM
- GuardrailStage: Filter and validate generated content
- GenerationPipeline: End-to-end pipeline orchestration
- Batch Processing: Process multiple requests
- Statistics: Track pipeline performance

---

### Metadata Tagging Pipeline

**Features:**
- MetadataTagger: Tag documents with difficulty, taxonomy, competencies
- EnrichmentPipeline: Batch enrichment pipeline
- Difficulty Detection: easy, medium, hard
- Taxonomy Detection: mathematics, science, etc.
- Competency Extraction: understanding, application, analysis, creation

---

## SDK Directory

### Python SDK (`sdk/python/simsekolah_ai/`)

**AIClient (Synchronous):**
- Built-in authentication with API key
- Retry logic with exponential backoff
- Circuit breaker protection
- HTTP timeout and connection limits
- Error handling (AuthenticationError, RateLimitError, ServiceUnavailableError, ValidationError)

**AsyncAIClient (Asynchronous):**
- Same features as AIClient but async
- Async context manager support

**Additional Components:**
- Config: Configuration management
- Circuit Breaker: Circuit breaker pattern for resilience
- Exceptions: Custom exception classes

---

## Tests Directory

### Test Coverage

**AI Agents Tests:**
- Tests for all 4 agents (Teacher, Student, Curriculum, Assessment)
- Unit tests for each agent method
- Integration tests for the AIAgentsEngine

**Pipeline Tests:**
- Tests for generation pipeline
- Tests for enrichment pipeline
- Tests for indexing pipeline
- Unit tests for each pipeline stage

**Testing Framework:**
- pytest-based unit tests with fixtures
- End-to-end pipeline testing
- Mock implementations for external dependencies

---

## Architecture Summary

### Communication Patterns

- **gRPC**: Synchronous service-to-service communication
- **RabbitMQ**: Asynchronous message processing
- **HTTP/REST**: External API access via SDK

### Key Technologies

- **gRPC**: Protocol Buffers for service communication
- **RabbitMQ**: Message queuing for async processing
- **PostgreSQL**: Audit logs storage
- **Qdrant**: Vector storage for embeddings
- **Redis**: Caching layer
- **MinIO**: Object storage for documents
- **Prometheus/Grafana**: Monitoring and visualization
- **OpenTelemetry**: Distributed tracing

### Design Patterns

- **Microservices Architecture**: Service-oriented design
- **Event-Driven Architecture**: Async message processing
- **Factory Pattern**: Client creation and management
- **Circuit Breaker Pattern**: Resilience and fault tolerance
- **Pipeline Pattern**: Data processing workflows
- **Agent Pattern**: AI assistant implementations

### Service Port Allocation

| Service | Port |
|---------|------|
| Parser Service | 50051 |
| Generation Service | 50053 |
| Retrieval Service | 50054 |
| Embedding Service | 50052 |
| Vision Service | 50055 |
| Semantic Chunk Service | 50056 |
| Metadata Service | 50057 |
| Reranking Service | 50058 |
| Audit Service | 50059 |
| Moderation Service | 50060 |
| Orchestration Service | 50061 |
| Curriculum Engine | 50062 |
| Pedagogy Engine | 50063 |
| Assessment Engine | 50064 |
| Learning Progression Engine | 50065 |
| Learning Graph Engine | 50066 |
| Adaptive Learning Engine | 50067 |
| Recommendation Engine | 50068 |
| Retrieval Enhancement Service | 50069 |
| Semantic Enrichment Service | 50070 |
| Educational Ontology Service | 50071 |
| AI Agents Service | 50072 |
| Hallucination Guard Service | 50073 |
| Educational Observability Service | 50074 |
| Educational Intelligence (Adaptive Learning) | 50075 |
| Educational Intelligence (Assessment) | 50076 |
| Educational Intelligence (Curriculum) | 50077 |
| Educational Intelligence (Learning Graph) | 50078 |
| Educational Intelligence (Learning Progression) | 50079 |
| Educational Intelligence (Pedagogy) | 50080 |
| Educational Intelligence (Recommendation) | 50081 |
| Advanced Enhancement (Retrieval) | 50083 |
| Advanced Enhancement (Semantic) | 50084 |
| Advanced Enhancement (Ontology) | 50085 |

---

## Conclusion

The AI Platform provides a comprehensive suite of 26 microservices designed to support educational AI applications. The platform covers the full spectrum of AI capabilities including natural language processing, computer vision, knowledge management, and educational-specific features like curriculum alignment, competency tracking, and pedagogical analysis. The microservices architecture ensures scalability, maintainability, and independent deployment of each service.
