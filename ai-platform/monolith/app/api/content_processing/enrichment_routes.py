"""Enrichment API Routes - Monolith Architecture"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
enrichment_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import semantic_enrichment_service

@enrichment_router.post("/enrich")
async def enrich_chunks(chunks: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich chunks - direct function call to enrichment service"""
    try:
        # Direct function call to actual enrichment service
        result = await semantic_enrichment_service.enrich_chunks(chunks.get('chunks', []))
        
        return result
    except Exception as e:
        logger.error(f"Error enriching chunks: {e}")
        raise HTTPException(status_code=500, detail=str(e))