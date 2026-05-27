"""
Pydantic schemas for Reranking Service requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentInput(BaseModel):
    """Document input for reranking"""
    id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Original relevance score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")


class RerankedDocument(BaseModel):
    """Reranked document with new score"""
    id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Reranked relevance score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    rank: int = Field(..., description="New rank position")


class RerankRequest(BaseModel):
    """Base rerank request"""
    query: str = Field(..., description="Search query", min_length=1)
    documents: List[DocumentInput] = Field(..., description="Documents to rerank", min_items=1)
    top_k: Optional[int] = Field(None, description="Number of top results to return")


class RerankResponse(BaseModel):
    """Rerank response"""
    results: List[RerankedDocument] = Field(..., description="Reranked results")
    query: str = Field(..., description="Original query")
    original_count: int = Field(..., description="Original document count")
    reranked_count: int = Field(..., description="Reranked document count")
    method: str = Field(..., description="Reranking method used")


class CurriculumLevel(str, Enum):
    """Curriculum levels for Kurikulum Merdeka"""
    SD = "SD"
    SMP = "SMP"
    SMA = "SMA"


class CompetencyType(str, Enum):
    """Core competency types"""
    KI_1 = "KI-1"
    KI_2 = "KI-2"
    KI_3 = "KI-3"
    KI_4 = "KI-4"


class CurriculumRerankRequest(BaseModel):
    """Curriculum-aware rerank request"""
    query: str = Field(..., description="Search query", min_length=1)
    documents: List[DocumentInput] = Field(..., description="Documents to rerank", min_items=1)
    curriculum_level: CurriculumLevel = Field(..., description="Curriculum level (SD/SMP/SMA)")
    subject: Optional[str] = Field(None, description="Subject name")
    competency_focus: Optional[CompetencyType] = Field(None, description="Competency type to focus on")


class CurriculumRerankResponse(BaseModel):
    """Curriculum rerank response"""
    results: List[RerankedDocument] = Field(..., description="Reranked results")
    query: str = Field(..., description="Original query")
    curriculum_level: str = Field(..., description="Curriculum level")
    subject: Optional[str] = Field(None, description="Subject")
    competency_focus: Optional[str] = Field(None, description="Competency focus")
    method: str = Field(..., description="Reranking method used")


class LearningStyle(str, Enum):
    """Learning styles (VARK model)"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING = "reading"
    KINESTHETIC = "kinesthetic"


class PedagogyType(str, Enum):
    """Pedagogical approaches"""
    DIRECT = "direct_instruction"
    INQUIRY = "inquiry_based"
    PROJECT = "project_based"
    COLLABORATIVE = "collaborative"
    PROBLEM = "problem_based"
    EXPERIENTIAL = "experiential"


class PedagogyRerankRequest(BaseModel):
    """Pedagogy-aware rerank request"""
    query: str = Field(..., description="Search query", min_length=1)
    documents: List[DocumentInput] = Field(..., description="Documents to rerank", min_items=1)
    learning_style: Optional[LearningStyle] = Field(None, description="Target learning style")
    pedagogy_type: Optional[PedagogyType] = Field(None, description="Pedagogical approach")


class PedagogyRerankResponse(BaseModel):
    """Pedagogy rerank response"""
    results: List[RerankedDocument] = Field(..., description="Reranked results")
    query: str = Field(..., description="Original query")
    learning_style: Optional[str] = Field(None, description="Learning style")
    pedagogy_type: Optional[str] = Field(None, description="Pedagogy type")
    method: str = Field(..., description="Reranking method used")


class BloomLevel(str, Enum):
    """Bloom's taxonomy levels"""
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class CompetencyRerankRequest(BaseModel):
    """Competency-aware rerank request"""
    query: str = Field(..., description="Search query", min_length=1)
    documents: List[DocumentInput] = Field(..., description="Documents to rerank", min_items=1)
    competency_type: CompetencyType = Field(..., description="Competency type (KI-1 to KI-4)")
    bloom_level: Optional[BloomLevel] = Field(None, description="Bloom's taxonomy level")


class CompetencyRerankResponse(BaseModel):
    """Competency rerank response"""
    results: List[RerankedDocument] = Field(..., description="Reranked results")
    query: str = Field(..., description="Original query")
    competency_type: str = Field(..., description="Competency type")
    bloom_level: Optional[str] = Field(None, description="Bloom's taxonomy level")
    method: str = Field(..., description="Reranking method used")


class RerankingHealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    model: str = Field(..., description="Current model")