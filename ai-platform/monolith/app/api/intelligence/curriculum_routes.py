"""
Curriculum API Routes - Monolith Architecture
Direct API endpoints that call curriculum service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
curriculum_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import curriculum_service

@curriculum_router.post("/create")
async def create_curriculum(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create curriculum - direct function call to curriculum service"""
    try:
        result = await curriculum_service.create_curriculum(
            curriculum_data=request_data.get('curriculum_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error creating curriculum: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@curriculum_router.post("/analyze-alignment")
async def analyze_alignment(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze curriculum alignment - direct function call to curriculum service"""
    try:
        result = await curriculum_service.analyze_alignment(
            curriculum_id=request_data.get('curriculum_id'),
            standards=request_data.get('standards', [])
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing alignment: {e}")
        raise HTTPException(status_code=500, detail=str(e))
