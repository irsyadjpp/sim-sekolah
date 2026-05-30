"""
Learning Progression API Routes - Monolith Architecture
Direct API endpoints that call learning progression service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
learning_progression_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import learning_progression_service

@learning_progression_router.post("/track")
async def track_progress(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Track learning progress - direct function call to learning progression service"""
    try:
        # Direct function call to actual learning progression service
        result = await learning_progression_service.track_progress(
            student_id=request_data.get('student_id'),
            course_id=request_data.get('course_id'),
            competency_id=request_data.get('competency_id'),
            progress_data=request_data.get('progress_data')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error tracking learning progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@learning_progression_router.post("/assess-mastery")
async def assess_mastery(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Assess student mastery level - direct function call to learning progression service"""
    try:
        # Direct function call to actual learning progression service
        result = await learning_progression_service.assess_mastery(
            student_id=request_data.get('student_id'),
            competency_id=request_data.get('competency_id')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error assessing mastery: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@learning_progression_router.post("/recommend-next-steps")
async def recommend_next_steps(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Recommend next learning steps - direct function call to learning progression service"""
    try:
        # Direct function call to actual learning progression service
        result = await learning_progression_service.recommend_next_steps(
            student_id=request_data.get('student_id'),
            course_id=request_data.get('course_id')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error recommending next steps: {e}")
        raise HTTPException(status_code=500, detail=str(e))
