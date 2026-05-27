"""
Pytest configuration for integration tests
"""

import asyncio
import os
import pytest
import logging
from pathlib import Path
from typing import AsyncGenerator, Generator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "contract: marks tests as contract tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "grpc: marks tests as gRPC tests"
    )
    config.addinivalue_line(
        "markers", "http: marks tests as HTTP tests"
    )


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Test environment: test, staging, production"
    )
    parser.addoption(
        "--skip-services",
        action="store",
        default="",
        help="Comma-separated list of services to skip"
    )
    parser.addoption(
        "--service-host",
        action="store",
        default="localhost",
        help="Default service host"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    env = config.getoption("--env")
    skip_services = config.getoption("--skip-services")
    
    if skip_services:
        skip_list = [s.strip() for s in skip_services.split(",")]
        
        for item in items:
            for service in skip_list:
                if service in item.nodeid:
                    item.add_marker(
                        pytest.mark.skip(reason=f"Skipping {service} service")
                    )


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_config(request):
    """Get test configuration."""
    env = request.config.getoption("--env")
    service_host = request.config.getoption("--service-host")
    
    return {
        "env": env,
        "service_host": service_host,
        "timeout": int(os.getenv("TEST_TIMEOUT", "30")),
        "fixtures_path": Path(os.getenv("TEST_FIXTURES_PATH", "./tests/fixtures")),
    }


@pytest.fixture(scope="function")
def test_data_dir(test_config):
    """Get test data directory."""
    return test_config["fixtures_path"]


@pytest.fixture(scope="function")
async def cleanup_test_data():
    """Cleanup test data after each test."""
    yield
    
    # Add cleanup logic here
    # This could involve:
    # - Deleting test documents
    # - Cleaning up test users
    # - Removing test embeddings
    # - Clearing test databases
    pass


# Service configuration fixtures
@pytest.fixture(scope="session")
def document_service_config(test_config):
    """Document service configuration."""
    return {
        "host": os.getenv("DOCUMENT_SERVICE_HOST", test_config["service_host"]),
        "port": int(os.getenv("DOCUMENT_SERVICE_PORT", "50051")),
        "timeout": test_config["timeout"],
    }


@pytest.fixture(scope="session")
def embedding_service_config(test_config):
    """Embedding service configuration."""
    return {
        "host": os.getenv("EMBEDDING_SERVICE_HOST", test_config["service_host"]),
        "port": int(os.getenv("EMBEDDING_SERVICE_PORT", "50052")),
        "timeout": test_config["timeout"],
    }


@pytest.fixture(scope="session")
def retrieval_service_config(test_config):
    """Retrieval service configuration."""
    return {
        "host": os.getenv("RETRIEVAL_SERVICE_HOST", test_config["service_host"]),
        "port": int(os.getenv("RETRIEVAL_SERVICE_PORT", "50053")),
        "timeout": test_config["timeout"],
    }


@pytest.fixture(scope="session")
def generation_service_config(test_config):
    """Generation service configuration."""
    return {
        "host": os.getenv("GENERATION_SERVICE_HOST", test_config["service_host"]),
        "port": int(os.getenv("GENERATION_SERVICE_PORT", "50054")),
        "timeout": test_config["timeout"],
    }


# Storage configuration fixtures
@pytest.fixture(scope="session")
def postgres_config():
    """PostgreSQL configuration for tests."""
    from storage.abstractions import StorageConfig
    
    return StorageConfig(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        username=os.getenv("POSTGRES_USERNAME", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        database=os.getenv("POSTGRES_DATABASE", "ai_platform_test"),
    )


@pytest.fixture(scope="session")
def qdrant_config():
    """Qdrant configuration for tests."""
    from storage.abstractions import StorageConfig
    
    return StorageConfig(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", "6333")),
    )


@pytest.fixture(scope="session")
def neo4j_config():
    """Neo4j configuration for tests."""
    from storage.abstractions import StorageConfig
    
    return StorageConfig(
        host=os.getenv("NEO4J_HOST", "localhost"),
        port=int(os.getenv("NEO4J_PORT", "7687")),
        username=os.getenv("NEO4J_USERNAME", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "password"),
        database=os.getenv("NEO4J_DATABASE", "neo4j"),
    )


# Async storage client fixtures
@pytest.fixture(scope="function")
async def postgres_client(postgres_config):
    """PostgreSQL client for tests."""
    from storage.abstractions import PostgreSQL
    
    async with PostgreSQL(postgres_config) as client:
        yield client


@pytest.fixture(scope="function")
async def qdrant_client(qdrant_config):
    """Qdrant client for tests."""
    from storage.abstractions import QdrantDB
    
    async with QdrantDB(qdrant_config) as client:
        yield client


@pytest.fixture(scope="function")
async def neo4j_client(neo4j_config):
    """Neo4j client for tests."""
    from storage.abstractions import Neo4jDB
    
    async with Neo4jDB(neo4j_config) as client:
        yield client


# Test data fixtures
@pytest.fixture(scope="function")
def sample_document():
    """Sample document for testing."""
    return {
        "title": "Test Document",
        "content": "This is a test document for integration testing.",
        "file_type": "txt",
        "metadata": {
            "source": "test",
            "category": "test"
        }
    }


@pytest.fixture(scope="function")
def sample_user():
    """Sample user for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "role": "user"
    }


@pytest.fixture(scope="function")
def sample_query():
    """Sample query for testing."""
    return {
        "text": "What is the main topic of the document?",
        "max_results": 5,
        "min_score": 0.7
    }