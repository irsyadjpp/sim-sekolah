"""
Audit API Routes - Monolith Architecture
Direct API endpoints that call audit service functions directly
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
audit_router = APIRouter()

# Import service instances from main.py (actual monolith instances)
from app.main import audit_service

@audit_router.post("/log")
async def log_audit_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Log audit event - direct function call to audit service"""
    try:
        # Direct function call to actual audit service
        result = await audit_service.log_event(event_data)
        
        return result
    except Exception as e:
        logger.error(f"Error logging audit event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@audit_router.post("/compliance")
async def check_compliance(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check compliance for event - direct function call to audit service"""
    try:
        # Direct function call to actual audit service
        result = await audit_service.check_compliance(
            event_type=request_data.get('event_type'),
            event_data=request_data.get('event_data'),
            user_id=request_data.get('user_id')
        )
        
        return result
    except Exception as e:
        logger.error(f"Error checking compliance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@audit_router.post("/query")
async def query_logs(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Query audit logs - direct function call to audit service"""
    try:
        # Direct function call to actual audit service
        result = await audit_service.query_logs(
            user_id=request_data.get('user_id'),
            session_id=request_data.get('session_id'),
            event_type=request_data.get('event_type'),
            start_date=request_data.get('start_date'),
            end_date=request_data.get('end_date'),
            limit=request_data.get('limit', 100),
            offset=request_data.get('offset', 0)
        )
        
        return result
    except Exception as e:
        logger.error(f"Error querying audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
