import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class TaxonomyTagger:
    """Tag text with Bloom's taxonomy cognitive levels"""
    
    def __init__(self):
        """Initialize taxonomy tagger"""
        self.bloom_taxonomy = {
            'remembering': [
                'mengingat', 'menyebut', 'mengenali', 'menyebut', 'menghafal',
                'recall', 'define', 'identify', 'list', 'state'
            ],
            'understanding': [
                'memahami', 'menjelaskan', 'menguraikan', 'menginterpretasi',
                'understand', 'explain', 'describe', 'discuss', 'interpret'
            ],
            'applying': [
                'menerapkan', 'menggunakan', 'mengaplikasikan', 'menjalankan',
                'apply', 'use', 'implement', 'execute', 'operate'
            ],
            'analyzing': [
                'menganalisis', 'membandingkan', 'mengorganisir', 'menghubungkan',
                'analyze', 'compare', 'organize', 'connect', 'differentiate'
            ],
            'evaluating': [
                'menilai', 'memeriksa', 'mengkaji', 'menganggap',
                'evaluate', 'assess', 'examine', 'critique', 'judge'
            ],
            'creating': [
                'membuat', 'mencipta', 'merancang', 'mengkonstruksi',
                'create', 'design', 'construct', 'produce', 'develop'
            ]
        }
        
        logger.info("Taxonomy tagger initialized")
    
    def tag(self, text: str) -> Dict[str, Any]:
        """Tag text with Bloom's taxonomy cognitive levels"""
        try:
            text_lower = text.lower()
            
            # Score each cognitive level
            level_scores = {}
            for level, verbs in self.bloom_taxonomy.items():
                score = sum(1 for verb in verbs if verb in text_lower)
                level_scores[level] = score
            
            # Find dominant level
            if level_scores:
                dominant_level = max(level_scores, key=level_scores.get)
                confidence = level_scores[dominant_level] / len(text.split()) if text.split() else 0
            else:
                dominant_level = 'understanding'  # Default level
                confidence = 0.5
            
            # Get all detected levels
            detected_levels = [
                level for level, score in level_scores.items() if score > 0
            ]
            
            result = {
                'levels': detected_levels,
                'dominant_level': dominant_level,
                'confidence': min(confidence, 1.0),
                'level_scores': level_scores
            }
            
            logger.info(f"Tagged taxonomy as {dominant_level} with confidence {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error tagging taxonomy: {str(e)}")
            return {
                'levels': [],
                'dominant_level': 'unknown',
                'confidence': 0.0,
                'level_scores': {},
                'error': str(e)
            }
    
    def classify_question(self, question: str) -> str:
        """Classify a question into Bloom's taxonomy level"""
        try:
            result = self.tag(question)
            return result.get('dominant_level', 'understanding')
        except Exception as e:
            logger.error(f"Error classifying question: {str(e)}")
            return 'understanding'