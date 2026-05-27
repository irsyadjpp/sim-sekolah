"""
RabbitMQ Consumer for Semantic Enrichment Service
"""
import os
import json
import logging
import pika

logger = logging.getLogger(__name__)

class AsyncSemanticEnrichmentConsumer:
    """Async consumer for semantic enrichment messages"""
    
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.queue_name = "semantic_enrichment_queue"
        self.exchange_name = "semantic_enrichment_exchange"
        self.routing_key = "semantic.enrichment.*"
        self.connection = None
        self.channel = None
    
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
        """Process incoming message"""
        try:
            message = json.loads(body)
            routing_key = method.routing_key
            logger.info(f"Processing message with routing key: {routing_key}")
            
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
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
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