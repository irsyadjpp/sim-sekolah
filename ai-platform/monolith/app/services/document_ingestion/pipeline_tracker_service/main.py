"""
Pipeline Tracker Service
Tracks document state through the AI processing pipeline
"""
import sys
sys.path.append('/app')

import logging
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncpg

# Import shared components
from common.config.settings import settings
from common.logging.logger import setup_logging
from common.schemas.common import HealthResponse

# Setup logging
logger = setup_logging("pipeline-tracker-service")

# Database connection pool
db_pool: Optional[asyncpg.Pool] = None


class PipelineTrackerService:
    """Pipeline state tracking service"""
    
    async def initialize_document(self, document_id: str, metadata: Dict[str, Any]) -> bool:
        """Initialize document in pipeline state"""
        try:
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO pipeline_state 
                    (document_id, current_stage, status, document_type, source_service, subject, grade_level, curriculum_phase)
                    VALUES ($1, 'pending', 'pending', $2, $3, $4, $5, $6)
                    ON CONFLICT (document_id) DO NOTHING
                """, 
                    document_id, 
                    metadata.get('document_type'),
                    metadata.get('source_service', 'unknown'),
                    metadata.get('subject'),
                    metadata.get('grade_level'),
                    metadata.get('curriculum_phase')
                )
                
            logger.info(f"Initialized document {document_id} in pipeline tracker")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing document {document_id}: {str(e)}")
            return False
    
    async def update_stage(self, document_id: str, stage: str, status: str, error_message: Optional[str] = None) -> bool:
        """Update document stage"""
        try:
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    SELECT update_pipeline_state($1, $2, $3, $4)
                """, document_id, stage, status, error_message)
                
            # Log event
            await self._log_event(document_id, f"stage_{status}", stage, status)
            
            logger.info(f"Updated document {document_id} to stage: {stage}, status: {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating stage for document {document_id}: {str(e)}")
            return False
    
    async def get_document_status(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get current document status"""
        try:
            async with db_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM pipeline_state WHERE document_id = $1
                """, document_id)
                
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            logger.error(f"Error getting status for document {document_id}: {str(e)}")
            return None
    
    async def get_failed_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get failed documents for monitoring"""
        try:
            async with db_pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM pipeline_state 
                    WHERE status = 'failed' AND retry_count < max_retries
                    ORDER BY updated_at DESC
                    LIMIT $1
                """, limit)
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting failed documents: {str(e)}")
            return []
    
    async def _log_event(self, document_id: str, event_type: str, stage: str, status: str, 
                        message: Optional[str] = None, duration_ms: Optional[int] = None,
                        service_name: str = "pipeline-tracker", metadata: Dict[str, Any] = None):
        """Log pipeline event"""
        try:
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    SELECT log_pipeline_event($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, document_id, event_type, stage, status, message, duration_ms, 
                     service_name, "2.0.0", metadata or {})
                
        except Exception as e:
            logger.error(f"Error logging event: {str(e)}")


pipeline_tracker = PipelineTrackerService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    global db_pool
    logger.info("Starting Pipeline Tracker Service")
    
    # Initialize database connection
    try:
        db_pool = await asyncpg.create_pool(
            host=settings.database_host,
            port=settings.database_port,
            user=settings.database_user,
            password=settings.database_password,
            database=settings.database_name,
            min_size=5,
            max_size=20
        )
        logger.info("Database connection pool initialized")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    
    yield
    logger.info("Shutting down Pipeline Tracker Service")
    
    # Close database connection
    if db_pool:
        await db_pool.close()
        logger.info("Database connection closed")


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Pipeline Tracker Service",
    description="Pipeline state tracking for AI document processing",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    db_status = "available" if db_pool else "unavailable"
    
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        services={
            "pipeline_tracker": "available",
            "database": db_status
        }
    )


@app.post("/api/v1/documents/{document_id}/initialize")
async def initialize_document(document_id: str, metadata: Dict[str, Any]):
    """Initialize document in pipeline tracker"""
    try:
        success = await pipeline_tracker.initialize_document(document_id, metadata)
        
        if success:
            return {"success": True, "document_id": document_id, "status": "initialized"}
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize document")
            
    except Exception as e:
        logger.error(f"Error initializing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/{document_id}/status")
async def get_document_status(document_id: str):
    """Get document pipeline status"""
    try:
        status = await pipeline_tracker.get_document_status(document_id)
        
        if status:
            return status
        else:
            raise HTTPException(status_code=404, detail="Document not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/documents/{document_id}/stage")
async def update_document_stage(document_id: str, stage: str, status: str, error_message: Optional[str] = None):
    """Update document stage in pipeline"""
    try:
        success = await pipeline_tracker.update_stage(document_id, stage, status, error_message)
        
        if success:
            return {"success": True, "document_id": document_id, "stage": stage, "status": status}
        else:
            raise HTTPException(status_code=500, detail="Failed to update stage")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating document stage: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/failed")
async def get_failed_documents(limit: int = 100):
    """Get failed documents for monitoring"""
    try:
        failed_docs = await pipeline_tracker.get_failed_documents(limit)
        return {
            "count": len(failed_docs),
            "documents": failed_docs
        }
    except Exception as e:
        logger.error(f"Error getting failed documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics/pipeline")
async def get_pipeline_metrics():
    """Get pipeline performance metrics"""
    try:
        async with db_pool.acquire() as conn:
            # Get pipeline overview
            total_docs = await conn.fetchval("SELECT COUNT(*) FROM pipeline_state")
            completed_docs = await conn.fetchval("SELECT COUNT(*) FROM pipeline_state WHERE status = 'completed'")
            failed_docs = await conn.fetchval("SELECT COUNT(*) FROM pipeline_state WHERE status = 'failed'")
            processing_docs = await conn.fetchval("SELECT COUNT(*) FROM pipeline_state WHERE status = 'processing'")
            
            # Get stage distribution
            stage_distribution = await conn.fetch("""
                SELECT current_stage, COUNT(*) as count 
                FROM pipeline_state 
                WHERE status != 'cancelled'
                GROUP BY current_stage
            """)
            
            return {
                "total_documents": total_docs,
                "completed": completed_docs,
                "failed": failed_docs,
                "processing": processing_docs,
                "success_rate": round((completed_docs / total_docs * 100) if total_docs > 0 else 0, 2),
                "stage_distribution": [dict(row) for row in stage_distribution]
            }
            
        except Exception as e:
        logger.error(f"Error getting pipeline metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8010,
        workers=1,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )
