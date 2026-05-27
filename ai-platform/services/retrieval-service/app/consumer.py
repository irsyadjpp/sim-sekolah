"""
RabbitMQ Consumer for Retrieval Service
Handles async retrieval and search requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any
from datetime import datetime

from shared.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from shared.messaging.rabbitmq_messages import (
    SemanticSearchMessage,
    SuccessResponse,
    ErrorResponse
)
from shared.configs.settings import settings

# Import retrieval components
from app.retrievers.semantic_retriever import SemanticRetriever
from app.retrievers.hybrid_retriever import HybridRetriever
from app.retrievers.metadata_retriever import MetadataRetriever
from app.query_builders.query_builder import QueryBuilder
from app.context_builders.context_builder import ContextBuilder

logger = logging.getLogger(__name__)


class RetrievalServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Retrieval Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize retrieval consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="retrieval.queue",
            exchange_name="ai.platform.exchange",
            routing_key="retrieval.*",
            prefetch_count=10
        )
        
        # Initialize retrievers
        self.semantic_retriever = SemanticRetriever()
        self.hybrid_retriever = HybridRetriever()
        self.metadata_retriever = MetadataRetriever()
        self.query_builder = QueryBuilder()
        self.context_builder = ContextBuilder()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("RetrievalServiceConsumer initialized")
    
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
            if message_type == "semantic_search":
                return self._process_semantic_search(message)
            elif message_type == "hybrid_search":
                return self._process_hybrid_search(message)
            elif message_type == "metadata_search":
                return self._process_metadata_search(message)
            elif message_type == "query_build":
                return self._process_query_build(message)
            elif message_type == "context_build":
                return self._process_context_build(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _process_semantic_search(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process semantic search request
        
        Args:
            message: SemanticSearchMessage dictionary
            
        Returns:
            Semantic search results
        """
        try:
            query = message.get('query')
            collection_name = message.get('collection_name', 'documents')
            limit = message.get('limit', 10)
            filters = message.get('filters', {})
            metadata = message.get('metadata', {})
            
            logger.info(f"Performing semantic search: {query}")
            
            # Perform semantic search
            results = self.semantic_retriever.search(
                query=query,
                collection_name=collection_name,
                limit=limit,
                filters=filters
            )
            
            result = {
                "query": query,
                "results": results,
                "collection_name": collection_name,
                "count": len(results),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"search_{query[:20]}",
                result=result,
                message_type="semantic_search"
            )
            
            logger.info(f"Semantic search completed: {len(results)} results")
            
            return {
                "success": True,
                "count": len(results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error performing semantic search: {str(e)}")
            raise
    
    def _process_hybrid_search(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process hybrid search request
        
        Args:
            message: Hybrid search message dictionary
            
        Returns:
            Hybrid search results
        """
        try:
            query = message.get('query')
            collection_name = message.get('collection_name', 'documents')
            limit = message.get('limit', 10)
            filters = message.get('filters', {})
            semantic_weight = message.get('semantic_weight', 0.7)
            keyword_weight = message.get('keyword_weight', 0.3)
            metadata = message.get('metadata', {})
            
            logger.info(f"Performing hybrid search: {query}")
            
            # Perform hybrid search
            results = self.hybrid_retriever.search(
                query=query,
                collection_name=collection_name,
                limit=limit,
                filters=filters,
                semantic_weight=semantic_weight,
                keyword_weight=keyword_weight
            )
            
            result = {
                "query": query,
                "results": results,
                "collection_name": collection_name,
                "count": len(results),
                "semantic_weight": semantic_weight,
                "keyword_weight": keyword_weight,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"hybrid_{query[:20]}",
                result=result,
                message_type="hybrid_search"
            )
            
            logger.info(f"Hybrid search completed: {len(results)} results")
            
            return {
                "success": True,
                "count": len(results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error performing hybrid search: {str(e)}")
            raise
    
    def _process_metadata_search(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process metadata-filtered search request
        
        Args:
            message: Metadata search message dictionary
            
        Returns:
            Metadata search results
        """
        try:
            filters = message.get('filters', {})
            collection_name = message.get('collection_name', 'documents')
            limit = message.get('limit', 10)
            metadata = message.get('metadata', {})
            
            logger.info(f"Performing metadata search with filters: {filters}")
            
            # Perform metadata search
            results = self.metadata_retriever.search(
                filters=filters,
                collection_name=collection_name,
                limit=limit
            )
            
            result = {
                "filters": filters,
                "results": results,
                "collection_name": collection_name,
                "count": len(results),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"metadata_{str(filters)[:20]}",
                result=result,
                message_type="metadata_search"
            )
            
            logger.info(f"Metadata search completed: {len(results)} results")
            
            return {
                "success": True,
                "count": len(results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error performing metadata search: {str(e)}")
            raise
    
    def _process_query_build(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process query building request
        
        Args:
            message: Query build message dictionary
            
        Returns:
            Optimized query
        """
        try:
            query = message.get('query')
            expansion_type = message.get('expansion_type', 'semantic')
            metadata = message.get('metadata', {})
            
            logger.info(f"Building query: {query}")
            
            # Build optimized query
            optimized_query = self.query_builder.build_query(
                query=query,
                expansion_type=expansion_type
            )
            
            result = {
                "original_query": query,
                "optimized_query": optimized_query,
                "expansion_type": expansion_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"query_{query[:20]}",
                result=result,
                message_type="query_build"
            )
            
            logger.info(f"Query building completed: {query}")
            
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error building query: {str(e)}")
            raise
    
    def _process_context_build(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process context building request
        
        Args:
            message: Context build message dictionary
            
        Returns:
            Built context
        """
        try:
            documents = message.get('documents', [])
            context_type = message.get('context_type', 'ranked')
            max_length = message.get('max_length', 2000)
            metadata = message.get('metadata', {})
            
            logger.info(f"Building context from {len(documents)} documents")
            
            # Build context
            context = self.context_builder.build_context(
                documents=documents,
                context_type=context_type,
                max_length=max_length
            )
            
            result = {
                "context": context,
                "document_count": len(documents),
                "context_type": context_type,
                "length": len(context),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                query_id=f"context_{len(documents)}_docs",
                result=result,
                message_type="context_build"
            )
            
            logger.info(f"Context building completed: {len(context)} characters")
            
            return {
                "success": True,
                "length": len(context),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            raise
    
    def _publish_result(self, query_id: str, result: Dict[str, Any], message_type: str):
        """Publish retrieval result to result queue"""
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
                routing_key=f"retrieval.result.{query_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {query_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncRetrievalServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of retrieval consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="retrieval.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="retrieval.*",
                       prefetch_count=10)
        
        # Initialize retrievers
        self.semantic_retriever = SemanticRetriever()
        self.hybrid_retriever = HybridRetriever()
        self.metadata_retriever = MetadataRetriever()
        self.query_builder = QueryBuilder()
        self.context_builder = ContextBuilder()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncRetrievalServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = RetrievalServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the retrieval service consumer"""
    logger.info("Starting Retrieval Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncRetrievalServiceConsumer()
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