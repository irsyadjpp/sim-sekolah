"""
Configuration management for SimSekolah AI SDK
"""

import os
from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for the AI SDK client."""
    
    # API Configuration
    api_key: str = Field(..., description="API key for authentication")
    base_url: str = Field(default="http://localhost:8002", description="Base URL for the API gateway")
    
    # Timeout Configuration
    timeout: float = Field(default=30.0, description="Request timeout in seconds")
    connect_timeout: float = Field(default=10.0, description="Connection timeout in seconds")
    
    # Retry Configuration
    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    retry_backoff_factor: float = Field(default=1.0, description="Backoff factor for retries")
    retry_status_codes: list = Field(
        default=[408, 429, 500, 502, 503, 504],
        description="HTTP status codes to retry"
    )
    
    # Circuit Breaker Configuration
    circuit_breaker_enabled: bool = Field(default=True, description="Enable circuit breaker")
    circuit_breaker_failure_threshold: int = Field(default=5, description="Failures before opening circuit")
    circuit_breaker_recovery_timeout: float = Field(default=60.0, description="Seconds to wait before trying again")
    
    # Connection Pool Configuration
    max_connections: int = Field(default=100, description="Maximum number of connections")
    max_keepalive_connections: int = Field(default=20, description="Maximum keepalive connections")
    
    # Logging Configuration
    enable_logging: bool = Field(default=True, description="Enable request logging")
    log_level: str = Field(default="INFO", description="Log level")
    
    # Advanced Configuration
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    user_agent: str = Field(default="simsekolah-ai-sdk/0.1.0", description="User agent string")
    
    class Config:
        env_prefix = "SIMSEKOLAH_AI_"
        env_file = ".env"
        extra = "ignore"
    
    @classmethod
    def from_env(cls) -> "Config:
        """Create configuration from environment variables."""
        return cls(
            api_key=os.getenv("SIMSEKOLAH_AI_API_KEY", ""),
            base_url=os.getenv("SIMSEKOLAH_AI_BASE_URL", "http://localhost:8002"),
            timeout=float(os.getenv("SIMSEKOLAH_AI_TIMEOUT", "30.0")),
            connect_timeout=float(os.getenv("SIMSEKOLAH_AI_CONNECT_TIMEOUT", "10.0")),
            max_retries=int(os.getenv("SIMSEKOLAH_AI_MAX_RETRIES", "3")),
            circuit_breaker_enabled=os.getenv("SIMSEKOLAH_AI_CIRCUIT_BREAKER_ENABLED", "true").lower() == "true",
            enable_logging=os.getenv("SIMSEKOLAH_AI_ENABLE_LOGGING", "true").lower() == "true",
        )