# Integration Tests

This directory contains integration tests for service-to-service contract testing.

## Overview

Integration tests verify that different services work together correctly by testing their contracts and interactions. These tests ensure that:

- gRPC service contracts are maintained
- API responses match expected schemas
- Service-to-service communication works correctly
- Data flows correctly through the system

## Structure

```
tests/integration/
├── contracts/       # Contract definitions and validation
│   ├── grpc/       # gRPC contract tests
│   └── http/       # HTTP API contract tests
├── services/       # Service integration tests
│   ├── document/   # Document service integration tests
│   ├── embedding/  # Embedding service integration tests
│   ├── retrieval/  # Retrieval service integration tests
│   └── generation/ # Generation service integration tests
├── helpers/        # Test helpers and utilities
│   ├── clients.py  # Service client helpers
│   ├── fixtures.py # Test fixtures
│   └── assertions.py # Custom assertions
├── conftest.py     # Pytest configuration
└── README.md      # This file
```

## Running Tests

```bash
# Run all integration tests
pytest tests/integration/

# Run specific test suite
pytest tests/integration/services/document/
pytest tests/integration/contracts/grpc/

# Run with coverage
pytest tests/integration/ --cov=ai_platform --cov-report=html

# Run against specific environment
pytest tests/integration/ --env=staging
```

## Test Configuration

Configure test environments using environment variables or `.env.test`:

```bash
# Service endpoints
DOCUMENT_SERVICE_HOST=localhost
DOCUMENT_SERVICE_PORT=50051
EMBEDDING_SERVICE_HOST=localhost
EMBEDDING_SERVICE_PORT=50052

# Storage backends
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Test settings
TEST_TIMEOUT=30
TEST_FIXTURES_PATH=./tests/fixtures
```

## Contract Testing

### gRPC Contracts

Test gRPC service contracts using the generated proto stubs:

```python
async def test_document_service_contract():
    client = DocumentServiceClient(host="localhost", port=50051)
    response = await client.UploadDocument(
        request=UploadDocumentRequest(
            title="Test Document",
            content="Test content"
        )
    )
    assert response.document_id is not None
    assert response.status == "uploaded"
```

### HTTP Contracts

Test HTTP API contracts using schema validation:

```python
async def test_document_api_contract():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/documents",
            json={"title": "Test", "content": "Content"}
        )
        assert response.status_code == 200
        assert validate_schema(response.json(), document_response_schema)
```

## Service Integration Tests

### Document Service Integration

```python
async def test_document_upload_flow():
    # Upload document
    doc_id = await upload_document("test.pdf")
    
    # Verify document was stored
    doc = await get_document(doc_id)
    assert doc.status == "processed"
    
    # Verify embedding was created
    embeddings = await get_document_embeddings(doc_id)
    assert len(embeddings) > 0
```

### End-to-End Workflow Tests

```python
async def test_rag_workflow():
    # Ingest document
    doc_id = await ingest_document("test.pdf")
    
    # Wait for processing
    await wait_for_document_processing(doc_id)
    
    # Query the system
    response = await query_system("What is the main topic?")
    
    # Verify response
    assert response.answer is not None
    assert len(response.sources) > 0
```

## Test Helpers

### Service Clients

```python
from helpers.clients import DocumentServiceClient, EmbeddingServiceClient

doc_client = DocumentServiceClient()
emb_client = EmbeddingServiceClient()
```

### Test Fixtures

```python
from helpers.fixtures import (
    create_test_document,
    create_test_user,
    cleanup_test_data
)
```

### Custom Assertions

```python
from helpers.assertions import (
    assert_document_processed,
    assert_embedding_created,
    assert_response_schema_valid
)
```

## Best Practices

1. **Isolation**: Each test should be independent and clean up after itself
2. **Deterministic**: Tests should produce consistent results
3. **Fast**: Integration tests should complete quickly
4. **Clear failure messages**: Tests should provide clear error messages
5. **Mock external dependencies**: Use mocks for external services
6. **Use test databases**: Separate test databases from production
7. **Parallel execution**: Tests should be able to run in parallel

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Integration Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start services
        run: docker-compose up -d
      - name: Run integration tests
        run: pytest tests/integration/ -v
      - name: Cleanup
        run: docker-compose down
```

## Troubleshooting

### Common Issues

**Tests fail with connection errors:**
- Ensure all services are running
- Check service endpoints in configuration
- Verify network connectivity

**Tests timeout:**
- Increase timeout in configuration
- Check service performance
- Verify test data size is reasonable

**Inconsistent test results:**
- Ensure proper cleanup between tests
- Check for shared state issues
- Verify test isolation

### Debug Mode

Run tests with debug output:

```bash
pytest tests/integration/ -v -s --log-cli-level=DEBUG
```

## Adding New Tests

1. Create test file in appropriate directory
2. Inherit from base test class
3. Use test helpers and fixtures
4. Add cleanup logic
5. Update this README with test documentation