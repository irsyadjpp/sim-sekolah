"""
Distributed tracing for AI Platform services

This module provides distributed tracing functionality using OpenTelemetry-like concepts.
"""

import time
import uuid
import threading
from typing import Dict, Optional, List, Any, Callable
from dataclasses import dataclass, field
from contextlib import contextmanager
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SpanKind(Enum):
    """Span kinds for different types of operations."""
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"
    INTERNAL = "INTERNAL"


@dataclass
class Span:
    """
    Represents a single span in a distributed trace.
    
    A span represents a single operation within a trace and contains
    timing information, metadata, and relationships to other spans.
    """
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    name: str = ""
    kind: SpanKind = SpanKind.INTERNAL
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: str = "ok"
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    links: List[Dict[str, str]] = field(default_factory=list)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.end()
        if exc_type is not None:
            self.record_exception(exc_type, exc_val, exc_tb)
    
    def set_attribute(self, key: str, value: Any):
        """Set an attribute on the span."""
        self.attributes[key] = value
    
    def set_attributes(self, attributes: Dict[str, Any]):
        """Set multiple attributes on the span."""
        self.attributes.update(attributes)
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Add an event to the span."""
        event = {
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {}
        }
        self.events.append(event)
    
    def record_exception(self, exc_type, exc_val, exc_tb):
        """Record an exception on the span."""
        self.status = "error"
        self.add_event(
            "exception",
            {
                "type": str(exc_type),
                "message": str(exc_val),
                "stack": str(exc_tb) if exc_tb else None
            }
        )
    
    def end(self, end_time: Optional[float] = None):
        """End the span."""
        if self.end_time is None:
            self.end_time = end_time or time.time()
    
    def duration(self) -> float:
        """Get span duration in seconds."""
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary for serialization."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "name": self.name,
            "kind": self.kind.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration(),
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
            "links": self.links
        }


class Tracer:
    """
    Distributed tracer for creating and managing spans.
    
    This class provides functionality to create spans, manage trace context,
    and export trace data.
    """
    
    def __init__(self, service_name: str):
        """
        Initialize tracer.
        
        Args:
            service_name: Name of the service
        """
        self.service_name = service_name
        self._current_span: Optional[Span] = None
        self._spans: Dict[str, Span] = {}
        self.lock = threading.Lock()
    
    def start_span(
        self,
        name: str,
        parent_span: Optional[Span] = None,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Span:
        """
        Start a new span.
        
        Args:
            name: Span name
            parent_span: Optional parent span
            kind: Span kind
            attributes: Optional initial attributes
            
        Returns:
            New span instance
        """
        trace_id = parent_span.trace_id if parent_span else str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        parent_span_id = parent_span.span_id if parent_span else None
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            kind=kind
        )
        
        if attributes:
            span.set_attributes(attributes)
        
        # Add service name attribute
        span.set_attribute("service.name", self.service_name)
        
        with self.lock:
            self._spans[span_id] = span
            self._current_span = span
        
        return span
    
    @contextmanager
    def span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """
        Context manager for creating a span.
        
        Args:
            name: Span name
            kind: Span kind
            attributes: Optional initial attributes
            
        Yields:
            Span instance
        """
        parent_span = self._current_span
        span = self.start_span(name, parent_span, kind, attributes)
        
        try:
            yield span
        except Exception as e:
            span.record_exception(type(e), e, e.__traceback__)
            raise
        finally:
            span.end()
            with self.lock:
                if self._current_span == span:
                    self._current_span = parent_span
    
    def current_span(self) -> Optional[Span]:
        """Get the current active span."""
        return self._current_span
    
    def get_span(self, span_id: str) -> Optional[Span]:
        """Get a span by ID."""
        with self.lock:
            return self._spans.get(span_id)
    
    def get_trace_spans(self, trace_id: str) -> List[Span]:
        """Get all spans in a trace."""
        with self.lock:
            return [
                span for span in self._spans.values()
                if span.trace_id == trace_id
            ]
    
    def get_all_spans(self) -> List[Span]:
        """Get all spans."""
        with self.lock:
            return list(self._spans.values())
    
    def export_spans(self) -> List[Dict[str, Any]]:
        """Export all spans as dictionaries."""
        with self.lock:
            return [span.to_dict() for span in self._spans.values()]
    
    def clear_spans(self):
        """Clear all spans."""
        with self.lock:
            self._spans.clear()
            self._current_span = None
    
    def get_trace_summary(self, trace_id: str) -> Dict[str, Any]:
        """
        Get summary of a trace.
        
        Args:
            trace_id: Trace ID
            
        Returns:
            Trace summary dictionary
        """
        spans = self.get_trace_spans(trace_id)
        if not spans:
            return {}
        
        # Calculate trace duration
        start_time = min(span.start_time for span in spans)
        end_time = max(span.end_time or span.start_time for span in spans)
        duration = end_time - start_time
        
        # Count spans by status
        status_counts = {}
        for span in spans:
            status_counts[span.status] = status_counts.get(span.status, 0) + 1
        
        return {
            "trace_id": trace_id,
            "span_count": len(spans),
            "duration": duration,
            "start_time": start_time,
            "end_time": end_time,
            "status_counts": status_counts,
            "service": self.service_name
        }


def trace_function(tracer: Optional[Tracer] = None, name: Optional[str] = None):
    """
    Decorator to trace function calls.
    
    Args:
        tracer: Optional tracer instance
        name: Optional span name (defaults to function name)
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            _tracer = tracer or get_tracer()
            _name = name or f"{func.__module__}.{func.__name__}"
            
            with _tracer.span(_name, SpanKind.INTERNAL):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# Global tracer instance
_global_tracer: Optional[Tracer] = None


def get_tracer(service_name: str = "ai-platform") -> Tracer:
    """
    Get or create the global tracer.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Tracer instance
    """
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer(service_name)
    return _global_tracer


def propagate_trace_context(span: Span) -> Dict[str, str]:
    """
    Extract trace context for propagation.
    
    Args:
        span: Span to extract context from
        
    Returns:
        Dictionary of trace context headers
    """
    return {
        "trace-id": span.trace_id,
        "span-id": span.span_id,
        "parent-span-id": span.parent_span_id or ""
    }


def extract_trace_context(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Extract trace context from headers.
    
    Args:
        headers: HTTP headers or similar
        
    Returns:
        Dictionary of trace context
    """
    return {
        "trace_id": headers.get("trace-id", ""),
        "span_id": headers.get("span-id", ""),
        "parent_span_id": headers.get("parent-span-id", "")
    }