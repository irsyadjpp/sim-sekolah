import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class PedagogyClassifier:
    """Classify pedagogical approach in educational text"""
    
    def __init__(self):
        """Initialize pedagogy classifier"""
        self.pedagogy_keywords = {
            'inquiry_learning': [
                'pertanyaan', 'inquiri', 'penelitian', 'hipotesis', 'eksperimen',
                'questioning', 'investigation', 'hypothesis', 'experiment'
            ],
            'differentiated_learning': [
                'berbeda', 'sesuai', 'kebutuhan', 'individual', 'adaptif',
                'differentiated', 'individualized', 'adaptive'
            ],
            'deep_learning': [
                'mendalam', 'analisis', 'sintesis', 'evaluasi', 'kritik',
                'deep', 'analysis', 'synthesis', 'evaluation', 'critical'
            ],
            'project_based_learning': [
                'proyek', 'kolaboratif', 'tim', 'kerja', 'produksi',
                'project', 'collaborative', 'team', 'work', 'production'
            ],
            'problem_based_learning': [
                'masalah', 'solusi', 'permasalahan', 'pemecahan',
                'problem', 'solution', 'issue', 'solving'
            ]
        }
        
        logger.info("Pedagogy classifier initialized")
    
    def classify(self, text: str) -> Dict[str, Any]:
        """Classify pedagogical approach in text"""
        try:
            text_lower = text.lower()
            
            pedagogy_scores = {}
            for pedagogy_type, keywords in self.pedagogy_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                pedagogy_scores[pedagogy_type] = score
            
            # Find dominant pedagogy
            if pedagogy_scores:
                dominant_pedagogy = max(pedagogy_scores, key=pedagogy_scores.get)
                confidence = pedagogy_scores[dominant_pedagogy] / len(text.split()) if text.split() else 0
            else:
                dominant_pedagogy = 'traditional'
                confidence = 0.5
            
            # Extract indicators
            indicators = self._extract_indicators(text_lower, dominant_pedagogy)
            
            result = {
                'pedagogy_type': dominant_pedagogy,
                'confidence': min(confidence, 1.0),
                'indicators': indicators,
                'all_scores': pedagogy_scores
            }
            
            logger.info(f"Classified pedagogy as {dominant_pedagogy} with confidence {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying pedagogy: {str(e)}")
            return {
                'pedagogy_type': 'unknown',
                'confidence': 0.0,
                'indicators': [],
                'error': str(e)
            }
    
    def _extract_indicators(self, text: str, pedagogy_type: str) -> List[str]:
        """Extract indicators for the detected pedagogy"""
        indicators = []
        
        if pedagogy_type in self.pedagogy_keywords:
            keywords = self.pedagogy_keywords[pedagogy_type]
            for keyword in keywords:
                if keyword in text:
                    indicators.append(keyword)
        
        return indicators