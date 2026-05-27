"""
Health check functionality for AI Platform services

This module provides health check capabilities for monitoring service health.
"""

import asyncio
from typing import Dict, List, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class HealthCheck:
    """Individual health check."""
    name: str
    status: HealthStatus
    message: str
    duration: float = 0.0
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "duration": self.duration,
            "metadata": self.metadata
        }


@dataclass
class HealthReport:
    """Overall health report."""
    status: HealthStatus
    checks: List[HealthCheck]
    timestamp: float
    service_name: str
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "status": self.status.value,
            "service": self.service_name,
            "version": self.version,
            "timestamp": self.timestamp,
            "checks": [check.to_dict() for check in self.checks],
            "check_count": len(self.checks),
            "healthy_count": sum(1 for c in self.checks if c.status == HealthStatus.HEALTHY),
            "degraded_count": sum(1 for c in self.checks if c.status == HealthStatus.DEGRADED),
            "unhealthy_count": sum(1 for c in self.checks if c.status == HealthStatus.UNHEALTHY)
        }


class HealthChecker:
    """
    Health checker for monitoring service health.
    
    Runs health checks and aggregates results into health reports.
    """
    
    def __init__(self, service_name: str = "ai-platform"):
        """
        Initialize health checker.
        
        Args:
            service_name: Name of the service
        """
        self.service_name = service_name
        self.checks: Dict[str, Callable[[], Awaitable[HealthCheck]]] = {}
    
    def register_check(self, name: str, check_func: Callable[[], Awaitable[HealthCheck]]):
        """
        Register a health check.
        
        Args:
            name: Check name
            check_func: Async function that performs the check
        """
        self.checks[name] = check_func
        logger.info(f"Registered health check: {name}")
    
    def remove_check(self, name: str) -> bool:
        """
        Remove a health check.
        
        Args:
            name: Check name
            
        Returns:
            True if check was removed
        """
        if name in self.checks:
            del self.checks[name]
            logger.info(f"Removed health check: {name}")
            return True
        return False
    
    async def run_check(self, name: str) -> HealthCheck:
        """
        Run a specific health check.
        
        Args:
            name: Check name
            
        Returns:
            Health check result
        """
        if name not in self.checks:
            return HealthCheck(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check '{name}' not found"
            )
        
        try:
            return await self.checks[name]()
        except Exception as e:
            logger.error(f"Health check '{name}' failed: {e}")
            return HealthCheck(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {str(e)}"
            )
    
    async def run_all_checks(self) -> HealthReport:
        """
        Run all registered health checks.
        
        Returns:
            Overall health report
        """
        import time
        start_time = time.time()
        
        # Run all checks concurrently
        tasks = [self.run_check(name) for name in self.checks.keys()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        checks = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                checks.append(HealthCheck(
                    name=list(self.checks.keys())[i],
                    status=HealthStatus.UNHEALTHY,
                    message=f"Check failed with exception: {str(result)}"
                ))
            else:
                checks.append(result)
        
        # Determine overall status
        if all(c.status == HealthStatus.HEALTHY for c in checks):
            overall_status = HealthStatus.HEALTHY
        elif any(c.status == HealthStatus.UNHEALTHY for c in checks):
            overall_status = HealthStatus.UNHEALTHY
        else:
            overall_status = HealthStatus.DEGRADED
        
        return HealthReport(
            status=overall_status,
            checks=checks,
            timestamp=start_time,
            service_name=self.service_name
        )
    
    async def quick_health(self) -> Dict[str, str]:
        """
        Quick health check (lightweight version).
        
        Returns:
            Simple health status dictionary
        """
        try:
            # Run a subset of critical checks
            critical_checks = [name for name in self.checks.keys() if "critical" in name.lower()]
            
            if critical_checks:
                tasks = [self.run_check(name) for name in critical_checks]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                if all(isinstance(r, HealthCheck) and r.status == HealthStatus.HEALTHY for r in results):
                    return {"status": "healthy"}
                else:
                    return {"status": "unhealthy"}
            else:
                # No critical checks, assume healthy if service is running
                return {"status": "healthy"}
                
        except Exception as e:
            logger.error(f"Quick health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}


def create_database_check(connection_func: Callable[[], Awaitable[bool]]) -> Callable[[], Awaitable[HealthCheck]]:
    """
    Create a database health check.
    
    Args:
        connection_func: Async function that tests database connection
        
    Returns:
        Health check function
    """
    async def check() -> HealthCheck:
        import time
        start_time = time.time()
        
        try:
            is_connected = await connection_func()
            duration = time.time() - start_time
            
            if is_connected:
                return HealthCheck(
                    name="database",
                    status=HealthStatus.HEALTHY,
                    message="Database connection successful",
                    duration=duration
                )
            else:
                return HealthCheck(
                    name="database",
                    status=HealthStatus.UNHEALTHY,
                    message="Database connection failed",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Database check failed: {str(e)}",
                duration=duration
            )
    
    return check


def create_cache_check(connection_func: Callable[[], Awaitable[bool]]) -> Callable[[], Awaitable[HealthCheck]]:
    """
    Create a cache health check.
    
    Args:
        connection_func: Async function that tests cache connection
        
    Returns:
        Health check function
    """
    async def check() -> HealthCheck:
        import time
        start_time = time.time()
        
        try:
            is_connected = await connection_func()
            duration = time.time() - start_time
            
            if is_connected:
                return HealthCheck(
                    name="cache",
                    status=HealthStatus.HEALTHY,
                    message="Cache connection successful",
                    duration=duration
                )
            else:
                return HealthCheck(
                    name="cache",
                    status=HealthStatus.DEGRADED,
                    message="Cache connection failed (degraded performance)",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return HealthCheck(
                name="cache",
                status=HealthStatus.DEGRADED,
                message=f"Cache check failed: {str(e)}",
                duration=duration
            )
    
    return check


def create_external_service_check(
    service_url: str,
    timeout: float = 5.0
) -> Callable[[], Awaitable[HealthCheck]]:
    """
    Create an external service health check.
    
    Args:
        service_url: URL of the service to check
        timeout: Request timeout in seconds
        
    Returns:
        Health check function
    """
    async def check() -> HealthCheck:
        import time
        import httpx
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(f"{service_url}/health")
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    return HealthCheck(
                        name=f"external_service_{service_url}",
                        status=HealthStatus.HEALTHY,
                        message="External service is healthy",
                        duration=duration,
                        metadata={"url": service_url, "status_code": response.status_code}
                    )
                else:
                    return HealthCheck(
                        name=f"external_service_{service_url}",
                        status=HealthStatus.UNHEALTHY,
                        message=f"External service returned status {response.status_code}",
                        duration=duration,
                        metadata={"url": service_url, "status_code": response.status_code}
                    )
        except Exception as e:
            duration = time.time() - start_time
            return HealthCheck(
                name=f"external_service_{service_url}",
                status=HealthStatus.UNHEALTHY,
                message=f"External service check failed: {str(e)}",
                duration=duration,
                metadata={"url": service_url}
            )
    
    return check


# Global health checker instance
_global_health_checker: Optional[HealthChecker] = None


def get_health_checker(service_name: str = "ai-platform") -> HealthChecker:
    """
    Get or create the global health checker.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Health checker instance
    """
    global _global_health_checker
    if _global_health_checker is None:
        _global_health_checker = HealthChecker(service_name)
    return _global_health_checker