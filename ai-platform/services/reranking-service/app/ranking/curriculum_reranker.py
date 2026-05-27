"""
Curriculum-aware reranker for Kurikulum Merdeka
Re-ranks documents based on curriculum level, subject, and competency
"""
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CurriculumReranker:
    """Curriculum-aware reranker for Kurikulum Merdeka"""
    
    def __init__(self):
        """Initialize curriculum reranker"""
        logger.info("Initializing curriculum-aware reranker")
        
        # Curriculum level weights (SD, SMP, SMA)
        self.level_weights = {
            "SD": 1.0,
            "SMP": 1.0,
            "SMA": 1.0
        }
        
        # Subject priorities (can be customized)
        self.subject_priorities = {
            "matematika": 1.0,
            "bahasa indonesia": 1.0,
            "ipa": 1.0,
            "ips": 1.0,
            "ppkn": 1.0,
            "seni": 0.9,
            "pjok": 0.9,
            "bahasa inggris": 0.8
        }
        
        # Competency weights (KI-1 to KI-4)
        self.competency_weights = {
            "KI-1": 1.0,  # Spiritual
            "KI-2": 1.0,  # Social
            "KI-3": 1.0,  # Knowledge
            "KI-4": 1.0   # Skills
        }
    
    async def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        curriculum_level: str,
        subject: Optional[str] = None,
        competency_focus: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using curriculum-aware strategy
        
        Args:
            query: Search query
            documents: List of documents
            curriculum_level: Target curriculum level (SD/SMP/SMA)
            subject: Optional target subject
            competency_focus: Optional competency type to focus on
        
        Returns:
            List of reranked documents
        """
        try:
            scored_documents = []
            
            for doc in documents:
                metadata = doc.get("metadata", {})
                original_score = doc.get("score", 0.0)
                
                # Calculate curriculum alignment score
                curriculum_score = self._calculate_curriculum_score(
                    metadata=metadata,
                    curriculum_level=curriculum_level,
                    subject=subject,
                    competency_focus=competency_focus
                )
                
                # Combine original score with curriculum score
                combined_score = 0.6 * original_score + 0.4 * curriculum_score
                
                scored_doc = doc.copy()
                scored_doc["rerank_score"] = combined_score
                scored_doc["curriculum_score"] = curriculum_score
                scored_documents.append(scored_doc)
            
            # Sort by combined score (descending)
            scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
            
            # Add rank
            for i, doc in enumerate(scored_documents):
                doc["rank"] = i + 1
            
            return scored_documents
            
        except Exception as e:
            logger.error(f"Error in curriculum reranking: {str(e)}")
            raise
    
    def _calculate_curriculum_score(
        self,
        metadata: Dict[str, Any],
        curriculum_level: str,
        subject: Optional[str],
        competency_focus: Optional[str]
    ) -> float:
        """
        Calculate curriculum alignment score
        
        Args:
            metadata: Document metadata
            curriculum_level: Target curriculum level
            subject: Optional target subject
            competency_focus: Optional competency type
        
        Returns:
            Curriculum alignment score
        """
        score = 0.0
        
        # Check curriculum level match
        doc_level = metadata.get("curriculum_level", "")
        if doc_level == curriculum_level:
            level_weight = self.level_weights.get(curriculum_level, 1.0)
            score += 0.4 * level_weight
        elif not doc_level:
            # No level specified, neutral
            score += 0.2
        else:
            # Wrong level, penalty
            score += 0.1
        
        # Check subject match
        if subject:
            doc_subject = metadata.get("subject", "").lower()
            if subject.lower() in doc_subject:
                subject_weight = self.subject_priorities.get(subject.lower(), 1.0)
                score += 0.3 * subject_weight
            elif not doc_subject:
                score += 0.1
            else:
                score += 0.05
        
        # Check competency focus
        if competency_focus:
            doc_competency = metadata.get("competency_type", "")
            if doc_competency == competency_focus:
                competency_weight = self.competency_weights.get(competency_focus, 1.0)
                score += 0.3 * competency_weight
            elif not doc_competency:
                score += 0.1
            else:
                score += 0.05
        
        return min(score, 1.0)
    
    async def rerank_by_grade(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        target_grade: int
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents by specific grade level
        
        Args:
            query: Search query
            documents: List of documents
            target_grade: Target grade (1-12)
        
        Returns:
            List of reranked documents
        """
        scored_documents = []
        
        for doc in documents:
            metadata = doc.get("metadata", {})
            original_score = doc.get("score", 0.0)
            
            # Calculate grade alignment
            doc_grade = metadata.get("grade", 0)
            grade_diff = abs(target_grade - doc_grade) if doc_grade else 6
            
            # Closer grades get higher scores
            grade_score = max(0.0, 1.0 - (grade_diff / 12.0))
            
            combined_score = 0.7 * original_score + 0.3 * grade_score
            
            scored_doc = doc.copy()
            scored_doc["rerank_score"] = combined_score
            scored_doc["grade_score"] = grade_score
            scored_documents.append(scored_doc)
        
        # Sort by combined score
        scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Add rank
        for i, doc in enumerate(scored_documents):
            doc["rank"] = i + 1
        
        return scored_documents