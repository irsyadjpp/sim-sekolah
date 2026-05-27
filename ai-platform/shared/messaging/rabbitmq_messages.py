"""
RabbitMQ Message Definitions for AI Platform Async Processing
This file defines the message schemas for RabbitMQ communication between Backend (Go) and AI Platform Services
"""
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from enum import Enum
import json
import uuid
from datetime import datetime


class MessageType(str, Enum):
    """Message types for RabbitMQ"""
    # Parser Service
    PARSE_DOCUMENT = "parse_document"
    PARSE_TEXT = "parse_text"
    EXTRACT_TABLES = "extract_tables"
    PROCESS_OCR = "process_ocr"
    
    # Chunk Service
    CHUNK_COMPETENCY = "chunk_competency"
    CHUNK_ACTIVITY = "chunk_activity"
    CHUNK_ASSESSMENT = "chunk_assessment"
    
    # Metadata Service
    ENRICH_DIFFICULTY = "enrich_difficulty"
    ENRICH_TAXONOMY = "enrich_taxonomy"
    ENRICH_COMPETENCY = "enrich_competency"
    
    # Embedding Service
    EMBED_TEXT = "embed_text"
    EMBED_TEXT_BATCH = "embed_text_batch"
    EMBED_IMAGE = "embed_image"
    
    # Retrieval Service
    SEMANTIC_SEARCH = "semantic_search"
    HYBRID_SEARCH = "hybrid_search"
    
    # Generation Service
    GENERATE_TEXT = "generate_text"
    GENERATE_WITH_CITATIONS = "generate_with_citations"


class MessagePriority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BaseMessage:
    """Base message structure"""
    message_id: str
    message_type: str
    timestamp: str
    priority: str
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert message to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseMessage':
        """Create message from dictionary"""
        return cls(**data)


# Parser Service Messages
@dataclass
class ParseDocumentMessage(BaseMessage):
    """Message for document parsing"""
    document_id: str
    document_data: str  # base64 encoded or file path
    document_type: str
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.PARSE_DOCUMENT.value


@dataclass
class ProcessOCRMessage(BaseMessage):
    """Message for OCR processing"""
    image_id: str
    image_data: str  # base64 encoded or file path
    language: str = "ind"
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.PROCESS_OCR.value


# Chunk Service Messages
@dataclass
class ChunkCompetencyMessage(BaseMessage):
    """Message for competency-based chunking"""
    content_id: str
    content: str
    competency_type: str  # CP code (e.g., CP-IPA-B-01)
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.CHUNK_COMPETENCY.value


# Embedding Service Messages
@dataclass
class EmbedTextMessage(BaseMessage):
    """Message for text embedding"""
    text_id: str
    text_content: str
    model: str = "BAAI/bge-m3"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.EMBED_TEXT.value
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmbedTextBatchMessage(BaseMessage):
    """Message for batch text embedding"""
    text_ids: List[str]
    text_contents: List[str]
    model: str = "BAAI/bge-m3"
    batch_size: int = 32
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.EMBED_TEXT_BATCH.value
        if self.metadata is None:
            self.metadata = {}


# Retrieval Service Messages
@dataclass
class SemanticSearchMessage(BaseMessage):
    """Message for semantic search"""
    query: str
    collection_name: str = "documents"
    limit: int = 10
    filters: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.SEMANTIC_SEARCH.value
        if self.filters is None:
            self.filters = {}


# Generation Service Messages
@dataclass
class GenerateTextMessage(BaseMessage):
    """Message for text generation"""
    prompt: str
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.GENERATE_TEXT.value
        if self.metadata is None:
            self.metadata = {}


@dataclass
class GenerateWithCitationsMessage(BaseMessage):
    """Message for text generation with citations"""
    prompt: str
    context: str
    documents: List[Dict[str, Any]]
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.GENERATE_WITH_CITATIONS.value


# Response Messages
@dataclass
class SuccessResponse(BaseMessage):
    """Success response message"""
    success: bool = True
    result: Dict[str, Any] = None
    processing_time_ms: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        if self.result is None:
            self.result = {}


