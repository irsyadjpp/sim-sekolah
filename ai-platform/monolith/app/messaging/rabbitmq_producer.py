"""
RabbitMQ Producer for Parser Service
Sends parsed documents to Semantic Chunk Service
"""
import logging
import json
from typing import Dict, Any, Optional
import pika
import hashlib
from datetime import datetime
from pika.exceptions import AMQPConnectionError

from common.config.settings import settings

logger = logging.getLogger(__name__)


class ParserServiceProducer:
    """RabbitMQ producer for parser service with idempotency support"""
    
    def __init__(self, rabbitmq_url: Optional[str] = None):
        """
        Initialize RabbitMQ producer with idempotency support
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        self.rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        self.connection = None
        self.channel = None
        self.exchange_name = "ai.platform.exchange"
        self.routing_key = "parser.document.parsed"
        
        # Initialize connection
        self.connect()
    
    def connect(self):
        """Establish RabbitMQ connection"""
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )
            
            logger.info("RabbitMQ producer connected successfully")
            
        except AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None
    
    def _generate_idempotency_key(self, document_id: str, stage: str) -> str:
        """
        Generate idempotency key for a message
        
        Args:
            document_id: Document identifier
            stage: Processing stage
            
        Returns:
            Idempotency key
        """
        # Create unique key based on document_id, stage, and timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        key_string = f"{document_id}_{stage}_{timestamp}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def send_parsed_document(self, document_data: Dict[str, Any]) -> bool:
        """
        Send parsed document to semantic chunk service with idempotency key
        
        Args:
            document_data: Parsed document data from parser service
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.channel:
            logger.warning("RabbitMQ channel not available, attempting to reconnect")
            self.connect()
            if not self.channel:
                return False
        
        try:
            # Generate idempotency key
            idempotency_key = self._generate_idempotency_key(
                document_data.get("document_id", ""),
                "chunking"
            )
            
            # Prepare message with idempotency key
            message = {
                "message_type": "document_parsed",
                "document_id": document_data.get("document_id"),
                "document_type": document_data.get("document_type"),
                "text_content": document_data.get("full_text", ""),
                "metadata": document_data.get("metadata", {}),
                "pages": document_data.get("pages", []),
                "timestamp": document_data.get("timestamp"),
                "idempotency_key": idempotency_key,  # Add idempotency key
                "stage": "chunking"
            }
            
            # Publish message
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=self.routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json',
                    message_id=idempotency_key  # Set message_id for deduplication
                )
            )
            
            logger.info(f"Sent parsed document {document_data.get('document_id')} to semantic chunk service with idempotency key {idempotency_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to RabbitMQ: {e}")
            # Try to reconnect
            self.connect()
            return False
    
    def send_error_notification(self, document_id: str, error_message: str) -> bool:
        """
        Send error notification for failed parsing
        
        Args:
            document_id: Document identifier
            error_message: Error message
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.channel:
            logger.warning("RabbitMQ channel not available for error notification")
            return False
        
        try:
            message = {
                "message_type": "parsing_error",
                "document_id": document_id,
                "error_message": error_message,
                "service": "parser-service",
                "timestamp": str(__import__('datetime').datetime.utcnow())
            }
            
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key="parser.error",
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            
            logger.info(f"Sent error notification for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending error notification: {e}")
            return False
    
    def close(self):
        """Close RabbitMQ connection"""
        if self.connection:
            self.connection.close()
            logger.info("RabbitMQ connection closed")