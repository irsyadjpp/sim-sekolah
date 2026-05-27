"""
Embedding Service - Generates embeddings for text, images, tables, and formulas
Supports multiple embedding models including BAAI/bge-m3 and multilingual-e5-large
"""
import os
import sys
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add shared modules to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../shared")))

from configs.settings import settings
from logging.logging_config import setup_logging
from middleware.error_handler import error_handler
from middleware.auth_middleware import auth_middleware
from schemas.embedding_schemas import (
    TextEmbeddingRequest,
    TextEmbeddingResponse,
    BatchTextEmbeddingRequest,
    BatchTextEmbeddingResponse,
    ImageEmbeddingRequest,
    ImageEmbeddingResponse,
    TableEmbeddingRequest,
    TableEmbeddingResponse,
    EmbeddingHealthResponse
)

from embedders.text.text_embedder import TextEmbedder
from embedders.image.image_embedder import ImageEmbedder
from embedders.table.table_embedder import TableEmbedder
from embedders.formula.formula_embedder import FormulaEmbedder
from app.consumer import AsyncEmbeddingServiceConsumer

# Setup logging
logger = setup_logging(__name__)

# Global embedder instances
text_embedder: Optional[TextEmbedder] = None
image_embedder: Optional[ImageEmbedder] = None
table_embedder: Optional[TableEmbedder] = None
formula_embedder: Optional[FormulaEmbedder] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global text_embedder, image_embedder, table_embedder, formula_embedder
    
    # Startup
    logger.info("Starting Embedding Service...")
    
    try:
        # Initialize text embedder
        text_embedder = TextEmbedder(
            model_name=settings.embedding_model,
            device=settings.embedding_device,
            batch_size=settings.embedding_batch_size
        )
        logger.info(f"Text embedder initialized with model: {settings.embedding_model}")
        
        # Initialize image embedder
        image_embedder = ImageEmbedder(device=settings.embedding_device)
        logger.info("Image embedder initialized")
        
        # Initialize table embedder
        table_embedder = TableEmbedder(device=settings.embedding_device)
        logger.info("Table embedder initialized")
        
        # Initialize formula embedder
        formula_embedder = FormulaEmbedder(device=settings.embedding_device)
        logger.info("Formula embedder initialized")
        
        # Start RabbitMQ consumer if enabled
        enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
        if enable_rabbitmq:
            logger.info("Starting RabbitMQ consumer")
            app.state.rabbitmq_consumer = AsyncEmbeddingServiceConsumer()
            app.state.rabbitmq_consumer.start_consuming_async()
            logger.info("RabbitMQ consumer started")
        
        logger.info("Embedding Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize embedders: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Embedding Service...")
    
    # Stop RabbitMQ consumer if running
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()
    
    # Cleanup embedders if needed
    logger.info("Embedding Service shut down")


