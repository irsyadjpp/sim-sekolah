"""
Generation Service - LLM integration with multiple providers
Supports OpenAI, Anthropic, and local models with citation and validation
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
from schemas.generation_schemas import (
    GenerationRequest,
    GenerationResponse,
    StreamingGenerationRequest,
    CitationGenerationRequest,
    CitationGenerationResponse,
    ValidationRequest,
    ValidationResponse,
    TemplateGenerationRequest,
    GenerationHealthResponse
)

from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.local_provider import LocalProvider
from prompts.prompt_manager import PromptManager
from citations.citation_system import CitationSystem
from validators.response_validator import ResponseValidator
from app.consumer import AsyncGenerationServiceConsumer

# Setup logging
logger = setup_logging(__name__)

# Global provider instances
openai_provider: Optional[OpenAIProvider] = None
anthropic_provider: Optional[AnthropicProvider] = None
local_provider: Optional[LocalProvider] = None
prompt_manager: Optional[PromptManager] = None
citation_system: Optional[CitationSystem] = None
response_validator: Optional[ResponseValidator] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global openai_provider, anthropic_provider, local_provider, prompt_manager, citation_system, response_validator
    
    # Startup
    logger.info("Starting Generation Service...")
    
    try:
        # Initialize OpenAI provider
        if settings.openai_api_key:
            openai_provider = OpenAIProvider(api_key=settings.openai_api_key)
            logger.info("OpenAI provider initialized")
        else:
            logger.warning("OpenAI API key not configured, skipping OpenAI provider")
        
        # Initialize Anthropic provider
        if settings.anthropic_api_key:
            anthropic_provider = AnthropicProvider(api_key=settings.anthropic_api_key)
            logger.info("Anthropic provider initialized")
        else:
            logger.warning("Anthropic API key not configured, skipping Anthropic provider")
        
        # Initialize local provider
        local_provider = LocalProvider(device=settings.embedding_device)
        logger.info("Local provider initialized")
        
        # Initialize prompt manager
        prompt_manager = PromptManager()
        logger.info("Prompt manager initialized")
        
        # Initialize citation system
        citation_system = CitationSystem()
        logger.info("Citation system initialized")
        
        # Initialize response validator
        response_validator = ResponseValidator()
        logger.info("Response validator initialized")
        
        # Start RabbitMQ consumer if enabled
        enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
        if enable_rabbitmq:
            logger.info("Starting RabbitMQ consumer")
            app.state.rabbitmq_consumer = AsyncGenerationServiceConsumer()
            app.state.rabbitmq_consumer.start_consuming_async()
            logger.info("RabbitMQ consumer started")
        
        logger.info("Generation Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize providers: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Generation Service...")
    
    # Stop RabbitMQ consumer if running
    enable_rabbitmq = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
    if enable_rabbitmq and hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer")
        app.state.rabbitmq_consumer.stop_consuming_async()
    
    # Cleanup providers if needed
    logger.info("Generation Service shut down")


# Create FastAPI app
app = FastAPI(
    title="Generation Service",
    description="LLM generation service with multiple providers and citation support",
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


@app.get("/health", response_model=GenerationHealthResponse)
async def health_check():
    """Health check endpoint"""
    return GenerationHealthResponse(
        status="healthy",
        service="generation-service",
        providers={
            "openai": openai_provider is not None,
            "anthropic": anthropic_provider is not None,
            "local": local_provider is not None
        }
    )


@app.post("/api/v1/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    """
    Generate text using specified LLM provider
    
    Args:
        request: Generation request with prompt and parameters
    
    Returns:
        GenerationResponse with generated text and metadata
    """
    try:
        provider = request.provider or "openai"
        
        # Select provider
        if provider == "openai" and openai_provider:
            response = await openai_provider.generate(
                prompt=request.prompt,
                model=request.model or "gpt-4",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        elif provider == "anthropic" and anthropic_provider:
            response = await anthropic_provider.generate(
                prompt=request.prompt,
                model=request.model or "claude-3-opus-20240229",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        elif provider == "local" and local_provider:
            response = await local_provider.generate(
                prompt=request.prompt,
                model=request.model or "default",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        else:
            raise HTTPException(status_code=400, detail=f"Provider {provider} not available")
        
        return GenerationResponse(
            text=response["text"],
            provider=provider,
            model=response.get("model", request.model or "unknown"),
            tokens_used=response.get("tokens_used", 0),
            latency_ms=response.get("latency_ms", 0)
        )
        
    except Exception as e:
        logger.error(f"Error in generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/generate/citations", response_model=CitationGenerationResponse)
async def generate_with_citations(request: CitationGenerationRequest):
    """
    Generate text with citations from retrieved documents
    
    Args:
        request: Citation generation request with context
    
    Returns:
        CitationGenerationResponse with generated text and citations
    """
    try:
        if citation_system is None:
            raise HTTPException(status_code=503, detail="Citation system not initialized")
        
        provider = request.provider or "openai"
        
        # Build prompt with citations
        cited_prompt = await citation_system.build_cited_prompt(
            prompt=request.prompt,
            context=request.context,
            documents=request.documents
        )
        
        # Generate response
        if provider == "openai" and openai_provider:
            response = await openai_provider.generate(
                prompt=cited_prompt,
                model=request.model or "gpt-4",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        elif provider == "anthropic" and anthropic_provider:
            response = await anthropic_provider.generate(
                prompt=cited_prompt,
                model=request.model or "claude-3-opus-20240229",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        else:
            raise HTTPException(status_code=400, detail=f"Provider {provider} not available")
        
        # Extract citations from response
        citations = await citation_system.extract_citations(
            response["text"],
            request.documents
        )
        
        return CitationGenerationResponse(
            text=response["text"],
            citations=citations,
            provider=provider,
            model=response.get("model", request.model),
            citation_count=len(citations)
        )
        
    except Exception as e:
        logger.error(f"Error in citation generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/validate", response_model=ValidationResponse)
async def validate_response(request: ValidationRequest):
    """
    Validate generated response for quality and accuracy
    
    Args:
        request: Validation request with response and context
    
    Returns:
        ValidationResponse with validation results
    """
    try:
        if response_validator is None:
            raise HTTPException(status_code=503, detail="Response validator not initialized")
        
        validation_result = await response_validator.validate(
            response=request.response,
            context=request.context,
            documents=request.documents
        )
        
        return ValidationResponse(
            is_valid=validation_result["is_valid"],
            confidence=validation_result["confidence"],
            issues=validation_result.get("issues", []),
            hallucination_score=validation_result.get("hallucination_score", 0.0),
            relevance_score=validation_result.get("relevance_score", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Error in validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/templates/generate")
async def generate_from_template(request: TemplateGenerationRequest):
    """
    Generate text using a prompt template
    
    Args:
        request: Template generation request
    
    Returns:
        Generated text using template
    """
    try:
        if prompt_manager is None:
            raise HTTPException(status_code=503, detail="Prompt manager not initialized")
        
        # Build prompt from template
        prompt = await prompt_manager.build_from_template(
            template_name=request.template_name,
            variables=request.variables
        )
        
        # Generate response
        provider = request.provider or "openai"
        if provider == "openai" and openai_provider:
            response = await openai_provider.generate(
                prompt=prompt,
                model=request.model or "gpt-4",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        elif provider == "anthropic" and anthropic_provider:
            response = await anthropic_provider.generate(
                prompt=prompt,
                model=request.model or "claude-3-opus-20240229",
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        else:
            raise HTTPException(status_code=400, detail=f"Provider {provider} not available")
        
        return {
            "text": response["text"],
            "template": request.template_name,
            "provider": provider,
            "model": response.get("model", request.model)
        }
        
    except Exception as e:
        logger.error(f"Error in template generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/providers")
async def list_providers():
    """List available LLM providers"""
    providers = []
    
    if openai_provider:
        providers.append({
            "name": "openai",
            "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "available": True
        })
    
    if anthropic_provider:
        providers.append({
            "name": "anthropic",
            "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
            "available": True
        })
    
    if local_provider:
        providers.append({
            "name": "local",
            "models": ["qwen", "mistral", "llama"],
            "available": True
        })
    
    return {"providers": providers}


@app.get("/api/v1/templates")
async def list_templates():
    """List available prompt templates"""
    if prompt_manager is None:
        return {"templates": []}
    
    return {"templates": await prompt_manager.list_templates()}


@app.get("/api/v1/stats")
async def get_stats():
    """Get generation service statistics"""
    return {
        "service": "generation-service",
        "providers": {
            "openai": openai_provider is not None,
            "anthropic": anthropic_provider is not None,
            "local": local_provider is not None
        },
        "components": {
            "prompt_manager": prompt_manager is not None,
            "citation_system": citation_system is not None,
            "response_validator": response_validator is not None
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8009,
        reload=settings.debug,
        workers=1 if settings.debug else 4
    )