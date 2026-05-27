# Base Docker Images for AI Platform

This directory contains base Docker images that are used by AI Platform services. Using base images reduces build time, ensures consistency, and makes dependency management easier.

## Available Base Images

### 1. `ai-platform-base:latest`
**File:** `Dockerfile.base`

The foundational Python image with common dependencies for all services.

**Includes:**
- Python 3.11 slim
- Common build tools (gcc, g++)
- uv for fast dependency management
- Standard Python utilities

**Used by:** All services as the foundation

### 2. `ai-platform-ocr:latest`
**File:** `Dockerfile.ocr`

Extends the base image with OCR and vision processing capabilities.

**Includes:**
- Tesseract OCR with English and Indonesian language packs
- OpenCV for image processing
- Pillow for image manipulation
- pytesseract Python wrapper

**Used by:**
- `parser-service` (for OCR functionality)
- `vision-service` (for image processing)

### 3. `ai-platform-ml:latest`
**File:** `Dockerfile.ml`

Extends the base image with machine learning and PyTorch capabilities.

**Includes:**
- PyTorch (CPU version by default)
- Transformers library
- Sentence Transformers
- NumPy, Pandas, scikit-learn
- Accelerate for distributed training

**Used by:**
- `embedding-service` (for text embeddings)
- `generation-service` (for LLM inference)
- `semantic-chunk-service` (for semantic analysis)
- `reranking-service` (for ML-based reranking)
- `moderation-service` (for content moderation)

### 4. `ai-platform-document:latest`
**File:** `Dockerfile.document`

Extends the base image with document processing capabilities.

**Includes:**
- PyMuPDF (fitz) for PDF processing
- pdfplumber for PDF table extraction
- unstructured for document parsing
- camelot for advanced table extraction
- Office document support (docx, xlsx)
- Ghostscript for PDF processing

**Used by:**
- `parser-service` (for document parsing)

## Building Base Images

### Build All Base Images
```bash
cd infra/docker
docker-compose build
```

### Build Specific Base Image
```bash
cd infra/docker
docker-compose build base
docker-compose build ocr
docker-compose build ml
docker-compose build document
```

### Build Using Profile
```bash
cd infra/docker
docker-compose --profile base build
docker-compose --profile ocr build
docker-compose --profile ml build
docker-compose --profile document build
```

## Using Base Images in Services

Update service Dockerfiles to use the appropriate base image:

### Example: Gateway Service (uses base image)
```dockerfile
FROM ai-platform-base:latest

WORKDIR /app

COPY pyproject.toml /app/
RUN uv pip install -e .

COPY app /app/app

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
```

### Example: Parser Service (uses document + ocr images)
```dockerfile
FROM ai-platform-document:latest

# Additional OCR-specific setup if needed
WORKDIR /app

COPY pyproject.toml /app/
RUN uv pip install -e .

COPY app /app/app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Example: Embedding Service (uses ml image)
```dockerfile
FROM ai-platform-ml:latest

WORKDIR /app

COPY pyproject.toml /app/
RUN uv pip install -e .

COPY app /app/app

EXPOSE 8005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
```

## Service to Base Image Mapping

| Service | Base Image | Reason |
|---------|-----------|---------|
| gateway-service | ai-platform-base | Standard API service |
| parser-service | ai-platform-document | PDF/document processing |
| semantic-chunk-service | ai-platform-ml | Semantic analysis with ML |
| metadata-service | ai-platform-base | Standard API service |
| embedding-service | ai-platform-ml | Text embeddings |
| retrieval-service | ai-platform-base | Vector search (lightweight) |
| generation-service | ai-platform-ml | LLM inference |
| audit-service | ai-platform-base | Standard API service |
| monitoring-service | ai-platform-base | Standard API service |
| moderation-service | ai-platform-ml | Content moderation |
| reranking-service | ai-platform-ml | ML-based reranking |
| vision-service | ai-platform-ocr | Image processing & OCR |

## GPU Support

For GPU-enabled services, modify the `Dockerfile.ml` to use CUDA-enabled PyTorch:

```dockerfile
# Replace CPU PyTorch installation with:
RUN pip install --no-cache-dir \
    torch==2.4.0 \
    torchvision==0.19.0 \
    torchaudio==2.4.0 \
    --index-url https://download.pytorch.org/whl/cu121
```

And update service Dockerfiles to use `nvidia` runtime:

```yaml
# In docker-compose.yml for the service:
runtime: nvidia
environment:
  - NVIDIA_VISIBLE_DEVICES=all
```

## Maintenance

### Update Base Images
When dependencies need updating:
1. Update the version in the respective Dockerfile
2. Rebuild the base image
3. Rebuild all dependent services

### Versioning
Consider using version tags for base images in production:
- `ai-platform-base:v1.0.0`
- `ai-platform-ml:v1.0.0`

This allows for rollback and controlled updates.

## Troubleshooting

### Build Failures
If a base image fails to build:
1. Check system dependency availability
2. Verify Python package versions are compatible
3. Check for network issues downloading packages

### Large Image Sizes
Base images can be large due to ML libraries. To optimize:
- Use multi-stage builds where possible
- Remove unnecessary files after installation
- Consider using `.dockerignore` files

## Best Practices

1. **Always build base images first** before building services
2. **Use specific version tags** in production (not `latest`)
3. **Test base images** before deploying to ensure compatibility
4. **Document changes** to base images in changelog
5. **Keep base images updated** with security patches