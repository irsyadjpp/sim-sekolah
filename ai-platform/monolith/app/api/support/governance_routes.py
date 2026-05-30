"""
Governance API Routes - Monolith Architecture
Direct API endpoints that call governance service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
governance_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import governance_service

@governance_router.post("/audit")
async def audit_action(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Audit action - direct function call to governance service"""
    try:
        result = await governance_service.audit_action(
            action_data=request_data.get('action_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error auditing action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@governance_router.post("/moderate")
async def moderate_content(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Moderate content - direct function call to governance service"""
    try:
        result = await governance_service.moderate_content(
            content_data=request_data.get('content_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error moderating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@governance_router.post("/check-hallucination")
async def check_hallucination(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check for hallucinations - direct function call to governance service"""
    try:
        result = await governance_service.check_hallucination(
            response_data=request_data.get('response_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error checking hallucination: {e}")
        raise HTTPException(status_code=500, detail=str(e))
