"""
Response validator for validating generated responses
Supports hallucination detection, relevance scoring, and quality checks
"""
import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ResponseValidator:
    """Validator for generated responses"""
    
    def __init__(self):
        """Initialize response validator"""
        logger.info("Initializing response validator")
        
        # Hallucination indicators (simplified)
        self.hallucination_indicators = [
            r"Saya tidak memiliki informasi",
            r"Tidak ada dalam konteks",
            r"Saya tidak tahu",
            r"Mungkin",
            r"Kemungkinan",
            r"Sepertinya"
        ]
    
    async def validate(
        self,
        response: str,
        context: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate generated response
        
        Args:
            response: Generated response
            context: Context information
            documents: Source documents
        
        Returns:
            Validation results
        """
        try:
            # Perform various validations
            hallucination_score = await self._detect_hallucination(response, documents)
            relevance_score = await self._check_relevance(response, context)
            quality_score = await self._check_quality(response)
            
            # Overall validity
            is_valid = (
                hallucination_score < 0.3 and
                relevance_score > 0.5 and
                quality_score > 0.5
            )
            
            confidence = (1 - hallucination_score) * relevance_score * quality_score
            
            # Collect issues
            issues = []
            if hallucination_score > 0.3:
                issues.append({
                    "type": "hallucination",
                    "severity": "high" if hallucination_score > 0.5 else "medium",
                    "message": f"High hallucination risk detected (score: {hallucination_score:.2f})"
                })
            if relevance_score < 0.5:
                issues.append({
                    "type": "relevance",
                    "severity": "high" if relevance_score < 0.3 else "medium",
                    "message": f"Low relevance to context (score: {relevance_score:.2f})"
                })
            if quality_score < 0.5:
                issues.append({
                    "type": "quality",
                    "severity": "medium",
                    "message": f"Low response quality (score: {quality_score:.2f})"
                })
            
            result = {
                "is_valid": is_valid,
                "confidence": confidence,
                "issues": issues,
                "hallucination_score": hallucination_score,
                "relevance_score": relevance_score,
                "quality_score": quality_score
            }
            
            logger.info(f"Validation completed. Valid: {is_valid}, Confidence: {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in validation: {str(e)}")
            raise
    
    async def _detect_hallucination(
        self,
        response: str,
        documents: List[Dict[str, Any]]
    ) -> float:
        """
        Detect hallucinations in response
        
        Args:
            response: Generated response
            documents: Source documents
        
        Returns:
            Hallucination score (0-1, higher = more likely hallucination)
        """
        try:
            score = 0.0
            response_lower = response.lower()
            
            # Check for hallucination indicators
            for indicator in self.hallucination_indicators:
                if re.search(indicator, response_lower):
                    score += 0.1
            
            # Check for factual consistency with documents
            if documents:
                document_text = " ".join([doc.get("content", "") for doc in documents])
                document_words = set(document_text.lower().split())
                response_words = set(response_lower.split())
                
                # Calculate overlap
                overlap = len(document_words & response_words)
                response_word_count = len(response_words)
                
                if response_word_count > 0:
                    overlap_ratio = overlap / response_word_count
                    # Low overlap might indicate hallucination
                    if overlap_ratio < 0.2:
                        score += 0.3
                    elif overlap_ratio < 0.4:
                        score += 0.1
            
            # Cap score at 1.0
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error detecting hallucination: {str(e)}")
            return 0.5  # Medium risk on error
    
    async def _check_relevance(
        self,
        response: str,
        context: str
    ) -> float:
        """
        Check relevance of response to context
        
        Args:
            response: Generated response
            context: Context information
        
        Returns:
            Relevance score (0-1, higher = more relevant)
        """
        try:
            if not context:
                return 0.5  # Neutral if no context
            
            response_lower = response.lower()
            context_lower = context.lower()
            
            # Calculate word overlap
            response_words = set(response_lower.split())
            context_words = set(context_lower.split())
            
            overlap = len(response_words & context_words)
            
            if len(response_words) == 0:
                return 0.0
            
            overlap_ratio = overlap / len(response_words)
            
            # Additional checks
            # Check if response addresses key terms from context
            key_terms = ["topik", "konsep", "materi", "pelajaran"]
            key_term_present = any(term in response_lower for term in key_terms)
            
            if key_term_present:
                overlap_ratio += 0.1
            
            return min(overlap_ratio, 1.0)
            
        except Exception as e:
            logger.error(f"Error checking relevance: {str(e)}")
            return 0.5
    
    async def _check_quality(self, response: str) -> float:
        """
        Check quality of response
        
        Args:
            response: Generated response
        
        Returns:
            Quality score (0-1, higher = better quality)
        """
        try:
            score = 0.0
            
            # Length check (not too short, not too long)
            word_count = len(response.split())
            if 50 <= word_count <= 500:
                score += 0.3
            elif word_count >= 20:
                score += 0.1
            
            # Structure check (has sentences)
            sentences = re.split(r'[.!?]+', response)
            if len(sentences) >= 2:
                score += 0.2
            
            # Coherence check (basic)
            # Check for transition words
            transition_words = ["karena", "sehingga", "namun", "selain itu", "oleh karena itu"]
            transition_count = sum(1 for word in transition_words if word in response.lower())
            if transition_count >= 1:
                score += 0.2
            
            # Language check (basic Indonesian)
            indonesian_words = ["dan", "atau", "tetapi", "karena", "yang", "untuk"]
            indonesian_count = sum(1 for word in indonesian_words if word in response.lower())
            if indonesian_count >= 2:
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error checking quality: {str(e)}")
            return 0.5
    
    async def check_coherence(self, response: str) -> float:
        """
        Check coherence of response
        
        Args:
            response: Generated response
        
        Returns:
            Coherence score (0-1)
        """
        try:
            sentences = re.split(r'[.!?]+', response)
            if len(sentences) < 2:
                return 0.5
            
            # Check for logical flow (simplified)
            # In a full implementation, this would use more sophisticated NLP
            coherence_score = 0.5  # Base score
            
            # Check sentence length variety
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            if len(set(sentence_lengths)) > 2:
                coherence_score += 0.2
            
            return min(coherence_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error checking coherence: {str(e)}")
            return 0.5