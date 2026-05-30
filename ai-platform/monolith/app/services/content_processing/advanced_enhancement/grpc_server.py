"""
gRPC Server Implementation - Advanced Enhancement Service
This file contains the gRPC server implementation that wraps the existing service classes.
"""

import grpc
from concurrent import futures
import asyncio
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import generated protobuf classes
try:
    import advanced_enhancement_pb2 as pb2
    import advanced_enhancement_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

from main import (
    AdvancedEnhancementEngine,
    RetrievalEnhancementRequest,
    QueryExpansionRequest,
    RerankingRequest,
    SemanticEnrichmentRequest,
    EmbeddingRequest,
    KnowledgeExtractionRequest,
    OntologyQueryRequest,
    OntologyAlignmentRequest,
    RelatedConceptsRequest
)

logger = logging.getLogger(__name__)


class AdvancedEnhancementServicer:
    """gRPC Servicer for Advanced Enhancement Service - wraps 3 services"""
    
    def __init__(self):
        self.engine = AdvancedEnhancementEngine()
        logger.info("Advanced Enhancement Servicer initialized with AdvancedEnhancementEngine")
    
    # Helper function to convert dict to protobuf map
    def _dict_to_map(self, data):
        """Convert dictionary to protobuf map"""
        return {str(k): str(v) for k, v in (data or {}).items()}
    
    # Helper function to convert list to protobuf repeated field
    def _list_to_repeated(self, data):
        """Convert list to protobuf repeated field"""
        return list(data or [])
    
    # ==================== Retrieval Enhancement Service Methods ====================
    
    def EnhanceQuery(self, request, context):
        """Enhance retrieval query"""
        logger.info(f"EnhanceQuery called: {request.request_id}")
        
        try:
            internal_request = RetrievalEnhancementRequest(
                request_id=request.request_id,
                query=request.query,
                subject=request.subject,
                phase=request.phase,
                initial_results=list(request.initial_results),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.retrieval_enhancement_service.enhance_query(internal_request)
            
            # Convert enhanced results to protobuf format
            enhanced_results = []
            for result_item in result.get("enhanced_results", []):
                enhanced_results.append(pb2.EnhancedResult(
                    document_id=result_item.get("document_id", ""),
                    content=result_item.get("content", ""),
                    enhanced_score=result_item.get("enhanced_score", 0.0),
                    enhancement_factors=self._list_to_repeated(result_item.get("enhancement_factors", []))
                ))
            
            return pb2.EnhancedRetrievalResponse(
                request_id=request.request_id,
                success=True,
                message="Query enhancement completed successfully",
                enhanced_results=enhanced_results,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in EnhanceQuery: {e}")
            return pb2.EnhancedRetrievalResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                enhanced_results=[],
                metadata={}
            )
    
    def ExpandQuery(self, request, context):
        """Expand query for better retrieval"""
        logger.info(f"ExpandQuery called: {request.request_id}")
        
        try:
            internal_request = QueryExpansionRequest(
                request_id=request.request_id,
                query=request.query,
                subject=request.subject,
                expansion_count=request.expansion_count
            )
            
            result = self.engine.retrieval_enhancement_service.expand_query(internal_request)
            
            return pb2.QueryExpansionResponse(
                request_id=request.request_id,
                success=True,
                message="Query expansion completed successfully",
                expanded_queries=self._list_to_repeated(result.get("expanded_queries", [])),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in ExpandQuery: {e}")
            return pb2.QueryExpansionResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                expanded_queries=[],
                metadata={}
            )
    
    def RerankResults(self, request, context):
        """Rerank retrieval results"""
        logger.info(f"RerankResults called: {request.request_id}")
        
        try:
            # Convert retrieval results from protobuf
            results = []
            for result in request.initial_results:
                results.append({
                    "document_id": result.document_id,
                    "content": result.content,
                    "score": result.score
                })
            
            internal_request = RerankingRequest(
                request_id=request.request_id,
                initial_results=results,
                query=request.query,
                reranking_strategy=request.reranking_strategy
            )
            
            result = self.engine.retrieval_enhancement_service.rerank_results(internal_request)
            
            # Convert reranked results to protobuf format
            reranked_results = []
            for result_item in result.get("reranked_results", []):
                reranked_results.append(pb2.RetrievalResult(
                    document_id=result_item.get("document_id", ""),
                    content=result_item.get("content", ""),
                    score=result_item.get("score", 0.0)
                ))
            
            return pb2.RerankingResponse(
                request_id=request.request_id,
                success=True,
                message="Results reranking completed successfully",
                reranked_results=reranked_results,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in RerankResults: {e}")
            return pb2.RerankingResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                reranked_results=[],
                metadata={}
            )
    
    # ==================== Semantic Enrichment Service Methods ====================
    
    def EnrichContent(self, request, context):
        """Enrich content with semantic information"""
        logger.info(f"EnrichContent called: {request.request_id}")
        
        try:
            internal_request = SemanticEnrichmentRequest(
                request_id=request.request_id,
                content=request.content,
                content_type=request.content_type,
                enrichment_types=list(request.enrichment_types),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.semantic_enrichment_service.enrich_content(internal_request)
            
            # Convert enrichments to protobuf format
            enrichments = []
            for enrichment in result.get("enrichments", []):
                enrichments.append(pb2.Enrichment(
                    enrichment_type=enrichment.get("enrichment_type", ""),
                    enriched_data=enrichment.get("enriched_data", ""),
                    confidence=enrichment.get("confidence", 0.0)
                ))
            
            return pb2.EnrichmentResponse(
                request_id=request.request_id,
                success=True,
                message="Content enrichment completed successfully",
                enriched_content=self._dict_to_map(result.get("enriched_content", {})),
                enrichments=enrichments,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in EnrichContent: {e}")
            return pb2.EnrichmentResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                enriched_content={},
                enrichments=[],
                metadata={}
            )
    
    def GenerateEmbeddings(self, request, context):
        """Generate embeddings for texts"""
        logger.info(f"GenerateEmbeddings called: {request.request_id}")
        
        try:
            internal_request = EmbeddingRequest(
                request_id=request.request_id,
                texts=list(request.texts),
                model=request.model,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.semantic_enrichment_service.generate_embeddings(internal_request)
            
            # Convert embeddings to protobuf format
            embeddings = []
            for embedding in result.get("embeddings", []):
                embeddings.append(pb2.Embedding(
                    text_id=embedding.get("text_id", ""),
                    vector=self._list_to_repeated(embedding.get("vector", [])),
                    dimension=embedding.get("dimension", 0)
                ))
            
            return pb2.EmbeddingResponse(
                request_id=request.request_id,
                success=True,
                message="Embeddings generated successfully",
                embeddings=embeddings,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GenerateEmbeddings: {e}")
            return pb2.EmbeddingResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                embeddings=[],
                metadata={}
            )
    
    def ExtractKnowledge(self, request, context):
        """Extract knowledge triples from content"""
        logger.info(f"ExtractKnowledge called: {request.request_id}")
        
        try:
            internal_request = KnowledgeExtractionRequest(
                request_id=request.request_id,
                content=request.content,
                extraction_type=request.extraction_type,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.semantic_enrichment_service.extract_knowledge(internal_request)
            
            # Convert knowledge triples to protobuf format
            knowledge_triples = []
            for triple in result.get("knowledge_triples", []):
                knowledge_triples.append(pb2.KnowledgeTriple(
                    subject=triple.get("subject", ""),
                    predicate=triple.get("predicate", ""),
                    object=triple.get("object", ""),
                    confidence=triple.get("confidence", 0.0)
                ))
            
            return pb2.KnowledgeExtractionResponse(
                request_id=request.request_id,
                success=True,
                message="Knowledge extraction completed successfully",
                knowledge_triples=knowledge_triples,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in ExtractKnowledge: {e}")
            return pb2.KnowledgeExtractionResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                knowledge_triples=[],
                metadata={}
            )
    
    # ==================== Educational Ontology Service Methods ====================
    
    def QueryOntology(self, request, context):
        """Query educational ontology"""
        logger.info(f"QueryOntology called: {request.request_id}")
        
        try:
            internal_request = OntologyQueryRequest(
                request_id=request.request_id,
                ontology_type=request.ontology_type,
                query=request.query,
                filters=list(request.filters)
            )
            
            result = self.engine.educational_ontology_service.query_ontology(internal_request)
            
            # Convert nodes to protobuf format
            nodes = []
            for node in result.get("nodes", []):
                nodes.append(pb2.OntologyNode(
                    node_id=node.get("node_id", ""),
                    node_type=node.get("node_type", ""),
                    properties=self._dict_to_map(node.get("properties", {}))
                ))
            
            # Convert edges to protobuf format
            edges = []
            for edge in result.get("edges", []):
                edges.append(pb2.OntologyEdge(
                    edge_id=edge.get("edge_id", ""),
                    source_node=edge.get("source_node", ""),
                    target_node=edge.get("target_node", ""),
                    edge_type=edge.get("edge_type", ""),
                    properties=self._dict_to_map(edge.get("properties", {}))
                ))
            
            return pb2.OntologyQueryResponse(
                request_id=request.request_id,
                success=True,
                message="Ontology query completed successfully",
                nodes=nodes,
                edges=edges,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in QueryOntology: {e}")
            return pb2.OntologyQueryResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                nodes=[],
                edges=[],
                metadata={}
            )
    
    def ValidateAlignment(self, request, context):
        """Validate content alignment with ontology"""
        logger.info(f"ValidateAlignment called: {request.request_id}")
        
        try:
            internal_request = OntologyAlignmentRequest(
                request_id=request.request_id,
                content=request.content,
                ontology_type=request.ontology_type,
                target_standards=list(request.target_standards)
            )
            
            result = self.engine.educational_ontology_service.validate_alignment(internal_request)
            alignment_result = result.get("alignment_result", {})
            
            return pb2.AlignmentValidationResponse(
                request_id=request.request_id,
                success=True,
                message="Alignment validation completed successfully",
                alignment_result=self._dict_to_map(alignment_result),
                is_aligned=alignment_result.get("is_aligned", False),
                alignment_score=alignment_result.get("alignment_score", 0.0),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in ValidateAlignment: {e}")
            return pb2.AlignmentValidationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                alignment_result={},
                is_aligned=False,
                alignment_score=0.0,
                metadata={}
            )
    
    def GetRelatedConcepts(self, request, context):
        """Get related concepts from ontology"""
        logger.info(f"GetRelatedConcepts called: {request.request_id}")
        
        try:
            internal_request = RelatedConceptsRequest(
                request_id=request.request_id,
                concept=request.concept,
                ontology_type=request.ontology_type,
                max_concepts=request.max_concepts
            )
            
            result = self.engine.educational_ontology_service.get_related_concepts(internal_request)
            
            # Convert concepts to protobuf format
            concepts = []
            for concept in result.get("concepts", []):
                concepts.append(pb2.RelatedConcept(
                    concept_id=concept.get("concept_id", ""),
                    concept_name=concept.get("concept_name", ""),
                    relatedness_score=concept.get("relatedness_score", 0.0),
                    relationship_type=concept.get("relationship_type", "")
                ))
            
            return pb2.RelatedConceptsResponse(
                request_id=request.request_id,
                success=True,
                message="Related concepts retrieved successfully",
                concepts=concepts,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GetRelatedConcepts: {e}")
            return pb2.RelatedConceptsResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                concepts=[],
                metadata={}
            )


def serve_retrieval_enhancement(port: int = 50083):
    """Start the Retrieval Enhancement Service gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Retrieval Enhancement Service gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = AdvancedEnhancementServicer()
    pb2_grpc.add_RetrievalEnhancementServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Retrieval Enhancement Service gRPC Server started successfully on port {port}")
    logger.info("Available methods: 3 (EnhanceQuery, ExpandQuery, RerankResults)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_semantic_enrichment(port: int = 50084):
    """Start the Semantic Enrichment Service gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Semantic Enrichment Service gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = AdvancedEnhancementServicer()
    pb2_grpc.add_SemanticEnrichmentServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Semantic Enrichment Service gRPC Server started successfully on port {port}")
    logger.info("Available methods: 3 (EnrichContent, GenerateEmbeddings, ExtractKnowledge)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_educational_ontology(port: int = 50085):
    """Start the Educational Ontology Service gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Educational Ontology Service gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = AdvancedEnhancementServicer()
    pb2_grpc.add_EducationalOntologyServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Educational Ontology Service gRPC Server started successfully on port {port}")
    logger.info("Available methods: 3 (QueryOntology, ValidateAlignment, GetRelatedConcepts)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import sys
    
    # Determine which service to start based on command line argument
    if len(sys.argv) > 1:
        service = sys.argv[1]
        port = int(os.getenv("GRPC_PORT", "50083"))
        
        if service == "retrieval-enhancement":
            serve_retrieval_enhancement(port)
        elif service == "semantic-enrichment":
            serve_semantic_enrichment(port + 1)
        elif service == "educational-ontology":
            serve_educational_ontology(port + 2)
        else:
            print(f"Unknown service: {service}")
            print("Available services: retrieval-enhancement, semantic-enrichment, educational-ontology")
    else:
        print("Usage: python grpc_server.py <service_name>")
        print("Available services: retrieval-enhancement, semantic-enrichment, educational-ontology")
