"""
AI Platform - Monolith Architecture
Single unified application combining all microservices
"""
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sys.path.append('/app')

# DOCUMENT INGESTION
from app.services.document_ingestion.parser_service import ParserService
from app.services.document_ingestion.pipeline_tracker_service import PipelineTrackerService

# PARSER SERVICE COMPONENTS (Legacy Parser Service Migration)
# Note: TextExtractor import removed - legacy text_extractor.py contains ImageExtractor instead
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.extractors.layout_detector import LayoutDetector
from app.extractors.enhanced_layout_detector import EnhancedLayoutDetector
from app.extractors.formula_extractor import FormulaExtractor
from app.extractors.figure_extractor import FigureExtractor
from app.pipelines.document_pipeline import DocumentPipeline
from app.pipelines.modern_document_pipeline import ModernDocumentPipeline
from app.pipelines.reading_order_resolver import ReadingOrderResolver
from app.pipelines.region_classifier import RegionClassifier
from app.normalizers.content_normalizer import ContentNormalizer
from app.schemas.parser_schemas import (
    DocumentUploadResponse,
    ParseRequest,
    ParseResponse,
    ExtractionResult,
    DocumentStatus
)
# from app.messaging.rabbitmq_producer import ParserServiceProducer  # Commented out due to missing pika dependency

# CONTENT PROCESSING
from app.services.content_processing.semantic_chunk_service import SemanticChunkService
from app.services.content_processing.semantic_enrichment_service import SemanticEnrichmentService
from app.services.content_processing.minio_chunking_service import MinIOChunkingService

# SEMANTIC CHUNK SERVICE COMPONENTS (Legacy Migration)
from app.builders.chunk_builder import ChunkBuilder
from app.enrichers.chunk_enricher import ChunkEnricher
from app.hierarchy.hierarchy_detector import HierarchyDetector
from app.pedagogy.pedagogy_classifier import PedagogyClassifier
from app.taxonomy.taxonomy_tagger import TaxonomyTagger
# from app.services.content_processing.embedding_service import EmbeddingService  # Commented out - needs service wrapper
from app.services.content_processing.retrieval_service import RetrievalService
from app.services.content_processing.generation_service import GenerationService
from app.services.content_processing.ontology_validation_service import OntologyValidationService
from app.services.content_processing.vision_service import VisionService
from app.services.content_processing.metadata_service import MetadataService
# from app.services.content_processing.hallucination_guard_service import HallucinationGuardService  # Commented out - needs service wrapper
# from app.services.content_processing.reranking_service import RerankingService  # Commented out - needs service wrapper

# INTELLIGENCE
from app.services.intelligence.pedagogy_service import PedagogyService
from app.services.intelligence.learning_graph_service import LearningGraphService
from app.services.intelligence.recommendation_service import RecommendationService
from app.services.intelligence.strategic_analysis_service import StrategicAnalysisService
from app.services.intelligence.adaptive_learning_service import AdaptiveLearningService
from app.services.intelligence.assessment_service import AssessmentService
from app.services.intelligence.curriculum_service import CurriculumService
# from app.services.intelligence.educational_intelligence_service import EducationalIntelligenceService  # Commented out - needs service wrapper
# from app.services.intelligence.ai_agents_service import AIAgentsService  # Commented out - needs service wrapper
# from app.services.intelligence.educational_ontology_service import EducationalOntologyService  # Commented out - needs service wrapper
from app.services.intelligence.learning_progression_service import LearningProgressionService

# SUPPORT
# from app.services.support.monitoring_service import MonitoringService  # Commented out - needs service wrapper
# from app.services.support.notification_service import NotificationService  # Commented out - needs service wrapper
# from app.services.support.orchestration_service import OrchestrationService  # Commented out - needs service wrapper
# from app.services.support.gateway_service import GatewayService  # Commented out - needs service wrapper
from app.services.support.governance_service import GovernanceService
from app.services.support.observability_service import ObservabilityService
# from app.services.support.audit_service import AuditService  # Commented out - needs service wrapper
# from app.services.support.educational_observability_service import EducationalObservabilityService  # Commented out - needs service wrapper
# from app.services.support.moderation_service import ModerationService  # Commented out - needs service wrapper

# Configuration
# from app.core.config import settings  # Commented out - missing pydantic_settings dependency
# from app.core.logging import setup_logging  # Commented out - may have dependencies

