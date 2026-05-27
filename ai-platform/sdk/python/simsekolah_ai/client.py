"""
Main client implementation for SimSekolah AI SDK
"""

import logging
from typing import Optional, Dict, Any, List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import Config
from .exceptions import (
    AIClientError,
    AuthenticationError,
    RateLimitError,
    ServiceUnavailableError,
    ValidationError,
    ConnectionError,
    TimeoutError,
)
from .circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)


class AIClient:
    """
    Synchronous client for SimSekolah AI Platform.
    
    This client provides methods to interact with various AI Platform services
    with built-in authentication, retry logic, and circuit breaker protection.
    """
    
    def __init__(self, config: Optional[Config] = None, **kwargs):
        """
        Initialize the AI client.
        
        Args:
            config: Configuration object (created from kwargs if not provided)
            **kwargs: Configuration parameters (api_key, base_url, etc.)
        """
        if config is None:
            config = Config(**kwargs)
        
        self.config = config
        self._client = self._create_http_client()
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=config.circuit_breaker_failure_threshold,
            recovery_timeout=config.circuit_breaker_recovery_timeout,
            expected_exception=(httpx.HTTPError, ConnectionError),
        )
        
        logger.info(f"Initialized AI client for {config.base_url}")
    
    def _create_http_client(self) -> httpx.Client:
        """Create HTTP client with configuration."""
        return httpx.Client(
            base_url=self.config.base_url,
            timeout=httpx.Timeout(self.config.timeout, connect=self.config.connect_timeout),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "User-Agent": self.config.user_agent,
                "Content-Type": "application/json",
            },
            verify=self.config.verify_ssl,
            limits=httpx.Limits(
                max_connections=self.config.max_connections,
                max_keepalive_connections=self.config.max_keepalive_connections,
            ),
        )
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic and circuit breaker.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            AIClientError: On request failure
        """
        url = endpoint
        
        try:
            response = self._circuit_breaker.call(
                self._client.request,
                method=method,
                url=url,
                json=data,
                params=params,
            )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)
        except httpx.TimeoutException as e:
            raise TimeoutError(
                f"Request timeout: {str(e)}",
                timeout=self.config.timeout
            )
        except httpx.ConnectError as e:
            raise ConnectionError(f"Connection failed: {str(e)}")
        except Exception as e:
            raise AIClientError(f"Unexpected error: {str(e)}")
    
    def _handle_http_error(self, error: httpx.HTTPStatusError):
        """Handle HTTP status errors."""
        status_code = error.response.status_code
        
        try:
            error_data = error.response.json()
            message = error_data.get("message", "Request failed")
            code = error_data.get("code", f"HTTP_{status_code}")
            details = error_data.get("details", {})
        except:
            message = f"HTTP {status_code}: {error.response.text}"
            code = f"HTTP_{status_code}"
            details = {}
        
        if status_code == 401:
            raise AuthenticationError(message, details=details)
        elif status_code == 429:
            retry_after = error.response.headers.get("Retry-After")
            raise RateLimitError(message, retry_after=int(retry_after) if retry_after else None, details=details)
        elif status_code in (502, 503, 504):
            raise ServiceUnavailableError(message, details=details)
        elif status_code == 422:
            raise ValidationError(message, details=details)
        else:
            raise AIClientError(message, code=code, details=details)
    
    # Service-specific methods would go here
    # For now, I'll add placeholder methods
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the AI Platform services are healthy.
        
        Returns:
            Health check response
        """
        return self._make_request("GET", "/health")
    
    def close(self):
        """Close the HTTP client."""
        self._client.close()
        logger.info("AI client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class AsyncAIClient:
    """
    Asynchronous client for SimSekolah AI Platform.
    
    This client provides async methods to interact with AI Platform services
    with built-in authentication, retry logic, and circuit breaker protection.
    """
    
    def __init__(self, config: Optional[Config] = None, **kwargs):
        """
        Initialize the async AI client.
        
        Args:
            config: Configuration object (created from kwargs if not provided)
            **kwargs: Configuration parameters (api_key, base_url, etc.)
        """
        if config is None:
            config = Config(**kwargs)
        
        self.config = config
        self._client = self._create_http_client()
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=config.circuit_breaker_failure_threshold,
            recovery_timeout=config.circuit_breaker_recovery_timeout,
            expected_exception=(httpx.HTTPError, ConnectionError),
        )
        
        logger.info(f"Initialized async AI client for {config.base_url}")
    
    def _create_http_client(self) -> httpx.AsyncClient:
        """Create async HTTP client with configuration."""
        return httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=httpx.Timeout(self.config.timeout, connect=self.config.connect_timeout),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "User-Agent": self.config.user_agent,
                "Content-Type": "application/json",
            },
            verify=self.config.verify_ssl,
            limits=httpx.Limits(
                max_connections=self.config.max_connections,
                max_keepalive_connections=self.config.max_keepalive_connections,
            ),
        )
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make async HTTP request with retry logic and circuit breaker.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            AIClientError: On request failure
        """
        url = endpoint
        
        try:
            response = await self._circuit_breaker.async_call(
                self._client.request,
                method=method,
                url=url,
                json=data,
                params=params,
            )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)
        except httpx.TimeoutException as e:
            raise TimeoutError(
                f"Request timeout: {str(e)}",
                timeout=self.config.timeout
            )
        except httpx.ConnectError as e:
            raise ConnectionError(f"Connection failed: {str(e)}")
        except Exception as e:
            raise AIClientError(f"Unexpected error: {str(e)}")
    
    def _handle_http_error(self, error: httpx.HTTPStatusError):
        """Handle HTTP status errors."""
        status_code = error.response.status_code
        
        try:
            error_data = error.response.json()
            message = error_data.get("message", "Request failed")
            code = error_data.get("code", f"HTTP_{status_code}")
            details = error_data.get("details", {})
        except:
            message = f"HTTP {status_code}: {error.response.text}"
            code = f"HTTP_{status_code}"
            details = {}
        
        if status_code == 401:
            raise AuthenticationError(message, details=details)
        elif status_code == 429:
            retry_after = error.response.headers.get("Retry-After")
            raise RateLimitError(message, retry_after=int(retry_after) if retry_after else None, details=details)
        elif status_code in (502, 503, 504):
            raise ServiceUnavailableError(message, details=details)
        elif status_code == 422:
            raise ValidationError(message, details=details)
        else:
            raise AIClientError(message, code=code, details=details)
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check if the AI Platform services are healthy.
        
        Returns:
            Health check response
        """
        return await self._make_request("GET", "/health")
    
    async def close(self):
        """Close the async HTTP client."""
        await self._client.aclose()
        logger.info("Async AI client closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()