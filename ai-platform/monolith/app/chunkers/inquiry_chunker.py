import re
import logging
from typing import Dict, Any, List
import uuid

logger = logging.getLogger(__name__)


class InquiryChunker:
    """Inquiry-based chunker for educational content"""
    
    def __init__(self):
        """Initialize inquiry chunker"""
        self.inquiry_patterns = [
            r'pertanyaan\s+(?:pemandu\s+)?(\d+)',  # pertanyaan pemandu X
            r'inquiri\s+(?:ke\-)?(\d+)',  # inquiri ke-X
            r'penelitian\s+(?:ke\-)?(\d+)',  # penelitian ke-X
            r'hipotesis',  # hipotesis sections
            r'kesimpulan',  # conclusion sections
        ]
        logger.info("Inquiry chunker initialized")
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk text based on inquiry learning components"""
        try:
            # Split by inquiry stages
            chunks = self._split_by_inquiry_stages(text)
            
            if not chunks:
                return self._fallback_chunking(text, metadata)
            
            result = []
            inquiry_stages = ['question', 'hypothesis', 'procedure', 'data', 'conclusion']
            
            for i, chunk_text in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                stage = inquiry_stages[i] if i < len(inquiry_stages) else 'general'
                result.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'metadata': {
                        'chunk_id': chunk_id,
                        'chunk_type': 'inquiry',
                        'inquiry_stage': stage,
                        'pedagogy_type': 'inquiry_learning',
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'chunk_quality_score': 0.75,
                        'educational_value_score': 0.85
                    },
                    'character_count': len(chunk_text),
                    'word_count': len(chunk_text.split()),
                    'position': i,
                    'confidence': 0.75
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error in inquiry chunking: {str(e)}")
            return self._fallback_chunking(text, metadata)
    
    def _split_by_inquiry_stages(self, text: str) -> List[str]:
        """Split text by inquiry learning stages"""
        # Look for stage indicators
        stage_indicators = [
            'pertanyaan', 'hipotesis', 'prosedur', 'data', 'kesimpulan',
            'question', 'hypothesis', 'procedure', 'conclusion'
        ]
        
        chunks = []
        current_chunk = []
        current_stage = None
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            # Check if this line indicates a new stage
            for indicator in stage_indicators:
                if indicator in line_lower:
                    if current_chunk:
                        chunks.append('\n'.join(current_chunk))
                    current_chunk = [line]
                    current_stage = indicator
                    break
            else:
                if current_chunk:
                    current_chunk.append(line)
                else:
                    current_chunk = [line]
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks if chunks else [text]
    
    def _fallback_chunking(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback chunking"""
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
                        'pedagogy_type': 'inquiry_learning',
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'chunk_quality_score': 0.5,
                        'educational_value_score': 0.6
                    },
                    'character_count': len(para),
                    'word_count': len(para.split()),
                    'position': i,
                    'confidence': 0.5
                })
        
        return chunks