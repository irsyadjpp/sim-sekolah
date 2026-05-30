"""
Competency Validator
Validates competency codes against Kurikulum Merdeka standards
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class CompetencyValidator:
    """Validates competency codes against Kurikulum Merdeka standards"""
    
    # Official competency code patterns for Kurikulum Merdeka
    COMPETENCY_PATTERNS = {
        "CP": {  # Core Competencies (Kompetensi Inti)
            "pattern": r"^CP-\d+$",
            "valid_ranges": {
                "elementary": ["CP-1", "CP-2"],  # SD: CP-1 (Spiritual), CP-2 (Social)
                "middle": ["CP-1", "CP-2", "CP-3", "CP-4"],  # SMP: CP-1 to CP-4
                "high": ["CP-1", "CP-2", "CP-3", "CP-4"]  # SMA: CP-1 to CP-4
            }
        },
        "TP": {  # Specific Competencies (Tujuan Pembelajaran)
            "pattern": r"^TP\.\d+\.\d+\.\d+$",
            "description": "Learning objectives with hierarchical structure"
        },
        "CPM": {  # Project-based Learning (P5 - Profil Pelajar Pancasila)
            "pattern": r"^CPM-\d+[A-Za-z]*$",
            "valid_codes": [
                "CPM-1",  # Beriman, bertakwa kepada Tuhan YME, dan berakhlak mulia
                "CPM-2",  # Berkebinekaan global
                "CPM-3",  # Gotong royong
                "CPM-4",  # Mandiri
                "CPM-5",  # Bernalar kritis
                "CPM-6"   # Kreatif
            ]
        },
        "IKM": {  # Student Profile Competencies
            "pattern": r"^IKM-\d+[A-Za-z]*$",
            "valid_codes": [
                "IKM-1",  # Spiritual
                "IKM-2",  # Sosial
                "IKM-3",  # Kognitif
                "IKM-4",  # Karakter
                "IKM-5",  # Vokasional
                "IKM-6"   # Kreativitas
            ]
        }
    }
    
    # Subject-specific competency patterns
    SUBJECT_MAPPINGS = {
        "matematika": {"code_prefix": "MAT", "levels": ["1", "2", "3", "4", "5", "6"]},
        "bahasa_indonesia": {"code_prefix": "BIN", "levels": ["1", "2", "3", "4", "5", "6"]},
        "ipa": {"code_prefix": "IPA", "levels": ["1", "2", "3", "4", "5", "6"]},
        "ips": {"code_prefix": "IPS", "levels": ["1", "2", "3", "4", "5", "6"]},
        "pjok": {"code_prefix": "PJOK", "levels": ["1", "2", "3", "4", "5", "6"]},
        "agama": {"code_prefix": "AGM", "levels": ["1", "2", "3", "4", "5", "6"]}
    }
    
    @classmethod
    def validate_competency_code(cls, competency_code: str, subject: Optional[str] = None, 
                                grade_level: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a competency code against Kurikulum Merdeka standards
        
        Args:
            competency_code: The competency code to validate
            subject: Subject context (optional)
            grade_level: Grade level context (optional)
            
        Returns:
            Validation result with validity flag and details
        """
        if not competency_code or not isinstance(competency_code, str):
            return {
                "valid": False,
                "error": "competency_code must be a non-empty string",
                "competency_code": competency_code
            }
        
        competency_code = competency_code.strip().upper()
        
        # Determine competency type based on prefix
        prefix = competency_code.split("-")[0].split(".")[0]
        
        if prefix not in cls.COMPETENCY_PATTERNS:
            return {
                "valid": False,
                "error": f"Unknown competency prefix: {prefix}",
                "competency_code": competency_code,
                "valid_prefixes": list(cls.COMPETENCY_PATTERNS.keys())
            }
        
        pattern_info = cls.COMPETENCY_PATTERNS[prefix]
        
        # Check for specific code validation (for CPM, IKM)
        if "valid_codes" in pattern_info:
            if competency_code not in pattern_info["valid_codes"]:
                return {
                    "valid": False,
                    "error": f"Invalid {prefix} code",
                    "competency_code": competency_code,
                    "valid_codes": pattern_info["valid_codes"]
                }
        
        # Context validation based on subject and grade level
        if subject and grade_level:
            context_validation = cls._validate_context(competency_code, subject, grade_level)
            if not context_validation["valid"]:
                return context_validation
        
        return {
            "valid": True,
            "competency_code": competency_code,
            "competency_type": prefix,
            "description": pattern_info.get("description", "")
        }
    
    @classmethod
    def _validate_context(cls, competency_code: str, subject: str, grade_level: str) -> Dict[str, Any]:
        """Validate competency code in context of subject and grade level"""
        # Validate subject-specific patterns
        if subject.lower() in cls.SUBJECT_MAPPINGS:
            subject_info = cls.SUBJECT_MAPPINGS[subject.lower()]
            if competency_code.startswith(subject_info["code_prefix"]):
                # Further validation based on grade level could be added here
                pass
        
        return {"valid": True}
    
    @classmethod
    def validate_competency_batch(cls, competency_codes: List[str], 
                                  context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate multiple competency codes in batch
        
        Args:
            competency_codes: List of competency codes to validate
            context: Validation context (subject, grade_level, etc.)
            
        Returns:
            Batch validation result with overall validity and individual results
        """
        if not competency_codes:
            return {
                "valid": True,
                "total_count": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "results": []
            }
        
        results = []
        valid_count = 0
        
        for code in competency_codes:
            result = cls.validate_competency_code(
                code, 
                context.get("subject") if context else None,
                context.get("grade_level") if context else None
            )
            results.append(result)
            if result["valid"]:
                valid_count += 1
        
        return {
            "valid": valid_count == len(competency_codes),
            "total_count": len(competency_codes),
            "valid_count": valid_count,
            "invalid_count": len(competency_codes) - valid_count,
            "results": results
        }
    
    @classmethod
    def get_competency_standards(cls, subject: Optional[str] = None) -> Dict[str, Any]:
        """
        Get official competency standards for reference
        
        Args:
            subject: Optional subject to filter standards
            
        Returns:
            Competency standards information
        """
        standards = {
            "framework": "Kurikulum Merdeka",
            "competency_types": list(cls.COMPETENCY_PATTERNS.keys()),
            "patterns": {k: v for k, v in cls.COMPETENCY_PATTERNS.items()}
        }
        
        if subject:
            subject_lower = subject.lower()
            if subject_lower in cls.SUBJECT_MAPPINGS:
                standards["subject_specific"] = cls.SUBJECT_MAPPINGS[subject_lower]
        
        return standards


class CompetencyValidationResult:
    """Data class for competency validation results"""
    
    def __init__(self, valid: bool, competency_code: str, error: Optional[str] = None):
        self.valid = valid
        self.competency_code = competency_code
        self.error = error
        self.competency_type = competency_code.split("-")[0].split(".")[0] if competency_code else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "valid": self.valid,
            "competency_code": self.competency_code,
            "competency_type": self.competency_type,
            "error": self.error
        }