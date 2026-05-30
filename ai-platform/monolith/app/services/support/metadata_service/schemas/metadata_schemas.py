from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class EnrichmentOptions(BaseModel):
    """Options for content enrichment"""
    difficulty: bool = True
    taxonomy: bool = True
    learning_style: bool = True
    competency: bool = True
    pedagogy: bool = True
    assessment: bool = True
    
    # Advanced options
    include_confidence: bool = True
    include_indicators: bool = True
    use_ml_models: bool = False  # For future ML-based enrichment


class DocumentMetadata(BaseModel):
    """Document-level metadata for enrichment context"""
    subject: Optional[str] = None
    grade: Optional[str] = None
    phase: Optional[str] = None
    curriculum_source: Optional[str] = None
    document_type: Optional[str] = None
    language: Optional[str] = None
    difficulty_level: Optional[str] = None


class EnrichmentRequest(BaseModel):
    """Request for content enrichment"""
    content_id: str
    text: str
    options: EnrichmentOptions = Field(default_factory=EnrichmentOptions)
    metadata: Optional[DocumentMetadata] = None


class EnrichmentResult(BaseModel):
    """Result of a specific enrichment process"""
    enrichment_type: str
    result: Dict[str, Any]
    confidence: float
    processing_time: float


class EnrichmentResponse(BaseModel):
    """Response for content enrichment"""
    success: bool
    content_id: str
    enrichments: Dict[str, Any]
    processing_time: float
    status: str
    message: Optional[str] = None


class BatchEnrichmentRequest(BaseModel):
    """Request for batch enrichment"""
    contents: List[EnrichmentRequest]
    options: EnrichmentOptions = Field(default_factory=EnrichmentOptions)


class BatchEnrichmentResponse(BaseModel):
    """Response for batch enrichment"""
    success: bool
    total_contents: int
    completed: int
    failed: int
    results: List[Dict[str, Any]]