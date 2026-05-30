"""
Recommendation Engine RabbitMQ Consumer
Consumes recommendation requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from common.infrastructure.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from common.infrastructure.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class RecommendationEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for recommendation engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="recommendation.queue",
            exchange_name="recommendation.exchange",
            routing_key="recommendation.generate"
        )
        from .main import RecommendationRequest, recommendation_engine
        self.RecommendationRequest = RecommendationRequest
        self.recommendation_engine = recommendation_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process recommendation message"""
        try:
            message_data = message.data
            
            # Create recommendation request
            recommendation_request = self.RecommendationRequest(
                request_id=message_data.get("request_id"),
                user_id=message_data.get("user_id"),
                context=message_data.get("context"),
                preferences=message_data.get("preferences"),
                strategy=message_data.get("strategy", "hybrid")
            )
            
            # Generate recommendations
            result = self.recommendation_engine.generate_recommendations(recommendation_request)
            
            logger.info(f"Processed recommendation request: {recommendation_request.request_id}")
            
            return {
                "request_id": recommendation_request.request_id,
                "user_id": recommendation_request.user_id,
                "recommendations": result["recommendations"],
                "strategy_used": result["strategy_used"],
                "confidence_scores": result["confidence_scores"]
            }
            
        except Exception as e:
            logger.error(f"Error processing recommendation message: {e}")
            raise


class AsyncRecommendationEngineConsumer(RecommendationEngineConsumer):
    """Async wrapper for recommendation engine consumer"""
    pass
