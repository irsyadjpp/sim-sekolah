"""
Learning Objective Tagger - Learning Objectives and Outcomes
Tags content with learning objectives and outcomes alignment with confidence scores
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


class LearningObjectiveTagger:
    """Tag educational content with learning objectives and outcomes"""
    
    def __init__(self):
        """Initialize learning objective tagger with objective patterns"""
        # Learning objective indicators
        self.objective_indicators = [
            r"tujuan pembelajaran", r"learning objective", r"objective",
            r"setelah pembelajaran", r"setelah kegiatan", r"siswa mampu",
            r"siswa dapat", r"diharapkan", r"target"
        ]
        
        # Outcome indicators
        self.outcome_indicators = [
            r"hasil belajar", r"learning outcome", r"outcome",
            r"capaian", r"pencapaian", r"kompetensi", r"standar"
        ]
        
        # Indonesian curriculum standard patterns
        self.curriculum_standards = {
            "CP": [  # Capaian Pembelajaran
                r"capaian pembelajaran", r"cp", r"capaian",
                r"learning achievement"
            ],
            "TP": [  # Tujuan Pembelajaran
                r"tujuan pembelajaran", r"tp", r"tujuan",
                r"learning objective"
            ],
            "ATP": [  # Alur Tujuan Pembelajaran
                r"alur tujuan pembelajaran", r"atp", r"alur",
                r"learning flow"
            ],
            "AKM": [  # Asesmen Kompetensi Minimum
                r"asesmen kompetensi minimum", r"akm", r"kompetensi minimum",
                r"minimum competency assessment"
            ]
        }
        
        # Objective structure patterns (SMART criteria)
        self.smart_patterns = {
            "specific": [
                r"spesifik", r"terukur", r"jelas", r"tertentu",
                r"mampu menjelaskan", r"dapat menerapkan"
            ],
            "measurable": [
                r"dapat diukur", r"terukur", r"80%", r"75%",
                r"skor", r"nilai", r"kriteria"
            ],
            "achievable": [
                r"dapat dicapai", r"realistis", r"sesuai kemampuan",
                r"developmentally appropriate"
            ],
            "relevant": [
                r"relevan", r"sesuai", r"bermakna", r"kontekstual",
                r"kehidupan sehari-hari"
            ],
            "time_bound": [
                r"waktu", r"pertemuan", r"jam", r"menit",
                r"akhir pembelajaran", r"sesi"
            ]
        }
        
        logger.info("LearningObjectiveTagger initialized with learning objective patterns")
    
    def tag(self, content: str, curriculum_standards: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Tag content with learning objective information with confidence scores
        
        Args:
            content: Text content to tag
            curriculum_standards: Curriculum standards to align with
            
        Returns:
            List of learning objective tags with confidence scores
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag learning objectives
            for pattern in self.objective_indicators:
                if re.search(pattern, content_lower):
                    confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                        pattern, content, len(content)
                    )
                    
                    tags.append({
                        "type": "learning_objective",
                        "indicator": pattern,
                        "confidence": confidence_obj.score,
                        "confidence_level": confidence_obj.confidence_level,
                        "confidence_method": confidence_obj.method,
                        "confidence_metadata": confidence_obj.metadata,
                        "context": "objective_identification"
                    })
            
            # Tag learning outcomes
            for pattern in self.outcome_indicators:
                if re.search(pattern, content_lower):
                    confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                        pattern, content, len(content)
                    )
                    
                    tags.append({
                        "type": "learning_outcome",
                        "indicator": pattern,
                        "confidence": confidence_obj.score,
                        "confidence_level": confidence_obj.confidence_level,
                        "confidence_method": confidence_obj.method,
                        "confidence_metadata": confidence_obj.metadata,
                        "context": "outcome_identification"
                    })
            
            # Tag curriculum standards
            for standard, patterns in self.curriculum_standards.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "curriculum_standard",
                            "standard": standard,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "curriculum_alignment"
                        })
            
            # Tag SMART criteria
            for criterion, patterns in self.smart_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "smart_criterion",
                            "criterion": criterion,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "objective_quality"
                        })
            
            # Add curriculum standards if provided
            if curriculum_standards:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=curriculum_standards,
                    probability=0.95,  # High confidence if explicitly provided
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "specified_standard",
                    "curriculum_standard": curriculum_standards,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "context": "curriculum_alignment"
                })
            
            # Extract learning objectives if present
            objectives = self._extract_objectives(content)
            if objectives:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction="extracted_objectives",
                    probability=0.90,
                    model_confidence=0.85
                )
                
                tags.append({
                    "type": "extracted_objectives",
                    "objectives": objectives,
                    "count": len(objectives),
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "context": "objective_extraction"
                })
            
            logger.info(f"Tagged content with {len(tags)} learning objective tags using confidence scoring")
            return tags
            
        except Exception as e:
            logger.error(f"Error in learning objective tagging: {str(e)}")
            return []
    
    def _extract_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from content"""
        try:
            objectives = []
            
            # Look for patterns like "1. Siswa mampu..." or "- Siswa dapat..."
            patterns = [
                r'\d+\.\s+(?:siswa\s+)?(?:mampu|dapat)\s+([^.]+\.?)',
                r'[-•]\s+(?:siswa\s+)?(?:mampu|dapat)\s+([^.]+\.?)',
                r'(?:siswa\s+)?(?:mampu|dapat)\s+([^.]+\.?)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                objectives.extend(matches)
            
            # Remove duplicates and limit
            objectives = list(set([obj.strip() for obj in objectives if len(obj.strip()) > 10]))
            return objectives[:10]  # Limit to top 10 objectives
            
        except Exception as e:
            logger.error(f"Error extracting objectives: {str(e)}")
            return []