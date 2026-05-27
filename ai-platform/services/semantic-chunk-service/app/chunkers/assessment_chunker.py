import re
import logging
from typing import Dict, Any, List
import uuid

logger = logging.getLogger(__name__)


class AssessmentChunker:
    """Assessment-based chunker for educational content"""
    
    def __init__(self):
        """Initialize assessment chunker"""
        self.assessment_patterns = [
            r'soal\s+(?:nomor\s+)?(\d+)',  # soal nomor X
            r'pertanyaan\s+(?:ke\-)?(\d+)',  # pertanyaan ke-X
            r'as(?:sesmen)?\s+(?:ke\-)?(\d+)',  # asesmen ke-X
            r'latihan\s+(?:ke\-)?(\d+)',  # latihan ke-X
        ]
        logger.info("Assessment chunker initialized")
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk text based on assessment components"""
        try:
            # Split by question patterns
            chunks = self._split_by_assessments(text)
            
            if not chunks:
                return self._fallback_chunking(text, metadata)
            
            # Build assessment chunks
            result = []
            for i, chunk_text in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                result.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'metadata': {
                        'chunk_id': chunk_id,
                        'chunk_type': 'assessment',
                        'assessment_type': 'question',
                        'question_number': i + 1,
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'chunk_quality_score': 0.8,
                        'educational_value_score': 0.9
                    },
                    'character_count': len(chunk_text),
                    'word_count': len(chunk_text.split()),
                    'position': i,
                    'confidence': 0.8
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error in assessment chunking: {str(e)}")
            return self._fallback_chunking(text, metadata)
    
    def _split_by_assessments(self, text: str) -> List[str]:
        """Split text by assessment indicators"""
        # Simple split by numbering patterns
        chunks = re.split(r'\n(?=\d+[\.\)]\s|\n?Soal\s|n?Pertanyaan\s)', text)
        return [c.strip() for c in chunks if c.strip()]
    
    def _fallback_chunking(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback paragraph chunking"""
        paragraphs = text.split('\n\n')
        chunks = []
        
        for i, para in enumerate(paragraphs):
            if para.strip():
                chunk_id = str(uuid.uuid4())
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': para.strip(),
                    'metadata': {
                        'chunk_id': chunk_id,
                        'chunk_type': 'generic',
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'chunk_quality_score': 0.5,
                        'educational_value_score': 0.5
                    },
                    'character_count': len(para),
                    'word_count': len(para.split()),
                    'position': i,
                    'confidence': 0.5
                })
        
        return chunks