"""
AI Platform Shared gRPC Module

This module provides shared gRPC utilities for AI Platform services including:
- Channel management with retry logic
- Authentication interceptors
- Timeout management
- Client factory for service connections
"""

from .channel import (
    ChannelConfig,
    ChannelManager,
    AuthInterceptor,
    TimeoutInterceptor,
    LoggingInterceptor,
    create_channel,
    call_with_retry,
)

from .client_factory import (
    ClientFactory,
    ServiceConfig,
    get_client_factory,
    create_service_client,
    close_all_connections,
)

__all__ = [
    # Channel management
    "ChannelConfig",
    "ChannelManager",
    "AuthInterceptor",
    "TimeoutInterceptor",
    "LoggingInterceptor",
    "create_channel",
    "call_with_retry",
    
    # Client factory
    "ClientFactory",
    "ServiceConfig",
    "get_client_factory",
    "create_service_client",
    "close_all_connections",
]

__version__ = "0.1.0"