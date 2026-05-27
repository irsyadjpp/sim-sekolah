"""
Base event definitions for AI Platform

This module contains base event classes and enums for event-driven communication.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class EventType(str, Enum):
    """Event types for the AI Platform."""
    
    # Document events
    DOCUMENT_UPLOADED = "document.uploaded"
    DOCUMENT_PROCESSED = "document.processed"
    DOCUMENT_FAILED = "document.failed"
    DOCUMENT_DELETED = "document.deleted"
    
    # Parsing events
    DOCUMENT_PARSED = "document.parsed"
    PARSE_FAILED = "parse.failed"
    
    # Chunking events
    DOCUMENT_CHUNKED = "document.chunked"
    CHUNK_FAILED = "chunk.failed"
    
    # Embedding events
    EMBEDDING_CREATED = "embedding.created"
    EMBEDDING_FAILED = "embedding.failed"
    EMBEDDING_BATCH_COMPLETED = "embedding.batch_completed"
    
    # Retrieval events
    QUERY_EXECUTED = "query.executed"
    RETRIEVAL_COMPLETED = "retrieval.completed"
    RETRIEVAL_FAILED = "retrieval.failed"
    
    # Generation events
    GENERATION_STARTED = "generation.started"
    GENERATION_COMPLETED = "generation.completed"
    GENERATION_FAILED = "generation.failed"
    
    # Moderation events
    MODERATION_CHECKED = "moderation.checked"
    MODERATION_FAILED = "moderation.failed"
    CONTENT_FLAGGED = "content.flagged"
    
    # Audit events
    AUDIT_LOG_CREATED = "audit.log_created"
    AUDIT_LOG_FAILED = "audit.log_failed"
    
    # System events
    SERVICE_HEALTH_CHECK = "system.health_check"
    SERVICE_STARTED = "service.started"
    SERVICE_STOPPED = "service.stopped"
    SERVICE_ERROR = "service.error"


class EventPriority(str, Enum):
    """Event priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class BaseEvent(BaseModel):
    """Base event class for all AI Platform events."""
    
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique event ID")
    event_type: EventType = Field(..., description="Type of the event")
    event_version: str = Field(default="1.0", description="Event schema version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    correlation_id: Optional[str] = Field(None, description="Correlation ID for tracing")
    causation_id: Optional[str] = Field(None, description="Causation ID for event chain")
    priority: EventPriority = Field(default=EventPriority.NORMAL, description="Event priority")
    source: str = Field(..., description="Event source service")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.uploaded",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "causation_id": None,
            "priority": "normal",
            "source": "parser-service",
            "data": {"document_id": "doc_123"},
            "metadata": {"user_id": "user_456"}
        }
    })


class DocumentEvent(BaseEvent):
    """Base class for document-related events."""
    
    document_id: str = Field(..., description="Document ID")
    user_id: Optional[str] = Field(None, description="User ID who owns the document")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.uploaded",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "causation_id": None,
            "priority": "normal",
            "source": "gateway-service",
            "document_id": "doc_123",
            "user_id": "user_456",
            "data": {"filename": "document.pdf"},
            "metadata": {}
        }
    })


class ProcessingEvent(BaseEvent):
    """Base class for processing-related events."""
    
    document_id: str = Field(..., description="Document ID being processed")
    processing_stage: str = Field(..., description="Current processing stage")
    status: str = Field(..., description="Processing status")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.parsed",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "causation_id": "evt_123",
            "priority": "normal",
            "source": "parser-service",
            "document_id": "doc_123",
            "processing_stage": "parsing",
            "status": "completed",
            "data": {"pages_processed": 10},
            "metadata": {"duration_ms": 1500}
        }
    })