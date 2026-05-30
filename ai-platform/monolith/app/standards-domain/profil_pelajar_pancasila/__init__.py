"""
Profil Pelajar Pancasila Module

This module contains the standards and assessment frameworks for the 6 dimensions
of Profil Pelajar Pancasila as defined in Kurikulum Merdeka.
"""

from .six_dimensions import ProfilPelajarPancasilaDimensions
from .indicators import DimensionIndicators
from .assessment import ProfilPelajarPancasilaAssessment

__all__ = [
    "ProfilPelajarPancasila",
    "ProfilPelajarPancasilaDimensions",
    "DimensionIndicators",
    "ProfilPelajarPancasilaAssessment"
]

class ProfilPelajarPancasila:
    """Main class for Profil Pelajar Pancasila management"""
    
    def __init__(self):
        self.dimensions = ProfilPelajarPancasilaDimensions()
        self.indicators = DimensionIndicators()
        self.assessment = ProfilPelajarPancasilaAssessment()
    
    def get_dimensions(self) -> list:
        """Get all 6 dimensions of Profil Pelajar Pancasila"""
        return self.dimensions.get_all_dimensions()
    
    def get_indicators_for_dimension(self, dimension: str) -> list:
        """Get indicators for specific dimension"""
        return self.indicators.get_indicators(dimension)
    
    def assess_student_dimension(self, student_id: str, dimension: str, assessment_data: dict) -> dict:
        """Assess student development in specific dimension"""
        return self.assessment.assess_dimension(student_id, dimension, assessment_data)
    
    def get_holistic_assessment(self, student_id: str) -> dict:
        """Get holistic assessment across all dimensions"""
        return self.assessment.get_holistic_assessment(student_id)