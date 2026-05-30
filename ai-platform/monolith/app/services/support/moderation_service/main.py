"""
Moderation Service - Fase 4.2
Governance & Observability - Content moderation and safety filtering
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ENABLE_GRPC_SERVER = os.getenv("ENABLE_GRPC_SERVER", "false").lower() == "true"
ENABLE_RABBITMQ_CONSUMER = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
GRPC_PORT = int(os.getenv("GRPC_PORT", "50060"))


# Pydantic models
class ModerationRequest(BaseModel):
    """Content moderation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    content_type: str = "text"  # text, image, etc.
    user_id: Optional[str] = None
    context: Optional[dict] = None


class ModerationResult(BaseModel):
    """Content moderation result"""
    request_id: str
    is_safe: bool
    toxicity_score: float
    bias_score: float
    categories: List[str]
    flags: List[str]
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModerationQuery(BaseModel):
    """Moderation query parameters"""
    user_id: Optional[str] = None
    content_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


# Moderation operations
class ModerationEngine:
    """Content moderation engine"""
    
    def __init__(self):
        self.toxicity_threshold = 0.7
        self.bias_threshold = 0.6
    
    def check_toxicity(self, content: str) -> float:
        """Check toxicity of content (simplified)"""
        # In production, use actual ML model
        toxic_words = ["bad", "hate", "violence", "abuse"]
        content_lower = content.lower()
        toxic_count = sum(1 for word in toxic_words if word in content_lower)
        return min(toxic_count * 0.2, 1.0)
    
    def check_bias(self, content: str) -> float:
        """Check bias in content (simplified)"""
        # In production, use actual ML model
        bias_indicators = ["always", "never", "all", "none"]
        content_lower = content.lower()
        bias_count = sum(1 for word in bias_indicators if word in content_lower)
        return min(bias_count * 0.15, 1.0)
    
    def detect_categories(self, content: str) -> List[str]:
        """Detect content categories"""
        categories = []
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["hate", "discrimination"]):
            categories.append("hate_speech")
        
        if any(word in content_lower for word in ["violence", "harm", "kill"]):
            categories.append("violence")
        
        if any(word in content_lower for word in ["sexual", "explicit"]):
            categories.append("sexual_content")
        
        if any(word in content_lower for word in ["spam", "advertisement"]):
            categories.append("spam")
        
        return categories
    
    def moderate(self, request: ModerationRequest) -> ModerationResult:
        """Moderate content"""
        toxicity_score = self.check_toxicity(request.content)
        bias_score = self.check_bias(request.content)
        categories = self.detect_categories(request.content)
        
        flags = []
        if toxicity_score > self.toxicity_threshold:
            flags.append("toxic")
        if bias_score > self.bias_threshold:
            flags.append("biased")
        
        is_safe = len(flags) == 0
        confidence = 1.0 - max(toxicity_score, bias_score)
        
        return ModerationResult(
            request_id=request.request_id,
            is_safe=is_safe,
            toxicity_score=toxicity_score,
            bias_score=bias_score,
            categories=categories,
            flags=flags,
            confidence=confidence
        )


# Initialize moderation engine
moderation_engine = ModerationEngine()


# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Import and start gRPC server if enabled
    if ENABLE_GRPC_SERVER:
        from .grpc_server import serve
        import asyncio
        asyncio.create_task(serve(GRPC_PORT))
    
    # Import and start RabbitMQ consumer if enabled
    if ENABLE_RABBITMQ_CONSUMER:
        from .consumer import AsyncModerationServiceConsumer
        consumer = AsyncModerationServiceConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Moderation Service",
    description="Governance & Observability - Content moderation and safety filtering",
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
        "service": "moderation-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Moderation endpoints
@app.post("/moderate")
async def moderate_content(request: ModerationRequest):
    """Moderate content"""
    result = moderation_engine.moderate(request)
    return result


@app.post("/moderate/batch")
async def moderate_batch(requests: List[ModerationRequest]):
    """Moderate multiple contents"""
    results = [moderation_engine.moderate(req) for req in requests]
    return {"results": results, "count": len(results)}


@app.get("/moderation/{request_id}")
async def get_moderation_result(request_id: str):
    """Get moderation result by request ID"""
    # In production, this would query a database
    return {"request_id": request_id, "status": "not_implemented"}


@app.get("/moderation/stats")
async def get_moderation_stats():
    """Get moderation statistics"""
    # In production, this would query a database
    return {
        "total_moderated": 0,
        "safe_count": 0,
        "flagged_count": 0,
        "average_toxicity": 0.0,
        "average_bias": 0.0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
