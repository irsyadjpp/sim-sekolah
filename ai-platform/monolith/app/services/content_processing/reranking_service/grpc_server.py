"""
gRPC Server for Reranking Service
Handles synchronous reranking requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
import time

# Import proto files
import app.reranking_service_pb2 as reranking_service_pb2
import app.reranking_service_pb2_grpc as reranking_service_pb2_grpc

# Import reranking components
from app.rerankers.cross_encoder_reranker import CrossEncoderReranker
from app.rerankers.mono_encoder_reranker import MonoEncoderReranker
from app.rerankers.curriculum_aware_reranker import CurriculumAwareReranker
from app.rerankers.pedagogy_aware_reranker import PedagogyAwareReranker
from app.rerankers.competency_aware_reranker import CompetencyAwareReranker
from app.rerankers.hybrid_reranker import HybridReranker

logger = logging.getLogger(__name__)


class RerankingServicer(reranking_service_pb2_grpc.RerankingServiceServicer):
    """gRPC Servicer for Reranking Service"""
    
    def __init__(self):
        # Initialize rerankers
        self.cross_encoder_reranker = CrossEncoderReranker()
        self.mono_encoder_reranker = MonoEncoderReranker()
        self.curriculum_aware_reranker = CurriculumAwareReranker()
        self.pedagogy_aware_reranker = PedagogyAwareReranker()
        self.competency_aware_reranker = CompetencyAwareReranker()
        self.hybrid_reranker = HybridReranker()
        logger.info("RerankingServicer initialized")
    
    def RerankCrossEncoder(self, request, context):
        """Rerank using cross-encoder model"""
        try:
            query_id = request.query_id
            query = request.query
            documents = list(request.documents)
            reranking_model = request.reranking_model or "default"
            top_k = request.top_k if request.top_k > 0 else 10
            options = dict(request.options)
            
            logger.info(f"RerankCrossEncoder called for: {query_id}")
            
            start_time = time.time()
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Rerank using cross-encoder
            rerank_result = self.cross_encoder_reranker.rerank(
                query=query,
                documents=doc_list,
                model=reranking_model,
                top_k=top_k,
                options=options
            )
            
            reranking_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = reranking_service_pb2.RerankCrossEncoderResponse(
                success=True,
                message="Cross-encoder reranking completed successfully"
            )
            
            # Build reranking result
            reranking_result_proto = self._build_reranking_result(
                rerank_result, reranking_time, "cross_encoder"
            )
            
            response.result.CopyFrom(reranking_result_proto)
            
            logger.info(f"RerankCrossEncoder completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in RerankCrossEncoder: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def RerankMonoEncoder(self, request, context):
        """Rerank using mono-encoder model"""
        try:
            query_id = request.query_id
            query = request.query
            documents = list(request.documents)
            reranking_model = request.reranking_model or "default"
            top_k = request.top_k if request.top_k > 0 else 10
            options = dict(request.options)
            
            logger.info(f"RerankMonoEncoder called for: {query_id}")
            
            start_time = time.time()
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Rerank using mono-encoder
            rerank_result = self.mono_encoder_reranker.rerank(
                query=query,
                documents=doc_list,
                model=reranking_model,
                top_k=top_k,
                options=options
            )
            
            reranking_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = reranking_service_pb2.RerankMonoEncoderResponse(
                success=True,
                message="Mono-encoder reranking completed successfully"
            )
            
            # Build reranking result
            reranking_result_proto = self._build_reranking_result(
                rerank_result, reranking_time, "mono_encoder"
            )
            
            response.result.CopyFrom(reranking_result_proto)
            
            logger.info(f"RerankMonoEncoder completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in RerankMonoEncoder: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def CurriculumAwareRerank(self, request, context):
        """Rerank with curriculum awareness"""
        try:
            query_id = request.query_id
            query = request.query
            documents = list(request.documents)
            phase = request.phase or ""
            grade = request.grade or ""
            subject = request.subject or ""
            target_competencies = list(request.target_competencies)
            top_k = request.top_k if request.top_k > 0 else 10
            options = dict(request.options)
            
            logger.info(f"CurriculumAwareRerank called for: {query_id}")
            
            start_time = time.time()
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Rerank with curriculum awareness
            rerank_result = self.curriculum_aware_reranker.rerank(
                query=query,
                documents=doc_list,
                phase=phase,
                grade=grade,
                subject=subject,
                target_competencies=target_competencies,
                top_k=top_k,
                options=options
            )
            
            reranking_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = reranking_service_pb2.CurriculumAwareRerankResponse(
                success=True,
                message="Curriculum-aware reranking completed successfully"
            )
            
            # Build reranking result
            reranking_result_proto = self._build_reranking_result(
                rerank_result, reranking_time, "curriculum_aware"
            )
            
            response.result.CopyFrom(reranking_result_proto)
            
            logger.info(f"CurriculumAwareRerank completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in CurriculumAwareRerank: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def PedagogyAwareRerank(self, request, context):
        """Rerank with pedagogy awareness"""
        try:
            query_id = request.query_id
            query = request.query
            documents = list(request.documents)
            pedagogy_type = request.pedagogy_type or "direct_instruction"
            grade = request.grade or ""
            subject = request.subject or ""
            learning_objectives = list(request.learning_objectives)
            top_k = request.top_k if request.top_k > 0 else 10
            options = dict(request.options)
            
            logger.info(f"PedagogyAwareRerank called for: {query_id}")
            
            start_time = time.time()
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Rerank with pedagogy awareness
            rerank_result = self.pedagogy_aware_reranker.rerank(
                query=query,
                documents=doc_list,
                pedagogy_type=pedagogy_type,
                grade=grade,
                subject=subject,
                learning_objectives=learning_objectives,
                top_k=top_k,
                options=options
            )
            
            reranking_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = reranking_service_pb2.PedagogyAwareRerankResponse(
                success=True,
                message="Pedagogy-aware reranking completed successfully"
            )
            
            # Build reranking result
            reranking_result_proto = self._build_reranking_result(
                rerank_result, reranking_time, "pedagogy_aware"
            )
            
            response.result.CopyFrom(reranking_result_proto)
            
            logger.info(f"PedagogyAwareRerank completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in PedagogyAwareRerank: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def CompetencyAwareRerank(self, request, context):
        """Rerank with competency awareness"""
        try:
            query_id = request.query_id
            query = request.query
            documents = list(request.documents)
            target_competencies = list(request.target_competencies)
            subject = request.subject or ""
            grade = request.grade or ""
            top_k = request.top_k if request.top_k > 0 else 10
            options = dict(request.options)
            
            logger.info(f"CompetencyAwareRerank called for: {query_id}")
            
            start_time = time.time()
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Rerank with competency awareness
            rerank_result = self.competency_aware_reranker.rerank(
                query=query,
                documents=doc_list,
                target_competencies=target_competencies,
                subject=subject,
                grade=grade,
                top_k=top_k,
                options=options
            )
            
            reranking_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = reranking_service_pb2.CompetencyAwareRerankResponse(
                success=True,
                message="Competency-aware reranking completed successfully"
            )
            
            # Build reranking result
            reranking_result_proto = self._build_reranking_result(
                rerank_result, reranking_time, "competency_aware"
            )
            
            response.result.CopyFrom(reranking_result_proto)
            
            logger.info(f"CompetencyAwareRerank completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in CompetencyAwareRerank: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def HybridRerank(self, request, context):
        """Rerank using hybrid strategy"""
        try:
            query_id = request.query_id
            query = request.query
            documents = list(request.documents)
            strategies = list(request.strategies)
            strategy_weights = list(request.strategy_weights)
            top_k = request.top_k if request.top_k > 0 else 10
            options = dict(request.options)
            
            logger.info(f"HybridRerank called for: {query_id}")
            
            start_time = time.time()
            
            # Convert protobuf documents to internal format
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "document_id": doc.document_id,
                    "content": doc.content,
                    "score": doc.score,
                    "metadata": dict(doc.metadata)
                })
            
            # Convert strategies to internal format
            strategy_list = []
            for strategy in strategies:
                strategy_list.append({
                    "strategy_name": strategy.strategy_name,
                    "strategy_type": strategy.strategy_type,
                    "parameters": dict(strategy.parameters)
                })
            
            # Rerank using hybrid strategy
            rerank_result = self.hybrid_reranker.rerank(
                query=query,
                documents=doc_list,
                strategies=strategy_list,
                strategy_weights=strategy_weights,
                top_k=top_k,
                options=options
            )
            
            reranking_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = reranking_service_pb2.HybridRerankResponse(
                success=True,
                message="Hybrid reranking completed successfully"
            )
            
            # Build reranking result
            reranking_result_proto = self._build_reranking_result(
                rerank_result, reranking_time, "hybrid"
            )
            
            response.result.CopyFrom(reranking_result_proto)
            
            logger.info(f"HybridRerank completed for: {query_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in HybridRerank: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def _build_reranking_result(self, rerank_result, reranking_time, method):
        """Helper method to build reranking result protobuf"""
        reranking_result_proto = reranking_service_pb2.RerankingResult()
        
        # Add reranked documents
        for doc in rerank_result.get("reranked_documents", []):
            doc_proto = reranking_service_pb2.RetrievalResult(
                document_id=doc.get("document_id", ""),
                content=doc.get("content", ""),
                score=doc.get("score", 0.0)
            )
            
            # Add metadata
            for key, value in doc.get("metadata", {}).items():
                doc_proto.metadata[key] = str(value)
            
            reranking_result_proto.reranked_documents.append(doc_proto)
        
        # Build summary
        summary = reranking_service_pb2.RerankingSummary(
            reranking_method=method,
            reranking_time_ms=reranking_time,
            improvement_score=rerank_result.get("improvement_score", 0.0)
        )
        
        # Add metrics
        for metric in rerank_result.get("metrics", []):
            metric_proto = reranking_service_pb2.Metric(
                metric_name=metric.get("name", ""),
                value=metric.get("value", 0.0)
            )
            summary.metrics.append(metric_proto)
        
        reranking_result_proto.summary.CopyFrom(summary)
        return reranking_result_proto


def serve(port: int = 50058):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    reranking_service_pb2_grpc.add_RerankingServiceServicer_to_server(
        RerankingServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Reranking Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50058
    serve(port)