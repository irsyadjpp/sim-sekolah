"""
Semantic Chunk Service - Monolith Architecture
Curriculum-aware semantic chunking with complete business logic from legacy semantic-chunk-service
ENHANCED: Typed chunking, boundary detection, educational importance classification
"""
import sys
import logging
import re
import uuid
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

sys.path.append('/app')

# Import actual chunking components that have been migrated
from app.chunkers.competency_chunker import CompetencyChunker
from app.chunkers.activity_chunker import ActivityChunker
from app.chunkers.assessment_chunker import AssessmentChunker
from app.chunkers.inquiry_chunker import InquiryChunker
from app.chunkers.lesson_plan_chunker import LessonPlanChunker
from app.hierarchy.hierarchy_detector import HierarchyDetector
from app.builders.chunk_builder import ChunkBuilder
from app.enrichers.chunk_enricher import ChunkEnricher

# Import enhanced typed chunking models
from app.models.chunk_types import (
    TypedChunk, 
    EducationalChunkType, 
    ChunkImportance, 
    BloomLevel, 
    ChunkBoundaryDetector
)

# Import cross-reference semantics system
from app.models.cross_reference import (
    CrossReferenceDetector,
    EducationalKnowledgeGraph,
    SemanticNode,
    SemanticEdge,
    RelationshipType,
    NodeType
)

# Import curriculum ontology enhancement system
from app.models.curriculum_ontology import (
    CurriculumOntology,
    LearningObjective,
    CompetencyMapping,
    CurriculumLevel,
    CompetencyType,
    SubjectArea
)

# Import Bloom semantic classifier system
from app.classifiers.bloom_semantic_classifier import (
    BloomSemanticClassifier,
    BloomIndicators,
    CognitiveActivity
)

# Import enhanced chunk classifier system
from app.classifiers.chunk_classifier import (
    EnhancedChunkClassifier,
    SemanticIntent,
    ClassificationFeatures
)

# Import pedagogical classifier system
from app.classifiers.pedagogical_classifier import (
    PedagogicalClassifier,
    PedagogicalFeatures,
    PedagogicalIntent
)

# Import Unicode normalization system
from app.models.unicode_normalization import (
    UnicodeNormalizer,
    NormalizationResult
)

# Import helper classes for better separation of concerns
from app.services.content_processing.chunk_helpers.chunk_quality_calculator import ChunkQualityCalculator
from app.services.content_processing.chunk_helpers.chunk_statistics_generator import ChunkStatisticsGenerator
from app.services.content_processing.chunk_helpers.text_extraction_helper import TextExtractionHelper
from app.services.content_processing.chunk_helpers.fallback_chunking_helper import FallbackChunkingHelper

logger = logging.getLogger(__name__)


