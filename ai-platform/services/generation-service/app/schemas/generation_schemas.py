"""
Pydantic schemas for Generation Service requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class GenerationProvider(str, Enum):
    """LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class GenerationRequest(BaseModel):
    """Base generation request"""
    prompt: str = Field(..., description="Prompt for generation", min_length=1)
    provider: Optional[GenerationProvider] = Field(None, description="LLM provider")
    model: Optional[str] = Field(None, description="Model name")
    temperature: float = Field(default=0.7, description="Temperature for generation", ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate", ge=1, le=8000)


class GenerationResponse(BaseModel):
    """Generation response"""
    text: str = Field(..., description="Generated text")
    provider: str = Field(..., description="Provider used")
    model: str = Field(..., description="Model used")
    tokens_used: int = Field(..., description="Tokens used")
    latency_ms: int = Field(..., description="Generation latency in milliseconds")


class DocumentReference(BaseModel):
    """Document reference for citations"""
    id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    source: str = Field(..., description="Document source")


class CitationGenerationRequest(BaseModel):
    """Citation generation request"""
    prompt: str = Field(..., description="Prompt for generation", min_length=1)
    context: str = Field(..., description="Context information")
    documents: List[DocumentReference] = Field(..., description="Documents to cite")
    provider: Optional[GenerationProvider] = Field(None, description="LLM provider")
    model: Optional[str] = Field(None, description="Model name")
    temperature: float = Field(default=0.7, description="Temperature for generation", ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate", ge=1, le=8000)


class Citation(BaseModel):
    """Citation information"""
    text: str = Field(..., description="Cited text")
    document_id: str = Field(..., description="Document ID")
    source: str = Field(..., description="Document source")
    position: List[int] = Field(..., description="Position in response")


class CitationGenerationResponse(BaseModel):
    """Citation generation response"""
    text: str = Field(..., description="Generated text with citations")
    citations: List[Citation] = Field(..., description="Extracted citations")
    provider: str = Field(..., description="Provider used")
    model: str = Field(..., description="Model used")
    citation_count: int = Field(..., description="Number of citations")


class ValidationRequest(BaseModel):
    """Validation request"""
    response: str = Field(..., description="Generated response to validate", min_length=1)
    context: str = Field(..., description="Context information")
    documents: List[DocumentReference] = Field(default_factory=list, description="Source documents")


class ValidationIssue(BaseModel):
    """Validation issue"""
    type: str = Field(..., description="Issue type")
    severity: str = Field(..., description="Issue severity (low, medium, high)")
    message: str = Field(..., description="Issue description")
    location: Optional[str] = Field(None, description="Location in response")


class ValidationResponse(BaseModel):
    """Validation response"""
    is_valid: bool = Field(..., description="Whether response is valid")
    confidence: float = Field(..., description="Validation confidence", ge=0.0, le=1.0)
    issues: List[ValidationIssue] = Field(default_factory=list, description="Validation issues")
    hallucination_score: float = Field(..., description="Hallucination score", ge=0.0, le=1.0)
    relevance_score: float = Field(..., description="Relevance score", ge=0.0, le=1.0)


class TemplateGenerationRequest(BaseModel):
    """Template generation request"""
    template_name: str = Field(..., description="Name of the template to use")
    variables: Dict[str, Any] = Field(..., description="Variables for the template")
    provider: Optional[GenerationProvider] = Field(None, description="LLM provider")
    model: Optional[str] = Field(None, description="Model name")
    temperature: float = Field(default=0.7, description="Temperature for generation", ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate", ge=1, le=8000)


class GenerationHealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    providers: Dict[str, bool] = Field(..., description="Provider availability")