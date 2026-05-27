"""
Conversation embeddings collection schema for Qdrant
"""

from typing import Dict, Any
from qdrant_client.models import Distance, VectorParams, PayloadSchema


COLLECTION_NAME = "conversation_embeddings"

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
    "conversation_id": "uuid",
    "message_id": "uuid",
    "user_id": "uuid",
    "role": "keyword",  # user, assistant, system
    "content": "text",
    "turn_number": "integer",
    "created_at": "datetime",
    "metadata": "json",
}

# Index configuration for efficient filtering
PAYLOAD_INDEXES = [
    {
        "field_name": "conversation_id",
        "field_schema": PayloadSchema(type="keyword"),
    },
    {
        "field_name": "user_id",
        "field_schema": PayloadSchema(type="keyword"),
    },
    {
        "field_name": "role",
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