import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class TaxonomyClassifier:
    """Classify Bloom's taxonomy cognitive level"""
    
    def __init__(self):
        """Initialize taxonomy classifier"""
        # Bloom's taxonomy levels with Indonesian and English keywords
        self.taxonomy_levels = {
            'remember': {
                'keywords': [
                    'mengingat', 'menghafal', 'mencatat', 'mengidentifikasi',
                    'remember', 'recall', 'identify', 'list', 'state'
                ],
                'level': 1
            },
            'understand': {
                'keywords': [
                    'memahami', 'menafsirkan', 'menjelaskan', 'merangkum',
                    'understand', 'explain', 'interpret', 'summarize', 'describe'
                ],
                'level': 2
            },
            'apply': {
                'keywords': [
                    'menerapkan', 'menggunakan', 'mengaplikasikan', 'melaksanakan',
                    'apply', 'use', 'implement', 'execute', 'carry out'
                ],
                'level': 3
            },
            'analyze': {
                'keywords': [
                    'menganalisis', 'membedakan', 'mengorganisasi', 'mengintegrasikan',
                    'analyze', 'differentiate', 'organize', 'integrate', 'compare'
                ],
                'level': 4
            },
            'evaluate': {
                'keywords': [
                    'mengevaluasi', 'menilai', 'mengkritik', 'mengesampingkan',
                    'evaluate', 'assess', 'critique', 'judge', 'justify'
                ],
                'level': 5
            },
            'create': {
                'keywords': [
                    'mencipta', 'merancang', 'mengembangkan', 'membangun',
                    'create', 'design', 'develop', 'construct', 'produce'
                ],
                'level': 6
            }
        }
        
        logger.info("Taxonomy classifier initialized")
    
    def classify(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Classify Bloom's taxonomy level"""
        try:
            text_lower = text.lower()
            
            # Score each taxonomy level
            level_scores = {}
            indicators = {}
            
            for level_name, level_info in self.taxonomy_levels.items():
                keywords = level_info['keywords']
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                level_scores[level_name] = matches
                
                if matches > 0:
                    indicators[level_name] = [keyword for keyword in keywords if keyword in text_lower]
            
            # Find dominant level (prefer higher levels if tie)
            if level_scores:
                # Sort by score, then by level (higher level preferred)
                sorted_levels = sorted(
                    level_scores.items(),
                    key=lambda x: (x[1], self.taxonomy_levels[x[0]]['level']),
                    reverse=True
                )
                dominant_level = sorted_levels[0][0]
                confidence = min(level_scores[dominant_level] / len(text.split()), 1.0) if text.split() else 0
            else:
                dominant_level = 'understand'  # Default
                confidence = 0.5
                indicators[dominant_level] = []
            
            result = {
                'taxonomy_level': dominant_level,
                'confidence': confidence,
                'all_levels': level_scores,
                'indicators': indicators
            }
            
            logger.info(f"Classified taxonomy as {dominant_level} with confidence {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying taxonomy: {str(e)}")
            return {
                'taxonomy_level': 'unknown',
                'confidence': 0.0,
                'all_levels': {},
                'indicators': {},
                'error': str(e)
            }