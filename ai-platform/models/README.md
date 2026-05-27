# AI Platform Models

This directory contains model cards, configurations, and registry pointers for all ML models used in the AI Platform.

## Directory Structure

```
models/
├── embeddings/          # Text and image embedding models
├── rerankers/          # Result reranking models
├── classifiers/         # Text classification models
├── vision/             # Computer vision and OCR models
├── OCR/                # OCR-specific models
├── moderation/         # Content moderation models
└── local-llm/          # Local LLM models (quantized, fine-tuned)

```

## Model Categories

### Embedding Models
Text and image embedding models for vector search and semantic similarity.

**Current Models**:
- BAAI/bge-m3 (multilingual embedding)
- sentence-transformers/all-MiniLM-L6-v2 (lightweight)
- OpenAI text-embedding-3-small (API-based)

**Use Cases**:
- Document chunk embedding
- Query embedding for retrieval
- Semantic search
- Similarity scoring

### Reranking Models
Models for reranking and improving retrieval results.

**Current Models**:
- BAAI/bge-reranker-base
- cross-encoder/ms-marco-MiniLM-L-6-v2

**Use Cases**:
- Retrieval result reranking
- Search result optimization
- Relevance scoring

### Classifiers
Text classification models for content categorization.

**Current Models**:
- Educational content classifier
- Difficulty level classifier
- Subject area classifier

**Use Cases**:
- Document classification
- Content tagging
- Metadata enrichment

### Vision Models
Computer vision models for image processing.

**Current Models**:
- Layout analysis models
- Document structure recognition
- Chart and diagram understanding

**Use Cases**:
- Document layout analysis
- Image understanding
- Visual content extraction

### OCR Models
Optical character recognition models.

**Current Models**:
- Tesseract (multi-language)
- PaddleOCR (Chinese/English)
- TrOCR (transformer-based)

**Use Cases**:
- Text extraction from images
- Document digitization
- Handwriting recognition

### Moderation Models
Content moderation and safety models.

**Current Models**:
- OpenAI Moderation API
- Perspective API (toxicity detection)
- Custom content filters

**Use Cases**:
- Content safety checks
- Toxicity detection
- Policy enforcement

### Local LLM Models
Local large language models for offline inference.

**Current Models**:
- Llama-3-8B-Instruct (quantized)
- Mistral-7B-Instruct (quantized)
- Qwen-7B-Instruct (quantized)

**Use Cases**:
- Offline text generation
- Privacy-preserving inference
- Cost optimization

## Model Card Template

Each model should have a model card with the following information:

### Model Card Structure

```yaml
model_name: Model Name
model_id: unique-model-id
version: 1.0.0
type: embedding/reranker/classifier/vision/ocr/moderation/llm
framework: pytorch/tensorflow/onnx
language: multilingual/indonesian/english
license: MIT/Apache-2.0/Proprietary

description: |
  Brief description of the model and its purpose.

intended_use: |
  Intended use cases and limitations.

training_data: |
  Information about training data sources and characteristics.

performance: |
  Benchmark results and performance metrics.

limitations: |
  Known limitations and biases.

ethical_considerations: |
  Ethical considerations and potential misuse.

deployment: |
  Deployment requirements (hardware, dependencies).
```

## Model Registry Integration

Models are stored in MinIO object storage (not in git):
- **Production models**: `s3://ai-platform-models/production/`
- **Staging models**: `s3://ai-platform-models/staging/`
- **Development models**: `s3://ai-platform-models/dev/`

### Model Download Script

Each model folder should include a `download.py` script:

```python
#!/usr/bin/env python3
"""
Download model from registry to local cache.
"""

import os
import argparse
from pathlib import Path

def download_model(model_name: str, version: str = "latest"):
    """Download model from MinIO."""
    # Implementation
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--version", default="latest")
    args = parser.parse_args()
    download_model(args.model, args.version)
```

### Benchmark Results

Each model folder should include `benchmark_results.json`:

```json
{
  "model_name": "bge-m3",
  "version": "1.0.0",
  "benchmarks": {
    "accuracy": 0.95,
    "latency_ms": 50,
    "throughput_samples_per_second": 100,
    "memory_usage_mb": 512
  },
  "test_date": "2024-01-01T00:00:00Z",
  "test_environment": "A100 GPU, PyTorch 2.0"
}
```

## Configuration Format

Each model should have a `config.yaml`:

```yaml
model:
  name: bge-m3
  version: 1.0.0
  type: embedding
  framework: pytorch
  language: multilingual

download:
  source: minio
  bucket: ai-platform-models
  path: embeddings/bge-m3/v1.0.0/
  files:
    - model.safetensors
    - config.json
    - tokenizer.json
    - vocab.txt

inference:
  device: cuda
  batch_size: 32
  max_length: 512
  precision: float16

resources:
  gpu_memory_mb: 2048
  cpu_cores: 4
  ram_mb: 8192

monitoring:
  enable_metrics: true
  log_predictions: false
```

## Best Practices

1. **Version Control**: Track model versions, not weights
2. **Documentation**: Complete model cards for each model
3. **Benchmarking**: Regular performance testing
4. **Security**: Scan models for vulnerabilities
5. **Licensing**: Clear license information
6. **Testing**: Validate model behavior before deployment
7. **Monitoring**: Track model performance in production
8. **Backup**: Maintain backup of critical models

## Model Selection Criteria

When adding new models, consider:

- **Performance**: Accuracy, speed, resource requirements
- **License**: Compatibility with commercial use
- **Language**: Support for Indonesian/English
- **Size**: Model size for deployment constraints
- **Maintenance**: Active development and updates
- **Community**: Support and documentation quality

## Troubleshooting

### Download Failures
- Check MinIO connectivity
- Verify model version exists
- Check available disk space
- Review access permissions

### Performance Issues
- Check hardware requirements
- Verify model configuration
- Monitor resource usage
- Review benchmark results

### Compatibility Issues
- Verify framework versions
- Check dependency conflicts
- Test in staging environment
- Review model format compatibility

## Contact

For model-related questions:
- Model Selection: ML engineering team
- Performance Issues: MLOps team
- Licensing: Legal department
- Integration: Platform engineering team