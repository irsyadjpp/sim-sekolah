"""
Audit Service - Monolith Architecture
Audit and governance functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

sys.path.append('/app')

logger = logging.getLogger(__name__)


class AuditService:
    """Audit service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize audit service with actual components"""
        self.initialized = False
        
        # Initialize actual audit components
        try:
            # Import from the actual audit-service code
            from audit.main import AuditEngine
            
            self.audit_engine = AuditEngine()
            
        except Exception as e:
            logger.error(f"Error initializing audit components: {e}")
    
    def initialize(self):
        """Initialize audit service"""
        try:
            logger.info("Initializing Audit Service with actual microservice code")
            self.initialized = True
            logger.info("Audit Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Audit Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for audit service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "audit_service",
            "architecture": "monolith",
            "components": {
                "audit_engine": "ready"
            }
        }
    
    async def log_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log audit event using actual microservice logic
        
        Args:
            event_data: Event data to log
            
        Returns:
            Log result
        """
        try:
            logger.info("Logging audit event")
            
            # Use actual audit engine logic
            result = await self.audit_engine.log_event(event_data)
            
            logger.info("Audit event logged successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error logging audit event: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def check_compliance(self, event_type: str, event_data: Dict[str, Any], 
                             user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Check compliance for event using actual microservice logic
        
        Args:
            event_type: Type of event
            event_data: Event data
            user_id: Optional user ID
            
        Returns:
            Compliance check result
        """
        try:
            logger.info(f"Checking compliance for event: {event_type}")
            
            # Use actual audit engine logic
            result = await self.audit_engine.check_compliance(event_type, event_data, user_id)
            
            logger.info("Compliance check completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error checking compliance: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def query_logs(self, user_id: Optional[str] = None, session_id: Optional[str] = None,
                        event_type: Optional[str] = None, start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Query audit logs using actual microservice logic
        
        Args:
            user_id: Optional user ID filter
            session_id: Optional session ID filter
            event_type: Optional event type filter
            start_date: Optional start date filter
            end_date: Optional end date filter
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            Query results
        """
        try:
            logger.info("Querying audit logs")
            
            # Use actual audit engine logic
            result = await self.audit_engine.query_logs(
                user_id=user_id,
                session_id=session_id,
                event_type=event_type,
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset
            )
            
            logger.info("Audit logs queried successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error querying audit logs: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
