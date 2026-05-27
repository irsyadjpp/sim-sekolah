"""
Qdrant collection schemas
"""

from .document_embeddings import (
    COLLECTION_NAME as DOCUMENT_EMBEDDINGS,
    get_collection_config as get_document_config,
    get_vector_params as get_document_params,
)
from .knowledge_embeddings import (
    COLLECTION_NAME as KNOWLEDGE_EMBEDDINGS,
    get_collection_config as get_knowledge_config,
    get_vector_params as get_knowledge_params,
)
from .conversation_embeddings import (
    COLLECTION_NAME as CONVERSATION_EMBEDDINGS,
    get_collection_config as get_conversation_config,
    get_vector_params as get_conversation_params,
)

__all__ = [
    "DOCUMENT_EMBEDDINGS",
    "KNOWLEDGE_EMBEDDINGS",
    "CONVERSATION_EMBEDDINGS",
    "get_document_config",
    "get_knowledge_config",
    "get_conversation_config",
    "get_document_params",
    "get_knowledge_params",
    "get_conversation_params",
]