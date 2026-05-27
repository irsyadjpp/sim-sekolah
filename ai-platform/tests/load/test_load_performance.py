"""
Load Tests - Performance and Scalability Tests
Load tests using Locust/K6 for performance testing
"""
from locust import HttpUser, task, between
import random


class GatewayUser(HttpUser):
    """Simulated user for Gateway Service"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts"""
        self.client.get("/health")
    
    @task(3)
    def query_endpoint(self):
        """Test query endpoint"""
        queries = [
            "What is the Pythagorean theorem?",
            "Explain photosynthesis",
            "What are the main causes of World War II?",
            "How do plants reproduce?",
            "What is the difference between mitosis and meiosis?"
        ]
        
        payload = {
            "query": random.choice(queries),
            "context": {"grade": str(random.randint(7, 9)), "subject": "mathematics"}
        }
        
        self.client.post("/query", json=payload)
    
    @task(1)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")


class ParserUser(HttpUser):
    """Simulated user for Parser Service"""
    wait_time = between(2, 5)
    
    @task
    def parse_endpoint(self):
        """Test parse endpoint"""
        contents = [
            "This is a test document for parsing.",
            "Another test document with more content.",
            "Document with mathematical formulas: a² + b² = c²"
        ]
        
        payload = {
            "content": random.choice(contents),
            "format": "text"
        }
        
        self.client.post("/parse", json=payload)
    
    @task(1)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")


class RetrievalUser(HttpUser):
    """Simulated user for Retrieval Service"""
    wait_time = between(1, 3)
    
    @task
    def search_endpoint(self):
        """Test search endpoint"""
        queries = [
            "test query",
            "mathematics",
            "science",
            "history",
            "language"
        ]
        
        payload = {
            "query": random.choice(queries),
            "top_k": random.randint(3, 10)
        }
        
        self.client.post("/search", json=payload)
    
    @task(1)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")


class GenerationUser(HttpUser):
    """Simulated user for Generation Service"""
    wait_time = between(3, 6)
    
    @task
    def generate_endpoint(self):
        """Test generate endpoint"""
        queries = [
            "What is the Pythagorean theorem?",
            "Explain the water cycle",
            "What are the parts of a cell?"
        ]
        
        payload = {
            "query": random.choice(queries),
            "context": "test context"
        }
        
        self.client.post("/generate", json=payload)
    
    @task(1)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")


# Run with: locust -f test_load_performance.py --host=http://localhost:8002
