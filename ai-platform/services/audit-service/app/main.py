"""
Audit Service - Fase 4.1
Governance & Observability - Comprehensive audit logging for AI platform
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
import uuid

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import asyncpg
from redis import asyncio as aioredis
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai_platform:ai_platform@postgres:5432/ai_platform")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
ENABLE_GRPC_SERVER = os.getenv("ENABLE_GRPC_SERVER", "false").lower() == "true"
ENABLE_RABBITMQ_CONSUMER = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
GRPC_PORT = int(os.getenv("GRPC_PORT", "50059"))

# Database connection pool
db_pool: Optional[asyncpg.Pool] = None

# Redis connection
redis_client: Optional[aioredis.Redis] = None


# Pydantic models
class AuditLog(BaseModel):
    """Audit log entry model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    event_type: str  # prompt, retrieval, answer, error, etc.
    event_data: dict
    latency_ms: Optional[float] = None
    token_count: Optional[int] = None
    model_version: Optional[str] = None
    compliance_status: Optional[str] = None  # compliant, non_compliant, pending
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class ComplianceCheck(BaseModel):
    """Compliance check request"""
    request_id: str
    event_type: str
    event_data: dict
    user_id: Optional[str] = None


class ComplianceResult(BaseModel):
    """Compliance check result"""
    request_id: str
    is_compliant: bool
    violations: list
    compliance_status: str


class AuditQuery(BaseModel):
    """Audit log query parameters"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


# Database operations
async def init_db():
    """Initialize database connection and create tables"""
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id VARCHAR(36) PRIMARY KEY,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                user_id VARCHAR(255),
                session_id VARCHAR(255),
                request_id VARCHAR(255),
                event_type VARCHAR(100) NOT NULL,
                event_data JSONB NOT NULL,
                latency_ms FLOAT,
                token_count INTEGER,
                model_version VARCHAR(100),
                compliance_status VARCHAR(50),
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
            CREATE INDEX IF NOT EXISTS idx_audit_logs_session_id ON audit_logs(session_id);
            CREATE INDEX IF NOT EXISTS idx_audit_logs_request_id ON audit_logs(request_id);
            CREATE INDEX IF NOT EXISTS idx_audit_logs_event_type ON audit_logs(event_type);
            CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
            CREATE INDEX IF NOT EXISTS idx_audit_logs_compliance_status ON audit_logs(compliance_status);
        """)


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    redis_client = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


async def close_db():
    """Close database connection"""
    global db_pool
    if db_pool:
        await db_pool.close()


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()


