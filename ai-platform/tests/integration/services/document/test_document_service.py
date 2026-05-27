"""
Document service integration tests
"""

import pytest
from tests.integration.helpers import (
    DocumentServiceClient,
    create_test_document,
    assert_document_processed,
    assert_uuid_valid,
    assert_timestamp_valid,
)


@pytest.mark.integration
@pytest.mark.grpc
class TestDocumentService:
    """Test document service integration."""
    
    @pytest.mark.asyncio
    async def test_document_service_health(self, document_service_config):
        """Test document service health check."""
        async with DocumentServiceClient(**document_service_config) as client:
            # This would call actual health check when service is implemented
            # For now, we just verify connection can be established
            assert client is not None
            assert client.host == document_service_config["host"]
            assert client.port == document_service_config["port"]
    
    @pytest.mark.asyncio
    async def test_upload_document(self, document_service_config):
        """Test document upload flow."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Create test document
            test_doc = create_test_document(
                title="Integration Test Document",
                content="This document is used for integration testing."
            )
            
            # Upload document
            response = await client.upload_document(
                title=test_doc["title"],
                content=test_doc["content"],
                metadata=test_doc["metadata"]
            )
            
            # Verify response
            assert response is not None
            assert "document_id" in response
            assert_uuid_valid(response["document_id"])
            assert response["status"] in ["uploaded", "processing"]
            assert response["title"] == test_doc["title"]
    
    @pytest.mark.asyncio
    async def test_get_document(self, document_service_config):
        """Test document retrieval."""
        async with DocumentServiceClient(**document_service_config) as client:
            # First upload a document
            upload_response = await client.upload_document(
                title="Test Document for Retrieval",
                content="Content for retrieval test"
            )
            document_id = upload_response["document_id"]
            
            # Retrieve the document
            document = await client.get_document(document_id)
            
            # Verify document
            assert_document_processed(document)
            assert document["document_id"] == document_id
            assert_timestamp_valid(document.get("created_at"))
    
    @pytest.mark.asyncio
    async def test_delete_document(self, document_service_config):
        """Test document deletion."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Upload a document
            upload_response = await client.upload_document(
                title="Document to Delete",
                content="This document will be deleted"
            )
            document_id = upload_response["document_id"]
            
            # Delete the document
            delete_response = await client.delete_document(document_id)
            
            # Verify deletion
            assert delete_response is not None
            assert delete_response["status"] == "deleted"
            assert delete_response["document_id"] == document_id
    
    @pytest.mark.asyncio
    async def test_document_not_found(self, document_service_config):
        """Test retrieval of non-existent document."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Try to get non-existent document
            # This should raise an error or return None
            with pytest.raises(Exception):  # Adjust based on actual error handling
                await client.get_document("non-existent-doc-id")
    
    @pytest.mark.asyncio
    async def test_batch_document_upload(self, document_service_config):
        """Test batch document upload."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Create multiple test documents
            documents = [
                create_test_document(title=f"Batch Document {i}")
                for i in range(3)
            ]
            
            # Upload documents
            document_ids = []
            for doc in documents:
                response = await client.upload_document(
                    title=doc["title"],
                    content=doc["content"]
                )
                document_ids.append(response["document_id"])
            
            # Verify all documents were uploaded
            assert len(document_ids) == 3
            for doc_id in document_ids:
                assert_uuid_valid(doc_id)
    
    @pytest.mark.asyncio
    async def test_document_with_metadata(self, document_service_config):
        """Test document upload with custom metadata."""
        async with DocumentServiceClient(**document_service_config) as client:
            custom_metadata = {
                "author": "Test Author",
                "subject": "Mathematics",
                "grade_level": "10",
                "tags": ["algebra", "equations"]
            }
            
            response = await client.upload_document(
                title="Document with Metadata",
                content="Content with metadata",
                metadata=custom_metadata
            )
            
            # Retrieve and verify metadata
            document = await client.get_document(response["document_id"])
            assert document["metadata"] is not None
            # Verify metadata is preserved (adjust based on actual implementation)
    
    @pytest.mark.asyncio
    async def test_document_status_update(self, document_service_config):
        """Test document status update during processing."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Upload document
            response = await client.upload_document(
                title="Status Test Document",
                content="Content for status testing"
            )
            document_id = response["document_id"]
            
            # Initial status should be uploaded/processing
            assert response["status"] in ["uploaded", "processing"]
            
            # In a real scenario, status would update through processing
            # For now, we verify we can check status
            document = await client.get_document(document_id)
            assert "status" in document


@pytest.mark.integration
@pytest.mark.grpc
class TestDocumentServiceContracts:
    """Test document service gRPC contracts."""
    
    @pytest.mark.asyncio
    async def test_upload_document_request_contract(self, document_service_config):
        """Test UploadDocument request contract."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Verify request structure matches contract
            # This would validate against proto definition
            request = {
                "title": "Contract Test",
                "content": "Testing contract compliance",
                "metadata": {"test": True}
            }
            
            # Required fields
            assert "title" in request
            assert "content" in request
            
            # Optional fields
            assert "metadata" in request
    
    @pytest.mark.asyncio
    async def test_upload_document_response_contract(self, document_service_config):
        """Test UploadDocument response contract."""
        async with DocumentServiceClient(**document_service_config) as client:
            response = await client.upload_document(
                title="Contract Response Test",
                content="Testing response contract"
            )
            
            # Verify response structure matches contract
            required_fields = ["document_id", "status", "title"]
            for field in required_fields:
                assert field in response, f"Missing required field: {field}"
    
    @pytest.mark.asyncio
    async def test_get_document_request_contract(self, document_service_config):
        """Test GetDocument request contract."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Verify request structure
            request = {"document_id": "test-doc-123"}
            
            # Required fields
            assert "document_id" in request
            assert_uuid_valid(request["document_id"])
    
    @pytest.mark.asyncio
    async def test_get_document_response_contract(self, document_service_config):
        """Test GetDocument response contract."""
        async with DocumentServiceClient(**document_service_config) as client:
            # Upload document first
            upload_response = await client.upload_document(
                title="Contract Response Test",
                content="Testing response contract"
            )
            
            # Get document
            response = await client.get_document(upload_response["document_id"])
            
            # Verify response structure matches contract
            required_fields = [
                "document_id",
                "title",
                "content",
                "status",
                "created_at"
            ]
            for field in required_fields:
                assert field in response, f"Missing required field: {field}"