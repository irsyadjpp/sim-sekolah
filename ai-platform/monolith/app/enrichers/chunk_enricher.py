"""
Basic Chunk Enricher - Only Basic Metadata (Not Semantic Enrichment)

Note: Semantic enrichment (pedagogy, taxonomy, etc.) is now handled by semantic-enrichment-service.
This chunk enricher only adds basic operational metadata required for chunk tracking.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ChunkEnricher:
    """
    Basic chunk enricher - adds only operational metadata.
    
    Semantic enrichment (pedagogy classification, taxonomy tagging, etc.) 
    is now handled by semantic-enrichment-service to maintain proper service boundaries.
    
    This class only provides:
    - Basic metadata fields
    - Timestamps
    - Quality metrics (non-semantic)
    """
    
    def __init__(self):
        """Initialize basic chunk enricher"""
        logger.info("Basic Chunk Enricher initialized - operational metadata only")
    
    def add_basic_metadata(self, chunk: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add basic operational metadata to chunk (NOT semantic enrichment)
        
        Args:
            chunk: Raw chunk data
            metadata: Document metadata
            
        Returns:
            Chunk with basic operational metadata
        """
        try:
            enriched_chunk = chunk.copy()
            chunk_metadata = chunk.get('metadata', {}).copy()
            
            # Add basic operational metadata
            chunk_metadata['enriched'] = True
            chunk_metadata['enrichment_level'] = 'basic'  # Not semantic enrichment
            chunk_metadata['enrichment_timestamp'] = str(__import__('datetime').datetime.utcnow())
            chunk_metadata['enrichment_service'] = 'chunk-service'
            
            # Add document context if not present
            if not chunk_metadata.get('document_id') and metadata.get('document_id'):
                chunk_metadata['document_id'] = metadata['document_id']
            if not chunk_metadata.get('document_type') and metadata.get('document_type'):
                chunk_metadata['document_type'] = metadata['document_type']
            
            # Add basic quality metrics (non-semantic)
            chunk_metadata['basic_quality_score'] = self._calculate_basic_quality(chunk)
            chunk_metadata['word_count'] = len(chunk.get('content', '').split())
            chunk_metadata['char_count'] = len(chunk.get('content', ''))
            
            enriched_chunk['metadata'] = chunk_metadata
            
            return enriched_chunk
            
        except Exception as e:
            logger.error(f"Error adding basic metadata to chunk: {str(e)}")
            return chunk
    
    def _calculate_basic_quality(self, chunk: Dict[str, Any]) -> float:
        """
        Calculate basic quality score (non-semantic factors)
        
        Considers only operational quality:
        - Content length
        - Text structure
        - Completeness
        
        NOT: pedagogy, taxonomy, cognitive level (those are semantic enrichment)
        """
        try:
            content = chunk.get('content', '')
            
            # Basic quality factors
            score = 0.5  # Base score
            
            # Content length factor (optimal: 100-500 words)
            word_count = len(content.split())
            if 100 <= word_count <= 500:
                score += 0.2
            elif 50 <= word_count < 100 or 500 < word_count <= 800:
                score += 0.1
            
            # Text structure factor
            if content.strip():  # Has content
                score += 0.1
            
            # Completeness factor
            if chunk.get('heading') or chunk.get('section_path'):  # Has context
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating basic quality: {str(e)}")
            return 0.5