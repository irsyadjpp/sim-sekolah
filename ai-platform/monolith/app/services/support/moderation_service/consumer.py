"""
Moderation Service RabbitMQ Consumer
Consumes moderation requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from common.infrastructure.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from common.infrastructure.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class ModerationServiceConsumer(AsyncRabbitMQConsumer):
    """Consumer for moderation service events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="moderation.queue",
            exchange_name="moderation.exchange",
            routing_key="moderation.check"
        )
        from .main import ModerationRequest, moderation_engine
        self.ModerationRequest = ModerationRequest
        self.moderation_engine = moderation_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process moderation message"""
        try:
            message_data = message.data
            
            # Create moderation request
            moderation_request = self.ModerationRequest(
                request_id=message_data.get("request_id"),
                content=message_data.get("content", ""),
                content_type=message_data.get("content_type", "text"),
                user_id=message_data.get("user_id"),
                context=message_data.get("context")
            )
            
            # Moderate content
            result = self.moderation_engine.moderate(moderation_request)
            
            logger.info(f"Processed moderation request: {result.request_id} - safe: {result.is_safe}")
            
            return result.dict()
            
        except Exception as e:
            logger.error(f"Error processing moderation message: {e}")
            raise


class AsyncModerationServiceConsumer(ModerationServiceConsumer):
    """Async wrapper for moderation service consumer"""
    pass
