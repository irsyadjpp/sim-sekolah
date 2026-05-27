import fitz  # PyMuPDF
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extract text from documents using PyMuPDF"""
    
    def __init__(self):
        """Initialize text extractor"""
        self.supported_formats = ['.pdf', '.txt', '.doc', '.docx']
    
    def extract(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Extract text from document
        
        Args:
            file_path: Path to document file
            options: Extraction options
            
        Returns:
            Extracted text
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.pdf':
                return self._extract_from_pdf(file_path, options)
            elif file_extension == '.txt':
                return self._extract_from_text_file(file_path)
            else:
                logger.warning(f"Text extraction not optimized for {file_extension}, using generic method")
                return self._extract_generic(file_path)
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise
    
    def _extract_from_pdf(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Extract text from PDF using PyMuPDF"""
        options = options or {}
        
        try:
            doc = fitz.open(file_path)
            text_content = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # Extract text with formatting preservation if requested
                if options.get('preserve_formatting', False):
                    text = page.get_text("html")
                else:
                    text = page.get_text("text")
                
                text_content.append(text)
            
            doc.close()
            
            full_text = "\n\n".join(text_content)
            logger.info(f"Extracted {len(full_text)} characters from PDF")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def _extract_from_text_file(self, file_path: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            logger.info(f"Extracted {len(text)} characters from text file")
            return text
            
        except UnicodeDecodeError:
            # Try different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    text = f.read()
                return text
            except Exception as e:
                logger.error(f"Error reading text file: {str(e)}")
                raise
    
    def _extract_generic(self, file_path: str) -> str:
        """Generic text extraction fallback"""
        try:
            # Try to open as text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            logger.info(f"Extracted {len(text)} characters using generic method")
            return text
            
        except Exception as e:
            logger.error(f"Generic text extraction failed: {str(e)}")
            raise
    
    def extract_with_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with document metadata
        
        Args:
            file_path: Path to document file
            
        Returns:
            Dictionary with text and metadata
        """
        try:
            doc = fitz.open(file_path)
            metadata = doc.metadata
            
            text_content = []
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text_content.append(page.get_text("text"))
            
            doc.close()
            
            return {
                "text": "\n\n".join(text_content),
                "metadata": {
                    "title": metadata.get("title"),
                    "author": metadata.get("author"),
                    "subject": metadata.get("subject"),
                    "keywords": metadata.get("keywords", "").split(",") if metadata.get("keywords") else [],
                    "creator": metadata.get("creator"),
                    "producer": metadata.get("producer"),
                    "creation_date": metadata.get("creationDate"),
                    "modification_date": metadata.get("modDate"),
                    "page_count": doc.page_count
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting text with metadata: {str(e)}")
            raise