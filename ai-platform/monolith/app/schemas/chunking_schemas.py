from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class ChunkingStrategy(str, Enum):
    """Semantic chunking strategies"""
    COMPETENCY_BASED = "competency_based"
    ACTIVITY_BASED = "activity_based"
    ASSESSMENT_BASED = "assessment_based"
    INQUIRY_BASED = "inquiry_based"
    LESSON_PLAN_BASED = "lesson_plan_based"
    SEMANTIC_BASED = "semantic"
    HIERARCHY_BASED = "hierarchy"


class ChunkingOptions(BaseModel):
    """Options for semantic chunking"""
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.SEMANTIC_BASED
    chunk_size: int = Field(default=500, ge=100, le=2000, description="Target chunk size in characters")
    chunk_overlap: int = Field(default=50, ge=0, le=200, description="Character overlap between chunks")
    include_metadata: bool = True
    detect_hierarchy: bool = True
    classify_pedagogy: bool = True
    tag_taxonomy: bool = True
    enrich_chunks: bool = True
    
    # Educational-specific options
    curriculum_aware: bool = True
    competency_aware: bool = True
    pedagogy_aware: bool = True
    
    # Content preservation
    preserve_structure: bool = True
    preserve_headers: bool = True


class ChunkMetadata(BaseModel):
    """Educational metadata for chunks"""
    chunk_id: str
    chunk_type: str  # competency, activity, assessment, inquiry, etc.
    competency: Optional[str] = None
    pedagogy_type: Optional[str] = None  # inquiry, differentiated, deep learning
    cognitive_level: Optional[str] = None  # Bloom's taxonomy
    learning_objective: Optional[str] = None
    difficulty: Optional[str] = None  # easy, medium, hard
    subject: Optional[str] = None
    grade: Optional[str] = None
    phase: Optional[str] = None
    assessment_type: Optional[str] = None
    activity_type: Optional[str] = None
    
    # Positional metadata
    document_position: int
    section_title: Optional[str] = None
    heading_level: Optional[int] = None
    
    # Quality metrics
    chunk_quality_score: Optional[float] = None
    educational_value_score: Optional[float] = None


class ChunkInfo(BaseModel):
    """Individual chunk information"""
    chunk_id: str
    text: str
    metadata: ChunkMetadata
    character_count: int
    word_count: int
    position: int
    confidence: float


class DocumentMetadata(BaseModel):
    """Document-level metadata"""
    title: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    phase: Optional[str] = None
    curriculum_source: Optional[str] = None  # CP, ATP, buku, etc.
    document_type: Optional[str] = None  # textbook, worksheet, assessment, etc.
    language: Optional[str] = None
    author: Optional[str] = None


class ChunkRequest(BaseModel):
    """Request for semantic chunking"""
    document_id: str
    text: str
    options: ChunkingOptions = Field(default_factory=ChunkingOptions)
    metadata: Optional[DocumentMetadata] = None


class BatchChunkRequest(BaseModel):
    """Request for batch chunking"""
    documents: List[ChunkRequest]
    options: ChunkingOptions = Field(default_factory=ChunkingOptions)


class ChunkResponse(BaseModel):
    """Response for semantic chunking"""
    success: bool
    document_id: str
    status: str  # processing, completed, failed
    chunks: Optional[List[ChunkInfo]] = None
    chunk_count: Optional[int] = None
    processing_time: Optional[float] = None
    statistics: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class BatchChunkResponse(BaseModel):
    """Response for batch chunking"""
    success: bool
    total_documents: int
    completed: int
    failed: int
    results: List[Dict[str, Any]]


class ChunkQualityMetrics(BaseModel):
    """Quality metrics for chunks"""
    average_chunk_size: float
    size_variance: float
    metadata_coverage: float
    hierarchy_preserved: bool
    educational_relevance: float


class ChunkingStatistics(BaseModel):
    """Statistics about chunking operation"""
    total_chunks: int
    average_chunk_length: float
    min_chunk_length: int
    max_chunk_length: int
    chunk_types_distribution: Dict[str, int]
    pedagogy_distribution: Dict[str, int]
    cognitive_level_distribution: Dict[str, int]
    quality_metrics: ChunkQualityMetrics