"""Embedding API Routes - Monolith Architecture"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
embedding_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import embedding_service

@embedding_router.post("/generate")
async def generate_embeddings(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate embeddings - direct function call to embedding service"""
    try:
        # Direct function call to actual embedding service
        result = await embedding_service.generate_embeddings(
            texts=data.get('texts', []),
            model=data.get('model', 'default')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))