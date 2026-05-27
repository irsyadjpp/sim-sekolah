"""
Citation system for managing citations in generated responses
Supports automatic citation extraction and formatting
"""
import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class CitationSystem:
    """System for managing citations in generated responses"""
    
    def __init__(self):
        """Initialize citation system"""
        logger.info("Initializing citation system")
        
        # Citation patterns
        self.citation_patterns = [
            r'\[(\d+)\]',  # [1], [2], etc.
            r'\[([^\]]+)\]',  # [source], [doc1], etc.
            r'\((\d+)\)',  # (1), (2), etc.
            r'\[source:\s*([^\]]+)\]',  # [source: doc1]
        ]
    
    async def build_cited_prompt(
        self,
        prompt: str,
        context: str,
        documents: List[Dict[str, Any]]
    ) -> str:
        """
        Build prompt with citation context
        
        Args:
            prompt: Original prompt
            context: Context information
            documents: List of documents to cite
        
        Returns:
            Built prompt with citations
        """
        try:
            # Add context with numbered references
            cited_context = "Context dengan referensi:\n\n"
            
            for i, doc in enumerate(documents, 1):
                content = doc.get("content", "")
                source = doc.get("source", f"Document {i}")
                cited_context += f"[{i}] {source}: {content}\n\n"
            
            # Build final prompt
            final_prompt = f"""{prompt}

{cited_context}

Instruksi:
- Gunakan informasi dari konteks yang diberikan
- Kutip sumber menggunakan format [1], [2], dll.
- Jangan membuat informasi yang tidak ada dalam konteks
- Jika informasi tidak cukup, jelaskan bahwa informasi tidak tersedia"""

            logger.info(f"Built cited prompt with {len(documents)} documents")
            
            return final_prompt
            
        except Exception as e:
            logger.error(f"Error building cited prompt: {str(e)}")
            raise
    
    async def extract_citations(
        self,
        text: str,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract citations from generated text
        
        Args:
            text: Generated text
            documents: List of documents
        
        Returns:
            List of extracted citations
        """
        try:
            citations = []
            
            # Extract citation markers
            for pattern in self.citation_patterns:
                matches = re.finditer(pattern, text)
                
                for match in matches:
                    citation_ref = match.group(1)
                    
                    # Try to parse as number
                    try:
                        doc_index = int(citation_ref) - 1
                        if 0 <= doc_index < len(documents):
                            doc = documents[doc_index]
                            citations.append({
                                "text": citation_ref,
                                "document_id": doc.get("id", ""),
                                "source": doc.get("source", ""),
                                "position": [match.start(), match.end()]
                            })
                    except ValueError:
                        # Not a number, try to match by source name
                        for doc in documents:
                            if citation_ref.lower() in doc.get("source", "").lower():
                                citations.append({
                                    "text": citation_ref,
                                    "document_id": doc.get("id", ""),
                                    "source": doc.get("source", ""),
                                    "position": [match.start(), match.end()]
                                })
                                break
            
            logger.info(f"Extracted {len(citations)} citations")
            
            return citations
            
        except Exception as e:
            logger.error(f"Error extracting citations: {str(e)}")
            return []
    
    async def format_citations(
        self,
        citations: List[Dict[str, Any]],
        style: str = "numeric"
    ) -> str:
        """
        Format citations for output
        
        Args:
            citations: List of citations
            style: Citation style (numeric, apa, mla)
        
        Returns:
            Formatted citation string
        """
        try:
            if style == "numeric":
                return self._format_numeric(citations)
            elif style == "apa":
                return self._format_apa(citations)
            elif style == "mla":
                return self._format_mla(citations)
            else:
                return self._format_numeric(citations)
                
        except Exception as e:
            logger.error(f"Error formatting citations: {str(e)}")
            return ""
    
    def _format_numeric(self, citations: List[Dict[str, Any]]) -> str:
        """Format citations in numeric style"""
        formatted = []
        for citation in citations:
            formatted.append(f"[{citation['text']}]")
        return " ".join(formatted)
    
    def _format_apa(self, citations: List[Dict[str, Any]]) -> str:
        """Format citations in APA style"""
        formatted = []
        for i, citation in enumerate(citations):
            formatted.append(f"({citation['source']})")
        return " ".join(formatted)
    
    def _format_mla(self, citations: List[Dict[str, Any]]) -> str:
        """Format citations in MLA style"""
        formatted = []
        for citation in citations:
            formatted.append(f"({citation['source']})")
        return " ".join(formatted)
    
    async def validate_citations(
        self,
        text: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate citations in text
        
        Args:
            text: Text with citations
            documents: Available documents
        
        Returns:
            Validation results
        """
        try:
            citations = await self.extract_citations(text, documents)
            
            # Check for invalid citations
            invalid_citations = []
            for pattern in self.citation_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    try:
                        doc_index = int(match) - 1
                        if doc_index < 0 or doc_index >= len(documents):
                            invalid_citations.append(match)
                    except ValueError:
                        # Non-numeric citation, skip validation
                        pass
            
            return {
                "valid": len(invalid_citations) == 0,
                "citation_count": len(citations),
                "invalid_citations": invalid_citations,
                "coverage": len(citations) / len(documents) if documents else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error validating citations: {str(e)}")
            return {
                "valid": False,
                "error": str(e)
            }