"""
RabbitMQ Consumer for Reranking Service
Handles async reranking requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any
from datetime import datetime

from shared.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from shared.messaging.rabbitmq_messages import (
    SuccessResponse,
    ErrorResponse
)
from shared.configs.settings import settings

# Import reranking components
from app.cross_encoder.cross_encoder import CrossEncoderReranker
from app.ranking.curriculum_reranker import CurriculumReranker
from app.ranking.pedagogy_reranker import PedagogyReranker
from app.ranking.competency_reranker import CompetencyReranker

logger = logging.getLogger(__name__)


class RerankingServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Reranking Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize reranking service consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="reranking.queue",
            exchange_name="ai.platform.exchange",
            routing_key="reranking.*",
            prefetch_count=5
        )
        
        # Initialize reranking components
        self.cross_encoder_reranker = CrossEncoderReranker(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            device=settings.embedding_device
        )
        self.curriculum_reranker = CurriculumReranker()
        self.pedagogy_reranker = PedagogyReranker()
        self.competency_reranker = CompetencyReranker()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("RerankingServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming message
        
        Args:
            message: Message dictionary from RabbitMQ
            
        Returns:
            Response dictionary with result
        """
        message_type = message.get('message_type', 'unknown')
        logger.info(f"Processing message type: {message_type}")
        
        try:
            if message_type == "rerank_cross_encoder":
                return self._process_cross_encoder_rerank(message)
            elif message_type == "rerank_curriculum":
                return self._process_curriculum_rerank(message)
            elif message_type == "rerank_pedagogy":
                return self._process_pedagogy_rerank(message)
            elif message_type == "rerank_competency":
                return self._process_competency_rerank(message)
            elif message_type == "rerank_hybrid":
                return self._process_hybrid_rerank(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _process_cross_encoder_rerank(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process cross-encoder reranking request
        
        Args:
            message: Cross-encoder reranking message dictionary
            
        Returns:
            Reranking result
        """
        try:
            query = message.get('query')
            documents = message.get('documents', [])
            top_k = message.get('top_k', 10)
            metadata = message.get('metadata', {})
            
            logger.info(f"Cross-encoder reranking for query: {query[:50]}")
            
            # Rerank using cross-encoder
            reranked_results = self.cross_encoder_reranker.rerank(
                query=query,
                documents=documents,
                top_k=top_k
            )
            
            result = {
                "query": query,
                "reranked_documents": reranked_results,
                "original_count": len(documents),
                "reranked_count": len(reranked_results),
                "reranking_method": "cross_encoder",
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"ce_{query[:20]}",
                result=result,
                message_type="rerank_cross_encoder"
            )
            
            logger.info(f"Cross-encoder reranking completed: {len(reranked_results)} results")
            
            return {
                "success": True,
                "reranked_count": len(reranked_results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error cross-encoder reranking: {str(e)}")
            raise
    
    def _process_curriculum_rerank(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process curriculum-aware reranking request
        
        Args:
            message: Curriculum reranking message dictionary
            
        Returns:
            Reranking result
        """
        try:
            query = message.get('query')
            documents = message.get('documents', [])
            grade_level = message.get('grade_level', '10')
            subject = message.get('subject', 'general')
            curriculum_standard = message.get('curriculum_standard', 'kurikulum_merdeka')
            top_k = message.get('top_k', 10)
            metadata = message.get('metadata', {})
            
            logger.info(f"Curriculum reranking for query: {query[:50]}")
            
            # Rerank using curriculum-aware strategy
            reranked_results = self.curriculum_reranker.rerank(
                query=query,
                documents=documents,
                grade_level=grade_level,
                subject=subject,
                curriculum_standard=curriculum_standard,
                top_k=top_k
            )
            
            result = {
                "query": query,
                "reranked_documents": reranked_results,
                "original_count": len(documents),
                "reranked_count": len(reranked_results),
                "reranking_method": "curriculum_aware",
                "grade_level": grade_level,
                "subject": subject,
                "curriculum_standard": curriculum_standard,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"curr_{query[:20]}",
                result=result,
                message_type="rerank_curriculum"
            )
            
            logger.info(f"Curriculum reranking completed: {len(reranked_results)} results")
            
            return {
                "success": True,
                "reranked_count": len(reranked_results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error curriculum reranking: {str(e)}")
            raise
    
    def _process_pedagogy_rerank(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process pedagogy-aware reranking request
        
        Args:
            message: Pedagogy reranking message dictionary
            
        Returns:
            Reranking result
        """
        try:
            query = message.get('query')
            documents = message.get('documents', [])
            learning_objective = message.get('learning_objective', '')
            pedagogy_type = message.get('pedagogy_type', 'inquiry_based')
            top_k = message.get('top_k', 10)
            metadata = message.get('metadata', {})
            
            logger.info(f"Pedagogy reranking for query: {query[:50]}")
            
            # Rerank using pedagogy-aware strategy
            reranked_results = self.pedagogy_reranker.rerank(
                query=query,
                documents=documents,
                learning_objective=learning_objective,
                pedagogy_type=pedagogy_type,
                top_k=top_k
            )
            
            result = {
                "query": query,
                "reranked_documents": reranked_results,
                "original_count": len(documents),
                "reranked_count": len(reranked_results),
                "reranking_method": "pedagogy_aware",
                "learning_objective": learning_objective,
                "pedagogy_type": pedagogy_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"ped_{query[:20]}",
                result=result,
                message_type="rerank_pedagogy"
            )
            
            logger.info(f"Pedagogy reranking completed: {len(reranked_results)} results")
            
            return {
                "success": True,
                "reranked_count": len(reranked_results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error pedagogy reranking: {str(e)}")
            raise
    
    def _process_competency_rerank(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process competency-aware reranking request
        
        Args:
            message: Competency reranking message dictionary
            
        Returns:
            Reranking result
        """
        try:
            query = message.get('query')
            documents = message.get('documents', [])
            competency_type = message.get('competency_type', 'KI-3')
            competency_level = message.get('competency_level', 'medium')
            top_k = message.get('top_k', 10)
            metadata = message.get('metadata', {})
            
            logger.info(f"Competency reranking for query: {query[:50]}")
            
            # Rerank using competency-aware strategy
            reranked_results = self.competency_reranker.rerank(
                query=query,
                documents=documents,
                competency_type=competency_type,
                competency_level=competency_level,
                top_k=top_k
            )
            
            result = {
                "query": query,
                "reranked_documents": reranked_results,
                "original_count": len(documents),
                "reranked_count": len(reranked_results),
                "reranking_method": "competency_aware",
                "competency_type": competency_type,
                "competency_level": competency_level,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"comp_{query[:20]}",
                result=result,
                message_type="rerank_competency"
            )
            
            logger.info(f"Competency reranking completed: {len(reranked_results)} results")
            
            return {
                "success": True,
                "reranked_count": len(reranked_results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error competency reranking: {str(e)}")
            raise
    
    def _process_hybrid_rerank(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process hybrid reranking request (combining multiple strategies)
        
        Args:
            message: Hybrid reranking message dictionary
            
        Returns:
            Reranking result
        """
        try:
            query = message.get('query')
            documents = message.get('documents', [])
            strategies = message.get('strategies', ['cross_encoder', 'curriculum'])
            strategy_weights = message.get('strategy_weights', {'cross_encoder': 0.5, 'curriculum': 0.5})
            top_k = message.get('top_k', 10)
            metadata = message.get('metadata', {})
            
            logger.info(f"Hybrid reranking for query: {query[:50]}")
            
            # Apply each reranking strategy
            all_reranked = []
            for strategy in strategies:
                if strategy == 'cross_encoder':
                    results = self.cross_encoder_reranker.rerank(query, documents, top_k)
                    all_reranked.append(('cross_encoder', results))
                elif strategy == 'curriculum':
                    results = self.curriculum_reranker.rerank(
                        query, documents, 
                        grade_level=metadata.get('grade_level', '10'),
                        subject=metadata.get('subject', 'general'),
                        top_k=top_k
                    )
                    all_reranked.append(('curriculum', results))
                elif strategy == 'pedagogy':
                    results = self.pedagogy_reranker.rerank(
                        query, documents,
                        learning_objective=metadata.get('learning_objective', ''),
                        pedagogy_type=metadata.get('pedagogy_type', 'inquiry_based'),
                        top_k=top_k
                    )
                    all_reranked.append(('pedagogy', results))
                elif strategy == 'competency':
                    results = self.competency_reranker.rerank(
                        query, documents,
                        competency_type=metadata.get('competency_type', 'KI-3'),
                        competency_level=metadata.get('competency_level', 'medium'),
                        top_k=top_k
                    )
                    all_reranked.append(('competency', results))
            
            # Combine results using weighted scores
            combined_scores = {}
            for strategy_name, results in all_reranked:
                weight = strategy_weights.get(strategy_name, 1.0 / len(strategies))
                for idx, doc in enumerate(results):
                    doc_id = doc.get('id', f"doc_{idx}")
                    score = doc.get('score', 1.0 - (idx / len(results)))
                    if doc_id not in combined_scores:
                        combined_scores[doc_id] = {
                            'document': doc,
                            'total_score': 0.0,
                            'strategies': []
                        }
                    combined_scores[doc_id]['total_score'] += score * weight
                    combined_scores[doc_id]['strategies'].append(strategy_name)
            
            # Sort by combined score
            final_results = sorted(
                combined_scores.values(),
                key=lambda x: x['total_score'],
                reverse=True
            )[:top_k]
            
            reranked_documents = [
                {
                    **item['document'],
                    'combined_score': item['total_score'],
                    'strategies_used': item['strategies']
                }
                for item in final_results
            ]
            
            result = {
                "query": query,
                "reranked_documents": reranked_documents,
                "original_count": len(documents),
                "reranked_count": len(reranked_documents),
                "reranking_method": "hybrid",
                "strategies": strategies,
                "strategy_weights": strategy_weights,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"hybrid_{query[:20]}",
                result=result,
                message_type="rerank_hybrid"
            )
            
            logger.info(f"Hybrid reranking completed: {len(reranked_documents)} results")
            
            return {
                "success": True,
                "reranked_count": len(reranked_documents),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error hybrid reranking: {str(e)}")
            raise
    
    def _publish_result(self, query_id: str, result: Dict[str, Any], message_type: str):
        """Publish reranking result to result queue"""
        try:
            response_message = SuccessResponse(
                message_id=query_id,
                message_type=f"{message_type}_result",
                timestamp=datetime.utcnow().isoformat(),
                priority="medium",
                success=True,
                result=result
            )
            
            self.result_producer.publish_message(
                exchange_name="ai.platform.exchange",
                routing_key=f"reranking.result.{query_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {query_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncRerankingServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of reranking service consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="reranking.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="reranking.*",
                       prefetch_count=5)
        
        # Initialize reranking components
        self.cross_encoder_reranker = CrossEncoderReranker(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            device=settings.embedding_device
        )
        self.curriculum_reranker = CurriculumReranker()
        self.pedagogy_reranker = PedagogyReranker()
        self.competency_reranker = CompetencyReranker()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncRerankingServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = RerankingServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the reranking service consumer"""
    logger.info("Starting Reranking Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncRerankingServiceConsumer()
        consumer.start_consuming_async()
        
        # Keep main thread alive
        import time
        while consumer.is_alive():
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping consumer")
        consumer.stop_consuming_async()
    except Exception as e:
        logger.error(f"Consumer error: {str(e)}")
        consumer.stop_consuming_async()


if __name__ == "__main__":
    start_consumer()
