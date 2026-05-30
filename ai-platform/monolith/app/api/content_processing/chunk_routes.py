"""
Chunk API Routes - Monolith Architecture
Direct API endpoints for semantic chunking
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
chunk_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import semantic_chunk_service

@chunk_router.post("/chunk")
async def chunk_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Chunk document - direct function call to chunk service"""
    try:
        # Direct function call to actual chunk service
        result = await semantic_chunk_service.chunk_document(document)
        
        return result
    except Exception as e:
        logger.error(f"Error chunking document: {e}")
        raise HTTPException(status_code=500, detail=str(e))