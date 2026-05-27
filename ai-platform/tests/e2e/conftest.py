"""
Pytest configuration for end-to-end tests
"""

import pytest
import os
import asyncio
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pytest_configure(config):
    """Configure pytest with E2E-specific markers."""
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "workflow: marks tests as workflow tests"
    )
    config.addinivalue_line(
        "markers", "scenario: marks tests as user scenario tests"
    )


def pytest_addoption(parser):
    """Add custom command line options for E2E tests."""
    parser.addoption(
        "--e2e-timeout",
        action="store",
        default="300",
        help="Default timeout for E2E tests in seconds"
    )
    parser.addoption(
        "--e2e-retry-count",
        action="store",
        default="3",
        help="Number of retries for failed E2E tests"
    )
    parser.addoption(
        "--skip-cleanup",
        action="store_true",
        help="Skip cleanup after E2E tests (useful for debugging)"
    )
    parser.addoption(
        "--test-data-dir",
        action="store",
        default="./tests/e2e/data",
        help="Directory for E2E test data"
    )


@pytest.fixture(scope="session")
def e2e_config(request):
    """Get E2E test configuration."""
    return {
        "timeout": int(request.config.getoption("--e2e-timeout")),
        "retry_count": int(request.config.getoption("--e2e-retry-count")),
        "skip_cleanup": request.config.getoption("--skip-cleanup"),
        "test_data_dir": Path(request.config.getoption("--test-data-dir")),
        "service_urls": {
            "document": os.getenv("DOCUMENT_SERVICE_URL", "http://localhost:50051"),
            "embedding": os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:50052"),
            "retrieval": os.getenv("RETRIEVAL_SERVICE_URL", "http://localhost:50053"),
            "generation": os.getenv("GENERATION_SERVICE_URL", "http://localhost:50054"),
            "guard": os.getenv("GUARD_SERVICE_URL", "http://localhost:50055"),
        },
        "storage_urls": {
            "postgres": os.getenv("POSTGRES_URL", "postgresql://localhost:5432/ai_platform_test"),
            "qdrant": os.getenv("QDRANT_URL", "http://localhost:6333"),
            "neo4j": os.getenv("NEO4J_URL", "bolt://localhost:7687"),
        }
    }


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async E2E tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_data(e2e_config):
    """Get test data directory."""
    data_dir = e2e_config["test_data_dir"]
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


@pytest.fixture(scope="function")
async def e2e_cleanup(e2e_config):
    """
    Cleanup fixture for E2E tests.
    
    Automatically cleans up test data after each test unless --skip-cleanup is used.
    """
    cleanup_resources = []
    
    async def add_cleanup(cleanup_func):
        """Add a cleanup function to be executed after the test."""
        cleanup_resources.append(cleanup_func)
    
    yield add_cleanup
    
    if not e2e_config["skip_cleanup"]:
        for cleanup_func in cleanup_resources:
            try:
                await cleanup_func()
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")


@pytest.fixture(scope="session")
async def service_health_check(e2e_config):
    """
    Check that all required services are healthy before running E2E tests.
    
    This fixture runs once at the beginning of the test session.
    """
    import httpx
    
    unhealthy_services = []
    
    # Check HTTP services
    for service_name, url in e2e_config["service_urls"].items():
        if url.startswith("http://") or url.startswith("https://"):
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(f"{url}/health")
                    if response.status_code != 200:
                        unhealthy_services.append(service_name)
            except Exception as e:
                logger.warning(f"Service {service_name} health check failed: {e}")
                unhealthy_services.append(service_name)
    
    # Check storage services
    for storage_name, url in e2e_config["storage_urls"].items():
        try:
            if storage_name == "postgres":
                # Check PostgreSQL connection
                import asyncpg
                conn = await asyncpg.connect(url)
                await conn.close()
            elif storage_name == "qdrant":
                # Check Qdrant connection
                import httpx
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(f"{url}/collections")
                    if response.status_code != 200:
                        unhealthy_services.append(storage_name)
            elif storage_name == "neo4j":
                # Check Neo4j connection
                from neo4j import GraphDatabase
                driver = GraphDatabase.driver(url)
                driver.verify_connectivity()
                driver.close()
        except Exception as e:
            logger.warning(f"Storage {storage_name} health check failed: {e}")
            unhealthy_services.append(storage_name)
    
    if unhealthy_services:
        pytest.fail(
            f"The following services/storage are unhealthy: {', '.join(unhealthy_services)}. "
            "Please start all required services before running E2E tests."
        )


# Test user fixtures
@pytest.fixture(scope="function")
def test_student_user():
    """Create a test student user."""
    return {
        "user_id": "e2e-student-001",
        "email": "e2e.student@example.com",
        "username": "e2e_student",
        "role": "student",
        "grade_level": "10",
        "subjects": ["mathematics", "science"]
    }


@pytest.fixture(scope="function")
def test_teacher_user():
    """Create a test teacher user."""
    return {
        "user_id": "e2e-teacher-001",
        "email": "e2e.teacher@example.com",
        "username": "e2e_teacher",
        "role": "teacher",
        "subjects": ["mathematics", "physics"],
        "grade_levels": ["9", "10", "11"]
    }


@pytest.fixture(scope="function")
def test_admin_user():
    """Create a test admin user."""
    return {
        "user_id": "e2e-admin-001",
        "email": "e2e.admin@example.com",
        "username": "e2e_admin",
        "role": "admin",
        "permissions": ["all"]
    }


# Test document fixtures
@pytest.fixture(scope="function")
def test_document_textbook():
    """Sample textbook document for E2E testing."""
    return {
        "title": "Introduction to Algebra",
        "content": """
        Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols. 
        It is a unifying thread of almost all mathematics and includes everything from solving elementary equations to studying abstractions such as groups, rings, and fields.
        
        The most basic part of algebra is elementary algebra, which is concerned with solving equations and manipulating formulas.
        More advanced parts include abstract algebra and linear algebra.
        """,
        "file_type": "txt",
        "metadata": {
            "subject": "mathematics",
            "grade_level": "9",
            "difficulty": "medium",
            "author": "E2E Test"
        }
    }


@pytest.fixture(scope="function)
def test_document_science():
    """Sample science document for E2E testing."""
    return {
        "title": "Photosynthesis Process",
        "content": """
        Photosynthesis is the process by which plants convert sunlight into energy.
        This process occurs in chloroplasts and produces glucose and oxygen as byproducts.
        
        The light-dependent reactions occur in the thylakoid membranes and require light energy to produce ATP and NADPH.
        The light-independent reactions (Calvin cycle) use these products to synthesize glucose.
        """,
        "file_type": "txt",
        "metadata": {
            "subject": "biology",
            "grade_level": "10",
            "difficulty": "easy",
            "author": "E2E Test"
        }
    }


@pytest.fixture(scope="function)
def test_queries():
    """Sample queries for E2E testing."""
    return [
        {
            "query": "What is photosynthesis?",
            "expected_topics": ["plants", "sunlight", "energy", "chloroplasts"],
            "difficulty": "easy"
        },
        {
            "query": "How do I solve quadratic equations?",
            "expected_topics": ["algebra", "equations", "quadratic formula"],
            "difficulty": "medium"
        },
        {
            "query": "Explain Newton's first law of motion",
            "expected_topics": ["physics", "force", "motion", "inertia"],
            "difficulty": "hard"
        }
    ]