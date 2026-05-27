# Storage Fixtures

This directory contains test datasets and CI/CD fixtures for storage backends.

## Structure

```
storage/fixtures/
├── documents/      # Sample documents for testing
│   ├── pdf/       # PDF files
│   ├── txt/       # Text files
│   └── metadata/  # Document metadata JSON files
├── vectors/       # Sample embedding vectors
│   ├── numpy/     # Numpy array files (.npy)
│   └── json/      # JSON vector files
├── graphs/        # Sample graph data
│   ├── nodes/     # Node definitions
│   └── edges/     # Edge definitions
├── sql/           # SQL fixture data
│   ├── seed.sql   # Seed data for PostgreSQL
│   └── cleanup.sql # Cleanup scripts
└── README.md      # This file
```

## Usage

### Loading Fixtures

```bash
# Load SQL fixtures into PostgreSQL
psql -h localhost -U postgres -d ai_platform -f sql/seed.sql

# Load document fixtures into object storage
python scripts/load_documents.py --source documents/

# Load vector fixtures into Qdrant
python scripts/load_vectors.py --source vectors/
```

### Generating Test Data

```bash
# Generate synthetic test documents
python scripts/generate_test_documents.py --count 100 --output documents/

# Generate random vectors for testing
python scripts/generate_test_vectors.py --dimension 1024 --count 1000 --output vectors/
```

## Document Fixtures

### Format

Documents should follow this metadata format:

```json
{
  "id": "doc-001",
  "title": "Sample Document",
  "file_type": "pdf",
  "source": "test_fixture",
  "category": "educational",
  "difficulty": "easy",
  "metadata": {
    "author": "Test Author",
    "subject": "Mathematics",
    "grade_level": "10"
  }
}
```

### Available Fixtures

- `documents/pdf/textbook_chapter_1.pdf` - Sample textbook chapter
- `documents/txt/lecture_notes.txt` - Sample lecture notes
- `documents/metadata/batch_1.json` - Metadata for document batch

## Vector Fixtures

### Format

Vectors should be stored as:

**Numpy format (.npy):**
```python
import numpy as np
vectors = np.random.rand(100, 1024)  # 100 vectors, 1024 dimensions
np.save("vectors/numpy/test_vectors.npy", vectors)
```

**JSON format:**
```json
{
  "vectors": [
    {"id": "vec-001", "values": [0.1, 0.2, ...], "metadata": {"doc_id": "doc-001"}},
    {"id": "vec-002", "values": [0.3, 0.4, ...], "metadata": {"doc_id": "doc-002"}}
  ],
  "dimension": 1024
}
```

## Graph Fixtures

### Node Format

```json
{
  "nodes": [
    {
      "id": "node-001",
      "label": "Concept",
      "properties": {
        "name": "photosynthesis",
        "domain": "biology",
        "difficulty": "medium"
      }
    }
  ]
}
```

### Edge Format

```json
{
  "edges": [
    {
      "from": "node-001",
      "to": "node-002",
      "type": "PREREQUISITE_FOR",
      "properties": {
        "strength": 0.8
      }
    }
  ]
}
```

## SQL Fixtures

### Seed Data Format

```sql
-- Insert test documents
INSERT INTO documents (id, title, content, status, source)
VALUES 
  ('doc-001', 'Test Document 1', 'This is test content...', 'processed', 'test_fixture'),
  ('doc-002', 'Test Document 2', 'More test content...', 'processed', 'test_fixture');

-- Insert test users
INSERT INTO users (id, email, username, role)
VALUES
  ('user-001', 'test@example.com', 'testuser', 'admin');
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Load test fixtures
  run: |
    psql -h localhost -U postgres -d ai_platform_test -f storage/fixtures/sql/seed.sql
    python storage/fixtures/scripts/load_fixtures.py --env test
```

### Docker Compose Example

```yaml
services:
  postgres:
    volumes:
      - ./storage/fixtures/sql/seed.sql:/docker-entrypoint-initdb.d/seed.sql
```

## Best Practices

1. **Keep fixtures small** - Use minimal data for faster CI/CD
2. **Use consistent IDs** - Easy to reference across different storage systems
3. **Version fixtures** - Track changes in fixture data
4. **Clean up after tests** - Use cleanup scripts to reset state
5. **Document fixtures** - Explain what each fixture tests
6. **Separate environments** - Different fixtures for dev/test/prod

## Adding New Fixtures

1. Create appropriate directory structure
2. Add files following format specifications
3. Update this README with new fixture descriptions
4. Add loading scripts if needed
5. Update CI/CD configuration

## Troubleshooting

### Fixture Loading Issues

```bash
# Check fixture format
python scripts/validate_fixtures.py --source documents/

# Test database connection
psql -h localhost -U postgres -d ai_platform -c "SELECT 1"

# Check Qdrant connection
curl http://localhost:6333/collections
```