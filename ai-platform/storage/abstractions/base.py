"""
Base storage backend abstraction
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class StorageType(Enum):
    """Storage backend types."""
    OBJECT = "object"      # S3, MinIO
    VECTOR = "vector"        # Qdrant, Pinecone, Weaviate
    RELATIONAL = "relational" # PostgreSQL, MySQL
    GRAPH = "graph"          # Neo4j, ArangoDB


@dataclass
class StorageConfig:
    """Configuration for storage backends."""
    
    # Connection settings
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    
    # SSL/TLS settings
    use_ssl: bool = False
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None
    
    # Performance settings
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    
    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Additional connection parameters
    extra_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.extra_params is None:
            self.extra_params = {}
    
    @classmethod
    def from_env(cls, prefix: str = "STORAGE_") -> "StorageConfig":
        """Create configuration from environment variables."""
        import os
        
        return cls(
            host=os.getenv(f"{prefix}HOST", "localhost"),
            port=int(os.getenv(f"{prefix}PORT", "5432")),
            username=os.getenv(f"{prefix}USERNAME"),
            password=os.getenv(f"{prefix}PASSWORD"),
            database=os.getenv(f"{prefix}DATABASE"),
            use_ssl=os.getenv(f"{prefix}USE_SSL", "false").lower() == "true",
            ssl_cert_path=os.getenv(f"{prefix}SSL_CERT_PATH"),
            ssl_key_path=os.getenv(f"{prefix}SSL_KEY_PATH"),
            pool_size=int(os.getenv(f"{prefix}POOL_SIZE", "10")),
            max_overflow=int(os.getenv(f"{prefix}MAX_OVERFLOW", "20")),
            pool_timeout=int(os.getenv(f"{prefix}POOL_TIMEOUT", "30")),
            max_retries=int(os.getenv(f"{prefix}MAX_RETRIES", "3")),
            retry_delay=float(os.getenv(f"{prefix}RETRY_DELAY", "1.0")),
        )


class StorageBackend(ABC):
    """
    Abstract base class for all storage backends.
    
    This provides a unified interface for different storage systems
    while allowing backend-specific optimizations.
    """
    
    def __init__(self, config: StorageConfig):
        """
        Initialize storage backend.
        
        Args:
            config: Storage configuration
        """
        self.config = config
        self._connection = None
        self._is_connected = False
    
    @abstractmethod
    async def connect(self) -> None:
        """
        Establish connection to storage backend.
        
        Raises:
            ConnectionError: If connection fails
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to storage backend."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Check if storage backend is healthy and accessible.
        
        Returns:
            Health check result with status and details
        """
        pass
    
    @abstractmethod
    async def ping(self) -> bool:
        """
        Simple ping to check connectivity.
        
        Returns:
            True if connected, False otherwise
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
    
    def __enter__(self):
        """Sync context manager entry."""
        # For sync contexts, we need to handle differently
        raise NotImplementedError("Use async context manager")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit."""
        raise NotImplementedError("Use async context manager")
    
    @property
    def is_connected(self) -> bool:
        """Check if backend is connected."""
        return self._is_connected