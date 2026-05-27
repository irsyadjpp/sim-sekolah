"""
RAG workflow end-to-end tests
"""

import pytest
from tests.e2e.helpers import (
    WorkflowOrchestrator,
    ingest_document_workflow,
    rag_workflow,
    assert_workflow_successful,
    assert_workflow_steps_completed,
    assert_workflow_duration_acceptable,
    assert_rag_response_valid,
    assert_guard_checks_passed,
    assert_response_quality_acceptable,
    assert_sources_relevant,
    assert_response_addresses_query,
)


@pytest.mark.e2e
@pytest.mark.workflow
@pytest.mark.slow
class TestRAGWorkflow:
    """End-to-end tests for RAG (Retrieval-Augmented Generation) workflow."""
    
    @pytest.mark.asyncio
    async def test_complete_rag_workflow(
        self,
        e2e_config,
        test_document_science,
        test_queries,
        e2e_cleanup
    ):
        """
        Test complete RAG workflow from document ingestion to query response.
        
        This test verifies:
        1. Document ingestion and processing
        2. Embedding generation and storage
        3. Query processing and retrieval
        4. Response generation with context
        5. Guard rail validation
        """
        # Setup service clients (mock for now, would be real clients in production)
        service_clients = {
            "document": MockDocumentServiceClient(),
            "embedding": MockEmbeddingServiceClient(),
            "retrieval": MockRetrievalServiceClient(),
            "generation": MockGenerationServiceClient(),
            "guard": MockGuardServiceClient(),
        }
        
        storage_clients = {
            "qdrant": MockQdrantClient(),
        }
        
        orchestrator = WorkflowOrchestrator(service_clients, storage_clients)
        
        # Step 1: Ingest document
        ingestion_result = await ingest_document_workflow(
            document_client=service_clients["document"],
            embedding_client=service_clients["embedding"],
            qdrant_client=storage_clients["qdrant"],
            document_data=test_document_science,
            orchestrator=orchestrator
        )
        
        assert_workflow_successful(ingestion_result)
        
        # Add cleanup
        async def cleanup_document():
            await service_clients["document"].delete_document(ingestion_result["document_id"])
        e2e_cleanup(cleanup_document)
        
        # Step 2: Execute RAG workflow
        query = test_queries[0]["query"]
        rag_result = await rag_workflow(
            retrieval_client=service_clients["retrieval"],
            generation_client=service_clients["generation"],
            guard_client=service_clients["guard"],
            query=query,
            orchestrator=orchestrator
        )
        
        # Verify RAG workflow
        assert_rag_response_valid(rag_result)
        assert_guard_checks_passed(rag_result["guard_checks"])
        assert_response_quality_acceptable(rag_result["response"])
        assert_response_addresses_query(rag_result["response"], query)
        
        # Verify workflow steps
        workflow_summary = orchestrator.get_workflow_summary()
        assert_workflow_successful(workflow_summary)
        assert_workflow_steps_completed(
            workflow_summary,
            expected_steps=[
                "upload_document",
                "create_embeddings",
                "store_vectors",
                "retrieve_documents",
                "generate_response",
                "apply_guards"
            ]
        )
        assert_workflow_duration_acceptable(workflow_summary, max_duration=60)
    
    @pytest.mark.asyncio
    async def test_rag_with_multiple_queries(
        self,
        e2e_config,
        test_document_textbook,
        test_queries,
        e2e_cleanup
    ):
        """
        Test RAG workflow with multiple sequential queries.
        """
        service_clients = {
            "document": MockDocumentServiceClient(),
            "embedding": MockEmbeddingServiceClient(),
            "retrieval": MockRetrievalServiceClient(),
            "generation": MockGenerationServiceClient(),
            "guard": MockGuardServiceClient(),
        }
        
        storage_clients = {
            "qdrant": MockQdrantClient(),
        }
        
        orchestrator = WorkflowOrchestrator(service_clients, storage_clients)
        
        # Ingest document
        ingestion_result = await ingest_document_workflow(
            document_client=service_clients["document"],
            embedding_client=service_clients["embedding"],
            qdrant_client=storage_clients["qdrant"],
            document_data=test_document_textbook,
            orchestrator=orchestrator
        )
        
        # Process multiple queries
        query_results = []
        for query_data in test_queries:
            rag_result = await rag_workflow(
                retrieval_client=service_clients["retrieval"],
                generation_client=service_clients["generation"],
                guard_client=service_clients["guard"],
                query=query_data["query"],
                orchestrator=orchestrator
            )
            
            assert_rag_response_valid(rag_result)
            assert_guard_checks_passed(rag_result["guard_checks"])
            assert_sources_relevant(
                rag_result["sources"],
                query_data["query"],
                min_relevance=0.5
            )
            
            query_results.append(rag_result)
        
        # Verify all queries were processed
        assert len(query_results) == len(test_queries)
        
        # Cleanup
        async def cleanup_document():
            await service_clients["document"].delete_document(ingestion_result["document_id"])
        e2e_cleanup(cleanup_document)
    
    @pytest.mark.asyncio
    async def test_rag_guard_rails_blocking(
        self,
        e2e_config,
        test_document_science,
        e2e_cleanup
    ):
        """
        Test that guard rails properly block inappropriate responses.
        """
        service_clients = {
            "document": MockDocumentServiceClient(),
            "embedding": MockEmbeddingServiceClient(),
            "retrieval": MockRetrievalServiceClient(),
            "generation": MockGenerationServiceClient(),
            "guard": MockGuardServiceClient(should_block=True),
        }
        
        storage_clients = {
            "qdrant": MockQdrantClient(),
        }
        
        orchestrator = WorkflowOrchestrator(service_clients, storage_clients)
        
        # Ingest document
        ingestion_result = await ingest_document_workflow(
            document_client=service_clients["document"],
            embedding_client=service_clients["embedding"],
            qdrant_client=storage_clients["qdrant"],
            document_data=test_document_science,
            orchestrator=orchestrator
        )
        
        # Execute RAG with query that should be blocked
        rag_result = await rag_workflow(
            retrieval_client=service_clients["retrieval"],
            generation_client=service_clients["generation"],
            guard_client=service_clients["guard"],
            query="Inappropriate query",
            orchestrator=orchestrator
        )
        
        # Verify guard rails blocked the response
        assert rag_result["status"] == "blocked"
        assert rag_result["guard_checks"]["passed"] is False
        
        # Cleanup
        async def cleanup_document():
            await service_clients["document"].delete_document(ingestion_result["document_id"])
        e2e_cleanup(cleanup_document)


