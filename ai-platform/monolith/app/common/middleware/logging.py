"""
Logging middleware for AI Platform services

This module provides request/response logging middleware.
"""

import time
import uuid
from typing import Callable, Awaitable
from fastapi import Request, Response
import logging

from common.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware:
    """
    Logging middleware for request/response logging.
    """
    
    def __init__(self, log_body: bool = False, log_headers: bool = False):
        """
        Initialize logging middleware.
        
        Args:
            log_body: Whether to log request/response bodies
            log_headers: Whether to log request/response headers
        """
        self.log_body = log_body
        self.log_headers = log_headers
    
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process request with logging.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            Response from next handler
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        
        logger.info(
            f"Incoming request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
                "path": request.url.path,
                "query_params": str(request.query_params) if request.query_params else None
            }
        )
        
        # Log headers if enabled
        if self.log_headers:
            logger.debug(
                f"Request headers",
                extra={
                    "request_id": request_id,
                    "headers": dict(request.headers)
                }
            )
        
        # Log body if enabled
        if self.log_body:
            try:
                body = await request.body()
                logger.debug(
                    f"Request body",
                    extra={
                        "request_id": request_id,
                        "body": body.decode('utf-8') if body else None
                    }
                )
            except Exception as e:
                logger.warning(
                    f"Failed to log request body: {e}",
                    extra={"request_id": request_id}
                )
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            logger.error(
                f"Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "duration": duration,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            raise
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration": duration,
                "user_id": getattr(request.state, "user_id", None)
            }
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Log response headers if enabled
        if self.log_headers:
            logger.debug(
                f"Response headers",
                extra={
                    "request_id": request_id,
                    "headers": dict(response.headers)
                }
            )
        
        return response


class RequestContextLog:
    """
    Context manager for request-specific logging context.
    """
    
    def __init__(self, request_id: str, user_id: Optional[str] = None):
        """
        Initialize request context.
        
        Args:
            request_id: Request ID
            user_id: Optional user ID
        """
        self.request_id = request_id
        self.user_id = user_id
        self.logger = get_logger(__name__)
    
    def __enter__(self):
        """Add context to log records."""
        # This would integrate with the logging system to add context
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Remove context from log records."""
        if exc_type is not None:
            self.logger.error(
                f"Request context error",
                extra={
                    "request_id": self.request_id,
                    "user_id": self.user_id,
                    "error": str(exc_val),
                    "error_type": exc_type.__name__
                }
            )
        return False