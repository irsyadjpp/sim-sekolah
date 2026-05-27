# AI Agents Service - Fase 7

**User-Facing Intelligence - 4 Specialized Educational Agents**

This service provides intelligent AI-powered agents designed to support educational stakeholders including teachers, students, curriculum developers, and assessment specialists.

## 🤖 Available Agents

### 1. Teacher Agent
A comprehensive assistant for educators that helps with:
- **Lesson Planning**: Create detailed lesson plans with learning objectives, activities, and assessments
- **Assessment Creation**: Generate formative and summative assessments with rubrics
- **Student Progress Analysis**: Analyze individual and class performance trends
- **Teaching Strategy Recommendations**: Suggest pedagogical approaches based on classroom context

### 2. Student Learning Agent
A personalized learning companion for students that provides:
- **Personalized Guidance**: Tailored learning support based on individual needs
- **Question Answering**: Intelligent Q&A with context awareness and conversation history
- **Learning Path Recommendations**: Adaptive learning paths based on mastery levels
- **Progress Tracking**: Monitor learning progress and identify areas for improvement
- **Adaptive Interaction**: Dynamic adjustment of content difficulty and engagement strategies

### 3. Curriculum Agent
A curriculum expert that assists with:
- **CP (Capaian Pembelajaran) Guidance**: Structured guidance for creating learning outcomes
- **ATP (Alur Tujuan Pembelajaran) Guidance**: Support for learning objective sequencing
- **Curriculum Alignment Checking**: Validate materials against curriculum standards
- **Curriculum Recommendations**: Suggestions for curriculum improvement
- **Expert Knowledge Integration**: Access to expert pedagogical knowledge and best practices

### 4. Assessment Agent
An assessment specialist that provides:
- **Assessment Generation**: Create comprehensive assessments aligned with learning objectives
- **Rubric Creation**: Develop detailed rubrics with performance criteria
- **Assessment Analytics**: Analyze assessment results and identify patterns
- **Quality Validation**: Ensure assessments meet quality standards before deployment

## 🚀 Features

### Core Capabilities
- **Conversation Management**: Maintain conversation context across interactions
- **Context Awareness**: Understand and utilize educational context
- **Adaptive Learning**: Dynamically adjust based on performance and engagement
- **Expert Knowledge**: Integrate validated educational research and best practices
- **Quality Assurance**: Multi-dimensional quality validation for educational content

### Performance Monitoring
- Response time tracking
- Agent usage analytics
- Satisfaction metrics
- Performance trend analysis

## 📡 Communication Protocols

This service supports both REST API and gRPC communication protocols:

### gRPC (Primary for Production)
The service uses gRPC for high-performance inter-service communication, accessible only by the backend.

- **Port**: 50072
- **Protocol**: gRPC
- **Access**: Backend-only (internal network)
- **Proto Definition**: `ai-platform/proto/ai_agents.proto`

#### gRPC Methods
The service exposes 16 gRPC methods across 4 agents:
- **Teacher Agent** (4 methods): LessonPlanningAssistant, AssessmentCreationAssistant, StudentProgressAnalysis, TeachingStrategyRecommendation
- **Student Learning Agent** (4 methods): PersonalizedGuidance, QuestionAnswering, LearningPathRecommendation, AdaptiveInteraction
- **Curriculum Agent** (5 methods): CPGuidance, ATPGuidance, CurriculumAlignmentChecking, CurriculumRecommendation, ExpertKnowledgeIntegration
- **Assessment Agent** (3 methods): AssessmentGenerationAssistant, RubricCreationAssistant, AssessmentAnalytics, QualityValidation

### REST API (Development/Testing)
REST API endpoints are available for local development and testing purposes.

- **Port**: 8023
- **Protocol**: HTTP/JSON
- **Access**: Local development and testing

## 📡 REST API Endpoints (Development Mode)

### Teacher Agent Endpoints
```bash
# Lesson Planning
POST /agent/teacher/lesson-planning
Body: {
  "topic": "string",
  "grade": "string",
  "subject": "string",
  "duration_minutes": int,
  "learning_objectives": [string],
  "pedagogy_type": "string",
  "context": {}
}

# Assessment Creation
POST /agent/teacher/assessment-creation
Body: {
  "topic": "string",
  "competency": "string",
  "grade": "string",
  "assessment_type": "string",
  "question_count": int,
  "difficulty": "string",
  "context": {}
}

# Student Progress Analysis
POST /agent/teacher/progress-analysis
Body: {
  "student_id": "string",
  "subject": "string",
  "time_period": "string",
  "include_recommendations": bool
}

# Teaching Strategy Recommendation
POST /agent/teacher/strategy-recommendation
Body: {
  "topic": "string",
  "grade": "string",
  "subject": "string",
  "class_size": int,
  "available_resources": [string],
  "student_profiles": [object]
}
```

