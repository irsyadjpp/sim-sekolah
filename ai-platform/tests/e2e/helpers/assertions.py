"""
E2E-specific assertions for end-to-end tests
"""

import pytest
from typing import Dict, Any, List, Optional


def assert_workflow_successful(workflow_result: Dict[str, Any]):
    """
    Assert that a workflow completed successfully.
    
    Args:
        workflow_result: Workflow result dictionary
    """
    assert workflow_result is not None, "Workflow result should not be None"
    assert "status" in workflow_result, "Workflow result should have status"
    assert workflow_result["status"] == "success", \
        f"Workflow should be successful, got status: {workflow_result['status']}"


def assert_workflow_steps_completed(workflow_summary: Dict[str, Any], expected_steps: List[str]):
    """
    Assert that all expected workflow steps completed.
    
    Args:
        workflow_summary: Workflow summary from orchestrator
        expected_steps: List of expected step names
    """
    completed_steps = [step["name"] for step in workflow_summary["steps"]]
    
    for expected_step in expected_steps:
        assert expected_step in completed_steps, \
            f"Expected step '{expected_step}' not found in completed steps: {completed_steps}"


def assert_workflow_duration_acceptable(workflow_summary: Dict[str, Any], max_duration: float):
    """
    Assert that workflow completed within acceptable time.
    
    Args:
        workflow_summary: Workflow summary from orchestrator
        max_duration: Maximum acceptable duration in seconds
    """
    total_duration = workflow_summary["total_duration"]
    assert total_duration <= max_duration, \
        f"Workflow duration {total_duration}s exceeds maximum {max_duration}s"


def assert_rag_response_valid(rag_result: Dict[str, Any]):
    """
    Assert that RAG response is valid and complete.
    
    Args:
        rag_result: RAG workflow result
    """
    assert rag_result is not None, "RAG result should not be None"
    assert "query" in rag_result, "RAG result should have query"
    assert "response" in rag_result, "RAG result should have response"
    assert "sources" in rag_result, "RAG result should have sources"
    assert "guard_checks" in rag_result, "RAG result should have guard_checks"
    
    # Verify response quality
    assert len(rag_result["response"]) > 0, "Response should not be empty"
    assert isinstance(rag_result["sources"], list), "Sources should be a list"
    assert len(rag_result["sources"]) > 0, "Should have at least one source"
    
    # Verify guard checks
    assert isinstance(rag_result["guard_checks"], dict), "Guard checks should be a dictionary"
    assert "passed" in rag_result["guard_checks"], "Guard checks should have passed status"


def assert_guard_checks_passed(guard_result: Dict[str, Any]):
    """
    Assert that all guard checks passed.
    
    Args:
        guard_result: Guard check result
    """
    assert guard_result is not None, "Guard result should not be None"
    assert "passed" in guard_result, "Guard result should have passed status"
    assert guard_result["passed"] is True, "Guard checks should have passed"
    
    # Check individual guard checks if available
    if "checks" in guard_result:
        for check_name, check_result in guard_result["checks"].items():
            assert check_result["status"] == "passed", \
                f"Guard check '{check_name}' should have passed, got {check_result['status']}"


def assert_response_quality_acceptable(response: str, min_length: int = 50, max_length: int = 2000):
    """
    Assert that response meets quality standards.
    
    Args:
        response: Generated response text
        min_length: Minimum acceptable length
        max_length: Maximum acceptable length
    """
    assert response is not None, "Response should not be None"
    assert isinstance(response, str), "Response should be a string"
    assert len(response) >= min_length, \
        f"Response length {len(response)} below minimum {min_length}"
    assert len(response) <= max_length, \
        f"Response length {len(response)} above maximum {max_length}"


def assert_sources_relevant(sources: List[Dict[str, Any]], query: str, min_relevance: float = 0.5):
    """
    Assert that retrieved sources are relevant to the query.
    
    Args:
        sources: List of retrieved sources
        query: Original query
        min_relevance: Minimum acceptable relevance score
    """
    assert len(sources) > 0, "Should have at least one source"
    
    for source in sources:
        assert "score" in source, "Source should have relevance score"
        assert source["score"] >= min_relevance, \
            f"Source relevance {source['score']} below minimum {min_relevance}"
        assert "content" in source, "Source should have content"
        assert len(source["content"]) > 0, "Source content should not be empty"


