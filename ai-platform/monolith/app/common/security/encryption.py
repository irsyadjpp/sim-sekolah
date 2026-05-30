"""
Encryption services for AI Platform

This module provides encryption and hashing utilities for data security.
"""

import base64
import os
import secrets
from typing import Optional, Dict, Any
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import logging

logger = logging.getLogger(__name__)


class EncryptionService:
    """
    Encryption service for encrypting and decrypting data.
    
    Uses AES-256-GCM for symmetric encryption.
    """
    
    def __init__(self, encryption_key: Optional[bytes] = None):
        """
        Initialize encryption service.
        
        Args:
            encryption_key: Optional 32-byte encryption key (generated if not provided)
        """
        self.encryption_key = encryption_key or secrets.token_bytes(32)
        self.backend = default_backend()
    
    def encrypt(self, plaintext: str) -> Dict[str, str]:
        """
        Encrypt plaintext string.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Dictionary with encrypted data and nonce
        """
        # Generate nonce
        nonce = secrets.token_bytes(12)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(nonce),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Encrypt data
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        
        # Get authentication tag
        tag = encryptor.tag
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }
    
    def decrypt(self, encrypted_data: Dict[str, str]) -> str:
        """
        Decrypt encrypted data.
        
        Args:
            encrypted_data: Dictionary with ciphertext, nonce, and tag
            
        Returns:
            Decrypted plaintext string
        """
        try:
            # Decode base64
            ciphertext = base64.b64decode(encrypted_data["ciphertext"])
            nonce = base64.b64decode(encrypted_data["nonce"])
            tag = base64.b64decode(encrypted_data["tag"])
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.encryption_key),
                modes.GCM(nonce, tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # Decrypt data
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Decryption failed")
    
    def encrypt_bytes(self, data: bytes) -> Dict[str, str]:
        """
        Encrypt binary data.
        
        Args:
            data: Bytes to encrypt
            
        Returns:
            Dictionary with encrypted data and nonce
        """
        nonce = secrets.token_bytes(12)
        
        cipher = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(nonce),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(data) + encryptor.finalize()
        tag = encryptor.tag
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }
    
    def decrypt_bytes(self, encrypted_data: Dict[str, str]) -> bytes:
        """
        Decrypt binary data.
        
        Args:
            encrypted_data: Dictionary with ciphertext, nonce, and tag
            
        Returns:
            Decrypted bytes
        """
        try:
            ciphertext = base64.b64decode(encrypted_data["ciphertext"])
            nonce = base64.b64decode(encrypted_data["nonce"])
            tag = base64.b64decode(encrypted_data["tag"])
            
            cipher = Cipher(
                algorithms.AES(self.encryption_key),
                modes.GCM(nonce, tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Decryption failed")


class PasswordHasher:
    """
    Password hashing service using PBKDF2.
    """
    
    def __init__(self, salt_length: int = 16, iterations: int = 100000):
        """
        Initialize password hasher.
        
        Args:
            salt_length: Length of salt in bytes
            iterations: Number of PBKDF2 iterations
        """
        self.salt_length = salt_length
        self.iterations = iterations
        self.backend = default_backend()
    
    def hash(self, password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        """
        Hash a password.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dictionary with hashed password and salt
        """
        if salt is None:
            salt = secrets.token_bytes(self.salt_length)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        
        hashed_password = kdf.derive(password.encode('utf-8'))
        
        return {
            "hash": base64.b64encode(hashed_password).decode('utf-8'),
            "salt": base64.b64encode(salt).decode('utf-8'),
            "iterations": self.iterations
        }
    
    def verify(self, password: str, hashed_password: str, salt: str, iterations: int = 100000) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Password to verify
            hashed_password: Hashed password
            salt: Salt used for hashing
            iterations: Number of iterations used
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            salt_bytes = base64.b64decode(salt)
            hash_bytes = base64.b64decode(hashed_password)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt_bytes,
                iterations=iterations,
                backend=self.backend
            )
            
            attempted_hash = kdf.derive(password.encode('utf-8'))
            
            # Use constant-time comparison
            return secrets.compare_digest(attempted_hash, hash_bytes)
            
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False


# Global instances
_global_encryption_service: Optional[EncryptionService] = None
_global_password_hasher: Optional[PasswordHasher] = None


def get_encryption_service(encryption_key: Optional[bytes] = None) -> EncryptionService:
    """
    Get or create the global encryption service.
    
    Args:
        encryption_key: Optional encryption key
        
    Returns:
        Encryption service instance
    """
    global _global_encryption_service
    if _global_encryption_service is None:
        _global_encryption_service = EncryptionService(encryption_key)
    return _global_encryption_service


def get_password_hasher() -> PasswordHasher:
    """
    Get or create the global password hasher.
    
    Returns:
        Password hasher instance
    """
    global _global_password_hasher
    if _global_password_hasher is None:
        _global_password_hasher = PasswordHasher()
    return _global_password_hasher


def encrypt_data(plaintext: str, encryption_key: Optional[bytes] = None) -> Dict[str, str]:
    """
    Encrypt data.
    
    Args:
        plaintext: Text to encrypt
        encryption_key: Optional encryption key
        
    Returns:
        Encrypted data dictionary
    """
    service = get_encryption_service(encryption_key)
    return service.encrypt(plaintext)


def decrypt_data(encrypted_data: Dict[str, str], encryption_key: Optional[bytes] = None) -> str:
    """
    Decrypt data.
    
    Args:
        encrypted_data: Encrypted data dictionary
        encryption_key: Optional encryption key
        
    Returns:
        Decrypted plaintext
    """
    service = get_encryption_service(encryption_key)
    return service.decrypt(encrypted_data)


def hash_password(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
    """
    Hash a password.
    
    Args:
        password: Password to hash
        salt: Optional salt
        
    Returns:
        Hash dictionary
    """
    hasher = get_password_hasher()
    return hasher.hash(password, salt)


def verify_password(password: str, hashed_password: str, salt: str, iterations: int = 100000) -> bool:
    """
    Verify a password.
    
    Args:
        password: Password to verify
        hashed_password: Hashed password
        salt: Salt
        iterations: Iterations
        
    Returns:
        True if password matches
    """
    hasher = get_password_hasher()
    return hasher.verify(password, hashed_password, salt, iterations)