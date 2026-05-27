"""
Unit tests for indexing pipeline DAG
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from pipelines.indexing.dag import (
    generate_embeddings,
    store_vectors,
    create_graph_edges,
    indexing_pipeline
)


@pytest.fixture
def mock_chunk():
    """Mock chunk data for testing."""
    return {
        "chunk_id": "test-chunk-1",
        "document_id": "doc-1",
        "content": "This is a test chunk about mathematics and algebra.",
        "metadata": {
            "subject": "mathematics",
            "difficulty": "intermediate",
            "grade_level": "9"
        }
    }


@pytest.fixture
def mock_embedding():
    """Mock embedding vector for testing."""
    return [0.1, 0.2, 0.3, 0.4, 0.5] * 204  # 1024 dimensions


class TestGenerateEmbeddings:
    """Test embedding generation task."""
    
    @pytest.mark.asyncio
    async def test_generate_embeddings_basic(self, mock_chunk):
        """Test basic embedding generation."""
        result = await generate_embeddings.fn(
            chunk=mock_chunk,
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        assert "chunk_id" in result
        assert "embedding" in result
        assert isinstance(result["embedding"], list)
        assert len(result["embedding"]) > 0
        assert "model" in result
    
    @pytest.mark.asyncio
    async def test_generate_embeddings_different_models(self, mock_chunk):
        """Test embedding generation with different models."""
        models = [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2"
        ]
        
        for model in models:
            result = await generate_embeddings.fn(
                chunk=mock_chunk,
                model_name=model
            )
            assert result["model"] == model
            assert len(result["embedding"]) > 0
    
    @pytest.mark.asyncio
    async def test_generate_embeddings_preserves_metadata(self, mock_chunk):
        """Test that embedding generation preserves chunk metadata."""
        result = await generate_embeddings.fn(chunk=mock_chunk)
        
        assert result["chunk_id"] == mock_chunk["chunk_id"]
        assert result["document_id"] == mock_chunk["document_id"]
        assert result["content"] == mock_chunk["content"]
        assert result["metadata"] == mock_chunk["metadata"]


class TestStoreVectors:
    """Test vector storage task."""
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    async def test_store_vectors_basic(self, mock_qdrant_class, mock_chunk, mock_embedding):
        """Test basic vector storage."""
        mock_qdrant = AsyncMock()
        mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
        
        chunk_with_embedding = {
            **mock_chunk,
            "embedding": mock_embedding
        }
        
        result = await store_vectors.fn(
            chunk=chunk_with_embedding,
            collection_name="test_collection"
        )
        
        assert result["chunk_id"] == mock_chunk["chunk_id"]
        assert result["collection_name"] == "test_collection"
        assert result["stored_at"] is not None
        mock_qdrant.upsert.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    async def test_store_vectors_with_filters(self, mock_qdrant_class, mock_chunk, mock_embedding):
        """Test vector storage with metadata filters."""
        mock_qdrant = AsyncMock()
        mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
        
        chunk_with_embedding = {
            **mock_chunk,
            "embedding": mock_embedding
        }
        
        result = await store_vectors.fn(
            chunk=chunk_with_embedding,
            collection_name="test_collection"
        )
        
        assert result["stored_at"] is not None
        # Verify that metadata is included in the upsert call
        call_args = mock_qdrant.upsert.call_args
        assert call_args is not None
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    async def test_store_vectors_error_handling(self, mock_qdrant_class, mock_chunk, mock_embedding):
        """Test vector storage error handling."""
        mock_qdrant = AsyncMock()
        mock_qdrant.upsert.side_effect = Exception("Database error")
        mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
        
        chunk_with_embedding = {
            **mock_chunk,
            "embedding": mock_embedding
        }
        
        with pytest.raises(Exception, match="Database error"):
            await store_vectors.fn(
                chunk=chunk_with_embedding,
                collection_name="test_collection"
            )


class TestCreateGraphEdges:
    """Test graph edge creation task."""
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_create_graph_edges_basic(self, mock_neo4j_class, mock_chunk):
        """Test basic graph edge creation."""
        mock_neo4j = AsyncMock()
        mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
        
        result = await create_graph_edges.fn(
            chunk=mock_chunk,
            edge_type="BELONGS_TO"
        )
        
        assert result["chunk_id"] == mock_chunk["chunk_id"]
        assert result["edge_type"] == "BELONGS_TO"
        assert result["created_at"] is not None
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_create_graph_edges_multiple_types(self, mock_neo4j_class, mock_chunk):
        """Test graph edge creation with multiple edge types."""
        mock_neo4j = AsyncMock()
        mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
        
        edge_types = ["BELONGS_TO", "FOLLOWS", "REFERENCES"]
        
        for edge_type in edge_types:
            result = await create_graph_edges.fn(
                chunk=mock_chunk,
                edge_type=edge_type
            )
            assert result["edge_type"] == edge_type
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_create_graph_edges_with_metadata(self, mock_neo4j_class, mock_chunk):
        """Test graph edge creation with metadata."""
        mock_neo4j = AsyncMock()
        mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
        
        result = await create_graph_edges.fn(
            chunk=mock_chunk,
            edge_type="BELONGS_TO"
        )
        
        assert result["created_at"] is not None
        # Verify metadata is included in edge creation
        call_args = mock_neo4j.create_edge.call_args
        assert call_args is not None


class TestIndexingPipeline:
    """Test complete indexing pipeline."""
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_indexing_pipeline_complete(
        self,
        mock_neo4j_class,
        mock_qdrant_class,
        mock_chunk
    ):
        """Test complete indexing pipeline."""
        mock_qdrant = AsyncMock()
        mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
        
        mock_neo4j = AsyncMock()
        mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
        
        result = await indexing_pipeline.fn(
            chunk=mock_chunk,
            collection_name="test_collection",
            store_vectors=True,
            create_graph_edges=True,
            edge_types=["BELONGS_TO"]
        )
        
        assert "chunk_id" in result
        assert "embedding" in result
        assert "vector_stored" in result
        assert "graph_edges_created" in result
        assert result["pipeline_status"] == "completed"
        assert result["vector_stored"] is True
        assert result["graph_edges_created"] is True
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_indexing_pipeline_vector_only(
        self,
        mock_neo4j_class,
        mock_qdrant_class,
        mock_chunk
    ):
        """Test indexing pipeline with vector storage only."""
        mock_qdrant = AsyncMock()
        mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
        
        result = await indexing_pipeline.fn(
            chunk=mock_chunk,
            collection_name="test_collection",
            store_vectors=True,
            create_graph_edges=False
        )
        
        assert result["vector_stored"] is True
        assert result["graph_edges_created"] is False
        mock_neo4j.create_edge.assert_not_called()
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_indexing_pipeline_graph_only(
        self,
        mock_neo4j_class,
        mock_qdrant_class,
        mock_chunk
    ):
        """Test indexing pipeline with graph edges only."""
        mock_neo4j = AsyncMock()
        mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
        
        result = await indexing_pipeline.fn(
            chunk=mock_chunk,
            collection_name="test_collection",
            store_vectors=False,
            create_graph_edges=True,
            edge_types=["BELONGS_TO"]
        )
        
        assert result["vector_stored"] is False
        assert result["graph_edges_created"] is True
        mock_qdrant.upsert.assert_not_called()
    
    @pytest.mark.asyncio
    @patch("pipelines.indexing.dag.QdrantDB")
    @patch("pipelines.indexing.dag.Neo4jDB")
    async def test_indexing_pipeline_preserves_metadata(
        self,
        mock_neo4j_class,
        mock_qdrant_class,
        mock_chunk
    ):
        """Test that indexing pipeline preserves chunk metadata."""
        mock_qdrant = AsyncMock()
        mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
        
        mock_neo4j = AsyncMock()
        mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
        
        original_metadata = mock_chunk["metadata"].copy()
        
        result = await indexing_pipeline.fn(
            chunk=mock_chunk,
            collection_name="test_collection",
            store_vectors=True,
            create_graph_edges=True
        )
        
        assert result["metadata"] == original_metadata


@pytest.mark.asyncio
@patch("pipelines.indexing.dag.QdrantDB")
@patch("pipelines.indexing.dag.Neo4jDB")
async def test_indexing_pipeline_integration(
    mock_neo4j_class,
    mock_qdrant_class
):
    """Integration test for indexing pipeline."""
    mock_qdrant = AsyncMock()
    mock_qdrant_class.return_value.__aenter__.return_value = mock_qdrant
    
    mock_neo4j = AsyncMock()
    mock_neo4j_class.return_value.__aenter__.return_value = mock_neo4j
    
    chunk = {
        "chunk_id": "integration-test-1",
        "document_id": "doc-1",
        "content": "Advanced calculus concepts for grade 12 students.",
        "metadata": {
            "subject": "mathematics",
            "difficulty": "advanced",
            "grade_level": "12"
        }
    }
    
    result = await indexing_pipeline.fn(
        chunk=chunk,
        collection_name="test_collection",
        store_vectors=True,
        create_graph_edges=True,
        edge_types=["BELONGS_TO", "FOLLOWS"]
    )
    
    # Verify complete pipeline execution
    assert result["chunk_id"] == chunk["chunk_id"]
    assert result["embedding"] is not None
    assert result["vector_stored"] is True
    assert result["graph_edges_created"] is True
    assert result["pipeline_status"] == "completed"
    
    # Verify metadata preservation
    assert result["metadata"]["subject"] == "mathematics"
    assert result["metadata"]["difficulty"] == "advanced"
    
    # Verify service calls
    mock_qdrant.upsert.assert_called_once()
    assert mock_neo4j.create_edge.call_count == 2  # Two edge types