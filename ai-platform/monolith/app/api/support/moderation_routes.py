"""
Moderation API Routes - Monolith Architecture
Direct API endpoints that call moderation service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
moderation_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import moderation_service

@moderation_router.post("/moderate")
async def moderate_content(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Moderate content - direct function call to moderation service"""
    try:
        # Direct function call to actual moderation service
        result = await moderation_service.moderate_content(
            content=request_data.get('content'),
            content_type=request_data.get('content_type', 'text')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error moderating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@moderation_router.post("/check-policy")
async def check_policy_violations(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check for policy violations - direct function call to moderation service"""
    try:
        # Direct function call to actual moderation service
        result = await moderation_service.check_policy_violations(
            content=request_data.get('content'),
            policy_type=request_data.get('policy_type', 'general')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error checking policy violations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@moderation_router.post("/filter")
async def filter_content(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Filter content based on rules - direct function call to moderation service"""
    try:
        # Direct function call to actual moderation service
        result = await moderation_service.filter_content(
            content=request_data.get('content'),
            filter_rules=request_data.get('filter_rules')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error filtering content: {e}")
        raise HTTPException(status_code=500, detail=str(e))
