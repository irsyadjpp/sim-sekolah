"""
Governance Service - Monolith Architecture
Governance functionality (audit, moderation, hallucination-guard) using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class GovernanceService:
    """Governance service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize governance service with actual components"""
        self.initialized = False
        
        # Initialize actual governance components
        try:
            # Import from the actual governance services code
            from governance.audit.main import AuditService
            from governance.moderation.main import ModerationService
            from governance.hallucination_guard.main import HallucinationGuardService
            
            self.audit_service = AuditService()
            self.moderation_service = ModerationService()
            self.hallucination_guard = HallucinationGuardService()
            
        except Exception as e:
            logger.error(f"Error initializing governance components: {e}")
    
    def initialize(self):
        """Initialize governance service"""
        try:
            logger.info("Initializing Governance Service with actual microservice code")
            self.initialized = True
            logger.info("Governance Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Governance Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for governance service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "governance_service",
            "architecture": "monolith",
            "components": {
                "audit_service": "ready",
                "moderation_service": "ready",
                "hallucination_guard": "ready"
            }
        }
    
    async def audit_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audit action using actual microservice logic
        
        Args:
            action_data: Action data to audit
            
        Returns:
            Audit result
        """
        try:
            logger.info(f"Auditing action: {action_data.get('action_type', 'unknown')}")
            
            # Use actual audit service logic
            result = self.audit_service.audit_action(action_data)
            
            logger.info("Action audited successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error auditing action: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def moderate_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Moderate content using actual microservice logic
        
        Args:
            content_data: Content data to moderate
            
        Returns:
            Moderation result
        """
        try:
            logger.info("Moderating content")
            
            # Use actual moderation service logic
            result = self.moderation_service.moderate_content(content_data)
            
            logger.info("Content moderated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error moderating content: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def check_hallucination(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for hallucinations using actual microservice logic
        
        Args:
            response_data: Response data to check
            
        Returns:
            Hallucination check result
        """
        try:
            logger.info("Checking for hallucinations")
            
            # Use actual hallucination guard logic
            result = self.hallucination_guard.check_hallucination(response_data)
            
            logger.info("Hallucination check completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error checking hallucination: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
