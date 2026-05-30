"""
gRPC Channel Management for AI Platform

This module provides channel creation and management utilities with built-in
retry logic, authentication, timeout configuration, and connection pooling.
"""

import grpc
from grpc import aio as grpc_aio
from typing import Optional, Dict, Any, Callable
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


class ChannelConfig:
    """Configuration for gRPC channels."""
    
    def __init__(
        self,
        target: str,
        max_receive_message_length: int = 4 * 1024 * 1024,  # 4MB
        max_send_message_length: int = 4 * 1024 * 1024,  # 4MB
        keepalive_time_ms: int = 30000,  # 30 seconds
        keepalive_timeout_ms: int = 5000,  # 5 seconds
        keepalive_permit_without_calls: bool = True,
        enable_retry: bool = True,
        max_retry_attempts: int = 3,
        initial_backoff_ms: int = 100,
        max_backoff_ms: int = 5000,
    ):
        self.target = target
        self.max_receive_message_length = max_receive_message_length
        self.max_send_message_length = max_send_message_length
        self.keepalive_time_ms = keepalive_time_ms
        self.keepalive_timeout_ms = keepalive_timeout_ms
        self.keepalive_permit_without_calls = keepalive_permit_without_calls
        self.enable_retry = enable_retry
        self.max_retry_attempts = max_retry_attempts
        self.initial_backoff_ms = initial_backoff_ms
        self.max_backoff_ms = max_backoff_ms


