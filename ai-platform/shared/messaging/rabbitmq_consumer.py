"""
Base RabbitMQ Consumer for AI Platform Services
This provides a reusable base class for consuming messages from RabbitMQ
"""
import pika
import json
import logging
from typing import Callable, Dict, Any
from abc import ABC, abstractmethod
import threading
import time

logger = logging.getLogger(__name__)


class BaseRabbitMQConsumer(ABC):
    """Base class for RabbitMQ consumers"""
    
    def __init__(
        self,
        rabbitmq_url: str,
        queue_name: str,
        exchange_name: str = "ai.platform.exchange",
        routing_key: str = None,
        prefetch_count: int = 10
    ):
        """
        Initialize base consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL
            queue_name: Queue name to consume from
            exchange_name: Exchange name
            routing_key: Routing key (default: queue_name.*)
            prefetch_count: Prefetch count for QoS
        """
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key or f"{queue_name}.*"
        self.prefetch_count = prefetch_count
        self.connection = None
        self.channel = None
        self.is_consuming = False
        
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url)
            )
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=self.prefetch_count)
            logger.info(f"Connected to RabbitMQ for queue: {self.queue_name}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def setup_queue(self):
        """Declare exchange and queue"""
        try:
            # Declare exchange
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )
            
            # Declare queue
            self.channel.queue_declare(
                queue=self.queue_name,
                durable=True,
                arguments={
                    'x-max-length': 10000,
                    'x-message-ttl': 3600000  # 1 hour
                }
            )
            
            # Bind queue to exchange
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.queue_name,
                routing_key=self.routing_key
            )
            
            logger.info(f"Queue {self.queue_name} set up successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup queue: {e}")
            raise
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the message (must be implemented by subclass)
        
        Args:
            message: Message dictionary
        
        Returns:
            Response dictionary with result or error
        """
        pass
    
    def callback(self, ch, method, properties, body):
        """Callback function for message consumption"""
        try:
            # Parse message
            message = json.loads(body)
            logger.info(f"Received message: {message.get('message_type', 'unknown')}")
            
            # Process message
            result = self.process_message(message)
            
            # Send response if reply_to is specified
            if properties.reply_to:
                response = {
                    "success": True,
                    "correlation_id": properties.correlation_id,
                    "result": result
                }
                ch.basic_publish(
                    exchange='',
                    routing_key=properties.reply_to,
                    properties=pika.BasicProperties(
                        correlation_id=properties.correlation_id
                    ),
                    body=json.dumps(response)
                )
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Message processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Negative acknowledgment (requeue)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_consuming(self):
        """Start consuming messages"""
        try:
            self.connect()
            self.setup_queue()
            
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.callback
            )
            
            self.is_consuming = True
            logger.info(f"Starting to consume from {self.queue_name}")
            
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Stopping consumer")
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Error in consumer: {e}")
            self.stop_consuming()
    
    def stop_consuming(self):
        """Stop consuming messages"""
        if self.channel and self.is_consuming:
            self.channel.stop_consuming()
            self.is_consuming = False
            logger.info("Stopped consuming")
        
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")


class AsyncRabbitMQConsumer(BaseRabbitMQConsumer):
    """Async RabbitMQ consumer with threading support"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_thread = None
    
    def start_consuming_async(self):
        """Start consuming in a separate thread"""
        self.consumer_thread = threading.Thread(
            target=self.start_consuming,
            daemon=True
        )
        self.consumer_thread.start()
        logger.info(f"Started async consumer for {self.queue_name}")
    
    def stop_consuming_async(self):
        """Stop async consumer"""
        if self.consumer_thread and self.consumer_thread.is_alive():
            self.stop_consuming()
            self.consumer_thread.join(timeout=5)
            logger.info("Async consumer stopped")
    
    def is_alive(self) -> bool:
        """Check if consumer thread is alive"""
        return self.consumer_thread and self.consumer_thread.is_alive()


# Message Producer for publishing results
class RabbitMQProducer:
    """RabbitMQ message producer"""
    
    def __init__(self, rabbitmq_url: str):
        """
        Initialize producer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL
        """
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url)
            )
            self.channel = self.connection.channel()
            logger.info("Producer connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect producer: {e}")
            raise
    
    def publish_message(
        self,
        exchange_name: str,
        routing_key: str,
        message: Dict[str, Any],
        reply_to: str = None,
        correlation_id: str = None
    ):
        """
        Publish message to RabbitMQ
        
        Args:
            exchange_name: Exchange name
            routing_key: Routing key
            message: Message dictionary
            reply_to: Queue name for reply
            correlation_id: Correlation ID for request-response pattern
        """
        try:
            if not self.connection:
                self.connect()
            
            properties = pika.BasicProperties(
                reply_to=reply_to,
                correlation_id=correlation_id,
                delivery_mode=2  # Persistent message
            )
            
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                properties=properties,
                body=json.dumps(message)
            )
            
            logger.info(f"Published message to {routing_key}")
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            logger.info("Producer connection closed")