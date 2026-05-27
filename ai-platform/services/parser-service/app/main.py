from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import os
import uuid
from pathlib import Path
import tempfile

# Import shared components
import sys
sys.path.append('/app')
from shared.configs.settings import settings
from shared.logging.logger import setup_logging
from shared.schemas.common import HealthResponse, BaseResponse, ErrorResponse, DocumentMetadata
from shared.exceptions.exceptions import ParsingError, FileUploadError
from shared.utils.helpers import generate_id, sanitize_filename

# Import parser components
from app.extractors.text_extractor import TextExtractor
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.extractors.layout_detector import LayoutDetector
from app.pipelines.document_pipeline import DocumentPipeline
from app.normalizers.content_normalizer import ContentNormalizer
from app.schemas.parser_schemas import (
    DocumentUploadResponse,
    ParseRequest,
    ParseResponse,
    ExtractionResult,
    DocumentStatus
)
from app.consumer import AsyncParserServiceConsumer

# Setup logging
logger = setup_logging("parser-service")

# Temporary storage for processing documents
TEMP_DIR = Path(tempfile.gettempdir()) / "parser-service"
TEMP_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Parser Service")
    # Initialize extractors
    app.state.text_extractor = TextExtractor()
    app.state.table_extractor = TableExtractor()
    app.state.image_extractor = ImageExtractor()
    app.state.ocr_extractor = OCRExtractor()
    app.state.layout_detector = LayoutDetector()
    app.state.content_normalizer = ContentNormalizer()
    app.state.document_pipeline = DocumentPipeline(
        text_extractor=app.state.text_extractor,
        table_extractor=app.state.table_extractor,
        image_extractor=app.state.image_extractor,
        ocr_extractor=app.state.ocr_extractor,
        layout_detector=app.state.layout_detector,
        content_normalizer=app.state.content_normalizer
    )
    
    # Start RabbitMQ consumer if enabled
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq:
        logger.info("Starting RabbitMQ consumer")
        app.state.rabbitmq_consumer = AsyncParserServiceConsumer()
        app.state.rabbitmq_consumer.start_consuming_async()
        logger.info("RabbitMQ consumer started")
    
    yield
    logger.info("Shutting down Parser Service")
    
    # Stop RabbitMQ consumer if running
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Parser Service",
    description="Document intelligence foundation for educational AI platform",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        services={
            "text_extractor": "available",
            "table_extractor": "available",
            "image_extractor": "available",
            "ocr_extractor": "available",
            "layout_detector": "available",
            "content_normalizer": "available"
        }
    )


@app.post("/api/v1/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload document for parsing"""
    
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.png', '.jpg', '.jpeg']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise FileUploadError(f"File type {file_extension} not allowed")
        
        # Generate document ID
        document_id = generate_id()
        
        # Create temporary file
        temp_file_path = TEMP_DIR / f"{document_id}{file_extension}"
        
        # Save uploaded file
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Document uploaded: {document_id}, filename: {file.filename}, size: {len(content)} bytes")
        
        return DocumentUploadResponse(
            success=True,
            document_id=document_id,
            filename=file.filename,
            file_size=len(content),
            file_type=file_extension,
            status=DocumentStatus.UPLOADED,
            message="Document uploaded successfully"
        )
        
    except FileUploadError as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/documents/parse", response_model=ParseResponse)
async def parse_document(request: ParseRequest, background_tasks: BackgroundTasks):
    """Parse uploaded document"""
    
    try:
        # Check if document exists
        file_extension = Path(request.filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"{request.document_id}{file_extension}"
        
        if not temp_file_path.exists():
            raise HTTPException(status_code=404, detail="Document not found")
        
        logger.info(f"Parsing document: {request.document_id}")
        
        # Run parsing in background
        def process_document():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                result = app.state.document_pipeline.process(
                    file_path=str(temp_file_path),
                    options=request.options
                )
                
                logger.info(f"Document parsed successfully: {request.document_id}")
                return result
                
            except Exception as e:
                logger.error(f"Error processing document {request.document_id}: {str(e)}")
                raise
        
        # Add background task
        background_tasks.add_task(process_document)
        
        return ParseResponse(
            success=True,
            document_id=request.document_id,
            status=DocumentStatus.PROCESSING,
            message="Document parsing started"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error parsing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/{document_id}/status", response_model=Dict[str, Any])
async def get_document_status(document_id: str):
    """Get document parsing status"""
    
    try:
        # Check if document exists in temp directory
        temp_files = list(TEMP_DIR.glob(f"{document_id}.*"))
        
        if not temp_files:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # For simplicity, return basic status
        # In production, this would check a database or queue
        return {
            "document_id": document_id,
            "status": DocumentStatus.PROCESSED,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/{document_id}/extracted", response_model=ExtractionResult)
async def get_extracted_content(document_id: str, extraction_type: str = "all"):
    """Get extracted content from document"""
    
    try:
        # Check if document exists
        temp_files = list(TEMP_DIR.glob(f"{document_id}.*"))
        
        if not temp_files:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = temp_files[0]
        
        # Extract based on type
        result = ExtractionResult(document_id=document_id)
        
        if extraction_type in ["all", "text"]:
            text_content = app.state.text_extractor.extract(str(file_path))
            result.text_content = text_content
        
        if extraction_type in ["all", "tables"]:
            tables = app.state.table_extractor.extract(str(file_path))
            result.tables = tables
        
        if extraction_type in ["all", "images"]:
            images = app.state.image_extractor.extract(str(file_path))
            result.images = images
        
        if extraction_type in ["all", "layout"]:
            layout = app.state.layout_detector.detect(str(file_path))
            result.layout = layout
        
        if extraction_type in ["all", "metadata"]:
            metadata = app.state.content_normalizer.extract_metadata(str(file_path))
            result.metadata = metadata
        
        logger.info(f"Content extracted for document: {document_id}, type: {extraction_type}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/documents/extract-text")
async def extract_text_only(file: UploadFile = File(...)):
    """Quick text extraction endpoint"""
    
    try:
        # Save temporary file
        temp_file_path = TEMP_DIR / f"temp_{generate_id()}{Path(file.filename).suffix}"
        
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        # Extract text
        text_content = app.state.text_extractor.extract(str(temp_file_path))
        
        # Clean up
        temp_file_path.unlink()
        
        return BaseResponse(
            success=True,
            data={
                "text": text_content,
                "length": len(text_content),
                "filename": file.filename
            }
        )
        
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/documents/detect-layout")
async def detect_layout(file: UploadFile = File(...)):
    """Detect document layout"""
    
    try:
        # Save temporary file
        temp_file_path = TEMP_DIR / f"temp_{generate_id()}{Path(file.filename).suffix}"
        
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        # Detect layout
        layout = app.state.layout_detector.detect(str(temp_file_path))
        
        # Clean up
        temp_file_path.unlink()
        
        return BaseResponse(
            success=True,
            data={
                "layout": layout,
                "filename": file.filename
            }
        )
        
    except Exception as e:
        logger.error(f"Error detecting layout: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete processed document"""
    
    try:
        # Find and delete document files
        temp_files = list(TEMP_DIR.glob(f"{document_id}.*"))
        
        if not temp_files:
            raise HTTPException(status_code=404, detail="Document not found")
        
        for file_path in temp_files:
            file_path.unlink()
        
        logger.info(f"Document deleted: {document_id}")
        
        return BaseResponse(
            success=True,
            message=f"Document {document_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """HTTP exception handler"""
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}"
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ).dict()
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8008,
        workers=1,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )