"""
Pedagogy Engine RabbitMQ Consumer
Consumes pedagogy analysis requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from shared.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from shared.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class PedagogyEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for pedagogy engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="pedagogy.queue",
            exchange_name="pedagogy.exchange",
            routing_key="pedagogy.analyze"
        )
        from .main import PedagogyAnalysisRequest, pedagogy_engine
        self.PedagogyAnalysisRequest = PedagogyAnalysisRequest
        self.pedagogy_engine = pedagogy_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process pedagogy message"""
        try:
            message_data = message.data
            
            # Create pedagogy analysis request
            pedagogy_request = self.PedagogyAnalysisRequest(
                request_id=message_data.get("request_id"),
                content=message_data.get("content", ""),
                content_type=message_data.get("content_type", "text"),
                context=message_data.get("context")
            )
            
            # Analyze pedagogy
            result = self.pedagogy_engine.detect_pedagogy(
                pedagogy_request.content,
                pedagogy_request.context
            )
            
            logger.info(f"Processed pedagogy request: {pedagogy_request.request_id} - type: {result['pedagogy_type']}")
            
            return {
                "request_id": pedagogy_request.request_id,
                "pedagogy_type": result["pedagogy_type"],
                "confidence": result["confidence"],
                "characteristics": result["characteristics"],
                "teaching_methods": result["teaching_methods"],
                "recommendations": result["recommendations"]
            }
            
        except Exception as e:
            logger.error(f"Error processing pedagogy message: {e}")
            raise


class AsyncPedagogyEngineConsumer(PedagogyEngineConsumer):
    """Async wrapper for pedagogy engine consumer"""
    pass
