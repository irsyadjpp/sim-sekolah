"""
Shared middleware for AI Platform services

This module provides common middleware components for request handling,
authentication, logging, and error handling.
"""

from .auth import AuthMiddleware
from .logging import LoggingMiddleware
from .error import ErrorMiddleware
from .cors import CORSMiddleware

__all__ = [
    "AuthMiddleware",
    "LoggingMiddleware",
    "ErrorMiddleware",
    "CORSMiddleware",
]