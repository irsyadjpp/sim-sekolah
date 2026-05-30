"""
Gateway API Routes - Monolith Architecture
Direct API endpoints that call gateway service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
gateway_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import gateway_service

@gateway_router.post("/route")
async def route_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Route request - direct function call to gateway service"""
    try:
        result = await gateway_service.route_request(
            request_data=request_data.get('request_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error routing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@gateway_router.post("/authenticate")
async def authenticate_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Authenticate request - direct function call to gateway service"""
    try:
        result = await gateway_service.authenticate_request(
            auth_data=request_data.get('auth_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error authenticating request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
