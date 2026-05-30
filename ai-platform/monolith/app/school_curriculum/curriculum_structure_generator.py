"""
Curriculum Structure Generator

This module generates curriculum structure for KSP (Kurikulum Satuan Pendidikan).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class CurriculumComponent(str, Enum):
    """Types of curriculum components"""
    CP = "cp"
    TP = "tp"
    ATP = "atp"
    MODUL_AJAR = "modul_ajar"
    ASESMENT = "asesmen"
    P5 = "p5"


class CurriculumStructureGenerator:
    """Generator for curriculum structure"""
    
    def __init__(self):
        self.structure_templates = self._initialize_structure_templates()
    
    def generate_curriculum_structure(
        self, 
        school_data: Dict, 
        vision_mission: Dict,
        context_analysis: Dict
    ) -> Dict:
        """Generate comprehensive curriculum structure"""
        curriculum_structure = {
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("school_name", ""),
            "generation_date": datetime.utcnow().isoformat(),
            "curriculum_components": {},
            "integration_plan": {},
            "implementation_timeline": {}
        }
        
        # Generate each curriculum component
        curriculum_structure["curriculum_components"][CurriculumComponent.CP.value] = self._generate_cp_structure(
            school_data, context_analysis
        )
        curriculum_structure["curriculum_components"][CurriculumComponent.TP.value] = self._generate_tp_structure(
            school_data
        )
        curriculum_structure["curriculum_components"][CurriculumComponent.ATP.value] = self._generate_atp_structure(
            school_data
        )
        curriculum_structure["curriculum_components"][CurriculumComponent.MODUL_AJAR.value] = self._generate_modul_ajar_structure(
            school_data
        )
        curriculum_structure["curriculum_components"][CurriculumComponent.ASESMENT.value] = self._generate_assessment_structure(
            school_data
        )
        curriculum_structure["curriculum_components"][CurriculumComponent.P5.value] = self._generate_p5_structure(
            school_data
        )
        
        # Generate integration plan
        curriculum_structure["integration_plan"] = self._generate_integration_plan(
            curriculum_structure["curriculum_components"]
        )
        
        # Generate implementation timeline
        curriculum_structure["implementation_timeline"] = self._generate_implementation_timeline(
            curriculum_structure["curriculum_components"]
        )
        
        return curriculum_structure
    
    def _generate_cp_structure(self, school_data: Dict, context_analysis: Dict) -> Dict:
        """Generate CP structure"""
        school_level = school_data.get("school_level", "")
        mata_pelajaran_list = school_data.get("mata_pelajaran", [])
        
        return {
            "component": CurriculumComponent.CP.value,
            "description": "Capaian Pembelajaran structure",
            "fase_coverage": self._determine_fase_coverage(school_level),
            "mata_pelajaran": mata_pelajaran_list,
            "cp_per_mata_pelajaran": self._estimate_cp_count(mata_pelajaran_list),
            "alignment_with_kurikulum_merdeka": True,
            "context_adaptation": self._generate_context_adaptation(context_analysis)
        }
    
    def _generate_tp_structure(self, school_data: Dict) -> Dict:
        """Generate TP structure"""
        mata_pelajaran_list = school_data.get("mata_pelajaran", [])
        
        return {
            "component": CurriculumComponent.TP.value,
            "description": "Tujuan Pembelajaran structure",
            "tp_derivation": "CP-based",
            "tp_per_cp": 3,
            "domain_distribution": {
                "kognitif": 0.6,
                "psikomotorik": 0.25,
                "afektif": 0.15
            },
            "difficulty_distribution": {
                "mudah": 0.2,
                "sedang": 0.6,
                "sulit": 0.2
            }
        }
    
    def _generate_atp_structure(self, school_data: Dict) -> Dict:
        """Generate ATP structure"""
        school_level = school_data.get("school_level", "")
        
        return {
            "component": CurriculumComponent.ATP.value,
            "description": "Alur Tujuan Pembelajaran structure",
            "periods_per_year": 4,
            "weeks_per_period": 8,
            "tp_per_period": self._estimate_tp_per_period(school_level),
            "integration_with_modul_ajar": True
        }
    
    def _generate_modul_ajar_structure(self, school_data: Dict) -> Dict:
        """Generate Modul Ajar structure"""
        school_level = school_data.get("school_level", "")
        
        return {
            "component": CurriculumComponent.MODUL_AJAR.value,
            "description": "Modul Ajar structure",
            "modul_ajar_per_atp": 1,
            "pemahaman_bermakna": True,
            "inquiry_based": True,
            "differentiated": True,
            "p5_integration": True,
            "template_structure": self._generate_modul_ajar_template(school_level)
        }
    
    def _generate_assessment_structure(self, school_data: Dict) -> Dict:
        """Generate assessment structure"""
        return {
            "component": CurriculumComponent.ASESMENT.value,
            "description": "Assessment structure",
            "assessment_types": ["formatif", "sumatif", "diagnostik", "kinerja"],
            "assessment_frequency": {
                "formatif": "weekly",
                "sumatif": "end_of_period",
                "diagnostik": "beginning_of_year",
                "kinerja": "as_needed"
            },
            "rubric_based": True,
            "performance_based": True
        }
    
    def _generate_p5_structure(self, school_data: Dict) -> Dict:
        """Generate P5 structure"""
        return {
            "component": CurriculumComponent.P5.value,
            "description": "Projek Penguatan Profil Pelajar Pancasila structure",
            "p5_per_year": 2,
            "dimensions": [
                "Beriman, bertakwa kepada Tuhan YME",
                "Berkebinekaan global",
                "Gotong royong",
                "Kreatif",
                "Mandiri",
                "Bernalar kritis"
            ],
            "project_duration": "4-6 minggu",
            "integration_with_mata_pelajaran": True
        }
    
    def _generate_integration_plan(self, curriculum_components: Dict) -> Dict:
        """Generate integration plan for curriculum components"""
        return {
            "cp_to_tp_integration": {
                "method": "derivation",
                "ratio": "1 CP : 3 TP"
            },
            "tp_to_atp_integration": {
                "method": "sequencing",
                "structure": "period-based"
            },
            "atp_to_modul_ajar_integration": {
                "method": "direct_mapping",
                "ratio": "1 ATP : 1 Modul Ajar"
            },
            "modul_ajar_to_assessment_integration": {
                "method": "alignment",
                "type": "TP-based"
            },
            "p5_integration": {
                "method": "cross-curricular",
                "frequency": "2 projects per year"
            }
        }
    
    def _generate_implementation_timeline(self, curriculum_components: Dict) -> Dict:
        """Generate implementation timeline"""
        return {
            "year_1": {
                "focus": "CP and TP development",
                "components": ["CP", "TP"],
                "timeline": "Jan - Jun"
            },
            "year_1_continued": {
                "focus": "ATP and Modul Ajar development",
                "components": ["ATP", "MODUL_AJAR"],
                "timeline": "Jul - Dec"
            },
            "year_2": {
                "focus": "Assessment and P5 implementation",
                "components": ["ASESMEN", "P5"],
                "timeline": "Jan - Jun"
            },
            "year_2_continued": {
                "focus": "Full implementation and review",
                "components": ["ALL"],
                "timeline": "Jul - Dec"
            }
        }
    
    def _determine_fase_coverage(self, school_level: str) -> List[str]:
        """Determine fase coverage based on school level"""
        if "SD" in school_level:
            return ["A", "B", "C"]
        elif "SMP" in school_level:
            return ["C", "D"]
        elif "SMA" in school_level:
            return ["E"]
        else:
            return ["A", "B", "C", "D", "E"]
    
    def _estimate_cp_count(self, mata_pelajaran_list: List[str]) -> Dict:
        """Estimate CP count per mata pelajaran"""
        return {
            mata_pelajaran: 3 for mata_pelajaran in mata_pelajaran_list
        }
    
    def _estimate_tp_per_period(self, school_level: str) -> int:
        """Estimate TP per period based on school level"""
        if "SD" in school_level:
            return 5
        elif "SMP" in school_level:
            return 7
        elif "SMA" in school_level:
            return 10
        else:
            return 6
    
    def _generate_context_adaptation(self, context_analysis: Dict) -> Dict:
        """Generate context adaptation recommendations"""
        context_factors = context_analysis.get("context_factors", {})
        
        adaptations = []
        
        # Cultural adaptation
        if context_factors.get("cultural", {}).get("score", 0) >= 0.7:
            adaptations.append({
                "factor": "cultural",
                "adaptation": "Integrate local culture into curriculum"
            })
        
        # Infrastructure adaptation
        if context_factors.get("infrastructure", {}).get("score", 0) < 0.5:
            adaptations.append({
                "factor": "infrastructure",
                "adaptation": "Adapt curriculum to available facilities"
            })
        
        # Human resources adaptation
        if context_factors.get("human_resources", {}).get("score", 0) < 0.5:
            adaptations.append({
                "factor": "human_resources",
                "adaptation": "Provide teacher training and support"
            })
        
        return adaptations
    
    def _generate_modul_ajar_template(self, school_level: str) -> Dict:
        """Generate Modul Ajar template structure"""
        return {
            "sections": [
                "Informasi Umum",
                "Tujuan Pembelajaran",
                "Pemahaman Bermakna",
                "Pertanyaan Pemantik",
                "Kegiatan Pembelajaran",
                "Asesmen",
                "Refleksi"
            ],
            "required_elements": [
                "Informasi fase, mata pelajaran, topik",
                "Tujuan pembelajaran",
                "Pemahaman bermakna",
                "Kegiatan pembelajaran",
                "Asesmen"
            ],
            "optional_elements": [
                "P5 project",
                "Differentiated activities",
                "Additional resources"
            ]
        }
    
    def _initialize_structure_templates(self) -> Dict:
        """Initialize curriculum structure templates"""
        return {
            "cp": {
                "min_cp_per_mata_pelajaran": 3,
                "max_cp_per_mata_pelajaran": 5
            },
            "tp": {
                "min_tp_per_cp": 2,
                "max_tp_per_cp": 4
            },
            "atp": {
                "periods_per_year": 4,
                "weeks_per_period": 8
            },
            "modul_ajar": {
                "sections": 7,
                "required_elements": 5
            }
        }
