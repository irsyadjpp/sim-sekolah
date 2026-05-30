"""
Standards Validation Engine

This module provides validation logic for curriculum documents against
Kurikulum Merdeka standards to ensure alignment and compliance.
"""

from typing import Dict, List, Optional
from enum import Enum


class ValidationSeverity(Enum):
    """Severity levels for validation issues"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationResult:
    """Validation result structure"""
    def __init__(self):
        self.valid = True
        self.issues = []
        self.score = 0.0
        self.recommendations = []
    
    def add_issue(self, severity: ValidationSeverity, message: str, location: Optional[str] = None):
        """Add validation issue"""
        self.issues.append({
            "severity": severity.value,
            "message": message,
            "location": location
        })
        
        if severity == ValidationSeverity.ERROR:
            self.valid = False
    
    def calculate_score(self) -> float:
        """Calculate validation score (0.0 to 1.0)"""
        if not self.issues:
            return 1.0
        
        total_issues = len(self.issues)
        error_count = sum(1 for issue in self.issues if issue["severity"] == "error")
        warning_count = sum(1 for issue in self.issues if issue["severity"] == "warning")
        
        # Error has higher penalty than warning
        score = 1.0 - (error_count * 0.3) - (warning_count * 0.1)
        return max(0.0, min(1.0, score))


class ValidationEngine:
    """Standards validation engine"""
    
    def __init__(self):
        self.phase_requirements = {
            "A": {"grade_range": ["1", "2"], "min_objectives": 5, "max_objectives": 10},
            "B": {"grade_range": ["3", "4"], "min_objectives": 6, "max_objectives": 12},
            "C": {"grade_range": ["5", "6"], "min_objectives": 7, "max_objectives": 14},
            "D": {"grade_range": ["7", "8", "9"], "min_objectives": 8, "max_objectives": 16}
        }
        
        self.subject_phases = {
            "IPA": ["A", "B", "C", "D"],
            "IPS": ["A", "B", "C", "D"],
            "Matematika": ["A", "B", "C", "D"],
            "Bahasa Indonesia": ["A", "B", "C", "D"],
            "PJOK": ["A", "B", "C", "D"],
            "Seni Budaya": ["A", "B", "C", "D"],
            "PPKn": ["A", "B", "C", "D"],
            "Informatika": ["C", "D"]
        }
    
    def validate_document(self, document_data: Dict, document_type: str) -> Dict:
        """Validate document against appropriate standards"""
        result = ValidationResult()
        
        if document_type == "CP":
            result = self._validate_cp(document_data)
        elif document_type == "ATP":
            result = self._validate_atp(document_data)
        elif document_type == "ModulAjar":
            result = self._validate_modul_ajar(document_data)
        else:
            result.add_issue(ValidationSeverity.ERROR, f"Unknown document type: {document_type}")
        
        result.calculate_score()
        
        return {
            "valid": result.valid,
            "score": result.score,
            "issues": result.issues,
            "recommendations": result.recommendations
        }
    
    def _validate_cp(self, cp_data: Dict) -> ValidationResult:
        """Validate CP document"""
        result = ValidationResult()
        
        # Validate required fields
        required_fields = ["phase", "subject", "learning_objectives", "competencies"]
        for field in required_fields:
            if field not in cp_data:
                result.add_issue(ValidationSeverity.ERROR, f"Missing required field: {field}")
        
        # Validate phase
        if "phase" in cp_data:
            if cp_data["phase"] not in self.phase_requirements:
                result.add_issue(ValidationSeverity.ERROR, f"Invalid phase: {cp_data['phase']}")
            else:
                result.recommendations.append(f"Phase {cp_data['phase']} requires {self.phase_requirements[cp_data['phase']]['min_objectives']}-{self.phase_requirements[cp_data['phase']]['max_objectives']} learning objectives")
        
        # Validate subject-phase compatibility
        if "phase" in cp_data and "subject" in cp_data:
            if cp_data["subject"] not in self.subject_phases:
                result.add_issue(ValidationSeverity.ERROR, f"Unknown subject: {cp_data['subject']}")
            elif cp_data["phase"] not in self.subject_phases[cp_data["subject"]]:
                result.add_issue(ValidationSeverity.ERROR, f"Subject {cp_data['subject']} not available in phase {cp_data['phase']}")
        
        # Validate learning objectives
        if "learning_objectives" in cp_data:
            objectives = cp_data["learning_objectives"]
            if len(objectives) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Learning objectives cannot be empty")
            elif "phase" in cp_data:
                req = self.phase_requirements.get(cp_data["phase"], {})
                min_obj = req.get("min_objectives", 5)
                max_obj = req.get("max_objectives", 10)
                
                if len(objectives) < min_obj:
                    result.add_issue(ValidationSeverity.WARNING, f"Insufficient learning objectives (have {len(objectives)}, need at least {min_obj})")
                    result.recommendations.append(f"Add {min_obj - len(objectives)} more learning objectives")
                elif len(objectives) > max_obj:
                    result.add_issue(ValidationSeverity.WARNING, f"Too many learning objectives (have {len(objectives)}, recommend max {max_obj})")
        
        # Validate competencies
        if "competencies" in cp_data:
            competencies = cp_data["competencies"]
            if "KI" not in competencies or len(competencies["KI"]) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Kompetensi Inti (KI) cannot be empty")
            if "KD" not in competencies or len(competencies["KD"]) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Kompetensi Dasar (KD) cannot be empty")
        
        return result
    
    def _validate_atp(self, atp_data: Dict) -> ValidationResult:
        """Validate ATP document"""
        result = ValidationResult()
        
        # Validate required fields
        required_fields = ["grade", "semester", "subject", "cp_id", "topics"]
        for field in required_fields:
            if field not in atp_data:
                result.add_issue(ValidationSeverity.ERROR, f"Missing required field: {field}")
        
        # Validate grade
        if "grade" in atp_data:
            valid_grades = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            if atp_data["grade"] not in valid_grades:
                result.add_issue(ValidationSeverity.ERROR, f"Invalid grade: {atp_data['grade']}")
        
        # Validate semester
        if "semester" in atp_data:
            valid_semesters = ["ganjil", "genap"]
            if atp_data["semester"] not in valid_semesters:
                result.add_issue(ValidationSeverity.ERROR, f"Invalid semester: {atp_data['semester']}")
        
        # Validate topics
        if "topics" in atp_data:
            topics = atp_data["topics"]
            if len(topics) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Topics cannot be empty")
            elif len(topics) < 8:
                result.add_issue(ValidationSeverity.WARNING, f"Low number of topics (have {len(topics)}, recommend 8-12)")
            
            # Validate each topic
            for i, topic in enumerate(topics):
                if "name" not in topic:
                    result.add_issue(ValidationSeverity.ERROR, f"Topic {i+1} missing name")
                if "weeks" not in topic:
                    result.add_issue(ValidationSeverity.ERROR, f"Topic {i+1} missing week allocation")
        
        # Validate CP reference
        if "cp_id" not in atp_data:
            result.add_issue(ValidationSeverity.ERROR, "Missing CP reference (cp_id)")
        
        # Validate time allocation
        if "time_allocation" in atp_data:
            time_alloc = atp_data["time_allocation"]
            if "weekly_hours" not in time_alloc:
                result.add_issue(ValidationSeverity.WARNING, "Missing weekly hours allocation")
            if "semester_hours" not in time_alloc:
                result.add_issue(ValidationSeverity.WARNING, "Missing semester hours allocation")
        
        return result
    
    def _validate_modul_ajar(self, modul_data: Dict) -> ValidationResult:
        """Validate Modul Ajar document"""
        result = ValidationResult()
        
        # Validate required fields
        required_fields = ["grade", "subject", "learning_objectives", "activities", "assessment"]
        for field in required_fields:
            if field not in modul_data:
                result.add_issue(ValidationSeverity.ERROR, f"Missing required field: {field}")
        
        # Validate learning objectives alignment
        if "learning_objectives" in modul_data:
            objectives = modul_data["learning_objectives"]
            if len(objectives) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Learning objectives cannot be empty")
            elif len(objectives) < 3:
                result.add_issue(ValidationSeverity.WARNING, "Insufficient learning objectives (recommend 3-5)")
        
        # Validate activities
        if "activities" in modul_data:
            activities = modul_data["activities"]
            if len(activities) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Activities cannot be empty")
            
            # Check for inquiry-based learning
            has_inquiry = any("inquiry" in str(activity).lower() or "explorasi" in str(activity).lower() 
                             for activity in activities)
            if not has_inquiry:
                result.add_issue(ValidationSeverity.WARNING, "Modul Ajar should include inquiry-based learning activities")
            
            # Check for collaborative learning
            has_collaboration = any("kolaborasi" in str(activity).lower() or "group" in str(activity).lower() 
                                     for activity in activities)
            if not has_collaboration:
                result.add_issue(ValidationSeverity.INFO, "Consider adding collaborative learning activities")
        
        # Validate assessment
        if "assessment" in modul_data:
            assessment = modul_data["assessment"]
            if len(assessment) == 0:
                result.add_issue(ValidationSeverity.ERROR, "Assessment cannot be empty")
            
            # Check for formative assessment
            has_formative = any("formatif" in str(a).lower() or "formative" in str(a).lower() 
                               for a in assessment)
            if not has_formative:
                result.add_issue(ValidationSeverity.WARNING, "Modul Ajar should include formative assessment")
        
        # Validate Profil Pelajar Pancasila integration
        profil_pelajar_pancasila_mentioned = (
            "profil pelajar pancasila" in str(modul_data).lower() or
            "profil pelajar pancasila" in str(modul_data).lower()
        )
        if not profil_pelajar_pancasila_mentioned:
            result.add_issue(ValidationSeverity.INFO, "Consider integrating Profil Pelajar Pancasila dimensions")
        
        return result