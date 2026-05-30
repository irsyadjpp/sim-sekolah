"""
RabbitMQ Consumer for Embedding Service
Handles async embedding generation requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any, List
from datetime import datetime

from common.infrastructure.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from common.infrastructure.messaging.rabbitmq_messages import (
    EmbedTextMessage,
    EmbedTextBatchMessage,
    SuccessResponse,
    ErrorResponse
)
from common.config.settings import settings

# Import embedding components
from app.embedders.text.text_embedder import TextEmbedder
from app.embedders.image.image_embedder import ImageEmbedder
from app.embedders.table.table_embedder import TableEmbedder
from app.embedders.formula.formula_embedder import FormulaEmbedder

logger = logging.getLogger(__name__)


class EmbeddingServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Embedding Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize embedding consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="embedding.queue",
            exchange_name="ai.platform.exchange",
            routing_key="embedding.*",
            prefetch_count=10
        )
        
        # Initialize embedders
        self.text_embedder = TextEmbedder()
        self.image_embedder = ImageEmbedder()
        self.table_embedder = TableEmbedder()
        self.formula_embedder = FormulaEmbedder()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("EmbeddingServiceConsumer initialized")
    
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
            if message_type == "embed_text":
                return self._process_embed_text(message)
            elif message_type == "embed_text_batch":
                return self._process_embed_text_batch(message)
            elif message_type == "embed_image":
                return self._process_embed_image(message)
            elif message_type == "embed_table":
                return self._process_embed_table(message)
            elif message_type == "embed_formula":
                return self._process_embed_formula(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _process_embed_text(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process single text embedding request
        
        Args:
            message: EmbedTextMessage dictionary
            
        Returns:
            Embedding result
        """
        try:
            text_id = message.get('text_id')
            text_content = message.get('text_content')
            model = message.get('model', 'BAAI/bge-m3')
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating embedding for text: {text_id}")
            
            # Generate embedding
            embedding = self.text_embedder.embed(text_content, model=model)
            
            result = {
                "text_id": text_id,
                "embedding": embedding,
                "model": model,
                "dimension": len(embedding),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                text_id=text_id,
                result=result,
                message_type="embed_text"
            )
            
            logger.info(f"Embedding generated for text: {text_id}")
            
            return {
                "success": True,
                "text_id": text_id,
                "dimension": len(embedding),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error generating text embedding: {str(e)}")
            raise
    
    def _process_embed_text_batch(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process batch text embedding request
        
        Args:
            message: EmbedTextBatchMessage dictionary
            
        Returns:
            Batch embedding result
        """
        try:
            text_ids = message.get('text_ids', [])
            text_contents = message.get('text_contents', [])
            model = message.get('model', 'BAAI/bge-m3')
            batch_size = message.get('batch_size', 32)
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating batch embeddings for {len(text_contents)} texts")
            
            # Generate batch embeddings
            embeddings = self.text_embedder.embed_batch(
                texts=text_contents,
                model=model,
                batch_size=batch_size
            )
            
            result = {
                "text_ids": text_ids,
                "embeddings": embeddings,
                "model": model,
                "dimension": len(embeddings[0]) if embeddings else 0,
                "count": len(embeddings),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                text_id=f"batch_{len(text_ids)}",
                result=result,
                message_type="embed_text_batch"
            )
            
            logger.info(f"Batch embeddings generated for {len(text_contents)} texts")
            
            return {
                "success": True,
                "count": len(embeddings),
                "dimension": len(embeddings[0]) if embeddings else 0,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    def _process_embed_image(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image embedding request
        
        Args:
            message: Image embedding message dictionary
            
        Returns:
            Image embedding result
        """
        try:
            image_id = message.get('image_id') or message.get('text_id')
            image_data = message.get('image_data') or message.get('text_content')
            model = message.get('model', 'openai/clip-vit-base-patch32')
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating embedding for image: {image_id}")
            
            # Generate image embedding
            embedding = self.image_embedder.embed(image_data, model=model)
            
            result = {
                "image_id": image_id,
                "embedding": embedding,
                "model": model,
                "dimension": len(embedding),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                text_id=image_id,
                result=result,
                message_type="embed_image"
            )
            
            logger.info(f"Embedding generated for image: {image_id}")
            
            return {
                "success": True,
                "image_id": image_id,
                "dimension": len(embedding),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error generating image embedding: {str(e)}")
            raise
    
    def _process_embed_table(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process table embedding request
        
        Args:
            message: Table embedding message dictionary
            
        Returns:
            Table embedding result
        """
        try:
            table_id = message.get('table_id') or message.get('text_id')
            table_data = message.get('table_data') or message.get('text_content')
            model = message.get('model', 'BAAI/bge-m3')
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating embedding for table: {table_id}")
            
            # Generate table embedding
            embedding = self.table_embedder.embed(table_data, model=model)
            
            result = {
                "table_id": table_id,
                "embedding": embedding,
                "model": model,
                "dimension": len(embedding),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                text_id=table_id,
                result=result,
                message_type="embed_table"
            )
            
            logger.info(f"Embedding generated for table: {table_id}")
            
            return {
                "success": True,
                "table_id": table_id,
                "dimension": len(embedding),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error generating table embedding: {str(e)}")
            raise
    
    def _process_embed_formula(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process formula embedding request
        
        Args:
            message: Formula embedding message dictionary
            
        Returns:
            Formula embedding result
        """
        try:
            formula_id = message.get('formula_id') or message.get('text_id')
            formula_data = message.get('formula_data') or message.get('text_content')
            model = message.get('model', 'BAAI/bge-m3')
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating embedding for formula: {formula_id}")
            
            # Generate formula embedding
            embedding = self.formula_embedder.embed(formula_data, model=model)
            
            result = {
                "formula_id": formula_id,
                "embedding": embedding,
                "model": model,
                "dimension": len(embedding),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                text_id=formula_id,
                result=result,
                message_type="embed_formula"
            )
            
            logger.info(f"Embedding generated for formula: {formula_id}")
            
            return {
                "success": True,
                "formula_id": formula_id,
                "dimension": len(embedding),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error generating formula embedding: {str(e)}")
            raise
    
    def _publish_result(self, text_id: str, result: Dict[str, Any], message_type: str):
        """Publish embedding result to result queue"""
        try:
            response_message = SuccessResponse(
                message_id=text_id,
                message_type=f"{message_type}_result",
                timestamp=datetime.utcnow().isoformat(),
                priority="medium",
                success=True,
                result=result
            )
            
            self.result_producer.publish_message(
                exchange_name="ai.platform.exchange",
                routing_key=f"embedding.result.{text_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {text_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncEmbeddingServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of embedding consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="embedding.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="embedding.*",
                       prefetch_count=10)
        
        # Initialize embedders
        self.text_embedder = TextEmbedder()
        self.image_embedder = ImageEmbedder()
        self.table_embedder = TableEmbedder()
        self.formula_embedder = FormulaEmbedder()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncEmbeddingServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = EmbeddingServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the embedding service consumer"""
    logger.info("Starting Embedding Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncEmbeddingServiceConsumer()
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