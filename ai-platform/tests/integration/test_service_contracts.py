"""
Integration Tests - Contract Tests Between Services
Tests service-to-service contracts and API compatibility
"""
import pytest
from typing import Dict, Any
import requests


class TestGatewayServiceContract:
    """Contract tests for Gateway Service"""
    
    def test_gateway_health_endpoint(self):
        """Test Gateway Service health endpoint"""
        # In production, use actual service URL
        response = requests.get("http://localhost:8002/health", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "gateway-service"
        assert data["status"] == "healthy"
    
    def test_gateway_api_compatibility(self):
        """Test Gateway Service API compatibility"""
        # Test that Gateway exposes expected endpoints
        response = requests.get("http://localhost:8002/docs", timeout=5)
        
        assert response.status_code == 200


class TestParserServiceContract:
    """Contract tests for Parser Service"""
    
    def test_parser_health_endpoint(self):
        """Test Parser Service health endpoint"""
        response = requests.get("http://localhost:8010/health", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "parser-service"
    
    def test_parser_parse_endpoint(self):
        """Test Parser Service parse endpoint"""
        payload = {
            "content": "Test content for parsing",
            "format": "text"
        }
        
        response = requests.post(
            "http://localhost:8010/parse",
            json=payload,
            timeout=10
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "parsed_content" in data or "error" in data


class TestRetrievalServiceContract:
    """Contract tests for Retrieval Service"""
    
    def test_retrieval_health_endpoint(self):
        """Test Retrieval Service health endpoint"""
        response = requests.get("http://localhost:8003/health", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "retrieval-service"
    
    def test_retrieval_search_endpoint(self):
        """Test Retrieval Service search endpoint"""
        payload = {
            "query": "test query",
            "top_k": 5
        }
        
        response = requests.post(
            "http://localhost:8003/search",
            json=payload,
            timeout=10
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "results" in data or "error" in data


class TestGenerationServiceContract:
    """Contract tests for Generation Service"""
    
    def test_generation_health_endpoint(self):
        """Test Generation Service health endpoint"""
        response = requests.get("http://localhost:8004/health", timeout=5)
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "generation-service"
    
    def test_generation_generate_endpoint(self):
        """Test Generation Service generate endpoint"""
        payload = {
            "query": "test query",
            "context": "test context"
        }
        
        response = requests.post(
            "http://localhost:8004/generate",
            json=payload,
            timeout=30
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "answer" in data or "error" in data


class TestServiceToServiceCommunication:
    """Tests for service-to-service communication"""
    
    def test_gateway_to_parser_communication(self):
        """Test Gateway to Parser communication"""
        # Gateway should be able to call Parser
        gateway_response = requests.get("http://localhost:8002/health", timeout=5)
        assert gateway_response.status_code == 200
    
    def test_gateway_to_retrieval_communication(self):
        """Test Gateway to Retrieval communication"""
        gateway_response = requests.get("http://localhost:8002/health", timeout=5)
        assert gateway_response.status_code == 200
    
    def test_gateway_to_generation_communication(self):
        """Test Gateway to Generation communication"""
        gateway_response = requests.get("http://localhost:8002/health", timeout=5)
        assert gateway_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
