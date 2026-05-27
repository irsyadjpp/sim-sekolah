from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import uuid
from pathlib import Path
import tempfile

# Import shared components
import sys
sys.path.append('/app')
from shared.configs.settings import settings
from shared.logging.logger import setup_logging
from shared.schemas.common import HealthResponse, BaseResponse, ErrorResponse
from shared.exceptions.exceptions import ChunkingError, ProcessingError
from shared.utils.helpers import generate_id

# Import chunking components
from app.chunkers.competency_chunker import CompetencyChunker
from app.chunkers.activity_chunker import ActivityChunker
from app.chunkers.assessment_chunker import AssessmentChunker
from app.chunkers.inquiry_chunker import InquiryChunker
from app.chunkers.lesson_plan_chunker import LessonPlanChunker
from app.hierarchy.hierarchy_detector import HierarchyDetector
from app.pedagogy.pedagogy_classifier import PedagogyClassifier
from app.taxonomy.taxonomy_tagger import TaxonomyTagger
from app.builders.chunk_builder import ChunkBuilder
from app.enrichers.chunk_enricher import ChunkEnricher
from app.schemas.chunking_schemas import (
    ChunkRequest,
    ChunkResponse,
    ChunkInfo,
    ChunkMetadata,
    ChunkingOptions,
    BatchChunkRequest,
    BatchChunkResponse
)
from app.consumer import AsyncChunkServiceConsumer

# Setup logging
logger = setup_logging("semantic-chunk-service")

# Temporary storage for chunking operations
TEMP_DIR = Path(tempfile.gettempdir()) / "semantic-chunk-service"
TEMP_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Semantic Chunk Service (MOST IMPORTANT)")
    
    # Initialize chunking components
    try:
        app.state.competency_chunker = CompetencyChunker()
        app.state.activity_chunker = ActivityChunker()
        app.state.assessment_chunker = AssessmentChunker()
        app.state.inquiry_chunker = InquiryChunker()
        app.state.lesson_plan_chunker = LessonPlanChunker()
        app.state.hierarchy_detector = HierarchyDetector()
        app.state.pedagogy_classifier = PedagogyClassifier()
        app.state.taxonomy_tagger = TaxonomyTagger()
        app.state.chunk_builder = ChunkBuilder()
        app.state.chunk_enricher = ChunkEnricher()
        
        logger.info("Semantic chunking components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing chunking components: {str(e)}")
    
    # Start RabbitMQ consumer if enabled
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq:
        logger.info("Starting RabbitMQ consumer")
        app.state.rabbitmq_consumer = AsyncChunkServiceConsumer()
        app.state.rabbitmq_consumer.start_consuming_async()
        logger.info("RabbitMQ consumer started")
    
    yield
    logger.info("Shutting down Semantic Chunk Service")
    
    # Stop RabbitMQ consumer if running
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Semantic Chunk Service",
    description="Curriculum-aware semantic chunking for educational AI platform",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        services={
            "competency_chunker": "available",
            "activity_chunker": "available",
            "assessment_chunker": "available",
            "inquiry_chunker": "available",
            "lesson_plan_chunker": "available",
            "hierarchy_detector": "available",
            "pedagogy_classifier": "available",
            "taxonomy_tagger": "available",
            "chunk_builder": "available",
            "chunk_enricher": "available"
        }
    )


@app.post("/api/v1/chunk", response_model=ChunkResponse)
async def create_chunks(request: ChunkRequest, background_tasks: BackgroundTasks):
    """
    Create semantic chunks from text
    
    This is the CORE function of the service - curriculum-aware semantic chunking
    """
    
    try:
        logger.info(f"Starting semantic chunking for document: {request.document_id}")
        
        # Run chunking in background for long documents
        def process_chunking():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Perform chunking
                result = app.state.chunk_builder.build_chunks(
                    text=request.text,
                    options=request.options,
                    metadata=request.metadata or {}
                )
                
                logger.info(f"Chunking completed for document: {request.document_id}, chunks: {len(result.get('chunks', []))}")
                return result
                
            except Exception as e:
                logger.error(f"Error in chunking background task: {str(e)}")
                raise
        
        # Add background task
        background_tasks.add_task(process_chunking)
        
        return ChunkResponse(
            success=True,
            document_id=request.document_id,
            status="processing",
            message="Semantic chunking started"
        )
        
    except Exception as e:
        logger.error(f"Error starting chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/sync", response_model=ChunkResponse)
async def create_chunks_sync(request: ChunkRequest):
    """
    Create semantic chunks synchronously (for shorter texts)
    """
    
    try:
        logger.info(f"Starting sync semantic chunking for document: {request.document_id}")
        
        # Perform chunking
        result = app.state.chunk_builder.build_chunks(
            text=request.text,
            options=request.options,
            metadata=request.metadata or {}
        )
        
        return ChunkResponse(
            success=True,
            document_id=request.document_id,
            status="completed",
            chunks=result.get('chunks', []),
            chunk_count=len(result.get('chunks', [])),
            processing_time=result.get('processing_time', 0.0),
            statistics=result.get('statistics', {}),
            message="Semantic chunking completed"
        )
        
    except Exception as e:
        logger.error(f"Error in sync chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/batch", response_model=BatchChunkResponse)
