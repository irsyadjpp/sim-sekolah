"""
Curriculum Domain - Bounded Context

This domain manages curriculum planning, management, and alignment with Kurikulum Merdeka standards.
It provides the core curriculum intelligence capabilities.
"""

from .cp_management import CPManagement
from .atp_generation import ATPGeneration
from .modul_ajar_creation import ModulAjarCreation
from .standards_alignment import StandardsAlignment

__all__ = [
    "CurriculumDomain",
    "CPManagement",
    "ATPGeneration",
    "ModulAjarCreation",
    "StandardsAlignment"
]

class CurriculumDomain:
    """Main class for curriculum domain operations"""
    
    def __init__(self):
        self.cp_management = CPManagement()
        self.atp_generation = ATPGeneration()
        self.modul_ajar_creation = ModulAjarCreation()
        self.standards_alignment = StandardsAlignment()
    
    def create_cp(self, phase: str, subject: str, context: dict) -> dict:
        """Create Curriculum Program"""
        return self.cp_management.create_cp(phase, subject, context)
    
    def generate_atp(self, cp_id: str, grade: str, semester: str, subject: str) -> dict:
        """Generate Annual Teaching Plan from CP"""
        return self.atp_generation.generate_atp(cp_id, grade, semester, subject)
    
    def create_modul_ajar(self, atp_data: dict, context: dict) -> dict:
        """Create Modul Ajar from ATP"""
        return self.modul_ajar_creation.create_modul_ajar(atp_data, context)
    
    def validate_alignment(self, curriculum_data: dict, target_standard: str) -> dict:
        """Validate curriculum alignment with standards"""
        return self.standards_alignment.validate(curriculum_data, target_standard)