"""
gRPC Server for Metadata Service
Handles synchronous metadata enrichment requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging

# Import proto files
import app.metadata_service_pb2 as metadata_service_pb2
import app.metadata_service_pb2_grpc as metadata_service_pb2_grpc

# Import metadata enrichment components
from app.enrichers.difficulty_enricher import DifficultyEnricher
from app.enrichers.taxonomy_classifier import TaxonomyClassifier
from app.enrichers.learning_style_detector import LearningStyleDetector
from app.enrichers.competency_tagger import CompetencyTagger
from app.enrichers.pedagogy_tagger import PedagogyTagger
from app.enrichers.assessment_tagger import AssessmentTagger

logger = logging.getLogger(__name__)


class MetadataServicer(metadata_service_pb2_grpc.MetadataServiceServicer):
    """gRPC Servicer for Metadata Service"""
    
    def __init__(self):
        # Initialize enrichers
        self.difficulty_enricher = DifficultyEnricher()
        self.taxonomy_classifier = TaxonomyClassifier()
        self.learning_style_detector = LearningStyleDetector()
        self.competency_tagger = CompetencyTagger()
        self.pedagogy_tagger = PedagogyTagger()
        self.assessment_tagger = AssessmentTagger()
        logger.info("MetadataServicer initialized")
    
    def EnrichDifficulty(self, request, context):
        """Enrich content with difficulty level"""
        try:
            content_id = request.content_id
            content = request.content
            content_type = request.content_type or "text"
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"EnrichDifficulty called for: {content_id}")
            
            # Enrich difficulty
            difficulty_result = self.difficulty_enricher.enrich(
                content=content,
                content_type=content_type,
                phase=phase,
                grade=grade,
                subject=subject,
                options=options
            )
            
            # Build protobuf response
            response = metadata_service_pb2.EnrichDifficultyResponse(
                success=True,
                message="Difficulty enrichment completed successfully"
            )
            
            # Build difficulty result
            difficulty_proto = metadata_service_pb2.DifficultyResult(
                difficulty_level=difficulty_result.get("difficulty_level", "medium"),
                confidence=difficulty_result.get("confidence", 0.0)
            )
            
            # Add factors if available
            if "factors" in difficulty_result:
                for factor in difficulty_result["factors"]:
                    factor_proto = metadata_service_pb2.DifficultyFactor(
                        factor_name=factor.get("name", ""),
                        contribution=factor.get("contribution", 0.0),
                        description=factor.get("description", "")
                    )
                    difficulty_proto.factors.append(factor_proto)
            
            response.result.CopyFrom(difficulty_proto)
            
            logger.info(f"EnrichDifficulty completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in EnrichDifficulty: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ClassifyTaxonomy(self, request, context):
        """Classify content according to taxonomy framework"""
        try:
            content_id = request.content_id
            content = request.content
            taxonomy_framework = request.taxonomy_framework or "bloom"
            options = dict(request.options)
            
            logger.info(f"ClassifyTaxonomy called for: {content_id}")
            
            # Classify taxonomy
            taxonomy_result = self.taxonomy_classifier.classify(
                content=content,
                framework=taxonomy_framework,
                options=options
            )
            
            # Build protobuf response
            response = metadata_service_pb2.ClassifyTaxonomyResponse(
                success=True,
                message="Taxonomy classification completed successfully"
            )
            
            # Build taxonomy classification result
            taxonomy_classification = metadata_service_pb2.TaxonomyClassification(
                primary_level=taxonomy_result.get("primary_level", ""),
                confidence=taxonomy_result.get("confidence", 0.0)
            )
            
            # Add labels if available
            if "labels" in taxonomy_result:
                for label in taxonomy_result["labels"]:
                    label_proto = metadata_service_pb2.TaxonomyLabel(
                        level=label.get("level", ""),
                        domain=label.get("domain", ""),
                        confidence=label.get("confidence", 0.0)
                    )
                    taxonomy_classification.labels.append(label_proto)
            
            response.result.CopyFrom(taxonomy_classification)
            
            logger.info(f"ClassifyTaxonomy completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ClassifyTaxonomy: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def DetectLearningStyle(self, request, context):
        """Detect student learning style"""
        try:
            student_id = request.student_id
            content_ids = list(request.content_ids)
            interaction_data = list(request.interaction_data)
            options = dict(request.options)
            
            logger.info(f"DetectLearningStyle called for: {student_id}")
            
            # Detect learning style
            learning_style_result = self.learning_style_detector.detect(
                student_id=student_id,
                content_ids=content_ids,
                interaction_data=interaction_data,
                options=options
            )
            
            # Build protobuf response
            response = metadata_service_pb2.DetectLearningStyleResponse(
                success=True,
                message="Learning style detection completed successfully"
            )
            
            # Build learning style result
            learning_style_proto = metadata_service_pb2.LearningStyleResult(
                primary_style=learning_style_result.get("primary_style", ""),
                confidence=learning_style_result.get("confidence", 0.0)
            )
            
            # Add secondary styles
            for style in learning_style_result.get("secondary_styles", []):
                learning_style_proto.secondary_styles.append(style)
            
            # Add preferences if available
            if "preferences" in learning_style_result:
                for pref in learning_style_result["preferences"]:
                    pref_proto = metadata_service_pb2.StylePreference(
                        style_type=pref.get("type", ""),
                        strength=pref.get("strength", 0.0)
                    )
                    learning_style_proto.preferences.append(pref_proto)
            
            response.result.CopyFrom(learning_style_proto)
            
            logger.info(f"DetectLearningStyle completed for: {student_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in DetectLearningStyle: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def TagCompetency(self, request, context):
        """Tag content with competency information"""
        try:
            content_id = request.content_id
            content = request.content
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"TagCompetency called for: {content_id}")
            
            # Tag competency
            competency_result = self.competency_tagger.tag(
                content=content,
                phase=phase,
                grade=grade,
                subject=subject,
                options=options
            )
            
            # Build protobuf response
            response = metadata_service_pb2.TagCompetencyResponse(
                success=True,
                message="Competency tagging completed successfully"
            )
            
            # Build competency tagging result
            competency_tagging = metadata_service_pb2.CompetencyTagging()
            
            # Add tags if available
            if "tags" in competency_result:
                for tag in competency_result["tags"]:
                    tag_proto = metadata_service_pb2.CompetencyTag(
                        competency_code=tag.get("code", ""),
                        competency_name=tag.get("name", ""),
                        confidence=tag.get("confidence", 0.0),
                        evidence=tag.get("evidence", "")
                    )
                    competency_tagging.tags.append(tag_proto)
            
            # Add suggestions if available
            if "suggestions" in competency_result:
                for suggestion in competency_result["suggestions"]:
                    suggestion_proto = metadata_service_pb2.CompetencySuggestion(
                        competency_code=suggestion.get("code", ""),
                        competency_name=suggestion.get("name", ""),
                        relevance=suggestion.get("relevance", 0.0),
                        reason=suggestion.get("reason", "")
                    )
                    competency_tagging.suggestions.append(suggestion_proto)
            
            response.result.CopyFrom(competency_tagging)
            
            logger.info(f"TagCompetency completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in TagCompetency: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def TagPedagogy(self, request, context):
        """Tag content with pedagogical information"""
        try:
            content_id = request.content_id
            content = request.content
            options = dict(request.options)
            
            logger.info(f"TagPedagogy called for: {content_id}")
            
            # Tag pedagogy
            pedagogy_result = self.pedagogy_tagger.tag(
                content=content,
                options=options
            )
            
            # Build protobuf response
            response = metadata_service_pb2.TagPedagogyResponse(
                success=True,
                message="Pedagogy tagging completed successfully"
            )
            
            # Build pedagogy tagging result
            pedagogy_tagging = metadata_service_pb2.PedagogyTagging()
            
            # Add tags if available
            if "tags" in pedagogy_result:
                for tag in pedagogy_result["tags"]:
                    tag_proto = metadata_service_pb2.PedagogyTag(
                        pedagogy_type=tag.get("type", ""),
                        pedagogy_method=tag.get("method", ""),
                        confidence=tag.get("confidence", 0.0)
                    )
                    
                    # Add characteristics
                    for char in tag.get("characteristics", []):
                        tag_proto.characteristics.append(char)
                    
                    pedagogy_tagging.tags.append(tag_proto)
            
            response.result.CopyFrom(pedagogy_tagging)
            
            logger.info(f"TagPedagogy completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in TagPedagogy: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def TagAssessment(self, request, context):
        """Tag content with assessment information"""
        try:
            content_id = request.content_id
            content = request.content
            assessment_type = request.assessment_type or "general"
            options = dict(request.options)
            
            logger.info(f"TagAssessment called for: {content_id}")
            
            # Tag assessment
            assessment_result = self.assessment_tagger.tag(
                content=content,
                assessment_type=assessment_type,
                options=options
            )
            
            # Build protobuf response
            response = metadata_service_pb2.TagAssessmentResponse(
                success=True,
                message="Assessment tagging completed successfully"
            )
            
            # Build assessment tagging result
            assessment_tagging = metadata_service_pb2.AssessmentTagging()
            
            # Add tags if available
            if "tags" in assessment_result:
                for tag in assessment_result["tags"]:
                    tag_proto = metadata_service_pb2.AssessmentTag(
                        assessment_type=tag.get("type", ""),
                        cognitive_level=tag.get("cognitive_level", ""),
                        competency_focus=tag.get("competency_focus", ""),
                        confidence=tag.get("confidence", 0.0)
                    )
                    assessment_tagging.tags.append(tag_proto)
            
            response.result.CopyFrom(assessment_tagging)
            
            logger.info(f"TagAssessment completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in TagAssessment: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def BatchEnrich(self, request, context):
        """Batch enrich multiple content items"""
        try:
            items = list(request.items)
            enrichment_types = list(request.enrichment_types)
            options = dict(request.options)
            
            logger.info(f"BatchEnrich called for {len(items)} items")
            
            # Placeholder implementation
            # In real implementation, this would call multiple enrichers
            
            # Build protobuf response
            response = metadata_service_pb2.BatchEnrichResponse(
                success=True,
                message="Batch enrichment completed successfully"
            )
            
            # Build batch enrichment result
            batch_result = metadata_service_pb2.BatchEnrichmentResult()
            
            # Add enriched items
            successful_items = 0
            for item in items:
                enriched_item = metadata_service_pb2.EnrichedItem(
                    content_id=item.content_id
                )
                
                # Add placeholder enriched metadata
                enriched_item.enriched_metadata["difficulty"] = "medium"
                enriched_item.enriched_metadata["taxomony"] = "apply"
                
                # Add enrichment types applied
                for enrich_type in enrichment_types:
                    enriched_item.enrichment_types_applied.append(enrich_type)
                
                batch_result.enriched_items.append(enriched_item)
                successful_items += 1
            
            # Build summary
            summary = metadata_service_pb2.BatchSummary(
                total_items=len(items),
                successful_items=successful_items,
                failed_items=len(items) - successful_items,
                success_rate=successful_items / len(items) if items else 0.0
            )
            
            # Add enrichment counts
            for enrich_type in enrichment_types:
                summary.enrichment_counts[enrich_type] = successful_items
            
            batch_result.summary.CopyFrom(summary)
            response.result.CopyFrom(batch_result)
            
            logger.info(f"BatchEnrich completed")
            return response
            
        except Exception as e:
            logger.error(f"Error in BatchEnrich: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise


def serve(port: int = 50057):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    metadata_service_pb2_grpc.add_MetadataServiceServicer_to_server(
        MetadataServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Metadata Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50057
    serve(port)