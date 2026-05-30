import re
import logging
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class CompetencyChunker:
    """
    Competency-based chunker for educational content
    
    This is the MOST IMPORTANT chunking strategy - chunks content based on competencies
    rather than arbitrary size or structure
    """
    
    def __init__(self):
        """Initialize competency chunker"""
        # Competency keywords and patterns (Indonesian education context)
        self.competency_patterns = [
            r'memahami\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # memahami X yang
            r'menerangkan\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # menerangkan X yang
            r'menjelaskan\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # menjelaskan X yang
            r'mengidentifikasi\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # mengidentifikasi X yang
            r'menganalisis\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # menganalisis X yang
            r'menerapkan\s+(.+?)\s+(?:untuk|dalam|pada)',  # menerapkan X untuk
            r'menilai\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # menilai X yang
            r'membuat\s+(.+?)\s+(?:yang|yang\s+dapat|untuk)',  # membuat X yang
        ]
        
        # Educational competency indicators
        self.competency_indicators = [
            'kompetensi', 'tujuan pembelajaran', 'capaian pembelajaran',
            'indikator pencapaian', 'kriteria ketuntasan'
        ]
        
        logger.info("Competency chunker initialized")
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk text based on competencies
        
        Args:
            text: Text to chunk
            metadata: Document metadata
            
        Returns:
            List of competency-based chunks
        """
        try:
            # Normalize text
            text = self._normalize_text(text)
            
            # Detect competency sections
            competency_sections = self._detect_competency_sections(text)
            
            if not competency_sections:
                # Fallback to sentence-based chunking
                logger.info("No competency sections detected, using fallback chunking")
                return self._fallback_chunking(text, metadata)
            
            # Build chunks from competency sections
            chunks = []
            for section in competency_sections:
                chunk = self._build_competency_chunk(section, metadata)
                chunks.append(chunk)
            
            logger.info(f"Created {len(chunks)} competency-based chunks")
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error in competency chunking: {str(e)}")
            raise
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for processing"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _detect_competency_sections(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect sections that represent competencies
        
        Returns:
            List of competency sections with position and content
        """
        sections = []
        
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        
        current_competency = None
        competency_content = []
        
        for para_num, paragraph in enumerate(paragraphs):
            # Check if paragraph starts a new competency
            new_competency = self._extract_competency(paragraph)
            
            if new_competency:
                # Save previous competency section
                if current_competency and competency_content:
                    sections.append({
                        'competency': current_competency,
                        'content': ' '.join(competency_content),
                        'start_position': para_num - len(competency_content),
                        'paragraph_count': len(competency_content)
                    })
                
                # Start new competency
                current_competency = new_competency
                competency_content = [paragraph]
            elif current_competency:
                # Add to current competency content
                competency_content.append(paragraph)
        
        # Don't forget the last competency
        if current_competency and competency_content:
            sections.append({
                'competency': current_competency,
                'content': ' '.join(competency_content),
                'start_position': len(paragraphs) - len(competency_content),
                'paragraph_count': len(competency_content)
            })
        
        return sections
    
    def _extract_competency(self, text: str) -> Optional[str]:
        """
        Extract competency from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Competency string or None
        """
        # Check for competency patterns
        for pattern in self.competency_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                competency = match.group(1).strip()
                # Clean up competency text
                competency = self._clean_competency_text(competency)
                return competency
        
        # Check for competency indicators
        for indicator in self.competency_indicators:
            if indicator.lower() in text.lower():
                # Extract text after indicator
                parts = text.split(indicator, 1)
                if len(parts) > 1:
                    competency = parts[1].strip()
                    competency = self._clean_competency_text(competency)
                    if competency:
                        return competency
        
        return None
    
    def _clean_competency_text(self, competency: str) -> str:
        """Clean up competency text"""
        # Remove trailing punctuation
        competency = re.sub(r'[.,;:!]+$', '', competency.strip())
        # Remove common filler words
        competency = re.sub(r'^(yang|yang\s+dapat|untuk)\s+', '', competency, flags=re.IGNORECASE)
        return competency.strip()
    
    def _build_competency_chunk(self, section: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a competency chunk from section data
        
        Args:
            section: Competency section data
            metadata: Document metadata
            
        Returns:
            Complete chunk information
        """
        competency = section['competency']
        content = section['content']
        
        # Generate chunk ID
        chunk_id = str(uuid.uuid4())
        
        # Calculate chunk statistics
        word_count = len(content.split())
        char_count = len(content)
        
        return {
            'chunk_id': chunk_id,
            'text': content,
            'metadata': {
                'chunk_id': chunk_id,
                'chunk_type': 'competency',
                'competency': competency,
                'subject': metadata.get('subject'),
                'grade': metadata.get('grade'),
                'phase': metadata.get('phase'),
                'document_position': section['start_position'],
                'chunk_quality_score': self._calculate_quality_score(content, competency),
                'educational_value_score': 0.8  # High educational value for competency chunks
            },
            'character_count': char_count,
            'word_count': word_count,
            'position': section['start_position'],
            'confidence': 0.8
        }
    
    def _calculate_quality_score(self, content: str, competency: str) -> float:
        """Calculate quality score for competency chunk"""
        score = 0.5  # Base score
        
        # Content length factor (ideal 100-500 words)
        word_count = len(content.split())
        if 100 <= word_count <= 500:
            score += 0.2
        elif 50 <= word_count < 100 or 500 < word_count <= 800:
            score += 0.1
        
        # Competency specificity factor
        if competency and len(competency) > 5:
            score += 0.2
        
        # Educational language factor
        educational_terms = ['peserta didik', 'siswa', 'guru', 'pembelajaran', 'materi']
        if any(term in content.lower() for term in educational_terms):
            score += 0.1
        
        return min(score, 1.0)
    
    def _fallback_chunking(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fallback chunking when no competencies detected
        
        Uses sentence-based chunking as fallback
        """
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        
        current_chunk = []
        current_word_count = 0
        target_size = 100  # words
        
        chunk_id = str(uuid.uuid4())
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_words = len(sentence.split())
            
            if current_word_count + sentence_words > target_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append(self._build_generic_chunk(chunk_text, len(chunks), metadata))
                
                # Start new chunk
                current_chunk = [sentence]
                current_word_count = sentence_words
            else:
                current_chunk.append(sentence)
                current_word_count += sentence_words
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(self._build_generic_chunk(chunk_text, len(chunks), metadata))
        
        logger.info(f"Fallback chunking created {len(chunks)} chunks")
        
        return chunks
    
    def _build_generic_chunk(self, content: str, position: int, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Build a generic chunk without specific competency"""
        chunk_id = str(uuid.uuid4())
        
        return {
            'chunk_id': chunk_id,
            'text': content,
            'metadata': {
                'chunk_id': chunk_id,
                'chunk_type': 'generic',
                'competency': None,
                'subject': metadata.get('subject'),
                'grade': metadata.get('grade'),
                'phase': metadata.get('phase'),
                'document_position': position,
                'chunk_quality_score': 0.5,
                'educational_value_score': 0.5
            },
            'character_count': len(content),
            'word_count': len(content.split()),
            'position': position,
            'confidence': 0.5
        }