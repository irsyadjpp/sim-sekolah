"""
Adaptive Learning API Routes - Monolith Architecture
Direct API endpoints that call adaptive learning service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
adaptive_learning_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import adaptive_learning_service

@adaptive_learning_router.post("/analyze-pattern")
async def analyze_learning_pattern(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze learning pattern - direct function call to adaptive learning service"""
    try:
        result = await adaptive_learning_service.analyze_learning_pattern(
            student_id=request_data.get('student_id'),
            learning_data=request_data.get('learning_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing learning pattern: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@adaptive_learning_router.post("/recommend-content")
async def recommend_content(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Recommend content - direct function call to adaptive learning service"""
    try:
        result = await adaptive_learning_service.recommend_content(
            student_id=request_data.get('student_id'),
            subject=request_data.get('subject'),
            performance_data=request_data.get('performance_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error recommending content: {e}")
        raise HTTPException(status_code=500, detail=str(e))
