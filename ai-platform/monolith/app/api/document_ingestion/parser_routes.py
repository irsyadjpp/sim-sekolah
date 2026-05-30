"""
Parser API Routes - Monolith Architecture
Direct API endpoints that call parser service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
parser_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import parser_service

@parser_router.post("/parse")
async def parse_document(document_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse document - direct function call to parser service"""
    try:
        # Direct function call to actual parser service
        result = await parser_service.parse_document(
            document_data=document_data.get('document_data'),
            document_type=document_data.get('document_type', 'pdf'),
            metadata=document_data.get('metadata', {})
        )
        
        return result
    except Exception as e:
        logger.error(f"Error parsing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))