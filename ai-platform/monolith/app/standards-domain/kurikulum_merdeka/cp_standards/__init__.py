"""
CP (Curriculum Program) Standards for Kurikulum Merdeka

CP standards define the structure and requirements for Curriculum Programs
across all phases (A, B, C, D) and subjects in Kurikulum Merdeka.
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class Phase(Enum):
    """Kurikulum Merdeka Phases"""
    A = "A"  # Kelas 1-2 (SD)
    B = "B"  # Kelas 3-4 (SD)
    C = "C"  # Kelas 5-6 (SD)
    D = "D"  # Kelas 7-9 (SMP)


class Subject(Enum):
    """Subjects in Kurikulum Merdeka"""
    IPA = "IPA"
    IPS = "IPS"
    MATEMATIKA = "Matematika"
    BAHASA_INDONESIA = "Bahasa Indonesia"
    PJOK = "PJOK"
    SENI_BUDAYA = "Seni Budaya"
    PPKn = "PPKn"
    INFORMATIKA = "Informatika"


@dataclass
class CPStructure:
    """CP Structure according to Kurikulum Merdeka standards"""
    phase: str
    grade_range: str
    subject: str
    learning_objectives: List[str] = field(default_factory=list)
    competencies: Dict[str, List[str]] = field(default_factory=dict)
    time_allocation: Dict[str, int] = field(default_factory=dict)
    assessment_requirements: List[str] = field(default_factory=list)


class CPStandards:
    """CP Standards Management"""
    
    def __init__(self):
        self.phase_grades = {
            "A": ["1", "2"],
            "B": ["3", "4"],
            "C": ["5", "6"],
            "D": ["7", "8", "9"]
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
    
    def get_standards(self, phase: str, subject: str) -> CPStructure:
        """Get CP standards for specific phase and subject"""
        if phase not in self.phase_grades:
            raise ValueError(f"Invalid phase: {phase}. Must be one of {list(self.phase_grades.keys())}")
        
        if subject not in self.subject_phases or phase not in self.subject_phases[subject]:
            raise ValueError(f"Subject {subject} not available in phase {phase}")
        
        return CPStructure(
            phase=phase,
            grade_range=f"Kelas {self.phase_grades[phase][0]}-{self.phase_grades[phase][-1]}",
            subject=subject,
            learning_objectives=self._get_sample_objectives(phase, subject),
            competencies=self._get_sample_competencies(phase, subject),
            time_allocation=self._get_sample_time_allocation(phase, subject),
            assessment_requirements=self._get_sample_assessment_requirements(phase, subject)
        )
    
    def validate_structure(self, cp_data: Dict) -> Dict:
        """Validate CP structure against Kurikulum Merdeka standards"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate phase
        if "phase" not in cp_data:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing 'phase' field")
        elif cp_data["phase"] not in self.phase_grades:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Invalid phase: {cp_data['phase']}")
        
        # Validate subject
        if "subject" not in cp_data:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing 'subject' field")
        
        # Validate learning objectives
        if "learning_objectives" not in cp_data or len(cp_data["learning_objectives"]) == 0:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing or empty 'learning_objectives'")
        elif len(cp_data["learning_objectives"]) < 5:
            validation_result["warnings"].append("Low number of learning objectives (recommended 5-10)")
        
        # Validate competencies
        if "competencies" not in cp_data:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing 'competencies' field")
        
        # Validate phase-subject compatibility
        if "phase" in cp_data and "subject" in cp_data:
            if cp_data["subject"] not in self.subject_phases or cp_data["phase"] not in self.subject_phases[cp_data["subject"]]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Subject {cp_data['subject']} not available in phase {cp_data['phase']}")
        
        return validation_result
    
    def _get_sample_objectives(self, phase: str, subject: str) -> List[str]:
        """Get sample learning objectives (placeholder for actual data)"""
        return [
            f"Memahami konsep dasar {subject} di fase {phase}",
            f"Mengaplikasikan pengetahuan {subject} dalam konteks nyata",
            f"Mengembangkan kemampuan berpikir kritis dalam {subject}",
            f"Menerapkan nilai-nilai karakter dalam pembelajaran {subject}",
            f"Berkolaborasi dalam pembelajaran {subject}"
        ]
    
    def _get_sample_competencies(self, phase: str, subject: str) -> Dict[str, List[str]]:
        """Get sample competencies (placeholder for actual data)"""
        return {
            "kompetensi_inti": [
                f"KI-1: Menghargai dan menghayati ajaran agama",
                f"KI-2: Menghargai dan menghayati perilaku jujur, disiplin",
                f"KI-3: Memahami pengetahuan faktual konseptual dalam {subject}",
                f"KI-4: Menerapkan pengetahuan dalam {subject}"
            ],
            "kompetensi_dasar": [
                f"KD 1: Mendeskripsikan konsep dasar {subject}",
                f"KD 2: Menganalisis hubungan antar konsep {subject}",
                f"KD 3: Menerapkan konsep {subject} dalam masalah nyata",
                f"KD 4: Mengevaluasi solusi menggunakan konsep {subject}"
            ]
        }
    
    def _get_sample_time_allocation(self, phase: str, subject: str) -> Dict[str, int]:
        """Get sample time allocation (placeholder for actual data)"""
        base_hours = {
            "A": 4,
            "B": 5,
            "C": 6,
            "D": 7
        }
        return {
            "weekly_hours": base_hours.get(phase, 5),
            "yearly_hours": base_hours.get(phase, 5) * 40,
            "per_objective_hours": 8
        }
    
    def _get_sample_assessment_requirements(self, phase: str, subject: str) -> List[str]:
        """Get sample assessment requirements (placeholder for actual data)"""
        return [
            "Formatif assessment weekly",
            "Sumatif assessment per semester",
            "Project-based assessment",
            "Self-assessment and peer assessment",
            "Performance assessment"