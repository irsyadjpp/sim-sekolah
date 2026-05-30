"""
AI Agents API Routes - Monolith Architecture
Direct API endpoints that call AI agents service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
ai_agents_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import ai_agents_service

@ai_agents_router.post("/execute-task")
async def execute_agent_task(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute agent task - direct function call to AI agents service"""
    try:
        result = await ai_agents_service.execute_agent_task(
            agent_type=request_data.get('agent_type'),
            task_data=request_data.get('task_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error executing agent task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@ai_agents_router.post("/create-agent")
async def create_agent(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create AI agent - direct function call to AI agents service"""
    try:
        result = await ai_agents_service.create_agent(
            agent_config=request_data.get('agent_config', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error creating AI agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
