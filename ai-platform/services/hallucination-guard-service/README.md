# Hallucination Guard Service - Fase 8.1

**Advanced AI Capabilities - 6 AI Validators + Hallucination Detection System**

This service provides comprehensive validation and hallucination detection capabilities for AI-generated educational content, ensuring accuracy, reliability, and alignment with educational standards.

## 🛡️ Overview

The Hallucination Guard Service is designed to detect and prevent AI hallucinations in educational content through multiple specialized validators and ML-powered detection mechanisms. It ensures that AI-generated content aligns with curriculum standards, pedagogical best practices, and competency frameworks.

## 🎯 Core Features

### 6 Specialized Validators

1. **Curriculum Validator**: Validates content against curriculum standards and learning outcomes
2. **Pedagogy Validator**: Ensures pedagogical approaches align with best practices
3. **Competency Validator**: Validates competency framework alignment and progression
4. **Assessment Validator**: Checks assessment quality, fairness, and validity
5. **Phase Validator**: Ensures developmental appropriateness for target phases
6. **Retrieval Grounding Validator**: Validates answer grounding in retrieved context

### Hallucination Detection System

- **Factual Consistency Checking**: Detects factual errors and inconsistencies
- **Logical Coherence Analysis**: Ensures logical flow and coherence
- **Contextual Appropriateness**: Validates fit within educational context
- **Source Verification**: Verifies claims against reference materials
- **Contradiction Detection**: Identifies contradictory statements

## 📡 API Endpoints

### Validation Endpoints

#### Curriculum Validator
```bash
POST /validator/curriculum
Content-Type: application/json

{
  "request_id": "uuid",
  "content": "string",
  "phase": "string",
  "grade": "string",
  "subject": "string",
  "expected_outcomes": ["string"],
  "context": {}
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "validator_type": "curriculum",
  "is_valid": true,
  "confidence_score": 0.85,
  "issues": [],
  "suggestions": [],
  "metadata": {
    "validation_details": {
      "curriculum_alignment": {...},
      "learning_outcomes_coverage": {...},
      "developmental_appropriateness": {...}
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Pedagogy Validator
```bash
POST /validator/pedagogy
Content-Type: application/json

{
  "request_id": "uuid",
  "content": "string",
  "pedagogy_type": "string",
  "target_grade": "string",
  "learning_objectives": ["string"],
  "context": {}
}
```

#### Competency Validator
```bash
POST /validator/competency
Content-Type: application/json

{
  "request_id": "uuid",
  "content": "string",
  "competency_framework": "string",
  "competency_level": "string",
  "subject": "string",
  "context": {}
}
```

#### Assessment Validator
```bash
POST /validator/assessment
Content-Type: application/json

{
  "request_id": "uuid",
  "assessment_content": "string",
  "assessment_type": "string",
  "cognitive_levels": ["string"],
  "subject": "string",
  "context": {}
}
```

#### Phase Validator
```bash
POST /validator/phase
Content-Type: application/json

{
  "request_id": "uuid",
  "content": "string",
  "target_phase": "string",
  "developmental_stage": "string",
  "context": {}
}
```

#### Retrieval Grounding Validator
```bash
POST /validator/retrieval-grounding
Content-Type: application/json

{
  "request_id": "uuid",
  "generated_answer": "string",
  "retrieved_context": ["string"],
  "query": "string",
  "context": {}
}
```

### Hallucination Detection Endpoint

```bash
POST /detector/hallucination
Content-Type: application/json

