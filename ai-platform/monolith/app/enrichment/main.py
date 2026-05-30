"""
Semantic Enrichment Service - Advanced Semantic Tagging
Provides 6 automated tagging systems for educational content enrichment
"""
import os
import sys
sys.path.append('/app')

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Import shared components
from common.config.settings import settings
from common.logging.logger import setup_logging
from common.schemas.common import HealthResponse

# Import tagger implementations
from app.taggers.competency_tagger import CompetencyTagger
from app.taggers.pedagogy_tagger import PedagogyTagger
from app.taggers.assessment_tagger import AssessmentTagger
from app.taggers.cognitive_level_tagger import CognitiveLevelTagger
from app.taggers.learning_objective_tagger import LearningObjectiveTagger
from app.taggers.deep_learning_tagger import DeepLearningTagger
from app.taggers.taxonomy_tagger import TaxonomyTagger

# Setup logging
logger = setup_logging("semantic-enrichment-service")

# Environment variables
ENABLE_GRPC_SERVER = os.getenv("ENABLE_GRPC_SERVER", "false").lower() == "true"
ENABLE_RABBITMQ_CONSUMER = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
GRPC_PORT = int(os.getenv("GRPC_PORT", "50070"))


# Pydantic models
class TaggingRequest(BaseModel):
    """Base tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    content_type: str = "text"  # text, document, lesson_plan, assessment
    context: Optional[Dict[str, Any]] = None


class CompetencyTaggingRequest(BaseModel):
    """Competency tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    curriculum_phase: Optional[str] = None
    subject: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class PedagogyTaggingRequest(BaseModel):
    """Pedagogy tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    grade_level: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AssessmentTaggingRequest(BaseModel):
    """Assessment tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    assessment_type: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class CognitiveLevelTaggingRequest(BaseModel):
    """Cognitive level tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    target_levels: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None


class LearningObjectiveTaggingRequest(BaseModel):
    """Learning objective tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    curriculum_standards: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class TaxonomyTaggingRequest(BaseModel):
    """Taxonomy tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    context: Optional[Dict[str, Any]] = None


class DeepLearningTaggingRequest(BaseModel):
    """Deep learning tagging request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    model_type: str = "transformer"  # transformer, bert, roberta
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    context: Optional[Dict[str, Any]] = None