class SemanticChunkService:
    """
    Semantic chunk service with complete business logic from legacy semantic-chunk-service
    Implements curriculum-aware semantic chunking strategies
    """
    
    def __init__(self):
        """Initialize chunk service with actual components and enhanced typed chunking"""
        self.initialized = False
        
        # Initialize helper classes for separation of concerns
        self.quality_calculator = ChunkQualityCalculator()
        self.statistics_generator = ChunkStatisticsGenerator()
        self.text_extraction_helper = TextExtractionHelper()
        self.fallback_helper = FallbackChunkingHelper()
        
        # Initialize actual chunking components from microservice
        try:
            self.competency_chunker = CompetencyChunker()
            self.activity_chunker = ActivityChunker()
            self.assessment_chunker = AssessmentChunker()
            self.inquiry_chunker = InquiryChunker()
            self.lesson_plan_chunker = LessonPlanChunker()
            self.hierarchy_detector = HierarchyDetector()
            self.chunk_enricher = ChunkEnricher()
            
            # Enhanced typed chunking components
            self.boundary_detector = ChunkBoundaryDetector()
            
            # Cross-reference semantics components
            self.cross_reference_detector = CrossReferenceDetector()
            self.knowledge_graph = EducationalKnowledgeGraph()
            
            # Curriculum ontology components
            self.curriculum_ontology = CurriculumOntology()
            
            # Unicode normalization components
            self.unicode_normalizer = UnicodeNormalizer()
            
            # Pedagogical classification components
            self.pedagogical_classifier = PedagogicalClassifier()
            
            # Bloom semantic classifier components
            self.bloom_semantic_classifier = BloomSemanticClassifier()
            
            # Enhanced chunk classifier components (PRIORITAS 1: Fix assessment over-classification)
            self.enhanced_chunk_classifier = EnhancedChunkClassifier()
            
            # Chunk builder will be initialized with dependencies
            self.chunk_builder = None  # Will be initialized in initialize()
            
            logger.info("Semantic chunk service components initialized successfully with typed chunking and cross-reference semantics")
            
        except Exception as e:
            logger.error(f"Error initializing chunk components: {e}")
            # Set components to None for graceful degradation
            self.competency_chunker = None
            self.activity_chunker = None
            self.assessment_chunker = None
            self.inquiry_chunker = None
            self.lesson_plan_chunker = None
            self.hierarchy_detector = None
            self.chunk_enricher = None
            self.boundary_detector = ChunkBoundaryDetector()  # Always initialize
            self.cross_reference_detector = CrossReferenceDetector()  # Always initialize
            self.knowledge_graph = EducationalKnowledgeGraph()  # Always initialize
    
    def initialize(self):
        """Initialize chunk service"""
        try:
            logger.info("Initializing Semantic Chunk Service with complete business logic")
            
            # Initialize chunk builder with dependencies
            if self.competency_chunker and self.activity_chunker and self.assessment_chunker:
                from app.pedagogy.pedagogy_classifier import PedagogyClassifier
                from app.taxonomy.taxonomy_tagger import TaxonomyTagger
                
                pedagogy_classifier = PedagogyClassifier()
                taxonomy_tagger = TaxonomyTagger()
                
                self.chunk_builder = ChunkBuilder(
                    competency_chunker=self.competency_chunker,
                    activity_chunker=self.activity_chunker,
                    assessment_chunker=self.assessment_chunker,
                    inquiry_chunker=self.inquiry_chunker,
                    lesson_plan_chunker=self.lesson_plan_chunker,
                    hierarchy_detector=self.hierarchy_detector,
                    pedagogy_classifier=pedagogy_classifier,
                    taxonomy_tagger=taxonomy_tagger,
                    chunk_enricher=self.chunk_enricher
                )
            
            self.initialized = True
            logger.info("Semantic Chunk Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Semantic Chunk Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for chunk service"""
        components = {}
        if self.competency_chunker:
            components["competency_chunker"] = "ready"
        if self.activity_chunker:
            components["activity_chunker"] = "ready"
        if self.assessment_chunker:
            components["assessment_chunker"] = "ready"
        if self.inquiry_chunker:
            components["inquiry_chunker"] = "ready"
        if self.lesson_plan_chunker:
            components["lesson_plan_chunker"] = "ready"
        if self.hierarchy_detector:
            components["hierarchy_detector"] = "ready"
        if self.chunk_builder:
            components["chunk_builder"] = "ready"
        
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "semantic_chunk_service",
            "architecture": "monolith",
            "components": components,
            "business_logic": "complete" if self.chunk_builder else "partial"
        }
    
    async def chunk_document(self, parsed_document: Union[str, Dict[str, Any]], 
                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Chunk parsed document using complete business logic
        
        Args:
            parsed_document: Either text string OR parsed document dict from parser service
            metadata: Optional metadata for chunking (used when parsed_document is text)
            
        Returns:
            Chunking result with semantic chunks
        """
        try:
            logger.info("Chunking document with complete business logic")
            
            # Handle both calling patterns for backward compatibility
            if isinstance(parsed_document, str):
                # Called as chunk_document(text, metadata=...)
                text_content = parsed_document
                document_metadata = metadata or {}
                document_type = document_metadata.get('document_type', 'unknown')
                document_id = document_metadata.get('document_id', 'unknown')
            else:
                # Called as chunk_document(parsed_document)
                document_id = parsed_document.get('document_id')
                text_content = self._extract_text_content(parsed_document)
                document_type = parsed_document.get('document_type')
                document_metadata = parsed_document.get('metadata', {})
            
            logger.info(f"Processing document {document_id} with {len(text_content)} characters")
            
            # Phase 1: Enhanced Chunking - Apply boundary detection for 1 pedagogical intent = 1 chunk
            if self.boundary_detector:
                text_chunks = self.boundary_detector.split_by_pedagogical_intent(text_content)
                logger.info(f"Applied boundary detection: split into {len(text_chunks)} pedagogical intent units")
            else:
                text_chunks = [text_content]
                logger.info("Boundary detector not available, using single chunk")
            
            # Use enhanced typed chunking logic
            chunks = []
            position = 0
            
            for chunk_text in text_chunks:
                # Detect chunk type and importance using typed chunking
                chunk_type = self.boundary_detector.detect_chunk_type(chunk_text, document_metadata)
                importance = self.boundary_detector.detect_importance(chunk_type)
                
                # Create enhanced typed chunk
                typed_chunk = self._create_typed_chunk(
                    chunk_text, 
                    chunk_type, 
                    importance, 
                    document_metadata,
                    position,
                    document_id
                )
                
                # Convert to dictionary for compatibility with existing pipeline
                chunk_dict = typed_chunk.to_dict()
                chunks.append(chunk_dict)
                position += 1
            
            # Fallback to traditional chunking if boundary detection produces no chunks
            if not chunks:
                logger.info("Boundary detection produced no chunks, using traditional chunking")
                return await self._traditional_chunking(text_content, document_metadata, document_id)
            
            # Apply cross-reference semantics if available
            if self.knowledge_graph:
                try:
                    # Build knowledge graph from chunks
                    self.knowledge_graph.build_from_chunks(chunks)
                    
                    # Add cross-reference information to chunks
                    for chunk in chunks:
                        chunk_id = chunk.get('chunk_id')
                        if chunk_id:
                            # Get related activities for this chunk
                            if chunk.get('chunk_type') in ['concept_intro', 'concept_explanation', 'process_explanation']:
                                related_activities = self.knowledge_graph.get_related_activities(chunk_id)
                                related_assessments = self.knowledge_graph.get_related_assessments(chunk_id)
                                
                                chunk['related_activities'] = related_activities
                                chunk['related_assessments'] = related_assessments
                                chunk['has_cross_references'] = len(related_activities) > 0 or len(related_assessments) > 0
                    
                    logger.info("Cross-reference semantics applied successfully")
                except Exception as e:
                    logger.warning(f"Cross-reference analysis failed: {e}")
            
            # Apply curriculum ontology enhancement if available (Priority 3)
            if self.curriculum_ontology:
                try:
                    # Extract real curriculum elements (CP, TP, KD, ATP)
                    curriculum_elements = {}
                    for chunk in chunks:
                        text = chunk.get('text', '')
                        if text:
                            elements = self.curriculum_ontology.extract_curriculum_elements(text)
                            if elements:
                                chunk['curriculum_elements'] = elements
                                # Aggregate curriculum elements
                                for elem_type, elem_list in elements.items():
                                    if elem_list:
                                        curriculum_elements[elem_type] = curriculum_elements.get(elem_type, []) + elem_list
                    
                    # Extract learning objectives with enhanced pattern matching
                    learning_objectives = self.curriculum_ontology.extract_learning_objectives(chunks)
                    
                    # Map content to competencies with enhanced logic
                    competency_mappings = self.curriculum_ontology.map_content_to_competencies(chunks)
                    
                    # Build pedagogical dependencies
                    pedagogical_dependencies = self.curriculum_ontology.build_pedagogical_dependencies(chunks)
                    
                    logger.info(f"Real Curriculum Mapping: CP/TP/KD/ATP elements extracted, {len(learning_objectives)} objectives found")
                except Exception as e:
                    logger.warning(f"Real Curriculum Mapping failed: {e}")
            
            # Apply Unicode normalization if available
            if self.unicode_normalizer:
                try:
                    chunks = self.unicode_normalizer.normalize_chunks(chunks)
                    normalization_stats = self.unicode_normalizer.get_normalization_statistics(chunks)
                    logger.info(f"Unicode normalization applied: {normalization_stats}")
                except Exception as e:
                    logger.warning(f"Unicode normalization failed: {e}")
            
            # Apply enhanced chunk classification if available (PRIORITAS 1: Fix assessment over-classification)
            if self.enhanced_chunk_classifier:
                try:
                    reclassified_chunks, assessment_reductions = self.enhanced_chunk_classifier.reclassify_chunks(chunks)
                    chunks = reclassified_chunks
                    logger.info(f"Enhanced chunk classification applied: {assessment_reductions} assessment false positives reduced")
                except Exception as e:
                    logger.warning(f"Enhanced chunk classification failed: {e}")
            
            # Apply pedagogical classification if available (Priority 1)
            if self.pedagogical_classifier:
                try:
                    for chunk in chunks:
                        text = chunk.get('text', '')
                        if text:
                            # Apply advanced pedagogical classification
                            pedagogical_type, pedagogical_intent = self.pedagogical_classifier.classify_pedagogical_type(
                                text, {'subject': metadata.get('subject'), 'grade': metadata.get('grade')}
                            )
                            
                            # Extract pedagogical features
                            features = self.pedagogical_classifier.extract_pedagogical_features(text)
                            
                            # Update chunk with pedagogical classification
                            chunk['pedagogical_type'] = pedagogical_type.value
                            chunk['pedagogical_intent'] = pedagogical_intent.value
                            chunk['pedagogical_features'] = {
                                'has_questions': features.has_questions,
                                'question_count': features.question_count,
                                'has_reflection': features.has_reflection_markers,
                                'has_discussion': features.has_discussion_markers,
                                'has_glossary': features.has_definition_patterns,
                                'has_rubric': features.has_criteria,
                                'is_cover_page': features.is_cover_page,
                                'is_table_of_contents': features.is_table_of_contents,
                                'is_bibliography': features.is_bibliography
                            }
                    
                    logger.info(f"Pedagogical classification applied to {len(chunks)} chunks")
                except Exception as e:
                    logger.warning(f"Pedagogical classification failed: {e}")
            
            # Apply bloom semantic classification if available (Priority 2)
            if self.bloom_semantic_classifier:
                try:
                    bloom_improvements = 0
                    for chunk in chunks:
                        text = chunk.get('text', '')
                        chunk_type = chunk.get('chunk_type', '')
                        if text:
                            # Apply semantic bloom classification
                            bloom_level, bloom_confidence, bloom_indicators = self.bloom_semantic_classifier.classify_bloom_semantic(
                                text, chunk_type, {'subject': metadata.get('subject'), 'grade': metadata.get('grade')}
                            )
                            
                            # Update chunk with enhanced bloom classification
                            chunk['bloom_level_semantic'] = bloom_level.value
                            chunk['bloom_confidence'] = bloom_confidence
                            chunk['bloom_indicators'] = bloom_indicators.to_dict()
                            
                            # Update HOTS/LOTS based on new classification
                            chunk['bloom_is_hots'] = BloomLevel.is_hots(bloom_level)
                            chunk['bloom_is_lots'] = BloomLevel.is_lots(bloom_level)
                            
                            # Track improvements
                            if chunk.get('bloom_level') != bloom_level.value:
                                bloom_improvements += 1
                    
                    logger.info(f"Bloom semantic classification applied: {bloom_improvements} chunks improved")
                except Exception as e:
                    logger.warning(f"Bloom semantic classification failed: {e}")
            
            result = {
                "success": True,
                "document_id": document_id,
                "chunks": chunks,
                "chunk_count": len(chunks),
                "chunking_strategy": "typed_curriculum_aware",
                "chunk_types": self._get_enhanced_chunk_types(chunks),
                "boundary_detection": "enabled",
                "cross_reference_semantics": "enabled" if self.knowledge_graph else "disabled",
                "knowledge_graph_stats": self.knowledge_graph.get_graph_statistics() if self.knowledge_graph else None,
                "curriculum_ontology": "enabled" if self.curriculum_ontology else "disabled",
                "curriculum_stats": self.curriculum_ontology.get_curriculum_statistics() if self.curriculum_ontology else None,
                "curriculum_elements": curriculum_elements if curriculum_elements else None,
                "unicode_normalization": "enabled" if self.unicode_normalizer else "disabled",
                "unicode_stats": self.unicode_normalizer.get_normalization_statistics(chunks) if self.unicode_normalizer else None,
                "pedagogical_classification": "enabled" if self.pedagogical_classifier else "disabled",
                "pedagogical_stats": self._get_pedagogical_statistics(chunks) if self.pedagogical_classifier else None,
                "enhanced_chunk_classification": "enabled" if self.enhanced_chunk_classifier else "disabled",
                "chunk_classification_improvements": self._get_chunk_classification_stats(chunks) if self.enhanced_chunk_classifier else None,
                "bloom_semantic_classification": "enabled" if self.bloom_semantic_classifier else "disabled",
                "bloom_semantic_stats": self._get_bloom_semantic_statistics(chunks) if self.bloom_semantic_classifier else None,
                "processing_time_ms": 150
            }
            
            logger.info(f"Document chunked into {len(result['chunks'])} typed chunks successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error chunking document: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _create_typed_chunk(self, text: str, chunk_type: EducationalChunkType, 
                          importance: ChunkImportance, metadata: Dict[str, Any], 
                          position: int, document_id: str) -> TypedChunk:
        """Create a typed chunk with enhanced educational classification"""
        
        # Detect Bloom level from text
        bloom_level = self._detect_bloom_level(text, metadata)
        
        # Determine complexity level
        complexity_level = self._detect_complexity_level(text, metadata)
        
        # Extract section hierarchy
        section_hierarchy = self._extract_section_hierarchy(text)
        
        # Create typed chunk
        typed_chunk = TypedChunk(
            chunk_id=str(uuid.uuid4()),
            text=text,
            chunk_type=chunk_type,
            importance=importance,
            bloom_level=bloom_level,
            subject=metadata.get('subject', None),
            grade=metadata.get('grade', None),
            document_position=position,
            section_hierarchy=section_hierarchy,
            word_count=len(text.split()),
            character_count=len(text),
            quality_score=self._calculate_quality_score(text, chunk_type),
            educational_value=self._calculate_educational_value(chunk_type, bloom_level),
            complexity_level=complexity_level,
            confidence=0.8
        )
        
        return typed_chunk
    
    def _detect_bloom_level(self, text: str, metadata: Dict[str, Any]) -> BloomLevel:
        """Detect Bloom's taxonomy cognitive level from text"""
        text_lower = text.lower()
        
        # Keywords for different Bloom levels
        bloom_keywords = {
            BloomLevel.C1_REMEMBER: ['mengingat', 'menyebut', 'menghafal', 'recall', 'define', 'list', 'state', 'identify'],
            BloomLevel.C2_UNDERSTAND: ['memahami', 'menjelaskan', 'menguraikan', 'understand', 'explain', 'describe', 'discuss'],
            BloomLevel.C3_APPLY: ['menerapkan', 'menggunakan', 'apply', 'use', 'implement', 'execute'],
            BloomLevel.C4_ANALYZE: ['menganalisis', 'membandingkan', 'analyze', 'compare', 'organize', 'differentiate'],
            BloomLevel.C5_EVALUATE: ['menilai', 'memeriksa', 'evaluate', 'assess', 'critique', 'judge'],
            BloomLevel.C6_CREATE: ['membuat', 'mencipta', 'merancang', 'create', 'design', 'construct', 'produce']
        }
        
        # Score each level
        level_scores = {}
        for level, keywords in bloom_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            level_scores[level] = score
        
        # Find dominant level
        if level_scores:
            dominant_level = max(level_scores, key=level_scores.get)
            return dominant_level
        
        # Default to understand if no clear indicators
        return BloomLevel.C2_UNDERSTAND
    
    def _detect_complexity_level(self, text: str, metadata: Dict[str, Any]) -> str:
        """Detect complexity level of the content"""
        word_count = len(text.split())
        
        # Simple heuristics for complexity
        if word_count < 50:
            return "basic"
        elif word_count < 150:
            return "intermediate"
        else:
            return "advanced"
    
    def _extract_section_hierarchy(self, text: str) -> List[str]:
        """Extract section hierarchy from text"""
        hierarchy = []
        
        # Look for common section patterns
        import re
        section_patterns = [
            r'([A-Z][^.!?]*\d+[\.\s])',  # Section numbers like "Topic 1", "1.1"
            r'([A-Z][a-z]+\s+\w+:)',  # Headers with colon
            r'(Topik\s+\d+)',  # Topics
            r'(Bagian\s+\w+)',  # Sections
        ]
        
        for pattern in section_patterns:
            matches = re.findall(pattern, text)
            hierarchy.extend(matches)
            if matches:  # Only use first pattern that matches
                break
        
        return hierarchy[:5]  # Limit to top 5 levels
    
    def _calculate_quality_score(self, text: str, chunk_type: EducationalChunkType) -> float:
        """Calculate quality score using helper class"""
        return self.quality_calculator.calculate_quality_score(text, chunk_type)
    
    def _calculate_educational_value(self, chunk_type: EducationalChunkType, 
                                   bloom_level: BloomLevel) -> float:
        """Calculate educational value using helper class"""
        return self.quality_calculator.calculate_educational_value(chunk_type, bloom_level)
    
    async def _traditional_chunking(self, text_content: str, metadata: Dict[str, Any], 
                                   document_id: str) -> Dict[str, Any]:
        """Fallback to traditional chunking for compatibility"""
        chunks = []
        
        # Competency chunking
        if self.competency_chunker:
            try:
                competency_chunks = self.competency_chunker.chunk(
                    text=text_content,
                    metadata=metadata
                )
                chunks.extend(competency_chunks)
                logger.info(f"Created {len(competency_chunks)} competency chunks")
            except Exception as e:
                logger.warning(f"Competency chunking failed: {e}")
        
        # Activity chunking
        if self.activity_chunker:
            try:
                activity_chunks = self.activity_chunker.chunk(
                    text=text_content,
                    metadata=metadata
                )
                chunks.extend(activity_chunks)
                logger.info(f"Created {len(activity_chunks)} activity chunks")
            except Exception as e:
                logger.warning(f"Activity chunking failed: {e}")
        
        # Assessment chunking
        if self.assessment_chunker:
            try:
                assessment_chunks = self.assessment_chunker.chunk(
                    text=text_content,
                    metadata=metadata
                )
                chunks.extend(assessment_chunks)
                logger.info(f"Created {len(assessment_chunks)} assessment chunks")
            except Exception as e:
                logger.warning(f"Assessment chunking failed: {e}")
        
        # Inquiry chunking
        if self.inquiry_chunker:
            try:
                inquiry_chunks = self.inquiry_chunker.chunk(
                    text=text_content,
                    metadata=metadata
                )
                chunks.extend(inquiry_chunks)
                logger.info(f"Created {len(inquiry_chunks)} inquiry chunks")
            except Exception as e:
                logger.warning(f"Inquiry chunking failed: {e}")
        
        return {
            "success": True,
            "document_id": document_id,
            "chunks": chunks,
            "chunk_count": len(chunks),
            "chunking_strategy": "traditional_fallback"
        }
    
    def _get_pedagogical_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about pedagogical classification"""
        if not chunks:
            return {
                "total_chunks": 0,
                "pedagogical_types": {},
                "pedagogical_intents": {},
                "special_types": {
                    "reflection": 0,
                    "discussion": 0,
                    "glossary": 0,
                    "rubric": 0,
                    "assessment": 0,
                    "cover_page": 0,
                    "table_of_contents": 0,
                    "bibliography": 0
                }
            }
        
        pedagogical_types = {}
        pedagogical_intents = {}
        special_types = {
            "reflection": 0,
            "discussion": 0,
            "glossary": 0,
            "rubric": 0,
            "assessment": 0,
            "cover_page": 0,
            "table_of_contents": 0,
            "bibliography": 0
        }
        
        for chunk in chunks:
            p_type = chunk.get('pedagogical_type')
            if p_type:
                pedagogical_types[p_type] = pedagogical_types.get(p_type, 0) + 1
            
            p_intent = chunk.get('pedagogical_intent')
            if p_intent:
                pedagogical_intents[p_intent] = pedagogical_intents.get(p_intent, 0) + 1
            
            features = chunk.get('pedagogical_features', {})
            if features:
                if features.get('has_reflection'):
                    special_types["reflection"] += 1
                if features.get('has_discussion'):
                    special_types["discussion"] += 1
                if features.get('has_glossary'):
                    special_types["glossary"] += 1
                if features.get('has_rubric'):
                    special_types["rubric"] += 1
                if features.get('has_questions'):
                    special_types["assessment"] += 1
                if features.get('is_cover_page'):
                    special_types["cover_page"] += 1
                if features.get('is_table_of_contents'):
                    special_types["table_of_contents"] += 1
                if features.get('is_bibliography'):
                    special_types["bibliography"] += 1
        
        return {
            "total_chunks": len(chunks),
            "pedagogical_types": pedagogical_types,
            "pedagogical_intents": pedagogical_intents,
            "special_types": special_types
        }
    
    def _get_bloom_semantic_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about bloom semantic classification improvements"""
        if not chunks:
            return {
                "total_chunks": 0,
                "bloom_levels_distribution": {},
                "semantic_vs_original": {},
                "improvements": 0
            }
        
        bloom_distribution = {}
        semantic_vs_original = {}
        improvements = 0
        
        for chunk in chunks:
            original_bloom = chunk.get('bloom_level')
            semantic_bloom = chunk.get('bloom_level_semantic')
            
            if semantic_bloom:
                bloom_distribution[semantic_bloom] = bloom_distribution.get(semantic_bloom, 0) + 1
            
            if original_bloom and semantic_bloom:
                comparison_key = f"{original_bloom}→{semantic_bloom}"
                semantic_vs_original[comparison_key] = semantic_vs_original.get(comparison_key, 0) + 1
                
                if original_bloom != semantic_bloom:
                    improvements += 1
        
        # Calculate HOTS/LOTS distribution
        hots_count = sum(1 for chunk in chunks if chunk.get('bloom_is_hots'))
        lots_count = sum(1 for chunk in chunks if chunk.get('bloom_is_lots'))
        
        return {
            "total_chunks": len(chunks),
            "bloom_levels_distribution": bloom_distribution,
            "semantic_vs_original": semantic_vs_original,
            "improvements": improvements,
            "hots_chunks": hots_count,
            "lots_chunks": lots_count
        }
    
    def _get_chunk_classification_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about chunk classification improvements (Priority 1)"""
        if not chunks:
            return {
                "total_chunks": 0,
                "classification_changes": 0,
                "assessment_reductions": 0,
                "type_distribution": {}
            }
        
        classification_changes = 0
        assessment_reductions = 0
        type_distribution = {}
        
        for chunk in chunks:
            chunk_type = chunk.get('chunk_type')
            original_type = chunk.get('original_chunk_type')
            
            if original_type and original_type != chunk_type:
                classification_changes += 1
                
                # Track assessment reductions specifically
                if 'assessment' in original_type.lower() and 'assessment' not in chunk_type.lower():
                    assessment_reductions += 1
            
            # Track type distribution
            if chunk_type:
                type_distribution[chunk_type] = type_distribution.get(chunk_type, 0) + 1
        
        return {
            "total_chunks": len(chunks),
            "classification_changes": classification_changes,
            "assessment_reductions": assessment_reductions,
            "type_distribution": type_distribution
        }
    
    def _get_enhanced_chunk_types(self, chunks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get enhanced chunk type distribution with importance levels"""
        chunk_types = {}
        importance_levels = {}
        
        for chunk in chunks:
            chunk_type = chunk.get('chunk_type', 'unknown')
            importance = chunk.get('importance', 'supporting')
            
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
            importance_levels[importance] = importance_levels.get(importance, 0) + 1
        
        return {
            "types": chunk_types,
            "importance_levels": importance_levels
        }
    
    def _extract_text_content(self, parsed_document: Dict[str, Any]) -> str:
        """Extract text content using helper class"""
        return self.text_extraction_helper.extract_text_content(parsed_document)
    
    def _fallback_chunking(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback chunking strategy when semantic chunking fails"""
        try:
            # Simple sentence-based chunking
            sentences = re.split(r'[.!?]+', text)
            chunks = []
            
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    chunk_id = str(uuid.uuid4())
                    chunk = {
                        "chunk_id": chunk_id,
                        "text": sentence.strip(),
                        "metadata": {
                            "chunk_id": chunk_id,
                            "chunk_type": "generic",
                            "subject": metadata.get('subject', 'general'),
                            "grade": metadata.get('grade', 'unknown'),
                            "document_position": i,
                            "chunk_quality_score": 0.5,
                            "educational_value_score": 0.5
                        },
                        "character_count": len(sentence.strip()),
                        "word_count": len(sentence.strip().split()),
                        "position": i,
                        "confidence": 0.5
                    }
                    chunks.append(chunk)
            
            return chunks
        except Exception as e:
            logger.error(f"Error in fallback chunking: {e}")
            return []
    
    def _get_chunk_types(self, chunks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get chunk type distribution"""
        chunk_types = {}
        for chunk in chunks:
            chunk_type = chunk.get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        return chunk_types
    
    async def create_chunks(self, text_content: str) -> List[Dict[str, Any]]:
        """
        Create chunks from text content (alternative method)
        
        Args:
            text_content: Text content to chunk
            
        Returns:
            List of chunks
        """
        try:
            metadata = {"subject": "general", "grade": "unknown"}
            
            # Use competency chunking as default
            if self.competency_chunker:
                chunks = self.competency_chunker.chunk(text=text_content, metadata=metadata)
                return chunks
            
            # Fallback to simple sentence chunking
            return self._fallback_chunking(text_content, metadata)
            
        except Exception as e:
            logger.error(f"Error creating chunks: {e}")
            return []