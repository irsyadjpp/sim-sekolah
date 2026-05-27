# AI Platform Pipelines

This package contains Prefect-based data processing and ML workflows for the AI Platform.

## Orchestrator: Prefect

We chose Prefect as our workflow orchestrator because:
- Python-native (fits our tech stack)
- Modern and actively maintained
- Great support for both batch and streaming workflows
- Built-in observability and error handling
- Excellent for ML/AI workflows
- Easy integration with our existing services

## Installation

```bash
pip install -e .
```

## Configuration

Configuration is managed through:
- Environment variables (see `.env.example`)
- `prefect.toml` file for Prefect-specific settings
- `config.py` for pipeline configuration

## Available Pipelines

### 1. Ingestion Pipeline (`pipelines/ingestion/`)

**Flow**: Document → Parsed → Chunked → Embedded → Indexed

The ingestion pipeline processes uploaded documents through the complete workflow:
1. **Validate Document** - Check file type, size, and accessibility
2. **Parse Document** - Extract text, tables, and images using Parser Service
3. **Chunk Document** - Split into semantic units using Semantic Chunk Service
4. **Embed Chunks** - Generate vector embeddings using Embedding Service
5. **Index Vectors** - Store in Qdrant vector database via Retrieval Service
6. **Update Status** - Mark document as completed in database
7. **Emit Events** - Publish completion events to message queue

**Usage**:
```python
from pipelines.ingestion.dag import document_ingestion_flow

# Single document
result = await document_ingestion_flow(
    document_id="doc_123",
    file_path="/path/to/document.pdf",
    user_id="user_456"
)

# Batch processing
from pipelines.ingestion.dag import batch_document_ingestion_flow

documents = [
    {"document_id": "doc_1", "file_path": "/path/doc1.pdf"},
    {"document_id": "doc_2", "file_path": "/path/doc2.pdf"},
]

result = await batch_document_ingestion_flow(documents, max_concurrent=4)
```

### 2. Enrichment Pipeline (`pipelines/enrichment/`)

**Flow**: Document → Metadata Tagging (difficulty, taxonomy, competency)

The enrichment pipeline adds educational metadata to documents:
- Difficulty level assessment
- Curriculum taxonomy mapping
- Competency alignment
- Learning objective tagging

### 3. Indexing Pipeline (`pipelines/indexing/`)

**Flow**: Chunk → Vector Store + Graph Edges

The indexing pipeline manages knowledge graph construction:
- Vector similarity indexing
- Knowledge graph edge creation
- Cross-document relationship mapping

### 4. Generation Pipeline (`pipelines/generation/`)

**Flow**: Retrieval → Context Building → LLM Generation → Guardrails

The generation pipeline powers AI responses:
- Retrieve relevant context
- Build prompt context
- Generate LLM responses
- Apply moderation guardrails

## Running Pipelines

### Development Mode

```bash
# Start Prefect UI
prefect ui start

# Run a flow
python -m pipelines.ingestion.dag

# Or use Prefect CLI
prefect run document_ingestion_flow
```

### Production Mode

```bash
# Deploy to Prefect Cloud/Server
prefect deploy document_ingestion_flow

# Run via Prefect API
curl -X POST "http://prefect-server:4200/api/flows/run" \
  -H "Authorization: Bearer $PREFECT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"deployment_id": "..."}'
```

## Monitoring

All pipelines include:
- **Automatic retries** with exponential backoff
- **Timeout handling** for long-running tasks
- **Error tracking** with detailed logging
- **Status updates** in database
- **Event emission** for real-time monitoring

Monitor pipeline runs via:
- Prefect UI: http://localhost:4200
- Logs: Configured in `prefect.toml`
- Metrics: Prometheus integration available

## Testing

```bash
# Run pipeline tests
pytest tests/pipelines/

# Run specific pipeline test
pytest tests/pipelines/test_ingestion.py
```

## Workers

Background workers execute pipeline tasks:
- **Document Workers** - Handle file processing
- **Embedding Workers** - Generate vector embeddings
- **Enrichment Workers** - Apply metadata enrichment
- **Indexing Workers** - Manage vector and graph operations
- **Cleanup Workers** - Handle data cleanup and maintenance

See `workers/` directory for worker implementations.

## Environment Variables

Required environment variables:
- `POSTGRES_URL` - Database connection string
- `REDIS_URL` - Redis connection string
- `QDRANT_URL` - Qdrant vector database URL
- `RABBITMQ_URL` - RabbitMQ connection string
- `MINIO_ENDPOINT` - MinIO object storage endpoint
- `MINIO_ACCESS_KEY` - MinIO access key
- `MINIO_SECRET_KEY` - MinIO secret key

Service-specific variables:
- `PARSER_SERVICE_URL` - Parser service URL
- `CHUNK_SERVICE_URL` - Semantic chunk service URL
- `EMBEDDING_SERVICE_URL` - Embedding service URL
- `RETRIEVAL_SERVICE_URL` - Retrieval service URL
- `GENERATION_SERVICE_URL` - Generation service URL

## Best Practices

1. **Idempotency**: Design tasks to be safely retryable
2. **Atomic Operations**: Use database transactions where needed
3. **Error Handling**: Always handle exceptions gracefully
4. **Logging**: Log at appropriate levels for debugging
5. **Timeouts**: Set reasonable timeouts for external calls
6. **Batching**: Process items in batches for efficiency
7. **Monitoring**: Emit events for real-time tracking

## Troubleshooting

### Pipeline Stuck
- Check Prefect UI for task status
- Review logs for error messages
- Verify service availability
- Check resource constraints

### Memory Issues
- Reduce batch sizes
- Process documents sequentially
- Increase worker memory limits

### Service Unavailable
- Check service health endpoints
- Verify network connectivity
- Review service logs
- Check circuit breaker status

## Additional Resources

- [Prefect Documentation](https://docs.prefect.io/)
- [Prefect UI Guide](https://docs.prefect.io/latest/ui/)
- [Flow Concepts](https://docs.prefect.io/latest/concepts/flows/)