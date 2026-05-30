"""
Reranking Service - Re-ranks retrieved documents using cross-encoders
Supports curriculum-aware, pedagogy-aware, and competency-aware reranking
"""
import os
import sys
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add shared modules to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../shared")))

from configs.settings import settings
from logging.logging_config import setup_logging
from middleware.error_handler import error_handler
from middleware.auth_middleware import auth_middleware
from schemas.reranking_schemas import (
    RerankRequest,
    RerankResponse,
    CurriculumRerankRequest,
    CurriculumRerankResponse,
    PedagogyRerankRequest,
    PedagogyRerankResponse,
    CompetencyRerankRequest,
    CompetencyRerankResponse,
    RerankingHealthResponse
)

from cross_encoder.cross_encoder import CrossEncoderReranker
from ranking.curriculum_reranker import CurriculumReranker
from ranking.pedagogy_reranker import PedagogyReranker
from ranking.competency_reranker import CompetencyReranker
from consumer import AsyncRerankingServiceConsumer

# Setup logging
logger = setup_logging(__name__)

# Global reranker instances
cross_encoder_reranker: Optional[CrossEncoderReranker] = None
curriculum_reranker: Optional[CurriculumReranker] = None
pedagogy_reranker: Optional[PedagogyReranker] = None
competency_reranker: Optional[CompetencyReranker] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global cross_encoder_reranker, curriculum_reranker, pedagogy_reranker, competency_reranker
    
    # Startup
    logger.info("Starting Reranking Service...")
    
    try:
        # Initialize cross-encoder reranker
        cross_encoder_reranker = CrossEncoderReranker(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            device=settings.embedding_device
        )
        logger.info("Cross-encoder reranker initialized")
        
        # Initialize curriculum-aware reranker
        curriculum_reranker = CurriculumReranker()
        logger.info("Curriculum reranker initialized")
        
        # Initialize pedagogy-aware reranker
        pedagogy_reranker = PedagogyReranker()
        logger.info("Pedagogy reranker initialized")
        
        # Initialize competency-aware reranker
        competency_reranker = CompetencyReranker()
        logger.info("Competency reranker initialized")
        
        logger.info("Reranking Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize rerankers: {str(e)}")
        raise
    
    # Start RabbitMQ consumer if enabled
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq:
        logger.info("Starting RabbitMQ consumer")
        app.state.rabbitmq_consumer = AsyncRerankingServiceConsumer()
        app.state.rabbitmq_consumer.start_consuming_async()
        logger.info("RabbitMQ consumer started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Reranking Service...")
    
    # Stop RabbitMQ consumer if running
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()
    
    # Cleanup rerankers if needed
    logger.info("Reranking Service shut down")