class TaggingResult(BaseModel):
    """Tagging result"""
    request_id: str
    tagging_type: str
    tags: List[Dict[str, Any]]
    confidence_scores: List[float]
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Semantic Enrichment Engine
class SemanticEnrichmentEngine:
    """Advanced semantic enrichment with 6 automated tagging systems"""
    
    def __init__(self):
        # Initialize all tagging systems with proper implementations
        self.competency_tagger = CompetencyTagger()
        self.pedagogy_tagger = PedagogyTagger()
        self.assessment_tagger = AssessmentTagger()
        self.cognitive_level_tagger = CognitiveLevelTagger()
        self.learning_objective_tagger = LearningObjectiveTagger()
        self.deep_learning_tagger = DeepLearningTagger()
        self.taxonomy_tagger = TaxonomyTagger()
        
        # Performance metrics
        self.performance_metrics = {
            "total_taggings": 0,
            "avg_tagging_time_ms": 0,
            "system_usage": {},
            "accuracy_metrics": {}
        }
        
        logger.info("SemanticEnrichmentEngine initialized with all 7 tagging systems (including taxonomy)")
    
    def tag_competencies(self, request: CompetencyTaggingRequest) -> Dict:
        """Automated competency tagging"""
        import time
        start_time = time.time()
        
        # Apply competency tagging
        tags = self.competency_tagger.tag(
            request.content,
            request.curriculum_phase,
            request.subject
        )
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("competency_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "curriculum_phase": request.curriculum_phase,
                "subject": request.subject,
                "tagging_method": "rule_based"
            }
        }
    
    def tag_pedagogy(self, request: PedagogyTaggingRequest) -> Dict:
        """Automated pedagogy tagging"""
        import time
        start_time = time.time()
        
        # Apply pedagogy tagging
        tags = self.pedagogy_tagger.tag(
            request.content,
            request.grade_level
        )
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("pedagogy_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "grade_level": request.grade_level,
                "tagging_method": "pattern_matching"
            }
        }
    
    def tag_assessment(self, request: AssessmentTaggingRequest) -> Dict:
        """Automated assessment tagging"""
        import time
        start_time = time.time()
        
        # Apply assessment tagging
        tags = self.assessment_tagger.tag(
            request.content,
            request.assessment_type
        )
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "assessment_type": request.assessment_type,
                "tagging_method": "classification"
            }
        }
    
    def tag_cognitive_level(self, request: CognitiveLevelTaggingRequest) -> Dict:
        """Automated cognitive level tagging"""
        import time
        start_time = time.time()
        
        # Apply cognitive level tagging
        tags = self.cognitive_level_tagger.tag(
            request.content,
            request.target_levels
        )
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("cognitive_level_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "target_levels": request.target_levels,
                "tagging_method": "bloom_taxonomy"
            }
        }
    
    def tag_learning_objectives(self, request: LearningObjectiveTaggingRequest) -> Dict:
        """Automated learning objective tagging"""
        import time
        start_time = time.time()
        
        # Apply learning objective tagging
        tags = self.learning_objective_tagger.tag(
            request.content,
            request.curriculum_standards
        )
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("learning_objective_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "curriculum_standards": request.curriculum_standards,
                "tagging_method": "objective_matching"
            }
        }
    
    def tag_deep_learning(self, request: DeepLearningTaggingRequest) -> Dict:
        """Deep learning-based tagging"""
        import time
        start_time = time.time()
        
        # Apply deep learning tagging
        tags = self.deep_learning_tagger.tag(
            request.content,
            request.model_type,
            request.confidence_threshold
        )
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("deep_learning_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "model_type": request.model_type,
                "confidence_threshold": request.confidence_threshold,
                "tagging_method": "neural_network"
            }
        }
    
    def tag_taxonomy(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict:
        """Taxonomy tagging - curriculum standards, subjects, grade levels"""
        import time
        start_time = time.time()
        
        # Apply taxonomy tagging
        tags = self.taxonomy_tagger.tag(content, context)
        
        # Update performance metrics
        tagging_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("taxonomy_tagger", tagging_time)
        
        return {
            "tags": tags,
            "confidence_scores": [tag.get("confidence", 0.8) for tag in tags],
            "metadata": {
                "tagging_method": "canonical_normalization",
                "ontology_version": "v2.0"
            }
        }
    
    def _update_performance_metrics(self, system_name: str, tagging_time_ms: float):
        """Update performance metrics"""
        self.performance_metrics["total_taggings"] += 1
        
        # Update average tagging time
        total = self.performance_metrics["total_taggings"]
        current_avg = self.performance_metrics["avg_tagging_time_ms"]
        new_avg = (current_avg * (total - 1) + tagging_time_ms) / total
        self.performance_metrics["avg_tagging_time_ms"] = new_avg
        
        # Update system usage
        if system_name not in self.performance_metrics["system_usage"]:
            self.performance_metrics["system_usage"][system_name] = 0
        self.performance_metrics["system_usage"][system_name] += 1


# Note: Proper tagger implementations are now in app/taggers/ directory
# Placeholder classes removed to use proper implementations


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Semantic Enrichment Service",
    description="Advanced semantic tagging service - provides 6 automated tagging systems for educational content",
    version="2.0.0",
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
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        services={
            "competency_tagger": "available",
            "pedagogy_tagger": "available",
            "assessment_tagger": "available",
            "cognitive_level_tagger": "available",
            "learning_objective_tagger": "available",
            "deep_learning_tagger": "available",
            "taxonomy_tagger": "available",
            "semantic_enrichment_engine": "available"
        }
    )


