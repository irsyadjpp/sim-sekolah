"""
Fallback Chunking Helper
Helper class for fallback chunking strategies
"""
import logging
import re
import uuid
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class FallbackChunkingHelper:
    """Helper class for fallback chunking strategies"""
    
    def fallback_chunking(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback chunking strategy when semantic chunking fails"""
        try:
            # Simple sentence-based chunking
            sentences = re.split(r'[.!?]+', text)
            chunks = []
            
            current_chunk = ""
            chunk_id = 0
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                if len(current_chunk) + len(sentence) < 500:  # Max 500 chars per chunk
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(self._create_fallback_chunk(current_chunk, metadata, chunk_id))
                        chunk_id += 1
                    current_chunk = sentence + ". "
            
            # Don't forget the last chunk
            if current_chunk.strip():
                chunks.append(self._create_fallback_chunk(current_chunk, metadata, chunk_id))
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error in fallback chunking: {e}")
            # Ultimate fallback: single chunk with all text
            return [{
                'chunk_id': str(uuid.uuid4()),
                'text': text,
                'metadata': {
                    'chunk_type': 'ultimate_fallback',
                    'chunk_id': str(uuid.uuid4()),
                    'subject': metadata.get('subject'),
                    'grade': metadata.get('grade'),
                    'chunk_quality_score': 0.3
                },
                'character_count': len(text),
                'word_count': len(text.split()),
                'position': 0,
                'confidence': 0.3
            }]
    
    def _create_fallback_chunk(self, text: str, metadata: Dict[str, Any], position: int) -> Dict[str, Any]:
        """Create a fallback chunk with metadata"""
        return {
            'chunk_id': str(uuid.uuid4()),
            'text': text.strip(),
            'metadata': {
                'chunk_type': 'fallback',
                'chunk_id': str(uuid.uuid4()),
                'subject': metadata.get('subject'),
                'grade': metadata.get('grade'),
                'chunk_quality_score': 0.5
            },
            'character_count': len(text.strip()),
            'word_count': len(text.split()),
            'position': position,
            'confidence': 0.5
        }
    
    def get_chunk_types(self, chunks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of chunk types"""
        chunk_types = {}
        for chunk in chunks:
            chunk_type = chunk.get('metadata', {}).get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        return chunk_types