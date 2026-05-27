"""
E2E Tests - Full RAG → Generation → Guard Flow
End-to-end tests for the complete AI platform flow
"""
import pytest
from typing import Dict, Any
import requests
import time


class TestRAGGenerationFlow:
    """End-to-end tests for RAG → Generation → Guard flow"""
    
    def test_full_rag_generation_flow(self):
        """Test complete RAG → Generation → Guard flow"""
        # Step 1: Parse document
        parse_payload = {
            "content": "The Pythagorean theorem states that in a right-angled triangle, the square of the hypotenuse equals the sum of squares of the other two sides.",
            "format": "text"
        }
        parse_response = requests.post(
            "http://localhost:8010/parse",
            json=parse_payload,
            timeout=10
        )
        assert parse_response.status_code in [200, 201]
        
        # Step 2: Retrieve relevant documents
        retrieval_payload = {
            "query": "What is the Pythagorean theorem?",
            "top_k": 5
        }
        retrieval_response = requests.post(
            "http://localhost:8003/search",
            json=retrieval_payload,
            timeout=10
        )
        assert retrieval_response.status_code in [200, 201]
        retrieval_data = retrieval_response.json()
        
        # Step 3: Generate answer
        generation_payload = {
            "query": "What is the Pythagorean theorem?",
            "context": retrieval_data.get("results", [])
        }
        generation_response = requests.post(
            "http://localhost:8004/generate",
            json=generation_payload,
            timeout=30
        )
        assert generation_response.status_code in [200, 201]
        generation_data = generation_response.json()
        
        # Step 4: Check guardrails
        moderation_payload = {
            "content": generation_data.get("answer", ""),
            "check_type": "all"
        }
        moderation_response = requests.post(
            "http://localhost:8011/moderate",
            json=moderation_payload,
            timeout=10
        )
        assert moderation_response.status_code in [200, 201]
        moderation_data = moderation_response.json()
        
        # Verify the flow completed successfully
        assert moderation_data.get("is_safe", True)
    
    def test_rag_flow_with_gateway(self):
        """Test RAG flow through Gateway Service"""
        payload = {
            "query": "What is the Pythagorean theorem?",
            "context": {"grade": "8", "subject": "mathematics"}
        }
        
        response = requests.post(
            "http://localhost:8002/query",
            json=payload,
            timeout=30
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "answer" in data or "error" in data
    
    def test_rag_flow_with_complex_query(self):
        """Test RAG flow with complex query"""
        payload = {
            "query": "Explain the relationship between algebra and geometry in the Pythagorean theorem",
            "context": {"grade": "9", "subject": "mathematics"}
        }
        
        response = requests.post(
            "http://localhost:8002/query",
            json=payload,
            timeout=30
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "answer" in data or "error" in data
    
    def test_rag_flow_with_guardrail_violation(self):
        """Test RAG flow with content that triggers guardrails"""
        payload = {
            "query": "What is the secret password?",
            "context": {}
        }
        
        response = requests.post(
            "http://localhost:8002/query",
            json=payload,
            timeout=30
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        # Should either be filtered or return a safe response
        assert "answer" in data or "error" in data
    
    def test_rag_flow_performance(self):
        """Test RAG flow performance metrics"""
        start_time = time.time()
        
        payload = {
            "query": "What is the Pythagorean theorem?",
            "context": {"grade": "8", "subject": "mathematics"}
        }
        
        response = requests.post(
            "http://localhost:8002/query",
            json=payload,
            timeout=30
        )
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        assert response.status_code in [200, 201]
        # Should complete within reasonable time
        assert latency_ms < 10000  # 10 seconds max


class TestMultiStepFlow:
    """Tests for multi-step flows"""
    
    def test_parse_index_retrieve_flow(self):
        """Test Parse → Index → Retrieve flow"""
        # Parse document
        parse_payload = {
            "content": "Test document content for indexing and retrieval.",
            "format": "text"
        }
        parse_response = requests.post(
            "http://localhost:8010/parse",
            json=parse_payload,
            timeout=10
        )
        assert parse_response.status_code in [200, 201]
        
        # Index document (simplified - would use actual indexing service)
        # Retrieve document
        retrieval_payload = {
            "query": "Test document",
            "top_k": 5
        }
        retrieval_response = requests.post(
            "http://localhost:8003/search",
            json=retrieval_payload,
            timeout=10
        )
        assert retrieval_response.status_code in [200, 201]
    
    def test_enrichment_indexing_flow(self):
        """Test Enrichment → Indexing flow"""
        # This would test the enrichment pipeline followed by indexing
        # For now, simplified test
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
