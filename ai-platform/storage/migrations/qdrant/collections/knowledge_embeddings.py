"""
Knowledge base embeddings collection schema for Qdrant
"""

from typing import Dict, Any
from qdrant_client.models import Distance, VectorParams, PayloadSchema


COLLECTION_NAME = "knowledge_embeddings"

COLLECTION_CONFIG = {
    "name": COLLECTION_NAME,
    "vectors": {
        "size": 1024,  # Default embedding dimension (adjust based on model)
        "distance": Distance.COSINE
    },
    "optimizers_config": {
        "default_segment_number": 2,
    },
    "replication_factor": 1,
    "write_consistency_factor": 1,
    "on_disk": True,
}

# Payload schema definition
PAYLOAD_SCHEMA = {
    "knowledge_id": "uuid",
    "title": "text",
    "content": "text",
    "category": "keyword",
    "difficulty": "keyword",
    "competency": "keyword",
    "taxonomy_path": "keyword",
    "version": "keyword",
    "created_at": "datetime",
    "updated_at": "datetime",
    "metadata": "json",
}

# Index configuration for efficient filtering
PAYLOAD_INDEXES = [
    {
        "field_name": "knowledge_id",
        "field_schema": PayloadSchema(type="keyword"),
    },
    {
        "field_name": "category",
        "field_schema": PayloadSchema(type="keyword"),
    },
    {
        "field_name": "difficulty",
        "field_schema": PayloadSchema(type="keyword"),
    },
    {
        "field_name": "competency",
        "field_schema": PayloadSchema(type="keyword"),
    },
    {
        "field_name": "taxonomy_path",
        "field_schema": PayloadSchema(type="keyword"),
    },
]

def get_collection_config(vector_size: int = 1024) -> Dict[str, Any]:
    """
    Get collection configuration with custom vector size.
    
    Args:
        vector_size: Embedding dimension size
        
    Returns:
        Collection configuration dictionary
    """
    config = COLLECTION_CONFIG.copy()
    config["vectors"]["size"] = vector_size
    return config

def get_vector_params(vector_size: int = 1024) -> VectorParams:
    """
    Get VectorParams for Qdrant collection creation.
    
    Args:
        vector_size: Embedding dimension size
        
    Returns:
        VectorParams object
    """
    return VectorParams(
        size=vector_size,
        distance=COLLECTION_CONFIG["vectors"]["distance"],
    )