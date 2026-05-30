"""
Error handling middleware for AI Platform services

This module provides centralized error handling and exception processing.
"""

import traceback
import uuid
from typing import Callable, Awaitable, Dict, Any, Optional
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from common.logging import get_logger

logger = get_logger(__name__)


class APIError(Exception):
    """Base API error class."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize API error.
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Application-specific error code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(APIError):
    """Validation error (400)."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details
        )


class NotFoundError(APIError):
    """Not found error (404)."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            details=details
        )


class ConflictError(APIError):
    """Conflict error (409)."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            details=details
        )


class RateLimitError(APIError):
    """Rate limit error (429)."""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details
        )


class ErrorMiddleware:
    """
    Centralized error handling middleware.
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize error middleware.
        
        Args:
            debug: Whether to include debug information in error responses
        """
        self.debug = debug
    
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process request with error handling.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            Response from next handler or error response
        """
        request_id = str(uuid.uuid4())
        
        try:
            response = await call_next(request)
            return response
            
        except HTTPException as e:
            # FastAPI HTTP exceptions
            return self._create_error_response(
                request_id=request_id,
                status_code=e.status_code,
                error_code="HTTP_ERROR",
                message=e.detail,
                details={"path": str(request.url.path)}
            )
            
        except APIError as e:
            # Custom API errors
            return self._create_error_response(
                request_id=request_id,
                status_code=e.status_code,
                error_code=e.error_code,
                message=e.message,
                details=e.details
            )
            
        except ValueError as e:
            # Validation errors
            return self._create_error_response(
                request_id=request_id,
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="VALIDATION_ERROR",
                message=str(e),
                details={"path": str(request.url.path)}
            )
            
        except KeyError as e:
            # Missing required fields
            return self._create_error_response(
                request_id=request_id,
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="MISSING_FIELD",
                message=f"Missing required field: {str(e)}",
                details={"path": str(request.url.path)}
            )
            
        except Exception as e:
            # Unexpected errors
            logger.error(
                f"Unexpected error: {str(e)}",
                extra={
                    "request_id": request_id,
                    "error_type": type(e).__name__,
                    "path": str(request.url.path),
                    "traceback": traceback.format_exc() if self.debug else None
                }
            )
            
            return self._create_error_response(
                request_id=request_id,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code="INTERNAL_ERROR",
                message="An unexpected error occurred" if not self.debug else str(e),
                details={
                    "path": str(request.url.path),
                    "traceback": traceback.format_exc() if self.debug else None
                } if self.debug else None
            )
    
    def _create_error_response(
        self,
        request_id: str,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> JSONResponse:
        """
        Create standardized error response.
        
        Args:
            request_id: Request ID
            status_code: HTTP status code
            error_code: Application error code
            message: Error message
            details: Additional error details
            
        Returns:
            JSON response with error information
        """
        error_response = {
            "error": True,
            "error_code": error_code,
            "message": message,
            "request_id": request_id,
        }
        
        if details:
            error_response["details"] = details
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )


def handle_errors(error_mapping: Optional[Dict[type, tuple]] = None):
    """
    Decorator for handling specific exceptions in route handlers.
    
    Args:
        error_mapping: Dictionary mapping exception types to (status_code, error_code)
        
    Returns:
        Decorator function
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if error_mapping and type(e) in error_mapping:
                    status_code, error_code = error_mapping[type(e)]
                    raise APIError(
                        message=str(e),
                        status_code=status_code,
                        error_code=error_code
                    )
                raise
        return wrapper
    return decorator