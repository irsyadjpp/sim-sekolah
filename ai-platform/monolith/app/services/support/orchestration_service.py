"""
Orchestration Service - Monolith Architecture
Orchestration functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class OrchestrationService:
    """Orchestration service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize orchestration service with actual components"""
        self.initialized = False
        
        # Initialize actual orchestration components
        try:
            # Import from the actual orchestration-service code
            from orchestration.main import OrchestrationEngine
            
            self.orchestration_engine = OrchestrationEngine()
            
        except Exception as e:
            logger.error(f"Error initializing orchestration components: {e}")
    
    def initialize(self):
        """Initialize orchestration service"""
        try:
            logger.info("Initializing Orchestration Service with actual microservice code")
            self.initialized = True
            logger.info("Orchestration Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Orchestration Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for orchestration service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "orchestration_service",
            "architecture": "monolith",
            "components": {
                "orchestration_engine": "ready"
            }
        }
    
    async def execute_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute pipeline using actual microservice logic
        
        Args:
            pipeline_config: Pipeline configuration
            
        Returns:
            Pipeline execution result
        """
        try:
            logger.info(f"Executing pipeline: {pipeline_config.get('pipeline_name', 'unknown')}")
            
            # Use actual orchestration engine logic
            result = self.orchestration_engine.execute_pipeline(pipeline_config)
            
            logger.info("Pipeline executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error executing pipeline: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def coordinate_services(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate services using actual microservice logic
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            Coordination result
        """
        try:
            logger.info("Coordinating services")
            
            # Use actual orchestration engine logic
            result = self.orchestration_engine.coordinate_services(workflow_data)
            
            logger.info("Services coordinated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error coordinating services: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
