"""
Object storage abstraction (S3/SeaweedFS/MinIO)
"""

from typing import Dict, Any, Optional, List, BinaryIO, Union
from pathlib import Path
from datetime import datetime
import hashlib

from .base import StorageBackend, StorageConfig


class ObjectStorage(StorageBackend):
    """
    Abstract object storage backend.
    
    Provides unified interface for S3-compatible object storage systems.
    """
    
    @abstractmethod
    async def upload_file(
        self,
        file_path: Union[str, Path, BinaryIO],
        bucket: str,
        object_key: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Upload a file to object storage.
        
        Args:
            file_path: Path to file or file-like object
            bucket: Bucket name
            object_key: Object key (path in bucket)
            metadata: Optional metadata to attach to object
            
        Returns:
            Object URL or identifier
        """
        pass
    
    @abstractmethod
    async def download_file(
        self,
        bucket: str,
        object_key: str,
        local_path: Union[str, Path],
    ) -> str:
        """
        Download a file from object storage.
        
        Args:
            bucket: Bucket name
            object_key: Object key
            local_path: Local path to save file
            
        Returns:
            Path to downloaded file
        """
        pass
    
    @abstractmethod
    async def delete_file(
        self,
        bucket: str,
        object_key: str,
    ) -> bool:
        """
        Delete a file from object storage.
        
        Args:
            bucket: Bucket name
            object_key: Object key
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def file_exists(
        self,
        bucket: str,
        object_key: str,
    ) -> bool:
        """
        Check if file exists in object storage.
        
        Args:
            bucket: Bucket name
            object_key: Object key
            
        Returns:
            True if file exists
        """
        pass
    
    @abstractmethod
    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        limit: int = 1000,
    ) -> List[Dict[str, Any]]:
        """
        List files in bucket with optional prefix filter.
        
        Args:
            bucket: Bucket name
            prefix: Prefix to filter files
            limit: Maximum number of files to return
            
        Returns:
            List of file information dictionaries
        """
        pass
    
    @abstractmethod
    async def get_file_metadata(
        self,
        bucket: str,
        object_key: str,
    ) -> Dict[str, Any]:
        """
        Get metadata for a file.
        
        Args:
            bucket: Bucket name
            object_key: Object key
            
        Returns:
            File metadata dictionary
        """
        pass
    
    @abstractmethod
    async def generate_presigned_url(
        self,
        bucket: str,
        object_key: str,
        expiration: int = 3600,
    ) -> str:
        """
        Generate presigned URL for temporary access.
        
        Args:
            bucket: Bucket name
            object_key: Object key
            expiration: URL expiration time in seconds
            
        Returns:
            Presigned URL
        """
        pass


class S3Storage(ObjectStorage):
    """
    AWS S3 storage implementation.
    
    Provides S3-compatible object storage using boto3.
    """
    
    def __init__(self, config: StorageConfig):
        """
        Initialize S3 storage backend.
        
        Args:
            config: Storage configuration
        """
        super().__init__(config)
        self._client = None
    
    async def connect(self) -> None:
        """Establish S3 connection."""
        import boto3
        
        session_config = {
            "aws_access_key_id": self.config.username,
            "aws_secret_access_key": self.config.password,
            "region_name": self.config.extra_params.get("region", "us-east-1"),
        }
        
        if self.config.use_ssl:
            session_config["verify"] = self.config.extra_params.get("ca_bundle", True)
        
        session = boto3.Session(**session_config)
        self._client = session.client("s3", endpoint_url=self._get_endpoint())
        
        self._is_connected = True
    
    async def disconnect(self) -> None:
        """Close S3 connection."""
        if self._client:
            self._client.close()
            self._client = None
        self._is_connected = False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check S3 health."""
        try:
            # List buckets to verify connectivity
            buckets = await self._client.list_buckets()
            return {
                "status": "healthy",
                "backend": "s3",
                "buckets_count": len(buckets.get("Buckets", [])),
                "details": {"endpoint": self._get_endpoint()}
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "s3",
                "error": str(e)
            }
    
    async def ping(self) -> bool:
        """Ping S3 backend."""
        try:
            self._client.head_bucket(Bucket="ping")
            return True
        except:
            return False
    
    def _get_endpoint(self) -> str:
        """Get S3 endpoint URL."""
        if self.config.extra_params.get("endpoint"):
            return self.config.extra_params["endpoint"]
        return f"https://s3.{self.config.extra_params.get('region', 'us-east-1')}.amazonaws.com"
    
    async def upload_file(
        self,
        file_path: Union[str, Path, BinaryIO],
        bucket: str,
        object_key: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Upload file to S3."""
        if isinstance(file_path, (str, Path)):
            with open(file_path, "rb") as f:
                self._client.upload_fileobj(
                    Bucket=bucket,
                    Key=object_key,
                    Fileobj=f,
                    Metadata=metadata or {}
                )
        else:
            self._client.upload_fileobj(
                Bucket=bucket,
                Key=object_key,
                Fileobj=file_path,
                Metadata=metadata or {}
            )
        
        return f"s3://{bucket}/{object_key}"
    
    async def download_file(
        self,
        bucket: str,
        object_key: str,
        local_path: Union[str, Path],
    ) -> str:
        """Download file from S3."""
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._client.download_file(
            Bucket=bucket,
            Key=object_key,
            Filename=str(local_path)
        )
        
        return str(local_path)
    
    async def delete_file(self, bucket: str, object_key: str) -> bool:
        """Delete file from S3."""
        self._client.delete_object(Bucket=bucket, Key=object_key)
        return True
    
    async def file_exists(self, bucket: str, object_key: str) -> bool:
        """Check if file exists in S3."""
        try:
            self._client.head_object(Bucket=bucket, Key=object_key)
            return True
        except:
            return False
    
    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        limit: int = 1000,
    ) -> List[Dict[str, Any]]:
        """List files in S3 bucket."""
        paginator = self._client.get_paginator("list_objects_v2")
        result = []
        
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", [])[:limit]:
                result.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"],
                    "etag": obj["ETag"].strip('"'),
                })
                
                if len(result) >= limit:
                    break
                    
        return result
    
    async def get_file_metadata(
        self,
        bucket: str,
        object_key: str,
    ) -> Dict[str, Any]:
        """Get file metadata from S3."""
        response = self._client.head_object(Bucket=bucket, Key=object_key)
        return {
            "key": response["ResponseMetadata"]["HTTPHeaders"].get("x-amz-meta-custom", ""),
            "size": int(response["ResponseMetadata"]["HTTPHeaders"]["content-length"]),
            "last_modified": response["ResponseMetadata"]["HTTPHeaders"]["last-modified"],
            "etag": response["ETag"].strip('"'),
            "metadata": response.get("Metadata", {})
        }
    
    async def generate_presigned_url(
        self,
        bucket: str,
        object_key: str,
        expiration: int = 3600,
    ) -> str:
        """Generate presigned URL for S3."""
        return self._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": object_key},
            ExpiresIn=expiration
        )


