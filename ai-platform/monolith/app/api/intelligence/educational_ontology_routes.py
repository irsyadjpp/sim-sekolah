"""
Educational Ontology API Routes - Monolith Architecture
Direct API endpoints that call educational ontology service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
educational_ontology_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import educational_ontology_service

@educational_ontology_router.post("/query")
async def query_ontology(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Query educational ontology - direct function call to educational ontology service"""
    try:
        # Direct function call to actual educational ontology service
        result = await educational_ontology_service.query_ontology(
            ontology_type=request_data.get('ontology_type'),
            query=request_data.get('query'),
            filters=request_data.get('filters', [])
        )
        
        return result
    except Exception as e:
        logger.error(f"Error querying ontology: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@educational_ontology_router.post("/validate-alignment")
async def validate_alignment(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate content alignment with ontology - direct function call to educational ontology service"""
    try:
        # Direct function call to actual educational ontology service
        result = await educational_ontology_service.validate_alignment(
            content=request_data.get('content'),
            ontology_type=request_data.get('ontology_type'),
            target_standards=request_data.get('target_standards', [])
        )
        
        return result
    except Exception as e:
        logger.error(f"Error validating alignment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@educational_ontology_router.post("/related-concepts")
async def get_related_concepts(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get related concepts from ontology - direct function call to educational ontology service"""
    try:
        # Direct function call to actual educational ontology service
        result = await educational_ontology_service.get_related_concepts(
            concept=request_data.get('concept'),
            ontology_type=request_data.get('ontology_type'),
            max_concepts=request_data.get('max_concepts', 10)
        )
        
        return result
    except Exception as e:
        logger.error(f"Error getting related concepts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
