"""
Shared observability package for AI Platform services

This module provides centralized observability functionality including
metrics, tracing, and monitoring that can be used across all services.
"""

from .metrics import (
    MetricsCollector,
    Counter,
    Gauge,
    Histogram,
    get_metrics_collector,
)

from .tracing import (
    Tracer,
    Span,
    get_tracer,
    trace_function,
)

__all__ = [
    # Metrics
    "MetricsCollector",
    "Counter",
    "Gauge",
    "Histogram",
    "get_metrics_collector",
    
    # Tracing
    "Tracer",
    "Span",
    "get_tracer",
    "trace_function",
]