# Create FastAPI app
app = FastAPI(
    title="Reranking Service",
    description="Re-ranks retrieved documents using cross-encoders and curriculum-aware strategies",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Add custom middleware
app.middleware("http")(error_handler)
app.middleware("http")(auth_middleware)


@app.get("/health", response_model=RerankingHealthResponse)
async def health_check():
    """Health check endpoint"""
    return RerankingHealthResponse(
        status="healthy",
        service="reranking-service",
        model="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )


@app.post("/api/v1/rerank", response_model=RerankResponse)
async def rerank(request: RerankRequest):
    """
    Rerank documents using cross-encoder model
    
    Args:
        request: Rerank request with documents and query
    
    Returns:
        RerankResponse with reranked results
    """
    try:
        if cross_encoder_reranker is None:
            raise HTTPException(status_code=503, detail="Cross-encoder reranker not initialized")
        
        reranked_results = await cross_encoder_reranker.rerank(
            query=request.query,
            documents=request.documents,
            top_k=request.top_k
        )
        
        return RerankResponse(
            results=reranked_results,
            query=request.query,
            original_count=len(request.documents),
            reranked_count=len(reranked_results),
            method="cross-encoder"
        )
        
    except Exception as e:
        logger.error(f"Error in reranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rerank/curriculum", response_model=CurriculumRerankResponse)
async def rerank_curriculum(request: CurriculumRerankRequest):
    """
    Rerank documents using curriculum-aware strategy
    
    Args:
        request: Curriculum rerank request
    
    Returns:
        CurriculumRerankResponse with reranked results
    """
    try:
        if curriculum_reranker is None:
            raise HTTPException(status_code=503, detail="Curriculum reranker not initialized")
        
        reranked_results = await curriculum_reranker.rerank(
            query=request.query,
            documents=request.documents,
            curriculum_level=request.curriculum_level,
            subject=request.subject,
            competency_focus=request.competency_focus
        )
        
        return CurriculumRerankResponse(
            results=reranked_results,
            query=request.query,
            curriculum_level=request.curriculum_level,
            subject=request.subject,
            competency_focus=request.competency_focus,
            method="curriculum-aware"
        )
        
    except Exception as e:
        logger.error(f"Error in curriculum reranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rerank/pedagogy", response_model=PedagogyRerankResponse)
async def rerank_pedagogy(request: PedagogyRerankRequest):
    """
    Rerank documents using pedagogy-aware strategy
    
    Args:
        request: Pedagogy rerank request
    
    Returns:
        PedagogyRerankResponse with reranked results
    """
    try:
        if pedagogy_reranker is None:
            raise HTTPException(status_code=503, detail="Pedagogy reranker not initialized")
        
        reranked_results = await pedagogy_reranker.rerank(
            query=request.query,
            documents=request.documents,
            learning_style=request.learning_style,
            pedagogy_type=request.pedagogy_type
        )
        
        return PedagogyRerankResponse(
            results=reranked_results,
            query=request.query,
            learning_style=request.learning_style,
            pedagogy_type=request.pedagogy_type,
            method="pedagogy-aware"
        )
        
    except Exception as e:
        logger.error(f"Error in pedagogy reranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rerank/competency", response_model=CompetencyRerankResponse)
async def rerank_competency(request: CompetencyRerankRequest):
    """
    Rerank documents using competency-aware strategy
    
    Args:
        request: Competency rerank request
    
    Returns:
        CompetencyRerankResponse with reranked results
    """
    try:
        if competency_reranker is None:
            raise HTTPException(status_code=503, detail="Competency reranker not initialized")
        
        reranked_results = await competency_reranker.rerank(
            query=request.query,
            documents=request.documents,
            competency_type=request.competency_type,
            bloom_level=request.bloom_level
        )
        
        return CompetencyRerankResponse(
            results=reranked_results,
            query=request.query,
            competency_type=request.competency_type,
            bloom_level=request.bloom_level,
            method="competency-aware"
        )
        
    except Exception as e:
        logger.error(f"Error in competency reranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/methods")
async def list_methods():
    """List available reranking methods"""
    return {
        "methods": [
            {
                "name": "cross-encoder",
                "description": "Cross-encoder model for relevance scoring",
                "model": "cross-encoder/ms-marco-MiniLM-L-6-v2"
            },
            {
                "name": "curriculum-aware",
                "description": "Curriculum-aware reranking for Kurikulum Merdeka",
                "factors": ["curriculum_level", "subject", "competency"]
            },
            {
                "name": "pedagogy-aware",
                "description": "Pedagogy-aware reranking based on learning styles",
                "factors": ["learning_style", "pedagogy_type"]
            },
            {
                "name": "competency-aware",
                "description": "Competency-aware reranking based on KI-1 to KI-4",
                "factors": ["competency_type", "bloom_level"]
            }
        ]
    }


@app.get("/api/v1/stats")
async def get_stats():
    """Get reranking service statistics"""
    return {
        "service": "reranking-service",
        "model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "device": settings.embedding_device,
        "status": {
            "cross_encoder": cross_encoder_reranker is not None,
            "curriculum_reranker": curriculum_reranker is not None,
            "pedagogy_reranker": pedagogy_reranker is not None,
            "competency_reranker": competency_reranker is not None
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8008,
        reload=settings.debug,
        workers=1 if settings.debug else 4
    )