"""
Educational Intelligence API Routes - Monolith Architecture
Direct API endpoints that call educational intelligence service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
educational_intelligence_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import educational_intelligence_service

@educational_intelligence_router.post("/analyze-performance")
async def analyze_student_performance(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze student performance - direct function call to educational intelligence service"""
    try:
        result = await educational_intelligence_service.analyze_student_performance(
            student_id=request_data.get('student_id'),
            performance_data=request_data.get('performance_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@educational_intelligence_router.post("/generate-insights")
async def generate_insights(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate educational insights - direct function call to educational intelligence service"""
    try:
        result = await educational_intelligence_service.generate_insights(
            institution_id=request_data.get('institution_id'),
            timeframe=request_data.get('timeframe', 'semester')
        )
        return result
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))
