"""
Unit tests for Vector Indexing Pipeline
"""
import pytest
from datetime import datetime
from pipelines.indexing.vector_indexing_pipeline import (
    EnrichedDocument,
    VectorIndexer,
    GraphEdgeBuilder,
    IndexingPipeline
)


class TestVectorIndexer:
    """Tests for VectorIndexer"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.indexer = VectorIndexer()
    
    def test_index_document(self):
        """Test document indexing"""
        document = EnrichedDocument(
            id="test_doc",
            content="Test content",
            source="test",
            enriched_metadata={"difficulty": "easy"},
            tags=["easy"],
            difficulty="easy",
            taxonomies=["mathematics"],
            competencies=["understanding"]
        )
        
        result = self.indexer.index_document(document)
        
        assert result.success is True
        assert result.document_id == "test_doc"
        assert result.vector_id == "vec_test_doc"
    
    def test_index_batch(self):
        """Test batch indexing"""
        documents = [
            EnrichedDocument(
                id="doc1",
                content="Content 1",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="easy",
                taxonomies=[],
                competencies=[]
            ),
            EnrichedDocument(
                id="doc2",
                content="Content 2",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="medium",
                taxonomies=[],
                competencies=[]
            )
        ]
        
        results = self.indexer.index_batch(documents)
        
        assert len(results) == 2
        assert all(r.success for r in results)
    
    def test_generate_embedding(self):
        """Test embedding generation"""
        embedding = self.indexer._generate_embedding("test content")
        
        assert isinstance(embedding, list)
        assert len(embedding) == 768
        assert all(isinstance(x, float) for x in embedding)


class TestGraphEdgeBuilder:
    """Tests for GraphEdgeBuilder"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.builder = GraphEdgeBuilder()
    
    def test_build_edges(self):
        """Test edge building"""
        document = EnrichedDocument(
            id="test_doc",
            content="Test content",
            source="test",
            enriched_metadata={},
            tags=["easy"],
            difficulty="easy",
            taxonomies=["mathematics"],
            competencies=["understanding", "application"]
        )
        
        edges = self.builder.build_edges(document)
        
        assert len(edges) > 0
        assert all(edge.source == "test_doc" for edge in edges)
    
    def test_build_batch_edges(self):
        """Test batch edge building"""
        documents = [
            EnrichedDocument(
                id="doc1",
                content="Content 1",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="easy",
                taxonomies=["mathematics"],
                competencies=["understanding"]
            ),
            EnrichedDocument(
                id="doc2",
                content="Content 2",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="medium",
                taxonomies=["science"],
                competencies=["application"]
            )
        ]
        
        edges = self.builder.build_batch_edges(documents)
        
        assert len(edges) > 0
        assert self.builder.edge_count == len(edges)


class TestIndexingPipeline:
    """Tests for IndexingPipeline"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.pipeline = IndexingPipeline()
    
    def test_run_pipeline(self):
        """Test pipeline execution"""
        documents = [
            EnrichedDocument(
                id="doc1",
                content="Test content",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="easy",
                taxonomies=[],
                competencies=[]
            )
        ]
        
        vector_results, graph_edges = self.pipeline.run(documents)
        
        assert len(vector_results) == 1
        assert len(graph_edges) > 0
    
    def test_get_stats(self):
        """Test pipeline statistics"""
        documents = [
            EnrichedDocument(
                id="doc1",
                content="Content 1",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="easy",
                taxonomies=[],
                competencies=[]
            ),
            EnrichedDocument(
                id="doc2",
                content="Content 2",
                source="test",
                enriched_metadata={},
                tags=[],
                difficulty="medium",
                taxonomies=[],
                competencies=[]
            )
        ]
        
        self.pipeline.run(documents)
        stats = self.pipeline.get_stats()
        
        assert stats["vector_indexed"] == 2
        assert stats["graph_edges"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
