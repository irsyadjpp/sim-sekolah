"""
Competency Tagger - Educational Competency Tagging System
Tags content with Indonesian curriculum competencies (KI-3, KI-4) with confidence scores
"""
import re
import logging
from typing import Dict, Any, List, Optional
import sys
sys.path.append('/app')

# from common.utils.confidence_scorer import confidence_scorer  # Commented out - legacy import

# Simple confidence scorer implementation for monolith
def confidence_scorer(text: str, pattern: str) -> float:
    """Simple confidence scorer for monolith architecture"""
    if not text or not pattern:
        return 0.0
    if re.search(pattern, text, re.IGNORECASE):
        return 0.8
    return 0.0

logger = logging.getLogger(__name__)


class CompetencyTagger:
    """Tag educational content with curriculum competencies"""
    
    def __init__(self):
        """Initialize competency tagger with curriculum patterns"""
        # Indonesian curriculum competency patterns
        self.competency_patterns = {
            "KI-3": [
                r"memahami", "mengenal", "menjelaskan", "mendeskripsikan", 
                "menganalisis", "mengidentifikasi", "membedakan", "mengkategorikan"
            ],
            "KI-4": [
                r"menerapkan", "menggunakan", "melakukan", "menyajikan",
                r"mengolah", "mengembangkan", "membuat", "merancang"
            ],
            "pengetahuan": [
                r"konsep", "prinsip", "teori", "definisi", "fakta",
                r"pengetahuan", "informasi", "data", "keterangan"
            ],
            "keterampilan": [
                r"keterampilan", "praktik", "eksperimen", "demonstrasi",
                r"latihan", "drill", "praktek"
            ]
        }
        
        # Subject-specific competency patterns
        self.subject_patterns = {
            "matematika": [
                r"operasi hitung", r"aljabar", r"geometri", r"statistika",
                r"peluang", r"bilangan", r"pecahan", r"persentase"
            ],
            "bahasa indonesia": [
                r"membaca", r"menulis", r"mendengarkan", r"berbicara",
                r"teks", r"paragraf", r"kata", r"kalimat"
            ],
            "ipa": [
                r"sains", r"alam", r"biologi", r"fisika", r"kimia",
                r"organisme", r"energi", r"materi", r"zat"
            ],
            "ips": [
                r"sejarah", r"geografi", r"sosiologi", r"ekonomi",
                r"masyarakat", r"budaya", r"wilayah", r"penduduk"
            ]
        }
        
        logger.info("CompetencyTagger initialized with Indonesian curriculum patterns")
    
    def tag(self, content: str, curriculum_phase: Optional[str] = None, 
            subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Tag content with competency information with confidence scores
        
        Args:
            content: Text content to tag
            curriculum_phase: Curriculum phase (A, B, C, etc.)
            subject: Subject area
            
        Returns:
            List of competency tags with confidence scores
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag competency types (KI-3, KI-4)
            for competency_type, patterns in self.competency_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "competency",
                            "competency_type": competency_type,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "curriculum_alignment"
                        })
            
            # Tag subject-specific competencies
            if subject:
                subject_lower = subject.lower()
                for subj, patterns in self.subject_patterns.items():
                    if subj in subject_lower:
                        for pattern in patterns:
                            if re.search(pattern, content_lower):
                                # Calculate proper confidence score
                                confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                                    pattern, content, len(content)
                                )
                                
                                tags.append({
                                    "type": "subject_competency",
                                    "subject": subj,
                                    "pattern_matched": pattern,
                                    "confidence": confidence_obj.score,
                                    "confidence_level": confidence_obj.confidence_level,
                                    "confidence_method": confidence_obj.method,
                                    "confidence_metadata": confidence_obj.metadata,
                                    "context": "subject_specific"
                                })
            
            # Add curriculum phase if provided
            if curriculum_phase:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=curriculum_phase,
                    probability=0.95,  # High confidence if explicitly provided
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "curriculum_info",
                    "curriculum_phase": curriculum_phase,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "context": "curriculum_phase"
                })
            
            logger.info(f"Tagged content with {len(tags)} competency tags using confidence scoring")
            return tags
            
        except Exception as e:
            logger.error(f"Error in competency tagging: {str(e)}")
            return []