"""
gRPC Server for Semantic Chunk Service
Handles synchronous semantic chunking requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging

# Import proto files
import app.semantic_chunk_service_pb2 as semantic_chunk_service_pb2
import app.semantic_chunk_service_pb2_grpc as semantic_chunk_service_pb2_grpc

# Import chunking components
from app.chunkers.competency_chunker import CompetencyChunker
from app.chunkers.activity_chunker import ActivityChunker
from app.chunkers.assessment_chunker import AssessmentChunker
from app.chunkers.inquiry_chunker import InquiryChunker
from app.chunkers.lesson_plan_chunker import LessonPlanChunker
from app.enrichers.chunk_enricher import ChunkEnricher

logger = logging.getLogger(__name__)


class ChunkServicer(semantic_chunk_service_pb2_grpc.SemanticChunkServiceServicer):
    """gRPC Servicer for Semantic Chunk Service"""
    
    def __init__(self):
        # Initialize chunkers
        self.competency_chunker = CompetencyChunker()
        self.activity_chunker = ActivityChunker()
        self.assessment_chunker = AssessmentChunker()
        self.inquiry_chunker = InquiryChunker()
        self.lesson_plan_chunker = LessonPlanChunker()
        self.chunk_enricher = ChunkEnricher()
        logger.info("ChunkServicer initialized")
    
    def ChunkCompetency(self, request, context):
        """Competency-based chunking"""
        try:
            content_id = request.content_id
            content = request.content
            competency = request.competency or "KI-3"
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"ChunkCompetency called for: {content_id}")
            
            # Chunk content based on competency
            chunks = self.competency_chunker.chunk(
                content=content,
                competency_type=competency,
                metadata=options
            )
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ChunkCompetencyResponse(
                success=True,
                message="Competency chunking completed successfully"
            )
            
            # Build chunk result
            chunk_result = semantic_chunk_service_pb2.ChunkResult()
            
            # Add chunks
            for chunk in chunks:
                chunk_proto = semantic_chunk_service_pb2.Chunk(
                    chunk_id=chunk.get("chunk_id", ""),
                    content=chunk.get("content", ""),
                    chunk_type="competency",
                    quality_score=chunk.get("quality_score", 0.0)
                )
                
                # Add metadata
                for key, value in chunk.get("metadata", {}).items():
                    chunk_proto.metadata[key] = str(value)
                
                # Add competencies
                for comp in chunk.get("competencies", []):
                    chunk_proto.competencies.append(comp)
                
                chunk_result.chunks.append(chunk_proto)
            
            # Build summary
            summary = semantic_chunk_service_pb2.ChunkingSummary(
                total_chunks=len(chunks),
                average_quality=sum(c.get("quality_score", 0.0) for c in chunks) / len(chunks) if chunks else 0.0
            )
            
            summary.chunk_types.append("competency")
            summary.type_counts["competency"] = len(chunks)
            
            chunk_result.summary.CopyFrom(summary)
            response.result.CopyFrom(chunk_result)
            
            logger.info(f"ChunkCompetency completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ChunkCompetency: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ChunkActivity(self, request, context):
        """Activity-based chunking"""
        try:
            content_id = request.content_id
            content = request.content
            activity_type = request.activity_type or "general"
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"ChunkActivity called for: {content_id}")
            
            # Chunk content based on activity
            chunks = self.activity_chunker.chunk(
                content=content,
                activity_type=activity_type,
                metadata=options
            )
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ChunkActivityResponse(
                success=True,
                message="Activity chunking completed successfully"
            )
            
            # Build chunk result
            chunk_result = semantic_chunk_service_pb2.ChunkResult()
            
            # Add chunks
            for chunk in chunks:
                chunk_proto = semantic_chunk_service_pb2.Chunk(
                    chunk_id=chunk.get("chunk_id", ""),
                    content=chunk.get("content", ""),
                    chunk_type="activity",
                    quality_score=chunk.get("quality_score", 0.0)
                )
                
                # Add metadata
                for key, value in chunk.get("metadata", {}).items():
                    chunk_proto.metadata[key] = str(value)
                
                # Add competencies
                for comp in chunk.get("competencies", []):
                    chunk_proto.competencies.append(comp)
                
                chunk_result.chunks.append(chunk_proto)
            
            # Build summary
            summary = semantic_chunk_service_pb2.ChunkingSummary(
                total_chunks=len(chunks),
                average_quality=sum(c.get("quality_score", 0.0) for c in chunks) / len(chunks) if chunks else 0.0
            )
            
            summary.chunk_types.append("activity")
            summary.type_counts["activity"] = len(chunks)
            
            chunk_result.summary.CopyFrom(summary)
            response.result.CopyFrom(chunk_result)
            
            logger.info(f"ChunkActivity completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ChunkActivity: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ChunkAssessment(self, request, context):
        """Assessment-based chunking"""
        try:
            content_id = request.content_id
            content = request.content
            assessment_type = request.assessment_type or "general"
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"ChunkAssessment called for: {content_id}")
            
            # Chunk content based on assessment
            chunks = self.assessment_chunker.chunk(
                content=content,
                assessment_type=assessment_type,
                metadata=options
            )
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ChunkAssessmentResponse(
                success=True,
                message="Assessment chunking completed successfully"
            )
            
            # Build chunk result
            chunk_result = semantic_chunk_service_pb2.ChunkResult()
            
            # Add chunks
            for chunk in chunks:
                chunk_proto = semantic_chunk_service_pb2.Chunk(
                    chunk_id=chunk.get("chunk_id", ""),
                    content=chunk.get("content", ""),
                    chunk_type="assessment",
                    quality_score=chunk.get("quality_score", 0.0)
                )
                
                # Add metadata
                for key, value in chunk.get("metadata", {}).items():
                    chunk_proto.metadata[key] = str(value)
                
                # Add competencies
                for comp in chunk.get("competencies", []):
                    chunk_proto.competencies.append(comp)
                
                chunk_result.chunks.append(chunk_proto)
            
            # Build summary
            summary = semantic_chunk_service_pb2.ChunkingSummary(
                total_chunks=len(chunks),
                average_quality=sum(c.get("quality_score", 0.0) for c in chunks) / len(chunks) if chunks else 0.0
            )
            
            summary.chunk_types.append("assessment")
            summary.type_counts["assessment"] = len(chunks)
            
            chunk_result.summary.CopyFrom(summary)
            response.result.CopyFrom(chunk_result)
            
            logger.info(f"ChunkAssessment completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ChunkAssessment: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ChunkInquiry(self, request, context):
        """Inquiry-based chunking"""
        try:
            content_id = request.content_id
            content = request.content
            inquiry_type = request.inquiry_type or "scientific"
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"ChunkInquiry called for: {content_id}")
            
            # Chunk content based on inquiry
            chunks = self.inquiry_chunker.chunk(
                content=content,
                inquiry_type=inquiry_type,
                metadata=options
            )
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ChunkInquiryResponse(
                success=True,
                message="Inquiry chunking completed successfully"
            )
            
            # Build chunk result
            chunk_result = semantic_chunk_service_pb2.ChunkResult()
            
            # Add chunks
            for chunk in chunks:
                chunk_proto = semantic_chunk_service_pb2.Chunk(
                    chunk_id=chunk.get("chunk_id", ""),
                    content=chunk.get("content", ""),
                    chunk_type="inquiry",
                    quality_score=chunk.get("quality_score", 0.0)
                )
                
                # Add metadata
                for key, value in chunk.get("metadata", {}).items():
                    chunk_proto.metadata[key] = str(value)
                
                # Add competencies
                for comp in chunk.get("competencies", []):
                    chunk_proto.competencies.append(comp)
                
                chunk_result.chunks.append(chunk_proto)
            
            # Build summary
            summary = semantic_chunk_service_pb2.ChunkingSummary(
                total_chunks=len(chunks),
                average_quality=sum(c.get("quality_score", 0.0) for c in chunks) / len(chunks) if chunks else 0.0
            )
            
            summary.chunk_types.append("inquiry")
            summary.type_counts["inquiry"] = len(chunks)
            
            chunk_result.summary.CopyFrom(summary)
            response.result.CopyFrom(chunk_result)
            
            logger.info(f"ChunkInquiry completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ChunkInquiry: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ChunkLessonPlan(self, request, context):
        """Lesson plan-based chunking"""
        try:
            content_id = request.content_id
            content = request.content
            lesson_plan_type = request.lesson_plan_type or "standard"
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            options = dict(request.options)
            
            logger.info(f"ChunkLessonPlan called for: {content_id}")
            
            # Chunk content based on lesson plan
            chunks = self.lesson_plan_chunker.chunk(
                content=content,
                lesson_plan_type=lesson_plan_type,
                metadata=options
            )
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ChunkLessonPlanResponse(
                success=True,
                message="Lesson plan chunking completed successfully"
            )
            
            # Build chunk result
            chunk_result = semantic_chunk_service_pb2.ChunkResult()
            
            # Add chunks
            for chunk in chunks:
                chunk_proto = semantic_chunk_service_pb2.Chunk(
                    chunk_id=chunk.get("chunk_id", ""),
                    content=chunk.get("content", ""),
                    chunk_type="lesson_plan",
                    quality_score=chunk.get("quality_score", 0.0)
                )
                
                # Add metadata
                for key, value in chunk.get("metadata", {}).items():
                    chunk_proto.metadata[key] = str(value)
                
                # Add competencies
                for comp in chunk.get("competencies", []):
                    chunk_proto.competencies.append(comp)
                
                chunk_result.chunks.append(chunk_proto)
            
            # Build summary
            summary = semantic_chunk_service_pb2.ChunkingSummary(
                total_chunks=len(chunks),
                average_quality=sum(c.get("quality_score", 0.0) for c in chunks) / len(chunks) if chunks else 0.0
            )
            
            summary.chunk_types.append("lesson_plan")
            summary.type_counts["lesson_plan"] = len(chunks)
            
            chunk_result.summary.CopyFrom(summary)
            response.result.CopyFrom(chunk_result)
            
            logger.info(f"ChunkLessonPlan completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ChunkLessonPlan: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def DetectHierarchy(self, request, context):
        """Detect document hierarchy"""
        try:
            content_id = request.content_id
            content = request.content
            options = dict(request.options)
            
            logger.info(f"DetectHierarchy called for: {content_id}")
            
            # Placeholder implementation
            # In real implementation, this would use a hierarchy detection component
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.DetectHierarchyResponse(
                success=True,
                message="Hierarchy detection completed successfully"
            )
            
            # Build hierarchy result
            hierarchy_result = semantic_chunk_service_pb2.HierarchyResult()
            
            # Add placeholder node
            node = semantic_chunk_service_pb2.HierarchyNode(
                node_id="root",
                node_type="document",
                content=content[:100] if len(content) > 100 else content,
                level=0
            )
            hierarchy_result.nodes.append(node)
            
            response.result.CopyFrom(hierarchy_result)
            
            logger.info(f"DetectHierarchy completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in DetectHierarchy: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ClassifyPedagogy(self, request, context):
        """Classify pedagogical approach"""
        try:
            content_id = request.content_id
            content = request.content
            options = dict(request.options)
            
            logger.info(f"ClassifyPedagogy called for: {content_id}")
            
            # Placeholder implementation
            # In real implementation, this would use a pedagogy classification component
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ClassifyPedagogyResponse(
                success=True,
                message="Pedagogy classification completed successfully"
            )
            
            # Build pedagogy classification result
            pedagogy_classification = semantic_chunk_service_pb2.PedagogyClassification(
                primary_pedagogy="direct_instruction",
                confidence=0.8
            )
            
            # Add placeholder label
            label = semantic_chunk_service_pb2.PedagogyLabel(
                pedagogy_type="direct_instruction",
                confidence=0.8
            )
            pedagogy_classification.labels.append(label)
            
            response.result.CopyFrom(pedagogy_classification)
            
            logger.info(f"ClassifyPedagogy completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ClassifyPedagogy: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ValidateQuality(self, request, context):
        """Validate chunk quality"""
        try:
            chunks = list(request.chunks)
            validation_criteria = dict(request.validation_criteria)
            
            logger.info(f"ValidateQuality called for {len(chunks)} chunks")
            
            # Placeholder implementation
            # In real implementation, this would validate chunk quality
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.ValidateQualityResponse(
                success=True,
                message="Quality validation completed successfully"
            )
            
            # Build quality validation result
            quality_validation = semantic_chunk_service_pb2.QualityValidation(
                overall_quality=0.85
            )
            
            # Add placeholder metric
            metric = semantic_chunk_service_pb2.QualityMetric(
                metric_name="coherence",
                value=0.85,
                status="good"
            )
            quality_validation.metrics.append(metric)
            
            response.result.CopyFrom(quality_validation)
            
            logger.info(f"ValidateQuality completed")
            return response
            
        except Exception as e:
            logger.error(f"Error in ValidateQuality: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def EnrichMetadata(self, request, context):
        """Enrich chunk metadata"""
        try:
            chunks = list(request.chunks)
            enrichment_types = list(request.enrichment_types)
            options = dict(request.options)
            
            logger.info(f"EnrichMetadata called for {len(chunks)} chunks")
            
            # Placeholder implementation
            # In real implementation, this would enrich chunk metadata
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.EnrichMetadataResponse(
                success=True,
                message="Metadata enrichment completed successfully"
            )
            
            # Build metadata enrichment result
            metadata_enrichment = semantic_chunk_service_pb2.MetadataEnrichment()
            
            # Add enriched chunks (placeholder)
            for chunk in chunks:
                enriched_chunk = semantic_chunk_service_pb2.Chunk()
                enriched_chunk.CopyFrom(chunk)
                metadata_enrichment.enriched_chunks.append(enriched_chunk)
            
            # Add enrichment summary
            summary = semantic_chunk_service_pb2.EnrichmentSummary(
                enrichment_type="metadata",
                chunks_enriched=len(chunks),
                success_rate=1.0
            )
            metadata_enrichment.summaries.append(summary)
            
            response.result.CopyFrom(metadata_enrichment)
            
            logger.info(f"EnrichMetadata completed")
            return response
            
        except Exception as e:
            logger.error(f"Error in EnrichMetadata: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def BuildChunks(self, request, context):
        """Build chunks with specified strategy"""
        try:
            content_id = request.content_id
            content = request.content
            chunking_strategy = request.chunking_strategy or "semantic"
            parameters = dict(request.parameters)
            
            logger.info(f"BuildChunks called for: {content_id}")
            
            # Placeholder implementation
            # In real implementation, this would build chunks with the specified strategy
            
            # Build protobuf response
            response = semantic_chunk_service_pb2.BuildChunksResponse(
                success=True,
                message="Chunk building completed successfully"
            )
            
            # Build chunk result
            chunk_result = semantic_chunk_service_pb2.ChunkResult()
            
            # Add placeholder chunk
            chunk_proto = semantic_chunk_service_pb2.Chunk(
                chunk_id=f"{content_id}_0",
                content=content,
                chunk_type=chunking_strategy,
                quality_score=0.8
            )
            chunk_result.chunks.append(chunk_proto)
            
            # Build summary
            summary = semantic_chunk_service_pb2.ChunkingSummary(
                total_chunks=1,
                average_quality=0.8
            )
            summary.chunk_types.append(chunking_strategy)
            summary.type_counts[chunking_strategy] = 1
            
            chunk_result.summary.CopyFrom(summary)
            response.result.CopyFrom(chunk_result)
            
            logger.info(f"BuildChunks completed for: {content_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in BuildChunks: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise


def serve(port: int = 50056):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    semantic_chunk_service_pb2_grpc.add_SemanticChunkServiceServicer_to_server(
        ChunkServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Semantic Chunk Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50056
    serve(port)