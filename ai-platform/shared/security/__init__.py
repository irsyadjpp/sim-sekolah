"""
Shared security utilities for AI Platform services

This module provides security functionality including authentication,
authorization, encryption, and token management.
"""

from .auth import (
    AuthService,
    TokenManager,
    get_auth_service,
    verify_token,
    generate_token,
)

from .encryption import (
    EncryptionService,
    get_encryption_service,
    encrypt_data,
    decrypt_data,
    hash_password,
    verify_password,
)

from .authorization import (
    Permission,
    Role,
    RoleManager,
    has_permission,
    require_permission,
)

__all__ = [
    # Authentication
    "AuthService",
    "TokenManager",
    "get_auth_service",
    "verify_token",
    "generate_token",
    
    # Encryption
    "EncryptionService",
    "get_encryption_service",
    "encrypt_data",
    "decrypt_data",
    "hash_password",
    "verify_password",
    
    # Authorization
    "Permission",
    "Role",
    "RoleManager",
    "has_permission",
    "require_permission",
]