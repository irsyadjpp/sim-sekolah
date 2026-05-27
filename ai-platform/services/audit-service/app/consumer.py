"""
Audit Service RabbitMQ Consumer
Consumes audit events from RabbitMQ and logs them
"""
import os
import json
import logging
from typing import Optional
from datetime import datetime

from shared.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from shared.messaging.rabbitmq_messages import (
    BaseMessage,
    MessageType,
    MessagePriority
)

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class AuditServiceConsumer(AsyncRabbitMQConsumer):
    """Consumer for audit service events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="audit.queue",
            exchange_name="audit.exchange",
            routing_key="audit.log"
        )
        from .main import log_event, check_compliance, AuditLog, ComplianceCheck
        self.log_event = log_event
        self.check_compliance = check_compliance
        self.AuditLog = AuditLog
        self.ComplianceCheck = ComplianceCheck
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process audit message"""
        try:
            message_data = message.data
            
            # Extract audit information
            audit_log = self.AuditLog(
                user_id=message_data.get("user_id"),
                session_id=message_data.get("session_id"),
                request_id=message_data.get("request_id"),
                event_type=message_data.get("event_type", "unknown"),
                event_data=message_data.get("event_data", {}),
                latency_ms=message_data.get("latency_ms"),
                token_count=message_data.get("token_count"),
                model_version=message_data.get("model_version"),
                ip_address=message_data.get("ip_address"),
                user_agent=message_data.get("user_agent")
            )
            
            # Check compliance if needed
            if message_data.get("check_compliance", False):
                compliance_check = self.ComplianceCheck(
                    request_id=message_data.get("request_id", ""),
                    event_type=audit_log.event_type,
                    event_data=audit_log.event_data,
                    user_id=audit_log.user_id
                )
                compliance_result = await self.check_compliance(compliance_check)
                audit_log.compliance_status = compliance_result.compliance_status
            
            # Log the event
            log_id = await self.log_event(audit_log)
            
            logger.info(f"Processed audit message: {log_id}")
            
            return {
                "status": "logged",
                "log_id": log_id,
                "compliance_status": audit_log.compliance_status
            }
            
        except Exception as e:
            logger.error(f"Error processing audit message: {e}")
            raise


class AsyncAuditServiceConsumer(AuditServiceConsumer):
    """Async wrapper for audit service consumer"""
    pass
