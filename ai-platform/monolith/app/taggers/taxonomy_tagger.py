"""
Taxonomy Tagger - Educational Taxonomy Classification System
Tags content with canonical educational taxonomy and curriculum standards with confidence scores
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


class TaxonomyTagger:
    """Tag educational content with canonical taxonomy and curriculum standards"""
    
    def __init__(self):
        """Initialize taxonomy tagger with Indonesian curriculum taxonomy"""
        
        # Indonesian Kurikulum Merdeka taxonomy
        self.curriculum_taxonomy = {
            "CP": {  # Capaian Pembelajaran
                "patterns": [r"capaian pembelajaran", r"cp", r"capaian"],
                "description": "Learning Achievement"
            },
            "TP": {  # Tujuan Pembelajaran  
                "patterns": [r"tujuan pembelajaran", r"tp", r"tujuan"],
                "description": "Learning Objectives"
            },
            "ATP": {  # Alur Tujuan Pembelajaran
                "patterns": [r"alur tujuan pembelajaran", r"atp", r"alur"],
                "description": "Learning Objectives Flow"
            },
            "AKM": {  # Asesmen Kompetensi Minimum
                "patterns": [r"asesmen kompetensi minimum", r"akm", r"kompetensi minimum"],
                "description": "Minimum Competency Assessment"
            }
        }
        
        # Subject taxonomy (canonical forms)
        self.subject_taxonomy = {
            "Matematika": {
                "canonical": "Matematika",
                "aliases": ["Math", "Matematik", "Mtk", "Mathematics"],
                "code": "SUBJ-MAT"
            },
            "Bahasa Indonesia": {
                "canonical": "Bahasa Indonesia",
                "aliases": ["Indonesian", "Bahasa", "BI"],
                "code": "SUBJ-BIN"
            },
            "IPA": {
                "canonical": "Ilmu Pengetahuan Alam",
                "aliases": ["Science", "Sains", "IPA"],
                "code": "SUBJ-IPA"
            },
            "IPS": {
                "canonical": "Ilmu Pengetahuan Sosial",
                "aliases": ["Social Studies", "IPS", "Sosial"],
                "code": "SUBJ-IPS"
            },
            "PJOK": {
                "canonical": "Pendidikan Jasmani, Olahraga, dan Kesehatan",
                "aliases": ["Physical Education", "PJOK", "Olahraga"],
                "code": "SUBJ-PJOK"
            },
            "Seni Budaya": {
                "canonical": "Seni Budaya",
                "aliases": ["Arts", "Seni", "Culture"],
                "code": "SUBJ-SBU"
            },
            "Bahasa Inggris": {
                "canonical": "Bahasa Inggris",
                "aliases": ["English", "Inggris"],
                "code": "SUBJ-BIG"
            }
        }
        
        # Grade level taxonomy
        self.grade_taxonomy = {
            "Kelas 1": {"grade": "1", "phase": "A"},
            "Kelas 2": {"grade": "2", "phase": "A"},
            "Kelas 3": {"grade": "3", "phase": "A"},
            "Kelas 4": {"grade": "4", "phase": "B"},
            "Kelas 5": {"grade": "5", "phase": "B"},
            "Kelas 6": {"grade": "6", "phase": "B"}
        }
        
        # Competency phase taxonomy
        self.phase_taxonomy = {
            "Fase A": {
                "grades": ["1", "2", "3"],
                "characteristics": ["konkret", "operasional dasar"]
            },
            "Fase B": {
                "grades": ["4", "5", "6"],
                "characteristics": ["semi-abstrak", "operasional maju"]
            }
        }
        
        logger.info("TaxonomyTagger initialized with Indonesian curriculum taxonomy")
    
    def tag(self, content: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Tag content with taxonomy information
        
        Args:
            content: Text content to tag
            context: Optional context information (subject, grade, etc.)
            
        Returns:
            List of taxonomy tags with canonical forms
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag curriculum standards
            curriculum_tags = self._tag_curriculum_standards(content_lower)
            tags.extend(curriculum_tags)
            
            # Tag subjects (with canonical normalization)
            subject_tags = self._tag_subjects(content_lower, context)
            tags.extend(subject_tags)
            
            # Tag grade levels
            grade_tags = self._tag_grade_levels(content_lower, context)
            tags.extend(grade_tags)
            
            # Tag phases
            phase_tags = self._tag_phases(content_lower, context)
            tags.extend(phase_tags)
            
            logger.info(f"Taxonomy tagging completed: {len(tags)} tags")
            return tags
            
        except Exception as e:
            logger.error(f"Error in taxonomy tagging: {str(e)}")
            return []
    
    def _tag_curriculum_standards(self, content_lower: str) -> List[Dict[str, Any]]:
        """Tag content with curriculum standards with confidence scoring"""
        tags = []
        
        for standard_name, standard_info in self.curriculum_taxonomy.items():
            for pattern in standard_info["patterns"]:
                if re.search(pattern, content_lower):
                    # Calculate proper confidence score
                    confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                        pattern, content_lower, len(content_lower)
                    )
                    
                    tags.append({
                        "type": "curriculum_standard",
                        "canonical": standard_name,
                        "description": standard_info["description"],
                        "confidence": confidence_obj.score,
                        "confidence_level": confidence_obj.confidence_level,
                        "confidence_method": confidence_obj.method,
                        "confidence_metadata": confidence_obj.metadata,
                        "pattern_matched": pattern
                    })
                    break  # Only tag once per standard
        
        return tags
    
    def _tag_subjects(self, content_lower: str, context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Tag content with subject taxonomy (with canonical normalization and confidence scoring)"""
        tags = []
        
        # First, check context if provided
        if context and context.get('subject'):
            subject = context['subject']
            canonical_subject = self._normalize_subject(subject)
            if canonical_subject:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=canonical_subject,
                    probability=0.95,  # High confidence if from context
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "subject",
                    "canonical": canonical_subject,
                    "original": subject,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "source": "context"
                })
                return tags  # Trust context over content analysis
        
        # Otherwise, analyze content
        for canonical_name, subject_info in self.subject_taxonomy.items():
            for alias in subject_info["aliases"]:
                if alias.lower() in content_lower:
                    # Calculate proper confidence score
                    confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                        alias, content_lower, len(content_lower)
                    )
                    
                    tags.append({
                        "type": "subject",
                        "canonical": canonical_name,
                        "original": alias,
                        "code": subject_info["code"],
                        "confidence": confidence_obj.score,
                        "confidence_level": confidence_obj.confidence_level,
                        "confidence_method": confidence_obj.method,
                        "confidence_metadata": confidence_obj.metadata,
                        "source": "content_analysis"
                    })
                    break  # Only tag once per subject
        
        return tags
    
    def _tag_grade_levels(self, content_lower: str, context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Tag content with grade level taxonomy with confidence scoring"""
        tags = []
        
        # Check context first
        if context and context.get('grade'):
            grade = context['grade']
            canonical_grade = self._normalize_grade(grade)
            if canonical_grade:
                phase_info = self.grade_taxonomy.get(canonical_grade, {})
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=canonical_grade,
                    probability=0.95,  # High confidence if from context
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "grade_level",
                    "canonical": canonical_grade,
                    "grade": phase_info.get("grade"),
                    "phase": phase_info.get("phase"),
                    "original": grade,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "source": "context"
                })
                return tags
        
        # Analyze content
        for canonical_grade, grade_info in self.grade_taxonomy.items():
            pattern = canonical_grade.lower().replace("kelas ", "kelas")
            if pattern in content_lower or re.search(rf"kelas\s*{grade_info['grade']}", content_lower):
                confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                    pattern, content_lower, len(content_lower)
                )
                
                tags.append({
                    "type": "grade_level",
                    "canonical": canonical_grade,
                    "grade": grade_info["grade"],
                    "phase": grade_info["phase"],
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "source": "content_analysis"
                })
        
        return tags
    
    def _tag_phases(self, content_lower: str, context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Tag content with curriculum phase taxonomy with confidence scoring"""
        tags = []
        
        # Check context first
        if context and context.get('phase'):
            phase = context['phase']
            canonical_phase = self._normalize_phase(phase)
            if canonical_phase:
                phase_info = self.phase_taxonomy.get(canonical_phase, {})
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=canonical_phase,
                    probability=0.95,  # High confidence if from context
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "curriculum_phase",
                    "canonical": canonical_phase,
                    "grades": phase_info.get("grades"),
                    "characteristics": phase_info.get("characteristics"),
                    "original": phase,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "source": "context"
                })
                return tags
        
        # Analyze content
        for phase_name, phase_info in self.phase_taxonomy.items():
            pattern = phase_name.lower()
            if pattern in content_lower or "fase" in content_lower:
                confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                    pattern, content_lower, len(content_lower)
                )
                
                tags.append({
                    "type": "curriculum_phase",
                    "canonical": phase_name,
                    "grades": phase_info.get("grades"),
                    "characteristics": phase_info.get("characteristics"),
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "source": "content_analysis"
                })
        
        return tags
    
    def _normalize_subject(self, subject: str) -> Optional[str]:
        """Normalize subject to canonical form"""
        subject_lower = subject.lower()
        
        for canonical_name, subject_info in self.subject_taxonomy.items():
            if subject_lower in [alias.lower() for alias in subject_info["aliases"]]:
                return canonical_name
            if subject_lower == canonical_name.lower():
                return canonical_name
        
        return None  # Unknown subject
    
    def _normalize_grade(self, grade: str) -> Optional[str]:
        """Normalize grade to canonical form"""
        grade_lower = grade.lower()
        
        for canonical_grade, grade_info in self.grade_taxonomy.items():
            if grade_lower == grade_info["grade"] or grade_lower in canonical_grade.lower():
                return canonical_grade
        
        return None  # Unknown grade
    
    def _normalize_phase(self, phase: str) -> Optional[str]:
        """Normalize phase to canonical form"""
        phase_lower = phase.lower()
        
        for canonical_phase in self.phase_taxonomy.keys():
            if phase_lower == canonical_phase.lower() or phase_lower.replace("fase ", "") in canonical_phase.lower():
                return canonical_phase
        
        return None  # Unknown phase