"""
Learning Graph API Routes - Monolith Architecture
Direct API endpoints that call learning graph service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)
learning_graph_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import learning_graph_service

@learning_graph_router.post("/build-graph")
async def build_knowledge_graph(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build knowledge graph - direct function call to learning graph service"""
    try:
        result = await learning_graph_service.build_knowledge_graph(
            curriculum_id=request_data.get('curriculum_id'),
            content_data=request_data.get('content_data', [])
        )
        return result
    except Exception as e:
        logger.error(f"Error building knowledge graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@learning_graph_router.post("/track-progression")
async def track_progression(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Track learning progression - direct function call to learning graph service"""
    try:
        result = await learning_graph_service.track_progression(
            student_id=request_data.get('student_id'),
            learning_path=request_data.get('learning_path', [])
        )
        return result
    except Exception as e:
        logger.error(f"Error tracking progression: {e}")
        raise HTTPException(status_code=500, detail=str(e))
