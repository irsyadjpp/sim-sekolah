"""Ontology API Routes - Monolith Architecture"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
ontology_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import ontology_validation_service

@ontology_router.post("/validate")
async def validate_ontology(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate ontology - direct function call to ontology service"""
    try:
        validation_type = data.get('validation_type', 'competency')
        validation_data = data.get('data', {})
        
        # Direct function call to actual ontology validation service
        if validation_type == 'competency':
            result = await ontology_validation_service.validate_competency(validation_data)
        elif validation_type == 'pedagogy':
            result = await ontology_validation_service.validate_pedagogy(validation_data)
        elif validation_type == 'taxonomy':
            result = await ontology_validation_service.validate_taxonomy(validation_data)
        else:
            result = {
                "success": False,
                "error": f"Unknown validation type: {validation_type}"
            }
        
        return result
    except Exception as e:
        logger.error(f"Error validating ontology: {e}")
        raise HTTPException(status_code=500, detail=str(e))