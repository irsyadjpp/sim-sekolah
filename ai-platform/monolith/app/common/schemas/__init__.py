"""
AI Platform Shared Schemas Module

This module provides shared Pydantic schemas for AI Platform services including:
- Common enums and types
- Standard response wrappers
- Pagination schemas
- Document and chunk references
- Health check schemas
"""

from .common import (
    Environment,
    LogLevel,
    DocumentFormat,
    DocumentStatus,
    ContentType,
    ChunkStrategy,
    EmbeddingModel,
    GenerationModel,
    ModerationCategory,
    RetrievalMode,
    Response,
    ErrorResponse,
    PaginationRequest,
    PaginationResponse,
    DocumentReference,
    ChunkReference,
    HealthCheckResponse,
    Metric,
)

__all__ = [
    # Enums
    "Environment",
    "LogLevel",
    "DocumentFormat",
    "DocumentStatus",
    "ContentType",
    "ChunkStrategy",
    "EmbeddingModel",
    "GenerationModel",
    "ModerationCategory",
    "RetrievalMode",
    
    # Response wrappers
    "Response",
    "ErrorResponse",
    
    # Pagination
    "PaginationRequest",
    "PaginationResponse",
    
    # References
    "DocumentReference",
    "ChunkReference",
    
    # Health & metrics
    "HealthCheckResponse",
    "Metric",
]

__version__ = "0.1.0"