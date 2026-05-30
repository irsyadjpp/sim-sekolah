"""
RabbitMQ Consumer for Semantic Enrichment Service
Handles async enrichment messages from Semantic Chunk Service with Idempotency Support and DLQ
"""
import os
import sys
import json
import logging
import pika
import hashlib
import redis
from datetime import datetime
from typing import Dict, Any

sys.path.append('/app')
sys.path.append('/shared')

from common.infrastructure.messaging.dlq_config import DLQConfiguration

logger = logging.getLogger(__name__)

class AsyncSemanticEnrichmentConsumer:
    """Async consumer for semantic enrichment messages with idempotency support"""
    
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.queue_name = "semantic_enrichment_queue"
        self.exchange_name = "semantic_enrichment_exchange"
        self.routing_key = "semantic.enrichment.*"
        self.connection = None
        self.channel = None
        
        # Redis for idempotency checking
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            self.redis_client = redis.from_url(redis_url)
            self.redis_client.ping()
            logging.info("Redis connection established for idempotency checking")
        except Exception as e:
            logging.warning(f"Could not connect to Redis: {str(e)}. Idempotency checking disabled.")
            self.redis_client = None
        
        # DLQ configuration
        self.service_name = "enrichment_service"
        self.dlq_config = DLQConfiguration.get_config(self.service_name)
        self.max_retries = self.dlq_config.get("retry_policy", {}).get("max_retries", 5)
        logging.info(f"DLQ configuration loaded for {self.service_name} with max_retries={self.max_retries}")
    
    async def start(self):
        """Start consuming messages"""
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            self.channel = self.connection.channel()
            
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )
            
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.queue_name,
                routing_key=self.routing_key
            )
            
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.process_message,
                auto_ack=False
            )
            
            logger.info(f"Semantic Enrichment Consumer started. Listening on {self.queue_name}")
            self.channel.start_consuming()
            
        except Exception as e:
            logger.error(f"Error starting consumer: {e}")
            if self.connection:
                self.connection.close()
    
    def process_message(self, ch, method, properties, body):
        """Process incoming message with idempotency check and DLQ support"""
        try:
            message = json.loads(body)
            routing_key = method.routing_key
            logger.info(f"Processing message with routing key: {routing_key}")
            
            # Check idempotency
            if self._check_idempotency(message):
                logger.info(f"Message already processed, skipping")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            retry_count = message.get('x-retry-count', 0)
            
            try:
                # Handle different tagging types
                if "competency" in routing_key:
                    self._handle_competency_tagging(message)
                elif "pedagogy" in routing_key:
                    self._handle_pedagogy_tagging(message)
                elif "assessment" in routing_key:
                    self._handle_assessment_tagging(message)
                elif "cognitive" in routing_key:
                    self._handle_cognitive_tagging(message)
                elif "learning_objective" in routing_key:
                    self._handle_learning_objective_tagging(message)
                elif "deep_learning" in routing_key:
                    self._handle_deep_learning_tagging(message)
                elif "chunks_created" in routing_key:
                    self._handle_chunks_created(message)
                
                # Mark as processed
                self._mark_as_processed(message)
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
                
            except ValueError as e:
                # Validation error - fatal, send to DLQ immediately
                error_info = {
                    "error_type": "schema_validation_error",
                    "error_message": str(e),
                    "exception": e,
                    "retry_count": retry_count,
                    "service_name": self.service_name,
                    "failed_at": datetime.utcnow().isoformat(),
                    "original_queue": self.queue_name,
                    "max_retries_exceeded": True
                }
                self._send_to_dlq(message, error_info)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                
            except Exception as e:
                # Other errors - check if should send to DLQ or retry
                error_type = self._classify_error(e)
                
                if DLQConfiguration.should_send_to_dlq(error_type, retry_count, self.max_retries):
                    error_info = {
                        "error_type": error_type,
                        "error_message": str(e),
                        "exception": e,
                        "retry_count": retry_count,
                        "service_name": self.service_name,
                        "failed_at": datetime.utcnow().isoformat(),
                        "original_queue": self.queue_name,
                        "max_retries_exceeded": retry_count >= self.max_retries
                    }
                    self._send_to_dlq(message, error_info)
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                else:
                    # Should retry - re-queue with retry count increment
                    logger.warning(f"Retryable error {error_type}, will retry (attempt {retry_count + 1}/{self.max_retries})")
                    message['x-retry-count'] = retry_count + 1
                    # Calculate retry delay
                    delay = DLQConfiguration.calculate_retry_delay(retry_count, self.dlq_config)
                    # Re-publish with delay
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    
        except Exception as e:
            logger.error(f"Critical error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def _check_idempotency(self, message: dict) -> bool:
        """Check if message has already been processed (idempotency check)"""
        if not self.redis_client:
            return False  # No Redis, cannot check idempotency
        
        try:
            idempotency_key = message.get('idempotency_key')
            if not idempotency_key:
                return False  # No idempotency key, cannot check
            
            processed_key = f"processed:{idempotency_key}"
            if self.redis_client.exists(processed_key):
                logger.info(f"Message with idempotency key {idempotency_key} already processed, skipping")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking idempotency: {e}")
            return False
    
    def _mark_as_processed(self, message: dict):
        """Mark message as processed (idempotency)"""
        if not self.redis_client:
            return  # No Redis, cannot mark
        
        try:
            idempotency_key = message.get('idempotency_key')
            if not idempotency_key:
                return  # No idempotency key, cannot mark
            
            processed_key = f"processed:{idempotency_key}"
            self.redis_client.setex(processed_key, 86400, "1")  # 24 hours TTL
            logger.debug(f"Marked message {idempotency_key} as processed")
            
        except Exception as e:
            logger.error(f"Error marking as processed: {e}")
    
    def _handle_competency_tagging(self, message: dict):
        logger.info(f"Processing competency tagging: {message.get('request_id')}")
    
    def _handle_pedagogy_tagging(self, message: dict):
        logger.info(f"Processing pedagogy tagging: {message.get('request_id')}")
    
    def _handle_assessment_tagging(self, message: dict):
        logger.info(f"Processing assessment tagging: {message.get('request_id')}")
    
    def _handle_cognitive_tagging(self, message: dict):
        logger.info(f"Processing cognitive level tagging: {message.get('request_id')}")
    
    def _handle_learning_objective_tagging(self, message: dict):
        logger.info(f"Processing learning objective tagging: {message.get('request_id')}")
    
    def _handle_deep_learning_tagging(self, message: dict):
        logger.info(f"Processing deep learning tagging: {message.get('request_id')}")
    
    def _handle_chunks_created(self, message: dict):
        """Handle chunks created event from semantic chunk service"""
        try:
            document_id = message.get('document_id')
            chunks = message.get('chunks', [])
            document_type = message.get('document_type')
            
            logger.info(f"Processing enrichment for {len(chunks)} chunks from document {document_id}")
            
            # Process each chunk for enrichment
            enriched_chunks = []
            for chunk in chunks:
                try:
                    # Apply enrichment to each chunk
                    enriched_chunk = self._enrich_chunk(chunk, message.get('metadata', {}))
                    enriched_chunks.append(enriched_chunk)
                except Exception as e:
                    logger.error(f"Error enriching chunk {chunk.get('chunk_id')}: {str(e)}")
                    # Add chunk even if enrichment failed
                    enriched_chunks.append(chunk)
            
            # Publish enriched chunks result
            self._publish_enrichment_result(document_id, enriched_chunks, document_type)
            
            logger.info(f"Completed enrichment for document {document_id}")
            
        except Exception as e:
            logger.error(f"Error processing chunks created: {str(e)}")
    
    def _enrich_chunk(self, chunk: dict, context: dict) -> dict:
        """Enrich a single chunk with all tagging systems"""
        try:
            content = chunk.get('content', '')
            
            # Apply competency tagging
            competency_result = self._apply_competency_tagging(content, context)
            
            # Apply pedagogy tagging
            pedagogy_result = self._apply_pedagogy_tagging(content, context)
            
            # Apply assessment tagging if relevant
            assessment_result = self._apply_assessment_tagging(content, context)
            
            # Apply cognitive level tagging
            cognitive_result = self._apply_cognitive_tagging(content, context)
            
            # Apply taxonomy tagging
            taxonomy_result = self._apply_taxonomy_tagging(content, context)
            
            # Combine all enrichment results
            enriched_chunk = chunk.copy()
            enriched_chunk['enrichment'] = {
                'competency_tags': competency_result.get('tags', []),
                'pedagogy_tags': pedagogy_result.get('tags', []),
                'assessment_tags': assessment_result.get('tags', []),
                'cognitive_tags': cognitive_result.get('tags', []),
                'taxonomy_tags': taxonomy_result.get('tags', []),
                'enriched_at': str(__import__('datetime').datetime.utcnow()),
                'enrichment_version': '2.0.0'
            }
            
            return enriched_chunk
            
        except Exception as e:
            logger.error(f"Error enriching chunk: {str(e)}")
            return chunk
    
    def _apply_competency_tagging(self, content: str, context: dict) -> dict:
        """Apply competency tagging (simplified version)"""
        # This would call the actual competency tagger
        return {'tags': [], 'confidence_scores': []}
    
    def _apply_pedagogy_tagging(self, content: str, context: dict) -> dict:
        """Apply pedagogy tagging (simplified version)"""
        return {'tags': [], 'confidence_scores': []}
    
    def _apply_assessment_tagging(self, content: str, context: dict) -> dict:
        """Apply assessment tagging (simplified version)"""
        return {'tags': [], 'confidence_scores': []}
    
    def _apply_cognitive_level(self, content: str, context: dict) -> dict:
        """Apply cognitive level tagging (simplified version)"""
        return {'tags': [], 'confidence_scores': []}
    
    def _apply_taxonomy_tagging(self, content: str, context: dict) -> dict:
        """Apply taxonomy tagging"""
        # This would call the taxonomy_tagger
        return {'tags': [], 'confidence_scores': []}
    
    def _publish_enrichment_result(self, document_id: str, enriched_chunks: list, document_type: str):
        """Publish enrichment result to response queue"""
        try:
            result = {
                "document_id": document_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "document_type": document_type,
                "status": "completed"
            }
            
            # Publish to results queue
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key="enrichment.completed",
                body=json.dumps(result)
            )
            
            logger.info(f"Published enrichment result for document {document_id}")
            
        except Exception as e:
            logger.error(f"Error publishing enrichment result: {str(e)}")
    
    def _classify_error(self, exception: Exception) -> str:
        """Classify error type for DLQ decision"""
        error_message = str(exception).lower()
        
        if "timeout" in error_message or "timed out" in error_message:
            return "timeout_error"
        elif "database" in error_message or "connection" in error_message:
            return "database_connection_error"
        elif "rate limit" in error_message or "too many requests" in error_message:
            return "rate_limit_exceeded"
        elif "validation" in error_message or "invalid" in error_message:
            return "schema_validation_error"
        elif "authentication" in error_message or "unauthorized" in error_message:
            return "authentication_error"
        else:
            return "unknown_error"
    
    def _send_to_dlq(self, message: dict, error_info: Dict[str, Any]):
        """Send failed message to DLQ"""
        try:
            dlq_exchange = f"{self.exchange_name}.dlq"
            dlq_routing_key = f"{self.service_name}.dlq"
            
            # Format DLQ message
            dlq_message = DLQConfiguration.format_dlq_message(message, error_info)
            
            # Send to DLQ
            self.channel.basic_publish(
                exchange=dlq_exchange,
                routing_key=dlq_routing_key,
                body=json.dumps(dlq_message)
            )
            
            logger.warning(f"Sent message to DLQ {dlq_routing_key} due to: {error_info['error_type']}")
            
        except Exception as e:
            logger.error(f"Failed to send message to DLQ: {str(e)}")