@app.post("/api/v1/enrich")
async def enrich_content(request: TaggingRequest):
    """
    Main enrichment endpoint - applies all 6 tagging systems to content
    
    This is the primary integration point for semantic-chunk-service to call
    for advanced semantic tagging of chunks.
    """
    try:
        logger.info(f"Processing enrichment request: {request.request_id}")
        
        # Apply all tagging systems
        enrichment_results = {}
        
        # Competency tagging
        if request.context and request.context.get('subject'):
            competency_request = CompetencyTaggingRequest(
                request_id=request.request_id,
                content=request.content,
                curriculum_phase=request.context.get('curriculum_phase'),
                subject=request.context.get('subject')
            )
            enrichment_results['competency'] = app.state.enrichment_engine.tag_competencies(competency_request)
        
        # Pedagogy tagging
        if request.context and request.context.get('grade_level'):
            pedagogy_request = PedagogyTaggingRequest(
                request_id=request.request_id,
                content=request.content,
                grade_level=request.context.get('grade_level')
            )
            enrichment_results['pedagogy'] = app.state.enrichment_engine.tag_pedagogy(pedagogy_request)
        
        # Assessment tagging
        if request.context and request.context.get('assessment_type'):
            assessment_request = AssessmentTaggingRequest(
                request_id=request.request_id,
                content=request.content,
                assessment_type=request.context.get('assessment_type')
            )
            enrichment_results['assessment'] = app.state.enrichment_engine.tag_assessment(assessment_request)
        
        # Cognitive level tagging
        cognitive_request = CognitiveLevelTaggingRequest(
            request_id=request.request_id,
            content=request.content,
            target_levels=request.context.get('target_levels') if request.context else None
        )
        enrichment_results['cognitive_level'] = app.state.enrichment_engine.tag_cognitive_level(cognitive_request)
        
        # Learning objective tagging
        if request.context and request.context.get('curriculum_standards'):
            objective_request = LearningObjectiveTaggingRequest(
                request_id=request.request_id,
                content=request.content,
                curriculum_standards=request.context.get('curriculum_standards')
            )
            enrichment_results['learning_objectives'] = app.state.enrichment_engine.tag_learning_objectives(objective_request)
        
        # Taxonomy tagging (NEW - moved from chunk service)
        taxonomy_tags = app.state.enrichment_engine.tag_taxonomy(request.content, request.context)
        enrichment_results['taxonomy'] = taxonomy_tags
        
        # Deep learning tagging
        dl_request = DeepLearningTaggingRequest(
            request_id=request.request_id,
            content=request.content,
            model_type="transformer",
            confidence_threshold=0.7
        )
        enrichment_results['deep_learning'] = app.state.enrichment_engine.tag_deep_learning(dl_request)
        
        logger.info(f"Enrichment completed for request: {request.request_id}")
        
        return {
            "success": True,
            "request_id": request.request_id,
            "tags": enrichment_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in enrichment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/competency", response_model=TaggingResult)
async def tag_competency(request: CompetencyTaggingRequest):
    """Competency tagging endpoint"""
    try:
        result = app.state.enrichment_engine.tag_competencies(request)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="competency",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in competency tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/pedagogy", response_model=TaggingResult)
async def tag_pedagogy(request: PedagogyTaggingRequest):
    """Pedagogy tagging endpoint"""
    try:
        result = app.state.enrichment_engine.tag_pedagogy(request)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="pedagogy",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in pedagogy tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/assessment", response_model=TaggingResult)
async def tag_assessment(request: AssessmentTaggingRequest):
    """Assessment tagging endpoint"""
    try:
        result = app.state.enrichment_engine.tag_assessment(request)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="assessment",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in assessment tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/cognitive", response_model=TaggingResult)
async def tag_cognitive_level(request: CognitiveLevelTaggingRequest):
    """Cognitive level tagging endpoint"""
    try:
        result = app.state.enrichment_engine.tag_cognitive_level(request)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="cognitive_level",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in cognitive level tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/objective", response_model=TaggingResult)
async def tag_learning_objective(request: LearningObjectiveTaggingRequest):
    """Learning objective tagging endpoint"""
    try:
        result = app.state.enrichment_engine.tag_learning_objectives(request)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="learning_objective",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in learning objective tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/deep_learning", response_model=TaggingResult)
async def tag_deep_learning(request: DeepLearningTaggingRequest):
    """Deep learning tagging endpoint"""
    try:
        result = app.state.enrichment_engine.tag_deep_learning(request)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="deep_learning",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in deep learning tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tag/taxonomy", response_model=TaggingResult)
async def tag_taxonomy(request: TaxonomyTaggingRequest):
    """Taxonomy tagging endpoint - moved from chunk service"""
    try:
        result = app.state.enrichment_engine.tag_taxonomy(request.content, request.context)
        
        return TaggingResult(
            request_id=request.request_id,
            tagging_type="taxonomy",
            tags=result.get('tags', []),
            confidence_scores=result.get('confidence_scores', []),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.error(f"Error in taxonomy tagging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics")
async def get_metrics():
    """Get performance metrics"""
    return app.state.enrichment_engine.performance_metrics
    
    # Import and start RabbitMQ consumer if enabled
    if ENABLE_RABBITMQ_CONSUMER:
        from .consumer import AsyncSemanticEnrichmentConsumer
        consumer = AsyncSemanticEnrichmentConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Semantic Enrichment Service",
    description="Advanced Enhancement - 6 Automated Tagging Systems",
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
        "service": "semantic-enrichment-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Semantic Enrichment endpoints
@app.post("/enrichment/competency")
async def tag_competencies(request: CompetencyTaggingRequest):
    """Automated competency tagging"""
    result = semantic_enrichment_engine.tag_competencies(request)
    return TaggingResult(
        request_id=request.request_id,
        tagging_type="competency_tagger",
        tags=result["tags"],
        confidence_scores=result["confidence_scores"],
        metadata=result["metadata"]
    )


@app.post("/enrichment/pedagogy")
async def tag_pedagogy(request: PedagogyTaggingRequest):
    """Automated pedagogy tagging"""
    result = semantic_enrichment_engine.tag_pedagogy(request)
    return TaggingResult(
        request_id=request.request_id,
        tagging_type="pedagogy_tagger",
        tags=result["tags"],
        confidence_scores=result["confidence_scores"],
        metadata=result["metadata"]
    )


@app.post("/enrichment/assessment")
async def tag_assessment(request: AssessmentTaggingRequest):
    """Automated assessment tagging"""
    result = semantic_enrichment_engine.tag_assessment(request)
    return TaggingResult(
        request_id=request.request_id,
        tagging_type="assessment_tagger",
        tags=result["tags"],
        confidence_scores=result["confidence_scores"],
        metadata=result["metadata"]
    )


@app.post("/enrichment/cognitive-level")
async def tag_cognitive_level(request: CognitiveLevelTaggingRequest):
    """Automated cognitive level tagging"""
    result = semantic_enrichment_engine.tag_cognitive_level(request)
    return TaggingResult(
        request_id=request.request_id,
        tagging_type="cognitive_level_tagger",
        tags=result["tags"],
        confidence_scores=result["confidence_scores"],
        metadata=result["metadata"]
    )


@app.post("/enrichment/learning-objective")
async def tag_learning_objective(request: LearningObjectiveTaggingRequest):
    """Automated learning objective tagging"""
    result = semantic_enrichment_engine.tag_learning_objectives(request)
    return TaggingResult(
        request_id=request.request_id,
        tagging_type="learning_objective_tagger",
        tags=result["tags"],
        confidence_scores=result["confidence_scores"],
        metadata=result["metadata"]
    )


@app.post("/enrichment/deep-learning")
async def tag_deep_learning(request: DeepLearningTaggingRequest):
    """Deep learning-based tagging"""
    result = semantic_enrichment_engine.tag_deep_learning(request)
    return TaggingResult(
        request_id=request.request_id,
        tagging_type="deep_learning_tagger",
        tags=result["tags"],
        confidence_scores=result["confidence_scores"],
        metadata=result["metadata"]
    )


# Performance monitoring
@app.get("/enrichment/performance")
async def get_performance_metrics():
    """Get tagging performance metrics"""
    return semantic_enrichment_engine.performance_metrics


@app.get("/enrichment/taggers")
async def get_available_taggers():
    """Get available tagging systems"""
    return {
        "taggers": [
            {
                "name": "competency_tagger",
                "description": "Tags content with subject competencies and curriculum alignment",
                "parameters": ["curriculum_phase", "subject"]
            },
            {
                "name": "pedagogy_tagger",
                "description": "Tags content with pedagogical methods and approaches",
                "parameters": ["grade_level"]
            },
            {
                "name": "assessment_tagger",
                "description": "Tags content with assessment types and question formats",
                "parameters": ["assessment_type"]
            },
            {
                "name": "cognitive_level_tagger",
                "description": "Tags content with Bloom's taxonomy cognitive levels",
                "parameters": ["target_levels"]
            },
            {
                "name": "learning_objective_tagger",
                "description": "Tags content with learning objective domains",
                "parameters": ["curriculum_standards"]
            },
            {
                "name": "deep_learning_tagger",
                "description": "Uses neural networks for advanced content tagging",
                "parameters": ["model_type", "confidence_threshold"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8021)