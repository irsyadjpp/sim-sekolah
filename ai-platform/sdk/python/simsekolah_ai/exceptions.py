"""
Exception definitions for SimSekolah AI SDK
"""


class AIClientError(Exception):
    """Base exception for all AI SDK errors."""
    
    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(AIClientError):
    """Authentication or authorization error."""
    
    def __init__(self, message: str = "Authentication failed", details: dict = None):
        super().__init__(message, code="AUTHENTICATION_ERROR", details=details)


class RateLimitError(AIClientError):
    """Rate limit exceeded error."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None, details: dict = None):
        self.retry_after = retry_after
        details = details or {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(message, code="RATE_LIMIT_ERROR", details=details)


class ServiceUnavailableError(AIClientError):
    """Service unavailable error."""
    
    def __init__(self, message: str = "Service unavailable", details: dict = None):
        super().__init__(message, code="SERVICE_UNAVAILABLE", details=details)


class ValidationError(AIClientError):
    """Validation error for request parameters."""
    
    def __init__(self, message: str = "Validation failed", field: str = None, details: dict = None):
        details = details or {}
        if field:
            details["field"] = field
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class ConnectionError(AIClientError):
    """Connection error."""
    
    def __init__(self, message: str = "Connection failed", details: dict = None):
        super().__init__(message, code="CONNECTION_ERROR", details=details)


class TimeoutError(AIClientError):
    """Request timeout error."""
    
    def __init__(self, message: str = "Request timeout", timeout: float = None, details: dict = None):
        self.timeout = timeout
        details = details or {}
        if timeout:
            details["timeout"] = timeout
        super().__init__(message, code="TIMEOUT_ERROR", details=details)


class CircuitBreakerError(AIClientError):
    """Circuit breaker is open error."""
    
    def __init__(self, message: str = "Circuit breaker is open", service: str = None, details: dict = None):
        details = details or {}
        if service:
            details["service"] = service
        super().__init__(message, code="CIRCUIT_BREAKER_ERROR", details=details)