"""
Assessment API Routes - Monolith Architecture
Direct API endpoints that call assessment service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
assessment_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import assessment_service

@assessment_router.post("/create")
async def create_assessment(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create assessment - direct function call to assessment service"""
    try:
        result = await assessment_service.create_assessment(
            assessment_data=request_data.get('assessment_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error creating assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@assessment_router.post("/evaluate")
async def evaluate_submission(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate submission - direct function call to assessment service"""
    try:
        result = await assessment_service.evaluate_submission(
            submission_data=request_data.get('submission_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error evaluating submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))
