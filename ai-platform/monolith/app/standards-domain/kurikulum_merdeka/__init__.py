"""
Kurikulum Merdeka Standards Module

This module contains the authoritative standards for Kurikulum Merdeka Indonesia,
including CP (Curriculum Program), ATP (Annual Teaching Plan), Modul Ajar, 
Assessment, and Rubric standards for all phases and subjects.
"""

from .cp_standards import CPStandards
from .atp_standards import ATPStandards
from .modul_ajar_standards import ModulAjarStandards
from .assessment_standards import AssessmentStandards
from .rubric_standards import RubricStandards

__all__ = [
    "KurikulumMerdekaStandards",
    "CPStandards",
    "ATPStandards",
    "ModulAjarStandards",
    "AssessmentStandards",
    "RubricStandards"
]

class KurikulumMerdekaStandards:
    """Main class for Kurikulum Merdeka standards management"""
    
    def __init__(self):
        self.cp_standards = CPStandards()
        self.atp_standards = ATPStandards()
        self.modul_ajar_standards = ModulAjarStandards()
        self.assessment_standards = AssessmentStandards()
        self.rubric_standards = RubricStandards()
    
    def get_cp_for_phase_subject(self, phase: str, subject: str) -> dict:
        """Get CP standards for specific phase and subject"""
        return self.cp_standards.get_standards(phase, subject)
    
    def get_atp_for_grade_semester(self, grade: str, semester: str, subject: str) -> dict:
        """Get ATP standards for specific grade, semester, and subject"""
        return self.atp_standards.get_standards(grade, semester, subject)
    
    def validate_cp_structure(self, cp_data: dict) -> dict:
        """Validate CP structure against Kurikulum Merdeka standards"""
        return self.cp_standards.validate_structure(cp_data)
    
    def validate_atp_structure(self, atp_data: dict) -> dict:
        """Validate ATP structure against Kurikulum Merdeka standards"""
        return self.atp_standards.validate_structure(atp_data)