async def create_chunks_batch(request: BatchChunkRequest):
    """
    Create chunks for multiple documents in batch
    """
    
    try:
        logger.info(f"Starting batch chunking for {len(request.documents)} documents")
        
        results = []
        
        for doc_request in request.documents:
            try:
                result = app.state.chunk_builder.build_chunks(
                    text=doc_request.text,
                    options=request.options,  # Use same options for all
                    metadata=doc_request.metadata or {}
                )
                
                results.append({
                    "document_id": doc_request.document_id,
                    "chunks": result.get('chunks', []),
                    "chunk_count": len(result.get('chunks', [])),
                    "status": "completed",
                    "processing_time": result.get('processing_time', 0.0)
                })
                
            except Exception as e:
                logger.error(f"Error chunking document {doc_request.document_id}: {str(e)}")
                results.append({
                    "document_id": doc_request.document_id,
                    "chunks": [],
                    "chunk_count": 0,
                    "status": "failed",
                    "error": str(e)
                })
        
        return BatchChunkResponse(
            success=True,
            total_documents=len(request.documents),
            completed=sum(1 for r in results if r['status'] == 'completed'),
            failed=sum(1 for r in results if r['status'] == 'failed'),
            results=results
        )
        
    except Exception as e:
        logger.error(f"Error in batch chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/chunk/{document_id}")
async def get_chunks(document_id: str):
    """
    Get chunks for a specific document
    """
    
    try:
        # In production, this would fetch from database
        # For now, return a placeholder response
        return BaseResponse(
            success=True,
            data={
                "document_id": document_id,
                "chunks": [],
                "message": "Document chunks would be retrieved from database"
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/competency-based")
async def competency_based_chunking(text: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Perform competency-based chunking
    
    This is a key educational chunking strategy based on competencies
    """
    
    try:
        logger.info("Performing competency-based chunking")
        
        chunks = app.state.competency_chunker.chunk(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "chunking_strategy": "competency-based",
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in competency-based chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/activity-based")
async def activity_based_chunking(text: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Perform activity-based chunking
    
    Chunks based on learning activities (inquiry, experiment, reflection, etc.)
    """
    
    try:
        logger.info("Performing activity-based chunking")
        
        chunks = app.state.activity_chunker.chunk(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "chunking_strategy": "activity-based",
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in activity-based chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/assessment-based")
async def assessment_based_chunking(text: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Perform assessment-based chunking
    
    Chunks based on assessment components (questions, rubrics, instructions)
    """
    
    try:
        logger.info("Performing assessment-based chunking")
        
        chunks = app.state.assessment_chunker.chunk(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "chunking_strategy": "assessment-based",
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in assessment-based chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/inquiry-based")
async def inquiry_based_chunking(text: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Perform inquiry-based chunking
    
    Chunks based on inquiry learning components (questions, investigations, hypotheses)
    """
    
    try:
        logger.info("Performing inquiry-based chunking")
        
        chunks = app.state.inquiry_chunker.chunk(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "chunking_strategy": "inquiry-based",
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in inquiry-based chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/lesson-plan-based")
async def lesson_plan_based_chunking(text: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Perform lesson plan-based chunking
    
    Chunks based on lesson plan structure (objectives, activities, assessments, materials)
    """
    
    try:
        logger.info("Performing lesson plan-based chunking")
        
        chunks = app.state.lesson_plan_chunker.chunk(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "chunking_strategy": "lesson-plan-based",
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in lesson plan-based chunking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/detect-hierarchy")
async def detect_hierarchy(text: str):
    """
    Detect document hierarchy structure
    
    Important for understanding document organization and creating meaningful chunks
    """
    
    try:
        logger.info("Detecting document hierarchy")
        
        hierarchy = app.state.hierarchy_detector.detect(text)
        
        return BaseResponse(
            success=True,
            data={
                "hierarchy": hierarchy,
                "hierarchy_levels": hierarchy.get('levels', []),
                "section_count": len(hierarchy.get('sections', []))
            }
        )
        
    except Exception as e:
        logger.error(f"Error detecting hierarchy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/classify-pedagogy")
async def classify_pedagogy(text: str):
    """
    Classify pedagogical approach in text
    
    Identifies inquiry learning, differentiated learning, deep learning, etc.
    """
    
    try:
        logger.info("Classifying pedagogical approach")
        
        pedagogy_result = app.state.pedagogy_classifier.classify(text)
        
        return BaseResponse(
            success=True,
            data={
                "pedagogy_type": pedagogy_result.get('pedagogy_type'),
                "confidence": pedagogy_result.get('confidence', 0.0),
                "indicators": pedagogy_result.get('indicators', [])
            }
        )
        
    except Exception as e:
        logger.error(f"Error classifying pedagogy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/tag-taxonomy")
async def tag_taxonomy(text: str):
    """
    Tag text with Bloom's taxonomy cognitive levels
    
    Identifies remembering, understanding, applying, analyzing, evaluating, creating
    """
    
    try:
        logger.info("Tagging Bloom's taxonomy levels")
        
        taxonomy_result = app.state.taxonomy_tagger.tag(text)
        
        return BaseResponse(
            success=True,
            data={
                "taxonomy_levels": taxonomy_result.get('levels', []),
                "dominant_level": taxonomy_result.get('dominant_level'),
                "confidence": taxonomy_result.get('confidence', 0.0)
            }
        )
        
    except Exception as e:
        logger.error(f"Error tagging taxonomy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chunk/enrich")
async def enrich_chunks(chunks: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None):
    """
    Enrich chunks with additional educational metadata
    
    Adds competency tags, pedagogy tags, cognitive levels, etc.
    """
    
    try:
        logger.info(f"Enriching {len(chunks)} chunks")
        
        enriched_chunks = []
        for chunk in chunks:
            enriched = app.state.chunk_enricher.enrich(chunk, metadata or {})
            enriched_chunks.append(enriched)
        
        return BaseResponse(
            success=True,
            data={
                "enriched_chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error enriching chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """HTTP exception handler"""
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}"
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ).dict()
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8011,
        workers=2,  # More workers as this is CPU-intensive
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )