"""
MinIO AIStor Configuration for Semantic Chunk Service
Configuration untuk akses knowledge assets dari MinIO AIStor S3-compatible storage
"""

import os
from typing import Optional
from dataclasses import dataclass
import boto3
from botocore.client import Config


@dataclass
class MinIOConfig:
    """Configuration untuk MinIO AIStor S3 client."""
    
    # S3 Endpoint Configuration
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "us-east-1"
    
    # Bucket Configuration
    bucket_name: str = "knowledge-assets"
    knowledge_prefix: str = "knowledge/"
    
    # Performance Configuration
    max_concurrent_requests: int = 10
    connect_timeout: int = 30
    read_timeout: int = 90
    
    # Caching Configuration
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600
    cache_directory: str = "/tmp/knowledge_cache"
    
    # Retry Configuration
    max_retries: int = 3
    retry_backoff: int = 2
    
    @classmethod
    def from_env(cls) -> 'MinIOConfig':
        """Create configuration dari environment variables."""
        return cls(
            endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://minio:9000'),
            aws_access_key_id=os.getenv('MINIO_ROOT_USER', 'admin'),
            aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD', 'admin123'),
            region_name=os.getenv('MINIO_REGION', 'us-east-1'),
            bucket_name=os.getenv('MINIO_KNOWLEDGE_BUCKET', 'knowledge-assets'),
            knowledge_prefix=os.getenv('MINIO_KNOWLEDGE_PREFIX', 'knowledge/'),
            max_concurrent_requests=int(os.getenv('MINIO_MAX_CONCURRENT', '10')),
            connect_timeout=int(os.getenv('MINIO_CONNECT_TIMEOUT', '30')),
            read_timeout=int(os.getenv('MINIO_READ_TIMEOUT', '90')),
            enable_cache=os.getenv('MINIO_ENABLE_CACHE', 'true').lower() == 'true',
            cache_ttl_seconds=int(os.getenv('MINIO_CACHE_TTL', '3600')),
            cache_directory=os.getenv('MINIO_CACHE_DIR', '/tmp/knowledge_cache'),
            max_retries=int(os.getenv('MINIO_MAX_RETRIES', '3')),
            retry_backoff=int(os.getenv('MINIO_RETRY_BACKOFF', '2'))
        )


