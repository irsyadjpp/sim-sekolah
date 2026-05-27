"""
Pydantic schemas for Embedding Service requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class EmbeddingRequest(BaseModel):
    """Base embedding request"""
    model: Optional[str] = Field(None, description="Model name for embedding")


class TextEmbeddingRequest(EmbeddingRequest):
    """Text embedding request"""
    text: str = Field(..., description="Text to embed", min_length=1)
    model: Optional[str] = Field(None, description="Model name (default: BAAI/bge-m3)")


class TextEmbeddingResponse(BaseModel):
    """Text embedding response"""
    embeddings: List[float] = Field(..., description="Embedding vector")
    model: str = Field(..., description="Model used")
    dimension: int = Field(..., description="Embedding dimension")
    text_length: int = Field(..., description="Original text length")


class BatchTextEmbeddingRequest(BaseModel):
    """Batch text embedding request"""
    texts: List[str] = Field(..., description="List of texts to embed", min_items=1)
    model: Optional[str] = Field(None, description="Model name (default: BAAI/bge-m3)")
    batch_size: Optional[int] = Field(None, description="Batch size for processing")


class BatchTextEmbeddingResponse(BaseModel):
    """Batch text embedding response"""
    embeddings: List[List[float]] = Field(..., description="List of embedding vectors")
    model: str = Field(..., description="Model used")
    dimension: int = Field(..., description="Embedding dimension")
    count: int = Field(..., description="Number of embeddings generated")


class ImageEmbeddingRequest(EmbeddingRequest):
    """Image embedding request"""
    image_data: str = Field(..., description="Base64 encoded image data or image URL")
    model: Optional[str] = Field(None, description="Model name (default: CLIP)")


class ImageEmbeddingResponse(BaseModel):
    """Image embedding response"""
    embeddings: List[float] = Field(..., description="Embedding vector")
    model: str = Field(..., description="Model used")
    dimension: int = Field(..., description="Embedding dimension")


class TableEmbeddingRequest(EmbeddingRequest):
    """Table embedding request"""
    table_data: Dict[str, Any] = Field(..., description="Table data as dictionary")
    model: Optional[str] = Field(None, description="Model name (default: table-transformer)")


class TableEmbeddingResponse(BaseModel):
    """Table embedding response"""
    embeddings: List[float] = Field(..., description="Embedding vector")
    model: str = Field(..., description="Model used")
    dimension: int = Field(..., description="Embedding dimension")


class FormulaEmbeddingRequest(EmbeddingRequest):
    """Formula embedding request"""
    formula: str = Field(..., description="Mathematical formula in LaTeX format")
    model: Optional[str] = Field(None, description="Model name")


class FormulaEmbeddingResponse(BaseModel):
    """Formula embedding response"""
    embeddings: List[float] = Field(..., description="Embedding vector")
    model: str = Field(..., description="Model used")
    dimension: int = Field(..., description="Embedding dimension")


class EmbeddingHealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    model: str = Field(..., description="Current model")
    device: str = Field(..., description="Device being used")


class EmbeddingStatsResponse(BaseModel):
    """Embedding service statistics"""
    service: str = Field(..., description="Service name")
    model: str = Field(..., description="Current model")
    device: str = Field(..., description="Device being used")
    batch_size: int = Field(..., description="Batch size")
    status: Dict[str, bool] = Field(..., description="Status of each embedder")