# Audit operations
async def log_event(audit_log: AuditLog) -> str:
    """Log an audit event"""
    global db_pool, redis_client
    
    # Store in database
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO audit_logs 
            (id, timestamp, user_id, session_id, request_id, event_type, event_data, 
             latency_ms, token_count, model_version, compliance_status, ip_address, user_agent)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            """,
            audit_log.id,
            audit_log.timestamp,
            audit_log.user_id,
            audit_log.session_id,
            audit_log.request_id,
            audit_log.event_type,
            json.dumps(audit_log.event_data),
            audit_log.latency_ms,
            audit_log.token_count,
            audit_log.model_version,
            audit_log.compliance_status,
            audit_log.ip_address,
            audit_log.user_agent
        )
    
    # Cache in Redis for quick access
    if redis_client:
        cache_key = f"audit:{audit_log.id}"
        await redis_client.setex(
            cache_key,
            3600,  # 1 hour TTL
            json.dumps(audit_log.dict())
        )
    
    logger.info(f"Audit event logged: {audit_log.id} - {audit_log.event_type}")
    return audit_log.id


async def query_audit_logs(query: AuditQuery) -> list:
    """Query audit logs"""
    global db_pool
    
    conditions = []
    params = []
    param_count = 1
    
    if query.user_id:
        conditions.append(f"user_id = ${param_count}")
        params.append(query.user_id)
        param_count += 1
    
    if query.session_id:
        conditions.append(f"session_id = ${param_count}")
        params.append(query.session_id)
        param_count += 1
    
    if query.event_type:
        conditions.append(f"event_type = ${param_count}")
        params.append(query.event_type)
        param_count += 1
    
    if query.start_date:
        conditions.append(f"timestamp >= ${param_count}")
        params.append(query.start_date)
        param_count += 1
    
    if query.end_date:
        conditions.append(f"timestamp <= ${param_count}")
        params.append(query.end_date)
        param_count += 1
    
    where_clause = " AND ".join(conditions) if conditions else "TRUE"
    
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            f"""
            SELECT * FROM audit_logs
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT ${param_count} OFFSET ${param_count + 1}
            """,
            *params,
            query.limit,
            query.offset
        )
    
    return [dict(row) for row in rows]


async def check_compliance(check: ComplianceCheck) -> ComplianceResult:
    """Check compliance for an event"""
    violations = []
    
    # Example compliance rules
    if check.event_type == "prompt":
        # Check for PII in prompts
        prompt_text = check.event_data.get("prompt", "")
        if "password" in prompt_text.lower() or "secret" in prompt_text.lower():
            violations.append("Potential PII detected in prompt")
    
    if check.event_type == "answer":
        # Check for inappropriate content
        answer_text = check.event_data.get("answer", "")
        if len(answer_text) < 10:
            violations.append("Answer too short")
    
    is_compliant = len(violations) == 0
    compliance_status = "compliant" if is_compliant else "non_compliant"
    
    return ComplianceResult(
        request_id=check.request_id,
        is_compliant=is_compliant,
        violations=violations,
        compliance_status=compliance_status
    )


# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    await init_db()
    await init_redis()
    
    # Import and start gRPC server if enabled
    if ENABLE_GRPC_SERVER:
        from .grpc_server import serve
        import asyncio
        asyncio.create_task(serve(GRPC_PORT))
    
    # Import and start RabbitMQ consumer if enabled
    if ENABLE_RABBITMQ_CONSUMER:
        from .consumer import AsyncAuditServiceConsumer
        consumer = AsyncAuditServiceConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield
    
    await close_db()
    await close_redis()


app = FastAPI(
    title="Audit Service",
    description="Governance & Observability - Comprehensive audit logging",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "audit-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Audit endpoints
@app.post("/audit/log")
async def log_audit_event(audit_log: AuditLog):
    """Log an audit event"""
    log_id = await log_event(audit_log)
    return {"id": log_id, "status": "logged"}


@app.post("/audit/compliance")
async def check_event_compliance(check: ComplianceCheck):
    """Check compliance for an event"""
    result = await check_compliance(check)
    return result


@app.post("/audit/query")
async def query_logs(query: AuditQuery):
    """Query audit logs"""
    logs = await query_audit_logs(query)
    return {"logs": logs, "count": len(logs)}


@app.get("/audit/{log_id}")
async def get_audit_log(log_id: str):
    """Get a specific audit log by ID"""
    global db_pool, redis_client
    
    # Try Redis cache first
    if redis_client:
        cached = await redis_client.get(f"audit:{log_id}")
        if cached:
            return json.loads(cached)
    
    # Fallback to database
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM audit_logs WHERE id = $1", log_id)
    
    if not row:
        raise HTTPException(status_code=404, detail="Audit log not found")
    
    return dict(row)


@app.get("/audit/stats")
async def get_audit_stats():
    """Get audit statistics"""
    global db_pool
    
    async with db_pool.acquire() as conn:
        total_logs = await conn.fetchval("SELECT COUNT(*) FROM audit_logs")
        event_types = await conn.fetch("""
            SELECT event_type, COUNT(*) as count 
            FROM audit_logs 
            GROUP BY event_type 
            ORDER BY count DESC
        """)
        compliance_stats = await conn.fetch("""
            SELECT compliance_status, COUNT(*) as count 
            FROM audit_logs 
            GROUP BY compliance_status
        """)
    
    return {
        "total_logs": total_logs,
        "event_types": [dict(row) for row in event_types],
        "compliance_stats": [dict(row) for row in compliance_stats]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
