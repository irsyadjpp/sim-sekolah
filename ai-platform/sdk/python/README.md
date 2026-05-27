# SimSekolah AI Platform Python SDK

Python SDK for the SimSekolah AI Platform, providing a clean interface for Python applications to interact with AI Platform gRPC services.

## Features

- **Type-safe gRPC clients**: Auto-generated from proto definitions
- **Async/sync support**: Both synchronous and asynchronous client implementations
- **Connection management**: Automatic connection pooling and keepalive
- **Circuit breaker**: Built-in circuit breaker pattern for resilience
- **Retry logic**: Automatic retry with configurable backoff using tenacity
- **Error handling**: Structured error types with proper error codes
- **Configuration**: Environment-based configuration with Pydantic validation
- **Health checks**: Built-in health check functionality

## Installation

### From PyPI (when published)

```bash
pip install simsekolah-ai
```

### From internal registry

```bash
pip install --index-url https://pypi.simsekolah.com/simple simsekolah-ai
```

### From source

```bash
git clone https://github.com/simsekolah/ai-platform-sdk-python
cd ai-platform-sdk-python
pip install -e .
```

### With development dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

### Synchronous Client

```python
from simsekolah_ai import AIClient, Config

# Create configuration
config = Config(
    document_service_url="localhost:50051",
    embedding_service_url="localhost:50052",
    retrieval_service_url="localhost:50053",
    generation_service_url="localhost:50054",
)

# Create client
client = AIClient(config)

# Use the client
try:
    # Upload document
    result = client.upload_document(
        title="Test Document",
        content="This is a test document",
        metadata={"author": "Test Author"}
    )
    print(f"Document uploaded: {result.document_id}")
    
    # Generate embeddings
    embeddings = client.create_embeddings(
        texts=["Hello world", "Test text"],
        model="bge-m3"
    )
    print(f"Created {len(embeddings)} embeddings")
    
finally:
    client.close()
```

### Asynchronous Client

```python
import asyncio
from simsekolah_ai import AsyncAIClient, Config

async def main():
    config = Config.from_env()  # Load from environment variables
    async with AsyncAIClient(config) as client:
        # Upload document
        result = await client.upload_document(
            title="Async Test Document",
            content="This is an async test"
        )
        print(f"Document uploaded: {result.document_id}")
        
        # Search documents
        results = await client.search(
            query="test query",
            limit=5
        )
        print(f"Found {len(results)} results")

asyncio.run(main())
```

## Configuration

Configure the SDK using environment variables:

```bash
# Service URLs
export AI_DOCUMENT_SERVICE_URL=localhost:50051
export AI_EMBEDDING_SERVICE_URL=localhost:50052
export AI_RETRIEVAL_SERVICE_URL=localhost:50053
export AI_GENERATION_SERVICE_URL=localhost:50054
export AI_GUARD_SERVICE_URL=localhost:50055

# Connection settings
export AI_MAX_CONNECTIONS=10
export AI_CONNECTION_TIMEOUT=30
export AI_KEEPALIVE_TIMEOUT=10

# Retry settings
export AI_MAX_RETRIES=3
export AI_RETRY_DELAY=1
export AI_RETRY_EXPONENTIAL_BASE=2

# Circuit breaker
export AI_CIRCUIT_BREAKER_ENABLED=true
export AI_CIRCUIT_BREAKER_THRESHOLD=5
export AI_CIRCUIT_BREAKER_TIMEOUT=30

# Authentication
export AI_API_KEY=your-api-key
export AI_JWT_TOKEN=your-jwt-token

# Debug
export AI_DEBUG=false
```

Or use Pydantic config:

```python
from simsekolah_ai import Config

config = Config(
    document_service_url="localhost:50051",
    embedding_service_url="localhost:50052",
    retrieval_service_url="localhost:50053",
    generation_service_url="localhost:50054",
    max_connections=10,
    connection_timeout=30,
    max_retries=3,
    circuit_breaker_enabled=True,
    circuit_breaker_threshold=5,
    api_key="your-api-key"
)
```

## Usage Examples

### Document Service

```python
from simsekolah_ai import AIClient, Config

config = Config.from_env()
client = AIClient(config)

# Upload document
result = client.upload_document(
    title="Introduction to AI",
    content="Artificial Intelligence is...",
    metadata={
        "author": "Dr. Smith",
        "subject": "Computer Science",
        "grade_level": "10"
    }
)

# Get document
document = client.get_document(result.document_id)

# Delete document
client.delete_document(result.document_id)
```

### Embedding Service

```python
# Create single embedding
embedding = client.create_embedding(
    text="Hello world",
    model="bge-m3"
)

# Batch create embeddings
embeddings = client.create_embeddings(
    texts=["Text 1", "Text 2", "Text 3"],
    model="bge-m3"
)

# Get embedding
existing = client.get_embedding(embedding.embedding_id)
```

### Retrieval Service

```python
# Semantic search
results = client.search(
    query="What is machine learning?",
    limit=5,
    filters={"subject": "Computer Science"}
)

# Hybrid search
results = client.hybrid_search(
    query="machine learning algorithms",
    keyword_query="algorithms",
    limit=10
)
```

### Generation Service

```python
# Simple generation
response = client.generate(
    prompt="Explain quantum computing",
    model="llama-3-8b"
)

# RAG generation
response = client.generate_with_rag(
    query="What is photosynthesis?",
    context=retrieved_documents,
    model="llama-3-8b"
)
```

## Error Handling

The SDK uses structured error types:

```python
from simsekolah_ai.exceptions import (
    AIClientError,
    AuthenticationError,
    RateLimitError,
    ServiceUnavailableError,
    ValidationError,
)

try:
    result = client.upload_document(title="Test", content="Content")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except AIClientError as e:
    print(f"SDK error: {e}")
```

## Circuit Breaker

The SDK includes a circuit breaker pattern for resilience:

```python
from simsekolah_ai.circuit_breaker import CircuitBreaker, CircuitBreakerError

# Circuit breaker is automatically configured
# but can be customized:

from simsekolah_ai import Config

config = Config(
    circuit_breaker_enabled=True,
    circuit_breaker_threshold=5,
    circuit_breaker_timeout=30
)
```

## Health Checks

Check service health:

```python
# Check all services
health = client.health_check()
print(health)
# {
#     "document": True,
#     "embedding": True,
#     "retrieval": True,
#     "generation": True
# }

# Check specific service
is_healthy = client.is_service_healthy("embedding")
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=simsekolah_ai --cov-report=html
```

### Code Quality

```bash
# Format code
black simsekolah_ai tests

# Sort imports
isort simsekolah_ai tests

# Type checking
mypy simsekolah_ai

# Linting
ruff check simsekolah_ai
```

### Building for Distribution

```bash
# Build wheel and source distribution
python -m build

# Or using hatch
hatch build
```

### Publishing to PyPI

```bash
# Build
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

### Publishing to Internal Registry

```bash
# Upload to internal registry
twine upload --repository-url https://pypi.simsekolah.com dist/*
```

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/simsekolah/ai-platform-sdk-python/issues
- Email: platform@simsekolah.com
- Documentation: https://docs.simsekolah.com/ai-platform/sdk/python