### Student Learning Agent Endpoints
```bash
# Personalized Guidance
POST /agent/student/guidance
Body: {
  "student_id": "string",
  "subject": "string",
  "current_topic": "string",
  "learning_style": "string",
  "weak_areas": [string],
  "strong_areas": [string]
}

# Question Answering
POST /agent/student/question-answering
Body: {
  "student_id": "string",
  "question": "string",
  "subject": "string",
  "context": {},
  "conversation_history": [object]
}

# Learning Path Recommendation
POST /agent/student/learning-path
Body: {
  "student_id": "string",
  "target_competency": "string",
  "current_mastery": {},
  "learning_style": "string",
  "time_constraint": int
}

# Adaptive Interaction
POST /agent/student/adaptive-interaction
Body: {
  "student_id": "string",
  "subject": "string",
  "interaction_data": {
    "response_time": float,
    "correctness": float,
    "frequency": float
  }
}
```

### Curriculum Agent Endpoints
```bash
# CP Guidance
POST /agent/curriculum/cp-guidance
Body: {
  "phase": "string",
  "grade": "string",
  "subject": "string",
  "current_cp": {}
}

# ATP Guidance
POST /agent/curriculum/atp-guidance
Body: {
  "cp_id": "string",
  "semester": "string",
  "time_allocation": {}
}

# Alignment Checking
POST /agent/curriculum/alignment-check
Body: {
  "teaching_material": {},
  "phase": "string",
  "grade": "string",
  "subject": "string"
}

# Curriculum Recommendation
POST /agent/curriculum/recommendation
Body: {
  "phase": "string",
  "grade": "string",
  "subject": "string",
  "current_coverage": {}
}

# Expert Knowledge Integration
POST /agent/curriculum/expert-knowledge
Body: {
  "query": "string",
  "context": {}
}
```

### Assessment Agent Endpoints
```bash
# Assessment Generation
POST /agent/assessment/generation
Body: {
  "topic": "string",
  "competency": "string",
  "grade": "string",
  "assessment_type": "string",
  "cognitive_levels": [string],
  "question_count": int
}

# Rubric Creation
POST /agent/assessment/rubric
Body: {
  "assessment_type": "string",
  "criteria": [string],
  "performance_levels": int,
  "context": {}
}

# Assessment Analytics
POST /agent/assessment/analytics
Body: {
  "assessment_id": "string",
  "class_id": "string",
  "analysis_type": "string"
}

# Quality Validation
POST /agent/assessment/quality-validation
Body: {
  "assessment_data": {}
}
```

### Monitoring Endpoints
```bash
# Get Performance Metrics
GET /agents/performance

# Get Available Agents
GET /agents/available
```

## 🔧 Configuration

### Environment Variables
```bash
# Service Configuration
ENABLE_GRPC_SERVER=false
ENABLE_RABBITMQ_CONSUMER=false
GRPC_PORT=50072

# Database Configuration (if needed)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# AI Provider Configuration (if needed)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Vector Database Configuration (if needed)
QDRANT_URL=http://localhost:6333
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t ai-agents-service:latest .
```

### Run Container (gRPC Mode - Production)
```bash
docker run -d \
  --name ai-agents-service \
  -p 50072:50072 \
  -e RUN_MODE=grpc \
  -e GRPC_PORT=50072 \
  ai-agents-service:latest
```

### Run Container (REST API Mode - Development)
```bash
docker run -d \
  --name ai-agents-service \
  -p 8023:8023 \
  -e RUN_MODE=rest \
  ai-agents-service:latest
```

### Docker Compose
```yaml
services:
  ai-agents-service:
    build: ./services/ai-agents-service
    ports:
      - "50072:50072"  # gRPC
      - "8023:8023"    # REST API (dev only)
    environment:
      - RUN_MODE=grpc  # Use 'grpc' for production, 'rest' for development
      - GRPC_PORT=50072
    depends_on:
      - postgres
      - qdrant
```

### Startup Script
A convenience script is provided for running the service in gRPC mode:

```bash
# Run the service in gRPC mode
./start_grpc.sh

# Or specify a custom port
GRPC_PORT=50072 ./start_grpc.sh
```

## 🧪 Development

