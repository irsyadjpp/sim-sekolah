# Educational Intelligence Service - Fase 5

**Advanced Educational Capabilities - 7 Educational Intelligence Engines**

This service provides intelligent educational engines designed to support advanced educational operations including adaptive learning, assessment generation, curriculum planning, learning graph analysis, learning progression tracking, pedagogy recommendations, and content recommendations.

## 🧠 Available Engines

### 1. Adaptive Learning Engine
A personalized learning system that provides:
- **Personalized Learning Paths**: Generate customized learning sequences based on student profile
- **Learning Pattern Analysis**: Analyze student learning patterns and behaviors
- **Adaptive Content Delivery**: Dynamically adjust content difficulty and presentation
- **Real-time Adaptation**: Modify learning paths based on performance

### 2. Assessment Engine
An intelligent assessment system that provides:
- **Adaptive Assessment Generation**: Create assessments that adapt to student ability
- **Assessment Analysis**: Analyze assessment results and provide insights
- **Difficulty Calibration**: Adjust question difficulty based on performance
- **Comprehensive Analytics**: Detailed analysis of student performance

### 3. Curriculum Engine
A curriculum planning system that provides:
- **Curriculum Plan Generation**: Create comprehensive curriculum plans
- **Content Alignment**: Align content with educational standards and frameworks
- **Competency Mapping**: Map learning objectives to curriculum standards
- **Time Optimization**: Optimize time allocation for different topics

### 4. Learning Graph Engine
A knowledge graph system that provides:
- **Learning Graph Construction**: Build knowledge graphs of subject dependencies
- **Learning Path Analysis**: Analyze and optimize learning paths
- **Prerequisite Mapping**: Identify prerequisite relationships between concepts
- **Bottleneck Detection**: Identify learning bottlenecks and suggest alternatives

### 5. Learning Progression Engine
A progression tracking system that provides:
- **Student Progression Tracking**: Monitor student progress across competencies
- **Learning Outcome Prediction**: Predict future learning outcomes
- **Mastery Level Analysis**: Track mastery levels for different competencies
- **Intervention Recommendations**: Suggest interventions when needed

### 6. Pedagogy Engine
A pedagogical recommendation system that provides:
- **Pedagogy Strategy Recommendations**: Suggest optimal teaching strategies
- **Teaching Effectiveness Evaluation**: Evaluate the effectiveness of pedagogical approaches
- **Differentiation Strategies**: Provide strategies for differentiated instruction
- **Assessment Method Recommendations**: Suggest appropriate assessment methods

### 7. Recommendation Engine
A content recommendation system that provides:
- **Content Recommendations**: Recommend learning content based on student needs
- **Activity Recommendations**: Suggest learning activities and exercises
- **Personalization**: Personalize recommendations based on learning profile
- **Multi-factor Scoring**: Use multiple factors to score recommendations

## 📡 Communication Protocols

This service supports both REST API and gRPC communication protocols:

### gRPC (Primary for Production)
The service uses gRPC for high-performance inter-service communication, accessible only by the backend.

- **Ports**: 50075-50081 (one per engine)
- **Protocol**: gRPC
- **Access**: Backend-only (internal network)
- **Proto Definition**: `ai-platform/proto/educational_intelligence.proto`

#### gRPC Methods and Ports
- **Adaptive Learning Engine** (Port 50075): GeneratePersonalizedLearningPath, AnalyzeStudentLearningPattern
- **Assessment Engine** (Port 50076): GenerateAdaptiveAssessment, AnalyzeAssessmentResults
- **Curriculum Engine** (Port 50077): GenerateCurriculumPlan, AlignContentWithStandards
- **Learning Graph Engine** (Port 50078): BuildLearningGraph, AnalyzeLearningPath
- **Learning Progression Engine** (Port 50079): TrackStudentProgression, PredictLearningOutcomes
- **Pedagogy Engine** (Port 50080): RecommendPedagogyStrategy, EvaluateTeachingEffectiveness
- **Recommendation Engine** (Port 50081): GenerateContentRecommendations, GenerateActivityRecommendations

### REST API (Development/Testing)
REST API endpoints are available for local development and testing purposes.

