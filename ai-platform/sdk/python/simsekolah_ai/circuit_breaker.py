"""
Circuit breaker implementation for SimSekolah AI SDK
"""

import time
import asyncio
from enum import Enum
from typing import Callable, Optional, Any
from functools import wraps
import logging

from .exceptions import CircuitBreakerError

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Circuit is open, blocking requests
    HALF_OPEN = "half_open"  # Testing if service has recovered


class CircuitBreaker:
    """
    Circuit breaker implementation to prevent cascading failures.
    
    The circuit breaker has three states:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Service is failing, requests are blocked
    - HALF_OPEN: Testing if service has recovered
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Exception = Exception,
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before trying again
            expected_exception: Exception type that counts as failure
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self._failure_count = 0
        self._last_failure_time: Optional[float] = None
        self._state = CircuitState.CLOSED
        
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        if self._state != CircuitState.OPEN:
            return False
        
        if self._last_failure_time is None:
            return True
            
        return time.time() - self._last_failure_time >= self.recovery_timeout
    
    def _record_failure(self):
        """Record a failure and potentially open the circuit."""
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker opened after {self._failure_count} failures"
            )
    
    def _record_success(self):
        """Record a success and potentially close the circuit."""
        self._failure_count = 0
        self._last_failure_time = None
        
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            logger.info("Circuit breaker closed after successful test")
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is open
        """
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker moved to half-open state")
            else:
                raise CircuitBreakerError(
                    "Circuit breaker is open",
                    details={"retry_after": self.recovery_timeout}
                )
        
        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except self.expected_exception as e:
            self._record_failure()
            raise
    
    async def async_call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute an async function with circuit breaker protection.
        
        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is open
        """
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker moved to half-open state")
            else:
                raise CircuitBreakerError(
                    "Circuit breaker is open",
                    details={"retry_after": self.recovery_timeout}
                )
        
        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except self.expected_exception as e:
            self._record_failure()
            raise
    
    def get_state(self) -> CircuitState:
        """Get current circuit state."""
        return self._state
    
    def get_failure_count(self) -> int:
        """Get current failure count."""
        return self._failure_count
    
    def reset(self):
        """Manually reset the circuit breaker to closed state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        logger.info("Circuit breaker manually reset")


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    expected_exception: Exception = Exception,
):
    """
    Decorator to apply circuit breaker to a function.
    
    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before trying again
        expected_exception: Exception type that counts as failure
    """
    def decorator(func):
        breaker = CircuitBreaker(failure_threshold, recovery_timeout, expected_exception)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await breaker.async_call(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator