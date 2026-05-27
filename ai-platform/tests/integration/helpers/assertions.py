"""
Custom assertions for integration tests
"""

import pytest
from typing import Any, Dict, List, Optional
import jsonschema


def assert_document_processed(document: Dict[str, Any]):
    """
    Assert that a document has been processed successfully.
    
    Args:
        document: Document dictionary
    """
    assert document is not None, "Document should not be None"
    assert "document_id" in document, "Document should have document_id"
    assert document.get("status") in ["processed", "completed"], \
        f"Document status should be processed, got {document.get('status')}"
    assert "title" in document, "Document should have title"
    assert document.get("title"), "Document title should not be empty"


def assert_embedding_created(embedding: Dict[str, Any]):
    """
    Assert that an embedding has been created successfully.
    
    Args:
        embedding: Embedding dictionary
    """
    assert embedding is not None, "Embedding should not be None"
    assert "embedding_id" in embedding, "Embedding should have embedding_id"
    assert "vector" in embedding, "Embedding should have vector"
    assert isinstance(embedding["vector"], list), "Vector should be a list"
    assert len(embedding["vector"]) > 0, "Vector should not be empty"
    assert "dimension" in embedding, "Embedding should have dimension"
    assert embedding["dimension"] == len(embedding["vector"]), \
        "Dimension should match vector length"


def assert_response_schema_valid(response: Dict[str, Any], schema: Dict[str, Any]):
    """
    Assert that response matches the provided JSON schema.
    
    Args:
        response: Response dictionary
        schema: JSON schema dictionary
    """
    try:
        jsonschema.validate(response, schema)
    except jsonschema.ValidationError as e:
        pytest.fail(f"Response schema validation failed: {e.message}")


def assert_service_healthy(health_check: Dict[str, Any]):
    """
    Assert that service health check indicates healthy status.
    
    Args:
        health_check: Health check response dictionary
    """
    assert health_check is not None, "Health check should not be None"
    assert "status" in health_check, "Health check should have status"
    assert health_check["status"] == "healthy", \
        f"Service should be healthy, got status: {health_check['status']}"


def assert_search_results_valid(results: List[Dict[str, Any]], min_count: int = 1):
    """
    Assert that search results are valid.
    
    Args:
        results: Search results list
        min_count: Minimum number of results expected
    """
    assert isinstance(results, list), "Results should be a list"
    assert len(results) >= min_count, \
        f"Expected at least {min_count} results, got {len(results)}"
    
    for result in results:
        assert "score" in result, "Each result should have a score"
        assert 0 <= result["score"] <= 1, "Score should be between 0 and 1"
        assert "document_id" in result, "Each result should have document_id"


def assert_generation_valid(generation: Dict[str, Any]):
    """
    Assert that generation response is valid.
    
    Args:
        generation: Generation response dictionary
    """
    assert generation is not None, "Generation should not be None"
    assert "response_id" in generation, "Generation should have response_id"
    assert "response" in generation, "Generation should have response"
    assert len(generation["response"]) > 0, "Response should not be empty"
    assert "model" in generation, "Generation should have model name"


def assert_user_created(user: Dict[str, Any]):
    """
    Assert that user has been created successfully.
    
    Args:
        user: User dictionary
    """
    assert user is not None, "User should not be None"
    assert "user_id" in user, "User should have user_id"
    assert "email" in user, "User should have email"
    assert "@" in user["email"], "Email should be valid"
    assert "username" in user, "User should have username"
    assert "role" in user, "User should have role"


def assert_conversation_created(conversation: Dict[str, Any]):
    """
    Assert that conversation has been created successfully.
    
    Args:
        conversation: Conversation dictionary
    """
    assert conversation is not None, "Conversation should not be None"
    assert "conversation_id" in conversation, "Conversation should have conversation_id"
    assert "user_id" in conversation, "Conversation should have user_id"
    assert "created_at" in conversation, "Conversation should have created_at"


