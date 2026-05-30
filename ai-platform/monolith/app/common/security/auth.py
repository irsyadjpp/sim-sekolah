"""
Authentication services for AI Platform

This module provides JWT-based authentication and token management.
"""

import jwt
import hashlib
import secrets
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TokenPayload:
    """JWT token payload."""
    user_id: str
    username: str
    role: str
    permissions: List[str]
    issued_at: datetime
    expires_at: datetime
    
    def to_dict(self) -> Dict:
        """Convert payload to dictionary."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "permissions": self.permissions,
            "iat": int(self.issued_at.timestamp()),
            "exp": int(self.expires_at.timestamp())
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TokenPayload':
        """Create payload from dictionary."""
        return cls(
            user_id=data["user_id"],
            username=data["username"],
            role=data["role"],
            permissions=data.get("permissions", []),
            issued_at=datetime.fromtimestamp(data["iat"]),
            expires_at=datetime.fromtimestamp(data["exp"])
        )


class TokenManager:
    """
    JWT token manager for creating and validating tokens.
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expiry_hours: int = 24):
        """
        Initialize token manager.
        
        Args:
            secret_key: Secret key for signing tokens
            algorithm: JWT algorithm
            token_expiry_hours: Token expiry time in hours
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_hours = token_expiry_hours
    
    def create_token(self, user_id: str, username: str, role: str, permissions: List[str]) -> str:
        """
        Create a JWT token.
        
        Args:
            user_id: User ID
            username: Username
            role: User role
            permissions: User permissions
            
        Returns:
            JWT token string
        """
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(hours=self.token_expiry_hours)
        
        payload = TokenPayload(
            user_id=user_id,
            username=username,
            role=role,
            permissions=permissions,
            issued_at=issued_at,
            expires_at=expires_at
        )
        
        token = jwt.encode(payload.to_dict(), self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[TokenPayload]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload.from_dict(payload)
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresh an expired token.
        
        Args:
            token: Expired JWT token
            
        Returns:
            New token if refresh successful, None otherwise
        """
        payload = self.verify_token(token)
        if payload is None:
            return None
        
        # Create new token with same user data
        return self.create_token(
            user_id=payload.user_id,
            username=payload.username,
            role=payload.role,
            permissions=payload.permissions
        )


class AuthService:
    """
    Authentication service for user authentication and authorization.
    """
    
    def __init__(self, token_manager: TokenManager):
        """
        Initialize auth service.
        
        Args:
            token_manager: Token manager instance
        """
        self.token_manager = token_manager
        self._active_sessions: Dict[str, Dict] = {}
    
    def authenticate(self, username: str, password: str, user_store: Dict) -> Optional[str]:
        """
        Authenticate a user with username and password.
        
        Args:
            username: Username
            password: Password
            user_store: User data store (dictionary of user_id -> user_data)
            
        Returns:
            JWT token if authentication successful, None otherwise
        """
        # Find user by username
        user_data = None
        for user_id, data in user_store.items():
            if data.get("username") == username:
                user_data = data
                break
        
        if not user_data:
            logger.warning(f"User not found: {username}")
            return None
        
        # Verify password (assuming password is hashed in user_store)
        from .encryption import verify_password
        if not verify_password(password, user_data.get("password_hash", "")):
            logger.warning(f"Invalid password for user: {username}")
            return None
        
        # Create token
        token = self.token_manager.create_token(
            user_id=user_id,
            username=username,
            role=user_data.get("role", "user"),
            permissions=user_data.get("permissions", [])
        )
        
        # Store session
        self._active_sessions[token] = {
            "user_id": user_id,
            "username": username,
            "created_at": datetime.utcnow()
        }
        
        return token
    
    def verify_token(self, token: str) -> Optional[TokenPayload]:
        """
        Verify a token and return payload.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload if valid, None otherwise
        """
        # Check if session is active
        if token not in self._active_sessions:
            logger.warning("Token not found in active sessions")
            return None
        
        payload = self.token_manager.verify_token(token)
        if payload is None:
            # Remove invalid session
            del self._active_sessions[token]
            return None
        
        return payload
    
    def logout(self, token: str) -> bool:
        """
        Logout a user by invalidating their token.
        
        Args:
            token: JWT token string
            
        Returns:
            True if logout successful
        """
        if token in self._active_sessions:
            del self._active_sessions[token]
            return True
        return False
    
    def get_active_sessions(self) -> List[Dict]:
        """
        Get all active sessions.
        
        Returns:
            List of active session data
        """
        return list(self._active_sessions.values())


# Global instances
_global_token_manager: Optional[TokenManager] = None
_global_auth_service: Optional[AuthService] = None


def get_token_manager(secret_key: Optional[str] = None) -> TokenManager:
    """
    Get or create the global token manager.
    
    Args:
        secret_key: Optional secret key (uses default if not provided)
        
    Returns:
        Token manager instance
    """
    global _global_token_manager
    if _global_token_manager is None:
        _secret_key = secret_key or secrets.token_urlsafe(32)
        _global_token_manager = TokenManager(_secret_key)
    return _global_token_manager


def get_auth_service(token_manager: Optional[TokenManager] = None) -> AuthService:
    """
    Get or create the global auth service.
    
    Args:
        token_manager: Optional token manager
        
    Returns:
        Auth service instance
    """
    global _global_auth_service
    if _global_auth_service is None:
        _token_manager = token_manager or get_token_manager()
        _global_auth_service = AuthService(_token_manager)
    return _global_auth_service


def generate_token(user_id: str, username: str, role: str, permissions: List[str]) -> str:
    """
    Generate a JWT token.
    
    Args:
        user_id: User ID
        username: Username
        role: User role
        permissions: User permissions
        
    Returns:
        JWT token string
    """
    token_manager = get_token_manager()
    return token_manager.create_token(user_id, username, role, permissions)


def verify_token(token: str) -> Optional[TokenPayload]:
    """
    Verify a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload if valid, None otherwise
    """
    auth_service = get_auth_service()
    return auth_service.verify_token(token)