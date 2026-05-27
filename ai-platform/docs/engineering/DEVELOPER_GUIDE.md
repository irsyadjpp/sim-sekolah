# Developer Guide

## Enterprise Educational AI Platform

---

# Development Environment Setup

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- PostgreSQL client
- Redis client
- kubectl (optional, for Kubernetes)

## Initial Setup

```bash
# Clone repository
git clone https://github.com/upt-sdi-bonerate-no-85-kepulauan/sim-sekolah-ai-platform.git
cd sim-sekolah-ai-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Start infrastructure
docker-compose up -d postgres qdrant minio rabbitmq redis

# Run migrations
python scripts/migrations/run_migrations.py

# Load fixtures
python scripts/fixtures/load_fixtures.py
```

---

# Project Structure

```
ai-platform/
├── services/              # Microservices
│   ├── gateway-service/
│   ├── parser-service/
│   ├── vision-service/
│   └── ...
├── shared/               # Shared code
│   ├── logging/
│   ├── telemetry/
│   ├── security/
│   └── middleware/
├── storage/              # Storage abstractions
│   ├── abstractions/
│   ├── migrations/
│   └── fixtures/
├── tests/                # Tests
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── load/
│   ├── security/
│   └── performance/
├── pipelines/            # Data pipelines
├── workers/              # Background workers
├── models/               # ML models
├── knowledge/            # Knowledge base
├── proto/                # gRPC proto files
├── sdk/                  # SDKs
│   ├── go/
│   └── python/
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── infra/                # Infrastructure configs
├── k8s/                  # Kubernetes manifests
└── docker-compose.yml    # Docker Compose config
```

---

# Service Development

## Creating a New Service

### 1. Create Service Directory

```bash
mkdir -p services/new-service/app
mkdir -p services/new-service/tests
```

### 2. Create Main Application

```python
# services/new-service/app/main.py
from fastapi import FastAPI
from shared.logging.logger import get_logger
from shared.telemetry.performance import track_performance

logger = get_logger(__name__)
app = FastAPI(title="New Service")

@app.get("/health")
@track_performance("health_check")
async def health_check():
    return {"status": "healthy", "service": "new-service"}

@app.post("/process")
@track_performance("process")
async def process_request(payload: dict):
    # Your logic here
    return {"result": "processed"}
```

### 3. Create Dockerfile

```dockerfile
# services/new-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
```

### 4. Add to Docker Compose

```yaml
# docker-compose.yml
new-service:
  build: ./services/new-service
  ports:
    - "8030:8030"
  environment:
    - DB_HOST=postgres
    - DB_PORT=5432
  depends_on:
    - postgres
```

### 5. Add Tests

```python
# services/new-service/tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

# API Development

## REST API

### Adding Endpoints

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

class RequestModel(BaseModel):
    field1: str
    field2: Optional[int] = None

class ResponseModel(BaseModel):
    result: str
    status: str

@app.post("/endpoint", response_model=ResponseModel)
async def endpoint_handler(request: RequestModel):
    try:
        # Process request
        result = process_logic(request)
        return ResponseModel(result=result, status="success")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

## gRPC API

### Adding gRPC Methods

1. Define in proto file:
```protobuf
// proto/service.proto
syntax = "proto3";

package service;

service NewService {
  rpc Process (ProcessRequest) returns (ProcessResponse);
}

message ProcessRequest {
  string field1 = 1;
  int32 field2 = 2;
}

message ProcessResponse {
  string result = 1;
  string status = 2;
}
```

2. Generate Python code:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/service.proto
```

3. Implement service:
```python
import grpc
from proto.service_pb2 import ProcessRequest, ProcessResponse
from proto.service_pb2_grpc import NewServiceServicer

class NewServiceImpl(NewServiceServicer):
    def Process(self, request, context):
        # Process request
        result = process_logic(request)
        return ProcessResponse(result=result, status="success")
```

---

# Database Development

## Using Storage Abstractions

```python
from storage.abstractions.relational_db import RelationalDatabase
from storage.abstractions.vector_db import VectorDatabase
from storage.abstractions.object_storage import ObjectStorage

# Initialize databases
db = RelationalDatabase()
vector_db = VectorDatabase()
object_storage = ObjectStorage()

# Use relational database
with db.get_session() as session:
    result = session.execute("SELECT * FROM documents")
    documents = result.fetchall()

# Use vector database
results = vector_db.search(
    collection="documents",
    query_vector=embedding,
    limit=10
)

# Use object storage
object_storage.upload(
    bucket="documents",
    key="document.pdf",
    data=file_data
)
```

## Running Migrations

```bash
# Create new migration
python scripts/migrations/create_migration.py --name "add_new_table"

# Run migrations
python scripts/migrations/run_migrations.py

# Rollback migration
python scripts/migrations/rollback_migration.py --version <version>
```

---

# Testing

## Unit Tests

```python
import pytest
from unittest.mock import Mock, patch

def test_function():
    # Arrange
    input_data = {"key": "value"}
    
    # Act
    result = process_function(input_data)
    
    # Assert
    assert result["status"] == "success"

def test_with_mock():
    with patch('module.external_function') as mock_func:
        mock_func.return_value = "mocked"
        result = function_using_external()
        assert result == "mocked"
```

## Integration Tests

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_integration_flow():
    # Step 1: Upload document
    response = client.post("/upload", files={"file": ("test.pdf", b"content")})
    assert response.status_code == 200
    document_id = response.json()["id"]
    
    # Step 2: Process document
    response = client.post(f"/process/{document_id}")
    assert response.status_code == 200
    
    # Step 3: Search
    response = client.post("/search", json={"query": "test"})
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# With coverage
pytest tests/ -v --cov=. --cov-report=html

# Specific test file
pytest tests/unit/test_main.py -v

# Specific test function
pytest tests/unit/test_main.py::test_function -v
```

---

# Performance Optimization

## Using Performance Monitor

```python
from shared.telemetry.performance import PerformanceMonitor, track_performance

monitor = PerformanceMonitor()

# Using decorator
@track_performance("operation_name")
def my_function():
    # Your code here
    pass

# Using context manager
with PerformanceContext("operation_name", monitor):
    # Your code here
    pass

# Manual tracking
start_time = time.time()
# Your code here
duration = time.time() - start_time
monitor.record_metric("operation_name", duration)
```

## Caching

```python
from functools import lru_cache
import redis

# Simple caching
@lru_cache(maxsize=100)
def expensive_function(param):
    # Expensive computation
    return result

# Redis caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_with_cache(key):
    cached = redis_client.get(key)
    if cached:
        return cached
    
    result = expensive_operation()
    redis_client.set(key, result, ex=3600)
    return result
```

---

# Debugging

## Local Debugging

```bash
# Using pdb
python -m pdb services/gateway-service/app/main.py

# Using IDE debugger
# Set breakpoints in VS Code or PyCharm
```

## Remote Debugging

```python
import debugpy

# Enable remote debugging
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()

# Your code here
```

## Logging

```python
from shared.logging.logger import get_logger

logger = get_logger(__name__)

logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
logger.debug("Debug message")
```

---

# Deployment

## Building Docker Images

```bash
# Build specific service
docker build -t new-service:latest ./services/new-service

# Build all services
docker-compose build

# Build with no cache
docker-compose build --no-cache
```

## Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f k8s/new-service-deployment.yaml

# Check status
kubectl get pods -l app=new-service

# View logs
kubectl logs -l app=new-service -f

# Scale deployment
kubectl scale deployment new-service --replicas=3
```

---

# Code Quality

## Linting

```bash
# Flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Black
black .

# isort
isort .

# mypy
mypy .
```

## Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

---

# Best Practices

## Code Organization

- Keep functions small and focused
- Use type hints
- Write docstrings
- Follow PEP 8
- Use meaningful variable names

## Error Handling

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

## Resource Management

```python
# Use context managers
with open("file.txt") as f:
    content = f.read()

# Clean up resources
try:
    resource = acquire_resource()
    # Use resource
finally:
    release_resource(resource)
```

---

# Contributing

## Pull Request Process

1. Create feature branch
2. Make changes
3. Add tests
4. Run tests locally
5. Update documentation
6. Create pull request
7. Address review feedback
8. Merge after approval

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance considered
- [ ] Security reviewed

---

# Resources

## Internal Documentation

- Architecture: `docs/architecture/`
- API Docs: `docs/API/`
- Runbooks: `docs/runbooks/`
- Deployment: `docs/deployment/`

## External Resources

- FastAPI: https://fastapi.tiangolo.com/
- gRPC: https://grpc.io/
- PostgreSQL: https://www.postgresql.org/docs/
- Qdrant: https://qdrant.tech/documentation/

---

# Getting Help

## Team Contacts

- Engineering Lead: engineering-lead@example.com
- Platform Team: platform-team@example.com
- DevOps Team: devops-team@example.com

## Communication Channels

- Slack: #ai-platform-dev
- Email: dev@example.com
- Jira: Project tracking

---

# FAQ

### Q: How do I add a new dependency?
A: Add to requirements.txt and run `pip install -r requirements.txt`

### Q: How do I run tests?
A: Run `pytest tests/ -v`

### Q: How do I debug a service?
A: Use `python -m pdb` or IDE debugger

### Q: How do I add a new database table?
A: Create migration using `python scripts/migrations/create_migration.py`

---

# Appendix

## Common Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Run tests
pytest tests/ -v

# Build services
docker-compose build

# Run migrations
python scripts/migrations/run_migrations.py

# Load fixtures
python scripts/fixtures/load_fixtures.py
```

## Environment Variables

See `.env.example` for all available environment variables.
