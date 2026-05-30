"""
Standards Alignment - Curriculum Standards Validation

This service validates curriculum alignment with Kurikulum Merdeka standards,
ensuring that CP, ATP, and Modul Ajar meet national requirements.
"""

from typing import Dict, List, Optional
from datetime import datetime


class StandardsAlignment:
    """Standards alignment validation for Kurikulum Merdeka"""
    
    def __init__(self):
        self.alignment_history = {}
        # In real implementation, this would integrate with standards-domain
    
    def validate(self, curriculum_data: Dict, target_standard: str) -> Dict:
        """Validate curriculum alignment with target standard"""
        alignment_id = f"align_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine curriculum type
        curriculum_type = curriculum_data.get("curriculum_type", "unknown")
        
        # Select appropriate validation strategy
        if curriculum_type == "cp":
            validation_result = self._validate_cp_alignment(curriculum_data)
        elif curriculum_type == "atp":
            validation_result = self._validate_atp_alignment(curriculum_data)
        elif curriculum_type == "modul_ajar":
            validation_result = self._validate_modul_ajar_alignment(curriculum_data)
        else:
            validation_result = self._validate_generic_alignment(curriculum_data)
        
        alignment_result = {
            "alignment_id": alignment_id,
            "target_standard": target_standard,
            "curriculum_type": curriculum_type,
            "validation_result": validation_result,
            "validated_at": datetime.utcnow().isoformat(),
            "next_review": self._calculate_next_review(validation_result["score"])
        }
        
        self.alignment_history[alignment_id] = alignment_result
        
        return alignment_result
    
    def check_compatibility(self, cp_data: Dict, atp_data: Dict) -> Dict:
        """Check compatibility between CP and ATP"""
        compatibility_score = 0.0
        issues = []
        recommendations = []
        
        # Check phase-subject alignment
        if cp_data.get("phase") != self._extract_phase_from_atp(atp_data):
            issues.append("Phase mismatch between CP and ATP")
        else:
            compatibility_score += 0.3
        
        # Check subject alignment
        if cp_data.get("subject") != atp_data.get("subject"):
            issues.append("Subject mismatch between CP and ATP")
        else:
            compatibility_score += 0.3
        
        # Check learning objective coverage
        cp_objectives = len(cp_data.get("learning_objectives", []))
        atp_objectives = self._count_atp_objectives(atp_data)
        
        if atp_objectives < cp_objectives:
            issues.append(f"ATP covers {atp_objectives} objectives vs {cp_objectives} in CP")
            recommendations.append("Add missing learning objectives to ATP")
        else:
            compatibility_score += 0.2
        
        # Check time allocation
        allocation_validation = atp_data.get("allocation_validation", {})
        if allocation_validation.get("valid"):
            compatibility_score += 0.2
        else:
            issues.append("ATP time allocation validation failed")
            recommendations.append("Adjust time allocation in ATP")
        
        return {
            "compatible": compatibility_score >= 0.7,
            "score": compatibility_score,
            "issues": issues,
            "recommendations": recommendations
        }
    
    def generate_alignment_report(self, alignment_id: str) -> Dict:
        """Generate detailed alignment report"""
        if alignment_id not in self.alignment_history:
            return {"error": "Alignment not found"}
        
        alignment = self.alignment_history[alignment_id]
        
        return {
            "alignment_id": alignment_id,
            "report": {
                "summary": f"Alignment score: {alignment['validation_result']['score']}",
                "strengths": alignment["validation_result"].get("strengths", []),
                "weaknesses": alignment["validation_result"].get("weaknesses", []),
                "recommendations": alignment["validation_result"].get("recommendations", []),
                "actionable_steps": self._generate_actionable_steps(alignment["validation_result"])
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _validate_cp_alignment(self, cp_data: Dict) -> Dict:
        """Validate CP alignment with Kurikulum Merdeka"""
        score = 0.0
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Check phase alignment
        phase = cp_data.get("phase")
        if phase in ["A", "B", "C", "D"]:
            score += 0.2
            strengths.append(f"Valid phase: {phase}")
        else:
            weaknesses.append(f"Invalid phase: {phase}")
            recommendations.append("Ensure phase is A, B, C, or D")
        
        # Check learning objectives
        objectives = cp_data.get("learning_objectives", [])
        if len(objectives) >= 5:
            score += 0.3
            strengths.append(f"Sufficient learning objectives: {len(objectives)}")
        else:
            weaknesses.append(f"Insufficient learning objectives: {len(objectives)}")
            recommendations.append("Add more learning objectives (minimum 5)")
        
        # Check essential materials
        essential_materials = cp_data.get("essential_materials", [])
        if len(essential_materials) > 0:
            score += 0.2
            strengths.append("Essential materials defined")
        else:
            weaknesses.append("Essential materials not defined")
            recommendations.append("Define essential materials for the subject")
        
        # Check Profil Pelajar Pancasila integration
        if any(obj.get("dimension") != "dimension_not_determined" for obj in objectives):
            score += 0.15
            strengths.append("Profil Pelajar Pancasila dimensions integrated")
        else:
            weaknesses.append("Profil Pelajar Pancasila dimensions not integrated")
            recommendations.append("Integrate Profil Pelajar Pancasila dimensions in learning objectives")
        
        # Check validation status
        if cp_data.get("alignment_validation", {}).get("valid"):
            score += 0.15
            strengths.append("CP validation passed")
        
        return {
            "valid": score >= 0.7,
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
    
    def _validate_atp_alignment(self, atp_data: Dict) -> Dict:
        """Validate ATP alignment with Kurikulum Merdeka"""
        score = 0.0
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Check time allocation
        allocation_validation = atp_data.get("allocation_validation", {})
        if allocation_validation.get("valid"):
            score += 0.4
            strengths.append("Time allocation validation passed")
        else:
            weaknesses.append("Time allocation validation failed")
            recommendations.append("Adjust time allocation to meet requirements")
        
        # Check weekly plan completeness
        weekly_plan = atp_data.get("weekly_plan", [])
        expected_weeks = atp_data.get("semester_info", {}).get("weeks", 20)
        
        if len(weekly_plan) == expected_weeks:
            score += 0.3
            strengths.append(f"Complete weekly plan: {len(weekly_plan)} weeks")
        else:
            weaknesses.append(f"Incomplete weekly plan: {len(weekly_plan)} vs {expected_weeks} weeks")
            recommendations.append("Complete weekly plan for all weeks")
        
        # Check reflection components
        has_reflection = all(
            week.get("reflection_components") is not None 
            for week in weekly_plan
        )
        if has_reflection:
            score += 0.15
            strengths.append("Reflection components integrated in weekly plans")
        else:
            weaknesses.append("Reflection components missing from weekly plans")
            recommendations.append("Add reflection components to all weekly plans")
        
        # Check assessment components
        has_assessment = any(
            week.get("assessment") and len(week.get("assessment", [])) > 0
            for week in weekly_plan
        )
        if has_assessment:
            score += 0.15
            strengths.append("Assessment components present")
        else:
            weaknesses.append("Assessment components missing")
            recommendations.append("Add assessment components to weekly plans")
        
        return {
            "valid": score >= 0.7,
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
    
    def _validate_modul_ajar_alignment(self, modul_ajar_data: Dict) -> Dict:
        """Validate Modul Ajar alignment with Kurikulum Merdeka"""
        score = 0.0
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Check template
        template = modul_ajar_data.get("template", {})
        if template.get("kurikulum_merdeka_aligned"):
            score += 0.25
            strengths.append("Kurikulum Merdeka aligned template")
        else:
            weaknesses.append("Template not Kurikulum Merdeka aligned")
            recommendations.append("Use Kurikulum Merdeka aligned template")
        
        # Check content sections
        content = modul_ajar_data.get("content", {})
        required_sections = ["introduction", "learning_objectives", "activities", "assessment", "reflection"]
        missing_sections = [section for section in required_sections if section not in content]
        
        if not missing_sections:
            score += 0.3
            strengths.append("All required sections present")
        else:
            weaknesses.append(f"Missing sections: {missing_sections}")
            recommendations.append(f"Add missing sections: {missing_sections}")
        
        # Check reflection components
        reflection = modul_ajar_data.get("reflection_components", {})
        if reflection.get("before_learning") and reflection.get("during_learning") and reflection.get("after_learning"):
            score += 0.25
            strengths.append("Complete reflection components for Pembelajaran Mendalam")
        else:
            weaknesses.append("Incomplete reflection components")
            recommendations.append("Add complete reflection components (before, during, after learning)")
        
        # Check alignment score
        alignment_score = modul_ajar_data.get("alignment_score", 0.85)
        if alignment_score >= 0.8:
            score += 0.2
            strengths.append(f"High alignment score: {alignment_score}")
        else:
            weaknesses.append(f"Low alignment score: {alignment_score}")
            recommendations.append("Improve content alignment with learning objectives")
        
        return {
            "valid": score >= 0.7,
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
    
    def _validate_generic_alignment(self, curriculum_data: Dict) -> Dict:
        """Generic alignment validation"""
        return {
            "valid": False,
            "score": 0.5,
            "strengths": [],
            "weaknesses": ["Unknown curriculum type"],
            "recommendations": ["Specify curriculum type (cp, atp, or modul_ajar)"]
        }
    
    def _extract_phase_from_atp(self, atp_data: Dict) -> Optional[str]:
        """Extract phase from ATP data"""
        grade = atp_data.get("grade", "1")
        
        # Map grade to phase
        if grade in ["1", "2"]:
            return "A"
        elif grade in ["3", "4"]:
            return "B"
        elif grade in ["5", "6"]:
            return "C"
        elif grade in ["7", "8", "9"]:
            return "D"
        
        return None
    
    def _count_atp_objectives(self, atp_data: Dict) -> int:
        """Count learning objectives in ATP"""
        count = 0
        weekly_plan = atp_data.get("weekly_plan", [])
        
        for week in weekly_plan:
            count += len(week.get("learning_objectives", []))
        
        return count
    
    def _calculate_next_review(self, score: float) -> str:
        """Calculate when next review should happen"""
        if score >= 0.9:
            return "6 months"
        elif score >= 0.8:
            return "3 months"
        elif score >= 0.7:
            return "1 month"
        else:
            return "1 week"
    
    def _generate_actionable_steps(self, validation_result: Dict) -> List[str]:
        """Generate actionable steps from validation result"""
        steps = []
        
        for recommendation in validation_result.get("recommendations", []):
            steps.append(f"1. {recommendation}")
        
        return steps