import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class CompetencyTagger:
    """Tag content with competencies from Kurikulum Merdeka"""
    
    def __init__(self):
        """Initialize competency tagger"""
        # Core competencies (Kompetensi Inti)
        self.core_competencies = {
            'KI-1': {
                'name': 'Spiritualitas',
                'keywords': [
                    'iman', 'taqwa', 'akhlak mulia', 'beriman', 'bertakwa',
                    'spiritual', 'moral', 'etika', 'nilai agama', 'kepercayaan'
                ]
            },
            'KI-2': {
                'name': 'Sosial-Emosional',
                'keywords': [
                    'gotong royong', 'toleransi', 'saling menghargai', 'kerjasama',
                    'interpersonal', 'empati', 'komunikasi', 'berbagi', 'solidaritas'
                ]
            },
            'KI-3': {
                'name': 'Pengetahuan',
                'keywords': [
                    'konsep', 'prinsip', 'teori', 'fakta', 'mengerti', 'memahami',
                    'knowledge', 'concept', 'theory', 'principle', 'explanation'
                ]
            },
            'KI-4': {
                'name': 'Keterampilan',
                'keywords': [
                    'menerapkan', 'menganalisis', 'mengevaluasi', 'mencipta',
                    'skill', 'aplikasi', 'analisis', 'evaluasi', 'kreasi'
                ]
            }
        }
        
        logger.info("Competency tagger initialized")
    
    def tag(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Tag content with competencies"""
        try:
            text_lower = text.lower()
            
            # Score each competency
            competency_scores = {}
            matched_keywords = {}
            
            for ki_code, ki_info in self.core_competencies.items():
                keywords = ki_info['keywords']
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                competency_scores[ki_code] = {
                    'name': ki_info['name'],
                    'score': matches
                }
                
                if matches > 0:
                    matched_keywords[ki_code] = [keyword for keyword in keywords if keyword in text_lower]
            
            # Filter competencies with positive matches
            detected_competencies = [
                {
                    'code': ki_code,
                    'name': info['name'],
                    'score': info['score']
                }
                for ki_code, info in competency_scores.items()
                if info['score'] > 0
            ]
            
            # Sort by score
            detected_competencies.sort(key=lambda x: x['score'], reverse=True)
            
            # Determine primary competency
            primary_competency = detected_competencies[0] if detected_competencies else None
            confidence = primary_competency['score'] / len(text.split()) if text.split() and primary_competency else 0.5
            
            result = {
                'competencies': detected_competencies,
                'primary_competency': primary_competency,
                'confidence': min(confidence, 1.0),
                'matched_keywords': matched_keywords
            }
            
            logger.info(f"Tagged {len(detected_competencies)} competencies, primary: {primary_competency}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error tagging competency: {str(e)}")
            return {
                'competencies': [],
                'primary_competency': None,
                'confidence': 0.0,
                'matched_keywords': {},
                'error': str(e)
            }