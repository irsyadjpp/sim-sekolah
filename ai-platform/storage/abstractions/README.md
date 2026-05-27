# Storage Abstractions

Unified interfaces for different storage backends in the AI Platform.

## Overview

This package provides a consistent API for interacting with various storage systems:

- **Object Storage**: S3, MinIO (document storage, model artifacts)
- **Vector Database**: Qdrant (embeddings, semantic search)
- **Graph Database**: Neo4j (knowledge graphs, relationships)
- **Relational Database**: PostgreSQL (metadata, user data)

## Installation

```bash
# Core abstractions (no dependencies)
pip install -e ai-platform/storage/abstractions

# With specific backend dependencies
pip install -e ai-platform/storage/abstractions[postgresql,qdrant,neo4j,s3]
```

## Usage

### Configuration

All storage backends use a common `StorageConfig`:

```python
from ai_platform.storage.abstractions import StorageConfig

config = StorageConfig(
    host="localhost",
    port=5432,
    username="user",
    password="pass",
    database="ai_platform",
    use_ssl=False,
    pool_size=10,
    max_retries=3
)

# Or from environment variables
config = StorageConfig.from_env(prefix="POSTGRES_")
```

### Object Storage (S3/MinIO)

```python
from ai_platform.storage.abstractions import S3Storage, MinIOStorage, StorageConfig

# S3
config = StorageConfig(
    host="s3.amazonaws.com",
    port=443,
    username="AWS_ACCESS_KEY",
    password="AWS_SECRET_KEY",
    extra_params={"region": "us-east-1"}
)

s3 = S3Storage(config)
await s3.connect()

# Upload file
await s3.upload_file(
    file_path="/path/to/file.pdf",
    bucket="documents",
    object_key="2024/05/file.pdf",
    metadata={"author": "John Doe", "category": "educational"}
)

# Download file
await s3.download_file(
    bucket="documents",
    object_key="2024/05/file.pdf",
    local_path="/tmp/downloaded.pdf"
)

# List files
files = await s3.list_files(bucket="documents", prefix="2024/", limit=100)

# Generate presigned URL
url = await s3.generate_presigned_url(
    bucket="documents",
    object_key="2024/05/file.pdf",
    expiration=3600
)

await s3.disconnect()
```

### Vector Database (Qdrant)

```python
from ai_platform.storage.abstractions import QdrantDB, StorageConfig

config = StorageConfig(
    host="localhost",
    port=6333
)

qdrant = QdrantDB(config)
await qdrant.connect()

# Create collection
await qdrant.create_collection(
    collection_name="document_embeddings",
    vector_size=1024,
    distance_metric="Cosine"
)

# Insert vectors
vector_ids = await qdrant.insert_vectors(
    collection_name="document_embeddings",
    vectors=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    payloads=[
        {"document_id": "doc1", "chunk_id": "chunk1"},
        {"document_id": "doc2", "chunk_id": "chunk1"}
    ],
    ids=["vec1", "vec2"]
)

# Search similar vectors
results = await qdrant.search(
    collection_name="document_embeddings",
    query_vector=[0.1, 0.2, ...],
    limit=10,
    score_threshold=0.7,
    filter_condition={"document_id": "doc1"}
)

# Get collection info
info = await qdrant.get_collection_info("document_embeddings")

await qdrant.disconnect()
```

### Graph Database (Neo4j)

```python
from ai_platform.storage.abstractions import Neo4jDB, StorageConfig

config = StorageConfig(
    host="localhost",
    port=7687,
    username="neo4j",
    password="password",
    database="knowledge_graph"
)

neo4j = Neo4jDB(config)
await neo4j.connect()

# Create node
node_id = await neo4j.create_node(
    label="Concept",
    properties={
        "name": "photosynthesis",
        "domain": "biology",
        "difficulty": "medium"
    }
)

# Create relationship
rel_id = await neo4j.create_relationship(
    from_node_id=node_id,
    to_node_id=another_node_id,
    relationship_type="PREREQUISITE_FOR",
    properties={"strength": 0.8}
)

# Find nodes
nodes = await neo4j.find_nodes(
    label="Concept",
    properties={"domain": "biology"},
    limit=100
)

# Get neighbors
neighbors = await neo4j.get_neighbors(
    node_id=node_id,
    relationship_type="PREREQUISITE_FOR",
    direction="outgoing"
)

# Find path
path = await neo4j.get_path(
    from_node_id=node_id,
    to_node_id=target_node_id,
    relationship_types=["PREREQUISITE_FOR", "RELATED_TO"],
    max_depth=5
)

# Execute custom Cypher query
results = await neo4j.execute_query(
    query="""
    MATCH (c:Concept {domain: $domain})
    RETURN c.name, c.difficulty
    ORDER BY c.difficulty
    LIMIT $limit
    """,
    parameters={"domain": "biology", "limit": 10}
)

await neo4j.disconnect()
```

