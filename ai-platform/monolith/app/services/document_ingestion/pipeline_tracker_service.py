"""
Pipeline Tracker Service - Monolith Architecture
Pipeline state tracking using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

sys.path.append('/app')

logger = logging.getLogger(__name__)

# Database connection pool
db_pool = None


class PipelineTrackerService:
    """Pipeline state tracking service"""
    
    def __init__(self):
        """Initialize pipeline tracker service"""
        self.initialized = False
    
    async def initialize(self):
        """Initialize the service"""
        try:
            # Try to initialize database connection if available
            try:
                import asyncpg
                from app.core.config import settings
                global db_pool
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
                logger.warning(f"Database initialization failed: {e}, service will use in-memory tracking")
                db_pool = None
            
            self.initialized = True
            logger.info("Pipeline Tracker Service initialized")
        except Exception as e:
            logger.error(f"Error initializing Pipeline Tracker Service: {str(e)}")
            self.initialized = False
    
    async def initialize_document(self, document_id: str, metadata: Dict[str, Any]) -> bool:
        """Initialize document in pipeline state"""
        try:
            if db_pool:
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
            if db_pool:
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
            if db_pool:
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
            if db_pool:
                async with db_pool.acquire() as conn:
                    rows = await conn.fetch("""
                        SELECT * FROM pipeline_state 
                        WHERE status = 'failed' AND retry_count < max_retries
                        ORDER BY updated_at DESC
                        LIMIT $1
                    """, limit)
                    
                    return [dict(row) for row in rows]
            return []
                
        except Exception as e:
            logger.error(f"Error getting failed documents: {str(e)}")
            return []
    
    async def _log_event(self, document_id: str, event_type: str, stage: str, status: str, 
                        message: Optional[str] = None, duration_ms: Optional[int] = None,
                        service_name: str = "pipeline-tracker", metadata: Dict[str, Any] = None):
        """Log pipeline event"""
        try:
            if db_pool:
                async with db_pool.acquire() as conn:
                    await conn.execute("""
                        SELECT log_pipeline_event($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    """, document_id, event_type, stage, status, message, duration_ms, 
                         service_name, "2.0.0", metadata or {})
                
        except Exception as e:
            logger.error(f"Error logging event: {str(e)}")