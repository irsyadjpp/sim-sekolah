from typing import Optional, Any, Dict


class BaseException(Exception):
    """Base exception class"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(BaseException):
    """Authentication failed exception"""
    pass


class AuthorizationError(BaseException):
    """Authorization failed exception"""
    pass


class ValidationError(BaseException):
    """Validation error exception"""
    pass


class NotFoundError(BaseException):
    """Resource not found exception"""
    pass


class ConflictError(BaseException):
    """Resource conflict exception"""
    pass


class RateLimitError(BaseException):
    """Rate limit exceeded exception"""
    pass


class ServiceUnavailableError(BaseException):
    """Service unavailable exception"""
    pass


class DatabaseError(BaseException):
    """Database error exception"""
    pass


class ExternalServiceError(BaseException):
    """External service error exception"""
    pass


class ConfigurationError(BaseException):
    """Configuration error exception"""
    pass


class ProcessingError(BaseException):
    """Processing error exception"""
    pass


class FileUploadError(BaseException):
    """File upload error exception"""
    pass


class AIModelError(BaseException):
    """AI model error exception"""
    pass


class RetrievalError(BaseException):
    """Retrieval system error exception"""
    pass


class EmbeddingError(BaseException):
    """Embedding generation error exception"""
    pass


class ParsingError(BaseException):
    """Document parsing error exception"""
    pass


class ChunkingError(BaseException):
    """Semantic chunking error exception"""
    pass