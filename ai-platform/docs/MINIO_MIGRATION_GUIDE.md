# SeaweedFS Migration Guide for Knowledge Folder

## Overview

Panduan komprehensif untuk memigrasikan knowledge folder dari local filesystem ke SeaweedFS distributed object storage.

---

## Architecture Changes

### Current Architecture
```
ai-platform/knowledge/ (local filesystem)
├── cp/
├── atp/
├── buku_guru/
├── buku_siswa/
└── ...

↓ Parser Service (local file access)
↓ Vision Service (local file access)
↓ Semantic Chunk Service (local file access)
↓ Metadata Service (local file access)
↓ Embedding Service (local file access)
```

### Target Architecture
```
SeaweedFS S3 Bucket: knowledge-assets
├── knowledge/cp/
├── knowledge/atp/
├── knowledge/buku_guru/
├── knowledge/buku_siswa/
└── ...

↓ Parser Service (SeaweedFS S3 API)
↓ Vision Service (SeaweedFS S3 API)
↓ Semantic Chunk Service (SeaweedFS S3 API)
↓ Metadata Service (SeaweedFS S3 API)
↓ Embedding Service (SeaweedFS S3 API)
```

---

## Migration Steps

### Phase 1: Preparation

#### 1.1 Setup SeaweedFS Configuration
```yaml
# seaweedfs_config.yaml
seaweedfs:
  s3:
    endpoint: "http://seaweedfs-s3:8333"
    region: "us-east-1"
    access_key_id: "admin"
    secret_access_key: "admin"
  bucket:
    name: "knowledge-assets"
    create_if_not_exists: true
```

#### 1.2 Test SeaweedFS Connectivity
```bash
# Test SeaweedFS S3 endpoint
curl http://localhost:8333

# Test dengan AWS CLI
aws --endpoint-url http://localhost:8333 s3 ls
```

### Phase 2: Data Migration

#### 2.1 Run Migration Script
```bash
# Setup Python environment
cd ai-platform/knowledge
pip install boto3

# Configure environment variables
export SEAWEEDFS_S3_ENDPOINT="http://seaweedfs-s3:8333"
export SEAWEEDFS_ACCESS_KEY="admin"
export SEAWEEDFS_SECRET_KEY="admin"
export BUCKET_NAME="knowledge-assets"
export KNOWLEDGE_ROOT="/path/to/ai-platform/knowledge"

# Run migration
python seaweedfs_migration.py
```

#### 2.2 Verify Migration
```python
# Verification script
import boto3

s3 = boto3.client('s3',
    endpoint_url='http://seaweedfs-s3:8333',
    aws_access_key_id='admin',
    aws_secret_access_key='admin',
    region_name='us-east-1'
)

# List objects in bucket
response = s3.list_objects_v2(Bucket='knowledge-assets', Prefix='knowledge/')
print(f"Total objects: {len(response.get('Contents', []))}")
```

### Phase 3: Service Integration

#### 3.1 Update Parser Service
```python
# services/parser-service/app/config.py
class ParserConfig:
    def __init__(self):
        # SeaweedFS Configuration
        self.seaweedfs_enabled = os.getenv('SEAWEEDFS_ENABLED', 'true').lower() == 'true'
        self.seaweedfs_endpoint = os.getenv('SEAWEEDFS_S3_ENDPOINT', 'http://seaweedfs-s3:8333')
        self.seaweedfs_bucket = os.getenv('SEAWEEDFS_KNOWLEDGE_BUCKET', 'knowledge-assets')
        
        # Fallback to local filesystem
        self.local_knowledge_path = os.getenv('LOCAL_KNOWLEDGE_PATH', '/app/knowledge')
```

```python
# services/parser-service/app/services/document_parser.py
from app.config.seaweedfs_config import get_seaweedfs_client

class DocumentParser:
    def __init__(self):
        self.seaweedfs_client = get_seaweedfs_client()
    
    def parse_document(self, document_path: str):
        """
        Parse document dari SeaweedFS atau local filesystem.
        
        Args:
            document_path: Path ke document (relatif terhadap knowledge prefix)
        """
        try:
            # Coba ambil dari SeaweedFS dulu
            content = self.seaweedfs_client.get_object(document_path)
            if content:
                return self._parse_content(content)
        except Exception as e:
            print(f"SeaweedFS access failed: {e}, trying local filesystem")
        
        # Fallback ke local filesystem
        local_path = f"/app/knowledge/{document_path}"
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                return self._parse_content(f.read())
        
        raise FileNotFoundError(f"Document not found: {document_path}")
```

