"""
Performance monitoring for AI Platform services

This module provides performance tracking and monitoring capabilities.
"""

import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from collections import deque
import statistics
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Performance metric data point."""
    operation: str
    duration: float
    timestamp: float
    success: bool
    metadata: Dict = field(default_factory=dict)


class PerformanceMonitor:
    """
    Performance monitor for tracking operation performance.
    
    Tracks execution times, success rates, and provides statistics.
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize performance monitor.
        
        Args:
            max_history: Maximum number of metrics to keep in history
        """
        self.max_history = max_history
        self.metrics: Dict[str, deque] = {}
        self.lock = threading.Lock()
    
    def record_metric(
        self,
        operation: str,
        duration: float,
        success: bool = True,
        metadata: Optional[Dict] = None
    ):
        """
        Record a performance metric.
        
        Args:
            operation: Operation name
            duration: Duration in seconds
            success: Whether operation succeeded
            metadata: Optional metadata
        """
        metric = PerformanceMetric(
            operation=operation,
            duration=duration,
            timestamp=time.time(),
            success=success,
            metadata=metadata or {}
        )
        
        with self.lock:
            if operation not in self.metrics:
                self.metrics[operation] = deque(maxlen=self.max_history)
            
            self.metrics[operation].append(metric)
    
    def get_operation_stats(self, operation: str) -> Optional[Dict]:
        """
        Get statistics for a specific operation.
        
        Args:
            operation: Operation name
            
        Returns:
            Statistics dictionary or None if no data
        """
        with self.lock:
            if operation not in self.metrics or not self.metrics[operation]:
                return None
            
            metrics = list(self.metrics[operation])
            durations = [m.duration for m in metrics]
            successes = [m for m in metrics if m.success]
            
            return {
                "operation": operation,
                "count": len(metrics),
                "avg_duration": statistics.mean(durations),
                "min_duration": min(durations),
                "max_duration": max(durations),
                "median_duration": statistics.median(durations),
                "success_rate": len(successes) / len(metrics),
                "failure_count": len(metrics) - len(successes),
                "p95_duration": self._percentile(durations, 95),
                "p99_duration": self._percentile(durations, 99),
            }
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """
        Get statistics for all operations.
        
        Returns:
            Dictionary of operation names to statistics
        """
        with self.lock:
            return {
                operation: self.get_operation_stats(operation)
                for operation in self.metrics
            }
    
    def get_recent_metrics(self, operation: str, count: int = 10) -> List[PerformanceMetric]:
        """
        Get recent metrics for an operation.
        
        Args:
            operation: Operation name
            count: Number of recent metrics to return
            
        Returns:
            List of recent metrics
        """
        with self.lock:
            if operation not in self.metrics:
                return []
            
            return list(self.metrics[operation])[-count:]
    
    def clear_metrics(self, operation: Optional[str] = None):
        """
        Clear metrics.
        
        Args:
            operation: Specific operation to clear, or None to clear all
        """
        with self.lock:
            if operation:
                if operation in self.metrics:
                    self.metrics[operation].clear()
            else:
                self.metrics.clear()
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


def track_performance(operation: str, monitor: Optional[PerformanceMonitor] = None):
    """
    Decorator to track function performance.
    
    Args:
        operation: Operation name
        monitor: Optional performance monitor
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            _monitor = monitor or get_performance_monitor()
            start_time = time.time()
            success = True
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                duration = time.time() - start_time
                _monitor.record_metric(
                    operation=operation,
                    duration=duration,
                    success=success,
                    metadata={"function": func.__name__}
                )
        return wrapper
    return decorator


class PerformanceContext:
    """Context manager for performance tracking."""
    
    def __init__(self, operation: str, monitor: Optional[PerformanceMonitor] = None, metadata: Optional[Dict] = None):
        """
        Initialize performance context.
        
        Args:
            operation: Operation name
            monitor: Optional performance monitor
            metadata: Optional metadata
        """
        self.operation = operation
        self.monitor = monitor or get_performance_monitor()
        self.metadata = metadata or {}
        self.start_time = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Record metric."""
        if self.start_time:
            duration = time.time() - self.start_time
            success = exc_type is None
            self.monitor.record_metric(
                operation=self.operation,
                duration=duration,
                success=success,
                metadata=self.metadata
            )
        return False


# Global performance monitor instance
_global_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """
    Get or create the global performance monitor.
    
    Returns:
        Performance monitor instance
    """
    global _global_performance_monitor
    if _global_performance_monitor is None:
        _global_performance_monitor = PerformanceMonitor()
    return _global_performance_monitor