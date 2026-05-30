"""
Storage Abstractions for AI Platform

This package provides unified interfaces for different storage backends:
- S3/SeaweedFS object storage
- Vector database (Qdrant)
- Graph database
- PostgreSQL database
"""

from .base import StorageBackend, StorageConfig
from .object_storage import ObjectStorage, S3Storage, SeaweedFSStorage
from .vector_db import VectorDB, QdrantDB
from .relational_db import RelationalDB, PostgreSQL
from .graph_db import GraphDB, Neo4jDB

__all__ = [
    # Base classes
    "StorageBackend",
    "StorageConfig",

    # Object storage
    "ObjectStorage",
    "S3Storage",
    "SeaweedFSStorage",

    # Vector database
    "VectorDB",
    "QdrantDB",

    # Relational database
    "RelationalDB",
    "PostgreSQL",

    # Graph database
    "GraphDB",
    "Neo4jDB",
]

__version__ = "0.1.0"