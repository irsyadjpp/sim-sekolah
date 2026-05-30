"""
Educational Observability API Routes - Monolith Architecture
Direct API endpoints that call educational observability service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
educational_observability_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import educational_observability_service

@educational_observability_router.post("/track-progress")
async def track_learning_progress(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Track learning progress - direct function call to educational observability service"""
    try:
        # Direct function call to actual educational observability service
        result = await educational_observability_service.track_learning_progress(
            student_id=request_data.get('student_id'),
            course_id=request_data.get('course_id'),
            progress_data=request_data.get('progress_data')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error tracking learning progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@educational_observability_router.post("/analyze-engagement")
async def analyze_engagement(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze student engagement - direct function call to educational observability service"""
    try:
        # Direct function call to actual educational observability service
        result = await educational_observability_service.analyze_engagement(
            student_id=request_data.get('student_id'),
            time_period=request_data.get('time_period', 'week')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error analyzing engagement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@educational_observability_router.post("/generate-insights")
async def generate_insights(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate educational insights - direct function call to educational observability service"""
    try:
        # Direct function call to actual educational observability service
        result = await educational_observability_service.generate_insights(
            course_id=request_data.get('course_id'),
            insight_type=request_data.get('insight_type', 'performance')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))
