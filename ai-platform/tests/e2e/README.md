# End-to-End Tests

This directory contains end-to-end tests for the AI Platform, testing complete user workflows across multiple services.

## Overview

End-to-end (E2E) tests verify that the entire system works together by simulating real user scenarios. These tests cover:

- **RAG Workflows**: Document ingestion → retrieval → generation
- **Generation Flows**: Query processing → context assembly → LLM generation → guard rails
- **Multi-step Workflows**: Complex scenarios involving multiple services
- **User Journeys**: Complete user stories from start to finish

## Structure

```
tests/e2e/
├── workflows/       # Complete workflow tests
│   ├── rag/        # RAG workflow tests
│   ├── generation/ # Generation workflow tests
│   └── ingestion/  # Document ingestion workflow tests
├── scenarios/      # User scenario tests
│   ├── student/    # Student user scenarios
│   ├── teacher/    # Teacher user scenarios
│   └── admin/      # Admin user scenarios
├── helpers/        # E2E test helpers
│   ├── workflows.py # Workflow orchestration
│   └── assertions.py # E2E-specific assertions
├── conftest.py     # Pytest configuration
└── README.md      # This file
```

## Running Tests

```bash
# Run all E2E tests
pytest tests/e2e/ -v

# Run specific workflow
pytest tests/e2e/workflows/rag/
pytest tests/e2e/scenarios/student/

# Run with timeout
pytest tests/e2e/ --timeout=300

# Run with detailed output
pytest tests/e2e/ -v -s
```

## Test Workflows

### RAG Workflow

Tests the complete Retrieval-Augmented Generation pipeline:

1. Document ingestion and processing
2. Vector embedding creation
3. Knowledge graph population
4. Query processing
5. Context retrieval
6. Response generation
7. Guard rail validation

```python
async def test_complete_rag_workflow():
    # 1. Ingest document
    document_id = await ingest_document("textbook_chapter.pdf")
    
    # 2. Wait for processing
    await wait_for_document_ready(document_id)
    
    # 3. Query the system
    response = await query_system("Explain photosynthesis")
    
    # 4. Verify response quality
    assert response.answer is not None
    assert len(response.sources) > 0
    assert response.guard_passed is True
```

### Generation Workflow

Tests the generation pipeline with guard rails:

1. Query validation
2. Context assembly
3. LLM generation
4. Content filtering
5. Quality checks

```python
async def test_generation_with_guards():
    # Generate response with guard rails
    response = await generate_with_guards(
        query="What is the capital of France?",
        context=retrieved_context
    )
    
    # Verify guard checks
    assert response.guard_checks["safety"] == "passed"
    assert response.guard_checks["quality"] == "passed"
    assert response.guard_checks["accuracy"] = "passed"
```

### Ingestion Workflow

Tests the document ingestion pipeline:

1. Document upload
2. Content extraction
3. Text chunking
4. Embedding generation
5. Vector storage
6. Graph indexing

```python
async def test_document_ingestion_workflow():
    # Upload and process document
    result = await ingest_document_workflow(
        file_path="sample.pdf",
        metadata={"subject": "biology", "grade": "10"}
    )
    
    # Verify all processing steps completed
    assert result.upload_status == "success"
    assert result.chunking_status == "success"
    assert result.embedding_status == "success"
    assert result.indexing_status == "success"
```

## User Scenarios

### Student Scenario

Tests typical student interactions:

```python
async def test_student_homework_help():
    # Student asks for help with homework
    conversation = await start_conversation(user_id="student-123")
    
    response = await ask_question(
        conversation_id=conversation.id,
        question="How do I solve quadratic equations?"
    )
    
    # Verify helpful response
    assert response.clarity_score > 0.8
    assert response.educational_level == "appropriate"
```

### Teacher Scenario

Tests teacher-specific features:

```python
async def test_teacher_content_creation():
    # Teacher creates educational content
    content = await create_educational_content(
        teacher_id="teacher-456",
        topic="Newton Laws",
        grade_level="11"
    )
    
    # Verify content quality
    assert content.quality_score > 0.85
    assert content.standards_aligned is True
```

## Configuration

Configure E2E tests using environment variables:

```bash
# Service endpoints
DOCUMENT_SERVICE_URL=http://localhost:50051
EMBEDDING_SERVICE_URL=http://localhost:50052
RETRIEVAL_SERVICE_URL=http://localhost:50053
GENERATION_SERVICE_URL=http://localhost:50054
GUARD_SERVICE_URL=http://localhost:50055

# Storage
POSTGRES_URL=postgresql://localhost:5432/ai_platform_test
QDRANT_URL=http://localhost:6333
NEO4J_URL=bolt://localhost:7687

# Test settings
E2E_TIMEOUT=300
E2E_RETRY_COUNT=3
E2E_CLEANUP_AFTER_TEST=true
```

## Best Practices

1. **Test complete workflows**: Don't skip steps in the middle
2. **Use realistic data**: Use test data that resembles production data
3. **Verify end states**: Check the final state, not just intermediate steps
4. **Clean up after tests**: Remove test data to avoid interference
5. **Use appropriate timeouts**: E2E tests take longer than unit tests
6. **Test error scenarios**: Include failure cases and edge cases
7. **Monitor performance**: Track test execution time

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start all services
        run: docker-compose up -d
      - name: Wait for services
        run: ./scripts/wait-for-services.sh
      - name: Run E2E tests
        run: pytest tests/e2e/ --timeout=600
      - name: Cleanup
        run: docker-compose down -v
```

## Troubleshooting

### Common Issues

**Tests timeout:**
- Increase E2E_TIMEOUT value
- Check service performance
- Verify test data size is reasonable

**Tests fail intermittently:**
- Add retry logic for transient failures
- Check for race conditions
- Ensure proper cleanup between tests

**Services not ready:**
- Add service health checks
- Increase wait times before tests
- Verify service startup order

### Debug Mode

Run tests with debug output:

```bash
pytest tests/e2e/ -v -s --log-cli-level=DEBUG
```

## Adding New E2E Tests

1. Create test file in appropriate directory
2. Define complete workflow scenario
3. Use workflow helpers for orchestration
4. Add comprehensive assertions
5. Include cleanup logic
6. Update this README

## Performance Benchmarks

Track E2E test performance to detect regressions:

- Document ingestion: < 30 seconds
- RAG query response: < 5 seconds
- Complete student session: < 60 seconds
- Multi-document analysis: < 120 seconds