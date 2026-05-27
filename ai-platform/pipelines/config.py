"""
Prefect configuration and setup for AI Platform pipelines
"""

import os
from prefect import flow, task
from prefect.blocks.system import JSON
from prefect.blocks.core import Block
from prefect.context import get_run_context
from prefect.logging import get_logger
import logging

logger = get_logger(__name__)


class PipelineConfig:
    """Configuration for AI Platform pipelines."""
    
    # Service URLs
    DATABASE_URL = os.getenv("POSTGRES_URL", "postgresql://ai_user:ai_password@localhost:5432/ai_platform")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin@localhost:5672")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    
    # Service addresses
    PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://localhost:8001")
    CHUNK_SERVICE_URL = os.getenv("CHUNK_SERVICE_URL", "http://localhost:8003")
    EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:8005")
    RETRIEVAL_SERVICE_URL = os.getenv("RETRIEVAL_SERVICE_URL", "http://localhost:8006")
    GENERATION_SERVICE_URL = os.getenv("GENERATION_SERVICE_URL", "http://localhost:8007")
    
    # Pipeline settings
    BATCH_SIZE = int(os.getenv("PIPELINE_BATCH_SIZE", "10"))
    MAX_WORKERS = int(os.getenv("PIPELINE_MAX_WORKERS", "4"))
    TIMEOUT_SECONDS = int(os.getenv("PIPELINE_TIMEOUT_SECONDS", "300"))
    
    # Retry settings
    MAX_RETRIES = int(os.getenv("PIPELINE_MAX_RETRIES", "3"))
    RETRY_DELAY_SECONDS = int(os.getenv("PIPELINE_RETRY_DELAY_SECONDS", "5"))
    
    # Storage settings
    CHUNK_SIZE = int(os.getenv("PIPELINE_CHUNK_SIZE", "512"))
    CHUNK_OVERLAP = int(os.getenv("PIPELINE_CHUNK_OVERLAP", "50"))
    
    # Embedding settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")
    EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
    
    @classmethod
    def from_env(cls) -> "PipelineConfig":
        """Create configuration from environment variables."""
        return cls()


def setup_logging():
    """Setup logging for pipelines."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def get_flow_run_id() -> str:
    """Get the current flow run ID from Prefect context."""
    try:
        context = get_run_context()
        return str(context.flow_run.id)
    except:
        return "unknown"


def get_flow_name() -> str:
    """Get the current flow name from Prefect context."""
    try:
        context = get_run_context()
        return context.flow.name
    except:
        return "unknown"