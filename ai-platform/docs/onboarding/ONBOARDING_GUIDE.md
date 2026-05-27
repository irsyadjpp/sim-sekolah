# Onboarding Guide

## Enterprise Educational AI Platform

---

# Welcome to the AI Platform Team!

This guide will help you get started with the Enterprise Educational AI Platform.

---

# Prerequisites

## Required Skills
- Python 3.11+
- Docker and Docker Compose
- Kubernetes (optional)
- PostgreSQL
- Vector databases (Qdrant)
- gRPC
- Machine Learning concepts

## Required Tools
- Git
- VS Code or PyCharm
- Docker Desktop
- kubectl (if using Kubernetes)
- Postman or similar API testing tool

---

# Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/upt-sdi-bonerate-no-85-kepulauan/sim-sekolah-ai-platform.git
cd sim-sekolah-ai-platform
```

## 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Required environment variables:
```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_platform
DB_USER=postgres
DB_PASSWORD=your_password

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Object Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Cache
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 4. Start Infrastructure

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or start specific services
docker-compose up -d postgres qdrant minio rabbitmq redis
```

## 5. Initialize Database

```bash
# Run migrations
python scripts/migrations/run_migrations.py

# Load fixtures
python scripts/fixtures/load_fixtures.py
```

## 6. Start Services

```bash
# Start all services
python scripts/start_all_services.py

# Or start individual services
python services/gateway-service/app/main.py
python services/parser-service/app/main.py
python services/vision-service/app/main.py
```

---

# Architecture Overview

## System Components

### Core Services
- **Gateway Service** (Port 8002): API gateway and routing
- **Parser Service** (Port 8010): Document parsing
- **Vision Service** (Port 8011): OCR and image processing
- **Semantic Chunk Service** (Port 8012): Semantic chunking
- **Metadata Service** (Port 8013): Metadata enrichment
- **Embedding Service** (Port 8014): Embedding generation
- **Retrieval Service** (Port 8003): Vector search
- **Reranking Service** (Port 8015): Result reranking
- **Generation Service** (Port 8004): AI generation
- **Moderation Service** (Port 8016): Content moderation
- **Orchestration Service** (Port 8017): Workflow orchestration

### Educational Intelligence Services
- **Adaptive Learning Engine** (Port 8018): Adaptive learning
- **Assessment Engine** (Port 8019): Assessment generation
- **Curriculum Engine** (Port 8020): Curriculum alignment
- **Learning Graph Engine** (Port 8021): Knowledge graph
- **Learning Progression Engine** (Port 8022): Progress tracking
- **Pedagogy Engine** (Port 8023): Pedagogy analysis
- **Recommendation Engine** (Port 8024): Personalized recommendations

### AI Agents Services
- **AI Agents Service** (Port 8025): AI agent orchestration
- **Advanced Enhancement Service** (Port 8026): Advanced features
- **Educational Observability Service** (Port 8027): Learning analytics
- **Hallucination Guard Service** (Port 8028): AI validation

## Data Flow

```
Document → Parser → Vision → Semantic Chunk → Metadata → Embedding → Retrieval → Reranking → Generation → Moderation → Response
```

---

# Development Workflow

## 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## 2. Make Changes

- Edit code in appropriate service directory
- Follow coding standards (see docs/engineering/CODING_STANDARD.md)
- Add tests for new functionality
- Update documentation

## 3. Test Locally

```bash
# Run unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run E2E tests
pytest tests/e2e/ -v
```

## 4. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

## 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
# Create PR on GitHub
```

---

# Common Tasks

## Adding a New Service

1. Create service directory in `services/`
2. Add `app/main.py` with FastAPI/gRPC setup
3. Add Dockerfile in service directory
4. Add service to `docker-compose.yml`
5. Add service to Kubernetes manifests
6. Add tests in `tests/`
7. Update documentation

## Adding a New Endpoint

1. Add endpoint in service's `main.py`
2. Add request/response models in `shared/schemas/`
3. Add tests in `tests/`
4. Update API documentation
5. Test endpoint locally

## Adding a New Model

1. Add model file in `models/`
2. Add model card documentation
3. Add model to model registry
4. Test model inference
5. Update documentation

---

# Testing

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only
pytest tests/e2e/ -v

# With coverage
pytest tests/ -v --cov=. --cov-report=html
```

## Test Coverage

- Aim for >80% code coverage
- Write tests for critical paths
- Test edge cases
- Test error handling

---

# Debugging

## Local Debugging

```bash
# Run service in debug mode
python -m pdb services/gateway-service/app/main.py

# Or use IDE debugger
# Set breakpoints in VS Code or PyCharm
```

## Remote Debugging

```bash
# Enable remote debugging in service
# Use debugpy for Python
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

## Viewing Logs

```bash
# Docker logs
docker logs <service-name> -f

# Kubernetes logs
kubectl logs <pod-name> -f

# Application logs
tail -f /var/log/ai-platform/*.log
```

---

# Monitoring

## Viewing Metrics

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
- **Service metrics**: http://localhost:<port>/metrics

## Viewing Logs

- **Loki**: http://localhost:3100
- **Grafana Logs**: http://localhost:3000/explore

## Health Checks

```bash
# Gateway health
curl http://localhost:8002/health

# Parser health
curl http://localhost:8010/health

# All services
for port in 8002 8010 8011 8012 8013 8014 8003 8015 8004 8016 8017; do
  curl http://localhost:$port/health
done
```

---

# Documentation

## Key Documentation Files

- `README.md`: Project overview
- `ARCHITECTURE.md`: System architecture
- `docs/API/README.md`: API documentation
- `docs/architecture/`: Architecture docs
- `docs/deployment/`: Deployment guides
- `docs/runbooks/`: Operational runbooks

## Updating Documentation

- Keep documentation up to date
- Add examples for new features
- Document API changes
- Update diagrams when architecture changes

---

# Best Practices

## Code Quality

- Follow PEP 8 style guide
- Use type hints
- Write docstrings
- Add comments for complex logic
- Keep functions small and focused

## Security

- Never commit secrets
- Use environment variables for sensitive data
- Validate all inputs
- Use parameterized queries
- Follow security guidelines

## Performance

- Use caching where appropriate
- Optimize database queries
- Use connection pooling
- Monitor resource usage
- Profile code regularly

---

# Getting Help

## Team Contacts

- **Engineering Lead**: engineering-lead@example.com
- **Platform Team**: platform-team@example.com
- **DevOps Team**: devops-team@example.com

## Resources

- **Slack**: #ai-platform channel
- **Confluence**: AI Platform documentation
- **Jira**: Project tracking
- **GitHub**: Code repository

## Troubleshooting

- Check runbooks in `docs/runbooks/`
- Search existing issues on GitHub
- Ask in Slack channel
- Create a support ticket

---

# Next Steps

1. Complete the setup steps above
2. Read the architecture documentation
3. Explore the codebase
4. Run the tests
5. Pick a small task to work on
6. Ask questions if you get stuck

---

# Welcome Aboard!

We're excited to have you on the team. Don't hesitate to reach out if you need help!
