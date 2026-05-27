"""
Unit tests for Metadata Tagging Pipeline
"""
import pytest
from datetime import datetime
from pipelines.enrichment.metadata_tagging_pipeline import Document, MetadataTagger, EnrichmentPipeline


class TestMetadataTagger:
    """Tests for MetadataTagger"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.tagger = MetadataTagger()
    
    def test_tag_document_basic(self):
        """Test basic document tagging"""
        document = Document(
            id="test_doc",
            content="This is a basic introduction to numbers for beginners.",
            source="knowledge/cp",
            metadata={"grade": "1"}
        )
        
        enriched = self.tagger.tag_document(document)
        
        assert enriched.id == "test_doc"
        assert enriched.difficulty in ["easy", "medium", "hard"]
        assert isinstance(enriched.taxonomies, list)
        assert isinstance(enriched.competencies, list)
        assert isinstance(enriched.tags, list)
    
    def test_determine_difficulty_easy(self):
        """Test difficulty detection for easy content"""
        content = "basic introduction fundamental simple beginner"
        difficulty = self.tagger._determine_difficulty(content)
        assert difficulty == "easy"
    
    def test_determine_difficulty_medium(self):
        """Test difficulty detection for medium content"""
        content = "intermediate practice apply develop build"
        difficulty = self.tagger._determine_difficulty(content)
        assert difficulty == "medium"
    
    def test_determine_difficulty_hard(self):
        """Test difficulty detection for hard content"""
        content = "advanced complex analyze evaluate create synthesize"
        difficulty = self.tagger._determine_difficulty(content)
        assert difficulty == "hard"
    
    def test_determine_taxonomies_mathematics(self):
        """Test taxonomy detection for mathematics"""
        content = "number algebra geometry measurement statistics"
        taxonomies = self.tagger._determine_taxonomies(content)
        assert "mathematics" in taxonomies
    
    def test_determine_taxonomies_science(self):
        """Test taxonomy detection for science"""
        content = "biology physics chemistry earth space"
        taxonomies = self.tagger._determine_taxonomies(content)
        assert "science" in taxonomies
    
    def test_extract_competencies(self):
        """Test competency extraction"""
        content = "Students will understand and apply concepts to analyze and create solutions."
        competencies = self.tagger._extract_competencies(content)
        assert "understanding" in competencies
        assert "application" in competencies
        assert "analysis" in competencies
        assert "creation" in competencies
    
    def test_tag_batch(self):
        """Test batch tagging"""
        documents = [
            Document(id="doc1", content="Basic introduction", source="test", metadata={}),
            Document(id="doc2", content="Advanced analysis", source="test", metadata={})
        ]
        
        enriched = self.tagger.tag_batch(documents)
        
        assert len(enriched) == 2
        assert enriched[0].id == "doc1"
        assert enriched[1].id == "doc2"


class TestEnrichmentPipeline:
    """Tests for EnrichmentPipeline"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.pipeline = EnrichmentPipeline()
    
    def test_run_pipeline(self):
        """Test pipeline execution"""
        documents = [
            Document(id="doc1", content="Basic introduction", source="test", metadata={})
        ]
        
        enriched = self.pipeline.run(documents)
        
        assert len(enriched) == 1
        assert enriched[0].id == "doc1"
    
    def test_get_stats(self):
        """Test pipeline statistics"""
        documents = [
            Document(id="doc1", content="Basic introduction", source="test", metadata={}),
            Document(id="doc2", content="Advanced analysis", source="test", metadata={})
        ]
        
        self.pipeline.run(documents)
        stats = self.pipeline.get_stats()
        
        assert stats["processed"] == 2
        assert stats["failed"] == 0
        assert stats["success_rate"] == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
