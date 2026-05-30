"""
Compliance Engine

This module checks compliance of curriculum components with Kurikulum Merdeka and education regulations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ComplianceStatus(str, Enum):
    """Compliance status"""
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"


class ComplianceEngine:
    """Engine for checking compliance with education standards"""
    
    def __init__(self):
        self.compliance_rules = self._initialize_compliance_rules()
    
    def check_cp_compliance(self, cp_data: Dict) -> Dict:
        """Check CP compliance with Kurikulum Merdeka"""
        compliance_result = {
            "component": "CP",
            "compliance_status": ComplianceStatus.COMPLIANT.value,
            "compliance_score": 1.0,
            "violations": [],
            "warnings": [],
            "recommendations": [],
            "checked_at": datetime.utcnow().isoformat()
        }
        
        # Check structure compliance
        structure_compliance = self._check_structure_compliance(cp_data, "cp")
        compliance_result["violations"].extend(structure_compliance["violations"])
        compliance_result["warnings"].extend(structure_compliance["warnings"])
        
        # Check content compliance
        content_compliance = self._check_content_compliance(cp_data, "cp")
        compliance_result["violations"].extend(content_compliance["violations"])
        compliance_result["warnings"].extend(content_compliance["warnings"])
        
        # Check alignment compliance
        alignment_compliance = self._check_alignment_compliance(cp_data, "cp")
        compliance_result["violations"].extend(alignment_compliance["violations"])
        compliance_result["warnings"].extend(alignment_compliance["warnings"])
        
        # Generate recommendations
        compliance_result["recommendations"] = self._generate_compliance_recommendations(
            compliance_result["violations"],
            compliance_result["warnings"]
        )
        
        # Determine overall compliance status
        compliance_result["compliance_score"] = self._calculate_compliance_score(compliance_result)
        compliance_result["compliance_status"] = self._determine_compliance_status(
            compliance_result["compliance_score"]
        )
        
        return compliance_result
    
    def check_tp_compliance(self, tp_data: Dict) -> Dict:
        """Check TP compliance with Kurikulum Merdeka"""
        compliance_result = {
            "component": "TP",
            "compliance_status": ComplianceStatus.COMPLIANT.value,
            "compliance_score": 1.0,
            "violations": [],
            "warnings": [],
            "recommendations": [],
            "checked_at": datetime.utcnow().isoformat()
        }
        
        # Check structure compliance
        structure_compliance = self._check_structure_compliance(tp_data, "tp")
        compliance_result["violations"].extend(structure_compliance["violations"])
        compliance_result["warnings"].extend(structure_compliance["warnings"])
        
        # Check content compliance
        content_compliance = self._check_content_compliance(tp_data, "tp")
        compliance_result["violations"].extend(content_compliance["violations"])
        compliance_result["warnings"].extend(content_compliance["warnings"])
        
        # Check alignment with CP
        cp_alignment = self._check_cp_alignment_compliance(tp_data)
        compliance_result["violations"].extend(cp_alignment["violations"])
        compliance_result["warnings"].extend(cp_alignment["warnings"])
        
        # Generate recommendations
        compliance_result["recommendations"] = self._generate_compliance_recommendations(
            compliance_result["violations"],
            compliance_result["warnings"]
        )
        
        # Determine overall compliance status
        compliance_result["compliance_score"] = self._calculate_compliance_score(compliance_result)
        compliance_result["compliance_status"] = self._determine_compliance_status(
            compliance_result["compliance_score"]
        )
        
        return compliance_result
    
    def check_atp_compliance(self, atp_data: Dict) -> Dict:
        """Check ATP compliance with Kurikulum Merdeka"""
        compliance_result = {
            "component": "ATP",
            "compliance_status": ComplianceStatus.COMPLIANT.value,
            "compliance_score": 1.0,
            "violations": [],
            "warnings": [],
            "recommendations": [],
            "checked_at": datetime.utcnow().isoformat()
        }
        
        # Check structure compliance
        structure_compliance = self._check_structure_compliance(atp_data, "atp")
        compliance_result["violations"].extend(structure_compliance["violations"])
        compliance_result["warnings"].extend(structure_compliance["warnings"])
        
        # Check content compliance
        content_compliance = self._check_content_compliance(atp_data, "atp")
        compliance_result["violations"].extend(content_compliance["violations"])
        compliance_result["warnings"].extend(content_compliance["warnings"])
        
        # Check alignment with TP
        tp_alignment = self._check_tp_alignment_compliance(atp_data)
        compliance_result["violations"].extend(tp_alignment["violations"])
        compliance_result["warnings"].extend(tp_alignment["warnings"])
        
        # Generate recommendations
        compliance_result["recommendations"] = self._generate_compliance_recommendations(
            compliance_result["violations"],
            compliance_result["warnings"]
        )
        
        # Determine overall compliance status
        compliance_result["compliance_score"] = self._calculate_compliance_score(compliance_result)
        compliance_result["compliance_status"] = self._determine_compliance_status(
            compliance_result["compliance_score"]
        )
        
        return compliance_result
    
    def check_modul_ajar_compliance(self, modul_ajar_data: Dict) -> Dict:
        """Check Modul Ajar compliance with Kurikulum Merdeka"""
        compliance_result = {
            "component": "Modul Ajar",
            "compliance_status": ComplianceStatus.COMPLIANT.value,
            "compliance_score": 1.0,
            "violations": [],
            "warnings": [],
            "recommendations": [],
            "checked_at": datetime.utcnow().isoformat()
        }
        
        # Check structure compliance
        structure_compliance = self._check_structure_compliance(modul_ajar_data, "modul_ajar")
        compliance_result["violations"].extend(structure_compliance["violations"])
        compliance_result["warnings"].extend(structure_compliance["warnings"])
        
        # Check content compliance
        content_compliance = self._check_content_compliance(modul_ajar_data, "modul_ajar")
        compliance_result["violations"].extend(content_compliance["violations"])
        compliance_result["warnings"].extend(content_compliance["warnings"])
        
        # Check Pembelajaran Mendalam compliance
        deep_learning_compliance = self._check_deep_learning_compliance(modul_ajar_data)
        compliance_result["violations"].extend(deep_learning_compliance["violations"])
        compliance_result["warnings"].extend(deep_learning_compliance["warnings"])
        
        # Check P5 compliance
        p5_compliance = self._check_p5_compliance(modul_ajar_data)
        compliance_result["violations"].extend(p5_compliance["violations"])
        compliance_result["warnings"].extend(p5_compliance["warnings"])
        
        # Generate recommendations
        compliance_result["recommendations"] = self._generate_compliance_recommendations(
            compliance_result["violations"],
            compliance_result["warnings"]
        )
        
        # Determine overall compliance status
        compliance_result["compliance_score"] = self._calculate_compliance_score(compliance_result)
        compliance_result["compliance_status"] = self._determine_compliance_status(
            compliance_result["compliance_score"]
        )
        
        return compliance_result
    
    def check_batch_compliance(
        self, 
        components: List[Dict],
        component_type: str
    ) -> Dict:
        """Check compliance for a batch of components"""
        batch_result = {
            "component_type": component_type,
            "total_components": len(components),
            "compliant_count": 0,
            "partially_compliant_count": 0,
            "non_compliant_count": 0,
            "compliance_results": [],
            "common_violations": [],
            "common_warnings": [],
            "checked_at": datetime.utcnow().isoformat()
        }
        
        violation_counts = {}
        warning_counts = {}
        
        for component in components:
            if component_type == "cp":
                result = self.check_cp_compliance(component)
            elif component_type == "tp":
                result = self.check_tp_compliance(component)
            elif component_type == "atp":
                result = self.check_atp_compliance(component)
            elif component_type == "modul_ajar":
                result = self.check_modul_ajar_compliance(component)
            else:
                result = {"error": f"Unknown component type: {component_type}"}
            
            batch_result["compliance_results"].append(result)
            
            # Count compliance status
            status = result.get("compliance_status", ComplianceStatus.PENDING_REVIEW.value)
            if status == ComplianceStatus.COMPLIANT.value:
                batch_result["compliant_count"] += 1
            elif status == ComplianceStatus.PARTIALLY_COMPLIANT.value:
                batch_result["partially_compliant_count"] += 1
            elif status == ComplianceStatus.NON_COMPLIANT.value:
                batch_result["non_compliant_count"] += 1
            
            # Count common violations and warnings
            for violation in result.get("violations", []):
                violation_counts[violation] = violation_counts.get(violation, 0) + 1
            
            for warning in result.get("warnings", []):
                warning_counts[warning] = warning_counts.get(warning, 0) + 1
        
        # Get most common violations and warnings
        batch_result["common_violations"] = [
            {"violation": v, "count": c}
            for v, c in sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        batch_result["common_warnings"] = [
            {"warning": w, "count": c}
            for w, c in sorted(warning_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        return batch_result
    
    def _check_structure_compliance(self, data: Dict, component_type: str) -> Dict:
        """Check structure compliance"""
        result = {"violations": [], "warnings": []}
        
        rules = self.compliance_rules.get(component_type, {})
        required_fields = rules.get("required_fields", [])
        
        for field in required_fields:
            if field not in data or not data[field]:
                result["violations"].append(f"Missing required field: {field}")
        
        return result
    
    def _check_content_compliance(self, data: Dict, component_type: str) -> Dict:
        """Check content compliance"""
        result = {"violations": [], "warnings": []}
        
        rules = self.compliance_rules.get(component_type, {})
        
        # Check text length if applicable
        if component_type in ["cp", "tp"]:
            text_field = "elemen" if component_type == "cp" else "tujuan_pembelajaran"
            if component_type == "cp":
                elements = data.get("elements", [])
                for element in elements:
                    text = element.get(text_field, "")
                    self._check_text_compliance(text, result)
            else:
                text = data.get(text_field, "")
                self._check_text_compliance(text, result)
        
        return result
    
    def _check_text_compliance(self, text: str, result: Dict) -> None:
        """Check text compliance"""
        if len(text) < 10:
            result["violations"].append("Text too short (minimum 10 characters)")
        elif len(text) > 300:
            result["warnings"].append("Text too long (consider splitting)")
        
        # Check if measurable
        if not self._is_measurable(text):
            result["warnings"].append("Text may not be measurable")
    
    def _check_alignment_compliance(self, data: Dict, component_type: str) -> Dict:
        """Check alignment compliance"""
        result = {"violations": [], "warnings": []}
        
        if component_type == "cp":
            # Check if CP has fase and mata_pelajaran
            if not data.get("fase"):
                result["violations"].append("CP missing fase")
            if not data.get("mata_pelajaran"):
                result["violations"].append("CP missing mata_pelajaran")
        
        return result
    
    def _check_cp_alignment_compliance(self, tp_data: Dict) -> Dict:
        """Check TP alignment with CP"""
        result = {"violations": [], "warnings": []}
        
        if not tp_data.get("cp_id"):
            result["warnings"].append("TP should reference a CP")
        
        return result
    
    def _check_tp_alignment_compliance(self, atp_data: Dict) -> Dict:
        """Check ATP alignment with TP"""
        result = {"violations": [], "warnings": []}
        
        tps = atp_data.get("tujuan_pembelajaran", [])
        if not tps:
            result["violations"].append("ATP must have at least one TP")
        
        if not atp_data.get("tp_ids"):
            result["warnings"].append("ATP should reference TP IDs")
        
        return result
    
    def _check_deep_learning_compliance(self, modul_ajar_data: Dict) -> Dict:
        """Check Pembelajaran Mendalam compliance"""
        result = {"violations": [], "warnings": []}
        
        # Check for meaningful learning
        if not modul_ajar_data.get("pemahaman_bermakna"):
            result["warnings"].append("Modul Ajar should include pemahaman bermakna")
        
        # Check for inquiry-based learning
        if not modul_ajar_data.get("inquiry_based"):
            result["warnings"].append("Modul Ajar should include inquiry-based learning")
        
        # Check for reflection
        if not modul_ajar_data.get("refleksi"):
            result["warnings"].append("Modul Ajar should include reflection activities")
        
        return result
    
    def _check_p5_compliance(self, modul_ajar_data: Dict) -> Dict:
        """Check P5 compliance"""
        result = {"violations": [], "warnings": []}
        
        # Check for P5 project
        if not modul_ajar_data.get("p5_project"):
            result["info"] = "Modul Ajar should include P5 project for Profil Pelajar Pancasila development"
        
        return result
    
    def _generate_compliance_recommendations(
        self, 
        violations: List[str], 
        warnings: List[str]
    ) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        if violations:
            recommendations.append("Address all violations to achieve full compliance")
        
        if warnings:
            recommendations.append("Review warnings to improve compliance quality")
        
        if not violations and not warnings:
            recommendations.append("Component is fully compliant with Kurikulum Merdeka")
        
        return recommendations
    
    def _calculate_compliance_score(self, compliance_result: Dict) -> float:
        """Calculate overall compliance score"""
        violation_count = len(compliance_result["violations"])
        warning_count = len(compliance_result["warnings"])
        
        # Start with 1.0, deduct for violations and warnings
        score = 1.0 - (violation_count * 0.3) - (warning_count * 0.1)
        
        return max(0.0, score)
    
    def _determine_compliance_status(self, score: float) -> str:
        """Determine compliance status from score"""
        if score >= 0.9:
            return ComplianceStatus.COMPLIANT.value
        elif score >= 0.7:
            return ComplianceStatus.PARTIALLY_COMPLIANT.value
        elif score >= 0.5:
            return ComplianceStatus.PARTIALLY_COMPLIANT.value
        else:
            return ComplianceStatus.NON_COMPLIANT.value
    
    def _is_measurable(self, text: str) -> bool:
        """Check if text is measurable"""
        measurable_indicators = ["dapat", "mampu", "mengukur", "menentukan", "menghitung"]
        text_lower = text.lower()
        
        for indicator in measurable_indicators:
            if indicator in text_lower:
                return True
        
        return False
    
    def _initialize_compliance_rules(self) -> Dict:
        """Initialize compliance rules"""
        return {
            "cp": {
                "required_fields": ["cp_id", "fase", "mata_pelajaran", "elements"],
                "min_elements": 1,
                "min_element_length": 10,
                "max_element_length": 300
            },
            "tp": {
                "required_fields": ["tp_id", "tujuan_pembelajaran", "domain"],
                "min_length": 10,
                "max_length": 200
            },
            "atp": {
                "required_fields": ["atp_id", "fase", "mata_pelajaran", "periode", "tujuan_pembelajaran"],
                "min_tps": 1
            },
            "modul_ajar": {
                "required_fields": ["modul_ajar_id", "fase", "mata_pelajaran", "topik", "tujuan_pembelajaran"],
                "min_tps": 1,
                "requires_deep_learning": True,
                "requires_p5": True
            }
        }
