"""
RabbitMQ Consumer for Retrieval Enhancement Service
"""
import os
import json
import logging
import pika
from datetime import datetime

logger = logging.getLogger(__name__)

class AsyncRetrievalEnhancementConsumer:
    """Async consumer for retrieval enhancement messages"""
    
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.queue_name = "retrieval_enhancement_queue"
        self.exchange_name = "retrieval_enhancement_exchange"
        self.routing_key = "retrieval.enhancement.*"
        self.connection = None
        self.channel = None
    
    async def start(self):
        """Start consuming messages"""
        try:
            # Connect to RabbitMQ
            self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )
            
            # Declare queue
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            
            # Bind queue to exchange
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.queue_name,
                routing_key=self.routing_key
            )
            
            # Set QoS
            self.channel.basic_qos(prefetch_count=1)
            
            # Start consuming
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.process_message,
                auto_ack=False
            )
            
            logger.info(f"Retrieval Enhancement Consumer started. Listening on {self.queue_name}")
            self.channel.start_consuming()
            
        except Exception as e:
            logger.error(f"Error starting consumer: {e}")
            if self.connection:
                self.connection.close()
    
    def process_message(self, ch, method, properties, body):
        """Process incoming message"""
        try:
            # Parse message
            message = json.loads(body)
            
            # Process based on routing key
            routing_key = method.routing_key
            logger.info(f"Processing message with routing key: {routing_key}")
            
            # Handle different retrieval types
            if "curriculum" in routing_key:
                self._handle_curriculum_request(message)
            elif "pedagogy" in routing_key:
                self._handle_pedagogy_request(message)
            elif "competency" in routing_key:
                self._handle_competency_request(message)
            elif "assessment" in routing_key:
                self._handle_assessment_request(message)
            elif "contextual" in routing_key:
                self._handle_contextual_request(message)
            elif "learning_style" in routing_key:
                self._handle_learning_style_request(message)
            else:
                logger.warning(f"Unknown routing key: {routing_key}")
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def _handle_curriculum_request(self, message: dict):
        """Handle curriculum-aware retrieval request"""
        logger.info(f"Processing curriculum request: {message.get('request_id')}")
        # Implementation would call the retrieval enhancement engine
    
    def _handle_pedagogy_request(self, message: dict):
        """Handle pedagogy-aware retrieval request"""
        logger.info(f"Processing pedagogy request: {message.get('request_id')}")
    
    def _handle_competency_request(self, message: dict):
        """Handle competency-aware retrieval request"""
        logger.info(f"Processing competency request: {message.get('request_id')}")
    
    def _handle_assessment_request(self, message: dict):
        """Handle assessment-aware retrieval request"""
        logger.info(f"Processing assessment request: {message.get('request_id')}")
    
    def _handle_contextual_request(self, message: dict):
        """Handle contextual retrieval request"""
        logger.info(f"Processing contextual request: {message.get('request_id')}")
    
    def _handle_learning_style_request(self, message: dict):
        """Handle learning style retrieval request"""
        logger.info(f"Processing learning style request: {message.get('request_id')}")