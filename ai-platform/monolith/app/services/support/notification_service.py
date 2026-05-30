"""
Notification Service - Monolith Architecture
Notification functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class NotificationService:
    """Notification service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize notification service with actual components"""
        self.initialized = False
        
        # Initialize actual notification components
        try:
            # Import from the actual notification-service code
            from notification.main import NotificationEngine
            
            self.notification_engine = NotificationEngine()
            
        except Exception as e:
            logger.error(f"Error initializing notification components: {e}")
    
    def initialize(self):
        """Initialize notification service"""
        try:
            logger.info("Initializing Notification Service with actual microservice code")
            self.initialized = True
            logger.info("Notification Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Notification Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for notification service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "notification_service",
            "architecture": "monolith",
            "components": {
                "notification_engine": "ready"
            }
        }
    
    async def send_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send notification using actual microservice logic
        
        Args:
            notification_data: Notification data
            
        Returns:
            Notification result
        """
        try:
            logger.info(f"Sending notification to: {notification_data.get('recipient', 'unknown')}")
            
            # Use actual notification engine logic
            result = self.notification_engine.send_notification(notification_data)
            
            logger.info("Notification sent successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def get_notification_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Get notification preferences using actual microservice logic
        
        Args:
            user_id: User identifier
            
        Returns:
            Notification preferences
        """
        try:
            logger.info(f"Getting notification preferences for user: {user_id}")
            
            # Use actual notification engine logic
            result = self.notification_engine.get_preferences(user_id)
            
            logger.info(f"Notification preferences retrieved for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting notification preferences: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
