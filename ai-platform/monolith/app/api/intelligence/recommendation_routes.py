"""
Recommendation API Routes - Monolith Architecture
Direct API endpoints that call recommendation service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
recommendation_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import recommendation_service

@recommendation_router.post("/get-recommendations")
async def get_content_recommendations(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get content recommendations - direct function call to recommendation service"""
    try:
        result = await recommendation_service.get_content_recommendations(
            user_id=request_data.get('user_id'),
            context=request_data.get('context', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error getting content recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@recommendation_router.post("/update-profile")
async def update_user_profile(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update user profile - direct function call to recommendation service"""
    try:
        result = await recommendation_service.update_user_profile(
            user_id=request_data.get('user_id'),
            interaction_data=request_data.get('interaction_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))
