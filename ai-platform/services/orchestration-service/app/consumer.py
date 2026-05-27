"""
Orchestration Service RabbitMQ Consumer
Consumes orchestration requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from shared.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from shared.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class OrchestrationServiceConsumer(AsyncRabbitMQConsumer):
    """Consumer for orchestration service events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="orchestration.queue",
            exchange_name="orchestration.exchange",
            routing_key="orchestration.execute"
        )
        from .main import WorkflowRequest, workflow_engine
        self.WorkflowRequest = WorkflowRequest
        self.workflow_engine = workflow_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process orchestration message"""
        try:
            message_data = message.data
            
            # Create workflow request
            workflow_request = self.WorkflowRequest(
                request_id=message_data.get("request_id"),
                user_id=message_data.get("user_id"),
                session_id=message_data.get("session_id"),
                query=message_data.get("query", ""),
                context=message_data.get("context"),
                preferences=message_data.get("preferences")
            )
            
            # Execute workflow
            result = self.workflow_engine.execute_workflow(workflow_request)
            
            logger.info(f"Processed orchestration request: {result.request_id} - intent: {result.intent}")
            
            return result.dict()
            
        except Exception as e:
            logger.error(f"Error processing orchestration message: {e}")
            raise


class AsyncOrchestrationServiceConsumer(OrchestrationServiceConsumer):
    """Async wrapper for orchestration service consumer"""
    pass