class SeaweedFSStorage(ObjectStorage):
    """
    SeaweedFS storage implementation (S3-compatible).

    Provides SeaweedFS object storage using boto3 with SeaweedFS S3 gateway endpoint.
    """

    def __init__(self, config: StorageConfig):
        """
        Initialize SeaweedFS storage backend.

        Args:
            config: Storage configuration
        """
        super().__init__(config)
        self._client = None

    async def connect(self) -> None:
        """Establish SeaweedFS connection."""
        import boto3

        session_config = {
            "aws_access_key_id": self.config.username,
            "aws_secret_access_key": self.config.password,
            "region_name": self.config.extra_params.get("region", "us-east-1"),
        }

        # SeaweedFS typically doesn't use SSL for local development
        if not self.config.use_ssl:
            session_config["verify"] = False

        session = boto3.Session(**session_config)

        # Use custom SeaweedFS S3 gateway endpoint
        endpoint_url = f"{'https' if self.config.use_ssl else 'http'}://{self.config.host}:{self.config.port}"

        self._client = session.client("s3", endpoint_url=endpoint_url)
        self._is_connected = True

    async def disconnect(self) -> None:
        """Close SeaweedFS connection."""
        if self._client:
            self._client.close()
            self._client = None
        self._is_connected = False

    async def health_check(self) -> Dict[str, Any]:
        """Check SeaweedFS health."""
        try:
            # List buckets to verify connectivity
            buckets = await self._client.list_buckets()
            return {
                "status": "healthy",
                "backend": "seaweedfs",
                "buckets_count": len(buckets.get("Buckets", [])),
                "details": {"endpoint": f"{self.config.host}:{self.config.port}"}
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "seaweedfs",
                "error": str(e)
            }
    
    async def ping(self) -> bool:
        """Ping SeaweedFS backend."""
        try:
            self._client.head_bucket(Bucket="ping")
            return True
        except:
            return False

    async def upload_file(
        self,
        file_path: Union[str, Path, BinaryIO],
        bucket: str,
        object_key: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Upload file to SeaweedFS."""
        if isinstance(file_path, (str, Path)):
            with open(file_path, "rb") as f:
                self._client.upload_fileobj(
                    Bucket=bucket,
                    Key=object_key,
                    Fileobj=f,
                    Metadata=metadata or {}
                )
        else:
            self._client.upload_fileobj(
                Bucket=bucket,
                Key=object_key,
                Fileobj=file_path,
                Metadata=metadata or {}
            )

        return f"seaweedfs://{bucket}/{object_key}"

    async def download_file(
        self,
        bucket: str,
        object_key: str,
        local_path: Union[str, Path],
    ) -> str:
        """Download file from SeaweedFS."""
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        self._client.download_file(
            Bucket=bucket,
            Key=object_key,
            Filename=str(local_path)
        )

        return str(local_path)

    async def delete_file(self, bucket: str, object_key: str) -> bool:
        """Delete file from SeaweedFS."""
        self._client.delete_object(Bucket=bucket, Key=object_key)
        return True

    async def file_exists(self, bucket: str, object_key: str) -> bool:
        """Check if file exists in SeaweedFS."""
        try:
            self._client.head_object(Bucket=bucket, Key=object_key)
            return True
        except:
            return False

    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        limit: int = 1000,
    ) -> List[Dict[str, Any]]:
        """List files in SeaweedFS bucket."""
        paginator = self._client.get_paginator("list_objects_v2")
        result = []

        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", [])[:limit]:
                result.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"],
                    "etag": obj["ETag"].strip('"'),
                })

                if len(result) >= limit:
                    break

        return result

    async def get_file_metadata(
        self,
        bucket: str,
        object_key: str,
    ) -> Dict[str, Any]:
        """Get file metadata from SeaweedFS."""
        response = self._client.head_object(Bucket=bucket, Key=object_key)
        return {
            "key": response["ResponseMetadata"]["HTTPHeaders"].get("x-amz-meta-custom", ""),
            "size": int(response["ResponseMetadata"]["HTTPHeaders"]["content-length"]),
            "last_modified": response["ResponseMetadata"]["HTTPHeaders"]["last-modified"],
            "etag": response["ETag"].strip('"'),
            "metadata": response.get("Metadata", {})
        }
    
    async def generate_presigned_url(
        self,
        bucket: str,
        object_key: str,
        expiration: int = 3600,
    ) -> str:
        """Generate presigned URL for SeaweedFS."""
        return self._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": object_key},
            ExpiresIn=expiration
        )