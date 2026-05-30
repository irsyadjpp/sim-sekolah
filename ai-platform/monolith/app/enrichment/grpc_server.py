"""
gRPC Server for Semantic Enrichment Service
Handles pedagogy classification, taxonomy tagging, and knowledge graph integration.
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
from typing import Dict, Any

try:
    import proto.semantic_enrichment_service_pb2 as pb2
    import proto.semantic_enrichment_service_pb2_grpc as pb2_grpc
except ImportError:
    print("Warning: Semantic Enrichment Service proto stubs not found.")
    print("Please compile proto files first.")
    pb2 = None
    pb2_grpc = None

from app.integration_service import get_enrichment_integration_service

logger = logging.getLogger(__name__)


class SemanticEnrichmentServicer:
    """gRPC Servicer for Semantic Enrichment Service"""
    
    def __init__(self):
        self.integration = get_enrichment_integration_service()
        logger.info("SemanticEnrichmentServicer initialized")
    
    def ClassifyPedagogy(self, request, context):
        """Classify pedagogical approach for content"""
        try:
            chunk_id = request.chunk_id
            content = request.content
            context_data = dict(request.context)
            options = dict(request.options)
            
            logger.info(f"ClassifyPedagogy called for chunk: {chunk_id}")
            
            import asyncio
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.integration.classify_pedagogy(
                    chunk_id=chunk_id,
                    content=content,
                    context=context_data
                )
            )
            loop.close()
            
            classification = pb2.PedagogyClassificationResult(
                primary_pedagogy=result.get("primary_pedagogy", ""),
                confidence=result.get("confidence", 0.0)
            )
            
            for label in result.get("labels", []):
                classification.labels.append(
                    pb2.PedagogyLabel(
                        pedagogy_type=label.get("pedagogy_type", ""),
                        confidence=label.get("confidence", 0.0)
                    )
                )
            
            response = pb2.ClassifyPedagogyResponse(
                success=result.get("success", True),
                message="Pedagogy classification completed",
                result=classification
            )
            
            logger.info(f"ClassifyPedagogy completed for {chunk_id}: {result.get('primary_pedagogy', '')}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ClassifyPedagogy: {str(e)}")
            return pb2.ClassifyPedagogyResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.PedagogyClassificationResult()
            )
    
    def TagTaxonomy(self, request, context):
        """Tag chunk with taxonomy information"""
        try:
            chunk_id = request.chunk_id
            content = request.content
            context_data = dict(request.context)
            options = dict(request.options)
            
            logger.info(f"TagTaxonomy called for chunk: {chunk_id}")
            
            import asyncio
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.integration.tag_taxonomy(
                    chunk_id=chunk_id,
                    content=content,
                    context=context_data
                )
            )
            loop.close()
            
            taxonomy_result = pb2.TaxonomyTaggingResult(
                primary_category=result.get("primary_category", ""),
                confidence=result.get("confidence", 0.0)
            )
            
            for tag in result.get("taxonomy_tags", []):
                taxonomy_result.tags.append(
                    pb2.TaxonomyTag(
                        taxonomy_code=tag.get("taxonomy_code", ""),
                        taxonomy_name=tag.get("taxonomy_name", ""),
                        confidence=tag.get("confidence", 0.0),
                        category=tag.get("category", "")
                    )
                )
            
            response = pb2.TagTaxonomyResponse(
                success=result.get("success", True),
                message="Taxonomy tagging completed",
                result=taxonomy_result
            )
            
            logger.info(f"TagTaxonomy completed for {chunk_id}: {len(result.get('taxonomy_tags', []))} tags")
            return response
            
        except Exception as e:
            logger.error(f"Error in TagTaxonomy: {str(e)}")
            return pb2.TagTaxonomyResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.TaxonomyTaggingResult()
            )
    
    def EnrichChunk(self, request, context):
        """Full enrichment of a chunk"""
        try:
            chunk_id = request.chunk_id
            content = request.content
            enrichment_types = list(request.enrichment_types)
            context_data = dict(request.context)
            options = dict(request.options)
            
            logger.info(f"EnrichChunk called for chunk: {chunk_id}")
            
            import asyncio
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.integration.enrich_chunk(
                    chunk_id=chunk_id,
                    content=content,
                    enrichment_types=enrichment_types,
                    context=context_data
                )
            )
            loop.close()
            
            # Build pedagogy result
            pedagogy = result.get("pedagogy", {})
            pedagogy_result = pb2.PedagogyClassificationResult(
                primary_pedagogy=pedagogy.get("primary_pedagogy", ""),
                confidence=pedagogy.get("confidence", 0.0)
            )
            for label in pedagogy.get("labels", []):
                pedagogy_result.labels.append(
                    pb2.PedagogyLabel(
                        pedagogy_type=label.get("pedagogy_type", ""),
                        confidence=label.get("confidence", 0.0)
                    )
                )
            
            # Build taxonomy result
            taxonomy = result.get("taxonomy", {})
            taxonomy_result = pb2.TaxonomyTaggingResult(
                primary_category=taxonomy.get("primary_category", ""),
                confidence=taxonomy.get("confidence", 0.0)
            )
            for tag in taxonomy.get("taxonomy_tags", []):
                taxonomy_result.tags.append(
                    pb2.TaxonomyTag(
                        taxonomy_code=tag.get("taxonomy_code", ""),
                        taxonomy_name=tag.get("taxonomy_name", ""),
                        confidence=tag.get("confidence", 0.0),
                        category=tag.get("category", "")
                    )
                )
            
            # Build ontology result
            ontology = result.get("ontology", {})
            ontology_result = pb2.OntologyResult()
            for entity in ontology.get("entities", []):
                ontology_result.entities.append(
                    pb2.OntologyEntity(
                        entity=entity.get("entity", ""),
                        entity_type=entity.get("entity_type", ""),
                        confidence=entity.get("confidence", 0.0)
                    )
                )
            for rel in ontology.get("relationships", []):
                ontology_result.relationships.append(
                    pb2.OntologyRelationship(
                        source=rel.get("source", ""),
                        target=rel.get("target", ""),
                        relationship=rel.get("relationship", "")
                    )
                )
            
            enriched_metadata = result.get("enriched_metadata", {})
            
            response = pb2.EnrichChunkResponse(
                success=result.get("success", True),
                message="Chunk enrichment completed",
                pedagogy=pedagogy_result,
                taxonomy=taxonomy_result,
                ontology=ontology_result,
                enriched_metadata=enriched_metadata
            )
            
            logger.info(f"EnrichChunk completed for {chunk_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in EnrichChunk: {str(e)}")
            return pb2.EnrichChunkResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def ValidateCurriculumAlignment(self, request, context):
        """Validate curriculum alignment"""
        try:
            chunk_id = request.chunk_id
            content = request.content
            competency_codes = list(request.competency_codes)
            phase = request.phase
            grade = request.grade
            subject = request.subject
            options = dict(request.options)
            
            logger.info(f"ValidateCurriculumAlignment called for chunk: {chunk_id}")
            
            import asyncio
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.integration.validate_curriculum_alignment(
                    chunk_id=chunk_id,
                    content=content,
                    competency_codes=competency_codes,
                    phase=phase,
                    grade=grade,
                    subject=subject
                )
            )
            loop.close()
            
            alignment_result = pb2.CurriculumAlignmentResult(
                is_aligned=result.get("is_aligned", False),
                alignment_score=result.get("alignment_score", 0.0)
            )
            
            for detail in result.get("details", []):
                alignment_result.details.append(
                    pb2.AlignmentDetail(
                        competency_code=detail.get("competency_code", ""),
                        competency_name=detail.get("competency_name", ""),
                        alignment_score=detail.get("alignment_score", 0.0),
                        status=detail.get("status", ""),
                        evidence=detail.get("evidence", "")
                    )
                )
            
            alignment_result.recommendations.extend(result.get("recommendations", []))
            
            response = pb2.ValidateCurriculumAlignmentResponse(
                success=result.get("success", True),
                message="Curriculum alignment validation completed",
                result=alignment_result
            )
            
            logger.info(f"ValidateCurriculumAlignment completed for {chunk_id}: aligned={result.get('is_aligned', False)}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ValidateCurriculumAlignment: {str(e)}")
            return pb2.ValidateCurriculumAlignmentResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def BatchEnrichChunks(self, request, context):
        """Batch enrich multiple chunks"""
        try:
            items = [
                {
                    "chunk_id": item.chunk_id,
                    "content": item.content,
                    "context": dict(item.context)
                }
                for item in request.items
            ]
            enrichment_types = list(request.enrichment_types)
            options = dict(request.options)
            
            logger.info(f"BatchEnrichChunks called for {len(items)} items")
            
            import asyncio
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.integration.batch_enrich(
                    items=items,
                    enrichment_types=enrichment_types
                )
            )
            loop.close()
            
            results = []
            for r in result.get("results", []):
                chunk_result = pb2.EnrichChunkResult(
                    chunk_id=r.get("chunk_id", ""),
                    success=r.get("success", False),
                    error=r.get("error", "")
                )
                results.append(chunk_result)
            
            summary = result.get("summary", {})
            batch_summary = pb2.BatchEnrichSummary(
                total_items=summary.get("total_items", 0),
                successful_items=summary.get("successful_items", 0),
                failed_items=summary.get("failed_items", 0),
                average_confidence=summary.get("average_confidence", 0.0)
            )
            
            response = pb2.BatchEnrichChunksResponse(
                success=True,
                message=f"Batch enrichment completed: {summary.get('successful_items', 0)}/{summary.get('total_items', 0)} successful",
                results=results,
                summary=batch_summary
            )
            
            logger.info(f"BatchEnrichChunks completed: {summary.get('successful_items', 0)}/{summary.get('total_items', 0)} successful")
            return response
            
        except Exception as e:
            logger.error(f"Error in BatchEnrichChunks: {str(e)}")
            return pb2.BatchEnrichChunksResponse(
                success=False,
                message=f"Error: {str(e)}"
            )


def serve(port: int = 50057):
    """Start the gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Semantic Enrichment Service gRPC Server on port {port}")
    
    if pb2 is None or pb2_grpc is None:
        logger.error("Proto stubs not available. Cannot start gRPC server.")
        logger.info("Please compile proto files first using: python -m grpc_tools.protoc ...")
        return
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = SemanticEnrichmentServicer()
    pb2_grpc.add_SemanticEnrichmentServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Semantic Enrichment Service gRPC Server started on port {port}")
    logger.info("Available methods: 5 (ClassifyPedagogy, TagTaxonomy, EnrichChunk, ValidateCurriculumAlignment, BatchEnrichChunks)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import os
    port = int(os.getenv("GRPC_PORT", "50057"))
    serve(port)