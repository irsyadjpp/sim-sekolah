import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class DifficultyClassifier:
    """Classify content difficulty level"""
    
    def __init__(self):
        """Initialize difficulty classifier"""
        self.difficulty_patterns = {
            'easy': [
                'mengenal', 'mengenali', 'mengidentifikasi', 'mengamati',
                'recognize', 'identify', 'understand', 'observe'
            ],
            'medium': [
                'menerangkan', 'menjelaskan', 'mengaplikasikan', 'menganalisis',
                'explain', 'apply', 'analyze', 'interpret', 'solve'
            ],
            'hard': [
                'mengevaluasi', 'menilai', 'mencipta', 'merancang', 'mengembangun',
                'evaluate', 'create', 'design', 'develop', 'synthesize'
            ]
        }
        
        logger.info("Difficulty classifier initialized")
    
    def classify(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Classify content difficulty level"""
        try:
            text_lower = text.lower()
            
            # Score each difficulty level
            difficulty_scores = {
                'easy': sum(1 for word in self.difficulty_patterns['easy'] if word in text_lower),
                'medium': sum(1 for word in self.difficulty_patterns['medium'] if word in text_lower),
                'hard': sum(1 for word in self.difficulty_patterns['hard'] if word in text_lower)
            }
            
            # Find dominant difficulty
            if difficulty_scores:
                dominant_difficulty = max(difficulty_scores, key=difficulty_scores.get)
                confidence = difficulty_scores[dominant_difficulty] / len(text.split()) if text.split() else 0
            else:
                dominant_difficulty = 'medium'  # Default
                confidence = 0.5
            
            # Extract indicators
            indicators = self._extract_indicators(text_lower, dominant_difficulty)
            
            result = {
                'difficulty': dominant_difficulty,
                'confidence': min(confidence, 1.0),
                'indicators': indicators
            }
            
            logger.info(f"Classified difficulty as {dominant_difficulty} with confidence {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying difficulty: {str(e)}")
            return {
                'difficulty': 'unknown',
                'confidence': 0.0,
                'indicators': [],
                'error': str(e)
            }
    
    def _extract_indicators(self, text: str, difficulty: str) -> List[str]:
        """Extract indicators for the detected difficulty"""
        indicators = []
        
        if difficulty in self.difficulty_patterns:
            keywords = self.difficulty_patterns[difficulty]
            for keyword in keywords:
                if keyword in text:
                    indicators.append(keyword)
        
        return indicators