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
import io

# Import shared components
import sys
sys.path.append('/app')
from shared.configs.settings import settings
from shared.logging.logger import setup_logging
from shared.schemas.common import HealthResponse, BaseResponse, ErrorResponse
from shared.exceptions.exceptions import ProcessingError
from shared.utils.helpers import generate_id

# Import vision components
from app.OCR.ocr_processor import OCRProcessor
from app.VLM.image_classifier import ImageClassifier
from app.captioning.image_captioning import ImageCaptioning
from app.diagram_analysis.diagram_analyzer import DiagramAnalyzer
from app.embeddings.image_embeddings import ImageEmbeddings
from app.schemas.vision_schemas import (
    ImageUploadResponse,
    OCRRequest,
    OCRResponse,
    ClassificationRequest,
    ClassificationResponse,
    DiagramAnalysisRequest,
    DiagramAnalysisResponse
)
from app.consumer import AsyncVisionServiceConsumer

# Setup logging
logger = setup_logging("vision-service")

# Temporary storage for processing images
TEMP_DIR = Path(tempfile.gettempdir()) / "vision-service"
TEMP_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Vision Service")
    
    # Initialize vision components
    try:
        app.state.ocr_processor = OCRProcessor()
        app.state.image_classifier = ImageClassifier()
        app.state.image_captioning = ImageCaptioning()
        app.state.diagram_analyzer = DiagramAnalyzer()
        app.state.image_embeddings = ImageEmbeddings()
        logger.info("Vision components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing vision components: {str(e)}")
        # Continue even if some components fail to initialize
    
    # Start RabbitMQ consumer if enabled
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq:
        logger.info("Starting RabbitMQ consumer")
        app.state.rabbitmq_consumer = AsyncVisionServiceConsumer()
        app.state.rabbitmq_consumer.start_consuming_async()
        logger.info("RabbitMQ consumer started")
    
    yield
    logger.info("Shutting down Vision Service")
    
    # Stop RabbitMQ consumer if running
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Vision Service",
    description="Image processing, OCR, and visual intelligence for educational AI platform",
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
    components_status = {
        "ocr_processor": "available" if app.state.ocr_processor.initialized else "unavailable",
        "image_classifier": "available" if app.state.image_classifier.initialized else "unavailable",
        "image_captioning": "available" if app.state.image_captioning.initialized else "unavailable",
        "diagram_analyzer": "available" if app.state.diagram_analyzer.initialized else "unavailable",
        "image_embeddings": "available" if app.state.image_embeddings.initialized else "unavailable"
    }
    
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        services=components_status
    )


@app.post("/api/v1/images/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload image for processing"""
    
    try:
        # Validate file type
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"File type {file_extension} not allowed")
        
        # Generate image ID
        image_id = generate_id()
        
        # Create temporary file
        temp_file_path = TEMP_DIR / f"{image_id}{file_extension}"
        
        # Save uploaded image
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Image uploaded: {image_id}, filename: {file.filename}, size: {len(content)} bytes")
        
        return ImageUploadResponse(
            success=True,
            image_id=image_id,
            filename=file.filename,
            file_size=len(content),
            file_type=file_extension,
            message="Image uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ocr", response_model=OCRResponse)