def assert_conversation_coherent(conversation_result: Dict[str, Any]):
    """
    Assert that conversation maintains coherence.
    
    Args:
        conversation_result: Conversation workflow result
    """
    assert conversation_result is not None, "Conversation result should not be None"
    assert "conversation_id" in conversation_result, "Should have conversation ID"
    assert "responses" in conversation_result, "Should have responses"
    
    responses = conversation_result["responses"]
    assert len(responses) > 0, "Should have at least one response"
    
    # Verify each response is valid
    for i, response in enumerate(responses):
        assert response["response"] is not None, f"Response {i} should not be None"
        assert len(response["response"]) > 0, f"Response {i} should not be empty"


def assert_document_ingestion_complete(ingestion_result: Dict[str, Any]):
    """
    Assert that document ingestion completed successfully.
    
    Args:
        ingestion_result: Document ingestion workflow result
    """
    assert ingestion_result is not None, "Ingestion result should not be None"
    assert "document_id" in ingestion_result, "Should have document ID"
    assert "embedding_ids" in ingestion_result, "Should have embedding IDs"
    assert "status" in ingestion_result, "Should have status"
    
    assert ingestion_result["status"] == "success", "Ingestion should be successful"
    assert len(ingestion_result["embedding_ids"]) > 0, "Should have created embeddings"


def assert_no_duplicate_sources(sources: List[Dict[str, Any]]):
    """
    Assert that there are no duplicate sources in results.
    
    Args:
        sources: List of retrieved sources
    """
    document_ids = [source.get("document_id") for source in sources]
    unique_ids = set(document_ids)
    
    assert len(document_ids) == len(unique_ids), \
        f"Found duplicate sources: {document_ids}"


def assert_response_addresses_query(response: str, query: str):
    """
    Assert that response actually addresses the user's query.
    
    This is a basic check - in production, you might use more sophisticated
    semantic similarity or NLP techniques.
    
    Args:
        response: Generated response
        query: Original query
    """
    assert response is not None, "Response should not be None"
    assert query is not None, "Query should not be None"
    
    # Basic check: response should not be empty and should contain some content
    assert len(response) > 0, "Response should not be empty"
    
    # Check for query keywords in response (basic relevance check)
    query_words = set(query.lower().split())
    response_words = set(response.lower().split())
    
    # At least some query words should appear in response
    overlap = query_words & response_words
    assert len(overlap) > 0, \
        f"Response should contain some query terms. Query: {query}, Response: {response}"


def assert_error_handling_workflow(workflow_result: Dict[str, Any], expected_error_type: str):
    """
    Assert that workflow handled errors appropriately.
    
    Args:
        workflow_result: Workflow result that should contain error info
        expected_error_type: Expected type of error
    """
    assert workflow_result is not None, "Workflow result should not be None"
    assert "status" in workflow_result, "Workflow result should have status"
    
    # If workflow failed, it should have error information
    if workflow_result["status"] == "failed":
        assert "error" in workflow_result or "errors" in workflow_result, \
            "Failed workflow should have error information"
        
        error_info = workflow_result.get("error", workflow_result.get("errors", {}))
        if isinstance(error_info, dict):
            assert "type" in error_info or "message" in error_info, \
                "Error info should have type or message"
        else:
            assert isinstance(error_info, str), "Error info should be string or dict"


def assert_performance_within_thresholds(
    workflow_summary: Dict[str, Any],
    thresholds: Dict[str, float]
):
    """
    Assert that workflow performance meets defined thresholds.
    
    Args:
        workflow_summary: Workflow summary from orchestrator
        thresholds: Dictionary of step names to maximum duration thresholds
    """
    for step in workflow_summary["steps"]:
        step_name = step["name"]
        if step_name in thresholds:
            max_duration = thresholds[step_name]
            actual_duration = step["duration"]
            assert actual_duration <= max_duration, \
                f"Step '{step_name}' duration {actual_duration}s exceeds threshold {max_duration}s"


def assert_data_consistency_across_services(
    document_data: Dict[str, Any],
    retrieval_result: Dict[str, Any],
    embedding_result: Dict[str, Any]
):
    """
    Assert that data remains consistent across different services.
    
    Args:
        document_data: Original document data
        retrieval_result: Result from retrieval service
        embedding_result: Result from embedding service
    """
    # Verify document ID consistency
    if "document_id" in document_data and "sources" in retrieval_result:
        for source in retrieval_result["sources"]:
            if "document_id" in source:
                assert source["document_id"] == document_data["document_id"], \
                    "Document ID should be consistent across services"
    
    # Verify content consistency
    if "content" in document_data:
        original_content = document_data["content"]
        # Content should be preserved in embeddings or retrieval
        # This is a basic check - adjust based on your data flow
        assert original_content is not None, "Original content should be preserved"