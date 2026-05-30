"""
Notification API Routes - Monolith Architecture
Direct API endpoints that call notification service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
notification_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import notification_service

@notification_router.post("/send")
async def send_notification(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send notification - direct function call to notification service"""
    try:
        result = await notification_service.send_notification(
            notification_data=request_data.get('notification_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@notification_router.get("/preferences/{user_id}")
async def get_notification_preferences(user_id: str) -> Dict[str, Any]:
    """Get notification preferences - direct function call to notification service"""
    try:
        result = await notification_service.get_notification_preferences(user_id)
        return result
    except Exception as e:
        logger.error(f"Error getting notification preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))