@dataclass
class ErrorResponse(BaseMessage):
    """Error response message"""
    success: bool = False
    error_code: str = ""
    error_message: str = ""
    error_details: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.error_details is None:
            self.error_details = {}


# Queue Definitions
QUEUES = {
    # Parser Service Queues
    "parser.queue": {
        "routing_key": "parser.*",
        "durable": True,
        "arguments": {
            "x-max-length": 10000,
            "x-message-ttl": 3600000  # 1 hour
        }
    },
    
    # Chunk Service Queues
    "chunk.queue": {
        "routing_key": "chunk.*",
        "durable": True,
        "arguments": {
            "x-max-length": 5000,
            "x-message-ttl": 7200000  # 2 hours
        }
    },
    
    # Embedding Service Queues
    "embedding.queue": {
        "routing_key": "embedding.*",
        "durable": True,
        "arguments": {
            "x-max-length": 10000,
            "x-message-ttl": 3600000  # 1 hour
        }
    },
    
    # Retrieval Service Queues
    "retrieval.queue": {
        "routing_key": "retrieval.*",
        "durable": True,
        "arguments": {
            "x-max-length": 5000,
            "x-message-ttl": 600000  # 10 minutes
        }
    },
    
    # Generation Service Queues
    "generation.queue": {
        "routing_key": "generation.*",
        "durable": True,
        "arguments": {
            "x-max-length": 2000,
            "x-message-ttl": 3600000  # 1 hour
        }
    },
    
    # Result Queues (for async responses)
    "parser.result.queue": {
        "routing_key": "parser.result.*",
        "durable": True,
        "arguments": {
            "x-max-length": 10000,
            "x-message-ttl": 86400000  # 24 hours
        }
    },
    
    "chunk.result.queue": {
        "routing_key": "chunk.result.*",
        "durable": True,
        "arguments": {
            "x-max-length": 5000,
            "x-message-ttl": 86400000  # 24 hours
        }
    },
    
    "embedding.result.queue": {
        "routing_key": "embedding.result.*",
        "durable": True,
        "arguments": {
            "x-max-length": 10000,
            "x-message-ttl": 86400000  # 24 hours
        }
    },
    
    "generation.result.queue": {
        "routing_key": "generation.result.*",
        "durable": True,
        "arguments": {
            "x-max-length": 2000,
            "x-message-ttl": 86400000  # 24 hours
        }
    }
}


# Exchange Definitions
EXCHANGES = {
    "ai.platform.exchange": {
        "type": "topic",
        "durable": True
    },
    "ai.platform.direct": {
        "type": "direct",
        "durable": True
    }
}


# Exchange-Queue Bindings
BINDINGS = [
    {
        "exchange": "ai.platform.exchange",
        "queue": "parser.queue",
        "routing_key": "parser.*"
    },
    {
        "exchange": "ai.platform.exchange",
        "queue": "chunk.queue",
        "routing_key": "chunk.*"
    },
    {
        "exchange": "ai.platform.exchange",
        "queue": "embedding.queue",
        "routing_key": "embedding.*"
    },
    {
        "exchange": "ai.platform.exchange",
        "queue": "retrieval.queue",
        "routing_key": "retrieval.*"
    },
    {
        "exchange": "ai.platform.exchange",
        "queue": "generation.queue",
        "routing_key": "generation.*"
    },
    {
        "exchange": "ai.platform.direct",
        "queue": "parser.result.queue",
        "routing_key": "parser.result"
    },
    {
        "exchange": "ai.platform.direct",
        "queue": "chunk.result.queue",
        "routing_key": "chunk.result"
    },
    {
        "exchange": "ai.platform.direct",
        "queue": "embedding.result.queue",
        "routing_key": "embedding.result"
    },
    {
        "exchange": "ai.platform.direct",
        "queue": "generation.result.queue",
        "routing_key": "generation.result"
    }
]