#### 3.2 Update Semantic Chunk Service
```python
# services/semantic-chunk-service/app/services/chunking_service.py
from app.config.seaweedfs_config import get_seaweedfs_client

class ChunkingService:
    def __init__(self):
        self.seaweedfs_client = get_seaweedfs_client()
    
    def chunk_document(self, document_path: str, options: ChunkingOptions):
        """
        Chunk document dari SeaweedFS.
        
        Args:
            document_path: Path ke document di SeaweedFS
            options: Chunking options
        """
        # Get document dengan metadata
        content, metadata = self.seaweedfs_client.get_object_with_metadata(document_path)
        
        if content is None:
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Extract text dari content
        text = self._extract_text(content, metadata.get('file_type'))
        
        # Perform semantic chunking
        chunks = self._semantic_chunk(text, options, metadata)
        
        return chunks
```

#### 3.3 Update Other Services

Similar pattern untuk:
- **Vision Service**: Untuk OCR dan image processing
- **Metadata Service**: Untuk metadata enrichment
- **Embedding Service**: Untuk vector generation
- **Retrieval Service**: Untuk knowledge retrieval

### Phase 4: Environment Configuration

#### 4.1 Update Docker Compose for AI Platform
```yaml
# ai-platform/docker-compose.yml
services:
  parser-service:
    environment:
      - SEAWEEDFS_S3_ENDPOINT=http://seaweedfs-s3:8333
      - SEAWEEDFS_ACCESS_KEY=admin
      - SEAWEEDFS_SECRET_KEY=admin
      - SEAWEEDFS_KNOWLEDGE_BUCKET=knowledge-assets
      - SEAWEEDFS_ENABLED=true
    depends_on:
      - seaweedfs-s3

  semantic-chunk-service:
    environment:
      - SEAWEEDFS_S3_ENDPOINT=http://seaweedfs-s3:8333
      - SEAWEEDFS_ACCESS_KEY=admin
      - SEAWEEDFS_SECRET_KEY=admin
      - SEAWEEDFS_KNOWLEDGE_BUCKET=knowledge-assets
      - SEAWEEDFS_ENABLED=true
    depends_on:
      - seaweedfs-s3

  # Similar configuration untuk semua services yang akses knowledge
```

#### 4.2 Update Service Configuration Files
```yaml
# services/*/config.yaml
storage:
  type: "seaweedfs"  # or "hybrid" untuk fallback ke local
  seaweedfs:
    endpoint: "${SEAWEEDFS_S3_ENDPOINT}"
    bucket: "${SEAWEEDFS_KNOWLEDGE_BUCKET}"
    access_key: "${SEAWEEDFS_ACCESS_KEY}"
    secret_key: "${SEAWEEDFS_SECRET_KEY}"
    prefix: "knowledge/"
  fallback:
    enabled: true
    local_path: "/app/knowledge"
```

### Phase 5: Testing & Validation

#### 5.1 Unit Tests
```python
# services/parser-service/tests/test_seaweedfs_integration.py
import pytest
from app.config.seaweedfs_config import SeaweedFSConfig, SeaweedFSClient

def test_seaweedfs_config():
    config = SeaweedFSConfig.from_env()
    assert config.endpoint_url is not None
    assert config.bucket_name == "knowledge-assets"

def test_seaweedfs_client():
    config = SeaweedFSConfig.from_env()
    client = SeaweedFSClient(config)
    
    # Test basic operations
    test_content = b"test content"
    client.upload_object("test/test.txt", test_content)
    
    retrieved = client.get_object("test/test.txt")
    assert retrieved == test_content
    
    # Cleanup
    client.s3_client.delete_object(Bucket=config.bucket_name, Key=f"{config.knowledge_prefix}test/test.txt")

@pytest.mark.integration
def test_document_parsing_with_seaweedfs():
    """Integration test untuk parsing dari SeaweedFS."""
    from app.services.document_parser import DocumentParser
    
    parser = DocumentParser()
    # Test dengan document yang sudah di-upload ke SeaweedFS
    chunks = parser.parse_document("cp/matematika/kelas-10/v1.0.0/cp.json")
    assert chunks is not None
```

#### 5.2 Integration Tests
```python
# tests/integration/test_knowledge_pipeline.py
def test_full_pipeline_with_seaweedfs():
    """Test full ingestion pipeline dengan SeaweedFS."""
    
    # 1. Parser Service reads dari SeaweedFS
    parsed_content = parser_service.parse("buku_guru/matematika/kelas-4/v1.0.0/contents.pdf")
    
    # 2. Vision Service processes images dari SeaweedFS
    ocr_results = vision_service.process_images(parsed_content['images'])
    
    # 3. Semantic Chunk Service chunks dari SeaweedFS content
    chunks = chunk_service.chunk(parsed_content['text'], options)
    
    # 4. Metadata Service enriches dari SeaweedFS metadata
    enriched_chunks = metadata_service.enrich(chunks)
    
    # 5. Embedding Service generates embeddings
    embeddings = embedding_service.generate_embeddings(enriched_chunks)
    
    # 6. Verify semua data berasal dari SeaweedFS
    assert all(chunk['source'] == 'seaweedfs' for chunk in chunks)
```

