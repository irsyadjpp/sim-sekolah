"""
Monitoring Service - Monolith Architecture
Monitoring functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class MonitoringService:
    """Monitoring service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize monitoring service with actual components"""
        self.initialized = False
        
        # Initialize actual monitoring components
        try:
            # Import from the actual monitoring-service code
            from monitoring.main import MonitoringEngine
            
            self.monitoring_engine = MonitoringEngine()
            
        except Exception as e:
            logger.error(f"Error initializing monitoring components: {e}")
    
    def initialize(self):
        """Initialize monitoring service"""
        try:
            logger.info("Initializing Monitoring Service with actual microservice code")
            self.initialized = True
            logger.info("Monitoring Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Monitoring Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for monitoring service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "monitoring_service",
            "architecture": "monolith",
            "components": {
                "monitoring_engine": "ready"
            }
        }
    
    async def collect_metrics(self, service_name: str, 
                             metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect metrics using actual microservice logic
        
        Args:
            service_name: Service name
            metrics_data: Metrics data
            
        Returns:
            Metrics collection result
        """
        try:
            logger.info(f"Collecting metrics for service: {service_name}")
            
            # Use actual monitoring engine logic
            result = self.monitoring_engine.collect_metrics(service_name, metrics_data)
            
            logger.info(f"Metrics collected successfully for service {service_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """
        Get system health using actual microservice logic
        
        Returns:
            System health status
        """
        try:
            logger.info("Getting system health")
            
            # Use actual monitoring engine logic
            result = self.monitoring_engine.get_system_health()
            
            logger.info("System health retrieved successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
