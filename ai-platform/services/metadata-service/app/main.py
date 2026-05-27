from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import uuid

# Import shared components
import sys
sys.path.append('/app')
from shared.configs.settings import settings
from shared.logging.logger import setup_logging
from shared.schemas.common import HealthResponse, BaseResponse, ErrorResponse
from shared.exceptions.exceptions import ProcessingError
from shared.utils.helpers import generate_id

# Import metadata components
from app.enrichers.difficulty_classifier import DifficultyClassifier
from app.enrichers.taxonomy_classifier import TaxonomyClassifier
from app.enrichers.learning_style_detector import LearningStyleDetector
from app.enrichers.competency_tagger import CompetencyTagger
from app.enrichers.pedagogy_tagger import PedagogyTagger
from app.enrichers.assessment_tagger import AssessmentTagger
from app.schemas.metadata_schemas import (
    EnrichmentRequest,
    EnrichmentResponse,
    EnrichmentResult,
    BatchEnrichmentRequest,
    BatchEnrichmentResponse
)
from app.consumer import AsyncMetadataServiceConsumer

# Setup logging
logger = setup_logging("metadata-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Metadata Service")
    
    # Initialize metadata components
    try:
        app.state.difficulty_classifier = DifficultyClassifier()
        app.state.taxonomy_classifier = TaxonomyClassifier()
        app.state.learning_style_detector = LearningStyleDetector()
        app.state.competency_tagger = CompetencyTagger()
        app.state.pedagogy_tagger = PedagogyTagger()
        app.state.assessment_tagger = AssessmentTagger()
        
        logger.info("Metadata enrichment components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing metadata components: {str(e)}")
    
    # Start RabbitMQ consumer if enabled
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq:
        logger.info("Starting RabbitMQ consumer")
        app.state.rabbitmq_consumer = AsyncMetadataServiceConsumer()
        app.state.rabbitmq_consumer.start_consuming_async()
        logger.info("RabbitMQ consumer started")
    
    yield
    logger.info("Shutting down Metadata Service")
    
    # Stop RabbitMQ consumer if running
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Metadata Service",
    description="AI enrichment service for educational content",
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
            "difficulty_classifier": "available",
            "taxonomy_classifier": "available",
            "learning_style_detector": "available",
            "competency_tagger": "available",
            "pedagogy_tagger": "available",
            "assessment_tagger": "available"
        }
    )


@app.post("/api/v1/enrich", response_model=EnrichmentResponse)
async def enrich_content(request: EnrichmentRequest):
    """
    Enrich content with educational metadata
    
    This is the main endpoint that orchestrates all enrichment processes
    """
    
    try:
        logger.info(f"Enriching content: {request.content_id}")
        
        start_time = datetime.utcnow()
        
        # Build enrichment result
        enrichment_result = {
            'content_id': request.content_id,
            'enrichments': {}
        }
        
        # Perform enrichments based on request options
        if request.options.difficulty:
            difficulty_result = app.state.difficulty_classifier.classify(request.text, request.metadata)
            enrichment_result['enrichments']['difficulty'] = difficulty_result
        
        if request.options.taxonomy:
            taxonomy_result = app.state.taxonomy_classifier.classify(request.text, request.metadata)
            enrichment_result['enrichments']['taxonomy'] = taxonomy_result
        
        if request.options.learning_style:
            learning_style_result = app.state.learning_style_detector.detect(request.text, request.metadata)
            enrichment_result['enrichments']['learning_style'] = learning_style_result
        
        if request.options.competency:
            competency_result = app.state.competency_tagger.tag(request.text, request.metadata)
            enrichment_result['enrichments']['competency'] = competency_result
        
        if request.options.pedagogy:
            pedagogy_result = app.state.pedagogy_tagger.tag(request.text, request.metadata)
            enrichment_result['enrichments']['pedagogy'] = pedagogy_result
        
        if request.options.assessment:
            assessment_result = app.state.assessment_tagger.tag(request.text, request.metadata)
            enrichment_result['enrichments']['assessment'] = assessment_result
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return EnrichmentResponse(
            success=True,
            content_id=request.content_id,
            enrichments=enrichment_result['enrichments'],
            processing_time=processing_time,
            status="completed"
        )
        
    except Exception as e:
        logger.error(f"Error enriching content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/difficulty")