### Relational Database (PostgreSQL)

```python
from ai_platform.storage.abstractions import PostgreSQL, StorageConfig, TableSchema, ColumnDefinition

config = StorageConfig(
    host="localhost",
    port=5432,
    username="postgres",
    password="password",
    database="ai_platform"
)

postgres = PostgreSQL(config)
await postgres.connect()

# Create table
schema = TableSchema(
    name="documents",
    columns=[
        ColumnDefinition(name="id", type="SERIAL", primary_key=True),
        ColumnDefinition(name="title", type="VARCHAR(255)", nullable=False),
        ColumnDefinition(name="content", type="TEXT"),
        ColumnDefinition(name="created_at", type="TIMESTAMP", default="NOW()"),
    ]
)

await postgres.create_table(schema)

# Insert data
inserted_ids = await postgres.insert(
    table_name="documents",
    data={
        "title": "Introduction to AI",
        "content": "Artificial Intelligence is..."
    }
)

# Select data
results = await postgres.select(
    table_name="documents",
    columns=["id", "title"],
    where={"title": "Introduction to AI"},
    limit=10,
    order_by=["created_at DESC"]
)

# Update data
affected_rows = await postgres.update(
    table_name="documents",
    data={"content": "Updated content..."},
    where={"id": 1}
)

# Delete data
affected_rows = await postgres.delete(
    table_name="documents",
    where={"id": 1}
)

# Transactions
transaction_id = await postgres.begin_transaction()
try:
    await postgres.insert(
        table_name="documents",
        data={"title": "Doc 1", "content": "..."}
    )
    await postgres.insert(
        table_name="documents",
        data={"title": "Doc 2", "content": "..."}
    )
    await postgres.commit_transaction(transaction_id)
except Exception as e:
    await postgres.rollback_transaction(transaction_id)
    raise

await postgres.disconnect()
```

## Context Manager Usage

All backends support async context managers:

```python
from ai_platform.storage.abstractions import QdrantDB, StorageConfig

config = StorageConfig(host="localhost", port=6333)

async with QdrantDB(config) as qdrant:
    results = await qdrant.search(
        collection_name="embeddings",
        query_vector=[...],
        limit=10
    )
    # Automatically disconnects after block
```

## Health Checks

All backends provide health check functionality:

```python
health = await qdrant.health_check()
print(health)
# {
#     "status": "healthy",
#     "backend": "qdrant",
#     "collections_count": 5,
#     "details": {...}
# }
```

## Error Handling

All backends raise standard exceptions:

- `ConnectionError`: Connection failures
- `TimeoutError`: Operation timeouts
- `ValueError`: Invalid parameters
- `RuntimeError`: Backend-specific errors

```python
try:
    await s3.upload_file(...)
except ConnectionError as e:
    print(f"Failed to connect: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Use context managers** for automatic connection management
2. **Check health** before critical operations
3. **Handle retries** via config (max_retries, retry_delay)
4. **Use connection pooling** for high-throughput scenarios
5. **Validate configuration** before connecting
6. **Clean up connections** in finally blocks or context managers

## Backend-Specific Notes

### S3/MinIO
- S3 requires AWS credentials in config
- MinIO can run locally without SSL for development
- Both support presigned URLs for temporary access
- Metadata is stored as key-value pairs on objects

### Qdrant
- Collections must be created before inserting vectors
- Distance metrics: Cosine (default), Euclidean, Dot
- Supports filtering by payload fields
- Batch insert for better performance

### Neo4j
- Uses Cypher query language
- Relationships are directional (incoming/outgoing/both)
- Supports complex graph traversals
- Indexes should be created for frequently queried properties

### PostgreSQL
- Supports transactions with rollback
- Use parameterized queries to prevent SQL injection
- Connection pooling is built-in
- Schema migrations should be managed separately

## Testing

Mock implementations are available for testing:

```python
from ai_platform.storage.abstractions import MockVectorDB

mock_db = MockVectorDB()
await mock_db.connect()
# Test without real database
```

## Contributing

When adding new storage backends:

1. Inherit from the appropriate abstract base class
2. Implement all abstract methods
3. Add health check and ping methods
4. Support async context managers
5. Add comprehensive error handling
6. Include unit tests
7. Update this README