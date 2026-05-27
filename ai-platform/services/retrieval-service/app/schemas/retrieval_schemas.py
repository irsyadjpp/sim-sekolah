"""
Pydantic schemas for Retrieval Service requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class SearchResult(BaseModel):
    """Single search result"""
    id: str = Field(..., description="Document ID")
    score: float = Field(..., description="Relevance score")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")


class SemanticSearchRequest(BaseModel):
    """Semantic search request"""
    query: str = Field(..., description="Search query", min_length=1)
    collection_name: str = Field(default="documents", description="Qdrant collection name")
    limit: int = Field(default=10, description="Number of results to return", ge=1, le=100)
    score_threshold: Optional[float] = Field(None, description="Minimum score threshold", ge=0.0, le=1.0)
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")


class SemanticSearchResponse(BaseModel):
    """Semantic search response"""
    results: List[SearchResult] = Field(..., description="Search results")
    query: str = Field(..., description="Original query")
    total: int = Field(..., description="Total number of results")
    latency_ms: int = Field(..., description="Query latency in milliseconds")


class HybridSearchRequest(BaseModel):
    """Hybrid search request"""
    query: str = Field(..., description="Search query", min_length=1)
    collection_name: str = Field(default="documents", description="Qdrant collection name")
    semantic_weight: float = Field(default=0.7, description="Weight for semantic search", ge=0.0, le=1.0)
    keyword_weight: float = Field(default=0.3, description="Weight for keyword search", ge=0.0, le=1.0)
    limit: int = Field(default=10, description="Number of results to return", ge=1, le=100)
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")


class HybridSearchResponse(BaseModel):
    """Hybrid search response"""
    results: List[SearchResult] = Field(..., description="Search results")
    query: str = Field(..., description="Original query")
    total: int = Field(..., description="Total number of results")
    weights: Dict[str, float] = Field(..., description="Search weights used")
    latency_ms: int = Field(..., description="Query latency in milliseconds")


class MetadataFilterRequest(BaseModel):
    """Metadata filter request"""
    collection_name: str = Field(default="documents", description="Qdrant collection name")
    filters: Dict[str, Any] = Field(..., description="Metadata filters")
    limit: int = Field(default=10, description="Number of results to return", ge=1, le=100)
    order_by: Optional[str] = Field(None, description="Field to order by")


class MetadataFilterResponse(BaseModel):
    """Metadata filter response"""
    results: List[SearchResult] = Field(..., description="Filtered results")
    total: int = Field(..., description="Total number of results")
    filters: Dict[str, Any] = Field(..., description="Filters applied")


class QueryExpansionMethod(str, Enum):
    """Query expansion methods"""
    SYNONYM = "synonym"
    SEMANTIC = "semantic"
    CURRICULUM = "curriculum"
    NONE = "none"


class QueryBuilderRequest(BaseModel):
    """Query builder request"""
    query: str = Field(..., description="Original query", min_length=1)
    expansion_method: QueryExpansionMethod = Field(default=QueryExpansionMethod.SEMANTIC)
    num_expansions: int = Field(default=3, description="Number of query expansions", ge=1, le=10)


class QueryBuilderResponse(BaseModel):
    """Query builder response"""
    original_query: str = Field(..., description="Original query")
    optimized_query: Dict[str, Any] = Field(..., description="Optimized query with expansions")
    expansions: List[str] = Field(..., description="Generated query expansions")
    method: str = Field(..., description="Expansion method used")


class ContextStrategy(str, Enum):
    """Context building strategies"""
    CONCATENATE = "concatenate"
    RANKED = "ranked"
    DIVERSE = "diverse"
    SUMMARIZE = "summarize"


class DocumentInput(BaseModel):
    """Document input for context building"""
    id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Relevance score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")


class ContextBuilderRequest(BaseModel):
    """Context builder request"""
    documents: List[DocumentInput] = Field(..., description="Retrieved documents", min_items=1)
    max_tokens: int = Field(default=2000, description="Maximum tokens in context", ge=100, le=8000)
    strategy: ContextStrategy = Field(default=ContextStrategy.RANKED)


class ContextBuilderResponse(BaseModel):
    """Context builder response"""
    context: str = Field(..., description="Built context string")
    document_count: int = Field(..., description="Number of documents used")
    token_count: int = Field(..., description="Estimated token count")
    strategy: str = Field(..., description="Context building strategy used")


class RetrievalHealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    qdrant_url: str = Field(..., description="Qdrant connection URL")