class AuthInterceptor(grpc_aio.ClientInterceptor):
    """Interceptor for adding authentication credentials to gRPC calls."""
    
    def __init__(self, token_provider: Callable[[], str]):
        """
        Initialize auth interceptor.
        
        Args:
            token_provider: Callable that returns the auth token
        """
        self._token_provider = token_provider
    
    async def _unary_unary(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-unary calls."""
        token = self._token_provider()
        metadata = (("authorization", f"Bearer {token}"),)
        
        new_details = grpc.ClientCallDetails(
            method=call_details.method,
            timeout=call_details.timeout,
            metadata=call_details.metadata + metadata if call_details.metadata else metadata,
            credentials=call_details.credentials,
        )
        
        return await method(request, new_details)
    
    async def _unary_stream(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-stream calls."""
        token = self._token_provider()
        metadata = (("authorization", f"Bearer {token}"),)
        
        new_details = grpc.ClientCallDetails(
            method=call_details.method,
            timeout=call_details.timeout,
            metadata=call_details.metadata + metadata if call_details.metadata else metadata,
            credentials=call_details.credentials,
        )
        
        return method(request, new_details)
    
    async def _stream_unary(
        self,
        method: Callable,
        request_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept stream-unary calls."""
        token = self._token_provider()
        metadata = (("authorization", f"Bearer {token}"),)
        
        new_details = grpc.ClientCallDetails(
            method=call_details.method,
            timeout=call_details.timeout,
            metadata=call_details.metadata + metadata if call_details.metadata else metadata,
            credentials=call_details.credentials,
        )
        
        return await method(request_iterator, new_details)
    
    async def _stream_stream(
        self,
        method: Callable,
        request_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept stream-stream calls."""
        token = self._token_provider()
        metadata = (("authorization", f"Bearer {token}"),)
        
        new_details = grpc.ClientCallDetails(
            method=call_details.method,
            timeout=call_details.timeout,
            metadata=call_details.metadata + metadata if call_details.metadata else metadata,
            credentials=call_details.credentials,
        )
        
        return method(request_iterator, new_details)
    
    def intercept_unary_unary(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-unary calls (sync version)."""
        return self._unary_unary(method, request, call_details)
    
    def intercept_unary_stream(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-stream calls (sync version)."""
        return self._unary_stream(method, request, call_details)
    
    def intercept_stream_unary(
        self,
        method: Callable,
        request_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept stream-unary calls (sync version)."""
        return self._stream_unary(method, request_iterator, call_details)
    
    def intercept_stream_stream(
        self,
        method: Callable,
        request_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept stream-stream calls (sync version)."""
        return self._stream_stream(method, request_iterator, call_details)


class TimeoutInterceptor(grpc_aio.ClientInterceptor):
    """Interceptor for adding default timeouts to gRPC calls."""
    
    def __init__(self, default_timeout: float = 30.0):
        """
        Initialize timeout interceptor.
        
        Args:
            default_timeout: Default timeout in seconds
        """
        self._default_timeout = default_timeout
    
    async def _unary_unary(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-unary calls."""
        if call_details.timeout is None:
            call_details = grpc.ClientCallDetails(
                method=call_details.method,
                timeout=self._default_timeout,
                metadata=call_details.metadata,
                credentials=call_details.credentials,
            )
        
        return await method(request, call_details)
    
    def intercept_unary_unary(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-unary calls (sync version)."""
        return self._unary_unary(method, request, call_details)


class LoggingInterceptor(grpc_aio.ClientInterceptor):
    """Interceptor for logging gRPC calls."""
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize logging interceptor.
        
        Args:
            logger: Logger instance (uses module logger if not provided)
        """
        self._logger = logger or logging.getLogger(__name__)
    
    async def _unary_unary(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-unary calls with logging."""
        self._logger.debug(f"gRPC call: {call_details.method}")
        
        try:
            response = await method(request, call_details)
            self._logger.debug(f"gRPC success: {call_details.method}")
            return response
        except Exception as e:
            self._logger.error(f"gRPC error: {call_details.method} - {str(e)}")
            raise
    
    def intercept_unary_unary(
        self,
        method: Callable,
        request: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        """Intercept unary-unary calls (sync version)."""
        return self._unary_unary(method, request, call_details)


class ChannelManager:
    """Manager for gRPC channel lifecycle."""
    
    def __init__(self, config: ChannelConfig):
        """
        Initialize channel manager.
        
        Args:
            config: Channel configuration
        """
        self._config = config
        self._channel: Optional[grpc_aio.Channel] = None
        self._lock = asyncio.Lock()
    
    async def get_channel(self) -> grpc_aio.Channel:
        """
        Get or create gRPC channel.
        
        Returns:
            gRPC channel
        """
        async with self._lock:
            if self._channel is None:
                self._channel = await self._create_channel()
            return self._channel
    
    async def _create_channel(self) -> grpc_aio.Channel:
        """
        Create new gRPC channel with configuration.
        
        Returns:
            New gRPC channel
        """
        options = [
            ("grpc.max_receive_message_length", self._config.max_receive_message_length),
            ("grpc.max_send_message_length", self._config.max_send_message_length),
            ("grpc.keepalive_time_ms", self._config.keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", self._config.keepalive_timeout_ms),
            ("grpc.keepalive_permit_without_calls", self._config.keepalive_permit_without_calls),
        ]
        
        if self._config.enable_retry:
            options.extend([
                ("grpc.enable_retry", 1),
                ("grpc.max_retry_attempts", self._config.max_retry_attempts),
                ("grpc.initial_backoff_ms", self._config.initial_backoff_ms),
                ("grpc.max_backoff_ms", self._config.max_backoff_ms),
            ])
        
        channel = grpc_aio.channel(self._config.target, options)
        logger.info(f"Created gRPC channel to {self._config.target}")
        return channel
    
    async def close(self):
        """Close the gRPC channel."""
        async with self._lock:
            if self._channel:
                await self._channel.close()
                self._channel = None
                logger.info(f"Closed gRPC channel to {self._config.target}")


def create_channel(
    target: str,
    auth_token: Optional[str] = None,
    token_provider: Optional[Callable[[], str]] = None,
    default_timeout: float = 30.0,
    enable_logging: bool = True,
    **kwargs
) -> grpc_aio.Channel:
    """
    Create a gRPC channel with common interceptors.
    
    Args:
        target: Target address (e.g., "localhost:50051")
        auth_token: Static auth token (deprecated, use token_provider)
        token_provider: Callable that returns auth token
        default_timeout: Default timeout in seconds
        enable_logging: Enable request logging
        **kwargs: Additional channel configuration
        
    Returns:
        Configured gRPC channel
    """
    config = ChannelConfig(target, **kwargs)
    
    interceptors = []
    
    # Add auth interceptor if token provider is given
    if token_provider:
        interceptors.append(AuthInterceptor(token_provider))
    elif auth_token:
        # Support static token for backwards compatibility
        interceptors.append(AuthInterceptor(lambda: auth_token))
    
    # Add timeout interceptor
    interceptors.append(TimeoutInterceptor(default_timeout))
    
    # Add logging interceptor
    if enable_logging:
        interceptors.append(LoggingInterceptor())
    
    # Create channel with interceptors
    channel = grpc_aio.channel(target, config=config, interceptors=interceptors)
    
    return channel


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(grpc.RpcError),
)
async def call_with_retry(
    method: Callable,
    *args,
    **kwargs
) -> Any:
    """
    Call a gRPC method with automatic retry logic.
    
    Args:
        method: gRPC method to call
        *args: Positional arguments for the method
        **kwargs: Keyword arguments for the method
        
    Returns:
        Method response
        
    Raises:
        grpc.RpcError: If all retry attempts fail
    """
    return await method(*args, **kwargs)