class MinIOClient:
    """Client untuk akses knowledge assets dari MinIO AIStor."""
    
    def __init__(self, config: MinIOConfig):
        """
        Initialize MinIO AIStor client.
        
        Args:
            config: MinIO AIStor configuration
        """
        self.config = config
        
        # Configure S3 client untuk MinIO AIStor
        self.s3_client = boto3.client(
            's3',
            endpoint_url=config.endpoint_url,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.region_name,
            config=Config(
                max_pool_connections=config.max_concurrent_requests,
                connect_timeout=config.connect_timeout,
                read_timeout=config.read_timeout,
                retries={
                    'max_attempts': config.max_retries,
                    'mode': 'adaptive'
                }
            )
        )
        
        # Initialize cache jika enabled
        self.cache = {}
        if config.enable_cache:
            self._init_cache()
    
    def _init_cache(self):
        """Initialize local cache directory."""
        import os
        os.makedirs(self.config.cache_directory, exist_ok=True)
    
    def get_object(self, key: str, use_cache: bool = True) -> Optional[bytes]:
        """
        Get object dari MinIO AIStor dengan optional caching.
        
        Args:
            key: Object key (relatif terhadap knowledge prefix)
            use_cache: Whether to use cache jika available
            
        Returns:
            Object content as bytes, or None jika not found
        """
        full_key = f"{self.config.knowledge_prefix}{key}"
        
        # Check cache first
        if use_cache and self.config.enable_cache:
            cache_key = self._get_cache_key(full_key)
            if cache_key in self.cache:
                return self.cache[cache_key]['content']
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.config.bucket_name,
                Key=full_key
            )
            
            content = response['Body'].read()
            
            # Cache the result
            if use_cache and self.config.enable_cache:
                self._cache_object(full_key, content, response.get('Metadata', {}))
            
            return content
            
        except self.s3_client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            print(f"Error getting object {full_key}: {e}")
            return None
    
    def get_object_with_metadata(self, key: str, use_cache: bool = True) -> Optional[tuple]:
        """
        Get object dengan metadata dari MinIO AIStor.
        
        Args:
            key: Object key (relatif terhadap knowledge prefix)
            use_cache: Whether to use cache jika available
            
        Returns:
            Tuple of (content, metadata), or None jika not found
        """
        full_key = f"{self.config.knowledge_prefix}{key}"
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.config.bucket_name,
                Key=full_key
            )
            
            content = response['Body'].read()
            metadata = response.get('Metadata', {})
            
            # Cache the result
            if use_cache and self.config.enable_cache:
                self._cache_object(full_key, content, metadata)
            
            return (content, metadata)
            
        except self.s3_client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            print(f"Error getting object {full_key}: {e}")
            return None
    
    def list_objects(self, prefix: str = "", recursive: bool = True) -> list:
        """
        List objects di knowledge bucket.
        
        Args:
            prefix: Prefix untuk filter objects
            recursive: Whether to list recursively
            
        Returns:
            List of object information dictionaries
        """
        full_prefix = f"{self.config.knowledge_prefix}{prefix}"
        
        objects = []
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(
                Bucket=self.config.bucket_name,
                Prefix=full_prefix,
                Delimiter='' if recursive else '/'
            ):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        # Remove knowledge prefix dari key
                        relative_key = obj['Key'].replace(self.config.knowledge_prefix, '')
                        objects.append({
                            'key': relative_key,
                            'size': obj['Size'],
                            'last_modified': obj['LastModified'],
                            'etag': obj['ETag']
                        })
                        
        except Exception as e:
            print(f"Error listing objects: {e}")
        
        return objects
    
    def upload_object(self, key: str, content: bytes, metadata: dict = None):
        """
        Upload object ke MinIO AIStor.
        
        Args:
            key: Object key (relatif terhadap knowledge prefix)
            content: Content to upload
            metadata: Optional metadata dictionary
        """
        full_key = f"{self.config.knowledge_prefix}{key}"
        
        extra_args = {}
        if metadata:
            for meta_key, meta_value in metadata.items():
                extra_args[f'Metadata-{meta_key}'] = str(meta_value)
        
        try:
            self.s3_client.put_object(
                Bucket=self.config.bucket_name,
                Key=full_key,
                Body=content,
                ExtraArgs=extra_args
            )
            
            # Invalidate cache
            cache_key = self._get_cache_key(full_key)
            if cache_key in self.cache:
                del self.cache[cache_key]
                
        except Exception as e:
            print(f"Error uploading object {full_key}: {e}")
            raise
    
    def _get_cache_key(self, full_key: str) -> str:
        """Generate cache key untuk object."""
        import hashlib
        return hashlib.md5(full_key.encode()).hexdigest()
    
    def _cache_object(self, full_key: str, content: bytes, metadata: dict):
        """Cache object dengan timestamp."""
        import time
        cache_key = self._get_cache_key(full_key)
        self.cache[cache_key] = {
            'content': content,
            'metadata': metadata,
            'timestamp': time.time()
        }
    
    def cleanup_cache(self):
        """Cleanup expired cache entries."""
        import time
        current_time = time.time()
        expired_keys = []
        
        for cache_key, cache_data in self.cache.items():
            if current_time - cache_data['timestamp'] > self.config.cache_ttl_seconds:
                expired_keys.append(cache_key)
        
        for key in expired_keys:
            del self.cache[key]
        
        print(f"Cleaned up {len(expired_keys)} expired cache entries")


# Global client instance
_minio_client: Optional[MinIOClient] = None


def get_minio_client() -> MinIOClient:
    """
    Get global MinIO AIStor client instance.
    
    Returns:
        MinIO AIStor client instance
    """
    global _minio_client
    
    if _minio_client is None:
        config = MinIOConfig.from_env()
        _minio_client = MinIOClient(config)
    
    return _minio_client


def reset_minio_client():
    """Reset global MinIO AIStor client instance (untuk testing)."""
    global _minio_client
    _minio_client = None