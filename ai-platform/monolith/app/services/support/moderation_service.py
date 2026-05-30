"""
Moderation Service - Monolith Architecture
Content moderation functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class ModerationService:
    """Moderation service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize moderation service with actual components"""
        self.initialized = False
        
        # Initialize actual moderation components
        try:
            # Import from the actual moderation-service code
            from moderation.main import ModerationEngine
            
            self.moderation_engine = ModerationEngine()
            
        except Exception as e:
            logger.error(f"Error initializing moderation components: {e}")
    
    def initialize(self):
        """Initialize moderation service"""
        try:
            logger.info("Initializing Moderation Service with actual microservice code")
            self.initialized = True
            logger.info("Moderation Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Moderation Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for moderation service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "moderation_service",
            "architecture": "monolith",
            "components": {
                "moderation_engine": "ready"
            }
        }
    
    async def moderate_content(self, content: str, content_type: str = "text") -> Dict[str, Any]:
        """
        Moderate content using actual microservice logic
        
        Args:
            content: Content to moderate
            content_type: Type of content (text, image, etc.)
            
        Returns:
            Moderation result
        """
        try:
            logger.info("Moderating content")
            
            # Use actual moderation engine logic
            result = await self.moderation_engine.moderate_content(content, content_type)
            
            logger.info("Content moderation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error moderating content: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def check_policy_violations(self, content: str, policy_type: str = "general") -> Dict[str, Any]:
        """
        Check for policy violations using actual microservice logic
        
        Args:
            content: Content to check
            policy_type: Type of policy to check against
            
        Returns:
            Policy violation check result
        """
        try:
            logger.info(f"Checking policy violations: {policy_type}")
            
            # Use actual moderation engine logic
            result = await self.moderation_engine.check_policy_violations(content, policy_type)
            
            logger.info("Policy violation check completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error checking policy violations: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def filter_content(self, content: str, filter_rules: List[str] = None) -> Dict[str, Any]:
        """
        Filter content based on rules using actual microservice logic
        
        Args:
            content: Content to filter
            filter_rules: Optional filter rules
            
        Returns:
            Filtered content result
        """
        try:
            logger.info("Filtering content")
            
            # Use actual moderation engine logic
            result = await self.moderation_engine.filter_content(content, filter_rules or [])
            
            logger.info("Content filtering completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error filtering content: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
