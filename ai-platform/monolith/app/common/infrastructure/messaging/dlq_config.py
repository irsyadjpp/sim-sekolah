"""
DLQ Configuration for AI Platform Services
Dead Letter Queue configuration for handling failed messages across all services
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class DLQConfiguration:
    """Dead Letter Queue configuration for all AI platform services"""
    
    # DLQ configuration for each service
    DLQ_CONFIGS = {
        "parser_service": {
            "queue": "parser.queue",
            "dlq": "parser.dlq",
            "exchange": "ai.platform.exchange",
            "retry_policy": {
                "max_retries": 3,
                "delay_ms": 5000,  # 5 seconds
                "exponential_backoff": True,
                "backoff_multiplier": 2.0
            }
        },
        "chunk_service": {
            "queue": "chunk.queue",
            "dlq": "chunk.dlq", 
            "exchange": "ai.platform.exchange",
            "retry_policy": {
                "max_retries": 3,
                "delay_ms": 10000,  # 10 seconds
                "exponential_backoff": True,
                "backoff_multiplier": 2.0
            }
        },
        "enrichment_service": {
            "queue": "enrichment.queue",
            "dlq": "enrichment.dlq",
            "exchange": "ai.platform.exchange",
            "retry_policy": {
                "max_retries": 5,  # More retries for enrichment (can be slow)
                "delay_ms": 30000,  # 30 seconds
                "exponential_backoff": True,
                "backoff_multiplier": 2.0
            }
        },
        "pipeline_tracker_service": {
            "queue": "pipeline_tracker.queue",
            "dlq": "pipeline_tracker.dlq",
            "exchange": "ai.platform.exchange",
            "retry_policy": {
                "max_retries": 2,
                "delay_ms": 3000,  # 3 seconds
                "exponential_backoff": False
            }
        }
    }
    
    # Error types that should be sent to DLQ immediately (no retry)
    FATAL_ERRORS = [
        "schema_validation_error",
        "invalid_message_format",
        "authentication_error",
        "authorization_error",
        "poison_pill_message"
    ]
    
    # Error types that should trigger retry before DLQ
    RETRIABLE_ERRORS = [
        "timeout_error",
        "database_connection_error",
        "external_service_unavailable",
        "rate_limit_exceeded",
        "temporary_resource_exhaustion"
    ]
    
    @classmethod
    def get_config(cls, service_name: str) -> Optional[Dict[str, Any]]:
        """Get DLQ configuration for a specific service"""
        return cls.DLQ_CONFIGS.get(service_name)
    
    @classmethod
    def should_send_to_dlq(cls, error_type: str, retry_count: int, max_retries: int) -> bool:
        """
        Determine if message should be sent to DLQ
        
        Args:
            error_type: Type of error that occurred
            retry_count: Current retry count
            max_retries: Maximum allowed retries
            
        Returns:
            True if should go to DLQ, False if should retry
        """
        # Fatal errors go directly to DLQ
        if error_type in cls.FATAL_ERRORS:
            logger.warning(f"Fatal error {error_type}, sending to DLQ immediately")
            return True
        
        # Retryable errors check retry count
        if error_type in cls.RETRIABLE_ERRORS:
            if retry_count >= max_retries:
                logger.warning(f"Retries exhausted for {error_type}, sending to DLQ")
                return True
            return False
        
        # Unknown error - send to DLQ after max retries
        if retry_count >= max_retries:
            logger.warning(f"Retries exhausted for unknown error {error_type}, sending to DLQ")
            return True
        
        return False