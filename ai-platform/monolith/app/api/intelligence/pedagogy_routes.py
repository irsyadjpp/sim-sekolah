"""
Pedagogy API Routes - Monolith Architecture
Direct API endpoints that call pedagogy service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
pedagogy_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import pedagogy_service

@pedagogy_router.post("/analyze-strategy")
async def analyze_learning_strategy(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze learning strategy - direct function call to pedagogy service"""
    try:
        result = await pedagogy_service.analyze_learning_strategy(
            student_id=request_data.get('student_id'),
            learning_data=request_data.get('learning_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing learning strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@pedagogy_router.post("/recommend-teaching-method")
async def recommend_teaching_method(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Recommend teaching method - direct function call to pedagogy service"""
    try:
        result = await pedagogy_service.recommend_teaching_method(
            subject=request_data.get('subject'),
            student_profile=request_data.get('student_profile', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error recommending teaching method: {e}")
        raise HTTPException(status_code=500, detail=str(e))
