"""
Pedagogy-aware reranker based on learning styles and pedagogical approaches
Re-ranks documents based on VARK learning styles and teaching methods
"""
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PedagogyReranker:
    """Pedagogy-aware reranker based on learning styles"""
    
    def __init__(self):
        """Initialize pedagogy reranker"""
        logger.info("Initializing pedagogy-aware reranker")
        
        # Learning style weights (VARK model)
        self.learning_style_weights = {
            "visual": {
                "visual": 1.0,
                "auditory": 0.3,
                "reading": 0.5,
                "kinesthetic": 0.4
            },
            "auditory": {
                "visual": 0.3,
                "auditory": 1.0,
                "reading": 0.6,
                "kinesthetic": 0.4
            },
            "reading": {
                "visual": 0.4,
                "auditory": 0.5,
                "reading": 1.0,
                "kinesthetic": 0.3
            },
            "kinesthetic": {
                "visual": 0.4,
                "auditory": 0.3,
                "reading": 0.3,
                "kinesthetic": 1.0
            }
        }
        
        # Pedagogy type weights
        self.pedagogy_weights = {
            "direct_instruction": {
                "direct_instruction": 1.0,
                "inquiry_based": 0.6,
                "project_based": 0.5,
                "collaborative": 0.5,
                "problem_based": 0.6,
                "experiential": 0.4
            },
            "inquiry_based": {
                "direct_instruction": 0.4,
                "inquiry_based": 1.0,
                "project_based": 0.8,
                "collaborative": 0.7,
                "problem_based": 0.9,
                "experiential": 0.7
            },
            "project_based": {
                "direct_instruction": 0.3,
                "inquiry_based": 0.8,
                "project_based": 1.0,
                "collaborative": 0.9,
                "problem_based": 0.8,
                "experiential": 0.8
            },
            "collaborative": {
                "direct_instruction": 0.4,
                "inquiry_based": 0.7,
                "project_based": 0.9,
                "collaborative": 1.0,
                "problem_based": 0.8,
                "experiential": 0.8
            },
            "problem_based": {
                "direct_instruction": 0.4,
                "inquiry_based": 0.9,
                "project_based": 0.8,
                "collaborative": 0.8,
                "problem_based": 1.0,
                "experiential": 0.7
            },
            "experiential": {
                "direct_instruction": 0.2,
                "inquiry_based": 0.7,
                "project_based": 0.8,
                "collaborative": 0.8,
                "problem_based": 0.7,
                "experiential": 1.0
            }
        }
    
    async def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        learning_style: Optional[str] = None,
        pedagogy_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using pedagogy-aware strategy
        
        Args:
            query: Search query
            documents: List of documents
            learning_style: Target learning style (VARK)
            pedagogy_type: Target pedagogical approach
        
        Returns:
            List of reranked documents
        """
        try:
            scored_documents = []
            
            for doc in documents:
                metadata = doc.get("metadata", {})
                original_score = doc.get("score", 0.0)
                
                # Calculate pedagogy alignment score
                pedagogy_score = self._calculate_pedagogy_score(
                    metadata=metadata,
                    learning_style=learning_style,
                    pedagogy_type=pedagogy_type
                )
                
                # Combine original score with pedagogy score
                combined_score = 0.6 * original_score + 0.4 * pedagogy_score
                
                scored_doc = doc.copy()
                scored_doc["rerank_score"] = combined_score
                scored_doc["pedagogy_score"] = pedagogy_score
                scored_documents.append(scored_doc)
            
            # Sort by combined score (descending)
            scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
            
            # Add rank
            for i, doc in enumerate(scored_documents):
                doc["rank"] = i + 1
            
            return scored_documents
            
        except Exception as e:
            logger.error(f"Error in pedagogy reranking: {str(e)}")
            raise
    
    def _calculate_pedagogy_score(
        self,
        metadata: Dict[str, Any],
        learning_style: Optional[str],
        pedagogy_type: Optional[str]
    ) -> float:
        """
        Calculate pedagogy alignment score
        
        Args:
            metadata: Document metadata
            learning_style: Target learning style
            pedagogy_type: Target pedagogy type
        
        Returns:
            Pedagogy alignment score
        """
        score = 0.0
        score_components = 0
        
        # Learning style alignment
        if learning_style:
            doc_learning_style = metadata.get("learning_style", "").lower()
            if learning_style.lower() in self.learning_style_weights:
                style_weights = self.learning_style_weights[learning_style.lower()]
                if doc_learning_style in style_weights:
                    score += 0.5 * style_weights[doc_learning_style]
                elif not doc_learning_style:
                    score += 0.2  # Neutral if not specified
                else:
                    score += 0.1  # Penalty for mismatch
                score_components += 1
        else:
            # No learning style specified, check content
            score += 0.2
        
        # Pedagogy type alignment
        if pedagogy_type:
            doc_pedagogy = metadata.get("pedagogy_type", "").lower()
            if pedagogy_type.lower() in self.pedagogy_weights:
                ped_weights = self.pedagogy_weights[pedagogy_type.lower()]
                if doc_pedagogy in ped_weights:
                    score += 0.5 * ped_weights[doc_pedagogy]
                elif not doc_pedagogy:
                    score += 0.2  # Neutral if not specified
                else:
                    score += 0.1  # Penalty for mismatch
                score_components += 1
        else:
            # No pedagogy type specified
            score += 0.2
        
        # Normalize score
        if score_components > 0:
            score = score / score_components
        
        return min(score, 1.0)
    
    async def rerank_by_activity_type(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        activity_type: str
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents by activity type
        
        Args:
            query: Search query
            documents: List of documents
            activity_type: Target activity type (individual, group, class)
        
        Returns:
            List of reranked documents
        """
        scored_documents = []
        
        for doc in documents:
            metadata = doc.get("metadata", {})
            original_score = doc.get("score", 0.0)
            
            # Calculate activity alignment
            doc_activity = metadata.get("activity_type", "").lower()
            if activity_type.lower() == doc_activity:
                activity_score = 1.0
            elif not doc_activity:
                activity_score = 0.5
            else:
                activity_score = 0.2
            
            combined_score = 0.7 * original_score + 0.3 * activity_score
            
            scored_doc = doc.copy()
            scored_doc["rerank_score"] = combined_score
            scored_doc["activity_score"] = activity_score
            scored_documents.append(scored_doc)
        
        # Sort by combined score
        scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Add rank
        for i, doc in enumerate(scored_documents):
            doc["rank"] = i + 1
        
        return scored_documents