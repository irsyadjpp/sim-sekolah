"""
Pedagogy Tagger - Teaching Methods and Learning Approaches
Tags content with pedagogical methods and learning strategies with confidence scores
"""
import re
import logging
from typing import Dict, Any, List, Optional
import sys
sys.path.append('/shared')

from common.utils.confidence_scorer import confidence_scorer

logger = logging.getLogger(__name__)


class PedagogyTagger:
    """Tag educational content with pedagogical approaches"""
    
    def __init__(self):
        """Initialize pedagogy tagger with teaching method patterns"""
        # Teaching method patterns
        self.teaching_methods = {
            "direct_instruction": [
                r"ceramah", r"penjelasan", r"pengajaran langsung", 
                r"eksplisit", r"instruksi", r"panduan"
            ],
            "inquiry_based": [
                r"inkuiri", r"penemuan", r"eksplorasi", r"investigasi",
                r"penelitian", r"pertanyaan", r"curiosity"
            ],
            "collaborative": [
                r"kolaborasi", r"kerja kelompok", r"diskusi",
                r"kooperatif", r"tim", r"bersama", r"peer learning"
            ],
            "problem_based": [
                r"berbasis masalah", r"problem solving", r"pbl",
                r"solved", r"masalah", r"problem"
            ],
            "project_based": [
                r"berbasis proyek", r"project based", r"proyek",
                r"tugas proyek", r"pjbl"
            ],
            "experiential": [
                r"pengalaman", r"praktik", r"eksperimen", r"hands-on",
                r"lapangan", r"simulasi", r"demonstrasi"
            ]
        }
        
        # Learning approach patterns
        self.learning_approaches = {
            "student_centered": [
                r"pusat siswa", r"student centered", r"mandiri",
                r"aktif", r"partisipasi"
            ],
            "differentiated": [
                r"differentiasi", r"differentiated", r"individual",
                r"kemampuan", r"kebutuhan"
            ],
            "scaffolding": [
                r"scaffolding", r"panduan bertahap", r"dukungan",
                r"zonk proksimal", r"zonk perkembangan"
            ]
        }
        
        logger.info("PedagogyTagger initialized with teaching method patterns")
    
    def tag(self, content: str, grade_level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Tag content with pedagogical information with confidence scores
        
        Args:
            content: Text content to tag
            grade_level: Grade level for age-appropriate methods
            
        Returns:
            List of pedagogy tags with confidence scores
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag teaching methods
            for method, patterns in self.teaching_methods.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "teaching_method",
                            "method": method,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "pedagogy"
                        })
            
            # Tag learning approaches
            for approach, patterns in self.learning_approaches.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "learning_approach",
                            "approach": approach,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "pedagogy"
                        })
            
            # Add grade level if provided
            if grade_level:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=grade_level,
                    probability=0.95,  # High confidence if explicitly provided
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "grade_info",
                    "grade_level": grade_level,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "context": "grade_appropriate"
                })
                
                # Grade-specific pedagogy suggestions
                if grade_level in ["1", "2", "3"]:
                    confidence_obj = confidence_scorer.calculate_classifier_confidence(
                        prediction="concrete_operational",
                        probability=0.75,
                        model_confidence=0.7
                    )
                    
                    tags.append({
                        "type": "pedagogy_suggestion",
                        "suggestion": "concrete_operational",
                        "confidence": confidence_obj.score,
                        "confidence_level": confidence_obj.confidence_level,
                        "confidence_method": confidence_obj.method,
                        "confidence_metadata": confidence_obj.metadata,
                        "context": "developmental_stage"
                    })
                elif grade_level in ["4", "5", "6"]:
                    confidence_obj = confidence_scorer.calculate_classifier_confidence(
                        prediction="formal_operational_transition",
                        probability=0.75,
                        model_confidence=0.7
                    )
                    
                    tags.append({
                        "type": "pedagogy_suggestion",
                        "suggestion": "formal_operational_transition",
                        "confidence": confidence_obj.score,
                        "confidence_level": confidence_obj.confidence_level,
                        "confidence_method": confidence_obj.method,
                        "confidence_metadata": confidence_obj.metadata,
                        "context": "developmental_stage"
                    })
            
            logger.info(f"Tagged content with {len(tags)} pedagogy tags using confidence scoring")
            return tags
            
        except Exception as e:
            logger.error(f"Error in pedagogy tagging: {str(e)}")
            return []