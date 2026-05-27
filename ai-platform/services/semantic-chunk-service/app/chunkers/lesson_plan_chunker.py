import re
import logging
from typing import Dict, Any, List
import uuid

logger = logging.getLogger(__name__)


class LessonPlanChunker:
    """Lesson plan-based chunker for educational content"""
    
    def __init__(self):
        """Initialize lesson plan chunker"""
        self.lesson_plan_patterns = [
            r'tujuan\s+(?:pembelajaran|)?\s*:',  # tujuan pembelajaran:
            r'materi\s+(?:ajar)?\s*:',  # materi ajar:
            r'kegiatan\s+(?:pembelajaran)?\s*:',  # kegiatan pembelajaran:
            r'metode\s+(?:pembelajaran)?\s*:',  # metode pembelajaran:
            r'penilaian\s*:',  # penilaian:
            r'alat\s+(?:bahan)?\s*:',  # alat/bahan:
        ]
        logger.info("Lesson plan chunker initialized")
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk text based on lesson plan structure"""
        try:
            # Split by lesson plan components
            chunks = self._split_by_lesson_plan_structure(text)
            
            if not chunks:
                return self._fallback_chunking(text, metadata)
            
            result = []
            lesson_plan_components = ['objectives', 'material', 'activity', 'method', 'assessment', 'resources']
            
            for i, chunk_text in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                component = lesson_plan_components[i] if i < len(lesson_plan_components) else 'general'
                result.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'metadata': {
                        'chunk_id': chunk_id,
                        'chunk_type': 'lesson_plan',
                        'lesson_plan_component': component,
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'phase': metadata.get('phase'),
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
            logger.error(f"Error in lesson plan chunking: {str(e)}")
            return self._fallback_chunking(text, metadata)
    
    def _split_by_lesson_plan_structure(self, text: str) -> List[str]:
        """Split text by lesson plan structure"""
        # Look for lesson plan component indicators
        component_patterns = [
            (r'tujuan\s*(?:pembelajaran)?\s*[:.]', 'objectives'),
            (r'materi\s*(?:ajar)?\s*[:.]', 'material'),
            (r'kegiatan\s*(?:pembelajaran)?\s*[:.]', 'activity'),
            (r'metode\s*(?:pembelajaran)?\s*[:.]', 'method'),
            (r'penilaian\s*[:.]', 'assessment'),
            (r'alat\s*(?:bahan)?\s*[:.]', 'resources'),
        ]
        
        chunks = []
        current_chunk = []
        
        lines = text.split('\n')
        for line in lines:
            # Check if this line indicates a new component
            new_component = None
            for pattern, component in component_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    new_component = component
                    break
            
            if new_component:
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
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
                        'lesson_plan_component': 'general',
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'phase': metadata.get('phase'),
                        'chunk_quality_score': 0.5,
                        'educational_value_score': 0.6
                    },
                    'character_count': len(para),
                    'word_count': len(para.split()),
                    'position': i,
                    'confidence': 0.5
                })
        
        return chunks