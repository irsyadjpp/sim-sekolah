import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class PedagogyTagger:
    """Tag content with pedagogical approaches"""
    
    def __init__(self):
        """Initialize pedagogy tagger"""
        # Pedagogical approaches
        self.pedagogy_types = {
            'direct_instruction': {
                'name': 'Direct Instruction',
                'keywords': [
                    'ceramah', 'penjelasan', 'instruksi langsung', 'panduan guru',
                    'lecture', 'explanation', 'direct instruction', 'teacher guidance',
                    'mengajar langsung', 'penyampaian materi'
                ]
            },
            'inquiry_based': {
                'name': 'Inquiry-Based Learning',
                'keywords': [
                    'penyelidikan', 'eksplorasi', 'pertanyaan terbuka',
                    'inquiry', 'investigation', 'open-ended questions',
                    'mencari jawaban', 'meneliti', 'explore'
                ]
            },
            'project_based': {
                'name': 'Project-Based Learning',
                'keywords': [
                    'projek', 'proyek', 'tugas proyek', 'pembuatan produk',
                    'project', 'product creation', 'problem-solving project',
                    'mengerjakan proyek', 'hasil karya'
                ]
            },
            'collaborative': {
                'name': 'Collaborative Learning',
                'keywords': [
                    'kelompok', 'kerjasama', 'diskusi kelompok', 'belajar bersama',
                    'group work', 'collaboration', 'group discussion',
                    'peer learning', 'gotong royong'
                ]
            },
            'differentiated': {
                'name': 'Differentiated Instruction',
                'keywords': [
                    'diferensiasi', 'penyesuaian', 'adaptasi', 'kebutuhan siswa',
                    'differentiation', 'adaptation', 'student needs',
                    'personalized learning', 'individual learning'
                ]
            },
            'experiential': {
                'name': 'Experiential Learning',
                'keywords': [
                    'pengalaman', 'praktik', 'demonstrasi', 'simulasi',
                    'experience', 'practice', 'demonstration', 'simulation',
                    'field trip', 'praktikum', 'hands-on'
                ]
            }
        }
        
        logger.info("Pedagogy tagger initialized")
    
    def tag(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Tag content with pedagogical approaches"""
        try:
            text_lower = text.lower()
            
            # Score each pedagogy type
            pedagogy_scores = {}
            matched_keywords = {}
            
            for ped_type, ped_info in self.pedagogy_types.items():
                keywords = ped_info['keywords']
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                pedagogy_scores[ped_type] = {
                    'name': ped_info['name'],
                    'score': matches
                }
                
                if matches > 0:
                    matched_keywords[ped_type] = [keyword for keyword in keywords if keyword in text_lower]
            
            # Filter pedagogies with positive matches
            detected_pedagogies = [
                {
                    'type': ped_type,
                    'name': info['name'],
                    'score': info['score']
                }
                for ped_type, info in pedagogy_scores.items()
                if info['score'] > 0
            ]
            
            # Sort by score
            detected_pedagogies.sort(key=lambda x: x['score'], reverse=True)
            
            # Determine dominant pedagogy
            dominant_pedagogy = detected_pedagogies[0] if detected_pedagogies else None
            confidence = dominant_pedagogy['score'] / len(text.split()) if text.split() and dominant_pedagogy else 0.5
            
            result = {
                'pedagogy_types': detected_pedagogies,
                'dominant_pedagogy': dominant_pedagogy,
                'confidence': min(confidence, 1.0),
                'matched_keywords': matched_keywords
            }
            
            logger.info(f"Tagged {len(detected_pedagogies)} pedagogies, dominant: {dominant_pedagogy}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error tagging pedagogy: {str(e)}")
            return {
                'pedagogy_types': [],
                'dominant_pedagogy': None,
                'confidence': 0.0,
                'matched_keywords': {},
                'error': str(e)
            }