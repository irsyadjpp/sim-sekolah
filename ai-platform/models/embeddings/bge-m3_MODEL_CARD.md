# Model Card: BGE-M3

## Model Information

- **Model Name**: BAAI/bge-m3
- **Model ID**: bge-m3-v1.0.0
- **Version**: 1.0.0
- **Type**: embedding
- **Framework**: PyTorch
- **Language**: multilingual (100+ languages including Indonesian)
- **License**: MIT

## Description

BGE-M3 is a multilingual embedding model from BAAI (Beijing Academy of Artificial Intelligence) designed for dense retrieval and semantic similarity tasks. It supports over 100 languages and provides state-of-the-art performance on multilingual benchmarks.

## Intended Use

### Primary Use Cases
- Document chunk embedding for retrieval
- Query embedding for semantic search
- Cross-lingual semantic similarity
- Text classification and clustering
- Recommendation systems

### Limitations
- Maximum sequence length: 8192 tokens
- Not optimized for code or technical documentation
- May have biases toward certain languages in training data
- Not suitable for real-time streaming applications

## Training Data

### Data Sources
- **CCMatrix**: Large-scale multilingual web text corpus
- **Wikipedia**: Multilingual Wikipedia dumps
- **mC4**: Multilingual Colossal Clean Common Crawl

### Data Characteristics
- **Language**: 100+ languages including Indonesian, English, Chinese, etc.
- **Domain**: General web text, encyclopedia content
- **Time Period**: Up to 2023
- **Size**: ~1.5T tokens

### Biases and Considerations
- May perform better on high-resource languages
- Web text may contain noise and biases
- Cultural biases present in source data
- Not specifically trained for educational content

## Performance

### Benchmark Results
```json
{
  "mteb_average": 64.53,
  "retrieval_accuracy": 0.78,
  "latency_ms": 45,
  "throughput_samples_per_second": 120,
  "memory_usage_mb": 2048,
  "embedding_dimension": 1024
}
```

### Test Environment
- **Hardware**: NVIDIA A100 GPU, 40GB VRAM
- **Software**: PyTorch 2.0.1, CUDA 11.8
- **Test Date**: 2024-01-15

### Language-Specific Performance
- **Indonesian**: 62.3 MTEB score
- **English**: 68.1 MTEB score
- **Chinese**: 65.8 MTEB score
- **Multilingual Average**: 64.53 MTEB score

## Technical Details

### Architecture
- **Model Type**: BERT-based encoder
- **Parameters**: 568M
- **Embedding Dimension**: 1024
- **Maximum Sequence Length**: 8192 tokens
- **Architecture Details**: 27-layer Transformer with 40 attention heads

### Requirements
- **Python Version**: 3.8+
- **Dependencies**: 
  - torch>=2.0.0
  - transformers>=4.30.0
  - sentence-transformers>=2.2.0
- **Hardware**: 
  - GPU: 4GB VRAM minimum (8GB recommended)
  - CPU: 8 cores recommended
  - RAM: 16GB recommended

### Inference Configuration
```yaml
device: cuda
batch_size: 32
max_length: 8192
precision: float16
normalize_embeddings: true
```

## Deployment

### Storage
- **Registry**: Hugging Face / MinIO
- **Path**: s3://ai-platform-models/embeddings/bge-m3/v1.0.0/
- **Size**: ~2.2GB (FP16), ~4.4GB (FP32)

### Resources
- **GPU Memory**: 4GB minimum (8GB recommended)
- **CPU Cores**: 4 minimum (8 recommended)
- **RAM**: 8GB minimum (16GB recommended)

### Environment Variables
```bash
MODEL_NAME=BAAI/bge-m3
MODEL_VERSION=1.0.0
MODEL_PATH=/models/embeddings/bge-m3
EMBEDDING_DEVICE=cuda
EMBEDDING_BATCH_SIZE=32
EMBEDDING_MAX_LENGTH=8192
```

### Download Script
```bash
python models/embeddings/download.py --model bge-m3 --version 1.0.0
```

## Monitoring

### Metrics to Track
- **Latency**: Embedding generation time per batch
- **Throughput**: Number of embeddings per second
- **GPU Utilization**: GPU memory and compute usage
- **Error Rate**: Failed embedding generations
- **Quality**: Embedding quality metrics (if available)

### Logging
- Enable prediction logging: false
- Log sample inputs: false
- Log performance metrics: true

## Integration

### Service Integration
- **Embedding Service**: Primary embedding model
- **Semantic Chunk Service**: Alternative for semantic chunking
- **Retrieval Service**: Query embedding

### API Usage
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-m3')
embeddings = model.encode(["text 1", "text 2"])
```

## Version History

### v1.0.0 (2024-01-15)
- Initial release
- Support for 100+ languages
- 8192 token context window
- 1024-dimensional embeddings

## Maintenance

### Update Schedule
- Review quarterly for potential updates
- Monitor BAAI repository for new versions
- Evaluate new models annually

### Known Issues
- None currently known

### Future Improvements
- Evaluate BGE-M3 v2 when available
- Consider domain-specific fine-tuning for educational content
- Optimize for Indonesian language performance

## References

- [Hugging Face Model Card](https://huggingface.co/BAAI/bge-m3)
- [Paper: BGE-M3](https://arxiv.org/abs/2402.03216)
- [GitHub Repository](https://github.com/FlagOpen/FlagEmbedding)
- [BAAI Website](https://www.baai.ac.cn/)

## Contact

- **Model Owner**: ML Engineering Team
- **Technical Contact**: ml-team@simsekolah.id
- **Support**: #ml-operations Slack channel