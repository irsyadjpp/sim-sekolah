"""
Common Pydantic schemas for AI Platform

This module contains shared Pydantic models and schemas used across multiple services.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List, Generic, TypeVar
from datetime import datetime
from enum import Enum


class Environment(str, Enum):
    """Environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Log levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DocumentFormat(str, Enum):
    """Document format types."""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    TXT = "txt"
    MD = "md"
    HTML = "html"
    PPTX = "pptx"
    XLSX = "xlsx"
    IMAGE = "image"


class DocumentStatus(str, Enum):
    """Document processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class ContentType(str, Enum):
    """Content types."""
    TEXT = "text"
    IMAGE = "image"
    TABLE = "table"
    FORMULA = "formula"
    CODE = "code"
    METADATA = "metadata"


class ChunkStrategy(str, Enum):
    """Chunk strategy types."""
    FIXED_SIZE = "fixed_size"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


class EmbeddingModel(str, Enum):
    """Embedding model types."""
    BGE_M3 = "bge_m3"
    BGE_SMALL = "bge_small"
    OPENAI_ADA = "openai_ada"
    OPENAI_SMALL = "openai_small"
    COHERE_EMBED = "cohere_embed"


class GenerationModel(str, Enum):
    """Generation model types."""
    GPT_4 = "gpt_4"
    GPT_35_TURBO = "gpt_35_turbo"
    CLAUDE_3_OPUS = "claude_3_opus"
    CLAUDE_3_SONNET = "claude_3_sonnet"
    CLAUDE_3_HAIKU = "claude_3_haiku"
    LLAMA_3_8B = "llama_3_8b"
    LLAMA_3_70B = "llama_3_70b"


class ModerationCategory(str, Enum):
    """Moderation categories."""
    VIOLENCE = "violence"
    SEXUAL = "sexual"
    HATE = "hate"
    HARASSMENT = "harassment"
    SELF_HARM = "self_harm"
    ILLEGAL = "illegal"
    MISINFORMATION = "misinformation"


class RetrievalMode(str, Enum):
    """Retrieval modes."""
    VECTOR = "vector"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    SEMANTIC = "semantic"


# Generic response wrapper
T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """Standard response wrapper."""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    data: Optional[T] = Field(None, description="Response data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "message": "Operation completed successfully",
            "data": {},
            "metadata": {}
        }
    })


class ErrorResponse(BaseModel):
    """Standard error response."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: List[str] = Field(default_factory=list, description="Error details")
    request_id: Optional[str] = Field(None, description="Request ID for tracing")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": ["Field 'email' is required"],
            "request_id": "req_123456",
            "metadata": {}
        }
    })


class PaginationRequest(BaseModel):
    """Pagination request parameters."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(None, description="Sort field")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "page": 1,
            "page_size": 10,
            "sort_by": "created_at",
            "sort_order": "desc"
        }
    })


class PaginationResponse(BaseModel):
    """Pagination response metadata."""
    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    current_page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "total_items": 100,
            "total_pages": 10,
            "current_page": 1,
            "page_size": 10,
            "has_next": True,
            "has_previous": False
        }
    })


class DocumentReference(BaseModel):
    """Reference to a document."""
    document_id: str = Field(..., description="Document ID")
    title: str = Field(..., description="Document title")
    source: str = Field(..., description="Document source")
    created_at: datetime = Field(..., description="Creation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "document_id": "doc_123",
            "title": "Sample Document",
            "source": "upload",
            "created_at": "2024-01-01T00:00:00Z",
            "metadata": {"author": "John Doe"}
        }
    })


class ChunkReference(BaseModel):
    """Reference to a document chunk."""
    chunk_id: str = Field(..., description="Chunk ID")
    document_id: str = Field(..., description="Parent document ID")
    chunk_index: int = Field(..., description="Chunk index in document")
    content_preview: str = Field(..., description="First 100 characters of content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "chunk_id": "chunk_456",
            "document_id": "doc_123",
            "chunk_index": 0,
            "content_preview": "This is the beginning of the document...",
            "metadata": {"page": 1}
        }
    })


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional health details")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "healthy",
            "version": "1.0.0",
            "details": {"database": "connected", "cache": "connected"}
        }
    })


class Metric(BaseModel):
    """Metric data point."""
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    labels: Dict[str, str] = Field(default_factory=dict, description="Metric labels")
    timestamp: datetime = Field(..., description="Metric timestamp")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "request_duration",
            "value": 0.123,
            "labels": {"endpoint": "/api/v1/embed"},
            "timestamp": "2024-01-01T00:00:00Z"
        }
    })