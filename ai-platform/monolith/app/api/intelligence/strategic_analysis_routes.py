"""
Strategic Analysis API Routes - Monolith Architecture
Direct API endpoints that call strategic analysis service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
strategic_analysis_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import strategic_analysis_service

@strategic_analysis_router.post("/analyze-curriculum-strategy")
async def analyze_curriculum_strategy(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze curriculum strategy - direct function call to strategic analysis service"""
    try:
        result = await strategic_analysis_service.analyze_curriculum_strategy(
            curriculum_id=request_data.get('curriculum_id'),
            strategic_goals=request_data.get('strategic_goals', [])
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing curriculum strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@strategic_analysis_router.post("/generate-strategic-report")
async def generate_strategic_report(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate strategic report - direct function call to strategic analysis service"""
    try:
        result = await strategic_analysis_service.generate_strategic_report(
            institution_id=request_data.get('institution_id'),
            timeframe=request_data.get('timeframe', 'academic_year')
        )
        return result
    except Exception as e:
        logger.error(f"Error generating strategic report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
