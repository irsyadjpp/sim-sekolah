# Generation Pipeline

This module implements the complete RAG (Retrieval-Augmented Generation) pipeline for AI response generation with guard rail validation.

## Pipeline Stages

### 1. Document Retrieval (`retrieve_documents`)
- Vector similarity search using Qdrant
- Configurable retrieval limits and score thresholds
- Metadata-based filtering support

### 2. Context Assembly (`assemble_context`)
- Formats retrieved documents into context string
- Respects maximum context length limits
- Optional metadata inclusion

### 3. LLM Generation (`generate_response`)
- Calls LLM service (placeholder for integration)
- Configurable model, temperature, and max tokens
- Tracks token usage and generation metadata

### 4. Guard Rail Validation (`guard_rails`)
- **Safety Check**: Detects harmful content
- **Quality Check**: Validates response length and relevance
- **Accuracy Check**: Ensures response is contextually accurate
- **Policy Check**: Enforces response policies

## Usage

### Single Query Generation

```python
from pipelines.generation import generation_pipeline

result = await generation_pipeline(
    query="What is photosynthesis?",
    collection_name="document_embeddings",
    retrieval_limit=5,
    model_name="llama-3-8b",
    temperature=0.7,
    max_tokens=500
)

print(result["pipeline_results"]["final_response"])
```

### Batch Generation

```python
from pipelines.generation import batch_generation_pipeline

queries = [
    "What is photosynthesis?",
    "How does the respiratory system work?",
    "Explain Newton's laws of motion"
]

result = await batch_generation_pipeline(
    queries=queries,
    collection_name="document_embeddings",
    batch_size=3
)

print(f"Generated {result['successful_generations']} responses")
```

### Individual Stage Execution

```python
from pipelines.generation import retrieve_documents, assemble_context

# Retrieve documents
docs = await retrieve_documents(
    query="What is photosynthesis?",
    limit=5
)

# Assemble context
context = await assemble_context(
    retrieved_docs=docs,
    max_context_length=4000
)
```

## Configuration

### Environment Variables

- `QDRANT_HOST`: Qdrant host address
- `QDRANT_PORT`: Qdrant port
- `QDRANT_API_KEY`: Qdrant API key (optional)

### Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `collection_name` | `"document_embeddings"` | Vector collection name |
| `retrieval_limit` | `5` | Number of documents to retrieve |
| `max_context_length` | `4000` | Maximum context length in characters |
| `model_name` | `"llama-3-8b"` | LLM model name |
| `temperature` | `0.7` | Sampling temperature |
| `max_tokens` | `500` | Maximum tokens to generate |
| `skip_guards` | `False` | Skip guard rail checks |

## Guard Rail Configuration

Guard rails can be configured via the `guard_config` parameter:

```python
guard_result = await guard_rails(
    response=response,
    query=query,
    context=context,
    guard_config={
        "safety": {
            "enabled": True,
            "severity_threshold": "high"
        },
        "quality": {
            "enabled": True,
            "min_length": 20,
            "max_length": 2000
        }
    }
)
```

## Deployment

### Deploy to Prefect Server

```bash
cd pipelines/generation
prefect deploy generation_pipeline:generation_pipeline
```

### Run with Prefect CLI

```bash
prefect run -n generation_pipeline
```

### Schedule as Cron Job

```python
from prefect import deployment

@deployment(
    name="scheduled-generation",
    schedule="0 * * * *"  # Every hour
)
async def scheduled_generation():
    # Your scheduled generation logic
    pass
```

## Monitoring

All pipeline stages include:
- Structured logging with request context
- Distributed tracing with OpenTelemetry
- Performance metrics collection
- Error tracking and alerting

## Testing

Run unit tests:

```bash
pytest pipelines/generation/tests/
```

Run integration tests:

```bash
pytest pipelines/generation/tests/integration/
```

## Next Steps

- Integrate with actual LLM service (currently using placeholder)
- Connect to embedding service for query embeddings
- Implement advanced guard rail models
- Add response caching for repeated queries
- Implement streaming responses