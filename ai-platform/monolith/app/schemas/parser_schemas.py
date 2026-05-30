from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class ExtractionOptions(BaseModel):
    """Options for document extraction"""
    extract_text: bool = True
    extract_tables: bool = True
    extract_images: bool = True
    extract_layout: bool = True
    perform_ocr: bool = True
    normalize_content: bool = True
    preserve_formatting: bool = False
    
    # OCR options
    ocr_language: str = "ind+eng"
    ocr_dpi: int = 300
    
    # Table extraction options
    table_flavor: str = "lattice"  # or "stream"
    
    # Image extraction options
    extract_images_from_text: bool = False
    image_min_size: int = 100


class DocumentUploadResponse(BaseModel):
    """Response for document upload"""
    success: bool
    document_id: str
    filename: str
    file_size: int
    file_type: str
    status: DocumentStatus
    message: Optional[str] = None


class ParseRequest(BaseModel):
    """Request for document parsing"""
    document_id: str
    filename: str
    options: ExtractionOptions = Field(default_factory=ExtractionOptions)


class ParseResponse(BaseModel):
    """Response for document parsing"""
    success: bool
    document_id: str
    status: DocumentStatus
    message: Optional[str] = None
    processing_time: Optional[float] = None


class TableData(BaseModel):
    """Extracted table data"""
    page_number: int
    table_number: int
    headers: List[str]
    rows: List[List[str]]
    accuracy: Optional[float] = None


class ImageData(BaseModel):
    """Extracted image data"""
    page_number: int
    image_number: int
    image_type: str  # "photo", "drawing", "chart", etc.
    bounding_box: List[int]  # [x1, y1, x2, y2]
    caption: Optional[str] = None


class LayoutRegion(BaseModel):
    """Layout region detected in document"""
    region_type: str  # "text", "table", "image", "header", "footer", etc.
    page_number: int
    bounding_box: List[int]  # [x1, y1, x2, y2]
    confidence: Optional[float] = None
    content: Optional[str] = None


class DocumentMetadata(BaseModel):
    """Document metadata"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[List[str]] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[datetime] = None
    modification_date: Optional[datetime] = None
    page_count: int
    word_count: Optional[int] = None
    character_count: Optional[int] = None
    language: Optional[str] = None


class ExtractionResult(BaseModel):
    """Complete extraction result"""
    document_id: str
    text_content: Optional[str] = None
    tables: Optional[List[TableData]] = None
    images: Optional[List[ImageData]] = None
    layout: Optional[List[LayoutRegion]] = None
    metadata: Optional[DocumentMetadata] = None
    extraction_time: Optional[float] = None
    confidence_score: Optional[float] = None


class ContentStatistics(BaseModel):
    """Statistics about extracted content"""
    total_pages: int
    total_text_length: int
    total_tables: int
    total_images: int
    total_words: int
    language_detected: Optional[str] = None
    avg_word_length: Optional[float] = None


class OCRResult(BaseModel):
    """OCR processing result"""
    text: str
    confidence: float
    language: str
    processing_time: float
    regions: Optional[List[LayoutRegion]] = None