# Setup logging
# logger = setup_logging("ai-platform-monolith")  # Commented out - missing dependencies
import logging
logger = logging.getLogger(__name__)

# Dummy settings for testing
class Settings:
    cors_origins = ["*"]
    title = "AI Platform Monolith"
    version = "1.0.0"
    description = "AI Platform Monolith Architecture"

settings = Settings()

# Initialize services (direct instantiation, no HTTP/gRPC)
parser_service = ParserService()
semantic_chunk_service = SemanticChunkService()
semantic_enrichment_service = SemanticEnrichmentService()
# embedding_service = EmbeddingService()  # Commented out - needs service wrapper
retrieval_service = RetrievalService()
generation_service = GenerationService()
pipeline_tracker_service = PipelineTrackerService()
ontology_validation_service = OntologyValidationService()
# hallucination_guard_service = HallucinationGuardService()  # Commented out - needs service wrapper
# reranking_service = RerankingService()  # Commented out - needs service wrapper

# Initialize additional services
adaptive_learning_service = AdaptiveLearningService()
assessment_service = AssessmentService()
curriculum_service = CurriculumService()
# educational_intelligence_service = EducationalIntelligenceService()  # Commented out - needs service wrapper
observability_service = ObservabilityService()
governance_service = GovernanceService()
learning_graph_service = LearningGraphService()
metadata_service = MetadataService()
# monitoring_service = MonitoringService()  # Commented out - needs service wrapper
# notification_service = NotificationService()  # Commented out - needs service wrapper
# orchestration_service = OrchestrationService()  # Commented out - needs service wrapper
pedagogy_service = PedagogyService()
recommendation_service = RecommendationService()
# retrieval_enhancement_service = RetrievalEnhancementService()  # Commented out - needs service wrapper
strategic_analysis_service = StrategicAnalysisService()
vision_service = VisionService()
# ai_agents_service = AIAgentsService()  # Commented out - needs service wrapper
# gateway_service = GatewayService()  # Commented out - needs service wrapper
# educational_ontology_service = EducationalOntologyService()  # Commented out - needs service wrapper
learning_progression_service = LearningProgressionService()
# audit_service = AuditService()  # Commented out - needs service wrapper
# educational_observability_service = EducationalObservabilityService()  # Commented out - needs service wrapper
# moderation_service = ModerationService()  # Commented out - needs service wrapper

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    logger.info("Starting AI Platform Monolith")
    
    # Initialize parser-service components (Legacy Parser Service Migration)
    try:
        # Initialize modern pipeline components
        app.state.layout_detector = EnhancedLayoutDetector()
        app.state.reading_order_resolver = ReadingOrderResolver()
        app.state.region_classifier = RegionClassifier()
        
        # Initialize extractors (region-aware)
        app.state.ocr_extractor = OCRExtractor()
        app.state.table_extractor = TableExtractor()
        app.state.formula_extractor = FormulaExtractor()
        app.state.figure_extractor = FigureExtractor()
        
        # Initialize modern pipeline
        app.state.modern_document_pipeline = ModernDocumentPipeline(
            layout_detector=app.state.layout_detector,
            reading_order_resolver=app.state.reading_order_resolver,
            region_classifier=app.state.region_classifier,
            ocr_extractor=app.state.ocr_extractor,
            table_extractor=app.state.table_extractor,
            formula_extractor=app.state.formula_extractor,
            figure_extractor=app.state.figure_extractor
        )
        
        # Initialize RabbitMQ producer for service communication
        # try:
        #     app.state.rabbitmq_producer = ParserServiceProducer()
        #     logger.info("RabbitMQ producer initialized successfully")
        # except Exception as e:
        #     logger.warning(f"Failed to initialize RabbitMQ producer: {e}")
        #     app.state.rabbitmq_producer = None
        app.state.rabbitmq_producer = None  # Temporarily disabled due to missing pika dependency
        
        # Keep old pipeline for backward compatibility
        # Note: TextExtractor removed - legacy text_extractor.py contains ImageExtractor instead
        app.state.image_extractor = ImageExtractor()
        app.state.layout_detector_old = LayoutDetector()
        app.state.content_normalizer = ContentNormalizer()
        # DocumentPipeline requires text_extractor, but since TextExtractor doesn't exist in legacy,
        # we'll use ImageExtractor as a workaround or skip the old pipeline initialization
        # app.state.document_pipeline = DocumentPipeline(
        #     text_extractor=app.state.text_extractor,  # This would fail
        #     table_extractor=app.state.table_extractor,
        #     image_extractor=app.state.image_extractor,
        #     ocr_extractor=app.state.ocr_extractor,
        #     layout_detector=app.state.layout_detector_old,
        #     content_normalizer=app.state.content_normalizer
        # )
        
        logger.info("Parser service components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing parser service components: {str(e)}")
        raise
    
    # Initialize all services
    try:
        parser_service.initialize()
        semantic_chunk_service.initialize()
        semantic_enrichment_service.initialize()
        
        # Initialize semantic-chunk-service components (Legacy Migration)
        try:
            app.state.chunk_builder = ChunkBuilder()
            app.state.chunk_enricher = ChunkEnricher()
            app.state.hierarchy_detector = HierarchyDetector()
            app.state.pedagogy_classifier = PedagogyClassifier()
            app.state.taxonomy_tagger = TaxonomyTagger()
            app.state.minio_chunking_service = MinIOChunkingService()
            logger.info("Semantic chunk service components initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize some semantic chunk components: {e}")
        
        # embedding_service.initialize()
        retrieval_service.initialize()
        generation_service.initialize()
        pipeline_tracker_service.initialize()
        ontology_validation_service.initialize()
        # hallucination_guard_service.initialize()
        # reranking_service.initialize()
        
        # Initialize additional services
        adaptive_learning_service.initialize()
        assessment_service.initialize()
        curriculum_service.initialize()
        # educational_intelligence_service.initialize()
        observability_service.initialize()
        governance_service.initialize()
        learning_graph_service.initialize()
        metadata_service.initialize()
        # monitoring_service.initialize()
        # notification_service.initialize()
        # orchestration_service.initialize()
        pedagogy_service.initialize()
        recommendation_service.initialize()
        # retrieval_enhancement_service.initialize()
        strategic_analysis_service.initialize()
        vision_service.initialize()
        # ai_agents_service.initialize()
        # gateway_service.initialize()
        # educational_ontology_service.initialize()
        learning_progression_service.initialize()
        # audit_service.initialize()
        # educational_observability_service.initialize()
        # moderation_service.initialize()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        raise
    
    yield
    logger.info("Shutting down AI Platform Monolith")
    # Cleanup if needed

