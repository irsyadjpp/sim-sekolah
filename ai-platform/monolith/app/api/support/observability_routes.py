"""
Observability API Routes - Monolith Architecture
Direct API endpoints that call observability service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
observability_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import observability_service

@observability_router.post("/track-event")
async def track_event(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Track educational event - direct function call to observability service"""
    try:
        result = await observability_service.track_event(
            event_data=request_data.get('event_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error tracking event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@observability_router.post("/generate-report")
async def generate_report(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate observability report - direct function call to observability service"""
    try:
        result = await observability_service.generate_report(
            report_type=request_data.get('report_type'),
            filters=request_data.get('filters', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