### Local Development

#### REST API Mode (Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8023 --reload
```

#### gRPC Mode (Production Testing)
```bash
# Install dependencies (includes gRPC libraries)
pip install -r requirements.txt

# Run the gRPC server
python app/grpc_server.py

# Or use the startup script
./start_grpc.sh
```

### Proto File Compilation
If you need to regenerate the gRPC stub files from proto definitions:

```bash
# Ensure grpcio-tools is installed
pip install grpcio-tools

# Generate Python stub files from proto
python -m grpc_tools.protoc \
  -I ../../proto \
  --python_out=. \
  --grpc_python_out=. \
  ../../proto/ai_agents.proto
```

### Testing
```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

## 📊 Architecture

The AI Agents Service follows a modular architecture:

```
ai-agents-service/
├── app/
│   └── main.py              # FastAPI application with all agent implementations
├── tests/                   # Test files
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Agent Implementation Structure

Each agent is implemented as a class with:
- **Core Methods**: Primary functionality for the agent's domain
- **Helper Methods**: Private methods for specific tasks
- **Context Management**: Memory and state management
- **Validation**: Quality checks and validation logic

## 🔄 Integration with Other Services

The AI Agents Service integrates with:
- **Educational Intelligence Services**: For domain-specific knowledge
- **Knowledge Graph Services**: For curriculum and competency data
- **Generation Service**: For AI-powered content generation
- **Audit Service**: For logging and compliance
- **Monitoring Service**: For performance tracking

## 📈 Performance Considerations

- **Response Time**: Target < 2 seconds for most operations
- **Concurrency**: Handle multiple concurrent requests
- **Memory Usage**: Efficient context management
- **Scalability**: Horizontal scaling capability

## 🔐 Security

- **Input Validation**: All inputs validated using Pydantic models
- **Context Isolation**: User-specific context isolation
- **Rate Limiting**: Configurable rate limiting (via Gateway)
- **Audit Logging**: All interactions logged for compliance

## 🌐 Language Support

- Primary language: Indonesian (Bahasa Indonesia)
- Secondary language: English
- Curriculum alignment: Kurikulum Merdeka (Indonesian National Curriculum)

## 📝 Usage Examples

### Example 1: Create a Lesson Plan
```python
import requests

response = requests.post(
    "http://localhost:8023/agent/teacher/lesson-planning",
    json={
        "topic": "Photosynthesis",
        "grade": "VII",
        "subject": "Science",
        "duration_minutes": 45,
        "learning_objectives": [
            "Understand the process of photosynthesis",
            "Identify the components needed for photosynthesis"
        ],
        "pedagogy_type": "inquiry"
    }
)

lesson_plan = response.json()
print(lesson_plan)
```

### Example 2: Adaptive Student Interaction
```python
import requests

response = requests.post(
    "http://localhost:8023/agent/student/adaptive-interaction",
    json={
        "student_id": "student_123",
        "subject": "Mathematics",
        "interaction_data": {
            "response_time": 25.5,
            "correctness": 0.8,
            "frequency": 1.2
        }
    }
)

adaptive_response = response.json()
print(adaptive_response)
```

### Example 3: Quality Validation
```python
import requests

response = requests.post(
    "http://localhost:8023/agent/assessment/quality-validation",
    json={
        "assessment_data": {
            "assessment_id": "assessment_001",
            "questions": [
                {
                    "id": "q1",
                    "question": "What is photosynthesis?",
                    "cognitive_level": "understand"
                }
            ]
        }
    }
)

quality_report = response.json()
print(quality_report)
```

## 🛣️ Roadmap

### Phase 7 Completed ✅
- [x] Teacher Agent implementation
- [x] Student Learning Agent implementation
- [x] Curriculum Agent implementation
- [x] Assessment Agent implementation
- [x] Adaptive interaction features
- [x] Expert knowledge integration
- [x] Quality validation system
- [x] API endpoints for all features
- [x] Performance monitoring
- [x] Docker deployment

### Future Enhancements
- [ ] Multi-language support expansion
- [ ] Advanced personalization algorithms
- [ ] Real-time collaboration features
- [ ] Voice interaction capabilities
- [ ] Integration with learning management systems
- [ ] Advanced analytics dashboard

## 📞 Support

For issues, questions, or contributions, please refer to the main project documentation.

## 📄 License

This service is part of the SIM Sekolah AI Platform project.

---

**Service Version**: 1.0.0  
**Implementation Phase**: Fase 7 - AI Agents  
**Last Updated**: 2026-05-27