### Phase 6: Deployment

#### 6.1 Staged Rollout
```bash
# 1. Deploy ke staging environment
kubectl apply -f infra/kubernetes/staging/

# 2. Test di staging
./scripts/test_staging.sh

# 3. Monitor metrics
./scripts/monitor_migration.sh

# 4. Deploy ke production
kubectl apply -f infra/kubernetes/production/
```

#### 6.2 Monitoring & Validation
```python
# monitoring/knowledge_access_monitor.py
import boto3
from datetime import datetime, timedelta

def monitor_seaweedfs_access():
    """Monitor access patterns ke knowledge assets di SeaweedFS."""
    s3 = boto3.client('s3',
        endpoint_url='http://seaweedfs-s3:8333',
        aws_access_key_id='admin',
        aws_secret_access_key='admin'
    )
    
    # Get access statistics
    stats = s3.list_objects_v2(Bucket='knowledge-assets')
    
    # Monitor popular files
    popular_files = sorted(
        stats.get('Contents', []),
        key=lambda x: x.get('LastModified'),
        reverse=True
    )[:10]
    
    print("Top 10 recently accessed files:")
    for file in popular_files:
        print(f"  - {file['Key']}: {file['LastModified']}")
```

---

## Benefits

### 1. **Scalability**
- Horizontal scaling dengan menambah volume servers
- No single point of failure
- Distributed load handling

### 2. **Performance**
- Parallel access dari multiple services
- Built-in caching mechanisms
- CDN-like distribution

### 3. **Maintenance**
- Centralized storage management
- Easier backup and restore
- Simplified updates and versioning

### 4. **Reliability**
- Built-in replication
- Automatic failover
- Data integrity checks

---

## Rollback Plan

Jika ada issues dengan SeaweedFS migration:

### Immediate Rollback
```bash
# 1. Switch back to local filesystem
export SEAWEEDFS_ENABLED=false

# 2. Restart services
kubectl rollout restart deployment/parser-service
kubectl rollout restart deployment/semantic-chunk-service
# ... untuk semua services

# 3. Verify functionality
./scripts/verify_local_access.sh
```

### Data Recovery
```python
# Emergency download dari SeaweedFS
def emergency_download_from_seaweedfs():
    """Download semua knowledge assets dari SeaweedFS ke local."""
    s3 = boto3.client('s3', endpoint_url='http://seaweedfs-s3:8333')
    
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket='knowledge-assets'):
        for obj in page.get('Contents', []):
            local_path = f"/app/knowledge/{obj['Key'].replace('knowledge/', '')}"
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            s3.download_file('knowledge-assets', obj['Key'], local_path)
            print(f"Downloaded: {local_path}")
```

---

## Troubleshooting

### Common Issues

#### Issue: Connection Timeout
```bash
# Solution: Increase timeout configuration
export SEAWEEDFS_CONNECT_TIMEOUT=60
export SEAWEEDFS_READ_TIMEOUT=180
```

#### Issue: Authentication Error
```bash
# Solution: Verify credentials
aws --endpoint-url http://seaweedfs-s3:8333 s3 ls --profile seaweedfs
```

#### Issue: Performance Issues
```python
# Solution: Enable caching dan increase concurrent requests
config.max_concurrent_requests = 20
config.enable_cache = True
```

---

## Maintenance Procedures

### Regular Tasks

#### 1. Cache Cleanup
```python
# Run daily cache cleanup
from app.config.seaweedfs_config import get_seaweedfs_client
client = get_seaweedfs_client()
client.cleanup_cache()
```

#### 2. Health Checks
```python
# Automated health check
def check_seaweedfs_health():
    """Check SeaweedFS service health."""
    try:
        s3 = boto3.client('s3', endpoint_url='http://seaweedfs-s3:8333')
        s3.head_bucket(Bucket='knowledge-assets')
        return True
    except Exception as e:
        print(f"SeaweedFS health check failed: {e}")
        return False
```

#### 3. Backup Verification
```bash
# Monthly backup verification
./scripts/verify_backup_integrity.sh
```

---

## Cost Analysis

### Storage Costs
- **SeaweedFS**: On-premise (no additional cost)
- **Local Filesystem**: On-premise (no additional cost)
- **Difference**: No significant storage cost difference

### Operational Costs
- **Maintenance**: Slightly higher dengan distributed system
- **Monitoring**: Additional monitoring requirements
- **Training**: Staff training for SeaweedFS management

### ROI Considerations
- **Scalability**: Significant improvement
- **Reliability**: Major improvement
- **Performance**: Moderate improvement
- **Maintenance**: Long-term improvement

---

## Conclusion

Migrating knowledge folder ke SeaweedFS provides significant benefits untuk scalability, reliability, dan maintenance. The migration process is straightforward dengan proper planning dan staged rollout.

**Recommendation**: Implement in phases dengan thorough testing di staging environment sebelum production deployment.
