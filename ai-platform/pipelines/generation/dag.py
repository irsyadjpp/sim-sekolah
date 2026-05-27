"""
Generation DAG for AI response generation

This pipeline handles the complete RAG generation flow:
- Retrieval of relevant documents
- Context assembly and formatting
- LLM response generation
- Guard rail validation
"""

from prefect import task, flow, get_run_logger
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from shared.observability import get_tracer
from shared.logging import get_logger
from storage.abstractions import QdrantDB, StorageConfig

logger = get_logger(__name__)


@task(name="retrieve_documents")
async def retrieve_documents(
    query: str,
    collection_name: str = "document_embeddings",
    limit: int = 5,
    score_threshold: float = 0.7,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant documents using vector similarity search.
    
    Args:
        query: User query text
        collection_name: Vector collection name
        limit: Maximum number of documents to retrieve
        score_threshold: Minimum similarity score
        filters: Optional filters for retrieval
        
    Returns:
        List of retrieved documents with similarity scores
    """
    logger = get_run_logger()
    tracer = get_tracer("generation")
    
    with tracer.span("retrieve_documents", kind="internal"):
        logger.info(f"Retrieving documents for query: {query}")
        
        # Get embedding for query (placeholder)
        query_embedding = await _generate_query_embedding(query)
        
        # Get Qdrant client
        config = StorageConfig.from_env(prefix="QDRANT_")
        async with QdrantDB(config) as qdrant:
            # Search for similar documents
            search_results = await qdrant.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                filter_condition=filters
            )
            
            # Format results
            retrieved_docs = []
            for result in search_results:
                retrieved_docs.append({
                    "chunk_id": result["id"],
                    "document_id": result["payload"]["document_id"],
                    "content": result["payload"]["content"],
                    "score": result["score"],
                    "metadata": result["payload"]
                })
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents")
            return retrieved_docs


@task(name="assemble_context")
async def assemble_context(
    retrieved_docs: List[Dict[str, Any]],
    max_context_length: int = 4000,
    include_metadata: bool = True
) -> str:
    """
    Assemble context from retrieved documents.
    
    Args:
        retrieved_docs: Retrieved documents with metadata
        max_context_length: Maximum context length in characters
        include_metadata: Whether to include document metadata
        
    Returns:
        Formatted context string
    """
    logger = get_run_logger()
    tracer = get_tracer("generation")
    
    with tracer.span("assemble_context", kind="internal"):
        logger.info(f"Assembling context from {len(retrieved_docs)} documents")
        
        context_parts = []
        current_length = 0
        
        for i, doc in enumerate(retrieved_docs):
            # Format document for context
            if include_metadata:
                doc_part = f"[Document {doc['document_id']} - Score: {doc['score']:.3f}]\n{doc['content']}\n"
            else:
                doc_part = f"{doc['content']}\n"
            
            # Check length limit
            if current_length + len(doc_part) > max_context_length:
                break
            
            context_parts.append(doc_part)
            current_length += len(doc_part)
        
        context = "\n".join(context_parts)
        logger.info(f"Context assembled (length: {len(context)} characters)")
        
        return context


@task(name="generate_response")
async def generate_response(
    query: str,
    context: str,
    model_name: str = "llama-3-8b",
    temperature: float = 0.7,
    max_tokens: int = 500
) -> Dict[str, Any]:
    """
    Generate response using LLM.
    
    Args:
        query: Original user query
        context: Assembled context from retrieved documents
        model_name: LLM model name
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated response with metadata
    """
    logger = get_run_logger()
    tracer = get_tracer("generation")
    
    with tracer.span("generate_response", kind="internal"):
        logger.info(f"Generating response using {model_name}")
        
        # Format prompt with context
        prompt = _format_rag_prompt(query, context)
        
        # Call LLM service (placeholder)
        llm_response = await _call_llm_service(
            prompt=prompt,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        result = {
            "query": query,
            "response": llm_response["text"],
            "model": model_name,
            "tokens_used": llm_response["tokens_used"],
            "prompt_tokens": llm_response.get("prompt_tokens"),
            "completion_tokens": llm_response.get("completion_tokens"),
            "context_length": len(context),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Response generated (tokens: {result['tokens_used']})")
        return result


@task(name="apply_guard_rails")
async def guard_rails(
    response: str,
    query: str,
    context: str,
    guard_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Apply guard rails to generated response.
    
    Args:
        response: Generated response text
        query: Original user query
        context: Used context
        guard_config: Guard configuration
        
    Returns:
        Guard check results
    """
    logger = get_run_logger()
    tracer = get_tracer("generation")
    
    with tracer.span("guard_rails", kind="internal"):
        logger.info("Applying guard rails to response")
        
        # Run various guard checks
        safety_check = await _check_safety(response)
        quality_check = await _check_quality(response, query, context)
        accuracy_check = await _check_accuracy(response, context)
        policy_check = await _check_policy(response)
        
        # Determine overall guard result
        all_passed = (
            safety_check["passed"] and
            quality_check["passed"] and
            accuracy_check["passed"] and
            policy_check["passed"]
        )
        
        result = {
            "passed": all_passed,
            "checks": {
                "safety": safety_check,
                "quality": quality_check,
                "accuracy": accuracy_check,
                "policy": policy_check
            },
            "response": response if all_passed else _generate_guard_message(all_passed),
            "checked_at": datetime.utcnow().isoformat()
        }
        
        if all_passed:
            logger.info("All guard checks passed")
        else:
            logger.warning(f"Guard checks failed: {[k for k, v in result['checks'].items() if not v['passed']]}")
        
        return result


@flow(name="generation_pipeline")
async def generation_pipeline(
    query: str,
    collection_name: str = "document_embeddings",
    retrieval_limit: int = 5,
    max_context_length: int = 4000,
    model_name: str = "llama-3-8b",
    temperature: float = 0.7,
    max_tokens: int = 500,
    skip_guards: bool = False
) -> Dict[str, Any]:
    """
    Complete RAG generation pipeline.
    
    Args:
        query: User query
        collection_name: Vector collection name
        retrieval_limit: Number of documents to retrieve
        max_context_length: Maximum context length
        model_name: LLM model name
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        skip_guards: Skip guard rail checks
        
    Returns:
        Complete generation pipeline result
    """
    logger = get_run_logger()
    logger.info(f"Starting generation pipeline for query: {query}")
    
    pipeline_results = {}
    
    # Retrieve documents
    retrieved_docs = await retrieve_documents(
        query=query,
        collection_name=collection_name,
        limit=retrieval_limit
    )
    pipeline_results["retrieval_count"] = len(retrieved_docs)
    
    # Assemble context
    context = await assemble_context(
        retrieved_docs=retrieved_docs,
        max_context_length=max_context_length
    )
    pipeline_results["context_length"] = len(context)
    
    # Generate response
    generation_result = await generate_response(
        query=query,
        context=context,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )
    pipeline_results["generation"] = generation_result
    
    # Apply guard rails
    if not skip_guards:
        guard_result = await guard_rails(
            response=generation_result["response"],
            query=query,
            context=context
        )
        pipeline_results["guards"] = guard_result
        
        # Use guarded response if guards failed
        if not guard_result["passed"]:
            generation_result["response"] = guard_result["response"]
            generation_result["guarded"] = True
    else:
        pipeline_results["guards"] = {"passed": True, "skipped": True}
        generation_result["guarded"] = False
    
    pipeline_results["final_response"] = generation_result["response"]
    
    logger.info("Generation pipeline completed")
    return {
        "query": query,
        "pipeline_results": pipeline_results,
        "pipeline_status": "completed"
    }


@flow(name="batch_generation_pipeline")
async def batch_generation_pipeline(
    queries: List[str],
    collection_name: str = "document_embeddings",
    batch_size: int = 3
) -> Dict[str, Any]:
    """
    Batch generation pipeline for multiple queries.
    
    Args:
        queries: List of user queries
        collection_name: Vector collection name
        batch_size: Number of queries to process in parallel
        
    Returns:
        Combined generation results
    """
    logger = get_run_logger()
    logger.info(f"Starting batch generation for {len(queries)} queries")
    
    results = []
    
    # Process queries in batches
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        
        # Process batch in parallel
        tasks = [
            generation_pipeline(
                query=query,
                collection_name=collection_name
            )
            for query in batch
        ]
        
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    
    logger.info(f"Batch generation completed for {len(results)} queries")
    
    return {
        "total_queries": len(queries),
        "successful_generations": len(results),
        "results": results
    }


# Helper functions
async def _generate_query_embedding(query: str) -> List[float]:
    """Generate embedding for query (placeholder)."""
    import numpy as np
    # In production, this would call the embedding service
    return np.random.rand(1024).tolist()


def _format_rag_prompt(query: str, context: str) -> str:
    """Format RAG prompt with context."""
    return f"""You are an AI assistant that helps answer questions based on the provided context.

Context:
{context}

Question: {query}

Please provide a helpful and accurate answer based on the context above. If the context doesn't contain the answer, say so."""


async def _call_llm_service(
    prompt: str,
    model_name: str,
    temperature: float,
    max_tokens: int
) -> Dict[str, Any]:
    """Call LLM service (placeholder)."""
    # In production, this would call the generation service
    # For now, return mock response
    await asyncio.sleep(0.5)  # Simulate API call
    
    # Generate mock response
    mock_response = f"Based on the provided context, here's an answer to the question. This is a simulated response from {model_name}."
    
    return {
        "text": mock_response,
        "tokens_used": len(mock_response.split()),
        "prompt_tokens": len(prompt.split()),
        "completion_tokens": len(mock_response.split()),
        "model": model_name
    }


async def _check_safety(response: str) -> Dict[str, Any]:
    """Check if response is safe (no harmful content)."""
    # In production, this would use content moderation service
    harmful_keywords = ["violence", "harm", "illegal", "drugs", "weapons"]
    response_lower = response.lower()
    
    found_harmful = [keyword for keyword in harmful_keywords if keyword in response_lower]
    
    return {
        "passed": len(found_harmful) == 0,
        "found_keywords": found_harmful,
        "severity": "high" if found_harmful else "none"
    }


async def _check_quality(response: str, query: str, context: str) -> Dict[str, Any]:
    """Check response quality."""
    # Simple quality checks
    min_length = 20
    max_length = 2000
    
    if len(response) < min_length:
        return {"passed": False, "reason": "response too short"}
    
    if len(response) > max_length:
        return {"passed": False, "reason": "response too long"}
    
    # Check if response addresses the query
    query_words = set(query.lower().split())
    response_words = set(response.lower().split())
    overlap = len(query_words & response_words)
    
    if overlap == 0:
        return {"passed": False, "reason": "response doesn't address query"}
    
    return {
        "passed": True,
        "relevance_score": overlap / len(query_words)
    }


async def _check_accuracy(response: str, context: str) -> Dict[str, Any]:
    """Check if response is accurate based on context."""
    # Simple check: ensure response doesn't contradict context
    # In production, this would use fact-checking models
    
    if "I don't know" in response or "not mentioned in the context" in response:
        # If context is empty, this is acceptable
        if not context.strip():
            return {"passed": True, "reason": "no context available"}
        return {"passed": False, "reason": "response indicates context doesn't contain answer"}
    
    return {
        "passed": True,
        "confidence": 0.8  # Placeholder confidence
    }


async def _check_policy(response: str) -> Dict[str, Any]:
    """Check if response complies with policies."""
    # Simple policy checks
    if len(response) < 10:
        return {"passed": False, "reason": "response too brief"}
    
    # Check for disclaimers
    if response.startswith("I cannot") or response.startswith("I'm not able"):
        return {"passed": False, "reason": "uses disclaimers without proper justification"}
    
    return {
        "passed": True,
        "policy_violations": []
    }


def _generate_guard_message(guard_passed: bool) -> str:
    """Generate appropriate guard message."""
    if guard_passed:
        return ""
    
    return "I apologize, but I cannot provide an answer based on the available information. The response may not meet safety or quality standards."