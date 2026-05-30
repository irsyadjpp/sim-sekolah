"""
Orchestration API Routes - Monolith Architecture
Direct API endpoints that call orchestration service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
orchestration_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import orchestration_service

@orchestration_router.post("/execute-pipeline")
async def execute_pipeline(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute pipeline - direct function call to orchestration service"""
    try:
        result = await orchestration_service.execute_pipeline(
            pipeline_config=request_data.get('pipeline_config', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error executing pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@orchestration_router.post("/coordinate-services")
async def coordinate_services(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Coordinate services - direct function call to orchestration service"""
    try:
        result = await orchestration_service.coordinate_services(
            workflow_data=request_data.get('workflow_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error coordinating services: {e}")
        raise HTTPException(status_code=500, detail=str(e))
