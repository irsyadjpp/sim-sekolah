"""
Gateway Service - Monolith Architecture
Gateway functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class GatewayService:
    """Gateway service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize gateway service with actual components"""
        self.initialized = False
        
        # Initialize actual gateway components
        try:
            # Import from the actual gateway-service code
            from gateway.main import GatewayEngine
            
            self.gateway_engine = GatewayEngine()
            
        except Exception as e:
            logger.error(f"Error initializing gateway components: {e}")
    
    def initialize(self):
        """Initialize gateway service"""
        try:
            logger.info("Initializing Gateway Service with actual microservice code")
            self.initialized = True
            logger.info("Gateway Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gateway Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for gateway service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "gateway_service",
            "architecture": "monolith",
            "components": {
                "gateway_engine": "ready"
            }
        }
    
    async def route_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route request using actual microservice logic
        
        Args:
            request_data: Request data for routing
            
        Returns:
            Routed request result
        """
        try:
            logger.info(f"Routing request to: {request_data.get('target_service', 'unknown')}")
            
            # Use actual gateway engine logic
            result = self.gateway_engine.route_request(request_data)
            
            logger.info("Request routed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error routing request: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def authenticate_request(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate request using actual microservice logic
        
        Args:
            auth_data: Authentication data
            
        Returns:
            Authentication result
        """
        try:
            logger.info("Authenticating request")
            
            # Use actual gateway engine logic
            result = self.gateway_engine.authenticate(auth_data)
            
            logger.info("Request authenticated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error authenticating request: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