async def classify_difficulty(text: str, metadata: Optional[Dict[str, Any]] = None):
    """Classify content difficulty level"""
    try:
        difficulty_result = app.state.difficulty_classifier.classify(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "difficulty": difficulty_result.get('difficulty'),
                "confidence": difficulty_result.get('confidence', 0.0),
                "indicators": difficulty_result.get('indicators', [])
            }
        )
    except Exception as e:
        logger.error(f"Error classifying difficulty: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/taxonomy")
async def classify_taxonomy(text: str, metadata: Optional[Dict[str, Any]] = None):
    """Classify Bloom's taxonomy cognitive level"""
    try:
        taxonomy_result = app.state.taxonomy_classifier.classify(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "taxonomy_level": taxonomy_result.get('taxonomy_level'),
                "confidence": taxonomy_result.get('confidence', 0.0),
                "all_levels": taxonomy_result.get('all_levels', []),
                "indicators": taxonomy_result.get('indicators', [])
            }
        )
    except Exception as e:
        logger.error(f"Error classifying taxonomy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/learning-style")
async def detect_learning_style(text: str, metadata: Optional[Dict[str, Any]] = None):
    """Detect learning style from content"""
    try:
        learning_style_result = app.state.learning_style_detector.detect(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "learning_style": learning_style_result.get('learning_style'),
                "confidence": learning_style_result.get('confidence', 0.0),
                "characteristics": learning_style_result.get('characteristics', [])
            }
        )
    except Exception as e:
        logger.error(f"Error detecting learning style: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/competency")
async def tag_competency(text: str, metadata: Optional[Dict[str, Any]] = None):
    """Tag content with competencies"""
    try:
        competency_result = app.state.competency_tagger.tag(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "competencies": competency_result.get('competencies', []),
                "primary_competency": competency_result.get('primary_competency'),
                "confidence": competency_result.get('confidence', 0.0)
            }
        )
    except Exception as e:
        logger.error(f"Error tagging competency: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/pedagogy")
async def tag_pedagogy(text: str, metadata: Optional[Dict[str, Any]] = None):
    """Tag content with pedagogical approach"""
    try:
        pedagogy_result = app.state.pedagogy_tagger.tag(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "pedagogy_types": pedagogy_result.get('pedagogy_types', []),
                "dominant_pedagogy": pedagogy_result.get('dominant_pedagogy'),
                "confidence": pedagogy_result.get('confidence', 0.0)
            }
        )
    except Exception as e:
        logger.error(f"Error tagging pedagogy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/assessment")
async def tag_assessment(text: str, metadata: Optional[Dict[str, Any]] = None):
    """Tag content with assessment type"""
    try:
        assessment_result = app.state.assessment_tagger.tag(text, metadata or {})
        
        return BaseResponse(
            success=True,
            data={
                "assessment_types": assessment_result.get('assessment_types', []),
                "primary_type": assessment_result.get('primary_type'),
                "cognitive_level": assessment_result.get('cognitive_level'),
                "confidence": assessment_result.get('confidence', 0.0)
            }
        )
    except Exception as e:
        logger.error(f"Error tagging assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/enrich/batch", response_model=BatchEnrichmentResponse)
async def enrich_batch(request: BatchEnrichmentRequest):
    """Enrich multiple contents in batch"""
    try:
        logger.info(f"Batch enriching {len(request.contents)} items")
        
        results = []
        
        for content_item in request.contents:
            try:
                # Build enrichment request
                enrichment_request = EnrichmentRequest(
                    content_id=content_item['content_id'],
                    text=content_item['text'],
                    options=request.options,
                    metadata=content_item.get('metadata')
                )
                
                # Call the main enrichment endpoint
                result = await enrich_content(enrichment_request)
                
                results.append({
                    'content_id': content_item['content_id'],
                    'enrichments': result.enrichments,
                    'processing_time': result.processing_time,
                    'status': result.status
                })
                
            except Exception as e:
                logger.error(f"Error enriching content {content_item['content_id']}: {str(e)}")
                results.append({
                    'content_id': content_item['content_id'],
                    'enrichments': {},
                    'processing_time': 0.0,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return BatchEnrichmentResponse(
            success=True,
            total_contents=len(request.contents),
            completed=sum(1 for r in results if r['status'] == 'completed'),
            failed=sum(1 for r in results if r['status'] == 'failed'),
            results=results
        )
        
    except Exception as e:
        logger.error(f"Error in batch enrichment: {str(e)}")
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
        port=8004,
        workers=2,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )