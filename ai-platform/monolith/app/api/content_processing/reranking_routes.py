"""
Reranking API Routes - Monolith Architecture
Direct API endpoints that call reranking service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
reranking_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import reranking_service

@reranking_router.post("/rerank")
async def rerank_results(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Rerank retrieval results - direct function call to reranking service"""
    try:
        # Direct function call to actual reranking service
        result = await reranking_service.rerank_results(
            query=request_data.get('query'),
            initial_results=request_data.get('initial_results'),
            strategy=request_data.get('strategy', 'cross_encoder')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error reranking results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@reranking_router.post("/cross-encoder")
async def cross_encoder_rerank(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Rerank using cross-encoder - direct function call to reranking service"""
    try:
        # Direct function call to actual reranking service
        result = await reranking_service.cross_encoder_rerank(
            query=request_data.get('query'),
            documents=request_data.get('documents')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error in cross-encoder reranking: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@reranking_router.post("/score")
async def score_documents(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Score documents for reranking - direct function call to reranking service"""
    try:
        # Direct function call to actual reranking service
        result = await reranking_service.score_documents(
            query=request_data.get('query'),
            documents=request_data.get('documents'),
            scoring_method=request_data.get('scoring_method', 'relevance')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error scoring documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
