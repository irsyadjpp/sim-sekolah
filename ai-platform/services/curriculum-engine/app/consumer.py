"""
Curriculum Engine RabbitMQ Consumer
Consumes curriculum validation requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from shared.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from shared.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class CurriculumEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for curriculum engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="curriculum.queue",
            exchange_name="curriculum.exchange",
            routing_key="curriculum.validate"
        )
        from .main import CurriculumValidationRequest, AlignmentCheckRequest, curriculum_engine
        self.CurriculumValidationRequest = CurriculumValidationRequest
        self.AlignmentCheckRequest = AlignmentCheckRequest
        self.curriculum_engine = curriculum_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process curriculum message"""
        try:
            message_data = message.data
            request_type = message_data.get("request_type", "validate")
            
            if request_type == "validate":
                # Create validation request
                validation_request = self.CurriculumValidationRequest(
                    request_id=message_data.get("request_id"),
                    validation_type=message_data.get("validation_type"),
                    cp_structure=message_data.get("cp_structure"),
                    atp_structure=message_data.get("atp_structure")
                )
                
                # Validate
                if validation_request.validation_type == "cp" and validation_request.cp_structure:
                    result = self.curriculum_engine.validate_cp(validation_request.cp_structure)
                    return {
                        "request_id": validation_request.request_id,
                        "is_valid": result["is_valid"],
                        "validation_type": "cp",
                        "errors": result["errors"],
                        "warnings": result["warnings"]
                    }
                elif validation_request.validation_type == "atp" and validation_request.atp_structure:
                    result = self.curriculum_engine.validate_atp(validation_request.atp_structure)
                    return {
                        "request_id": validation_request.request_id,
                        "is_valid": result["is_valid"],
                        "validation_type": "atp",
                        "errors": result["errors"],
                        "warnings": result["warnings"]
                    }
            
            elif request_type == "alignment":
                # Create alignment check request
                alignment_request = self.AlignmentCheckRequest(
                    request_id=message_data.get("request_id"),
                    cp_id=message_data.get("cp_id"),
                    atp_id=message_data.get("atp_id"),
                    cp_structure=message_data.get("cp_structure"),
                    atp_structure=message_data.get("atp_structure")
                )
                
                # Check alignment
                result = self.curriculum_engine.check_alignment(
                    alignment_request.cp_structure,
                    alignment_request.atp_structure
                )
                
                return {
                    "request_id": alignment_request.request_id,
                    "cp_id": alignment_request.cp_id,
                    "atp_id": alignment_request.atp_id,
                    "is_aligned": result["is_aligned"],
                    "alignment_score": result["alignment_score"],
                    "missing_competencies": result["missing_competencies"],
                    "extra_topics": result["extra_topics"],
                    "recommendations": result["recommendations"]
                }
            
            logger.info(f"Processed curriculum message: {message_data.get('request_id')}")
            return None
            
        except Exception as e:
            logger.error(f"Error processing curriculum message: {e}")
            raise


class AsyncCurriculumEngineConsumer(CurriculumEngineConsumer):
    """Async wrapper for curriculum engine consumer"""
    pass