# Create FastAPI app
app = FastAPI(
    title="AI Platform - Monolith",
    description="Unified AI Platform for Educational Intelligence (Monolith Architecture)",
    version="2.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import API routes
from app.api.document_ingestion.parser_routes import parser_router
from app.api.content_processing.chunk_routes import chunk_router
from app.api.content_processing.enrichment_routes import enrichment_router
# from app.api.content_processing.embedding_routes import embedding_router  # Commented out - circular import
# from app.api.content_processing.retrieval_routes import retrieval_router  # Commented out - circular import
# from app.api.content_processing.generation_routes import generation_router  # Commented out - circular import
from app.api.content_processing.ontology_routes import ontology_router

# Import additional API routes
# from app.api.intelligence.adaptive_learning_routes import adaptive_learning_router  # Commented out - circular import
# from app.api.intelligence.assessment_routes import assessment_router  # Commented out - circular import
# from app.api.intelligence.curriculum_routes import curriculum_router  # Commented out - circular import
# from app.api.intelligence.educational_intelligence_routes import educational_intelligence_router  # Commented out - circular import
from app.api.support.observability_routes import observability_router
# from app.api.support.governance_routes import governance_router  # Commented out - circular import
# from app.api.intelligence.learning_graph_routes import learning_graph_router  # Commented out - circular import
from app.api.content_processing.metadata_routes import metadata_router
# from app.api.support.monitoring_routes import monitoring_router  # Commented out - circular import
# from app.api.support.notification_routes import notification_router  # Commented out - circular import
# from app.api.support.orchestration_routes import orchestration_router  # Commented out - circular import
# from app.api.intelligence.pedagogy_routes import pedagogy_router  # Commented out - circular import
# from app.api.intelligence.recommendation_routes import recommendation_router  # Commented out - circular import
# from app.api.content_processing.retrieval_enhancement_routes import retrieval_enhancement_router  # Commented out - circular import
# from app.api.intelligence.strategic_analysis_routes import strategic_analysis_router  # Commented out - circular import
# from app.api.content_processing.vision_routes import vision_router  # Commented out - circular import
# from app.api.intelligence.ai_agents_routes import ai_agents_router  # Commented out - circular import
# from app.api.support.gateway_routes import gateway_router  # Commented out - circular import

# Import new API routes
# from app.api.intelligence.educational_ontology_routes import educational_ontology_router  # Commented out - circular import
# from app.api.support.audit_routes import audit_router  # Commented out - circular import
# from app.api.support.educational_observability_routes import educational_observability_router  # Commented out - circular import
# from app.api.content_processing.hallucination_guard_routes import hallucination_guard_router  # Commented out - circular import
# from app.api.intelligence.learning_progression_routes import learning_progression_router  # Commented out - circular import
# from app.api.support.moderation_routes import moderation_router  # Commented out - circular import
# from app.api.content_processing.reranking_routes import reranking_router  # Commented out - circular import

# Register API routes
app.include_router(parser_router, prefix="/api/v1/parser", tags=["parser"])
app.include_router(chunk_router, prefix="/api/v1/chunk", tags=["semantic-chunk"])
app.include_router(enrichment_router, prefix="/api/v1/enrichment", tags=["semantic-enrichment"])
# app.include_router(embedding_router, prefix="/api/v1/embedding", tags=["embedding"])  # Commented out - circular import
# app.include_router(retrieval_router, prefix="/api/v1/retrieval", tags=["retrieval"])  # Commented out - circular import
# app.include_router(generation_router, prefix="/api/v1/generation", tags=["generation"])  # Commented out - circular import
app.include_router(ontology_router, prefix="/api/v1/ontology", tags=["ontology"])

# Register additional API routes
# app.include_router(adaptive_learning_router, prefix="/api/v1/adaptive-learning", tags=["adaptive-learning"])  # Commented out - circular import
# app.include_router(assessment_router, prefix="/api/v1/assessment", tags=["assessment"])  # Commented out - circular import
# app.include_router(curriculum_router, prefix="/api/v1/curriculum", tags=["curriculum"])  # Commented out - circular import
# app.include_router(educational_intelligence_router, prefix="/api/v1/educational-intelligence", tags=["educational-intelligence"])  # Commented out - circular import
app.include_router(observability_router, prefix="/api/v1/observability", tags=["observability"])
# app.include_router(governance_router, prefix="/api/v1/governance", tags=["governance"])  # Commented out - circular import
# app.include_router(learning_graph_router, prefix="/api/v1/learning-graph", tags=["learning-graph"])  # Commented out - circular import
app.include_router(metadata_router, prefix="/api/v1/metadata", tags=["metadata"])
# app.include_router(monitoring_router, prefix="/api/v1/monitoring", tags=["monitoring"])  # Commented out - circular import
# app.include_router(notification_router, prefix="/api/v1/notification", tags=["notification"])  # Commented out - circular import
# app.include_router(orchestration_router, prefix="/api/v1/orchestration", tags=["orchestration"])  # Commented out - circular import
# app.include_router(pedagogy_router, prefix="/api/v1/pedagogy", tags=["pedagogy"])  # Commented out - circular import
# app.include_router(recommendation_router, prefix="/api/v1/recommendation", tags=["recommendation"])  # Commented out - circular import
# app.include_router(retrieval_enhancement_router, prefix="/api/v1/retrieval-enhancement", tags=["retrieval-enhancement"])  # Commented out - circular import
# app.include_router(strategic_analysis_router, prefix="/api/v1/strategic-analysis", tags=["strategic-analysis"])  # Commented out - circular import
# app.include_router(vision_router, prefix="/api/v1/vision", tags=["vision"])  # Commented out - circular import
# app.include_router(ai_agents_router, prefix="/api/v1/ai-agents", tags=["ai-agents"])  # Commented out - circular import
# app.include_router(gateway_router, prefix="/api/v1/gateway", tags=["gateway"])  # Commented out - circular import

# Register new API routes
# app.include_router(educational_ontology_router, prefix="/api/v1/educational-ontology", tags=["educational-ontology"])  # Commented out - circular import
# app.include_router(audit_router, prefix="/api/v1/audit", tags=["audit"])  # Commented out - circular import
# app.include_router(educational_observability_router, prefix="/api/v1/educational-observability", tags=["educational-observability"])  # Commented out - circular import
# app.include_router(hallucination_guard_router, prefix="/api/v1/hallucination-guard", tags=["hallucination-guard"])  # Commented out - circular import
# app.include_router(learning_progression_router, prefix="/api/v1/learning-progression", tags=["learning-progression"])  # Commented out - circular import
# app.include_router(moderation_router, prefix="/api/v1/moderation", tags=["moderation"])  # Commented out - circular import
# app.include_router(reranking_router, prefix="/api/v1/reranking", tags=["reranking"])  # Commented out - circular import

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check for monolith"""
    return {
        "status": "healthy",
        "architecture": "monolith",
        "services": {
            "parser_service": parser_service.health(),
            "semantic_chunk_service": semantic_chunk_service.health(),
            "semantic_enrichment_service": semantic_enrichment_service.health(),
            # "embedding_service": embedding_service.health(),
            "retrieval_service": retrieval_service.health(),
            "generation_service": generation_service.health(),
            "pipeline_tracker_service": pipeline_tracker_service.health(),
            "ontology_validation_service": ontology_validation_service.health(),
            # "hallucination_guard_service": hallucination_guard_service.health(),
            # "reranking_service": reranking_service.health(),
            "adaptive_learning_service": adaptive_learning_service.health(),
            "assessment_service": assessment_service.health(),
            "curriculum_service": curriculum_service.health(),
            # "educational_intelligence_service": educational_intelligence_service.health(),
            "observability_service": observability_service.health(),
            "governance_service": governance_service.health(),
            "learning_graph_service": learning_graph_service.health(),
            "metadata_service": metadata_service.health(),
            # "monitoring_service": monitoring_service.health(),
            # "notification_service": notification_service.health(),
            # "orchestration_service": orchestration_service.health(),
            "pedagogy_service": pedagogy_service.health(),
            "recommendation_service": recommendation_service.health(),
            # "retrieval_enhancement_service": retrieval_enhancement_service.health(),
            "strategic_analysis_service": strategic_analysis_service.health(),
            "vision_service": vision_service.health(),
            # "ai_agents_service": ai_agents_service.health(),
            # "gateway_service": gateway_service.health(),
            # "educational_ontology_service": educational_ontology_service.health(),
            "learning_progression_service": learning_progression_service.health(),
            # "audit_service": audit_service.health(),
            # "educational_observability_service": educational_observability_service.health(),
            # "moderation_service": moderation_service.health()
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Platform - Monolith Architecture",
        "version": "2.0.0",
        "description": "Unified Educational AI Platform",
        "architecture": "monolith",
        "endpoints": {
            "parser": "/api/v1/parser",
            "chunk": "/api/v1/chunk", 
            "enrichment": "/api/v1/enrichment",
            "embedding": "/api/v1/embedding",
            "retrieval": "/api/v1/retrieval",
            "generation": "/api/v1/generation",
            "ontology": "/api/v1/ontology",
            "hallucination_guard": "/api/v1/hallucination-guard",
            "reranking": "/api/v1/reranking",
            "adaptive_learning": "/api/v1/adaptive-learning",
            "assessment": "/api/v1/assessment",
            "curriculum": "/api/v1/curriculum",
            "educational_intelligence": "/api/v1/educational-intelligence",
            "observability": "/api/v1/observability",
            "governance": "/api/v1/governance",
            "learning_graph": "/api/v1/learning-graph",
            "metadata": "/api/v1/metadata",
            "monitoring": "/api/v1/monitoring",
            "notification": "/api/v1/notification",
            "orchestration": "/api/v1/orchestration",
            "pedagogy": "/api/v1/pedagogy",
            "recommendation": "/api/v1/recommendation",
            "retrieval_enhancement": "/api/v1/retrieval-enhancement",
            "strategic_analysis": "/api/v1/strategic-analysis",
            "vision": "/api/v1/vision",
            "ai_agents": "/api/v1/ai-agents",
            "gateway": "/api/v1/gateway",
            "educational_ontology": "/api/v1/educational-ontology",
            "learning_progression": "/api/v1/learning-progression",
            "audit": "/api/v1/audit",
            "educational_observability": "/api/v1/educational-observability",
            "moderation": "/api/v1/moderation"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )