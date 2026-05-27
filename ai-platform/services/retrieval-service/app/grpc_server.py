"""
gRPC Server for Retrieval Service
Handles synchronous retrieval and search requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
import time

# Import proto files
import app.retrieval_service_pb2 as retrieval_service_pb2
import app.retrieval_service_pb2_grpc as retrieval_service_pb2_grpc

# Import retrieval components
from app.retrievers.semantic_retriever import SemanticRetriever
from app.retrievers.hybrid_retriever import HybridRetriever
from app.retrievers.metadata_filter import MetadataFilter
from app.context.context_builder import ContextBuilder
from app.query.query_expander import QueryExpander
from app.scoring.relevance_scorer import RelevanceScorer

logger = logging.getLogger(__name__)


class RetrievalServicer(retrieval_service_pb2_grpc.RetrievalServiceServicer):
    """gRPC Servicer for Retrieval Service"""
    
    def __init__(self):
        # Initialize retrievers
        self.semantic_retriever = SemanticRetriever()
        self.hybrid_retriever = HybridRetriever()
        self.metadata_filter = MetadataFilter()
        self.context_builder = ContextBuilder()
        self.query_expander = QueryExpander()
        self.relevance_scorer = RelevanceScorer()
        logger.info("RetrievalServicer initialized")
    
    def SemanticSearch(self, request, context):
        """Perform semantic search"""
        try:
            query_id = request.query_id
            query_text = request.query_text
            collection_name = request.collection_name or "default"
            limit = request.limit if request.limit > 0 else 10
            filters = dict(request.filters)
            options = dict(request.options)
            
            logger.info(f"SemanticSearch called for: {query_id}")
            
            start_time = time.time()
            
            # Perform semantic search
            search_result = self.semantic_retriever.search(
                query=query_text,
                collection=collection_name,
                limit=limit,
                filters=filters,
                options=options
            )
            
            search_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = retrieval_service_pb2.SemanticSearchResponse(
                success=True,
                message="Semantic search completed successfully"
            )
            
            # Build search result
            search_result_proto = retrieval_service_pb2.SearchResult()
            
            # Add documents
            for doc in search_result.get("documents", []):
                doc_proto = retrieval_service_pb2.RetrievedDocument(
                    document_id=doc.get("document_id", ""),
                    content=doc.get("content", ""),
                    score=doc.get("score", 0.0)
                )
                
                # Add metadata
                for key, value in doc.get("metadata", {}).items():
                    doc_proto.metadata[key] = str(value)
                
                search_result_proto.documents.append(doc_proto)
            
            # Build summary
            summary = retrieval_service_pb2.SearchSummary(
                total_results=len(search_result.get("documents", [])),
                search_time_ms=search_time,
                search_strategy="semantic"
            )
            
            search_result_proto.summary.CopyFrom(summary)
            response.result.CopyFrom(search_result_proto)
            
            logger.info(f"SemanticSearch completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in SemanticSearch: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def HybridSearch(self, request, context):
        """Perform hybrid search (semantic + keyword)"""
        try:
            query_id = request.query_id
            query_text = request.query_text
            collection_name = request.collection_name or "default"
            semantic_weight = request.semantic_weight if request.semantic_weight > 0 else 0.5
            keyword_weight = request.keyword_weight if request.keyword_weight > 0 else 0.5
            limit = request.limit if request.limit > 0 else 10
            filters = dict(request.filters)
            options = dict(request.options)
            
            logger.info(f"HybridSearch called for: {query_id}")
            
            start_time = time.time()
            
            # Perform hybrid search
            search_result = self.hybrid_retriever.search(
                query=query_text,
                collection=collection_name,
                semantic_weight=semantic_weight,
                keyword_weight=keyword_weight,
                limit=limit,
                filters=filters,
                options=options
            )
            
            search_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = retrieval_service_pb2.HybridSearchResponse(
                success=True,
                message="Hybrid search completed successfully"
            )
            
            # Build search result
            search_result_proto = retrieval_service_pb2.SearchResult()
            
            # Add documents
            for doc in search_result.get("documents", []):
                doc_proto = retrieval_service_pb2.RetrievedDocument(
                    document_id=doc.get("document_id", ""),
                    content=doc.get("content", ""),
                    score=doc.get("score", 0.0)
                )
                
                # Add metadata
                for key, value in doc.get("metadata", {}).items():
                    doc_proto.metadata[key] = str(value)
                
                search_result_proto.documents.append(doc_proto)
            
            # Build summary
            summary = retrieval_service_pb2.SearchSummary(
                total_results=len(search_result.get("documents", [])),
                search_time_ms=search_time,
                search_strategy="hybrid"
            )
            
            search_result_proto.summary.CopyFrom(summary)
            response.result.CopyFrom(search_result_proto)
            
            logger.info(f"HybridSearch completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in HybridSearch: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def FilterByMetadata(self, request, context):
        """Filter documents by metadata"""
        try:
            collection_name = request.collection_name or "default"
            filters = dict(request.filters)
            limit = request.limit if request.limit > 0 else 100
            options = dict(request.options)
            
            logger.info(f"FilterByMetadata called for collection: {collection_name}")
            
            # Perform metadata filtering
            filter_result = self.metadata_filter.filter(
                collection=collection_name,
                filters=filters,
                limit=limit,
                options=options
            )
            
            # Build protobuf response
            response = retrieval_service_pb2.FilterByMetadataResponse(
                success=True,
                message="Metadata filtering completed successfully"
            )
            
            # Build filter result
            filter_result_proto = retrieval_service_pb2.FilterResult(
                total_filtered=filter_result.get("total_filtered", 0)
            )
            
            # Add documents
            for doc in filter_result.get("documents", []):
                doc_proto = retrieval_service_pb2.RetrievedDocument(
                    document_id=doc.get("document_id", ""),
                    content=doc.get("content", ""),
                    score=doc.get("score", 0.0)
                )
                
                # Add metadata
                for key, value in doc.get("metadata", {}).items():
                    doc_proto.metadata[key] = str(value)
                
                filter_result_proto.documents.append(doc_proto)
            
            # Add applied filters
            for filter_key in filters.keys():
                filter_result_proto.applied_filters.append(filter_key)
            
            response.result.CopyFrom(filter_result_proto)
            
            logger.info(f"FilterByMetadata completed")
            return response
            
        except Exception as e:
            logger.error(f"Error in FilterByMetadata: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def BuildContext(self, request, context):
        """Build context from retrieved documents"""
        try:
            query_id = request.query_id
            documents = list(request.documents)
            max_context_length = request.max_context_length if request.max_context_length > 0 else 2000
            options = dict(request.options)
            
            logger.info(f"BuildContext called for: {query_id}")
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Build context
            context_result = self.context_builder.build(
                documents=doc_list,
                max_length=max_context_length,
                options=options
            )
            
            # Build protobuf response
            response = retrieval_service_pb2.BuildContextResponse(
                success=True,
                message="Context building completed successfully"
            )
            
            # Build context result
            context_result_proto = retrieval_service_pb2.ContextResult(
                context=context_result.get("context", ""),
                total_tokens=context_result.get("total_tokens", 0)
            )
            
            # Add sources
            for source in context_result.get("sources", []):
                source_proto = retrieval_service_pb2.ContextSource(
                    document_id=source.get("document_id", ""),
                    snippet=source.get("snippet", "")
                )
                
                # Add used chunk indices
                for idx in source.get("used_chunk_indices", []):
                    source_proto.used_chunk_indices.append(idx)
                
                context_result_proto.sources.append(source_proto)
            
            response.result.CopyFrom(context_result_proto)
            
            logger.info(f"BuildContext completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in BuildContext: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ExpandQuery(self, request, context):
        """Expand query with related terms"""
        try:
            query_id = request.query_id
            original_query = request.original_query
            expansion_strategy = request.expansion_strategy or "semantic"
            num_expansions = request.num_expansions if request.num_expansions > 0 else 5
            options = dict(request.options)
            
            logger.info(f"ExpandQuery called for: {query_id}")
            
            # Expand query
            expansion_result = self.query_expander.expand(
                query=original_query,
                strategy=expansion_strategy,
                num_expansions=num_expansions,
                options=options
            )
            
            # Build protobuf response
            response = retrieval_service_pb2.ExpandQueryResponse(
                success=True,
                message="Query expansion completed successfully"
            )
            
            # Build query expansion result
            expansion_result_proto = retrieval_service_pb2.QueryExpansionResult()
            
            # Add expanded queries
            for expanded in expansion_result.get("expanded_queries", []):
                expanded_proto = retrieval_service_pb2.ExpandedQuery(
                    query_text=expanded.get("query_text", ""),
                    expansion_score=expanded.get("expansion_score", 0.0),
                    expansion_type=expanded.get("expansion_type", expansion_strategy)
                )
                expansion_result_proto.expanded_queries.append(expanded_proto)
            
            response.result.CopyFrom(expansion_result_proto)
            
            logger.info(f"ExpandQuery completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ExpandQuery: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def GetRelevanceScores(self, request, context):
        """Get relevance scores for documents"""
        try:
            query_id = request.query_id
            documents = list(request.documents)
            query_text = request.query_text
            options = dict(request.options)
            
            logger.info(f"GetRelevanceScores called for: {query_id}")
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Get relevance scores
            scoring_result = self.relevance_scorer.score(
                query=query_text,
                documents=doc_list,
                options=options
            )
            
            # Build protobuf response
            response = retrieval_service_pb2.GetRelevanceScoresResponse(
                success=True,
                message="Relevance scoring completed successfully"
            )
            
            # Build relevance scoring result
            scoring_result_proto = retrieval_service_pb2.RelevanceScoringResult()
            
            # Add document scores
            for doc_score in scoring_result.get("scores", []):
                doc_score_proto = retrieval_service_pb2.DocumentScore(
                    document_id=doc_score.get("document_id", ""),
                    relevance_score=doc_score.get("relevance_score", 0.0)
                )
                
                # Add score components
                for comp in doc_score.get("components", []):
                    comp_proto = retrieval_service_pb2.ScoreComponent(
                        component_name=comp.get("name", ""),
                        score=comp.get("score", 0.0),
                        weight=comp.get("weight", 0.0)
                    )
                    doc_score_proto.components.append(comp_proto)
                
                scoring_result_proto.scores.append(doc_score_proto)
            
            # Build scoring summary
            summary = retrieval_service_pb2.ScoringSummary(
                average_score=scoring_result.get("average_score", 0.0),
                min_score=scoring_result.get("min_score", 0.0),
                max_score=scoring_result.get("max_score", 0.0),
                scoring_method=scoring_result.get("scoring_method", "hybrid")
            )
            
            scoring_result_proto.summary.CopyFrom(summary)
            response.result.CopyFrom(scoring_result_proto)
            
            logger.info(f"GetRelevanceScores completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GetRelevanceScores: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise


def serve(port: int = 50054):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    retrieval_service_pb2_grpc.add_RetrievalServiceServicer_to_server(
        RetrievalServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Retrieval Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50054
    serve(port)