async def perform_ocr(request: OCRRequest):
    """Perform OCR on image"""
    
    try:
        # Check if image exists
        file_extension = Path(request.filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"{request.image_id}{file_extension}"
        
        if not temp_file_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        logger.info(f"Performing OCR on image: {request.image_id}")
        
        # Perform OCR
        ocr_options = {
            'language': request.language,
            'dpi': request.dpi,
            'return_regions': request.return_regions
        }
        
        ocr_result = app.state.ocr_processor.process(str(temp_file_path), ocr_options)
        
        return OCRResponse(
            success=True,
            image_id=request.image_id,
            text=ocr_result['text'],
            confidence=ocr_result.get('confidence', 0.0),
            language=ocr_result.get('language', 'unknown'),
            regions=ocr_result.get('regions', []) if request.return_regions else [],
            processing_time=ocr_result.get('processing_time', 0.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing OCR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/classify", response_model=ClassificationResponse)
async def classify_image(request: ClassificationRequest):
    """Classify image content"""
    
    try:
        # Check if image exists
        file_extension = Path(request.filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"{request.image_id}{file_extension}"
        
        if not temp_file_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        logger.info(f"Classifying image: {request.image_id}")
        
        # Perform classification
        classification_result = app.state.image_classifier.classify(
            str(temp_file_path),
            request.classification_type
        )
        
        return ClassificationResponse(
            success=True,
            image_id=request.image_id,
            classification_type=request.classification_type,
            predicted_class=classification_result.get('predicted_class'),
            confidence=classification_result.get('confidence', 0.0),
            classes=classification_result.get('classes', []),
            processing_time=classification_result.get('processing_time', 0.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error classifying image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/caption")
async def generate_caption(image_id: str, filename: str):
    """Generate caption for image"""
    
    try:
        # Check if image exists
        file_extension = Path(filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"{image_id}{file_extension}"
        
        if not temp_file_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        logger.info(f"Generating caption for image: {image_id}")
        
        # Generate caption
        caption_result = app.state.image_captioning.generate_caption(str(temp_file_path))
        
        return BaseResponse(
            success=True,
            data={
                "image_id": image_id,
                "caption": caption_result.get('caption', ''),
                "confidence": caption_result.get('confidence', 0.0),
                "processing_time": caption_result.get('processing_time', 0.0)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze-diagram", response_model=DiagramAnalysisResponse)
async def analyze_diagram(request: DiagramAnalysisRequest):
    """Analyze diagram structure"""
    
    try:
        # Check if image exists
        file_extension = Path(request.filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"{request.image_id}{file_extension}"
        
        if not temp_file_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        logger.info(f"Analyzing diagram: {request.image_id}")
        
        # Perform diagram analysis
        analysis_result = app.state.diagram_analyzer.analyze(
            str(temp_file_path),
            request.diagram_type
        )
        
        return DiagramAnalysisResponse(
            success=True,
            image_id=request.image_id,
            diagram_type=request.diagram_type,
            detected_type=analysis_result.get('detected_type'),
            elements=analysis_result.get('elements', []),
            structure=analysis_result.get('structure', {}),
            confidence=analysis_result.get('confidence', 0.0),
            processing_time=analysis_result.get('processing_time', 0.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing diagram: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/embeddings")
async def generate_image_embeddings(image_id: str, filename: str):
    """Generate embeddings for image"""
    
    try:
        # Check if image exists
        file_extension = Path(filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"{image_id}{file_extension}"
        
        if not temp_file_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        logger.info(f"Generating embeddings for image: {image_id}")
        
        # Generate embeddings
        embedding_result = app.state.image_embeddings.generate(str(temp_file_path))
        
        return BaseResponse(
            success=True,
            data={
                "image_id": image_id,
                "embeddings": embedding_result.get('embeddings', []),
                "embedding_dimension": embedding_result.get('dimension', 0),
                "model": embedding_result.get('model', ''),
                "processing_time": embedding_result.get('processing_time', 0.0)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/process-document-images")
async def process_document_images(file: UploadFile = File(...)):
    """Process document images (batch OCR and classification)"""
    
    try:
        # Save uploaded file
        file_extension = Path(file.filename).suffix.lower()
        temp_file_path = TEMP_DIR / f"temp_{generate_id()}{file_extension}"
        
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Processing document images from: {file.filename}")
        
        # Process document to extract images and process them
        # This would typically call the parser service first
        # For now, return a placeholder response
        
        return BaseResponse(
            success=True,
            data={
                "message": "Document image processing initiated",
                "filename": file.filename,
                "status": "processing"
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing document images: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/images/{image_id}")
async def delete_image(image_id: str):
    """Delete processed image"""
    
    try:
        # Find and delete image files
        temp_files = list(TEMP_DIR.glob(f"{image_id}.*"))
        
        if not temp_files:
            raise HTTPException(status_code=404, detail="Image not found")
        
        for file_path in temp_files:
            file_path.unlink()
        
        logger.info(f"Image deleted: {image_id}")
        
        return BaseResponse(
            success=True,
            message=f"Image {image_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting image: {str(e)}")
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
        port=8012,
        workers=1,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )