"""
Service client helpers for integration tests
"""

import asyncio
import logging
from typing import Optional, Dict, Any
import grpc
import httpx

logger = logging.getLogger(__name__)


class BaseServiceClient:
    """Base class for service clients."""
    
    def __init__(self, host: str, port: int, timeout: int = 30):
        """
        Initialize service client.
        
        Args:
            host: Service host
            port: Service port
            timeout: Request timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self._channel = None
    
    async def connect(self):
        """Establish connection to service."""
        raise NotImplementedError
    
    async def disconnect(self):
        """Close connection to service."""
        raise NotImplementedError
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


class GrpcClient(BaseServiceClient):
    """gRPC service client."""
    
    def __init__(self, host: str, port: int, timeout: int = 30, stub_class=None):
        """
        Initialize gRPC client.
        
        Args:
            host: Service host
            port: Service port
            timeout: Request timeout in seconds
            stub_class: gRPC stub class
        """
        super().__init__(host, port, timeout)
        self.stub_class = stub_class
        self.stub = None
    
    async def connect(self):
        """Establish gRPC connection."""
        self._channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        if self.stub_class:
            self.stub = self.stub_class(self._channel)
        
        # Wait for channel to be ready
        await self._channel.ready()
        logger.info(f"Connected to gRPC service at {self.host}:{self.port}")
    
    async def disconnect(self):
        """Close gRPC connection."""
        if self._channel:
            await self._channel.close()
            logger.info(f"Disconnected from gRPC service at {self.host}:{self.port}")
    
    async def call_unary_unary(self, method, request, timeout=None):
        """
        Call unary-unary gRPC method.
        
        Args:
            method: gRPC method to call
            request: Request message
            timeout: Override default timeout
            
        Returns:
            Response message
        """
        timeout = timeout or self.timeout
        try:
            response = await method(request, timeout=timeout)
            return response
        except grpc.aio.AioRpcError as e:
            logger.error(f"gRPC error: {e.code()}: {e.details()}")
            raise


class HttpClient(BaseServiceClient):
    """HTTP service client."""
    
    def __init__(self, host: str, port: int, timeout: int = 30, base_path: str = ""):
        """
        Initialize HTTP client.
        
        Args:
            host: Service host
            port: Service port
            timeout: Request timeout in seconds
            base_path: Base path for API endpoints
        """
        super().__init__(host, port, timeout)
        self.base_path = base_path
        self.base_url = f"http://{host}:{port}{base_path}"
        self._client = None
    
    async def connect(self):
        """Initialize HTTP client."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        logger.info(f"Initialized HTTP client for {self.base_url}")
    
    async def disconnect(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            logger.info(f"Closed HTTP client for {self.base_url}")
    
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        """
        Send GET request.
        
        Args:
            path: API path
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{path}"
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def post(self, path: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None):
        """
        Send POST request.
        
        Args:
            path: API path
            data: Form data
            json: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{path}"
        response = await self._client.post(url, data=data, json=json)
        response.raise_for_status()
        return response.json()
    
    async def put(self, path: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None):
        """
        Send PUT request.
        
        Args:
            path: API path
            data: Form data
            json: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{path}"
        response = await self._client.put(url, data=data, json=json)
        response.raise_for_status()
        return response.json()
    
    async def delete(self, path: str):
        """
        Send DELETE request.
        
        Args:
            path: API path
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{path}"
        response = await self._client.delete(url)
        response.raise_for_status()
        return response.json()


# Specific service clients
class DocumentServiceClient(GrpcClient):
    """Document service gRPC client."""
    
    def __init__(self, host: str, port: int, timeout: int = 30):
        super().__init__(host, port, timeout)
        # Import stub class when available
        # from ai_platform.proto.document_service_pb2 import DocumentServiceStub
        # self.stub_class = DocumentServiceStub
    
    async def upload_document(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Upload document to service."""
        # This would use the actual proto stubs when available
        # For now, return a mock response
        return {
            "document_id": "test-doc-001",
            "status": "uploaded",
            "title": title
        }
    
    async def get_document(self, document_id: str):
        """Get document from service."""
        return {
            "document_id": document_id,
            "title": "Test Document",
            "content": "Test content",
            "status": "processed"
        }
    
    async def delete_document(self, document_id: str):
        """Delete document from service."""
        return {"status": "deleted", "document_id": document_id}


class EmbeddingServiceClient(GrpcClient):
    """Embedding service gRPC client."""
    
    def __init__(self, host: str, port: int, timeout: int = 30):
        super().__init__(host, port, timeout)
        # Import stub class when available
        # from ai_platform.proto.embedding_service_pb2 import EmbeddingServiceStub
        # self.stub_class = EmbeddingServiceStub
    
    async def create_embedding(self, text: str, model: str = "bge-m3"):
        """Create embedding for text."""
        # Mock embedding response
        return {
            "embedding_id": "emb-001",
            "vector": [0.1] * 1024,  # Mock 1024-dimensional vector
            "model": model,
            "dimension": 1024
        }
    
    async def batch_create_embeddings(self, texts: list, model: str = "bge-m3"):
        """Create embeddings for multiple texts."""
        return {
            "embeddings": [
                {
                    "embedding_id": f"emb-{i}",
                    "vector": [0.1] * 1024,
                    "model": model,
                    "dimension": 1024
                }
                for i in range(len(texts))
            ]
        }


class RetrievalServiceClient(GrpcClient):
    """Retrieval service gRPC client."""
    
    def __init__(self, host: str, port: int, timeout: int = 30):
        super().__init__(host, port, timeout)
        # Import stub class when available
        # from ai_platform.proto.retrieval_service_pb2 import RetrievalServiceStub
        # self.stub_class = RetrievalServiceStub
    
    async def search(self, query: str, limit: int = 10, filters: Optional[Dict[str, Any]] = None):
        """Search for relevant documents."""
        return {
            "results": [
                {
                    "document_id": "doc-001",
                    "chunk_id": "chunk-001",
                    "score": 0.95,
                    "content": "Relevant content..."
                }
            ],
            "query": query,
            "total_results": 1
        }


class GenerationServiceClient(GrpcClient):
    """Generation service gRPC client."""
    
    def __init__(self, host: str, port: int, timeout: int = 30):
        super().__init__(host, port, timeout)
        # Import stub class when available
        # from ai_platform.proto.generation_service_pb2 import GenerationServiceStub
        # self.stub_class = GenerationServiceStub
    
    async def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None):
        """Generate response."""
        return {
            "response_id": "gen-001",
            "response": "This is a generated response.",
            "model": "llama-3-8b",
            "tokens_used": 150
        }
    
    async def generate_with_rag(self, query: str, retrieved_docs: list):
        """Generate response using RAG."""
        return {
            "response_id": "gen-002",
            "response": "This is a RAG-generated response based on retrieved documents.",
            "sources": [doc["document_id"] for doc in retrieved_docs],
            "model": "llama-3-8b",
            "tokens_used": 200
        }