- **Port**: 50075 (default engine - Adaptive Learning)
- **Protocol**: HTTP/JSON
- **Access**: Local development and testing

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t educational-intelligence-service:latest .
```

### Run Container (gRPC Mode - Production)
```bash
# For specific engine
docker run -d \
  --name educational-intelligence-adaptive \
  -p 50075:50075 \
  -e RUN_MODE=grpc \
  educational-intelligence-service:latest \
  python app/grpc_server.py adaptive-learning

# Or use startup script
./start_grpc.sh adaptive-learning
```

### Run Container (REST API Mode - Development)
```bash
docker run -d \
  --name educational-intelligence-rest \
  -p 50075:50075 \
  -e RUN_MODE=rest \
  educational-intelligence-service:latest
```

### Docker Compose
```yaml
services:
  educational-intelligence-adaptive:
    build: ./services/educational-intelligence-service
    ports:
      - "50075:50075"  # gRPC
    environment:
      - RUN_MODE=grpc
    command: ["python", "app/grpc_server.py", "adaptive-learning"]
  
  educational-intelligence-assessment:
    build: ./services/educational-intelligence-service
    ports:
      - "50076:50076"  # gRPC
    environment:
      - RUN_MODE=grpc
    command: ["python", "app/grpc_server.py", "assessment"]
```

## 🧪 Development

### Local Development

#### REST API Mode (Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 50075 --reload
```

#### gRPC Mode (Production Testing)
```bash
# Install dependencies (includes gRPC libraries)
pip install -r requirements.txt

# Run a specific gRPC engine
./start_grpc.sh adaptive-learning
./start_grpc.sh assessment
./start_grpc.sh curriculum
./start_grpc.sh learning-graph
./start_grpc.sh learning-progression
./start_grpc.sh pedagogy
./start_grpc.sh recommendation
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
  ../../proto/educational_intelligence.proto
```

## 🔧 Configuration

### Environment Variables
```bash
# Service Configuration
RUN_MODE=grpc  # or 'rest' for development
GRPC_PORT=50075  # Base port for gRPC services

# Database Configuration (if needed)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# AI Provider Configuration (if needed)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Vector Database Configuration (if needed)
QDRANT_URL=http://localhost:6333
```

## 📋 Engine Details

### Adaptive Learning Engine
- **Port**: 50075 (gRPC)
- **Methods**: 2
- **Use Case**: Personalized learning path generation and pattern analysis

### Assessment Engine
- **Port**: 50076 (gRPC)
- **Methods**: 2
- **Use Case**: Adaptive assessment generation and analysis

### Curriculum Engine
- **Port**: 50077 (gRPC)
- **Methods**: 2
- **Use Case**: Curriculum planning and content alignment

### Learning Graph Engine
- **Port**: 50078 (gRPC)
- **Methods**: 2
- **Use Case**: Knowledge graph construction and path analysis

### Learning Progression Engine
- **Port**: 50079 (gRPC)
- **Methods**: 2
- **Use Case**: Progression tracking and outcome prediction

### Pedagogy Engine
- **Port**: 50080 (gRPC)
- **Methods**: 2
- **Use Case**: Pedagogy recommendations and effectiveness evaluation

### Recommendation Engine
- **Port**: 50081 (gRPC)
- **Methods**: 2
- **Use Case**: Content and activity recommendations

## 🚀 Features

### Core Capabilities
- **Multi-Engine Architecture**: 7 specialized educational engines
- **Adaptive Learning**: Personalized learning paths and content
- **Intelligent Assessment**: Adaptive assessments and analytics
- **Curriculum Intelligence**: Smart curriculum planning and alignment
- **Knowledge Graphs**: Learning dependencies and path optimization
- **Progression Tracking**: Comprehensive student progression monitoring
- **Pedagogical Intelligence**: Teaching strategy recommendations
- **Smart Recommendations**: Content and activity suggestions

### Performance Monitoring
- Response time tracking
- Engine usage analytics
- Recommendation accuracy metrics
- Learning outcome predictions

## 📊 Architecture

```
Backend (Go) 
    ↓ gRPC
Educational Intelligence Service (Python)
    ├── Adaptive Learning Engine (Port 50075)
    ├── Assessment Engine (Port 50076)
    ├── Curriculum Engine (Port 50077)
    ├── Learning Graph Engine (Port 50078)
    ├── Learning Progression Engine (Port 50079)
    ├── Pedagogy Engine (Port 50080)
    └── Recommendation Engine (Port 50081)
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📝 License

This service is part of the AI Platform project.
