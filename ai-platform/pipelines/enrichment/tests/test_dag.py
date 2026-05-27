"""
Unit tests for enrichment pipeline DAG
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from pipelines.enrichment.dag import (
    extract_difficulty,
    extract_taxonomy,
    extract_competency,
    enrichment_pipeline
)


@pytest.fixture
def mock_chunk():
    """Mock chunk data for testing."""
    return {
        "chunk_id": "test-chunk-1",
        "document_id": "doc-1",
        "content": "This is a complex topic about advanced mathematics and calculus.",
        "metadata": {
            "subject": "mathematics",
            "grade_level": "12"
        }
    }


class TestExtractDifficulty:
    """Test difficulty extraction task."""
    
    @pytest.mark.asyncio
    async def test_extract_difficulty_basic(self, mock_chunk):
        """Test basic difficulty extraction."""
        result = await extract_difficulty.fn(mock_chunk)
        
        assert "difficulty" in result
        assert result["difficulty"] in ["beginner", "intermediate", "advanced"]
        assert "chunk_id" in result
        assert result["chunk_id"] == mock_chunk["chunk_id"]
    
    @pytest.mark.asyncio
    async def test_extract_difficulty_with_keywords(self):
        """Test difficulty extraction with specific keywords."""
        chunk = {
            "chunk_id": "test-1",
            "content": "Basic introduction to simple concepts for beginners.",
            "metadata": {}
        }
        
        result = await extract_difficulty.fn(chunk)
        assert result["difficulty"] == "beginner"
    
    @pytest.mark.asyncio
    async def test_extract_difficulty_advanced_keywords(self):
        """Test difficulty extraction with advanced keywords."""
        chunk = {
            "chunk_id": "test-2",
            "content": "Advanced quantum mechanics and theoretical physics.",
            "metadata": {}
        }
        
        result = await extract_difficulty.fn(chunk)
        assert result["difficulty"] == "advanced"


class TestExtractTaxonomy:
    """Test taxonomy extraction task."""
    
    @pytest.mark.asyncio
    async def test_extract_taxonomy_basic(self, mock_chunk):
        """Test basic taxonomy extraction."""
        result = await extract_taxonomy.fn(mock_chunk)
        
        assert "taxonomy" in result
        assert isinstance(result["taxonomy"], dict)
        assert "chunk_id" in result
    
    @pytest.mark.asyncio
    async def test_extract_taxonomy_with_subject(self):
        """Test taxonomy extraction with subject metadata."""
        chunk = {
            "chunk_id": "test-1",
            "content": "Photosynthesis is the process plants use to make food.",
            "metadata": {"subject": "biology"}
        }
        
        result = await extract_taxonomy.fn(chunk)
        assert result["taxonomy"]["subject"] == "biology"
    
    @pytest.mark.asyncio
    async def test_extract_taxonomy_auto_detection(self):
        """Test automatic taxonomy detection from content."""
        chunk = {
            "chunk_id": "test-1",
            "content": "The quadratic formula is x = (-b ± √(b² - 4ac)) / 2a",
            "metadata": {}
        }
        
        result = await extract_taxonomy.fn(chunk)
        assert "subject" in result["taxonomy"]
        assert result["taxonomy"]["subject"] == "mathematics"


class TestExtractCompetency:
    """Test competency extraction task."""
    
    @pytest.mark.asyncio
    async def test_extract_competency_basic(self, mock_chunk):
        """Test basic competency extraction."""
        result = await extract_competency.fn(mock_chunk)
        
        assert "competency" in result
        assert isinstance(result["competency"], dict)
        assert "chunk_id" in result
    
    @pytest.mark.asyncio
    async def test_extract_competency_with_grade(self):
        """Test competency extraction with grade level."""
        chunk = {
            "chunk_id": "test-1",
            "content": "Basic arithmetic operations.",
            "metadata": {"grade_level": "3"}
        }
        
        result = await extract_competency.fn(chunk)
        assert result["competency"]["grade_level"] == "3"
    
    @pytest.mark.asyncio
    async def test_extract_competency_skills_detection(self):
        """Test skills detection from content."""
        chunk = {
            "chunk_id": "test-1",
            "content": "Students will learn to solve equations and graph functions.",
            "metadata": {}
        }
        
        result = await extract_competency.fn(chunk)
        assert "skills" in result["competency"]
        assert isinstance(result["competency"]["skills"], list)


class TestEnrichmentPipeline:
    """Test complete enrichment pipeline."""
    
    @pytest.mark.asyncio
    async def test_enrichment_pipeline_single_chunk(self, mock_chunk):
        """Test enrichment pipeline with single chunk."""
        result = await enrichment_pipeline.fn(
            chunk=mock_chunk,
            enrich_difficulty=True,
            enrich_taxonomy=True,
            enrich_competency=True
        )
        
        assert "chunk_id" in result
        assert "metadata" in result
        assert "difficulty" in result["metadata"]
        assert "taxonomy" in result["metadata"]
        assert "competency" in result["metadata"]
        assert "enriched_at" in result
        assert result["pipeline_status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_enrichment_pipeline_selective_enrichment(self, mock_chunk):
        """Test enrichment pipeline with selective enrichment."""
        result = await enrichment_pipeline.fn(
            chunk=mock_chunk,
            enrich_difficulty=True,
            enrich_taxonomy=False,
            enrich_competency=False
        )
        
        assert "difficulty" in result["metadata"]
        assert "taxonomy" not in result["metadata"]
        assert "competency" not in result["metadata"]
    
    @pytest.mark.asyncio
    async def test_enrichment_pipeline_error_handling(self):
        """Test enrichment pipeline error handling."""
        # Test with invalid chunk
        chunk = {
            "chunk_id": "test-1",
            # Missing required fields
        }
        
        with pytest.raises(KeyError):
            await enrichment_pipeline.fn(chunk=chunk)
    
    @pytest.mark.asyncio
    async def test_enrichment_pipeline_preserves_original_data(self, mock_chunk):
        """Test that enrichment pipeline preserves original chunk data."""
        original_content = mock_chunk["content"]
        original_metadata = mock_chunk["metadata"].copy()
        
        result = await enrichment_pipeline.fn(chunk=mock_chunk)
        
        assert result["content"] == original_content
        # Original metadata should be preserved and enriched
        assert result["metadata"]["subject"] == original_metadata["subject"]
        assert result["metadata"]["grade_level"] == original_metadata["grade_level"]


@pytest.mark.asyncio
async def test_enrichment_pipeline_integration():
    """Integration test for enrichment pipeline."""
    chunk = {
        "chunk_id": "integration-test-1",
        "document_id": "doc-1",
        "content": "Advanced calculus concepts including derivatives and integrals for grade 12 students.",
        "metadata": {
            "subject": "mathematics",
            "grade_level": "12",
            "chapter": "calculus"
        }
    }
    
    result = await enrichment_pipeline.fn(
        chunk=chunk,
        enrich_difficulty=True,
        enrich_taxonomy=True,
        enrich_competency=True
    )
    
    # Verify all enrichments
    assert result["metadata"]["difficulty"] == "advanced"
    assert result["metadata"]["taxonomy"]["subject"] == "mathematics"
    assert result["metadata"]["competency"]["grade_level"] == "12"
    assert result["pipeline_status"] == "completed"
    
    # Verify enrichment metadata
    assert result["enriched_at"] is not None
    assert isinstance(result["enriched_at"], str)