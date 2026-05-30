"""
Document Schemas for Semantic Chunk Service
Handles incoming documents from Parser Service
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class DocumentChunkingRequest(BaseModel):
    """Request for chunking a parsed document"""
    document_id: str = Field(..., description="Document identifier from parser service")
    document_type: Optional[str] = Field(None, description="Type of document (textbook, lesson_plan, assessment, etc.)")
    text_content: str = Field(..., description="Full text content from parser service")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Document metadata from parser service")
    chunking_options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Chunking options")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_123",
                "document_type": "textbook",
                "text_content": "Full text content...",
                "metadata": {
                    "subject": "Mathematics",
                    "grade": "5",
                    "phase": "A"
                },
                "chunking_options": {
                    "chunk_size": 500,
                    "overlap": 50
                }
            }
        }


class DocumentChunkingResponse(BaseModel):
    """Response for document chunking"""
    success: bool = Field(..., description="Whether chunking was successful")
    document_id: str = Field(..., description="Document identifier")
    status: str = Field(..., description="Status of chunking operation")
    chunk_count: Optional[int] = Field(None, description="Number of chunks created")
    chunks: Optional[List[Dict[str, Any]]] = Field(None, description="Semantic chunks created")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    statistics: Optional[Dict[str, Any]] = Field(None, description="Chunking statistics")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "document_id": "doc_123",
                "status": "completed",
                "chunk_count": 25,
                "chunks": [
                    {
                        "chunk_id": "chunk_1",
                        "content": "Chunk content...",
                        "metadata": {
                            "chunk_type": "competency",
                            "subject": "Mathematics"
                        }
                    }
                ],
                "processing_time": 2.5,
                "statistics": {
                    "average_chunk_size": 450,
                    "total_chunks": 25
                },
                "message": "Document chunked successfully",
                "timestamp": "2024-01-01T00:00:00"
            }
        }