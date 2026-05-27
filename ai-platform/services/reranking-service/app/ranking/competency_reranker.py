"""
Competency-aware reranker based on Kurikulum Merdeka core competencies (KI-1 to KI-4)
Re-ranks documents based on competency type and Bloom's taxonomy level
"""
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CompetencyReranker:
    """Competency-aware reranker for Kurikulum Merdeka"""
    
    def __init__(self):
        """Initialize competency reranker"""
        logger.info("Initializing competency-aware reranker")
        
        # Competency type weights (KI-1 to KI-4)
        self.competency_weights = {
            "KI-1": {
                "KI-1": 1.0,
                "KI-2": 0.6,
                "KI-3": 0.3,
                "KI-4": 0.3
            },
            "KI-2": {
                "KI-1": 0.6,
                "KI-2": 1.0,
                "KI-3": 0.4,
                "KI-4": 0.4
            },
            "KI-3": {
                "KI-1": 0.3,
                "KI-2": 0.4,
                "KI-3": 1.0,
                "KI-4": 0.7
            },
            "KI-4": {
                "KI-1": 0.3,
                "KI-2": 0.4,
                "KI-3": 0.7,
                "KI-4": 1.0
            }
        }
        
        # Bloom's taxonomy hierarchy (lower to higher)
        self.bloom_hierarchy = {
            "remember": 1,
            "understand": 2,
            "apply": 3,
            "analyze": 4,
            "evaluate": 5,
            "create": 6
        }
        
        # Bloom's taxonomy alignment weights
        self.bloom_weights = {
            "remember": {
                "remember": 1.0,
                "understand": 0.8,
                "apply": 0.6,
                "analyze": 0.4,
                "evaluate": 0.3,
                "create": 0.2
            },
            "understand": {
                "remember": 0.7,
                "understand": 1.0,
                "apply": 0.8,
                "analyze": 0.6,
                "evaluate": 0.5,
                "create": 0.3
            },
            "apply": {
                "remember": 0.5,
                "understand": 0.7,
                "apply": 1.0,
                "analyze": 0.8,
                "evaluate": 0.7,
                "create": 0.6
            },
            "analyze": {
                "remember": 0.3,
                "understand": 0.5,
                "apply": 0.7,
                "analyze": 1.0,
                "evaluate": 0.8,
                "create": 0.7
            },
            "evaluate": {
                "remember": 0.2,
                "understand": 0.4,
                "apply": 0.6,
                "analyze": 0.8,
                "evaluate": 1.0,
                "create": 0.9
            },
            "create": {
                "remember": 0.2,
                "understand": 0.3,
                "apply": 0.5,
                "analyze": 0.7,
                "evaluate": 0.9,
                "create": 1.0
            }
        }
    
    async def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        competency_type: str,
        bloom_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using competency-aware strategy
        
        Args:
            query: Search query
            documents: List of documents
            competency_type: Target competency type (KI-1 to KI-4)
            bloom_level: Optional Bloom's taxonomy level
        
        Returns:
            List of reranked documents
        """
        try:
            scored_documents = []
            
            for doc in documents:
                metadata = doc.get("metadata", {})
                original_score = doc.get("score", 0.0)
                
                # Calculate competency alignment score
                competency_score = self._calculate_competency_score(
                    metadata=metadata,
                    competency_type=competency_type,
                    bloom_level=bloom_level
                )
                
                # Combine original score with competency score
                combined_score = 0.6 * original_score + 0.4 * competency_score
                
                scored_doc = doc.copy()
                scored_doc["rerank_score"] = combined_score
                scored_doc["competency_score"] = competency_score
                scored_documents.append(scored_doc)
            
            # Sort by combined score (descending)
            scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
            
            # Add rank
            for i, doc in enumerate(scored_documents):
                doc["rank"] = i + 1
            
            return scored_documents
            
        except Exception as e:
            logger.error(f"Error in competency reranking: {str(e)}")
            raise
    
    def _calculate_competency_score(
        self,
        metadata: Dict[str, Any],
        competency_type: str,
        bloom_level: Optional[str]
    ) -> float:
        """
        Calculate competency alignment score
        
        Args:
            metadata: Document metadata
            competency_type: Target competency type
            bloom_level: Optional Bloom's level
        
        Returns:
            Competency alignment score
        """
        score = 0.0
        score_components = 0
        
        # Competency type alignment
        doc_competency = metadata.get("competency_type", "")
        if competency_type in self.competency_weights:
            comp_weights = self.competency_weights[competency_type]
            if doc_competency in comp_weights:
                score += 0.5 * comp_weights[doc_competency]
            elif not doc_competency:
                score += 0.2  # Neutral if not specified
            else:
                score += 0.1  # Penalty for mismatch
            score_components += 1
        else:
            score += 0.2
        
        # Bloom's taxonomy alignment
        if bloom_level:
            doc_bloom = metadata.get("bloom_taxonomy", "").lower()
            if bloom_level.lower() in self.bloom_weights:
                bloom_weights = self.bloom_weights[bloom_level.lower()]
                if doc_bloom in bloom_weights:
                    score += 0.5 * bloom_weights[doc_bloom]
                elif not doc_bloom:
                    score += 0.2  # Neutral if not specified
                else:
                    score += 0.1  # Penalty for mismatch
                score_components += 1
        else:
            score += 0.2
        
        # Normalize score
        if score_components > 0:
            score = score / score_components
        
        return min(score, 1.0)
    
    async def rerank_by_bloom_progression(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        target_bloom: str,
        include_lower: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents by Bloom's taxonomy progression
        
        Args:
            query: Search query
            documents: List of documents
            target_bloom: Target Bloom's level
            include_lower: Whether to include lower levels
        
        Returns:
            List of reranked documents
        """
        target_level = self.bloom_hierarchy.get(target_bloom.lower(), 3)
        
        scored_documents = []
        
        for doc in documents:
            metadata = doc.get("metadata", {})
            original_score = doc.get("score", 0.0)
            
            # Calculate Bloom level alignment
            doc_bloom = metadata.get("bloom_taxonomy", "").lower()
            doc_level = self.bloom_hierarchy.get(doc_bloom, 3)
            
            if doc_level == target_level:
                bloom_score = 1.0
            elif include_lower and doc_level < target_level:
                # Lower levels get partial credit
                bloom_score = 0.5 + (0.5 * doc_level / target_level)
            else:
                bloom_score = 0.2
            
            combined_score = 0.7 * original_score + 0.3 * bloom_score
            
            scored_doc = doc.copy()
            scored_doc["rerank_score"] = combined_score
            scored_doc["bloom_score"] = bloom_score
            scored_documents.append(scored_doc)
        
        # Sort by combined score
        scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Add rank
        for i, doc in enumerate(scored_documents):
            doc["rank"] = i + 1
        
        return scored_documents