"""
Metadata API Routes - Monolith Architecture
Direct API endpoints that call metadata service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
metadata_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import metadata_service

@metadata_router.post("/extract")
async def extract_metadata(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract metadata - direct function call to metadata service"""
    try:
        result = await metadata_service.extract_metadata(
            content_data=request_data.get('content_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error extracting metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@metadata_router.post("/update")
async def update_metadata(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update metadata - direct function call to metadata service"""
    try:
        result = await metadata_service.update_metadata(
            resource_id=request_data.get('resource_id'),
            metadata_updates=request_data.get('metadata_updates', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error updating metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e))
