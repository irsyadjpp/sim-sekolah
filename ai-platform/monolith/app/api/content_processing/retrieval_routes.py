"""Retrieval API Routes - Monolith Architecture"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
retrieval_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import retrieval_service

@retrieval_router.post("/retrieve")
async def retrieve_documents(query: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve documents - direct function call to retrieval service"""
    try:
        # Direct function call to actual retrieval service
        result = await retrieval_service.retrieve_documents(
            query=query.get('query', ''),
            filters=query.get('filters', {})
        )
        
        return result
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))