{
  "request_id": "uuid",
  "content": "string",
  "content_type": "string",
  "reference_materials": ["string"],
  "context": {}
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "is_hallucination": false,
  "hallucination_probability": 0.15,
  "detected_issues": [],
  "grounded_facts": [],
  "ungrounded_claims": [],
  "confidence_score": 0.85,
  "metadata": {
    "detection_details": {
      "factual_consistency": {...},
      "logical_coherence": {...},
      "contextual_appropriateness": {...}
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Monitoring Endpoints

```bash
# Get validation metrics
GET /validators/metrics

# Get available validators
GET /validators/available
```

## 🔧 Configuration

### Environment Variables
```bash
# Service Configuration
ENABLE_GRPC_SERVER=false
ENABLE_RABBITMQ_CONSUMER=false
GRPC_PORT=50073

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
docker build -t hallucination-guard-service:latest .
```

### Run Container
```bash
docker run -d \
  --name hallucination-guard-service \
  -p 8024:8024 \
  -e ENABLE_GRPC_SERVER=false \
  -e ENABLE_RABBITMQ_CONSUMER=false \
  hallucination-guard-service:latest
```

### Docker Compose
```yaml
services:
  hallucination-guard-service:
    build: ./services/hallucination-guard-service
    ports:
      - "8024:8024"
    environment:
      - ENABLE_GRPC_SERVER=false
      - ENABLE_RABBITMQ_CONSUMER=false
    depends_on:
      - postgres
      - qdrant
```

## 🧪 Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8024 --reload
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

```
hallucination-guard-service/
├── app/
│   └── main.py              # FastAPI application with validators
├── tests/                   # Test files
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Validator Architecture

Each validator follows a consistent architecture:

```
Validator Class
├── __init__()              # Initialize with databases and frameworks
├── validate()             # Main validation method
├── _check_*() methods     # Specific validation checks
├── _calculate_*() methods # Score calculations
└── _load_*() methods      # Database/framework loading
```

## 🔄 Integration with Other Services

The Hallucination Guard Service integrates with:
- **Generation Service**: Validate AI-generated content before delivery
- **AI Agents Service**: Validate agent outputs and recommendations
- **Audit Service**: Log validation results for compliance
- **Educational Ontology Service**: Access curriculum and competency data
- **Knowledge Graph Service**: Access educational knowledge structures

## 📈 Performance Considerations

- **Validation Time**: Target < 1 second per validation
- **Detection Time**: Target < 2 seconds per hallucination check
- **Concurrent Validations**: Support multiple parallel validations
- **Memory Usage**: Efficient caching of curriculum standards
- **Scalability**: Horizontal scaling capability

## 🔐 Security

- **Input Validation**: All inputs validated using Pydantic models
- **Result Confidentiality**: Validation results protected
- **Audit Trail**: All validations logged for compliance
- **Rate Limiting**: Configurable rate limiting (via Gateway)
- **Secure Context**: Secure handling of sensitive educational content

## 🌐 Language Support

- Primary language: Indonesian (Bahasa Indonesia)
- Secondary language: English
- Curriculum alignment: Kurikulum Merdeka (Indonesian National Curriculum)
- Multi-language validation support for content in different languages

## 📝 Usage Examples

### Example 1: Validate Curriculum Content
```python
import requests

response = requests.post(
    "http://localhost:8024/validator/curriculum",
    json={
        "content": "Students will learn about photosynthesis...",
        "phase": "C",
        "grade": "VII",
        "subject": "Science",
        "expected_outcomes": [
            "Understand photosynthesis process",
            "Identify components needed"
        ]
    }
)

validation_result = response.json()
print(validation_result)
```

### Example 2: Detect Hallucinations
```python
import requests

response = requests.post(
    "http://localhost:8024/detector/hallucination",
    json={
        "content": "Photosynthesis occurs in the mitochondria...",
        "content_type": "science_explanation",
        "reference_materials": [
            "Photosynthesis occurs in chloroplasts",
            "Mitochondria are for cellular respiration"
        ]
    }
)

detection_result = response.json()
if detection_result["is_hallucination"]:
    print("Hallucination detected!")
    print(f"Probability: {detection_result['hallucination_probability']}")
```

### Example 3: Validate Retrieval Grounding
```python
import requests

response = requests.post(
    "http://localhost:8024/validator/retrieval-grounding",
    json={
        "generated_answer": "Photosynthesis converts light energy to chemical energy...",
        "retrieved_context": [
            "Photosynthesis is the process by which plants convert light energy",
            "Chloroplasts are the organelles where photosynthesis occurs"
        ],
        "query": "What is photosynthesis?"
    }
)

grounding_result = response.json()
print(f"Grounding score: {grounding_result['confidence_score']}")
print(f"Is valid: {grounding_result['is_valid']}")
```

## 🎓 Educational Context

### Curriculum Frameworks
- **Kurikulum Merdeka**: Indonesian national curriculum
- **Phase System**: Fases A-D with specific developmental focuses
- **Competency Frameworks**: Literasi, Numerasi, Karakter (Lifelong Learning Characters)

### Pedagogy Types
- **Inquiry-based**: Exploration, investigation, reflection
- **Differentiated**: Tiered content, flexible grouping
- **Project-based**: Authentic problems, collaboration
- **Direct Instruction**: Explicit instruction, guided practice

### Quality Dimensions
- **Fairness**: Bias detection, cultural appropriateness
- **Reliability**: Consistency, internal coherence
- **Validity**: Content, construct, criterion validity
- **Alignment**: Objectives, curriculum, cognitive alignment

## 🛠️ Troubleshooting

### Common Issues

**Issue**: Validation fails unexpectedly
- **Solution**: Check input format, ensure required fields are present

**Issue**: High false positive rate in hallucination detection
- **Solution**: Adjust similarity thresholds, improve reference materials

**Issue**: Slow validation performance
- **Solution**: Enable caching, optimize database queries, scale horizontally

**Issue**: Curriculum alignment errors
- **Solution**: Update curriculum standards database, check phase/grade mapping

## 📞 Support

For issues, questions, or contributions, please refer to the main project documentation.

## 📄 License

This service is part of the SIM Sekolah AI Platform project.

---

**Service Version**: 1.0.0  
**Implementation Phase**: Fase 8.1 - Advanced AI Capabilities (Hallucination Guard)  
**Last Updated**: 2026-05-27
