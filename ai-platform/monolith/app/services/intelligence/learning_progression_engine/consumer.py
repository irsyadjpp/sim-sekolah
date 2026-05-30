"""
Learning Progression Engine RabbitMQ Consumer
Consumes progression tracking requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from common.infrastructure.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from common.infrastructure.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class LearningProgressionEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for learning progression engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="progression.queue",
            exchange_name="progression.exchange",
            routing_key="progression.track"
        )
        from .main import MasteryTrackingRequest, GapDetectionRequest, progression_engine
        self.MasteryTrackingRequest = MasteryTrackingRequest
        self.GapDetectionRequest = GapDetectionRequest
        self.progression_engine = progression_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process progression message"""
        try:
            message_data = message.data
            request_type = message_data.get("request_type", "mastery")
            
            if request_type == "mastery":
                # Create mastery tracking request
                mastery_request = self.MasteryTrackingRequest(
                    request_id=message_data.get("request_id"),
                    user_id=message_data.get("user_id"),
                    competency=message_data.get("competency"),
                    performance_data=message_data.get("performance_data", []),
                    context=message_data.get("context")
                )
                
                # Track mastery
                result = self.progression_engine.track_mastery(mastery_request)
                
                logger.info(f"Processed mastery request: {mastery_request.request_id} - level: {result['mastery_level']}")
                
                return {
                    "request_id": mastery_request.request_id,
                    "user_id": mastery_request.user_id,
                    "competency": mastery_request.competency,
                    "mastery_level": result["mastery_level"],
                    "mastery_score": result["mastery_score"],
                    "progression_trend": result["progression_trend"],
                    "recommendations": result["recommendations"]
                }
            
            elif request_type == "gap":
                # Create gap detection request
                gap_request = self.GapDetectionRequest(
                    request_id=message_data.get("request_id"),
                    user_id=message_data.get("user_id"),
                    target_competency=message_data.get("target_competency"),
                    current_mastery=message_data.get("current_mastery", {}),
                    prerequisite_map=message_data.get("prerequisite_map", {}),
                    context=message_data.get("context")
                )
                
                # Detect gaps
                result = self.progression_engine.detect_gaps(gap_request)
                
                logger.info(f"Processed gap request: {gap_request.request_id} - has_gaps: {result['has_gaps']}")
                
                return {
                    "request_id": gap_request.request_id,
                    "user_id": gap_request.user_id,
                    "target_competency": gap_request.target_competency,
                    "has_gaps": result["has_gaps"],
                    "missing_prerequisites": result["missing_prerequisites"],
                    "weak_prerequisites": result["weak_prerequisites"],
                    "recommended_path": result["recommended_path"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing progression message: {e}")
            raise


class AsyncLearningProgressionEngineConsumer(LearningProgressionEngineConsumer):
    """Async wrapper for learning progression engine consumer"""
    pass