# Create FastAPI app
app = FastAPI(
    title="Embedding Service",
    description="Generates embeddings for text, images, tables, and formulas",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Add custom middleware
app.middleware("http")(error_handler)
app.middleware("http")(auth_middleware)


@app.get("/health", response_model=EmbeddingHealthResponse)
async def health_check():
    """Health check endpoint"""
    return EmbeddingHealthResponse(
        status="healthy",
        service="embedding-service",
        model=settings.embedding_model,
        device=settings.embedding_device
    )


@app.post("/api/v1/embed/text", response_model=TextEmbeddingResponse)
async def embed_text(request: TextEmbeddingRequest):
    """
    Generate embeddings for text
    
    Args:
        request: Text embedding request with text and optional parameters
    
    Returns:
        TextEmbeddingResponse with embeddings vector and metadata
    """
    try:
        if text_embedder is None:
            raise HTTPException(status_code=503, detail="Text embedder not initialized")
        
        embeddings = await text_embedder.embed(
            text=request.text,
            model=request.model or settings.embedding_model
        )
        
        return TextEmbeddingResponse(
            embeddings=embeddings,
            model=request.model or settings.embedding_model,
            dimension=len(embeddings),
            text_length=len(request.text)
        )
        
    except Exception as e:
        logger.error(f"Error embedding text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/embed/text/batch", response_model=BatchTextEmbeddingResponse)
async def embed_text_batch(request: BatchTextEmbeddingRequest):
    """
    Generate embeddings for multiple texts in batch
    
    Args:
        request: Batch text embedding request with list of texts
    
    Returns:
        BatchTextEmbeddingResponse with list of embeddings
    """
    try:
        if text_embedder is None:
            raise HTTPException(status_code=503, detail="Text embedder not initialized")
        
        embeddings = await text_embedder.embed_batch(
            texts=request.texts,
            model=request.model or settings.embedding_model,
            batch_size=request.batch_size or settings.embedding_batch_size
        )
        
        return BatchTextEmbeddingResponse(
            embeddings=embeddings,
            model=request.model or settings.embedding_model,
            dimension=len(embeddings[0]) if embeddings else 0,
            count=len(embeddings)
        )
        
    except Exception as e:
        logger.error(f"Error embedding text batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/embed/image", response_model=ImageEmbeddingResponse)
async def embed_image(request: ImageEmbeddingRequest):
    """
    Generate embeddings for images
    
    Args:
        request: Image embedding request with image data
    
    Returns:
        ImageEmbeddingResponse with embeddings vector
    """
    try:
        if image_embedder is None:
            raise HTTPException(status_code=503, detail="Image embedder not initialized")
        
        embeddings = await image_embedder.embed(
            image_data=request.image_data,
            model=request.model
        )
        
        return ImageEmbeddingResponse(
            embeddings=embeddings,
            model=request.model or "default",
            dimension=len(embeddings)
        )
        
    except Exception as e:
        logger.error(f"Error embedding image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/embed/table", response_model=TableEmbeddingResponse)
async def embed_table(request: TableEmbeddingRequest):
    """
    Generate embeddings for tables
    
    Args:
        request: Table embedding request with table data
    
    Returns:
        TableEmbeddingResponse with embeddings vector
    """
    try:
        if table_embedder is None:
            raise HTTPException(status_code=503, detail="Table embedder not initialized")
        
        embeddings = await table_embedder.embed(
            table_data=request.table_data,
            model=request.model
        )
        
        return TableEmbeddingResponse(
            embeddings=embeddings,
            model=request.model or "default",
            dimension=len(embeddings)
        )
        
    except Exception as e:
        logger.error(f"Error embedding table: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/embed/formula")
async def embed_formula(formula: str, model: Optional[str] = None):
    """
    Generate embeddings for mathematical formulas
    
    Args:
        formula: Mathematical formula in LaTeX format
        model: Optional model name
    
    Returns:
        Formula embedding response
    """
    try:
        if formula_embedder is None:
            raise HTTPException(status_code=503, detail="Formula embedder not initialized")
        
        embeddings = await formula_embedder.embed(
            formula=formula,
            model=model
        )
        
        return {
            "embeddings": embeddings,
            "model": model or "default",
            "dimension": len(embeddings)
        }
        
    except Exception as e:
        logger.error(f"Error embedding formula: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/models")
async def list_models():
    """List available embedding models"""
    return {
        "text_models": [
            "BAAI/bge-m3",
            "intfloat/multilingual-e5-large",
            "sentence-transformers/all-MiniLM-L6-v2"
        ],
        "image_models": [
            "openai/clip-vit-base-patch32",
            "google/siglip-base-patch16-224"
        ],
        "table_models": [
            "table-transformer",
            "default"
        ],
        "formula_models": [
            "math-embedding",
            "default"
        ]
    }


@app.get("/api/v1/stats")
async def get_stats():
    """Get embedding service statistics"""
    return {
        "service": "embedding-service",
        "model": settings.embedding_model,
        "device": settings.embedding_device,
        "batch_size": settings.embedding_batch_size,
        "status": {
            "text_embedder": text_embedder is not None,
            "image_embedder": image_embedder is not None,
            "table_embedder": table_embedder is not None,
            "formula_embedder": formula_embedder is not None
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8006,
        reload=settings.debug,
        workers=1 if settings.debug else 4
    )