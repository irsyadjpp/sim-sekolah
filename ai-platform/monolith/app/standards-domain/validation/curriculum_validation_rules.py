"""
Curriculum Validation Rules

This module contains validation rules for curriculum components according to Kurikulum Merdeka.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ValidationRuleType(str, Enum):
    """Types of validation rules"""
    STRUCTURE = "structure"
    CONTENT = "content"
    ALIGNMENT = "alignment"
    COMPLETENESS = "completeness"
    QUALITY = "quality"


class ValidationSeverity(str, Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class CurriculumValidationRules:
    """Validation rules for curriculum components"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def validate_cp(self, cp_data: Dict) -> Dict:
        """Validate CP (Capaian Pembelajaran)"""
        validation_result = {
            "component": "CP",
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": [],
            "score": 1.0,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        # Validate structure
        structure_validation = self._validate_cp_structure(cp_data)
        validation_result["errors"].extend(structure_validation["errors"])
        validation_result["warnings"].extend(structure_validation["warnings"])
        
        # Validate content
        content_validation = self._validate_cp_content(cp_data)
        validation_result["errors"].extend(content_validation["errors"])
        validation_result["warnings"].extend(content_validation["warnings"])
        validation_result["info"].extend(content_validation["info"])
        
        # Validate alignment
        alignment_validation = self._validate_cp_alignment(cp_data)
        validation_result["errors"].extend(alignment_validation["errors"])
        validation_result["warnings"].extend(alignment_validation["warnings"])
        
        # Calculate overall validity
        validation_result["valid"] = len(validation_result["errors"]) == 0
        
        # Calculate validation score
        validation_result["score"] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def validate_tp(self, tp_data: Dict) -> Dict:
        """Validate TP (Tujuan Pembelajaran)"""
        validation_result = {
            "component": "TP",
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": [],
            "score": 1.0,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        # Validate structure
        structure_validation = self._validate_tp_structure(tp_data)
        validation_result["errors"].extend(structure_validation["errors"])
        validation_result["warnings"].extend(structure_validation["warnings"])
        
        # Validate content
        content_validation = self._validate_tp_content(tp_data)
        validation_result["errors"].extend(content_validation["errors"])
        validation_result["warnings"].extend(content_validation["warnings"])
        validation_result["info"].extend(content_validation["info"])
        
        # Validate alignment with CP
        alignment_validation = self._validate_tp_cp_alignment(tp_data)
        validation_result["errors"].extend(alignment_validation["errors"])
        validation_result["warnings"].extend(alignment_validation["warnings"])
        
        # Calculate overall validity
        validation_result["valid"] = len(validation_result["errors"]) == 0
        
        # Calculate validation score
        validation_result["score"] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def validate_atp(self, atp_data: Dict) -> Dict:
        """Validate ATP (Alur Tujuan Pembelajaran)"""
        validation_result = {
            "component": "ATP",
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": [],
            "score": 1.0,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        # Validate structure
        structure_validation = self._validate_atp_structure(atp_data)
        validation_result["errors"].extend(structure_validation["errors"])
        validation_result["warnings"].extend(structure_validation["warnings"])
        
        # Validate content
        content_validation = self._validate_atp_content(atp_data)
        validation_result["errors"].extend(content_validation["errors"])
        validation_result["warnings"].extend(content_validation["warnings"])
        
        # Validate alignment with TP
        alignment_validation = self._validate_atp_tp_alignment(atp_data)
        validation_result["errors"].extend(alignment_validation["errors"])
        validation_result["warnings"].extend(alignment_validation["warnings"])
        
        # Calculate overall validity
        validation_result["valid"] = len(validation_result["errors"]) == 0
        
        # Calculate validation score
        validation_result["score"] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def validate_modul_ajar(self, modul_ajar_data: Dict) -> Dict:
        """Validate Modul Ajar"""
        validation_result = {
            "component": "Modul Ajar",
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": [],
            "score": 1.0,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        # Validate structure
        structure_validation = self._validate_modul_ajar_structure(modul_ajar_data)
        validation_result["errors"].extend(structure_validation["errors"])
        validation_result["warnings"].extend(structure_validation["warnings"])
        
        # Validate content
        content_validation = self._validate_modul_ajar_content(modul_ajar_data)
        validation_result["errors"].extend(content_validation["errors"])
        validation_result["warnings"].extend(content_validation["warnings"])
        validation_result["info"].extend(content_validation["info"])
        
        # Validate Pembelajaran Mendalam alignment
        deep_learning_validation = self._validate_deep_learning_alignment(modul_ajar_data)
        validation_result["errors"].extend(deep_learning_validation["errors"])
        validation_result["warnings"].extend(deep_learning_validation["warnings"])
        
        # Calculate overall validity
        validation_result["valid"] = len(validation_result["errors"]) == 0
        
        # Calculate validation score
        validation_result["score"] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def _validate_cp_structure(self, cp_data: Dict) -> Dict:
        """Validate CP structure"""
        result = {"errors": [], "warnings": []}
        
        required_fields = ["cp_id", "fase", "mata_pelajaran", "elements"]
        
        for field in required_fields:
            if field not in cp_data or not cp_data[field]:
                result["errors"].append(f"Missing required field: {field}")
        
        # Validate elements
        elements = cp_data.get("elements", [])
        if not elements:
            result["errors"].append("CP must have at least one element")
        
        for element in elements:
            if not element.get("elemen"):
                result["errors"].append("Element missing 'elemen' field")
        
        return result
    
    def _validate_cp_content(self, cp_data: Dict) -> Dict:
        """Validate CP content"""
        result = {"errors": [], "warnings": [], "info": []}
        
        elements = cp_data.get("elements", [])
        
        for element in elements:
            elemen_text = element.get("elemen", "")
            
            # Check length
            if len(elemen_text) < 10:
                result["errors"].append("Element text too short")
            elif len(elemen_text) > 300:
                result["warnings"].append("Element text too long")
            
            # Check if measurable
            if not self._is_measurable(elemen_text):
                result["info"].append("Element may not be measurable")
        
        return result
    
    def _validate_cp_alignment(self, cp_data: Dict) -> Dict:
        """Validate CP alignment with standards"""
        result = {"errors": [], "warnings": []}
        
        # Check if CP is appropriate for the fase
        fase = cp_data.get("fase", "")
        if not fase:
            result["errors"].append("CP missing fase information")
        
        # Check if CP is appropriate for the mata pelajaran
        mata_pelajaran = cp_data.get("mata_pelajaran", "")
        if not mata_pelajaran:
            result["errors"].append("CP missing mata_pelajaran information")
        
        return result
    
    def _validate_tp_structure(self, tp_data: Dict) -> Dict:
        """Validate TP structure"""
        result = {"errors": [], "warnings": []}
        
        required_fields = ["tp_id", "tujuan_pembelajaran", "domain"]
        
        for field in required_fields:
            if field not in tp_data or not tp_data[field]:
                result["errors"].append(f"Missing required field: {field}")
        
        return result
    
    def _validate_tp_content(self, tp_data: Dict) -> Dict:
        """Validate TP content"""
        result = {"errors": [], "warnings": [], "info": []}
        
        tp_text = tp_data.get("tujuan_pembelajaran", "")
        
        # Check length
        if len(tp_text) < 10:
            result["errors"].append("TP text too short")
        elif len(tp_text) > 200:
            result["warnings"].append("TP text too long")
        
        # Check if starts with verb
        if not self._starts_with_verb(tp_text):
            result["warnings"].append("TP should start with an action verb")
        
        # Check if measurable
        if not self._is_measurable(tp_text):
            result["info"].append("TP may not be measurable")
        
        return result
    
    def _validate_tp_cp_alignment(self, tp_data: Dict) -> Dict:
        """Validate TP alignment with CP"""
        result = {"errors": [], "warnings": []}
        
        # Check if TP references a CP
        if not tp_data.get("cp_id"):
            result["warnings"].append("TP should reference a CP")
        
        return result
    
    def _validate_atp_structure(self, atp_data: Dict) -> Dict:
        """Validate ATP structure"""
        result = {"errors": [], "warnings": []}
        
        required_fields = ["atp_id", "fase", "mata_pelajaran", "periode", "tujuan_pembelajaran"]
        
        for field in required_fields:
            if field not in atp_data or not atp_data[field]:
                result["errors"].append(f"Missing required field: {field}")
        
        # Validate tujuan_pembelajaran is a list
        if not isinstance(atp_data.get("tujuan_pembelajaran"), list):
            result["errors"].append("tujuan_pembelajaran must be a list")
        
        return result
    
    def _validate_atp_content(self, atp_data: Dict) -> Dict:
        """Validate ATP content"""
        result = {"errors": [], "warnings": []}
        
        tps = atp_data.get("tujuan_pembelajaran", [])
        
        if not tps:
            result["errors"].append("ATP must have at least one TP")
        
        # Check if period is valid
        periode = atp_data.get("periode", "")
        if not periode:
            result["warnings"].append("ATP missing period information")
        
        return result
    
    def _validate_atp_tp_alignment(self, atp_data: Dict) -> Dict:
        """Validate ATP alignment with TP"""
        result = {"errors": [], "warnings": []}
        
        tps = atp_data.get("tujuan_pembelajaran", [])
        
        # Check if TPs are referenced
        if not atp_data.get("tp_ids"):
            result["warnings"].append("ATP should reference TP IDs")
        
        return result
    
    def _validate_modul_ajar_structure(self, modul_ajar_data: Dict) -> Dict:
        """Validate Modul Ajar structure"""
        result = {"errors": [], "warnings": []}
        
        required_fields = ["modul_ajar_id", "fase", "mata_pelajaran", "topik", "tujuan_pembelajaran"]
        
        for field in required_fields:
            if field not in modul_ajar_data or not modul_ajar_data[field]:
                result["errors"].append(f"Missing required field: {field}")
        
        return result
    
    def _validate_modul_ajar_content(self, modul_ajar_data: Dict) -> Dict:
        """Validate Modul Ajar content"""
        result = {"errors": [], "warnings": [], "info": []}
        
        # Check if has learning objectives
        tps = modul_ajar_data.get("tujuan_pembelajaran", [])
        if not tps:
            result["errors"].append("Modul Ajar must have learning objectives")
        
        # Check if has assessment
        if not modul_ajar_data.get("asesmen"):
            result["warnings"].append("Modul Ajar should have assessment")
        
        return result
    
    def _validate_deep_learning_alignment(self, modul_ajar_data: Dict) -> Dict:
        """Validate alignment with Pembelajaran Mendalam"""
        result = {"errors": [], "warnings": []}
        
        # Check for meaningful learning
        if not modul_ajar_data.get("pemahaman_bermakna"):
            result["warnings"].append("Modul Ajar should include pemahaman bermakna")
        
        # Check for inquiry-based learning
        if not modul_ajar_data.get("inquiry_based"):
            result["warnings"].append("Modul Ajar should include inquiry-based learning")
        
        # Check for P5 project
        if not modul_ajar_data.get("p5_project"):
            result["info"].append("Modul Ajar should include P5 project")
        
        return result
    
    def _is_measurable(self, text: str) -> bool:
        """Check if text is measurable"""
        measurable_indicators = ["dapat", "mampu", "mengukur", "menentukan", "menghitung"]
        text_lower = text.lower()
        
        for indicator in measurable_indicators:
            if indicator in text_lower:
                return True
        
        return False
    
    def _starts_with_verb(self, text: str) -> bool:
        """Check if text starts with a verb"""
        verbs = ["mampu", "dapat", "harus", "akan", "men", "meng", "mem", "me"]
        text_lower = text.lower()
        
        for verb in verbs:
            if text_lower.startswith(verb):
                return True
        
        return False
    
    def _calculate_validation_score(self, validation_result: Dict) -> float:
        """Calculate overall validation score"""
        error_count = len(validation_result["errors"])
        warning_count = len(validation_result["warnings"])
        
        # Start with 1.0, deduct for errors and warnings
        score = 1.0 - (error_count * 0.3) - (warning_count * 0.1)
        
        return max(0.0, score)
    
    def _initialize_rules(self) -> Dict:
        """Initialize validation rules"""
        return {
            "cp": {
                "min_elements": 1,
                "max_element_length": 300,
                "min_element_length": 10
            },
            "tp": {
                "min_length": 10,
                "max_length": 200,
                "required_fields": ["tp_id", "tujuan_pembelajaran", "domain"]
            },
            "atp": {
                "min_tps": 1,
                "required_fields": ["atp_id", "fase", "mata_pelajaran", "periode", "tujuan_pembelajaran"]
            },
            "modul_ajar": {
                "min_tps": 1,
                "required_fields": ["modul_ajar_id", "fase", "mata_pelajaran", "topik", "tujuan_pembelajaran"]
            }
        }
