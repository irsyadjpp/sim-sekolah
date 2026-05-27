"""
Retrieval Service - Semantic and hybrid search with Qdrant
Supports metadata filtering, query expansion, and relevance scoring
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
from schemas.retrieval_schemas import (
    SemanticSearchRequest,
    SemanticSearchResponse,
    HybridSearchRequest,
    HybridSearchResponse,
    MetadataFilterRequest,
    MetadataFilterResponse,
    QueryBuilderRequest,
    QueryBuilderResponse,
    ContextBuilderRequest,
    ContextBuilderResponse,
    RetrievalHealthResponse
)

from retrievers.semantic_retriever import SemanticRetriever
from retrievers.hybrid_retriever import HybridRetriever
from retrievers.metadata_retriever import MetadataRetriever
from query_builders.query_builder import QueryBuilder
from context_builders.context_builder import ContextBuilder
from app.consumer import AsyncRetrievalServiceConsumer

# Setup logging
logger = setup_logging(__name__)

# Global retriever instances
semantic_retriever: Optional[SemanticRetriever] = None
hybrid_retriever: Optional[HybridRetriever] = None
metadata_retriever: Optional[MetadataRetriever] = None
query_builder: Optional[QueryBuilder] = None
context_builder: Optional[ContextBuilder] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global semantic_retriever, hybrid_retriever, metadata_retriever, query_builder, context_builder
    
    # Startup
    logger.info("Starting Retrieval Service...")
    
    try:
        # Initialize semantic retriever
        semantic_retriever = SemanticRetriever(
            qdrant_url=settings.qdrant_url,
            qdrant_api_key=settings.qdrant_api_key
        )
        logger.info("Semantic retriever initialized")
        
        # Initialize hybrid retriever
        hybrid_retriever = HybridRetriever(
            qdrant_url=settings.qdrant_url,
            qdrant_api_key=settings.qdrant_api_key
        )
        logger.info("Hybrid retriever initialized")
        
        # Initialize metadata retriever
        metadata_retriever = MetadataRetriever(
            qdrant_url=settings.qdrant_url,
            qdrant_api_key=settings.qdrant_api_key
        )
        logger.info("Metadata retriever initialized")
        
        # Initialize query builder
        query_builder = QueryBuilder()
        logger.info("Query builder initialized")
        
        # Initialize context builder
        context_builder = ContextBuilder()
        logger.info("Context builder initialized")
        
        # Start RabbitMQ consumer if enabled
        enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
        if enable_rabbitmq:
            logger.info("Starting RabbitMQ consumer")
            app.state.rabbitmq_consumer = AsyncRetrievalServiceConsumer()
            app.state.rabbitmq_consumer.start_consuming_async()
            logger.info("RabbitMQ consumer started")
        
        logger.info("Retrieval Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize retrievers: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Retrieval Service...")
    
    # Stop RabbitMQ consumer if running
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()
    
    # Cleanup retrievers if needed
    logger.info("Retrieval Service shut down")


# Create FastAPI app
app = FastAPI(
    title="Retrieval Service",
    description="Semantic and hybrid search with Qdrant vector database",
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


@app.get("/health", response_model=RetrievalHealthResponse)
async def health_check():
    """Health check endpoint"""
    return RetrievalHealthResponse(
        status="healthy",
        service="retrieval-service",
        qdrant_url=settings.qdrant_url
    )


@app.post("/api/v1/search/semantic", response_model=SemanticSearchResponse)
async def semantic_search(request: SemanticSearchRequest):
    """
    Perform semantic search using vector embeddings
    
    Args:
        request: Semantic search request with query and parameters
    
    Returns:
        SemanticSearchResponse with ranked results
    """
    try:
        if semantic_retriever is None:
            raise HTTPException(status_code=503, detail="Semantic retriever not initialized")
        
        results = await semantic_retriever.search(
            query=request.query,
            collection_name=request.collection_name,
            limit=request.limit,
            score_threshold=request.score_threshold,
            filters=request.filters
        )
        
        return SemanticSearchResponse(
            results=results,
            query=request.query,
            total=len(results),
            latency_ms=0  # TODO: implement latency tracking
        )
        
    except Exception as e:
        logger.error(f"Error in semantic search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/search/hybrid", response_model=HybridSearchResponse)
async def hybrid_search(request: HybridSearchRequest):
    """
    Perform hybrid search combining semantic and keyword search
    
    Args:
        request: Hybrid search request with query and weights
    
    Returns:
        HybridSearchResponse with ranked results
    """
    try:
        if hybrid_retriever is None:
            raise HTTPException(status_code=503, detail="Hybrid retriever not initialized")
        
        results = await hybrid_retriever.search(
            query=request.query,
            collection_name=request.collection_name,
            semantic_weight=request.semantic_weight,
            keyword_weight=request.keyword_weight,
            limit=request.limit,
            filters=request.filters
        )
        
        return HybridSearchResponse(
            results=results,
            query=request.query,
            total=len(results),
            weights={
                "semantic": request.semantic_weight,
                "keyword": request.keyword_weight
            },
            latency_ms=0  # TODO: implement latency tracking
        )
        
    except Exception as e:
        logger.error(f"Error in hybrid search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/search/metadata", response_model=MetadataFilterResponse)
async def metadata_search(request: MetadataFilterRequest):
    """
    Perform search with metadata filtering
    
    Args:
        request: Metadata filter request with filters
    
    Returns:
        MetadataFilterResponse with filtered results
    """
    try:
        if metadata_retriever is None:
            raise HTTPException(status_code=503, detail="Metadata retriever not initialized")
        
        results = await metadata_retriever.search(
            collection_name=request.collection_name,
            filters=request.filters,
            limit=request.limit,
            order_by=request.order_by
        )
        
        return MetadataFilterResponse(
            results=results,
            total=len(results),
            filters=request.filters
        )
        
    except Exception as e:
        logger.error(f"Error in metadata search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/query/build", response_model=QueryBuilderResponse)
async def build_query(request: QueryBuilderRequest):
    """
    Build optimized query with expansion and transformation
    
    Args:
        request: Query builder request
    
    Returns:
        QueryBuilderResponse with optimized query
    """
    try:
        if query_builder is None:
            raise HTTPException(status_code=503, detail="Query builder not initialized")
        
        optimized_query = await query_builder.build(
            query=request.query,
            expansion_method=request.expansion_method,
            num_expansions=request.num_expansions
        )
        
        return QueryBuilderResponse(
            original_query=request.query,
            optimized_query=optimized_query,
            expansions=optimized_query.get("expansions", []),
            method=request.expansion_method
        )
        
    except Exception as e:
        logger.error(f"Error building query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/context/build", response_model=ContextBuilderResponse)
async def build_context(request: ContextBuilderRequest):
    """
    Build context from retrieved documents for LLM generation
    
    Args:
        request: Context builder request with documents
    
    Returns:
        ContextBuilderResponse with formatted context
    """
    try:
        if context_builder is None:
            raise HTTPException(status_code=503, detail="Context builder not initialized")
        
        context = await context_builder.build(
            documents=request.documents,
            max_tokens=request.max_tokens,
            strategy=request.strategy
        )
        
        return ContextBuilderResponse(
            context=context,
            document_count=len(request.documents),
            token_count=len(context.split()),  # Rough estimate
            strategy=request.strategy
        )
        
    except Exception as e:
        logger.error(f"Error building context: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/collections")
async def list_collections():
    """List available collections in Qdrant"""
    try:
        if semantic_retriever is None:
            raise HTTPException(status_code=503, detail="Semantic retriever not initialized")
        
        collections = await semantic_retriever.list_collections()
        
        return {
            "collections": collections,
            "count": len(collections)
        }
        
    except Exception as e:
        logger.error(f"Error listing collections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats")
async def get_stats():
    """Get retrieval service statistics"""
    return {
        "service": "retrieval-service",
        "qdrant_url": settings.qdrant_url,
        "status": {
            "semantic_retriever": semantic_retriever is not None,
            "hybrid_retriever": hybrid_retriever is not None,
            "metadata_retriever": metadata_retriever is not None,
            "query_builder": query_builder is not None,
            "context_builder": context_builder is not None
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=settings.debug,
        workers=1 if settings.debug else 4
    )