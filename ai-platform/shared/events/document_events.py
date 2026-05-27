"""
Document-specific event definitions for AI Platform

This module contains event definitions for document-related operations.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from .base import DocumentEvent, EventType, EventPriority


class DocumentUploadedEvent(DocumentEvent):
    """Event emitted when a document is uploaded."""
    
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of the file")
    storage_path: str = Field(..., description="Storage path/URL")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.uploaded",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "priority": "normal",
            "source": "gateway-service",
            "document_id": "doc_123",
            "user_id": "user_456",
            "filename": "document.pdf",
            "file_size": 1024000,
            "mime_type": "application/pdf",
            "storage_path": "s3://bucket/documents/doc_123.pdf",
            "data": {},
            "metadata": {}
        }
    })


class DocumentProcessedEvent(DocumentEvent):
    """Event emitted when document processing is completed."""
    
    processing_duration_ms: int = Field(..., description="Processing duration in milliseconds")
    pages_count: int = Field(..., description="Number of pages processed")
    chunks_count: int = Field(..., description="Number of chunks created")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.processed",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "causation_id": "evt_123",
            "priority": "normal",
            "source": "parser-service",
            "document_id": "doc_123",
            "user_id": "user_456",
            "processing_duration_ms": 5000,
            "pages_count": 10,
            "chunks_count": 25,
            "data": {},
            "metadata": {}
        }
    })


class DocumentFailedEvent(DocumentEvent):
    """Event emitted when document processing fails."""
    
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    failed_stage: str = Field(..., description="Stage where processing failed")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.failed",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "causation_id": "evt_123",
            "priority": "high",
            "source": "parser-service",
            "document_id": "doc_123",
            "user_id": "user_456",
            "error_code": "PARSE_ERROR",
            "error_message": "Failed to parse PDF file",
            "failed_stage": "parsing",
            "data": {},
            "metadata": {}
        }
    })


class DocumentDeletedEvent(DocumentEvent):
    """Event emitted when a document is deleted."""
    
    deletion_reason: Optional[str] = Field(None, description="Reason for deletion")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "evt_123456",
            "event_type": "document.deleted",
            "event_version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "correlation_id": "corr_789",
            "priority": "normal",
            "source": "gateway-service",
            "document_id": "doc_123",
            "user_id": "user_456",
            "deletion_reason": "User requested deletion",
            "data": {},
            "metadata": {}
        }
    })