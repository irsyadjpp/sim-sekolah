"""
Resource monitoring for AI Platform services

This module provides system resource monitoring capabilities.
"""

import psutil
import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import deque
import logging

logger = logging.getLogger(__name__)


@dataclass
class ResourceSnapshot:
    """Snapshot of system resource usage."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_free_gb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_used_mb": self.memory_used_mb,
            "memory_available_mb": self.memory_available_mb,
            "disk_percent": self.disk_percent,
            "disk_used_gb": self.disk_used_gb,
            "disk_free_gb": self.disk_free_gb,
            "network_sent_mb": self.network_sent_mb,
            "network_recv_mb": self.network_recv_mb,
            "process_count": self.process_count
        }


class ResourceMonitor:
    """
    System resource monitor.
    
    Tracks CPU, memory, disk, network, and process usage.
    """
    
    def __init__(self, history_size: int = 60, interval: float = 1.0):
        """
        Initialize resource monitor.
        
        Args:
            history_size: Number of snapshots to keep in history
            interval: Collection interval in seconds
        """
        self.history_size = history_size
        self.interval = interval
        self.history: deque = deque(maxlen=history_size)
        self.lock = threading.Lock()
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Track network counters for delta calculation
        self._last_network_counters = None
    
    def collect_snapshot(self) -> ResourceSnapshot:
        """
        Collect current resource usage snapshot.
        
        Returns:
            Resource snapshot
        """
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 * 1024)
        memory_available_mb = memory.available / (1024 * 1024)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 * 1024 * 1024)
        disk_free_gb = disk.free / (1024 * 1024 * 1024)
        
        # Network usage
        network = psutil.net_io_counters()
        network_sent_mb = network.bytes_sent / (1024 * 1024)
        network_recv_mb = network.bytes_recv / (1024 * 1024)
        
        # Process count
        process_count = len(psutil.pids())
        
        return ResourceSnapshot(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            memory_available_mb=memory_available_mb,
            disk_percent=disk_percent,
            disk_used_gb=disk_used_gb,
            disk_free_gb=disk_free_gb,
            network_sent_mb=network_sent_mb,
            network_recv_mb=network_recv_mb,
            process_count=process_count
        )
    
    def get_current_snapshot(self) -> ResourceSnapshot:
        """
        Get current resource usage without storing in history.
        
        Returns:
            Current resource snapshot
        """
        return self.collect_snapshot()
    
    def get_history(self) -> List[ResourceSnapshot]:
        """
        Get resource usage history.
        
        Returns:
            List of historical snapshots
        """
        with self.lock:
            return list(self.history)
    
    def get_average_usage(self, duration_seconds: float = 60.0) -> Dict[str, float]:
        """
        Get average resource usage over a time period.
        
        Args:
            duration_seconds: Time period in seconds
            
        Returns:
            Dictionary of average usage statistics
        """
        with self.lock:
            if not self.history:
                return {}
            
            current_time = time.time()
            cutoff_time = current_time - duration_seconds
            
            # Filter snapshots within time period
            recent_snapshots = [
                snapshot for snapshot in self.history
                if snapshot.timestamp >= cutoff_time
            ]
            
            if not recent_snapshots:
                return {}
            
            return {
                "avg_cpu_percent": sum(s.cpu_percent for s in recent_snapshots) / len(recent_snapshots),
                "avg_memory_percent": sum(s.memory_percent for s in recent_snapshots) / len(recent_snapshots),
                "max_cpu_percent": max(s.cpu_percent for s in recent_snapshots),
                "max_memory_percent": max(s.memory_percent for s in recent_snapshots),
                "min_cpu_percent": min(s.cpu_percent for s in recent_snapshots),
                "min_memory_percent": min(s.memory_percent for s in recent_snapshots),
                "snapshot_count": len(recent_snapshots)
            }
    
    def start_monitoring(self):
        """Start continuous resource monitoring."""
        if self._monitoring:
            logger.warning("Resource monitoring already running")
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("Started resource monitoring")
    
    def stop_monitoring(self):
        """Stop continuous resource monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)
            self._monitor_thread = None
        logger.info("Stopped resource monitoring")
    
    def _monitor_loop(self):
        """Monitoring loop that runs in background thread."""
        while self._monitoring:
            try:
                snapshot = self.collect_snapshot()
                with self.lock:
                    self.history.append(snapshot)
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.interval)
    
    def check_thresholds(
        self,
        cpu_threshold: float = 80.0,
        memory_threshold: float = 80.0,
        disk_threshold: float = 90.0
    ) -> Dict[str, bool]:
        """
        Check if resource usage exceeds thresholds.
        
        Args:
            cpu_threshold: CPU usage threshold percentage
            memory_threshold: Memory usage threshold percentage
            disk_threshold: Disk usage threshold percentage
            
        Returns:
            Dictionary of threshold check results
        """
        snapshot = self.get_current_snapshot()
        
        return {
            "cpu_exceeded": snapshot.cpu_percent >= cpu_threshold,
            "memory_exceeded": snapshot.memory_percent >= memory_threshold,
            "disk_exceeded": snapshot.disk_percent >= disk_threshold,
            "cpu_percent": snapshot.cpu_percent,
            "memory_percent": snapshot.memory_percent,
            "disk_percent": snapshot.disk_percent
        }
    
    def get_process_info(self, pid: int) -> Optional[Dict]:
        """
        Get information about a specific process.
        
        Args:
            pid: Process ID
            
        Returns:
            Process information dictionary or None if not found
        """
        try:
            process = psutil.Process(pid)
            return {
                "pid": pid,
                "name": process.name(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "status": process.status(),
                "create_time": process.create_time(),
                "num_threads": process.num_threads()
            }
        except psutil.NoSuchProcess:
            return None
        except Exception as e:
            logger.error(f"Error getting process info for {pid}: {e}")
            return None


# Global resource monitor instance
_global_resource_monitor: Optional[ResourceMonitor] = None


def get_resource_monitor(history_size: int = 60, interval: float = 1.0) -> ResourceMonitor:
    """
    Get or create the global resource monitor.
    
    Args:
        history_size: Number of snapshots to keep in history
        interval: Collection interval in seconds
        
    Returns:
        Resource monitor instance
    """
    global _global_resource_monitor
    if _global_resource_monitor is None:
        _global_resource_monitor = ResourceMonitor(history_size, interval)
    return _global_resource_monitor