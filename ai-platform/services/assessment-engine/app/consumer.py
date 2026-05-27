"""
Assessment Engine RabbitMQ Consumer
Consumes assessment generation requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from shared.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from shared.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class AssessmentEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for assessment engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="assessment.queue",
            exchange_name="assessment.exchange",
            routing_key="assessment.generate"
        )
        from .main import AssessmentGenerationRequest, HOTSQuestionRequest, RubricGenerationRequest, assessment_engine
        self.AssessmentGenerationRequest = AssessmentGenerationRequest
        self.HOTSQuestionRequest = HOTSQuestionRequest
        self.RubricGenerationRequest = RubricGenerationRequest
        self.assessment_engine = assessment_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process assessment message"""
        try:
            message_data = message.data
            request_type = message_data.get("request_type", "generate")
            
            if request_type == "generate":
                # Create assessment generation request
                assessment_request = self.AssessmentGenerationRequest(
                    request_id=message_data.get("request_id"),
                    topic=message_data.get("topic", ""),
                    competency=message_data.get("competency", ""),
                    grade=message_data.get("grade", ""),
                    assessment_type=message_data.get("assessment_type", "formative"),
                    question_count=message_data.get("question_count", 5),
                    difficulty=message_data.get("difficulty", "medium"),
                    context=message_data.get("context")
                )
                
                # Generate assessment
                result = self.assessment_engine.generate_assessment(assessment_request)
                
                logger.info(f"Processed assessment request: {assessment_request.request_id}")
                
                return {
                    "request_id": assessment_request.request_id,
                    "questions": result["questions"],
                    "rubric": result["rubric"],
                    "metadata": result["metadata"]
                }
            
            elif request_type == "hots":
                # Create HOTS question request
                hots_request = self.HOTSQuestionRequest(
                    request_id=message_data.get("request_id"),
                    topic=message_data.get("topic", ""),
                    competency=message_data.get("competency", ""),
                    cognitive_level=message_data.get("cognitive_level", "analyze"),
                    question_count=message_data.get("question_count", 3),
                    context=message_data.get("context")
                )
                
                # Generate HOTS questions
                result = self.assessment_engine.generate_hots_questions(hots_request)
                
                logger.info(f"Processed HOTS request: {hots_request.request_id}")
                
                return result
            
            elif request_type == "rubric":
                # Create rubric generation request
                rubric_request = self.RubricGenerationRequest(
                    request_id=message_data.get("request_id"),
                    assessment_type=message_data.get("assessment_type", "formative"),
                    criteria=message_data.get("criteria", []),
                    performance_levels=message_data.get("performance_levels", 4),
                    context=message_data.get("context")
                )
                
                # Generate rubric
                result = self.assessment_engine.generate_rubric(rubric_request)
                
                logger.info(f"Processed rubric request: {rubric_request.request_id}")
                
                return result
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing assessment message: {e}")
            raise


class AsyncAssessmentEngineConsumer(AssessmentEngineConsumer):
    """Async wrapper for assessment engine consumer"""
    pass
