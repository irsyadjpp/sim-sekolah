"""
Configuration Settings for Monolith Architecture
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "AI Platform - Monolith"
    app_version: str = "2.0.0"
    debug: bool = True
    environment: str = "development"
    
    # CORS
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Database
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "ai_user"
    database_password: str = "ai_password"
    database_name: str = "ai_platform"
    database_url: str = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
    
    # Vector Database (Qdrant)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_url: str = f"http://{qdrant_host}:{qdrant_port}"
    
    # Object Storage
    storage_endpoint: str = "localhost"
    storage_port: int = 8333
    storage_access_key: str = "admin"
    storage_secret_key: str = "admin"
    
    # AI Models
    embedding_model: str = "BAAI/bge-m3"
    generation_model: str = "gpt-4"
    use_local_models: bool = False
    
    # Processing
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    chunk_size: int = 512
    chunk_overlap: int = 50
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()