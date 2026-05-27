"""
Pytest configuration for Hallucination Guard Service tests
"""
import pytest
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure pytest
@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "test_mode": True,
        "database_url": "sqlite:///:memory:",
        "skip_external_calls": True
    }


# Skip integration tests by default
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
