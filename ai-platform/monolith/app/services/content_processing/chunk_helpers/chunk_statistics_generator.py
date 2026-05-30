"""
Chunk Statistics Generator
Helper class for generating statistics from chunked content
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ChunkStatisticsGenerator:
    """Helper class for generating chunk statistics"""
    
    def get_pedagogical_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate pedagogical statistics from chunks"""
        stats = {
            'total_chunks': len(chunks),
            'special_types': {
                'reflection': 0,
                'glossary': 0,
                'rubric': 0,
                'bibliography': 0
            },
            'pedagogical_distribution': {}
        }
        
        for chunk in chunks:
            chunk_type = chunk.get('metadata', {}).get('chunk_type', 'unknown')
            
            # Check for special types
            text = chunk.get('text', '').lower()
            if 'refleksi' in text or 'reflection' in text or 'pertanyaan refleksi' in text:
                stats['special_types']['reflection'] += 1
            if 'glosarium' in text or 'glossary' in text or 'istilah' in text:
                stats['special_types']['glossary'] += 1
            if 'rubrik' in text or 'rubric' in text:
                stats['special_types']['rubric'] += 1
            if 'daftar pustaka' in text or 'bibliografi' in text or 'references' in text:
                stats['special_types']['bibliography'] += 1
            
            # Pedagogical distribution
            stats['pedagogical_distribution'][chunk_type] = stats['pedagogical_distribution'].get(chunk_type, 0) + 1
        
        return stats
    
    def get_bloom_semantic_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate Bloom semantic statistics from chunks"""
        stats = {
            'bloom_distribution': {},
            'high_order_thinking': 0,
            'low_order_thinking': 0
        }
        
        for chunk in chunks:
            bloom_level = chunk.get('metadata', {}).get('bloom_level', 'unknown')
            stats['bloom_distribution'][bloom_level] = stats['bloom_distribution'].get(bloom_level, 0) + 1
            
            # HOTS vs LOTS classification
            if bloom_level in ['C4_ANALYZE', 'C5_EVALUATE', 'C6_CREATE']:
                stats['high_order_thinking'] += 1
            elif bloom_level in ['C1_REMEMBER', 'C2_UNDERSTAND', 'C3_APPLY']:
                stats['low_order_thinking'] += 1
        
        return stats
    
    def get_chunk_classification_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate chunk classification statistics"""
        stats = {
            'assessment_reductions': 0,
            'concept_improvements': 0,
            'classification_accuracy': 0.0
        }
        
        assessment_count = sum(1 for c in chunks if c.get('metadata', {}).get('chunk_type') == 'assessment')
        concept_count = sum(1 for c in chunks if c.get('metadata', {}).get('chunk_type') in ['concept_explanation', 'concept_intro'])
        total = len(chunks)
        
        stats['assessment_count'] = assessment_count
        stats['concept_count'] = concept_count
        stats['classification_accuracy'] = (concept_count / total * 100) if total > 0 else 0
        
        return stats
    
    def get_enhanced_chunk_types(self, chunks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of enhanced chunk types"""
        chunk_types = {}
        for chunk in chunks:
            chunk_type = chunk.get('metadata', {}).get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        return chunk_types