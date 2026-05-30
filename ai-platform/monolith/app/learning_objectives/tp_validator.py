"""
TP Validator

This module validates Tujuan Pembelajaran (TP) according to Kurikulum Merdeka standards.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ValidationSeverity(str, Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class TPValidator:
    """Validator for Tujuan Pembelajaran"""
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.verb_taxonomy = self._initialize_verb_taxonomy()
    
    def validate_tp(
        self, 
        tp: Dict,
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Validate a single TP"""
        validation_result = {
            "tp_id": tp.get("tp_id", ""),
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": [],
            "score": 1.0,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        # Validate structure
        structure_validation = self._validate_structure(tp)
        validation_result["errors"].extend(structure_validation["errors"])
        validation_result["warnings"].extend(structure_validation["warnings"])
        
        # Validate content
        content_validation = self._validate_content(tp)
        validation_result["errors"].extend(content_validation["errors"])
        validation_result["warnings"].extend(content_validation["warnings"])
        validation_result["info"].extend(content_validation["info"])
        
        # Validate alignment with Kurikulum Merdeka
        alignment_validation = self._validate_kurikulum_merdeka(tp, fase)
        validation_result["errors"].extend(alignment_validation["errors"])
        validation_result["warnings"].extend(alignment_validation["warnings"])
        
        # Validate domain
        domain_validation = self._validate_domain(tp)
        validation_result["errors"].extend(domain_validation["errors"])
        validation_result["warnings"].extend(domain_validation["warnings"])
        
        # Validate difficulty
        difficulty_validation = self._validate_difficulty(tp)
        validation_result["warnings"].extend(difficulty_validation["warnings"])
        
        # Calculate overall validity
        validation_result["valid"] = len(validation_result["errors"]) == 0
        
        # Calculate validation score
        validation_result["score"] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def validate_tp_batch(
        self, 
        tps: List[Dict],
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Validate a batch of TPs"""
        batch_result = {
            "fase": fase,
            "mata_pelajaran": mata_pelajaran,
            "total_tps": len(tps),
            "valid_tps": 0,
            "invalid_tps": 0,
            "validation_results": [],
            "common_errors": [],
            "common_warnings": [],
            "validated_at": datetime.utcnow().isoformat()
        }
        
        error_counts = {}
        warning_counts = {}
        
        for tp in tps:
            result = self.validate_tp(tp, fase, mata_pelajaran)
            batch_result["validation_results"].append(result)
            
            if result["valid"]:
                batch_result["valid_tps"] += 1
            else:
                batch_result["invalid_tps"] += 1
            
            # Count common errors and warnings
            for error in result["errors"]:
                error_counts[error] = error_counts.get(error, 0) + 1
            
            for warning in result["warnings"]:
                warning_counts[warning] = warning_counts.get(warning, 0) + 1
        
        # Get most common errors and warnings
        batch_result["common_errors"] = [
            {"error": error, "count": count}
            for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        batch_result["common_warnings"] = [
            {"warning": warning, "count": count}
            for warning, count in sorted(warning_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        return batch_result
    
    def _validate_structure(self, tp: Dict) -> Dict:
        """Validate TP structure"""
        result = {"errors": [], "warnings": []}
        
        required_fields = ["tp_id", "tujuan_pembelajaran", "domain"]
        
        for field in required_fields:
            if field not in tp or not tp[field]:
                result["errors"].append(f"Missing required field: {field}")
        
        # Check TP ID format
        if "tp_id" in tp:
            tp_id = tp["tp_id"]
            if not tp_id.startswith("TP_"):
                result["warnings"].append("TP ID should start with 'TP_'")
        
        return result
    
    def _validate_content(self, tp: Dict) -> Dict:
        """Validate TP content"""
        result = {"errors": [], "warnings": [], "info": []}
        
        tp_text = tp.get("tujuan_pembelajaran", "")
        
        # Check length
        if len(tp_text) < 10:
            result["errors"].append("TP text too short (minimum 10 characters)")
        elif len(tp_text) > 200:
            result["warnings"].append("TP text too long (consider splitting into multiple TPs)")
        
        # Check if starts with verb
        if not self._starts_with_verb(tp_text):
            result["warnings"].append("TP should start with an action verb")
        
        # Check if measurable
        if not self._is_measurable(tp_text):
            result["info"].append("TP may not be measurable - consider adding measurable criteria")
        
        # Check if specific
        if not self._is_specific(tp_text):
            result["warnings"].append("TP should be more specific")
        
        return result
    
    def _validate_kurikulum_merdeka(self, tp: Dict, fase: str) -> Dict:
        """Validate alignment with Kurikulum Merdeka"""
        result = {"errors": [], "warnings": []}
        
        tp_text = tp.get("tujuan_pembelajaran", "")
        domain = tp.get("domain", "")
        
        # Check if TP is appropriate for the fase
        fase_appropriateness = self._check_fase_appropriateness(tp_text, fase)
        if not fase_appropriateness["appropriate"]:
            result["warnings"].append(fase_appropriateness["message"])
        
        # Check if TP follows Kurikulum Merdeka principles
        principles_check = self._check_kurikulum_principles(tp_text)
        if not principles_check["follows_principles"]:
            result["warnings"].append(principles["message"])
        
        return result
    
    def _validate_domain(self, tp: Dict) -> Dict:
        """Validate TP domain"""
        result = {"errors": [], "warnings": []}
        
        domain = tp.get("domain", "")
        valid_domains = ["kognitif", "psikomotorik", "afektif"]
        
        if domain not in valid_domains:
            result["errors"].append(f"Invalid domain: {domain}. Must be one of {valid_domains}")
        
        # Check if domain matches TP content
        tp_text = tp.get("tujuan_pembelajaran", "")
        inferred_domain = self._infer_domain(tp_text)
        
        if inferred_domain != domain:
            result["warnings"].append(
                f"Domain '{domain}' may not match TP content. Inferred domain: '{inferred_domain}'"
            )
        
        return result
    
    def _validate_difficulty(self, tp: Dict) -> Dict:
        """Validate TP difficulty"""
        result = {"warnings": []}
        
        difficulty = tp.get("difficulty", "")
        valid_difficulties = ["mudah", "sedang", "sulit"]
        
        if difficulty not in valid_difficulties:
            result["warnings"].append(f"Invalid difficulty: {difficulty}. Must be one of {valid_difficulties}")
        
        # Check if difficulty matches TP complexity
        tp_text = tp.get("tujuan_pembelajaran", "")
        inferred_difficulty = self._infer_difficulty(tp_text)
        
        if inferred_difficulty != difficulty:
            result["warnings"].append(
                f"Difficulty '{difficulty}' may not match TP complexity. Inferred difficulty: '{inferred_difficulty}'"
            )
        
        return result
    
    def _starts_with_verb(self, text: str) -> bool:
        """Check if text starts with a verb"""
        verbs = ["mampu", "dapat", "harus", "akan", "men", "meng", "mem", "me"]
        text_lower = text.lower()
        
        for verb in verbs:
            if text_lower.startswith(verb):
                return True
        
        return False
    
    def _is_measurable(self, text: str) -> bool:
        """Check if TP is measurable"""
        measurable_indicators = ["dapat", "mampu", "mengukur", "menentukan", "menghitung"]
        text_lower = text.lower()
        
        for indicator in measurable_indicators:
            if indicator in text_lower:
                return True
        
        return False
    
    def _is_specific(self, text: str) -> bool:
        """Check if TP is specific"""
        # Simple heuristic: TP should have at least 5 words
        return len(text.split()) >= 5
    
    def _check_fase_appropriateness(self, tp_text: str, fase: str) -> Dict:
        """Check if TP is appropriate for the given fase"""
        # Simplified check - in production, use more sophisticated logic
        fase_complexity = {
            "A": "low",
            "B": "low",
            "C": "medium",
            "D": "medium",
            "E": "high"
        }
        
        tp_complexity = self._infer_complexity(tp_text)
        expected_complexity = fase_complexity.get(fase, "medium")
        
        if tp_complexity == "high" and expected_complexity == "low":
            return {
                "appropriate": False,
                "message": f"TP may be too complex for Fase {fase}"
            }
        
        return {"appropriate": True, "message": ""}
    
    def _check_kurikulum_principles(self, tp_text: str) -> Dict:
        """Check if TP follows Kurikulum Merdeka principles"""
        principles = ["bermakna", "kontekstual", "inquiry", "kolaboratif"]
        
        found_principles = [p for p in principles if p in tp_text.lower()]
        
        if not found_principles:
            return {
                "follows_principles": False,
                "message": "TP should incorporate Kurikulum Merdeka principles (bermakna, kontekstual, inquiry, kolaboratif)"
            }
        
        return {"follows_principles": True, "message": ""}
    
    def _infer_domain(self, tp_text: str) -> str:
        """Infer domain from TP text"""
        kognitif_keywords = ["memahami", "menganalisis", "mengevaluasi", "mengerti", "mengenal"]
        psikomotorik_keywords = ["melakukan", "menerapkan", "menyusun", "membuat", "mengoperasikan"]
        afektif_keywords = ["menghargai", "menyukai", "menghormati", "peduli", "berperilaku"]
        
        text_lower = tp_text.lower()
        
        for keyword in kognitif_keywords:
            if keyword in text_lower:
                return "kognitif"
        
        for keyword in psikomotorik_keywords:
            if keyword in text_lower:
                return "psikomotorik"
        
        for keyword in afektif_keywords:
            if keyword in text_lower:
                return "afektif"
        
        return "kognitif"  # Default
    
    def _infer_difficulty(self, tp_text: str) -> str:
        """Infer difficulty from TP text"""
        complexity_indicators = {
            "mudah": ["mengenal", "mengingat", "menyebutkan"],
            "sedang": ["memahami", "menjelaskan", "mengidentifikasi"],
            "sulit": ["menganalisis", "mengevaluasi", "mengkreasi", "merancang"]
        }
        
        text_lower = tp_text.lower()
        
        for level, keywords in complexity_indicators.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return "sedang"  # Default
    
    def _infer_complexity(self, tp_text: str) -> str:
        """Infer complexity level from TP text"""
        # Simple heuristic based on length and vocabulary
        if len(tp_text.split()) < 5:
            return "low"
        elif len(tp_text.split()) < 10:
            return "medium"
        else:
            return "high"
    
    def _calculate_validation_score(self, validation_result: Dict) -> float:
        """Calculate overall validation score"""
        error_count = len(validation_result["errors"])
        warning_count = len(validation_result["warnings"])
        
        # Start with 1.0, deduct for errors and warnings
        score = 1.0 - (error_count * 0.3) - (warning_count * 0.1)
        
        return max(0.0, score)
    
    def _initialize_validation_rules(self) -> Dict:
        """Initialize validation rules"""
        return {
            "min_length": 10,
            "max_length": 200,
            "required_fields": ["tp_id", "tujuan_pembelajaran", "domain"],
            "valid_domains": ["kognitif", "psikomotorik", "afektif"],
            "valid_difficulties": ["mudah", "sedang", "sulit"]
        }
    
    def _initialize_verb_taxonomy(self) -> Dict:
        """Initialize verb taxonomy for validation"""
        return {
            "kognitif": {
                "low": ["mengingat", "mengidentifikasi", "menyebutkan"],
                "medium": ["memahami", "menjelaskan", "menginterpretasi"],
                "high": ["menganalisis", "mengevaluasi", "mengkreasi"]
            },
            "psikomotorik": {
                "low": ["meniru", "mengamati"],
                "medium": ["melakukan", "menerapkan", "menyusun"],
                "high": ["menginovasi", "mengembangkan", "merancang"]
            },
            "afektif": {
                "low": ["menerima", "menyadari"],
                "medium": ["menyukai", "menghormati", "peduli"],
                "high": ["menginternalisasi", "mengamalkan", "mempromosikan"]
            }
        }
