"""Generation API Routes - Monolith Architecture"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
generation_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import generation_service

@generation_router.post("/generate")
async def generate_content(prompt: Dict[str, Any]) -> Dict[str, Any]:
    """Generate content - direct function call to generation service"""
    try:
        # Direct function call to actual generation service
        result = await generation_service.generate_content(
            prompt=prompt.get('prompt', ''),
            context=prompt.get('context', ''),
            provider=prompt.get('provider', 'openai')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))