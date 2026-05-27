from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class ImageUploadResponse(BaseModel):
    """Response for image upload"""
    success: bool
    image_id: str
    filename: str
    file_size: int
    file_type: str
    message: Optional[str] = None


class OCRRequest(BaseModel):
    """Request for OCR processing"""
    image_id: str
    filename: str
    language: str = "ind+eng"
    dpi: int = 300
    return_regions: bool = False


class OCRResponse(BaseModel):
    """Response for OCR processing"""
    success: bool
    image_id: str
    text: str
    confidence: float
    language: str
    regions: Optional[List[Dict[str, Any]]] = None
    processing_time: float


class ClassificationRequest(BaseModel):
    """Request for image classification"""
    image_id: str
    filename: str
    classification_type: str = "general"  # general, educational, document, diagram


class ClassificationResponse(BaseModel):
    """Response for image classification"""
    success: bool
    image_id: str
    classification_type: str
    predicted_class: str
    confidence: float
    classes: Optional[List[Dict[str, Any]]] = None
    processing_time: float


class DiagramAnalysisRequest(BaseModel):
    """Request for diagram analysis"""
    image_id: str
    filename: str
    diagram_type: Optional[str] = None  # auto-detect if not specified


class DiagramAnalysisResponse(BaseModel):
    """Response for diagram analysis"""
    success: bool
    image_id: str
    diagram_type: Optional[str] = None
    detected_type: str
    elements: Optional[List[Dict[str, Any]]] = None
    structure: Optional[Dict[str, Any]] = None
    confidence: float
    processing_time: float


class ImageRegion(BaseModel):
    """Image region detected"""
    region_type: str  # text, image, table, diagram, chart
    bounding_box: List[int]  # [x1, y1, x2, y2]
    confidence: float
    content: Optional[str] = None


class ImageProcessingResult(BaseModel):
    """Result of image processing"""
    image_id: str
    regions: Optional[List[ImageRegion]] = None
    ocr_result: Optional[Dict[str, Any]] = None
    classification: Optional[Dict[str, Any]] = None
    processing_time: float