"""
Metrics collection for AI Platform services

This module provides metrics collection functionality using Prometheus-style metrics.
"""

import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    """Base metric class."""
    name: str
    description: str
    labels: Dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class CounterMetric(Metric):
    """Counter metric that can only increase."""
    value: float = 0.0
    
    def inc(self, amount: float = 1.0):
        """Increment counter by amount."""
        if amount < 0:
            raise ValueError("Counter can only be incremented by positive amounts")
        self.value += amount


@dataclass
class GaugeMetric(Metric):
    """Gauge metric that can go up or down."""
    value: float = 0.0
    
    def inc(self, amount: float = 1.0):
        """Increment gauge by amount."""
        self.value += amount
    
    def dec(self, amount: float = 1.0):
        """Decrement gauge by amount."""
        self.value -= amount
    
    def set(self, value: float):
        """Set gauge to specific value."""
        self.value = value


@dataclass
class HistogramMetric(Metric):
    """Histogram metric for tracking distributions."""
    buckets: List[float] = field(default_factory=lambda: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0])
    sample_count: int = 0
    sample_sum: float = 0.0
    bucket_counts: Dict[int, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize bucket counts."""
        for i in range(len(self.buckets) + 1):
            self.bucket_counts[i] = 0
    
    def observe(self, value: float):
        """Observe a value."""
        self.sample_count += 1
        self.sample_sum += value
        
        # Find appropriate bucket
        for i, bucket in enumerate(self.buckets):
            if value <= bucket:
                self.bucket_counts[i] += 1
                return
        
        # Value exceeds all buckets
        self.bucket_counts[len(self.buckets)] += 1


class MetricsCollector:
    """
    Centralized metrics collector for services.
    
    This class provides a thread-safe way to collect and manage metrics
    across a service.
    """
    
    def __init__(self, service_name: str):
        """
        Initialize metrics collector.
        
        Args:
            service_name: Name of the service
        """
        self.service_name = service_name
        self.counters: Dict[str, CounterMetric] = {}
        self.gauges: Dict[str, GaugeMetric] = {}
        self.histograms: Dict[str, HistogramMetric] = {}
        self.lock = threading.Lock()
    
    def counter(self, name: str, description: str, labels: Optional[Dict[str, str]] = None) -> CounterMetric:
        """
        Get or create a counter metric.
        
        Args:
            name: Metric name
            description: Metric description
            labels: Optional labels
            
        Returns:
            Counter metric instance
        """
        with self.lock:
            if name not in self.counters:
                self.counters[name] = CounterMetric(
                    name=name,
                    description=description,
                    labels=labels or {}
                )
            return self.counters[name]
    
    def gauge(self, name: str, description: str, labels: Optional[Dict[str, str]] = None) -> GaugeMetric:
        """
        Get or create a gauge metric.
        
        Args:
            name: Metric name
            description: Metric description
            labels: Optional labels
            
        Returns:
            Gauge metric instance
        """
        with self.lock:
            if name not in self.gauges:
                self.gauges[name] = GaugeMetric(
                    name=name,
                    description=description,
                    labels=labels or {}
                )
            return self.gauges[name]
    
    def histogram(self, name: str, description: str, buckets: Optional[List[float]] = None, labels: Optional[Dict[str, str]] = None) -> HistogramMetric:
        """
        Get or create a histogram metric.
        
        Args:
            name: Metric name
            description: Metric description
            buckets: Optional bucket boundaries
            labels: Optional labels
            
        Returns:
            Histogram metric instance
        """
        with self.lock:
            if name not in self.histograms:
                self.histograms[name] = HistogramMetric(
                    name=name,
                    description=description,
                    buckets=buckets,
                    labels=labels or {}
                )
            return self.histograms[name]
    
    def increment_counter(self, name: str, amount: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """
        Increment a counter metric.
        
        Args:
            name: Metric name
            amount: Amount to increment
            labels: Optional labels
        """
        metric = self.counter(name, "Auto-created counter", labels)
        metric.inc(amount)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        Set a gauge metric value.
        
        Args:
            name: Metric name
            value: Value to set
            labels: Optional labels
        """
        metric = self.gauge(name, "Auto-created gauge", labels)
        metric.set(value)
    
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        Observe a value for a histogram metric.
        
        Args:
            name: Metric name
            value: Value to observe
            labels: Optional labels
        """
        metric = self.histogram(name, "Auto-created histogram", labels=labels)
        metric.observe(value)
    
    def get_all_metrics(self) -> Dict:
        """
        Get all metrics in Prometheus format.
        
        Returns:
            Dictionary of all metrics
        """
        with self.lock:
            metrics = {
                "service": self.service_name,
                "counters": [
                    {
                        "name": name,
                        "description": metric.description,
                        "value": metric.value,
                        "labels": metric.labels
                    }
                    for name, metric in self.counters.items()
                ],
                "gauges": [
                    {
                        "name": name,
                        "description": metric.description,
                        "value": metric.value,
                        "labels": metric.labels
                    }
                    for name, metric in self.gauges.items()
                ],
                "histograms": [
                    {
                        "name": name,
                        "description": metric.description,
                        "sample_count": metric.sample_count,
                        "sample_sum": metric.sample_sum,
                        "buckets": metric.buckets,
                        "bucket_counts": metric.bucket_counts,
                        "labels": metric.labels
                    }
                    for name, metric in self.histograms.items()
                ]
            }
            return metrics
    
    def reset(self):
        """Reset all metrics to zero."""
        with self.lock:
            for counter in self.counters.values():
                counter.value = 0.0
            for gauge in self.gauges.values():
                gauge.value = 0.0
            for histogram in self.histograms.values():
                histogram.sample_count = 0
                histogram.sample_sum = 0.0
                histogram.bucket_counts = {i: 0 for i in range(len(histogram.buckets) + 1)}


# Convenience classes
class Counter:
    """Convenience wrapper for counter metrics."""
    
    def __init__(self, name: str, description: str, collector: Optional[MetricsCollector] = None):
        self.name = name
        self.description = description
        self.collector = collector or get_metrics_collector()
    
    def inc(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Increment counter."""
        self.collector.increment_counter(self.name, amount, labels)


class Gauge:
    """Convenience wrapper for gauge metrics."""
    
    def __init__(self, name: str, description: str, collector: Optional[MetricsCollector] = None):
        self.name = name
        self.description = description
        self.collector = collector or get_metrics_collector()
    
    def set(self, value: float, labels: Optional[Dict[str, str]] = None):
        """Set gauge value."""
        self.collector.set_gauge(self.name, value, labels)
    
    def inc(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Increment gauge."""
        metric = self.collector.gauge(self.name, self.description, labels)
        metric.inc(amount)
    
    def dec(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Decrement gauge."""
        metric = self.collector.gauge(self.name, self.description, labels)
        metric.dec(amount)


class Histogram:
    """Convenience wrapper for histogram metrics."""
    
    def __init__(self, name: str, description: str, buckets: Optional[List[float]] = None, collector: Optional[MetricsCollector] = None):
        self.name = name
        self.description = description
        self.buckets = buckets
        self.collector = collector or get_metrics_collector()
    
    def observe(self, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe a value."""
        self.collector.observe_histogram(self.name, value, labels)


# Global metrics collector instance
_global_collector: Optional[MetricsCollector] = None


def get_metrics_collector(service_name: str = "ai-platform") -> MetricsCollector:
    """
    Get or create the global metrics collector.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Metrics collector instance
    """
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector(service_name)
    return _global_collector


def time_metric(histogram_name: str):
    """
    Decorator to time function calls and record to histogram.
    
    Args:
        histogram_name: Name of histogram metric
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                get_metrics_collector().observe_histogram(histogram_name, duration)
        return wrapper
    return decorator