"""
Authentication middleware for AI Platform services

This module provides JWT-based authentication middleware.
"""

from typing import Optional, Callable, Awaitable
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from common.security.auth import get_auth_service, TokenPayload

logger = logging.getLogger(__name__)

security = HTTPBearer()


class AuthMiddleware:
    """
    Authentication middleware for validating JWT tokens.
    """
    
    def __init__(self, optional: bool = False):
        """
        Initialize auth middleware.
        
        Args:
            optional: Whether authentication is optional
        """
        self.optional = optional
        self.auth_service = get_auth_service()
    
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable]
    ):
        """
        Process request with authentication.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            Response from next handler
        """
        try:
            # Extract authorization header
            authorization = request.headers.get("Authorization")
            
            if not authorization:
                if self.optional:
                    return await call_next(request)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing authorization header"
                )
            
            # Extract token
            if not authorization.startswith("Bearer "):
                if self.optional:
                    return await call_next(request)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )
            
            token = authorization[7:]  # Remove "Bearer " prefix
            
            # Verify token
            payload = self.auth_service.verify_token(token)
            if not payload:
                if self.optional:
                    return await call_next(request)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            
            # Add user info to request state
            request.state.user_id = payload.user_id
            request.state.username = payload.username
            request.state.role = payload.role
            request.state.permissions = payload.permissions
            
            logger.debug(f"Authenticated user: {payload.username} ({payload.user_id})")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            if not self.optional:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Authentication error"
                )
        
        return await call_next(request)


def get_current_user(request: Request) -> TokenPayload:
    """
    Get current authenticated user from request.
    
    Args:
        request: FastAPI request
        
    Returns:
        Token payload with user info
        
    Raises:
        HTTPException: If user not authenticated
    """
    if not hasattr(request.state, "user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return TokenPayload(
        user_id=request.state.user_id,
        username=request.state.username,
        role=request.state.role,
        permissions=request.state.permissions,
        issued_at=None,  # Not available in request state
        expires_at=None  # Not available in request state
    )


def require_role(*roles: str):
    """
    Decorator to require specific user roles.
    
    Args:
        *roles: Required roles
        
    Returns:
        Decorator function
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            user = get_current_user(request)
            
            if user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required roles: {roles}"
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_permission(*permissions: str):
    """
    Decorator to require specific permissions.
    
    Args:
        *permissions: Required permissions
        
    Returns:
        Decorator function
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            user = get_current_user(request)
            
            user_permissions = set(user.permissions)
            required_permissions = set(permissions)
            
            if not required_permissions.issubset(user_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required: {permissions}"
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator