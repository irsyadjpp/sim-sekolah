# AI Platform Monolith - README

## Overview

AI Platform Monolith adalah arsitektur terpadu yang menggabungkan semua 33+ microservices menjadi satu aplikasi Python unified. Arsitektur ini dirancang untuk deployment yang lebih simple, performance yang lebih baik, dan development yang lebih efficient.

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- 8GB+ RAM
- 20GB+ disk space

### Local Development

```bash
# Clone repository
cd ai-platform/monolith

# Start infrastructure services
docker-compose up -d postgres qdrant redis minio

# Install dependencies
pip install -r requirements.txt

# Run monolith
python -m uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Start complete stack
docker-compose up -d

# View logs
docker-compose logs -f ai-platform-monolith

# Stop stack
docker-compose down
```

---

## Architecture

### Key Components
- **Parser Service**: Document parsing and text extraction
- **Semantic Chunk Service**: Curriculum-aware semantic chunking
- **Semantic Enrichment Service**: Educational tag enrichment
- **Embedding Service**: Vector embedding generation
- **Retrieval Service**: Hybrid semantic retrieval
- **Generation Service**: AI-powered content generation
- **Pipeline Tracker Service**: Document pipeline state tracking
- **Ontology Validation Service**: Educational tag validation

### Communication Pattern
- **Before**: HTTP/gRPC calls between microservices
- **After**: Direct function calls within monolith
- **Result**: Zero network latency, simplified debugging

---

## API Endpoints

### Health Check
```
GET /health
```

### Parser Service
```
POST /api/v1/parser/parse
Content-Type: application/json
{
  "document_data": "...",
  "document_type": "pdf",
  "metadata": {...}
}
```

### Semantic Chunk Service
```
POST /api/v1/chunk/chunk
Content-Type: application/json
{
  "document": {...},
  "chunking_strategy": "semantic"
}
```

### Other Services
- `/api/v1/enrichment/enrich` - Semantic enrichment
- `/api/v1/embedding/generate` - Embedding generation
- `/api/v1/retrieval/retrieve` - Document retrieval
- `/api/v1/generation/generate` - Content generation
- `/api/v1/ontology/validate` - Ontology validation

---

## Configuration

### Environment Variables
See `.env` file for configuration options:
- Database connection settings
- Vector database settings
- Storage configuration
- AI model settings
- Processing parameters

### Database Schema
Monolith uses single PostgreSQL database:
- `pipeline_state` - Document pipeline tracking
- `documents` - Document metadata
- `chunks` - Semantic chunks
- `embeddings` - Vector embeddings

---

## Benefits

### Compared to Microservices
1. **Simpler Deployment**: Single container vs 33+ containers
2. **Better Performance**: Zero network latency
3. **Easier Debugging**: Single codebase, direct function calls
4. **Cost Efficiency**: Reduced infrastructure overhead
5. **Faster Development**: No inter-service mocking

### Performance Improvements
- Eliminates network latency between services
- Shared memory access
- Direct function calls vs HTTP/gRPC
- Unified caching strategy
- Single database connection pool

---

## Development

### Adding New Functionality
```python
# 1. Add service class to app/services/
# 2. Add API routes to app/api/
# 3. Register routes in app/main.py
# 4. Initialize service in lifespan
```

### Testing
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_parser_service.py

# Run with coverage
pytest --cov=app
```

---

## Migration Path

### From Microservices to Monolith
1. ✅ Created unified application structure
2. ✅ Consolidated dependencies
3. ✅ Integrated core services
4. ✅ Simplified deployment
5. ✅ Updated documentation

### Future Expansion Options
- Horizontal scaling: Multiple instances
- Service extraction: Extract specific services if needed
- Hybrid approach: Core services in monolith, specialized as microservices

---

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# View application logs
docker-compose logs -f ai-platform-monolith

# View infrastructure logs
docker-compose logs -f postgres qdrant redis
```

### Metrics
- Application metrics via Prometheus
- Database metrics via pg_stat
- Vector DB metrics via Qdrant dashboard

---

## Troubleshooting

### Common Issues
1. **Database Connection**: Check PostgreSQL container health
2. **Vector Database**: Verify Qdrant container is running
3. **Memory Issues**: Increase Docker memory allocation
4. **Model Loading**: Ensure model files are accessible

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true

# Run with detailed logging
python -m uvicorn app.main:app --log-level debug
```

---

## Comparison with Microservices

| Aspect | Microservices | Monolith |
|--------|---------------|----------|
| Containers | 33+ | 1 |
| Network Calls | Inter-service HTTP/gRPC | Direct function calls |
| Deployment Complexity | High | Low |
| Debugging | Cross-service tracing | Single codebase |
| Network Latency | High | Zero |
| Infrastructure Cost | High | Low |
| Team Coordination | Complex | Simple |
| Scaling | Per-service | Application-level |

---

## Next Steps

### Phase 2 Integration (Future)
- Integrate remaining specialized services
- Add comprehensive error handling
- Implement advanced caching strategies
- Add performance monitoring

### Phase 3 Integration (Future)
- Integrate assessment engine
- Integrate curriculum engine
- Integrate pedagogy engine
- Integrate learning graph engine

---

## Support

For issues and questions:
- Check ARCHITECTURE.md for detailed documentation
- Review docker-compose.yml for infrastructure setup
- See .env for configuration options

---

## License

Same as parent AI Platform project.