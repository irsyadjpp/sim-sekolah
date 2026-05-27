import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class LearningStyleDetector:
    """Detect learning style from content"""
    
    def __init__(self):
        """Initialize learning style detector"""
        # Learning style indicators
        self.learning_style_patterns = {
            'visual': [
                'gambar', 'diagram', 'grafik', 'skema', 'ilustrasi', 'tabel',
                'image', 'diagram', 'graph', 'schema', 'illustration', 'table',
                'visual', 'melihat', 'observe', 'chart', 'plot'
            ],
            'auditory': [
                'mendengarkan', 'diskusi', 'presentasi', 'ceramah', 'audio',
                'listen', 'discussion', 'presentation', 'lecture', 'audio',
                'berbicara', 'speak', 'verbal', 'mengucapkan'
            ],
            'reading/writing': [
                'membaca', 'menulis', 'teks', 'buku', 'artikel', 'catatan',
                'read', 'write', 'text', 'book', 'article', 'notes',
                'dokumen', 'document', 'literatur', 'literature'
            ],
            'kinesthetic': [
                'praktikum', 'eksperimen', 'aktivitas fisik', 'demonstrasi',
                'laboratory', 'experiment', 'physical activity', 'demonstration',
                'hands-on', 'membuat', 'create', 'membangun', 'build'
            ]
        }
        
        logger.info("Learning style detector initialized")
    
    def detect(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Detect learning style from content"""
        try:
            text_lower = text.lower()
            
            # Score each learning style
            style_scores = {}
            indicators = {}
            
            for style_name, keywords in self.learning_style_patterns.items():
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                style_scores[style_name] = matches
                
                if matches > 0:
                    indicators[style_name] = [keyword for keyword in keywords if keyword in text_lower]
            
            # Find dominant learning style
            if style_scores:
                dominant_style = max(style_scores, key=style_scores.get)
                total_matches = sum(style_scores.values())
                confidence = style_scores[dominant_style] / total_matches if total_matches > 0 else 0
            else:
                dominant_style = 'reading/writing'  # Default
                confidence = 0.5
                indicators[dominant_style] = []
            
            # Get characteristics
            characteristics = self._get_characteristics(dominant_style)
            
            result = {
                'learning_style': dominant_style,
                'confidence': confidence,
                'characteristics': characteristics,
                'indicators': indicators
            }
            
            logger.info(f"Detected learning style {dominant_style} with confidence {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error detecting learning style: {str(e)}")
            return {
                'learning_style': 'unknown',
                'confidence': 0.0,
                'characteristics': [],
                'indicators': {},
                'error': str(e)
            }
    
    def _get_characteristics(self, style: str) -> List[str]:
        """Get characteristics for learning style"""
        characteristics_map = {
            'visual': [
                'Prefers visual aids like images, charts, and diagrams',
                'Learns through observation and visual representation',
                'Benefits from graphic organizers and mind maps'
            ],
            'auditory': [
                'Prefers spoken explanations and discussions',
                'Learns through listening and verbal instruction',
                'Benefits from lectures, podcasts, and group discussions'
            ],
            'reading/writing': [
                'Prefers reading text and writing notes',
                'Learns through written words and text-based resources',
                'Benefits from reading materials and written exercises'
            ],
            'kinesthetic': [
                'Prefers hands-on activities and movement',
                'Learns through doing, touching, and physical interaction',
                'Benefits from experiments, field trips, and practical applications'
            ]
        }
        
        return characteristics_map.get(style, [])