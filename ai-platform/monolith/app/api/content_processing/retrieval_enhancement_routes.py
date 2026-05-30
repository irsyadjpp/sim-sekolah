"""
Retrieval Enhancement API Routes - Monolith Architecture
Direct API endpoints that call retrieval enhancement service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
retrieval_enhancement_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import retrieval_enhancement_service

@retrieval_enhancement_router.post("/enhance-query")
async def enhance_query(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhance query - direct function call to retrieval enhancement service"""
    try:
        result = await retrieval_enhancement_service.enhance_query(
            query_data=request_data.get('query_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error enhancing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@retrieval_enhancement_router.post("/rerank")
async def rerank_results(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Rerank results - direct function call to retrieval enhancement service"""
    try:
        result = await retrieval_enhancement_service.rerank_results(
            query=request_data.get('query'),
            results=request_data.get('results', [])
        )
        return result
    except Exception as e:
        logger.error(f"Error reranking results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@retrieval_enhancement_router.post("/advanced-enhancement")
async def apply_advanced_enhancement(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply advanced enhancement - direct function call to retrieval enhancement service"""
    try:
        result = await retrieval_enhancement_service.apply_advanced_enhancement(
            retrieval_data=request_data.get('retrieval_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error applying advanced enhancement: {e}")
        raise HTTPException(status_code=500, detail=str(e))
