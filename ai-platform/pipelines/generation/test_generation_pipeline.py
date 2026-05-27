"""
Unit tests for Generation Pipeline
"""
import pytest
from datetime import datetime
from pipelines.generation.generation_pipeline import (
    GenerationRequest,
    RetrievalStage,
    ContextBuilderStage,
    LLMGenerationStage,
    GuardrailStage,
    GenerationPipeline
)


class TestRetrievalStage:
    """Tests for RetrievalStage"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.retrieval = RetrievalStage()
    
    def test_retrieve(self):
        """Test document retrieval"""
        result = self.retrieval.retrieve("test query", top_k=3)
        
        assert result.query == "test query"
        assert len(result.documents) <= 3
        assert len(result.scores) == len(result.documents)
    
    def test_retrieve_with_custom_top_k(self):
        """Test retrieval with custom top_k"""
        result = self.retrieval.retrieve("test query", top_k=10)
        
        assert len(result.documents) <= 10


class TestContextBuilderStage:
    """Tests for ContextBuilderStage"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.builder = ContextBuilderStage()
    
    def test_build_context(self):
        """Test context building"""
        from pipelines.generation.generation_pipeline import RetrievalResult
        
        retrieval = RetrievalResult(
            documents=[
                {"id": "doc1", "content": "Content 1", "source": "test", "metadata": {}},
                {"id": "doc2", "content": "Content 2", "source": "test", "metadata": {}}
            ],
            scores=[0.9, 0.8],
            query="test query"
        )
        
        context = self.builder.build_context(retrieval)
        
        assert context.context is not None
        assert len(context.context) > 0
        assert len(context.sources) == 2
        assert context.metadata["source_count"] == 2


class TestLLMGenerationStage:
    """Tests for LLMGenerationStage"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.llm = LLMGenerationStage()
    
    def test_generate(self):
        """Test LLM generation"""
        result = self.llm.generate("test query", "test context")
        
        assert result.answer is not None
        assert result.model == "gpt-4"
        assert result.tokens_used > 0
        assert result.latency_ms >= 0
    
    def test_generate_with_long_context(self):
        """Test generation with long context"""
        long_context = "test context " * 100
        result = self.llm.generate("test query", long_context)
        
        assert result.answer is not None
        assert result.metadata["context_length"] == len(long_context)


class TestGuardrailStage:
    """Tests for GuardrailStage"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.guardrail = GuardrailStage()
    
    def test_check_safe_content(self):
        """Test guardrail check for safe content"""
        from pipelines.generation.generation_pipeline import GenerationResult
        
        generation = GenerationResult(
            answer="This is a safe answer.",
            model="gpt-4",
            tokens_used=100,
            latency_ms=500,
            metadata={}
        )
        
        result = self.guardrail.check(generation)
        
        assert result.is_safe is True
        assert len(result.flags) == 0
    
    def test_check_unsafe_content(self):
        """Test guardrail check for unsafe content"""
        from pipelines.generation.generation_pipeline import GenerationResult
        
        generation = GenerationResult(
            answer="This contains a password and secret information.",
            model="gpt-4",
            tokens_used=100,
            latency_ms=500,
            metadata={}
        )
        
        result = self.guardrail.check(generation)
        
        assert result.is_safe is False
        assert len(result.flags) > 0
        assert result.filtered_content is not None
    
    def test_check_short_answer(self):
        """Test guardrail check for short answer"""
        from pipelines.generation.generation_pipeline import GenerationResult
        
        generation = GenerationResult(
            answer="Short",
            model="gpt-4",
            tokens_used=5,
            latency_ms=100,
            metadata={}
        )
        
        result = self.guardrail.check(generation)
        
        assert result.is_safe is False
        assert "Answer too short" in result.flags


class TestGenerationPipeline:
    """Tests for GenerationPipeline"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.pipeline = GenerationPipeline()
    
    def test_run_pipeline(self):
        """Test pipeline execution"""
        request = GenerationRequest(
            request_id="test_req",
            query="test query",
            context={"grade": "8"},
            user_id="user_123"
        )
        
        result = self.pipeline.run(request)
        
        assert result.request_id == "test_req"
        assert result.query == "test query"
        assert result.retrieval is not None
        assert result.context is not None
        assert result.generation is not None
        assert result.guard is not None
    
    def test_run_pipeline_with_unsafe_content(self):
        """Test pipeline with unsafe content"""
        request = GenerationRequest(
            request_id="test_req",
            query="What is the password?",
            context={},
            user_id="user_123"
        )
        
        result = self.pipeline.run(request)
        
        assert result.guard.is_safe is False
        assert result.final_answer is not None
    
    def test_run_batch(self):
        """Test batch pipeline execution"""
        requests = [
            GenerationRequest(
                request_id="req1",
                query="query 1",
                context={},
                user_id="user_123"
            ),
            GenerationRequest(
                request_id="req2",
                query="query 2",
                context={},
                user_id="user_123"
            )
        ]
        
        results = self.pipeline.run_batch(requests)
        
        assert len(results) == 2
        assert all(r.request_id in ["req1", "req2"] for r in results)
    
    def test_get_stats(self):
        """Test pipeline statistics"""
        request = GenerationRequest(
            request_id="test_req",
            query="test query",
            context={},
            user_id="user_123"
        )
        
        self.pipeline.run(request)
        stats = self.pipeline.get_stats()
        
        assert stats["processed"] == 1
        assert stats["failed"] == 0
        assert stats["success_rate"] == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
