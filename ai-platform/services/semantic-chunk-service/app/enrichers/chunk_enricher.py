import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ChunkEnricher:
    """Enrich chunks with additional educational metadata"""
    
    def __init__(self):
        """Initialize chunk enricher"""
        logger.info("Chunk enricher initialized")
    
    def enrich(self, chunk: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a single chunk with additional metadata"""
        try:
            enriched_chunk = chunk.copy()
            enriched_metadata = chunk.get('metadata', {}).copy()
            
            # Add enrichment information
            enriched_metadata['enriched'] = True
            enriched_metadata['enrichment_timestamp'] = str(__import__('datetime').datetime.utcnow())
            
            # Add subject/grade/phase from document metadata if not present
            if not enriched_metadata.get('subject') and metadata.get('subject'):
                enriched_metadata['subject'] = metadata['subject']
            if not enriched_metadata.get('grade') and metadata.get('grade'):
                enriched_metadata['grade'] = metadata['grade']
            if not enriched_metadata.get('phase') and metadata.get('phase'):
                enriched_metadata['phase'] = metadata['phase']
            
            # Calculate enhanced quality score
            current_quality = enriched_metadata.get('chunk_quality_score', 0.5)
            enhanced_quality = self._calculate_enhanced_quality(chunk, metadata)
            enriched_metadata['enhanced_quality_score'] = enhanced_quality
            
            enriched_chunk['metadata'] = enriched_metadata
            
            return enriched_chunk
            
        except Exception as e:
            logger.error(f"Error enriching chunk: {str(e)}")
            return chunk
    
    def _calculate_enhanced_quality(self, chunk: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Calculate enhanced quality score for chunk"""
        try:
            base_score = chunk.get('metadata', {}).get('chunk_quality_score', 0.5)
            
            # Quality boost factors
            boost = 0.0
            
            # Educational content boost
            if chunk.get('metadata', {}).get('competency'):
                boost += 0.2
            if chunk.get('metadata', {}).get('pedagogy_type'):
                boost += 0.1
            if chunk.get('metadata', {}).get('cognitive_level'):
                boost += 0.1
            
            # Content length boost (optimal length)
            word_count = chunk.get('word_count', 0)
            if 50 <= word_count <= 300:
                boost += 0.1
            elif 30 <= word_count < 50 or 300 < word_count <= 500:
                boost += 0.05
            
            # Metadata completeness boost
            metadata_fields = ['competency', 'pedagogy_type', 'cognitive_level', 'subject', 'grade']
            filled_fields = sum(1 for field in metadata_fields if chunk.get('metadata', {}).get(field))
            boost += (filled_fields / len(metadata_fields)) * 0.1
            
            enhanced_score = min(base_score + boost, 1.0)
            return enhanced_score
            
        except Exception as e:
            logger.error(f"Error calculating enhanced quality: {str(e)}")
            return 0.5