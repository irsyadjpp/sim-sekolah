"""
SimSekolah AI Platform Python SDK

Main SDK package providing client access to AI Platform services.
"""

from simsekolah_ai.client import AIClient, AsyncAIClient
from simsekolah_ai.config import Config
from simsekolah_ai.exceptions import (
    AIClientError,
    AuthenticationError,
    RateLimitError,
    ServiceUnavailableError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "AIClient",
    "AsyncAIClient",
    "Config",
    "AIClientError",
    "AuthenticationError",
    "RateLimitError",
    "ServiceUnavailableError",
    "ValidationError",
]