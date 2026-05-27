"""
AI Platform Shared Events Module

This module provides shared event definitions for AI Platform services including:
- Base event classes and enums
- Document-specific events
- Event utilities for RabbitMQ integration
"""

from .base import (
    EventType,
    EventPriority,
    BaseEvent,
    DocumentEvent,
    ProcessingEvent,
)

from .document_events import (
    DocumentUploadedEvent,
    DocumentProcessedEvent,
    DocumentFailedEvent,
    DocumentDeletedEvent,
)

__all__ = [
    # Base types
    "EventType",
    "EventPriority",
    "BaseEvent",
    "DocumentEvent",
    "ProcessingEvent",
    
    # Document events
    "DocumentUploadedEvent",
    "DocumentProcessedEvent",
    "DocumentFailedEvent",
    "DocumentDeletedEvent",
]

__version__ = "0.1.0"