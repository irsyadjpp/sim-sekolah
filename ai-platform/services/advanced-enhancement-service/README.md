# Advanced Enhancement Service - Fase 6

**Advanced AI Capabilities - 3 Enhancement Services**

This service provides intelligent enhancement capabilities designed to improve retrieval quality, semantic understanding, and educational knowledge management through advanced AI techniques.

## 🔧 Available Services

### 1. Retrieval Enhancement Service
A retrieval optimization system that provides:
- **Query Enhancement**: Improve retrieval queries with semantic understanding
- **Query Expansion**: Expand queries with related terms and concepts
- **Result Reranking**: Rerank retrieval results using advanced algorithms
- **Educational Context**: Incorporate educational context into retrieval

### 2. Semantic Enrichment Service
A semantic understanding system that provides:
- **Content Enrichment**: Enrich content with semantic information and entities
- **Embedding Generation**: Generate embeddings for texts and documents
- **Knowledge Extraction**: Extract knowledge triples and relationships
- **Semantic Analysis**: Analyze semantic relationships and concepts

### 3. Educational Ontology Service
An educational knowledge system that provides:
- **Ontology Query**: Query educational ontologies for concepts and relationships
- **Alignment Validation**: Validate content alignment with educational standards
- **Related Concepts**: Find related concepts and dependencies
- **Knowledge Graph**: Access structured educational knowledge

## 📡 Communication Protocols

This service supports both REST API and gRPC communication protocols:

### gRPC (Primary for Production)
The service uses gRPC for high-performance inter-service communication, accessible only by the backend.

- **Ports**: 50083-50085 (one per service)
- **Protocol**: gRPC
- **Access**: Backend-only (internal network)
- **Proto Definition**: `ai-platform/proto/advanced_enhancement.proto`

#### gRPC Methods and Ports
- **Retrieval Enhancement Service** (Port 50083): EnhanceQuery, ExpandQuery, RerankResults
- **Semantic Enrichment Service** (Port 50084): EnrichContent, GenerateEmbeddings, ExtractKnowledge
- **Educational Ontology Service** (Port 50085): QueryOntology, ValidateAlignment, GetRelatedConcepts

### REST API (Development/Testing)
REST API endpoints are available for local development and testing purposes.

- **Port**: 50083 (default service - Retrieval Enhancement)
- **Protocol**: HTTP/JSON
- **Access**: Local development and testing

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t advanced-enhancement-service:latest .
```

### Run Container (gRPC Mode - Production)
```bash
# For specific service
docker run -d \
  --name advanced-enhancement-retrieval \
  -p 50083:50083 \
  -e RUN_MODE=grpc \
  advanced-enhancement-service:latest \
  python app/grpc_server.py retrieval-enhancement

# Or use startup script
./start_grpc.sh retrieval-enhancement
```

### Run Container (REST API Mode - Development)
```bash
docker run -d \
  --name advanced-enhancement-rest \
  -p 50083:50083 \
  -e RUN_MODE=rest \
  advanced-enhancement-service:latest
```

### Docker Compose
```yaml
services:
  advanced-enhancement-retrieval:
    build: ./services/advanced-enhancement-service
    ports:
      - "50083:50083"  # gRPC
    environment:
      - RUN_MODE=grpc
    command: ["python", "app/grpc_server.py", "retrieval-enhancement"]
  
  advanced-enhancement-semantic:
    build: ./services/advanced-enhancement-service
    ports:
      - "50084:50084"  # gRPC
    environment:
      - RUN_MODE=grpc
    command: ["python", "app/grpc_server.py", "semantic-enrichment"]
  
  advanced-enhancement-ontology:
    build: ./services/advanced-enhancement-service
    ports:
      - "50085:50085"  # gRPC
    environment:
      - RUN_MODE=grpc
    command: ["python", "app/grpc_server.py", "educational-ontology"]
```

## 🧪 Development

### Local Development

#### REST API Mode (Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 50083 --reload
```

#### gRPC Mode (Production Testing)
```bash
# Install dependencies (includes gRPC libraries)
pip install -r requirements.txt

# Run a specific gRPC service
./start_grpc.sh retrieval-enhancement
./start_grpc.sh semantic-enrichment
./start_grpc.sh educational-ontology
```

### Proto File Compilation
If you need to regenerate the gRPC stub files from proto definitions:

```bash
# Ensure grpcio-tools is installed
pip install grpcio-tools

# Generate Python stub files from proto
python -m grpc_tools.protoc \
  -I ../../proto \
  --python_out=app \
  --grpc_python_out=app \
  ../../proto/advanced_enhancement.proto
```

## 🔧 Configuration

### Environment Variables
```bash
# Service Configuration
RUN_MODE=grpc  # or 'rest' for development
GRPC_PORT=50083  # Base port for gRPC services

# Database Configuration (if needed)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# AI Provider Configuration (if needed)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Vector Database Configuration (if needed)
QDRANT_URL=http://localhost:6333
```

## 📋 Service Details

### Retrieval Enhancement Service
- **Port**: 50083 (gRPC)
- **Methods**: 3
- **Use Case**: Query enhancement, expansion, and result reranking

### Semantic Enrichment Service
- **Port**: 50084 (gRPC)
- **Methods**: 3
- **Use Case**: Content enrichment, embedding generation, knowledge extraction

### Educational Ontology Service
- **Port**: 50085 (gRPC)
- **Methods**: 3
- **Use Case**: Ontology querying, alignment validation, related concepts

## 🚀 Features

### Core Capabilities
- **Retrieval Optimization**: Advanced query enhancement and result reranking
- **Semantic Understanding**: Deep semantic analysis and enrichment
- **Knowledge Management**: Educational ontology and knowledge graphs
- **Multi-factor Enhancement**: Context-aware retrieval improvement
- **Embedding Generation**: High-quality text embeddings
- **Knowledge Extraction**: Automated knowledge triple extraction
- **Alignment Validation**: Standards compliance checking
- **Related Concepts**: Concept relationship discovery

### Performance Monitoring
- Retrieval quality metrics
- Enrichment accuracy tracking
- Query enhancement effectiveness
- Knowledge extraction precision

## 📊 Architecture

```
Backend (Go) 
    ↓ gRPC
Advanced Enhancement Service (Python)
    ├── Retrieval Enhancement Service (Port 50083)
    ├── Semantic Enrichment Service (Port 50084)
    └── Educational Ontology Service (Port 50085)
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📝 Integration

### with Retrieval Service
The Retrieval Enhancement Service can be integrated with the main retrieval pipeline:
1. Initial retrieval from vector database
2. Query enhancement and expansion
3. Result reranking with educational context
4. Enhanced results returned to backend

### with Content Processing
The Semantic Enrichment Service can enhance content processing:
1. Raw content ingestion
2. Semantic enrichment and entity extraction
3. Knowledge triple extraction
4. Enriched content stored with metadata

### with Curriculum Management
The Educational Ontology Service supports curriculum operations:
1. Content alignment validation
2. Related concept discovery
3. Knowledge graph queries
4. Standards compliance checking

## 📝 License

This service is part of the AI Platform project.
