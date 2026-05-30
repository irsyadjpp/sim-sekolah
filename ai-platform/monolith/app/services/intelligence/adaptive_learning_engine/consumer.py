"""
Adaptive Learning Engine RabbitMQ Consumer
Consumes adaptive learning requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from common.infrastructure.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from common.infrastructure.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class AdaptiveLearningEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for adaptive learning engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="adaptive.queue",
            exchange_name="adaptive.exchange",
            routing_key="adaptive.generate"
        )
        from .main import PersonalizedPathRequest, ContentSelectionRequest, adaptive_engine
        self.PersonalizedPathRequest = PersonalizedPathRequest
        self.ContentSelectionRequest = ContentSelectionRequest
        self.adaptive_engine = adaptive_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process adaptive learning message"""
        try:
            message_data = message.data
            request_type = message_data.get("request_type", "path")
            
            if request_type == "path":
                # Create personalized path request
                path_request = self.PersonalizedPathRequest(
                    request_id=message_data.get("request_id"),
                    user_id=message_data.get("user_id"),
                    target_competency=message_data.get("target_competency"),
                    current_mastery=message_data.get("current_mastery", {}),
                    learning_style=message_data.get("learning_style"),
                    preferences=message_data.get("preferences"),
                    context=message_data.get("context")
                )
                
                # Generate personalized path
                result = self.adaptive_engine.generate_personalized_path(path_request)
                
                logger.info(f"Processed adaptive path request: {path_request.request_id}")
                
                return {
                    "request_id": path_request.request_id,
                    "user_id": path_request.user_id,
                    "target_competency": path_request.target_competency,
                    "learning_path": result["learning_path"],
                    "estimated_duration": result["estimated_duration"],
                    "adaptation_notes": result["adaptation_notes"]
                }
            
            elif request_type == "content":
                # Create content selection request
                content_request = self.ContentSelectionRequest(
                    request_id=message_data.get("request_id"),
                    user_id=message_data.get("user_id"),
                    competency=message_data.get("competency"),
                    current_level=message_data.get("current_level"),
                    learning_style=message_data.get("learning_style"),
                    context=message_data.get("context")
                )
                
                # Select adaptive content
                result = self.adaptive_engine.select_content(content_request)
                
                logger.info(f"Processed adaptive content request: {content_request.request_id}")
                
                return {
                    "request_id": content_request.request_id,
                    "user_id": content_request.user_id,
                    "competency": content_request.competency,
                    "recommended_content": result["recommended_content"],
                    "adaptation_reason": result["adaptation_reason"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing adaptive learning message: {e}")
            raise


class AsyncAdaptiveLearningEngineConsumer(AdaptiveLearningEngineConsumer):
    """Async wrapper for adaptive learning engine consumer"""
    pass
