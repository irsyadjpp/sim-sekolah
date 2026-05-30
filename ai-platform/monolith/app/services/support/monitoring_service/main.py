from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry
from prometheus_client.core import GaugeMetricFamily
import httpx
import redis
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

# Import shared components
import sys
sys.path.append('/app')
from common.config.settings import settings
from common.logging.logger import setup_logging
from common.schemas.common import HealthResponse, BaseResponse, ErrorResponse

# Setup logging
logger = setup_logging("monitoring-service")

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis setup
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# Prometheus metrics
registry = CollectorRegistry()

# Custom metrics
request_metrics = Counter(
    'monitoring_service_requests_total',
    'Total monitoring service requests',
    ['endpoint', 'method'],
    registry=registry
)

service_health_gauge = Gauge(
    'service_health_status',
    'Health status of services',
    ['service'],
    registry=registry
)

system_metrics_gauge = Gauge(
    'system_metrics',
    'System metrics',
    ['metric_type'],
    registry=registry
)

response_time_histogram = Histogram(
    'monitoring_service_response_time_seconds',
    'Response time in seconds',
    ['endpoint'],
    registry=registry
)


class ServiceHealthCollector:
    """Custom collector for service health metrics"""
    
    def __init__(self):
        self.services = {
            "gateway": "http://gateway-service:8002",
            "parser": "http://parser-service:8008",
            "semantic-chunk": "http://semantic-chunk-service:8011",
            "metadata": "http://metadata-service:8004",
            "embedding": "http://embedding-service:8001",
            "retrieval": "http://retrieval-service:8010",
            "generation": "http://generation-service:8003",
            "audit": "http://audit-service:8000",
        }
    
    def collect(self):
        """Collect health metrics for all services"""
        for service_name, service_url in self.services.items():
            try:
                # Check service health
                health_status = asyncio.run(self.check_service_health(service_url))
                gauge = GaugeMetricFamily(
                    f'service_health_status',
                    'Health status of services',
                    labels=['service']
                )
                gauge.add_metric([service_name], health_status)
                yield gauge
            except Exception as e:
                logger.error(f"Error collecting metrics for {service_name}: {str(e)}")
    
    async def check_service_health(self, service_url: str) -> float:
        """Check health of a single service"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service_url}/health")
                if response.status_code == 200:
                    return 1.0  # Healthy
                else:
                    return 0.0  # Unhealthy
        except Exception:
            return 0.0  # Unhealthy


# Register custom collector
registry.register(ServiceHealthCollector())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Monitoring Service")
    yield
    logger.info("Shutting down Monitoring Service")


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Monitoring Service",
    description="Monitoring and observability service for AI Platform",
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
            "prometheus": settings.prometheus_url,
            "grafana": settings.grafana_url,
            "redis": settings.redis_url,
            "database": settings.database_url
        }
    )


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from fastapi.responses import Response
    return Response(content=generate_latest(registry), media_type="text/plain")


# Service health check endpoint
@app.get("/api/v1/services/health")
async def check_services_health():
    """Check health of all services"""
    
    services_status = {}
    services = {
        "gateway": "http://gateway-service:8002",
        "parser": "http://parser-service:8008",
        "semantic-chunk": "http://semantic-chunk-service:8011",
        "metadata": "http://metadata-service:8004",
        "embedding": "http://embedding-service:8001",
        "retrieval": "http://retrieval-service:8010",
        "generation": "http://generation-service:8003",
        "audit": "http://audit-service:8000",
    }
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for service_name, service_url in services.items():
            tasks.append(check_single_service(client, service_name, service_url))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict):
                services_status.update(result)
    
    return BaseResponse(
        success=True,
        data={"services": services_status}
    )


async def check_single_service(client: httpx.AsyncClient, service_name: str, service_url: str) -> Dict[str, Any]:
    """Check health of a single service"""
    try:
        response = await client.get(f"{service_url}/health", timeout=5.0)
        return {
            service_name: {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code
            }
        }
    except Exception as e:
        return {
            service_name: {
                "status": "unreachable",
                "error": str(e)
            }
        }


# System metrics endpoint
@app.get("/api/v1/system/metrics")
async def get_system_metrics():
    """Get system metrics"""
    
    try:
        # Get system metrics from Prometheus
        async with httpx.AsyncClient() as client:
            prometheus_response = await client.get(
                f"{settings.prometheus_url}/api/v1/query",
                params={"query": "up"},
                timeout=10.0
            )
            
            if prometheus_response.status_code == 200:
                prometheus_data = prometheus_response.json()
            else:
                prometheus_data = {}
    except Exception as e:
        logger.error(f"Error fetching Prometheus metrics: {str(e)}")
        prometheus_data = {}
    
    # Get Redis metrics
    redis_metrics = {}
    try:
        redis_info = redis_client.info()
        redis_metrics = {
            "connected_clients": redis_info.get("connected_clients", 0),
            "used_memory_human": redis_info.get("used_memory_human", "0B"),
            "uptime_in_seconds": redis_info.get("uptime_in_seconds", 0),
            "total_connections_received": redis_info.get("total_connections_received", 0)
        }
    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {str(e)}")
    
    # Get database metrics
    db_metrics = {}
    try:
        session = SessionLocal()
        result = session.execute(text("SELECT version()"))
        db_version = result.scalar()
        db_metrics = {
            "version": db_version,
            "status": "connected"
        }
        session.close()
    except Exception as e:
        logger.error(f"Error fetching database metrics: {str(e)}")
        db_metrics = {"status": "error", "error": str(e)}
    
    return BaseResponse(
        success=True,
        data={
            "prometheus": prometheus_data,
            "redis": redis_metrics,
            "database": db_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Custom metrics aggregation endpoint
@app.get("/api/v1/metrics/custom")
async def get_custom_metrics(
    metric_name: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    """Get custom metrics from Prometheus"""
    
    try:
        async with httpx.AsyncClient() as client:
            # Build query
            query = metric_name if metric_name else "up"
            
            params = {"query": query}
            if start_time:
                params["start"] = start_time
            if end_time:
                params["end"] = end_time
            
            response = await client.get(
                f"{settings.prometheus_url}/api/v1/query_range",
                params=params,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return BaseResponse(
                    success=True,
                    data=data
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error fetching metrics: {response.text}"
                )
                
    except Exception as e:
        logger.error(f"Error fetching custom metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Alert rules endpoint
@app.get("/api/v1/alerts")
async def get_alerts():
    """Get current alerts from Prometheus"""
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.prometheus_url}/api/v1/alerts",
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return BaseResponse(
                    success=True,
                    data=data
                )
            else:
                return BaseResponse(
                    success=True,
                    data={"alerts": []}
                )
                
    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}")
        return BaseResponse(
            success=True,
            data={"alerts": []}
        )


# Performance metrics endpoint
@app.get("/api/v1/performance")
async def get_performance_metrics():
    """Get performance metrics for analysis"""
    
    try:
        async with httpx.AsyncClient() as client:
            # Get request rate
            rate_response = await client.get(
                f"{settings.prometheus_url}/api/v1/query",
                params={"query": 'rate(gateway_requests_total[5m])'},
                timeout=10.0
            )
            
            # Get error rate
            error_response = await client.get(
                f"{settings.prometheus_url}/api/v1/query",
                params={"query": 'rate(gateway_requests_total{status=~"5.."}[5m])'},
                timeout=10.0
            )
            
            # Get latency
            latency_response = await client.get(
                f"{settings.prometheus_url}/api/v1/query",
                params={"query": 'histogram_quantile(0.95, gateway_request_duration_seconds)'},
                timeout=10.0
            )
            
            return BaseResponse(
                success=True,
                data={
                    "request_rate": rate_response.json() if rate_response.status_code == 200 else {},
                    "error_rate": error_response.json() if error_response.status_code == 200 else {},
                    "latency_p95": latency_response.json() if latency_response.status_code == 200 else {},
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
    except Exception as e:
        logger.error(f"Error fetching performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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
        host="0.0.0.0",
        port=8006,
        workers=1,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )