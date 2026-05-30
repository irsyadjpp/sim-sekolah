import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentNormalizer:
    """Normalize and clean extracted document content"""
    
    def __init__(self):
        """Initialize content normalizer"""
        pass
    
    def normalize(self, text: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Normalize text content
        
        Args:
            text: Raw text to normalize
            options: Normalization options
            
        Returns:
            Normalized text
        """
        try:
            options = options or {}
            
            if not text:
                return ""
            
            # Apply normalization steps
            normalized = text
            
            # Remove excessive whitespace
            if options.get('remove_extra_whitespace', True):
                normalized = self._remove_extra_whitespace(normalized)
            
            # Normalize line breaks
            if options.get('normalize_line_breaks', True):
                normalized = self._normalize_line_breaks(normalized)
            
            # Remove special characters
            if options.get('remove_special_chars', False):
                normalized = self._remove_special_chars(normalized)
            
            # Fix encoding issues
            if options.get('fix_encoding', True):
                normalized = self._fix_encoding(normalized)
            
            # Normalize quotes
            if options.get('normalize_quotes', True):
                normalized = self._normalize_quotes(normalized)
            
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing content: {str(e)}")
            return text
    
    def _remove_extra_whitespace(self, text: str) -> str:
        """Remove excessive whitespace"""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def _normalize_line_breaks(self, text: str) -> str:
        """Normalize line breaks to Unix style"""
        return text.replace('\r\n', '\n').replace('\r', '\n')
    
    def _remove_special_chars(self, text: str) -> str:
        """Remove special characters but keep basic punctuation"""
        # Keep letters, numbers, spaces, and basic punctuation
        text = re.sub(r'[^\w\s\.\,\?\!\;\:\-\(\)]', '', text)
        return text
    
    def _fix_encoding(self, text: str) -> str:
        """Fix common encoding issues"""
        # Fix common encoding artifacts
        encoding_fixes = {
            'â€™': "'",
            'â€œ': '"',
            'â€\x9d': '"',
            'â€”': '—',
            'â€¢': '•',
            'â€¦': '…',
        }
        
        for artifact, replacement in encoding_fixes.items():
            text = text.replace(artifact, replacement)
        
        return text
    
    def _normalize_quotes(self, text: str) -> str:
        """Normalize quotes to straight quotes"""
        # Replace curly quotes with straight quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        return text
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from document
        
        Args:
            file_path: Path to document file
            
        Returns:
            Document metadata
        """
        try:
            doc = fitz.open(file_path)
            metadata = doc.metadata
            
            # Process metadata
            processed_metadata = {
                "title": metadata.get("title", "").strip(),
                "author": metadata.get("author", "").strip(),
                "subject": metadata.get("subject", "").strip(),
                "keywords": self._parse_keywords(metadata.get("keywords", "")),
                "creator": metadata.get("creator", "").strip(),
                "producer": metadata.get("producer", "").strip(),
                "creation_date": self._parse_date(metadata.get("creationDate")),
                "modification_date": self._parse_date(metadata.get("modDate")),
                "page_count": doc.page_count
            }
            
            # Add additional statistics
            processed_metadata["word_count"] = self._count_words(doc)
            processed_metadata["character_count"] = self._count_characters(doc)
            processed_metadata["language"] = self._detect_language(doc)
            
            doc.close()
            
            return processed_metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            return {}
    
    def _parse_keywords(self, keywords_str: str) -> List[str]:
        """Parse keywords string into list"""
        if not keywords_str:
            return []
        
        # Split by common delimiters
        keywords = re.split(r'[,;|]', keywords_str)
        return [kw.strip() for kw in keywords if kw.strip()]
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        try:
            # Try PDF date format (D:YYYYMMDDHHmmSS)
            if date_str.startswith("D:"):
                date_str = date_str[2:16]  # Extract YYYYMMDDHHmmSS
                return datetime.strptime(date_str, "%Y%m%d%H%M%S")
            
            # Try other common formats
            for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception as e:
            logger.warning(f"Error parsing date '{date_str}': {str(e)}")
            return None
    
    def _count_words(self, doc) -> int:
        """Count total words in document"""
        try:
            word_count = 0
            for page in doc:
                text = page.get_text("text")
                words = text.split()
                word_count += len(words)
            return word_count
        except Exception as e:
            logger.warning(f"Error counting words: {str(e)}")
            return 0
    
    def _count_characters(self, doc) -> int:
        """Count total characters in document"""
        try:
            char_count = 0
            for page in doc:
                text = page.get_text("text")
                char_count += len(text)
            return char_count
        except Exception as e:
            logger.warning(f"Error counting characters: {str(e)}")
            return 0
    
    def _detect_language(self, doc) -> Optional[str]:
        """Detect document language (simplified)"""
        try:
            # This is a placeholder - in production you'd use a proper language detection library
            # For now, we'll assume Indonesian/English based on common patterns
            total_text = ""
            for page in doc:
                total_text += page.get_text("text")
            
            # Simple heuristic - check for Indonesian words
            indonesian_indicators = ['yang', 'dan', 'di', 'ke', 'untuk', 'dengan', 'atau', 'ini', 'itu']
            text_lower = total_text.lower()
            
            indonesian_count = sum(1 for word in indonesian_indicators if word in text_lower)
            
            if indonesian_count > 5:
                return "indonesian"
            else:
                return "english"
                
        except Exception as e:
            logger.warning(f"Error detecting language: {str(e)}")
            return None
    
    def extract_statistics(self, file_path: str) -> Dict[str, Any]:
        """
        Extract document statistics
        
        Args:
            file_path: Path to document file
            
        Returns:
            Document statistics
        """
        try:
            metadata = self.extract_metadata(file_path)
            
            return {
                "total_pages": metadata.get("page_count", 0),
                "total_words": metadata.get("word_count", 0),
                "total_characters": metadata.get("character_count", 0),
                "language_detected": metadata.get("language", "unknown"),
                "avg_words_per_page": metadata.get("word_count", 0) / max(1, metadata.get("page_count", 1)),
                "avg_chars_per_page": metadata.get("character_count", 0) / max(1, metadata.get("page_count", 1))
            }
            
        except Exception as e:
            logger.error(f"Error extracting statistics: {str(e)}")
            return {}