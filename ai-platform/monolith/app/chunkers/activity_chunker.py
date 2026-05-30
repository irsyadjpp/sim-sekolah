import re
import logging
from typing import Dict, Any, List
import uuid

logger = logging.getLogger(__name__)


class ActivityChunker:
    """
    Activity-based chunker for educational content
    
    Chunks content based on learning activities (experiments, projects, discussions, etc.)
    """
    
    def __init__(self):
        """Initialize activity chunker"""
        self.activity_patterns = [
            r'kegiatan\s+(.+?)',  # kegiatan X
            r'aktivitas\s+(.+?)',  # aktivitas X
            r'praktikum\s+(.+?)',  # praktikum X
            r'percobaan\s+(.+?)',  # percobaan X
            r'proyek\s+(.+?)',  # proyek X
            r'tugas\s+(.+?)',  # tugas X
            r'diskusi\s+(.+?)',  # diskusi X
        ]
        
        logger.info("Activity chunker initialized")
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk text based on learning activities"""
        try:
            text = self._normalize_text(text)
            
            # Detect activity sections
            activity_sections = self._detect_activity_sections(text)
            
            if not activity_sections:
                return self._fallback_chunking(text, metadata)
            
            # Build chunks from activity sections
            chunks = []
            for section in activity_sections:
                chunk = self._build_activity_chunk(section, metadata)
                chunks.append(chunk)
            
            logger.info(f"Created {len(chunks)} activity-based chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error in activity chunking: {str(e)}")
            raise
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for processing"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _detect_activity_sections(self, text: str) -> List[Dict[str, Any]]:
        """Detect sections that represent activities"""
        sections = []
        paragraphs = text.split('\n\n')
        
        current_activity = None
        activity_content = []
        
        for para in paragraphs:
            new_activity = self._extract_activity(para)
            
            if new_activity:
                if current_activity and activity_content:
                    sections.append({
                        'activity': current_activity,
                        'content': ' '.join(activity_content)
                    })
                
                current_activity = new_activity
                activity_content = [para]
            elif current_activity:
                activity_content.append(para)
        
        if current_activity and activity_content:
            sections.append({
                'activity': current_activity,
                'content': ' '.join(activity_content)
            })
        
        return sections
    
    def _extract_activity(self, text: str) -> str:
        """Extract activity from text"""
        for pattern in self.activity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _build_activity_chunk(self, section: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Build an activity chunk"""
        chunk_id = str(uuid.uuid4())
        content = section['content']
        
        return {
            'chunk_id': chunk_id,
            'text': content,
            'metadata': {
                'chunk_id': chunk_id,
                'chunk_type': 'activity',
                'activity_type': section['activity'],
                'subject': metadata.get('subject'),
                'grade': metadata.get('grade'),
                'chunk_quality_score': 0.7,
                'educational_value_score': 0.75
            },
            'character_count': len(content),
            'word_count': len(content.split()),
            'position': 0,
            'confidence': 0.7
        }
    
    def _fallback_chunking(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback chunking when no activities detected"""
        # Simple paragraph-based chunking
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