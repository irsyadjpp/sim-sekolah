"""Shared logging configuration for AI Platform services"""

from .logger import (
    setup_logging,
    get_logger,
    JSONFormatter,
    ColoredFormatter,
    RequestContext,
    log_function_call,
    default_logger,
)

__all__ = [
    "setup_logging",
    "get_logger",
    "JSONFormatter",
    "ColoredFormatter",
    "RequestContext",
    "log_function_call",
    "default_logger",
]