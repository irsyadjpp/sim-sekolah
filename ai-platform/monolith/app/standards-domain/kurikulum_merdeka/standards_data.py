"""
Kurikulum Merdeka National Standards Data

This module contains the systematic encoding of Kurikulum Merdeka national standards
including CP structures for all phases, learning objectives, and competency mappings.
"""

from typing import Dict, List, Optional


class KurikulumMerdekaStandardsData:
    """Systematic encoding of Kurikulum Merdeka national standards"""
    
    def __init__(self):
        self.phase_standards = {
            "A": self._initialize_phase_a_standards(),
            "B": self._initialize_phase_b_standards(),
            "C": self._initialize_phase_c_standards(),
            "D": self._initialize_phase_d_standards()
        }
        
        self.subject_standards = self._initialize_subject_standards()
        self.learning_objectives_db = self._initialize_learning_objectives()
    
    def get_cp_standards_for_phase(self, phase: str, subject: str) -> Dict:
        """Get CP standards for specific phase and subject"""
        if phase not in self.phase_standards:
            raise ValueError(f"Invalid phase: {phase}")
        
        if subject not in self.phase_standards[phase]:
            raise ValueError(f"Subject {subject} not available in phase {phase}")
        
        return self.phase_standards[phase][subject]
    
    def get_learning_objectives_for_cp(self, cp_id: str) -> List[str]:
        """Get learning objectives for specific CP"""
        return self.learning_objectives_db.get(cp_id, [])
    
    def get_competency_mapping(self, phase: str, subject: str) -> Dict:
        """Get competency mapping for phase and subject"""
        cp_standards = self.get_cp_standards_for_phase(phase, subject)
        return cp_standards.get("competencies", {})
    
    def _initialize_phase_a_standards(self) -> Dict:
        """Initialize Phase A (Kelas 1-2) standards"""
        return {
            "IPA": {
                "phase": "A",
                "grade_range": "1-2",
                "subject": "IPA",
                "learning_objectives": [
                    "TP-1: Mengidentifikasi objek dan gejala alam di lingkungan sekitar",
                    "TP-2: Mendeskripsikan ciri-ciri makhluk hidup",
                    "TP-3: Mengelompokkan benda berdasarkan sifatnya",
                    "TP-4: Menerapkan konsep pengamatan sederhana",
                    "TP-5: Menjelaskan pengaruh perubahan cuaca"
                ],
                "competencies": {
                    "KI": [
                        "KI-1: Menghargai dan menghayati ajaran agama",
                        "KI-2: Menghargai dan menghayati perilaku jujur",
                        "KI-3: Memahami pengetahuan faktual konseptual IPA",
                        "KI-4: Menerapkan pengetahuan IPA dalam kehidupan"
                    ],
                    "KD": [
                        "KD 3.1: Mengidentifikasi objek dan gejala alam",
                        "KD 3.2: Mendeskripsikan ciri makhluk hidup",
                        "KD 3.3: Mengelompokkan benda berdasarkan sifat",
                        "KD 4.1: Mengamati objek alam secara sederhana",
                        "KD 4.2: Menyajikan hasil pengamatan IPA"
                    ]
                },
                "bloom_levels": {
                    "TP-1": "remember",
                    "TP-2": "understand", 
                    "TP-3": "apply",
                    "TP-4": "analyze",
                    "TP-5": "evaluate"
                }
            },
            "IPS": {
                "phase": "A",
                "grade_range": "1-2", 
                "subject": "IPS",
                "learning_objectives": [
                    "TP-1: Mengenal diri sendiri dan keluarga",
                    "TP-2: Mengenal lingkungan sekitar",
                    "TP-3: Mengenal kegiatan ekonomi sederhana",
                    "TP-4: Mengenal keragaman budaya",
                    "TP-5: Mengenal kebersamaan dan perbedaan"
                ],
                "competencies": {
                    "KI": [
                        "KI-1: Menghargai dan menghayati ajaran agama",
                        "KI-2: Menghargai dan menghayati perilaku jujur",
                        "KI-3: Memahami pengetahuan faktual konseptual IPS",
                        "KI-4: Menerapkan pengetahuan IPS dalam kehidupan"
                    ],
                    "KD": [
                        "KD 3.1: Mengenal diri dan keluarga",
                        "KD 3.2: Mengenal lingkungan sekitar",
                        "KD 3.3: Mengenal kegiatan ekonomi sederhana",
                        "KD 4.1: Menyajikan diri dan keluarga",
                        "KD 4.2: Menjelaskan kegiatan ekonomi sederhana"
                    ]
                }
            }
        }
    
    def _initialize_phase_b_standards(self) -> Dict:
        """Initialize Phase B (Kelas 3-4) standards"""
        return {
            "IPA": {
                "phase": "B",
                "grade_range": "3-4",
                "subject": "IPA",
                "learning_objectives": [
                    "TP-1: Mengidentifikasi bagian tumbuhan dan hewan",
                    "TP-2: Mendeskripsikan perubahan bentuk benda",
                    "TP-3: Menerapkan konsep gaya dan gerak",
                    "TP-4: Menerapkan konsep energi",
                    "TP-5: Menerapkan konsep perubahan iklim"
                ],
                "competencies": {
                    "KI": [
                        "KI-1: Menghargai dan menghayati ajaran agama",
                        "KI-2: Menghargai dan menghayati perilaku jujur",
                        "KI-3: Memahami pengetahuan faktual konseptual IPA",
                        "KI-4: Menerapkan pengetahuan IPA dalam kehidupan"
                    ],
                    "KD": [
                        "KD 3.1: Mengidentifikasi bagian tumbuhan dan hewan",
                        "KD 3.2: Mendeskripsikan perubahan bentuk benda",
                        "KD 3.3: Menerapkan konsep gaya dan gerak",
                        "KD 4.1: Melakukan pengamatan pada tumbuhan dan hewan",
                        "KD 4.2: Menjelaskan pengaruh gaya pada gerak"
                    ]
                }
            }
        }
    
    def _initialize_phase_c_standards(self) -> Dict:
        """Initialize Phase C (Kelas 5-6) standards"""
        return {
            "IPA": {
                "phase": "C",
                "grade_range": "5-6",
                "subject": "IPA",
                "learning_objectives": [
                    "TP-1: Menganalisis sistem pencernaan manusia",
                    "TP-2: Menerapkan konsep listrik dinamis",
                    "TP-3: Menerapkan konsep perubahan zat",
                    "TP-4: Menganalisis sistem tata surya",
                    "TP-5: Menerapkan konsep bioteknologi"
                ],
                "competencies": {
                    "KI": [
                        "KI-1: Menghargai dan menghayati ajaran agama",
                        "KI-2: Menghargai dan menghayati perilaku jujur",
                        "KI-3: Memahami pengetahuan faktual konseptual IPA",
                        "KI-4: Menerapkan pengetahuan IPA dalam kehidupan"
                    ],
                    "KD": [
                        "KD 3.1: Menganalisis sistem pencernaan manusia",
                        "KD 3.2: Menerapkan konsep listrik dinamis",
                        "KD 3.3: Menerapkan konsep perubahan zat",
                        "KD 4.1: Mengamati sistem pencernaan manusia",
                        "KD 4.2: Menerapkan konsep listrik dalam kehidupan"
                    ]
                }
            }
        }
    
    def _initialize_phase_d_standards(self) -> Dict:
        """Initialize Phase D (Kelas 7-9) standards"""
        return {
            "IPA": {
                "phase": "D",
                "grade_range": "7-9",
                "subject": "IPA",
                "learning_objectives": [
                    "TP-1: Menganalisis sistem organisme",
                    "TP-2: Menerapkan konsep materi dan zat",
                    "TP-3: Menerapkan konsep energi dan perubahannya",
                    "TP-4: Menerapkan konsep bumi dan alam semesta",
                    "TP-5: Menerapkan konsep bioteknologi modern"
                ],
                "competencies": {
                    "KI": [
                        "KI-1: Menghargai dan menghayati ajaran agama",
                        "KI-2: Menghargai dan menghayati perilaku jujur",
                        "KI-3: Memahami pengetahuan faktual konseptual IPA",
                        "KI-4: Menerapkan pengetahuan IPA dalam kehidupan"
                    ],
                    "KD": [
                        "KD 3.1: Menganalisis sistem organisme",
                        "KD 3.2: Menerapkan konsep materi dan zat",
                        "KD 3.3: Menerapkan konsep energi dan perubahannya",
                        "KD 4.1: Mengamati sistem organisme",
                        "KD 4.2: Menerapkan konsep zat dalam kehidupan"
                    ]
                }
            }
        }
    
    def _initialize_subject_standards(self) -> Dict:
        """Initialize subject-specific standards"""
        return {
            "IPA": {
                "phases": ["A", "B", "C", "D"],
                "key_concepts": [
                    "Observation and investigation",
                    "Scientific method",
                    "Living organisms",
                    "Matter and energy",
                    "Earth and space",
                    "Biotechnology"
                ]
            },
            "IPS": {
                "phases": ["A", "B", "C", "D"],
                "key_concepts": [
                    "Identity and diversity",
                    "Environment and sustainability",
                    "Economic activities",
                    "Social interaction",
                    "Cultural heritage"
                ]
            },
            "Matematika": {
                "phases": ["A", "B", "C", "D"],
                "key_concepts": [
                    "Number operations",
                    "Geometry and measurement",
                    "Algebraic thinking",
                    "Data analysis",
                    "Problem solving"
                ]
            }
        }
    
    def _initialize_learning_objectives(self) -> Dict:
        """Initialize learning objectives database"""
        objectives_db = {}
        
        # Add learning objectives for each CP
        for phase, subjects in self.phase_standards.items():
            for subject, standards in subjects.items():
                cp_id = f"CP_{subject}_{phase}"
                objectives_db[cp_id] = standards.get("learning_objectives", [])
        
        return objectives_db
    
    def get_all_phases(self) -> List[str]:
        """Get all available phases"""
        return list(self.phase_standards.keys())
    
    def get_all_subjects_for_phase(self, phase: str) -> List[str]:
        """Get all subjects available for specific phase"""
        if phase not in self.phase_standards:
            return []
        return list(self.phase_standards[phase].keys())
    
    def export_standards_summary(self) -> Dict:
        """Export summary of all standards"""
        return {
            "phases": self.get_all_phases(),
            "subjects_by_phase": {
                phase: self.get_all_subjects_for_phase(phase)
                for phase in self.get_all_phases()
            },
            "total_cps": sum(len(subjects) for subjects in self.phase_standards.values()),
            "total_objectives": len(self.learning_objectives_db)
        }