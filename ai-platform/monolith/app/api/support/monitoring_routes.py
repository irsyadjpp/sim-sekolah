"""
Monitoring API Routes - Monolith Architecture
Direct API endpoints that call monitoring service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
monitoring_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import monitoring_service

@monitoring_router.post("/collect-metrics")
async def collect_metrics(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Collect metrics - direct function call to monitoring service"""
    try:
        result = await monitoring_service.collect_metrics(
            service_name=request_data.get('service_name'),
            metrics_data=request_data.get('metrics_data', {})
        )
        return result
    except Exception as e:
        logger.error(f"Error collecting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@monitoring_router.get("/system-health")
async def get_system_health() -> Dict[str, Any]:
    """Get system health - direct function call to monitoring service"""
    try:
        result = await monitoring_service.get_system_health()
        return result
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(status_code=500, detail=str(e))
