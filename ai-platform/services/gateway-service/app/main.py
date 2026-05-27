from fastapi import FastAPI, Request, Response, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import time
from typing import Optional, Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Response as FastAPIResponse
import asyncio
import httpx

# Import shared components
import sys
sys.path.append('/app')
from shared.configs.settings import settings
from shared.logging.logger import setup_logging
from shared.security.jwt import verify_token
from shared.schemas.common import HealthResponse, ErrorResponse, BaseResponse
from shared.exceptions.exceptions import (
    AuthenticationError, 
    AuthorizationError, 
    RateLimitError,
    ServiceUnavailableError
)

# Setup logging
logger = setup_logging("gateway-service")

# Prometheus metrics
request_count = Counter(
    'gateway_requests_total', 
    'Total gateway requests',
    ['method', 'endpoint', 'status']
)
request_duration = Histogram(
    'gateway_request_duration_seconds', 
    'Request duration',
    ['method', 'endpoint']
)
active_connections = Gauge('gateway_active_connections', 'Active connections')

# Security
security = HTTPBearer()

# Service registry
SERVICES = {
    "parser": {"url": "http://parser-service:8008", "timeout": 30.0},
    "semantic-chunk": {"url": "http://semantic-chunk-service:8011", "timeout": 30.0},
    "metadata": {"url": "http://metadata-service:8004", "timeout": 30.0},
    "embedding": {"url": "http://embedding-service:8001", "timeout": 30.0},
    "retrieval": {"url": "http://retrieval-service:8010", "timeout": 30.0},
    "generation": {"url": "http://generation-service:8003", "timeout": 60.0},
    "audit": {"url": "http://audit-service:8000", "timeout": 30.0},
    "monitoring": {"url": "http://monitoring-service:8006", "timeout": 30.0},
}

# Rate limiting (simple in-memory, use Redis for production)
rate_limit_store: Dict[str, list] = {}
RATE_LIMIT_REQUESTS = settings.rate_limit_per_minute
RATE_LIMIT_WINDOW = 60  # seconds


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Gateway Service")
    active_connections.inc()
    yield
    logger.info("Shutting down Gateway Service")
    active_connections.dec()


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Gateway Service",
    description="API Gateway for Educational AI Platform",
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
            service: info["url"] 
            for service, info in SERVICES.items()
        }
    )


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return FastAPIResponse(content=generate_latest(), media_type="text/plain")


# Rate limiting middleware
async def check_rate_limit(client_id: str):
    """Check if client has exceeded rate limit"""
    current_time = time.time()
    
    # Clean old requests
    if client_id in rate_limit_store:
        rate_limit_store[client_id] = [
            timestamp for timestamp in rate_limit_store[client_id]
            if current_time - timestamp < RATE_LIMIT_WINDOW
        ]
    else:
        rate_limit_store[client_id] = []
    
    # Check if limit exceeded
    if len(rate_limit_store[client_id]) >= RATE_LIMIT_REQUESTS:
        raise RateLimitError(f"Rate limit exceeded: {RATE_LIMIT_REQUESTS} requests per minute")
    
    # Add current request
    rate_limit_store[client_id].append(current_time)


# Authentication dependency
async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = verify_token(credentials.credentials, "access")
        if payload is None:
            raise AuthenticationError("Invalid token")
        return payload
    except Exception as e:
        raise AuthenticationError(f"Authentication failed: {str(e)}")


# Service proxy endpoints
@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_service(
    service: str,
    path: str,
    request: Request,
    auth_payload: Optional[Dict[str, Any]] = Depends(verify_jwt if not settings.debug else None)
):
    """Proxy requests to appropriate service"""
    
    start_time = time.time()
    method = request.method
    endpoint = f"/{service}/{path}"
    client_id = request.client.host if request.client else "unknown"
    
    try:
        # Check rate limit
        await check_rate_limit(client_id)
        
        # Validate service
        if service not in SERVICES:
            raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
        
        service_config = SERVICES[service]
        service_url = f"{service_config['url']}/{path}"
        
        # Prepare request headers
        headers = dict(request.headers)
        headers["X-User-ID"] = str(auth_payload.get("user_id", "anonymous")) if auth_payload else "anonymous"
        headers["X-Request-ID"] = request.state.request_id if hasattr(request.state, "request_id") else ""
        
        # Prepare request body
        body = await request.body()
        
        # Proxy request to service
        async with httpx.AsyncClient(timeout=service_config["timeout"]) as client:
            response = await client.request(
                method=method,
                url=service_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
        
        # Record metrics
        request_count.labels(method=method, endpoint=endpoint, status=response.status_code).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
        
        # Return response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except RateLimitError as e:
        request_count.labels(method=method, endpoint=endpoint, status=429).inc()
        logger.warning(f"Rate limit exceeded for client {client_id}")
        raise HTTPException(status_code=429, detail=str(e))
        
    except httpx.TimeoutException:
        request_count.labels(method=method, endpoint=endpoint, status=504).inc()
        logger.error(f"Timeout proxying to service {service}")
        raise HTTPException(status_code=504, detail="Service timeout")
        
    except httpx.ConnectError:
        request_count.labels(method=method, endpoint=endpoint, status=503).inc()
        logger.error(f"Failed to connect to service {service}")
        raise HTTPException(status_code=503, detail=f"Service '{service}' unavailable")
        
    except Exception as e:
        request_count.labels(method=method, endpoint=endpoint, status=500).inc()
        logger.error(f"Error proxying request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# API aggregation endpoints
@app.get("/api/v1/aggregate")
async def aggregate_requests(
    requests: list[Dict[str, Any]],
    auth_payload: Optional[Dict[str, Any]] = Depends(verify_jwt if not settings.debug else None)
):
    """Aggregate multiple service requests into a single response"""
    
    results = []
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for req in requests:
            service = req.get("service")
            path = req.get("path")
            method = req.get("method", "GET")
            
            if service not in SERVICES:
                results.append({
                    "service": service,
                    "error": f"Service '{service}' not found"
                })
                continue
            
            service_url = f"{SERVICES[service]['url']}/{path}"
            tasks.append(client.request(method, service_url))
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                results.append({
                    "service": requests[i].get("service"),
                    "error": str(response)
                })
            else:
                results.append({
                    "service": requests[i].get("service"),
                    "status": response.status_code,
                    "data": response.json() if response.content else None
                })
    
    return BaseResponse(
        success=True,
        data={"results": results}
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
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
async def general_exception_handler(request: Request, exc: Exception):
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
        host=settings.gateway_host,
        port=settings.gateway_port,
        workers=settings.gateway_workers,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )