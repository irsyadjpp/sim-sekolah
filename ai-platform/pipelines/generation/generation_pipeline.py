"""
Generation Pipeline - Retrieval → Context → LLM → Guard
End-to-end generation pipeline with retrieval, context building, LLM generation, and guardrails
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GenerationRequest:
    """Request for generation pipeline"""
    request_id: str
    query: str
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class RetrievalResult:
    """Result from retrieval stage"""
    documents: List[Dict[str, Any]]
    scores: List[float]
    query: str


@dataclass
class ContextResult:
    """Result from context building stage"""
    context: str
    sources: List[str]
    metadata: Dict[str, Any]


@dataclass
class GenerationResult:
    """Result from LLM generation stage"""
    answer: str
    model: str
    tokens_used: int
    latency_ms: float
    metadata: Dict[str, Any]


@dataclass
class GuardResult:
    """Result from guardrail stage"""
    is_safe: bool
    flags: List[str]
    confidence: float
    filtered_content: Optional[str] = None


@dataclass
class PipelineResult:
    """Final pipeline result"""
    request_id: str
    query: str
    retrieval: RetrievalResult
    context: ContextResult
    generation: GenerationResult
    guard: GuardResult
    final_answer: Optional[str]
    timestamp: datetime


class RetrievalStage:
    """Retrieval stage - fetches relevant documents"""
    
    def __init__(self):
        self.vector_store = {}  # In-memory (in production, use Qdrant/Weaviate)
    
    def retrieve(self, query: str, top_k: int = 5) -> RetrievalResult:
        """Retrieve relevant documents for query"""
        # Simplified retrieval - in production use vector similarity search
        documents = []
        scores = []
        
        # Mock retrieval results
        for i in range(min(top_k, 3)):
            documents.append({
                "id": f"doc_{i}",
                "content": f"Relevant content for query: {query}",
                "source": "knowledge/cp",
                "metadata": {"grade": str(i + 1)}
            })
            scores.append(0.9 - (i * 0.1))
        
        logger.info(f"Retrieved {len(documents)} documents for query")
        
        return RetrievalResult(
            documents=documents,
            scores=scores,
            query=query
        )


class ContextBuilderStage:
    """Context building stage - builds context from retrieved documents"""
    
    def build_context(self, retrieval: RetrievalResult) -> ContextResult:
        """Build context from retrieval results"""
        context_parts = []
        sources = []
        
        for doc in retrieval.documents:
            context_parts.append(f"Document: {doc['id']}\n{doc['content']}")
            sources.append(doc['id'])
        
        context = "\n\n".join(context_parts)
        
        logger.info(f"Built context from {len(sources)} sources")
        
        return ContextResult(
            context=context,
            sources=sources,
            metadata={
                "source_count": len(sources),
                "context_length": len(context)
            }
        )


class LLMGenerationStage:
    """LLM generation stage - generates answer using LLM"""
    
    def __init__(self):
        self.model = "gpt-4"
    
    def generate(self, query: str, context: str) -> GenerationResult:
        """Generate answer using LLM"""
        start_time = datetime.utcnow()
        
        # Simplified generation - in production call LLM service
        answer = f"Based on the context, here's the answer to: {query}"
        
        # Calculate latency
        latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        logger.info(f"Generated answer in {latency_ms:.2f}ms")
        
        return GenerationResult(
            answer=answer,
            model=self.model,
            tokens_used=150,  # Simplified
            latency_ms=latency_ms,
            metadata={
                "context_length": len(context),
                "query_length": len(query)
            }
        )


class GuardrailStage:
    """Guardrail stage - filters and validates generated content"""
    
    def __init__(self):
        self.forbidden_words = ["password", "secret", "confidential"]
    
    def check(self, generation: GenerationResult) -> GuardResult:
        """Check generated content against guardrails"""
        flags = []
        content_lower = generation.answer.lower()
        
        # Check for forbidden words
        for word in self.forbidden_words:
            if word in content_lower:
                flags.append(f"Contains forbidden word: {word}")
        
        # Check for inappropriate content
        if len(generation.answer) < 10:
            flags.append("Answer too short")
        
        is_safe = len(flags) == 0
        confidence = 1.0 if is_safe else 0.5
        
        filtered_content = None
        if not is_safe:
            filtered_content = "[Content filtered due to policy violations]"
        
        logger.info(f"Guardrail check: {'SAFE' if is_safe else 'UNSAFE'} - {len(flags)} flags")
        
        return GuardResult(
            is_safe=is_safe,
            flags=flags,
            confidence=confidence,
            filtered_content=filtered_content
        )


class GenerationPipeline:
    """End-to-end generation pipeline"""
    
    def __init__(self):
        self.retrieval = RetrievalStage()
        self.context_builder = ContextBuilderStage()
        self.llm = LLMGenerationStage()
        self.guardrail = GuardrailStage()
        self.processed_count = 0
        self.failed_count = 0
    
    def run(self, request: GenerationRequest) -> PipelineResult:
        """Run generation pipeline"""
        logger.info(f"Starting generation pipeline for request {request.request_id}")
        
        # Stage 1: Retrieval
        retrieval = self.retrieval.retrieve(request.query)
        
        # Stage 2: Context Building
        context = self.context_builder.build_context(retrieval)
        
        # Stage 3: LLM Generation
        generation = self.llm.generate(request.query, context.context)
        
        # Stage 4: Guardrail
        guard = self.guardrail.check(generation)
        
        # Determine final answer
        final_answer = generation.answer if guard.is_safe else guard.filtered_content
        
        self.processed_count += 1
        
        result = PipelineResult(
            request_id=request.request_id,
            query=request.query,
            retrieval=retrieval,
            context=context,
            generation=generation,
            guard=guard,
            final_answer=final_answer,
            timestamp=datetime.utcnow()
        )
        
        logger.info(f"Generation pipeline complete for request {request.request_id}")
        
        return result
    
    def run_batch(self, requests: List[GenerationRequest]) -> List[PipelineResult]:
        """Run pipeline for multiple requests"""
        results = []
        for req in requests:
            try:
                result = self.run(req)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing request {req.request_id}: {e}")
                self.failed_count += 1
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "processed": self.processed_count,
            "failed": self.failed_count,
            "success_rate": self.processed_count / max(self.processed_count + self.failed_count, 1)
        }


# Example usage
if __name__ == "__main__":
    # Example request
    request = GenerationRequest(
        request_id="req_001",
        query="What is the Pythagorean theorem?",
        context={"grade": "8", "subject": "mathematics"},
        user_id="user_123"
    )
    
    # Run pipeline
    pipeline = GenerationPipeline()
    result = pipeline.run(request)
    
    print(f"Pipeline Result for {result.request_id}")
    print(f"Query: {result.query}")
    print(f"Retrieved {len(result.retrieval.documents)} documents")
    print(f"Context built from {len(result.context.sources)} sources")
    print(f"Generated answer: {result.generation.answer}")
    print(f"Latency: {result.generation.latency_ms:.2f}ms")
    print(f"Guardrail: {'SAFE' if result.guard.is_safe else 'UNSAFE'}")
    print(f"Final answer: {result.final_answer}")
    
    print(f"\nPipeline stats: {pipeline.get_stats()}")
