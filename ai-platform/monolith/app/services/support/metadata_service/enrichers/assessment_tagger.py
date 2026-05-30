import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class AssessmentTagger:
    """Tag content with assessment types"""
    
    def __init__(self):
        """Initialize assessment tagger"""
        # Assessment types
        self.assessment_types = {
            'diagnostic': {
                'name': 'Diagnostic Assessment',
                'keywords': [
                    'diagnostik', 'pra-tes', 'tes awal', 'evaluasi awal',
                    'diagnostic', 'pre-test', 'initial assessment',
                    'pengetahuan awal', 'initial knowledge'
                ],
                'cognitive_level': 'remember'
            },
            'formative': {
                'name': 'Formative Assessment',
                'keywords': [
                    'formatif', 'evaluasi proses', ' asesmen formatif', 'penilaian harian',
                    'formative', 'process assessment', 'daily assessment',
                    'tugas rutin', 'latihan', 'quiz'
                ],
                'cognitive_level': 'apply'
            },
            'summative': {
                'name': 'Summative Assessment',
                'keywords': [
                    'sumatif', 'ujian akhir', 'evaluasi akhir', 'tes akhir',
                    'summative', 'final exam', 'end assessment',
                    'ujian semester', 'ujian tahunan'
                ],
                'cognitive_level': 'evaluate'
            },
            'performance_based': {
                'name': 'Performance-Based Assessment',
                'keywords': [
                    'kinerja', 'performance', 'praktik', 'demonstrasi',
                    'performance', 'practical', 'demonstration',
                    'portfolio', 'proyek', 'produk'
                ],
                'cognitive_level': 'create'
            },
            'peer_assessment': {
                'name': 'Peer Assessment',
                'keywords': [
                    'sejawat', 'teman sebaya', 'penilaian teman',
                    'peer', 'peer review', 'self-assessment',
                    'penilaian diri', 'self-review'
                ],
                'cognitive_level': 'evaluate'
            },
            'authentic': {
                'name': 'Authentic Assessment',
                'keywords': [
                    'autentik', 'nyata', 'kontekstual', 'situasi nyata',
                    'authentic', 'real-world', 'contextual',
                    'kasus nyata', 'case study'
                ],
                'cognitive_level': 'apply'
            }
        }
        
        logger.info("Assessment tagger initialized")
    
    def tag(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Tag content with assessment types"""
        try:
            text_lower = text.lower()
            
            # Score each assessment type
            assessment_scores = {}
            matched_keywords = {}
            
            for ass_type, ass_info in self.assessment_types.items():
                keywords = ass_info['keywords']
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                assessment_scores[ass_type] = {
                    'name': ass_info['name'],
                    'score': matches,
                    'cognitive_level': ass_info['cognitive_level']
                }
                
                if matches > 0:
                    matched_keywords[ass_type] = [keyword for keyword in keywords if keyword in text_lower]
            
            # Filter assessments with positive matches
            detected_assessments = [
                {
                    'type': ass_type,
                    'name': info['name'],
                    'score': info['score'],
                    'cognitive_level': info['cognitive_level']
                }
                for ass_type, info in assessment_scores.items()
                if info['score'] > 0
            ]
            
            # Sort by score
            detected_assessments.sort(key=lambda x: x['score'], reverse=True)
            
            # Determine primary assessment
            primary_assessment = detected_assessments[0] if detected_assessments else None
            confidence = primary_assessment['score'] / len(text.split()) if text.split() and primary_assessment else 0.5
            cognitive_level = primary_assessment['cognitive_level'] if primary_assessment else 'unknown'
            
            result = {
                'assessment_types': detected_assessments,
                'primary_type': primary_assessment,
                'cognitive_level': cognitive_level,
                'confidence': min(confidence, 1.0),
                'matched_keywords': matched_keywords
            }
            
            logger.info(f"Tagged {len(detected_assessments)} assessments, primary: {primary_assessment}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error tagging assessment: {str(e)}")
            return {
                'assessment_types': [],
                'primary_type': None,
                'cognitive_level': 'unknown',
                'confidence': 0.0,
                'matched_keywords': {},
                'error': str(e)
            }