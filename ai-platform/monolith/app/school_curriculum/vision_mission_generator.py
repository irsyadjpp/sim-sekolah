"""
Vision Mission Generator

This module generates vision and mission statements for schools based on context and SWOT analysis.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class VisionMissionType(str, Enum):
    """Types of vision and mission statements"""
    VISION = "vision"
    MISSION = "mission"
    VALUES = "values"


class VisionMissionGenerator:
    """Generator for school vision and mission statements"""
    
    def __init__(self):
        self.vision_templates = self._initialize_vision_templates()
        self.mission_templates = self._initialize_mission_templates()
        self.values_templates = self._initialize_values_templates()
    
    def generate_vision_mission(
        self, 
        school_data: Dict, 
        context_analysis: Dict,
        swot_analysis: Dict
    ) -> Dict:
        """Generate comprehensive vision and mission statements"""
        vision_mission = {
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("school_name", ""),
            "generation_date": datetime.utcnow().isoformat(),
            "vision": {},
            "mission": {},
            "values": {},
            "strategic_goals": []
        }
        
        # Generate vision statement
        vision_mission["vision"] = self._generate_vision(
            school_data, context_analysis, swot_analysis
        )
        
        # Generate mission statement
        vision_mission["mission"] = self._generate_mission(
            school_data, context_analysis, swot_analysis
        )
        
        # Generate values
        vision_mission["values"] = self._generate_values(
            school_data, context_analysis
        )
        
        # Generate strategic goals
        vision_mission["strategic_goals"] = self._generate_strategic_goals(
            vision_mission["vision"],
            vision_mission["mission"],
            swot_analysis
        )
        
        return vision_mission
    
    def _generate_vision(
        self, 
        school_data: Dict, 
        context_analysis: Dict,
        swot_analysis: Dict
    ) -> Dict:
        """Generate vision statement"""
        school_name = school_data.get("school_name", "")
        school_level = school_data.get("school_level", "")
        
        # Analyze strengths for vision
        strengths = swot_analysis.get("swot_matrix", {}).get("strengths", [])
        key_strengths = [s["factor"] for s in strengths[:3]]
        
        # Generate vision statement
        vision_statement = self._construct_vision_statement(
            school_name, school_level, key_strengths
        )
        
        return {
            "type": VisionMissionType.VISION.value,
            "statement": vision_statement,
            "key_elements": key_strengths,
            "timeframe": "5-10 tahun",
            "description": f"Vision for {school_name} to become a leading {school_level}"
        }
    
    def _generate_mission(
        self, 
        school_data: Dict, 
        context_analysis: Dict,
        swot_analysis: Dict
    ) -> Dict:
        """Generate mission statement"""
        school_name = school_data.get("school_name", "")
        school_level = school_data.get("school_level", "")
        
        # Analyze context and SWOT for mission
        context_factors = context_analysis.get("context_factors", {})
        opportunities = swot_analysis.get("swot_matrix", {}).get("opportunities", [])
        
        # Generate mission components
        mission_components = self._construct_mission_components(
            school_name, school_level, context_factors, opportunities
        )
        
        return {
            "type": VisionMissionType.MISSION.value,
            "statement": self._combine_mission_components(mission_components),
            "components": mission_components,
            "description": f"Mission of {school_name} to achieve its vision"
        }
    
    def _generate_values(
        self, 
        school_data: Dict, 
        context_analysis: Dict
    ) -> Dict:
        """Generate school values"""
        cultural_context = context_analysis.get("context_factors", {}).get("cultural", {})
        
        # Base values from Kurikulum Merdeka
        base_values = [
            "Beriman, bertakwa kepada Tuhan YME",
            "Berkebinekaan global",
            "Gotong royong",
            "Kreatif",
            "Mandiri",
            "Bernalar kritis"
        ]
        
        # Add context-specific values
        context_values = []
        if cultural_context.get("score", 0) >= 0.7:
            context_values.append("Menghargai budaya lokal")
        
        return {
            "type": VisionMissionType.VALUES.value,
            "core_values": base_values,
            "context_values": context_values,
            "description": "Core values guiding school operations"
        }
    
    def _generate_strategic_goals(
        self, 
        vision: Dict, 
        mission: Dict,
        swot_analysis: Dict
    ) -> List[Dict]:
        """Generate strategic goals based on vision, mission, and SWOT"""
        goals = []
        
        # Goals from vision
        vision_elements = vision.get("key_elements", [])
        for element in vision_elements:
            goals.append({
                "goal": f"Enhance {element}",
                "category": "vision",
                "priority": "high",
                "timeframe": "3-5 tahun"
            })
        
        # Goals from SWOT opportunities
        opportunities = swot_analysis.get("swot_matrix", {}).get("opportunities", [])
        for opp in opportunities[:2]:
            goals.append({
                "goal": f"Pursue {opp['factor']}",
                "category": "opportunity",
                "priority": "medium",
                "timeframe": "2-3 tahun"
            })
        
        # Goals from SWOT weaknesses
        weaknesses = swot_analysis.get("swot_matrix", {}).get("weaknesses", [])
        for weakness in weaknesses[:2]:
            goals.append({
                "goal": f"Address {weakness['factor']}",
                "category": "improvement",
                "priority": "high",
                "timeframe": "1-2 tahun"
            })
        
        return goals
    
    def _construct_vision_statement(
        self, 
        school_name: str, 
        school_level: str, 
        key_strengths: List[str]
    ) -> str:
        """Construct vision statement"""
        if not key_strengths:
            key_strengths = ["akademik", "karakter"]
        
        vision_templates = [
            f"Menjadi {school_level} unggulan yang menghasilkan lulusan berkarakter dan berprestasi",
            f"Menjadi pusat keunggulan {school_level} yang mengintegrasikan {', '.join(key_strengths[:2])}",
            f"Menjadi {school_level} terdepan dalam pembentukan karakter dan prestasi akademik",
            f"Menjadi {school_level} yang menginspirasi dan memberdayakan generasi masa depan"
        ]
        
        # Select appropriate template based on school level
        if "SD" in school_level:
            return vision_templates[0]
        elif "SMP" in school_level:
            return vision_templates[1]
        elif "SMA" in school_level:
            return vision_templates[2]
        else:
            return vision_templates[3]
    
    def _construct_mission_components(
        self, 
        school_name: str, 
        school_level: str, 
        context_factors: Dict,
        opportunities: List[Dict]
    ) -> List[str]:
        """Construct mission components"""
        components = []
        
        # Component 1: Academic excellence
        components.append(
            "Menyelenggarakan pendidikan berkualitas yang mengembangkan potensi akademik peserta didik"
        )
        
        # Component 2: Character development
        components.append(
            "Membentuk karakter peserta didik sesuai Profil Pelajar Pancasila"
        )
        
        # Component 3: Context-specific component
        if context_factors.get("cultural", {}).get("score", 0) >= 0.7:
            components.append(
                "Mengembangkan potensi peserta didik dengan memperhatikan konteks budaya lokal"
            )
        
        # Component 4: Innovation
        if any("technology" in opp["factor"] for opp in opportunities):
            components.append(
                "Mengintegrasikan teknologi dalam pembelajaran untuk meningkatkan kualitas pendidikan"
            )
        
        # Component 5: Community
        components.append(
            "Membangun kemitraan dengan masyarakat untuk mendukung pembelajaran"
        )
        
        return components
    
    def _combine_mission_components(self, components: List[str]) -> str:
        """Combine mission components into a single statement"""
        if not components:
            return "Menyelenggarakan pendidikan berkualitas untuk mengembangkan potensi peserta didik"
        
        return " ".join(components)
    
    def _initialize_vision_templates(self) -> Dict:
        """Initialize vision statement templates"""
        return {
            "SD": [
                "Menjadi SD unggulan yang menghasilkan lulusan berkarakter dan berprestasi",
                "Menjadi SD yang mencetak generasi cerdas, berkarakter, dan berakhlak mulia"
            ],
            "SMP": [
                "Menjadi SMP unggulan yang mengintegrasikan akademik dan karakter",
                "Menjadi SMP yang mengembangkan potensi peserta didik secara holistik"
            ],
            "SMA": [
                "Menjadi SMA terdepan dalam pembentukan karakter dan prestasi akademik",
                "Menjadi SMA yang menghasilkan lulusan siap kuliah dan berkarakter"
            ]
        }
    
    def _initialize_mission_templates(self) -> Dict:
        """Initialize mission statement templates"""
        return {
            "components": [
                "Menyelenggarakan pendidikan berkualitas",
                "Membentuk karakter peserta didik",
                "Mengembangkan potensi peserta didik",
                "Membangun kemitraan dengan masyarakat"
            ]
        }
    
    def _initialize_values_templates(self) -> Dict:
        """Initialize values templates"""
        return {
            "profil_pelajar_pancasila": [
                "Beriman, bertakwa kepada Tuhan YME",
                "Berkebinekaan global",
                "Gotong royong",
                "Kreatif",
                "Mandiri",
                "Bernalar kritis"
            ],
            "additional_values": [
                "Jujur",
                "Disiplin",
                "Tanggung jawab",
                "Peduli",
                "Santun"
            ]
        }
