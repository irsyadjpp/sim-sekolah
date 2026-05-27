"""
CORS middleware for AI Platform services

This module provides Cross-Origin Resource Sharing (CORS) middleware.
"""

from typing import Callable, Awaitable, List, Optional
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
import logging

logger = logging.getLogger(__name__)


class CORSMiddleware(FastAPICORSMiddleware):
    """
    Extended CORS middleware with additional features.
    
    This extends FastAPI's built-in CORS middleware with additional
    logging and configuration options.
    """
    
    def __init__(
        self,
        allow_origins: List[str] = ["*"],
        allow_credentials: bool = True,
        allow_methods: List[str] = ["*"],
        allow_headers: List[str] = ["*"],
        expose_headers: List[str] = [],
        max_age: int = 600,
        log_requests: bool = False
    ):
        """
        Initialize CORS middleware.
        
        Args:
            allow_origins: List of allowed origins
            allow_credentials: Whether to allow credentials
            allow_methods: List of allowed HTTP methods
            allow_headers: List of allowed headers
            expose_headers: List of headers to expose
            max_age: Maximum cache time for preflight requests
            log_requests: Whether to log CORS requests
        """
        self.log_requests = log_requests
        
        super().__init__(
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            expose_headers=expose_headers,
            max_age=max_age
        )
        
        logger.info(
            f"CORS middleware initialized",
            extra={
                "allow_origins": allow_origins,
                "allow_credentials": allow_credentials,
                "allow_methods": allow_methods,
                "allow_headers": allow_headers
            }
        )
    
    async def preflight_response(self, request: Request, call_next: Callable) -> Response:
        """
        Handle preflight OPTIONS requests.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            CORS preflight response
        """
        if self.log_requests:
            logger.info(
                f"CORS preflight request",
                extra={
                    "method": request.method,
                    "origin": request.headers.get("origin"),
                    "access_control_request_method": request.headers.get("access-control-request-method"),
                    "access_control_request_headers": request.headers.get("access-control-request-headers")
                }
            )
        
        return await super().preflight_response(request, call_next)
    
    async def simple_response(self, request: Request, call_next: Callable) -> Response:
        """
        Handle simple requests with CORS headers.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            Response with CORS headers
        """
        if self.log_requests:
            logger.debug(
                f"CORS simple request",
                extra={
                    "method": request.method,
                    "origin": request.headers.get("origin")
                }
            )
        
        return await super().simple_response(request, call_next)


def get_cors_middleware(
    environment: str = "development",
    custom_origins: Optional[List[str]] = None
) -> CORSMiddleware:
    """
    Get CORS middleware configuration based on environment.
    
    Args:
        environment: Environment name (development, staging, production)
        custom_origins: Optional custom allowed origins
        
    Returns:
        Configured CORS middleware
    """
    if environment == "production":
        # Strict CORS for production
        allow_origins = custom_origins or [
            "https://api.simsekolah.com",
            "https://simsekolah.com"
        ]
        allow_credentials = True
        log_requests = True
    elif environment == "staging":
        # Moderate CORS for staging
        allow_origins = custom_origins or [
            "https://staging.simsekolah.com",
            "https://api-staging.simsekolah.com"
        ]
        allow_credentials = True
        log_requests = True
    else:
        # Permissive CORS for development
        allow_origins = ["*"]
        allow_credentials = True
        log_requests = False
    
    return CORSMiddleware(
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Total-Count", "X-Page-Count"],
        max_age=600,
        log_requests=log_requests
    )