def assert_message_valid(message: Dict[str, Any]):
    """
    Assert that message is valid.
    
    Args:
        message: Message dictionary
    """
    assert message is not None, "Message should not be None"
    assert "message_id" in message, "Message should have message_id"
    assert "conversation_id" in message, "Message should have conversation_id"
    assert "role" in message, "Message should have role"
    assert message["role"] in ["user", "assistant", "system"], \
        f"Role should be user/assistant/system, got {message['role']}"
    assert "content" in message, "Message should have content"
    assert len(message["content"]) > 0, "Message content should not be empty"


def assert_graph_node_created(node: Dict[str, Any]):
    """
    Assert that graph node has been created successfully.
    
    Args:
        node: Node dictionary
    """
    assert node is not None, "Node should not be None"
    assert "id" in node, "Node should have id"
    assert "label" in node, "Node should have label"
    assert "properties" in node, "Node should have properties"
    assert isinstance(node["properties"], dict), "Properties should be a dictionary"


def assert_graph_edge_created(edge: Dict[str, Any]):
    """
    Assert that graph edge has been created successfully.
    
    Args:
        edge: Edge dictionary
    """
    assert edge is not None, "Edge should not be None"
    assert "id" in edge, "Edge should have id"
    assert "type" in edge, "Edge should have type"
    assert "start_node" in edge, "Edge should have start_node"
    assert "end_node" in edge, "Edge should have end_node"


def assert_api_response_success(response: Dict[str, Any], status_code: int = 200):
    """
    Assert that API response indicates success.
    
    Args:
        response: Response dictionary
        status_code: Expected HTTP status code
    """
    assert response is not None, "Response should not be None"
    if "status_code" in response:
        assert response["status_code"] == status_code, \
            f"Expected status code {status_code}, got {response['status_code']}"
    if "success" in response:
        assert response["success"] is True, "Response should indicate success"


def assert_pagination_valid(response: Dict[str, Any]):
    """
    Assert that paginated response is valid.
    
    Args:
        response: Paginated response dictionary
    """
    assert "data" in response, "Response should have data field"
    assert "pagination" in response, "Response should have pagination field"
    
    pagination = response["pagination"]
    assert "page" in pagination, "Pagination should have page"
    assert "page_size" in pagination, "Pagination should have page_size"
    assert "total" in pagination, "Pagination should have total"
    assert "total_pages" in pagination, "Pagination should have total_pages"
    
    assert pagination["page"] >= 1, "Page should be >= 1"
    assert pagination["page_size"] > 0, "Page size should be > 0"
    assert pagination["total"] >= 0, "Total should be >= 0"
    assert pagination["total_pages"] >= 1, "Total pages should be >= 1"


def assert_error_response_valid(error: Dict[str, Any]):
    """
    Assert that error response is valid.
    
    Args:
        error: Error response dictionary
    """
    assert error is not None, "Error response should not be None"
    assert "error" in error, "Error response should have error field"
    assert "message" in error, "Error response should have message field"
    assert len(error["message"]) > 0, "Error message should not be empty"
    
    if "code" in error:
        assert isinstance(error["code"], (int, str)), "Error code should be int or str"


def assert_timestamp_valid(timestamp: Any):
    """
    Assert that timestamp is valid.
    
    Args:
        timestamp: Timestamp value (string or datetime)
    """
    assert timestamp is not None, "Timestamp should not be None"
    
    if isinstance(timestamp, str):
        # Check if it's a valid ISO format timestamp
        try:
            from datetime import datetime
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")


def assert_uuid_valid(uuid_str: str):
    """
    Assert that UUID string is valid.
    
    Args:
        uuid_str: UUID string to validate
    """
    assert uuid_str is not None, "UUID should not be None"
    assert isinstance(uuid_str, str), "UUID should be a string"
    
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    assert re.match(uuid_pattern, uuid_str.lower()), \
        f"Invalid UUID format: {uuid_str}"


def assert_metadata_valid(metadata: Dict[str, Any], required_keys: Optional[List[str]] = None):
    """
    Assert that metadata dictionary is valid.
    
    Args:
        metadata: Metadata dictionary
        required_keys: List of required keys
    """
    assert metadata is not None, "Metadata should not be None"
    assert isinstance(metadata, dict), "Metadata should be a dictionary"
    
    if required_keys:
        for key in required_keys:
            assert key in metadata, f"Metadata should have required key: {key}"