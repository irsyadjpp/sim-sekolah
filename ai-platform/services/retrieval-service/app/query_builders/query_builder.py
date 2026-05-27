"""
Query builder for optimizing and expanding search queries
Supports semantic, synonym, and curriculum-based expansion
"""
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class QueryBuilder:
    """Query builder for optimizing and expanding search queries"""
    
    def __init__(self):
        """Initialize query builder"""
        logger.info("Initializing query builder")
        
        # Simple synonym dictionary (in production, use proper thesaurus)
        self.synonyms = {
            "matematika": ["math", "angka", "hitung"],
            "ipa": ["sains", "science", "alam"],
            "ips": ["sosial", "social"],
            "bahasa": ["language", "sastra"],
            "belajar": ["mempelajari", "pelajaran", "edukasi"],
            "mengajar": ["mendidik", "pengajaran", "instruksi"],
            "ujian": ["tes", "assessment", "evaluasi"],
            "tugas": ["pekerjaan", "latihan", "eksplorasi"]
        }
        
        # Curriculum terms for Kurikulum Merdeka
        self.curriculum_terms = {
            "profil pelajar": ["profil pelajar pancasila", "p5", "projek"],
            "cp": ["capaian pembelajaran"],
            "tp": ["tujuan pembelajaran"],
            "atk": ["aktivitas"],
            "assessment": ["penilaian", "evaluasi"],
            "ki-1": ["spiritual", "agama"],
            "ki-2": ["sosial", "karakter"],
            "ki-3": "pengetahuan",
            "ki-4": "keterampilan"
        }
    
    async def build(
        self,
        query: str,
        expansion_method: str = "semantic",
        num_expansions: int = 3
    ) -> Dict[str, Any]:
        """
        Build optimized query with expansions
        
        Args:
            query: Original query
            expansion_method: Expansion method (semantic, synonym, curriculum, none)
            num_expansions: Number of expansions to generate
        
        Returns:
            Dictionary with optimized query and expansions
        """
        try:
            # Clean and normalize query
            cleaned_query = self._clean_query(query)
            
            # Generate expansions based on method
            expansions = []
            
            if expansion_method == "synonym":
                expansions = self._synonym_expansion(cleaned_query, num_expansions)
            elif expansion_method == "curriculum":
                expansions = self._curriculum_expansion(cleaned_query, num_expansions)
            elif expansion_method == "semantic":
                # In production, this would use embedding similarity
                expansions = self._semantic_expansion(cleaned_query, num_expansions)
            else:
                expansions = []
            
            return {
                "original_query": query,
                "cleaned_query": cleaned_query,
                "expanded_query": self._combine_query(cleaned_query, expansions),
                "expansions": expansions,
                "method": expansion_method,
                "expansion_count": len(expansions)
            }
            
        except Exception as e:
            logger.error(f"Error building query: {str(e)}")
            raise
    
    def _clean_query(self, query: str) -> str:
        """
        Clean and normalize query
        
        Args:
            query: Original query
        
        Returns:
            Cleaned query
        """
        # Convert to lowercase
        query = query.lower()
        
        # Remove extra whitespace
        query = " ".join(query.split())
        
        # Remove special characters (keep alphanumeric and spaces)
        import re
        query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
        
        return query
    
    def _synonym_expansion(self, query: str, num_expansions: int) -> List[str]:
        """
        Generate synonym-based expansions
        
        Args:
            query: Query text
            num_expansions: Number of expansions
        
        Returns:
            List of synonym expansions
        """
        expansions = []
        query_words = query.split()
        
        for word in query_words:
            if word in self.synonyms:
                for synonym in self.synonyms[word][:num_expansions]:
                    expanded = query.replace(word, synonym, 1)
                    if expanded != query:
                        expansions.append(expanded)
        
        return expansions[:num_expansions]
    
    def _curriculum_expansion(self, query: str, num_expansions: int) -> List[str]:
        """
        Generate curriculum-based expansions for Kurikulum Merdeka
        
        Args:
            query: Query text
            num_expansions: Number of expansions
        
        Returns:
            List of curriculum expansions
        """
        expansions = []
        
        for term, related in self.curriculum_terms.items():
            if term in query:
                if isinstance(related, list):
                    for related_term in related[:num_expansions]:
                        expanded = query.replace(term, related_term, 1)
                        if expanded != query:
                            expansions.append(expanded)
                else:
                    expanded = query.replace(term, related, 1)
                    if expanded != query:
                        expansions.append(expanded)
        
        return expansions[:num_expansions]
    
    def _semantic_expansion(self, query: str, num_expansions: int) -> List[str]:
        """
        Generate semantic-based expansions (simplified)
        
        Args:
            query: Query text
            num_expansions: Number of expansions
        
        Returns:
            List of semantic expansions
        """
        # In production, this would use embedding similarity
        # For now, fallback to synonym expansion
        return self._synonym_expansion(query, num_expansions)
    
    def _combine_query(self, original: str, expansions: List[str]) -> str:
        """
        Combine original query with expansions
        
        Args:
            original: Original query
            expansions: List of expansions
        
        Returns:
            Combined query string
        """
        if not expansions:
            return original
        
        # Add expansions as OR clauses
        combined_parts = [original] + expansions
        return " OR ".join(f"({part})" for part in combined_parts)
    
    async def expand_for_educational_context(self, query: str) -> Dict[str, Any]:
        """
        Expand query specifically for educational context
        
        Args:
            query: Original query
        
        Returns:
            Expanded query with educational context
        """
        educational_terms = [
            "pembelajaran", "pendidikan", "kurikulum", 
            "kompetensi", "tujuan", "aktivitas"
        ]
        
        query_lower = query.lower()
        
        # Add educational context if not present
        for term in educational_terms:
            if term not in query_lower:
                return await self.build(
                    query=f"{query} {term}",
                    expansion_method="curriculum",
                    num_expansions=2
                )
        
        return await self.build(
            query=query,
            expansion_method="curriculum",
            num_expansions=3
        )