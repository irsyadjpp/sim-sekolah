"""
Test helpers for integration tests
"""

from .clients import (
    BaseServiceClient,
    GrpcClient,
    HttpClient,
    DocumentServiceClient,
    EmbeddingServiceClient,
    RetrievalServiceClient,
    GenerationServiceClient,
)

from .assertions import (
    assert_document_processed,
    assert_embedding_created,
    assert_response_schema_valid,
    assert_service_healthy,
    assert_search_results_valid,
    assert_generation_valid,
    assert_user_created,
    assert_conversation_created,
    assert_message_valid,
    assert_graph_node_created,
    assert_graph_edge_created,
    assert_api_response_success,
    assert_pagination_valid,
    assert_error_response_valid,
    assert_timestamp_valid,
    assert_uuid_valid,
    assert_metadata_valid,
)

from .fixtures import (
    generate_test_document_id,
    generate_test_user_id,
    generate_test_conversation_id,
    create_test_document,
    create_test_user,
    create_test_conversation,
    create_test_message,
    create_test_embedding,
    create_test_search_result,
    create_test_graph_node,
    create_test_graph_edge,
    create_test_batch_documents,
    create_test_pagination_response,
    create_test_error_response,
    cleanup_test_document,
    cleanup_test_user,
    TestCleanup,
)

__all__ = [
    # Clients
    "BaseServiceClient",
    "GrpcClient",
    "HttpClient",
    "DocumentServiceClient",
    "EmbeddingServiceClient",
    "RetrievalServiceClient",
    "GenerationServiceClient",
    
    # Assertions
    "assert_document_processed",
    "assert_embedding_created",
    "assert_response_schema_valid",
    "assert_service_healthy",
    "assert_search_results_valid",
    "assert_generation_valid",
    "assert_user_created",
    "assert_conversation_created",
    "assert_message_valid",
    "assert_graph_node_created",
    "assert_graph_edge_created",
    "assert_api_response_success",
    "assert_pagination_valid",
    "assert_error_response_valid",
    "assert_timestamp_valid",
    "assert_uuid_valid",
    "assert_metadata_valid",
    
    # Fixtures
    "generate_test_document_id",
    "generate_test_user_id",
    "generate_test_conversation_id",
    "create_test_document",
    "create_test_user",
    "create_test_conversation",
    "create_test_message",
    "create_test_embedding",
    "create_test_search_result",
    "create_test_graph_node",
    "create_test_graph_edge",
    "create_test_batch_documents",
    "create_test_pagination_response",
    "create_test_error_response",
    "cleanup_test_document",
    "cleanup_test_user",
    "TestCleanup",
]