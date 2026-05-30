"""
Character Domain - Bounded Context

This domain manages character development, Profil Pelajar Pancasila integration,
character assessment, value tracking, and character reporting capabilities.
This is a CRITICAL component for Kurikulum Merdeka alignment and Pembelajaran Mendalam.
"""

from .profil_pelajar_pancasila_integration import ProfilPelajarPancasilaIntegration
from .character_assessment import CharacterAssessment
from .value_tracking import ValueTracking
from .character_reporting import CharacterReporting

__all__ = [
    "CharacterDomain",
    "ProfilPelajarPancasilaIntegration",
    "CharacterAssessment",
    "ValueTracking",
    "CharacterReporting"
]

class CharacterDomain:
    """Main class for character domain operations"""
    
    def __init__(self):
        self.profil_pelajar_pancasila = ProfilPelajarPancasilaIntegration()
        self.character_assessment = CharacterAssessment()
        self.value_tracking = ValueTracking()
        self.character_reporting = CharacterReporting()
    
    def integrate_profil_pelajar_pancasila(self, learning_context: dict) -> dict:
        """Integrate Profil Pelajar Pancasila dimensions into learning context"""
        return self.profil_pelajar_pancasila.integrate(learning_context)
    
    def assess_character(self, student_id: str, context: dict) -> dict:
        """Assess student character development"""
        return self.character_assessment.assess(student_id, context)
    
    def track_value_development(self, student_id: str, activity: dict) -> dict:
        """Track student value development over activities"""
        return self.value_tracking.track(student_id, activity)
    
    def generate_character_report(self, student_id: str, timeframe: str) -> dict:
        """Generate character development report for student"""
        return self.character_reporting.generate_report(student_id, timeframe)
    
    def assess_profil_pelajar_pancasila_mastery(self, student_id: str) -> dict:
        """Assess student mastery of Profil Pelajar Pancasila dimensions"""
        return self.profil_pelajar_pancasila.assess_mastery(student_id)
    
    def recommend_character_development(self, student_id: str) -> dict:
        """Recommend character development activities"""
        return self.character_assessment.recommend_development(student_id)