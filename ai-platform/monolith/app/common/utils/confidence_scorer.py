"""
Confidence Scoring Utility
Provides confidence scoring mechanisms for AI predictions across all services
"""
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ConfidenceScore:
    """Data class for confidence score with metadata"""
    score: float
    method: str
    confidence_level: str  # 'high', 'medium', 'low'
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "score": self.score,
            "method": self.method,
            "confidence_level": self.confidence_level,
            "metadata": self.metadata
        }


class ConfidenceScorer:
    """Confidence scoring utility for AI predictions"""
    
    # Confidence thresholds
    THRESHOLDS = {
        "high": 0.85,      # High confidence: >= 0.85
        "medium": 0.65,    # Medium confidence: 0.65-0.84
        "low": 0.40,       # Low confidence: 0.40-0.64
        "reject": 0.40     # Reject: < 0.40
    }
    
    def __init__(self, default_threshold: float = 0.65):
        """
        Initialize confidence scorer
        
        Args:
            default_threshold: Minimum confidence threshold for accepting predictions
        """
        self.default_threshold = default_threshold
        logger.info(f"ConfidenceScorer initialized with default threshold: {default_threshold}")
    
    def calculate_pattern_match_confidence(self, pattern: str, content: str, 
                                          content_length: int) -> ConfidenceScore:
        """
        Calculate confidence based on pattern match strength
        
        Args:
            pattern: Regex pattern that was matched
            content: Content text
            content_length: Length of content
            
        Returns:
            ConfidenceScore object
        """
        try:
            # Base score for pattern match
            base_score = 0.75
            
            # Adjust based on pattern complexity
            pattern_complexity = len(pattern.split())
            if pattern_complexity > 2:
                base_score += 0.10  # More complex patterns = higher confidence
            elif pattern_complexity > 1:
                base_score += 0.05
            
            # Adjust based on content length (longer content = more context)
            if content_length > 100:
                base_score += 0.05
            elif content_length > 50:
                base_score += 0.02
            
            # Normalize to [0, 1]
            normalized_score = min(1.0, max(0.0, base_score))
            
            confidence_level = self._get_confidence_level(normalized_score)
            
            metadata = {
                "pattern_complexity": pattern_complexity,
                "content_length": content_length,
                "base_score": base_score,
                "calculated_at": datetime.utcnow().isoformat()
            }
            
            return ConfidenceScore(
                score=normalized_score,
                method="pattern_match",
                confidence_level=confidence_level,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error calculating pattern match confidence: {str(e)}")
            return ConfidenceScore(
                score=0.5,
                method="pattern_match_fallback",
                confidence_level="low",
                metadata={"error": str(e)}
            )
    
    def calculate_semantic_confidence(self, content: str, matched_terms: List[str],
                                    context_relevance: float = 0.8) -> ConfidenceScore:
        """
        Calculate confidence based on semantic relevance
        
        Args:
            content: Content text
            matched_terms: List of matched terms
            context_relevance: Context relevance score (0-1)
            
        Returns:
            ConfidenceScore object
        """
        try:
            if not matched_terms:
                return ConfidenceScore(
                    score=0.0,
                    method="semantic",
                    confidence_level="reject",
                    metadata={"matched_terms_count": 0}
                )
            
            # Base score from term matches
            term_density = len(matched_terms) / max(1, len(content.split()))
            term_score = min(1.0, term_density * 10)  # Scale up for meaningful scores
            
            # Combine with context relevance
            combined_score = (term_score * 0.4) + (context_relevance * 0.6)
            
            # Normalize to [0, 1]
            normalized_score = min(1.0, max(0.0, combined_score))
            
            confidence_level = self._get_confidence_level(normalized_score)
            
            metadata = {
                "matched_terms_count": len(matched_terms),
                "term_density": term_density,
                "context_relevance": context_relevance,
                "calculated_at": datetime.utcnow().isoformat()
            }
            
            return ConfidenceScore(
                score=normalized_score,
                method="semantic",
                confidence_level=confidence_level,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error calculating semantic confidence: {str(e)}")
            return ConfidenceScore(
                score=0.5,
                method="semantic_fallback",
                confidence_level="low",
                metadata={"error": str(e)}
            )
    
    def calculate_ensemble_confidence(self, confidence_scores: List[float],
                                     weights: Optional[List[float]] = None) -> ConfidenceScore:
        """
        Calculate ensemble confidence from multiple confidence scores
        
        Args:
            confidence_scores: List of confidence scores to combine
            weights: Optional weights for each score (default: equal weights)
            
        Returns:
            ConfidenceScore object
        """
        try:
            if not confidence_scores:
                return ConfidenceScore(
                    score=0.0,
                    method="ensemble",
                    confidence_level="reject",
                    metadata={"input_scores_count": 0}
                )
            
            if weights is None:
                weights = [1.0 / len(confidence_scores)] * len(confidence_scores)
            
            # Weighted average
            weighted_sum = sum(score * weight for score, weight in zip(confidence_scores, weights))
            ensemble_score = weighted_sum / sum(weights)
            
            confidence_level = self._get_confidence_level(ensemble_score)
            
            metadata = {
                "input_scores": confidence_scores,
                "weights": weights,
                "weighted_sum": weighted_sum,
                "calculated_at": datetime.utcnow().isoformat()
            }
            
            return ConfidenceScore(
                score=ensemble_score,
                method="ensemble",
                confidence_level=confidence_level,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error calculating ensemble confidence: {str(e)}")
            return ConfidenceScore(
                score=0.5,
                method="ensemble_fallback",
                confidence_level="low",
                metadata={"error": str(e)}
            )
    
    def calculate_classifier_confidence(self, prediction: str, probability: float,
                                      model_confidence: float = 0.8) -> ConfidenceScore:
        """
        Calculate confidence for classifier predictions
        
        Args:
            prediction: Predicted class/label
            probability: Raw probability score from model
            model_confidence: Overall model confidence
            
        Returns:
            ConfidenceScore object
        """
        try:
            # Combine raw probability with model confidence
            combined_score = (probability * 0.7) + (model_confidence * 0.3)
            
            confidence_level = self._get_confidence_level(combined_score)
            
            metadata = {
                "prediction": prediction,
                "raw_probability": probability,
                "model_confidence": model_confidence,
                "calculated_at": datetime.utcnow().isoformat()
            }
            
            return ConfidenceScore(
                score=combined_score,
                method="classifier",
                confidence_level=confidence_level,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error calculating classifier confidence: {str(e)}")
            return ConfidenceScore(
                score=0.5,
                method="classifier_fallback",
                confidence_level="low",
                metadata={"error": str(e)}
            )
    
    def _get_confidence_level(self, score: float) -> str:
        """Get confidence level label based on score"""
        if score >= self.THRESHOLDS["high"]:
            return "high"
        elif score >= self.THRESHOLDS["medium"]:
            return "medium"
        elif score >= self.THRESHOLDS["low"]:
            return "low"
        else:
            return "reject"
    
    def should_accept_prediction(self, confidence_score: float, 
                                 threshold: Optional[float] = None) -> bool:
        """
        Determine if prediction should be accepted based on confidence
        
        Args:
            confidence_score: Confidence score to evaluate
            threshold: Optional custom threshold (default: default_threshold)
            
        Returns:
            True if should accept, False otherwise
        """
        threshold = threshold or self.default_threshold
        return confidence_score >= threshold
    
    def filter_by_confidence(self, predictions: List[Dict[str, Any]],
                           threshold: Optional[float] = None,
                           confidence_field: str = "confidence") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Filter predictions by confidence threshold
        
        Args:
            predictions: List of prediction dictionaries
            threshold: Optional custom threshold
            confidence_field: Field name containing confidence score
            
        Returns:
            Tuple of (accepted_predictions, rejected_predictions)
        """
        threshold = threshold or self.default_threshold
        accepted = []
        rejected = []
        
        for prediction in predictions:
            confidence = prediction.get(confidence_field, 0.0)
            if self.should_accept_prediction(confidence, threshold):
                accepted.append(prediction)
            else:
                rejected.append(prediction)
        
        return accepted, rejected
    
    def add_confidence_to_tags(self, tags: List[Dict[str, Any]], 
                             content: str, method: str = "pattern_match") -> List[Dict[str, Any]]:
        """
        Add confidence scores to existing tags
        
        Args:
            tags: List of tag dictionaries
            content: Content text for context
            method: Confidence calculation method
            
        Returns:
            Updated tags with confidence scores
        """
        for tag in tags:
            try:
                if method == "pattern_match":
                    pattern = tag.get("pattern_matched", "")
                    content_length = len(content)
                    confidence_obj = self.calculate_pattern_match_confidence(pattern, content, content_length)
                elif method == "semantic":
                    matched_terms = tag.get("matched_terms", [])
                    context_relevance = tag.get("context_relevance", 0.8)
                    confidence_obj = self.calculate_semantic_confidence(content, matched_terms, context_relevance)
                else:
                    # Default to moderate confidence
                    confidence_obj = ConfidenceScore(
                        score=0.75,
                        method="default",
                        confidence_level="medium",
                        metadata={"calculated_at": datetime.utcnow().isoformat()}
                    )
                
                tag["confidence"] = confidence_obj.score
                tag["confidence_level"] = confidence_obj.confidence_level
                tag["confidence_method"] = confidence_obj.method
                tag["confidence_metadata"] = confidence_obj.metadata
                
            except Exception as e:
                logger.error(f"Error adding confidence to tag: {str(e)}")
                tag["confidence"] = 0.5  # Fallback
                tag["confidence_level"] = "low"
                tag["confidence_method"] = "error_fallback"
                tag["confidence_metadata"] = {"error": str(e)}
        
        return tags


# Global confidence scorer instance
confidence_scorer = ConfidenceScorer(default_threshold=0.65)