# Mock clients for testing (would be replaced with real clients)
class MockDocumentServiceClient:
    """Mock document service client for testing."""
    
    async def upload_document(self, title, content, metadata=None):
        return {
            "document_id": "mock-doc-001",
            "status": "uploaded",
            "title": title
        }
    
    async def delete_document(self, document_id):
        return {"status": "deleted"}


class MockEmbeddingServiceClient:
    """Mock embedding service client for testing."""
    
    async def batch_create_embeddings(self, texts):
        return {
            "embeddings": [
                {
                    "embedding_id": f"mock-emb-{i}",
                    "vector": [0.1] * 1024,
                    "model": "mock-model"
                }
                for i in range(len(texts))
            ]
        }


class MockQdrantClient:
    """Mock Qdrant client for testing."""
    
    async def insert_vectors(self, collection_name, vectors, payloads, ids):
        return ids


class MockRetrievalServiceClient:
    """Mock retrieval service client for testing."""
    
    async def search(self, query, limit=5):
        return {
            "results": [
                {
                    "document_id": "mock-doc-001",
                    "chunk_id": "mock-chunk-001",
                    "score": 0.95,
                    "content": "Mock relevant content"
                }
            ]
        }


class MockGenerationServiceClient:
    """Mock generation service client for testing."""
    
    async def generate_with_rag(self, query, retrieved_docs):
        return {
            "response": f"Mock response to: {query}",
            "sources": [doc["document_id"] for doc in retrieved_docs]
        }


class MockGuardServiceClient:
    """Mock guard service client for testing."""
    
    def __init__(self, should_block=False):
        self.should_block = should_block
    
    async def check_response(self, response, context):
        return {
            "passed": not self.should_block,
            "checks": {
                "safety": {"status": "passed" if not self.should_block else "blocked"},
                "quality": {"status": "passed"},
                "accuracy": {"status": "passed"}
            }
        }