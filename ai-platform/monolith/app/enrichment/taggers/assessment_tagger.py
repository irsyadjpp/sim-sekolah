"""
Assessment Tagger - Assessment Types and Evaluation Methods
Tags content with assessment and evaluation information with confidence scores
"""
import re
import logging
from typing import Dict, Any, List, Optional
import sys
sys.path.append('/shared')

from common.utils.confidence_scorer import confidence_scorer

logger = logging.getLogger(__name__)


class AssessmentTagger:
    """Tag educational content with assessment types and methods"""
    
    def __init__(self):
        """Initialize assessment tagger with assessment patterns"""
        # Assessment type patterns
        self.assessment_types = {
            "formative": [
                r"formatif", r"assessment for learning", r"diagnostic",
                r"selama pembelajaran", r"ongoing", r"monitoring"
            ],
            "summative": [
                r"sumatif", r"assessment of learning", r"akhir",
                r"evaluasi", r"ujian", r"tes akhir"
            ],
            "diagnostic": [
                r"diagnostik", r"awal", r"pre-test", r"preassessment",
                r"pengetahuan awal", r"prerequisite"
            ]
        }
        
        # Assessment method patterns
        self.assessment_methods = {
            "written_test": [
                r"tes tertulis", r"pilihan ganda", r"essay",
                r"urain", r"benar salah", r"isian"
            ],
            "oral_assessment": [
                r"lisan", r"presentasi", r"wawancara",
                r"bicara", r"mengucapkan", r"spoken"
            ],
            "performance_task": [
                r"kinerja", r"performance", r"praktik",
                r"demonstrasi", r"proyek", r"portfolio"
            ],
            "observation": [
                r"observasi", r"pengamatan", r"checklist",
                r"rating scale", r"rubrik"
            ],
            "self_assessment": [
                r"self assessment", r"penilaian diri", r"refleksi",
                r"jurnal", r"logbook"
            ],
            "peer_assessment": [
                r"peer assessment", r"penilaian teman sebaya",
                r"sesama", r"teman"
            ]
        }
        
        # Cognitive domain patterns (Bloom's)
        self.cognitive_domains = {
            "remembering": [
                r"mengingat", r"mengenal", r"menyebutkan",
                r"mendefinisikan", r"mengidentifikasi"
            ],
            "understanding": [
                r"memahami", r"menjelaskan", r"menginterpretasi",
                r"merangkum", r"menyimpulkan"
            ],
            "applying": [
                r"menerapkan", r"menggunakan", r"melaksanakan",
                r"mengimplementasikan"
            ],
            "analyzing": [
                r"menganalisis", r"membedakan", r"mengorganisasi",
                r"menghubungkan", r"membandingkan"
            ],
            "evaluating": [
                r"mengevaluasi", r"mengkritik", r"menilai",
                r"memeriksa", r"menghakimi"
            ],
            "creating": [
                r"membuat", r"merancang", r"mengkonstruksi",
                r"merencanakan", r"menghasilkan"
            ]
        }
        
        logger.info("AssessmentTagger initialized with assessment patterns")
    
    def tag(self, content: str, assessment_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Tag content with assessment information with confidence scores
        
        Args:
            content: Text content to tag
            assessment_type: Specific assessment type if known
            
        Returns:
            List of assessment tags with confidence scores
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag assessment types
            for ass_type, patterns in self.assessment_types.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "assessment_type",
                            "assessment_type": ass_type,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "assessment"
                        })
            
            # Tag assessment methods
            for method, patterns in self.assessment_methods.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "assessment_method",
                            "method": method,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "assessment"
                        })
            
            # Tag cognitive domains
            for domain, patterns in self.cognitive_domains.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "cognitive_domain",
                            "domain": domain,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "bloom_taxonomy"
                        })
            
            # Add assessment type if provided
            if assessment_type:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction=assessment_type,
                    probability=0.95,  # High confidence if explicitly provided
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "specified_assessment",
                    "assessment_type": assessment_type,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "context": "assessment_type"
                })
            
            logger.info(f"Tagged content with {len(tags)} assessment tags using confidence scoring")
            return tags
            
        except Exception as e:
            logger.error(f"Error in assessment tagging: {str(e)}")
            return []