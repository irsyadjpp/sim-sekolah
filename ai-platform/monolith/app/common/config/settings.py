from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    @validator('debug', pre=True, always=True)
    def parse_debug(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return bool(v)
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_host: str = Field(default="localhost", env="DATABASE_HOST")
    database_port: int = Field(default=5432, env="DATABASE_PORT")
    database_name: str = Field(default="ai_platform", env="DATABASE_NAME")
    database_user: str = Field(default="ai_user", env="DATABASE_USER")
    database_password: str = Field(default="ai_password", env="DATABASE_PASSWORD")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # RabbitMQ
    rabbitmq_url: str = Field(default="amqp://admin:admin@localhost:5672", env="RABBITMQ_URL")
    rabbitmq_host: str = Field(default="localhost", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(default="admin", env="RABBITMQ_USER")
    rabbitmq_password: str = Field(default="admin", env="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field(default="/", env="RABBITMQ_VHOST")
    
    # Qdrant
    qdrant_url: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    qdrant_host: str = Field(default="localhost", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")
    qdrant_api_key: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    
    # SeaweedFS S3
    seaweedfs_s3_endpoint: str = Field(default="localhost:8333", env="SEAWEDFS_S3_ENDPOINT")
    seaweedfs_access_key: str = Field(default="admin", env="SEAWEDFS_ACCESS_KEY")
    seaweedfs_secret_key: str = Field(default="admin", env="SEAWEDFS_SECRET_KEY")
    seaweedfs_secure: bool = Field(default=False, env="SEAWEDFS_SECURE")
    seaweedfs_bucket: str = Field(default="ai-platform-documents", env="SEAWEDFS_BUCKET")
    seaweedfs_region: str = Field(default="us-east-1", env="SEAWEDFS_REGION")
    
    # JWT
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_minutes: int = Field(default=30, env="JWT_EXPIRATION_MINUTES")
    jwt_refresh_expiration_days: int = Field(default=7, env="JWT_REFRESH_EXPIRATION_DAYS")
    
    # Gateway
    gateway_host: str = Field(default="0.0.0.0", env="GATEWAY_HOST")
    gateway_port: int = Field(default=8002, env="GATEWAY_PORT")
    gateway_workers: int = Field(default=4, env="GATEWAY_WORKERS")
    
    # Monitoring
    prometheus_url: str = Field(default="http://localhost:9090", env="PROMETHEUS_URL")
    grafana_url: str = Field(default="http://localhost:3000", env="GRAFANA_URL")
    loki_url: str = Field(default="http://localhost:3100", env="LOKI_URL")
    tempo_url: str = Field(default="http://localhost:3100", env="TEMPO_URL")
    
    # OpenTelemetry
    otel_exporter_otlp_endpoint: str = Field(default="http://localhost:4317", env="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_service_name: str = Field(default="ai-platform", env="OTEL_SERVICE_NAME")
    otel_resource_attributes: str = Field(default="environment=development", env="OTEL_RESOURCE_ATTRIBUTES")
    
    # AI Models
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Embedding
    embedding_model: str = Field(default="BAAI/bge-m3", env="EMBEDDING_MODEL")
    embedding_device: str = Field(default="cuda", env="EMBEDDING_DEVICE")
    embedding_batch_size: int = Field(default=32, env="EMBEDDING_BATCH_SIZE")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # File Upload
    max_file_size: str = Field(default="100MB", env="MAX_FILE_SIZE")
    allowed_file_types: str = Field(default="pdf,doc,docx,txt,images", env="ALLOWED_FILE_TYPES")
    
    # CORS
    cors_origins: str = Field(default="*", env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: str = Field(default="GET,POST,PUT,DELETE,OPTIONS", env="CORS_ALLOW_METHODS")
    cors_allow_headers: str = Field(default="Authorization,Content-Type,X-Requested-With", env="CORS_ALLOW_HEADERS")
    
    # Cache
    cache_ttl_seconds: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Monitoring Toggle
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    tracing_enabled: bool = Field(default=True, env="TRACING_ENABLED")
    logging_enabled: bool = Field(default=True, env="LOGGING_ENABLED")
    
    # Security
    encryption_key: str = Field(default="", env="ENCRYPTION_KEY")
    security_headers_enabled: bool = Field(default=True, env="SECURITY_HEADERS_ENABLED")
    https_enabled: bool = Field(default=False, env="HTTPS_ENABLED")
    
    @validator('cors_origins')
    def parse_cors_origins(cls, v):
        if v == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",")]
    
    @validator('allowed_file_types')
    def parse_allowed_file_types(cls, v):
        return [file_type.strip().lower() for file_type in v.split(",")]
    
    @validator('cors_allow_methods')
    def parse_cors_allow_methods(cls, v):
        return [method.strip().upper() for method in v.split(",")]
    
    @validator('cors_allow_headers')
    def parse_cors_allow_headers(cls, v):
        return [header.strip() for header in v.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()