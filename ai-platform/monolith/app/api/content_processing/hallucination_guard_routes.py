"""
Hallucination Guard API Routes - Monolith Architecture
Direct API endpoints that call hallucination guard service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
hallucination_guard_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import hallucination_guard_service

@hallucination_guard_router.post("/detect")
async def detect_hallucination(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Detect hallucination in generated text - direct function call to hallucination guard service"""
    try:
        # Direct function call to actual hallucination guard service
        result = await hallucination_guard_service.detect_hallucination(
            generated_text=request_data.get('generated_text'),
            context=request_data.get('context'),
            confidence_threshold=request_data.get('confidence_threshold', 0.7)
        )
        
        return result
    except Exception as e:
        logger.error(f"Error detecting hallucination: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@hallucination_guard_router.post("/validate-facts")
async def validate_facts(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate factual accuracy of statements - direct function call to hallucination guard service"""
    try:
        # Direct function call to actual hallucination guard service
        result = await hallucination_guard_service.validate_facts(
            statements=request_data.get('statements'),
            knowledge_base=request_data.get('knowledge_base')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error validating facts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@hallucination_guard_router.post("/check-consistency")
async def check_consistency(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check consistency of response with conversation history - direct function call to hallucination guard service"""
    try:
        # Direct function call to actual hallucination guard service
        result = await hallucination_guard_service.check_consistency(
            response=request_data.get('response'),
            conversation_history=request_data.get('conversation_history')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error checking consistency: {e}")
        raise HTTPException(status_code=500, detail=str(e))
