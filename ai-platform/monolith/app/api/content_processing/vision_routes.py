"""
Vision API Routes - Monolith Architecture
Direct API endpoints that call vision service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
vision_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import vision_service

@vision_router.post("/analyze-image")
async def analyze_image(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze image - direct function call to vision service"""
    try:
        result = await vision_service.analyze_image(
            image_data=request_data.get('image_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@vision_router.post("/extract-text")
async def extract_text_from_image(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract text from image - direct function call to vision service"""
    try:
        result = await vision_service.extract_text_from_image(
            image_data=request_data.get('image_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        raise HTTPException(status_code=500, detail=str(e))
