"""
School Profile Generator

This module generates comprehensive school profiles for KSP (Kurikulum Satuan Pendidikan).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ProfileSection(str, Enum):
    """School profile sections"""
    GENERAL = "general"
    ACADEMIC = "academic"
    FACILITIES = "facilities"
    HUMAN_RESOURCES = "human_resources"
    ACHIEVEMENTS = "achievements"
    CHALLENGES = "challenges"


class SchoolProfileGenerator:
    """Generator for school profiles"""
    
    def __init__(self):
        self.profile_templates = self._initialize_profile_templates()
    
    def generate_school_profile(
        self, 
        school_data: Dict, 
        context_analysis: Dict,
        swot_analysis: Dict
    ) -> Dict:
        """Generate comprehensive school profile"""
        profile = {
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("school_name", ""),
            "profile_date": datetime.utcnow().isoformat(),
            "profile_sections": {},
            "summary": "",
            "key_highlights": []
        }
        
        # Generate each profile section
        profile["profile_sections"][ProfileSection.GENERAL.value] = self._generate_general_section(
            school_data
        )
        profile["profile_sections"][ProfileSection.ACADEMIC.value] = self._generate_academic_section(
            school_data
        )
        profile["profile_sections"][ProfileSection.FACILITIES.value] = self._generate_facilities_section(
            school_data
        )
        profile["profile_sections"][ProfileSection.HUMAN_RESOURCES.value] = self._generate_hr_section(
            school_data
        )
        profile["profile_sections"][ProfileSection.ACHIEVEMENTS.value] = self._generate_achievements_section(
            school_data
        )
        profile["profile_sections"][ProfileSection.CHALLENGES.value] = self._generate_challenges_section(
            swot_analysis
        )
        
        # Generate summary
        profile["summary"] = self._generate_summary(profile["profile_sections"])
        
        # Generate key highlights
        profile["key_highlights"] = self._generate_key_highlights(profile["profile_sections"])
        
        return profile
    
    def _generate_general_section(self, school_data: Dict) -> Dict:
        """Generate general information section"""
        return {
            "section": ProfileSection.GENERAL.value,
            "school_name": school_data.get("school_name", ""),
            "npsn": school_data.get("npsn", ""),
            "address": school_data.get("address", {}),
            "contact": school_data.get("contact", {}),
            "establishment_date": school_data.get("establishment_date", ""),
            "school_level": school_data.get("school_level", ""),
            "accreditation": school_data.get("accreditation_status", ""),
            "principal": school_data.get("principal", ""),
            "total_students": school_data.get("demographics", {}).get("total_students", 0),
            "total_teachers": school_data.get("human_resources", {}).get("total_teachers", 0)
        }
    
    def _generate_academic_section(self, school_data: Dict) -> Dict:
        """Generate academic information section"""
        academic = school_data.get("academic", {})
        
        return {
            "section": ProfileSection.ACADEMIC.value,
            "curriculum": academic.get("curriculum", "Kurikulum Merdeka"),
            "programs_offered": academic.get("programs", []),
            "student_achievement_rate": academic.get("achievement_rate", 0),
            "graduation_rate": academic.get("graduation_rate", 0),
            "special_programs": academic.get("special_programs", []),
            "extracurricular_activities": academic.get("extracurricular", []),
            "assessment_methods": academic.get("assessment_methods", [])
        }
    
    def _generate_facilities_section(self, school_data: Dict) -> Dict:
        """Generate facilities information section"""
        infrastructure = school_data.get("infrastructure", {})
        
        return {
            "section": ProfileSection.FACILITIES.value,
            "building_condition": infrastructure.get("building_condition", ""),
            "total_classrooms": infrastructure.get("classrooms", 0),
            "laboratories": infrastructure.get("laboratories", []),
            "library": infrastructure.get("library", {}),
            "sports_facilities": infrastructure.get("sports_facilities", []),
            "technology_facilities": infrastructure.get("technology_facilities", []),
            "other_facilities": infrastructure.get("other_facilities", [])
        }
    
    def _generate_hr_section(self, school_data: Dict) -> Dict:
        """Generate human resources information section"""
        hr = school_data.get("human_resources", {})
        
        return {
            "section": ProfileSection.HUMAN_RESOURCES.value,
            "total_teachers": hr.get("total_teachers", 0),
            "teacher_qualifications": hr.get("qualifications", {}),
            "teacher_experience": hr.get("experience", {}),
            "professional_development": hr.get("professional_development", []),
            "administrative_staff": hr.get("administrative_staff", 0),
            "support_staff": hr.get("support_staff", 0)
        }
    
    def _generate_achievements_section(self, school_data: Dict) -> Dict:
        """Generate achievements section"""
        achievements = school_data.get("achievements", [])
        
        return {
            "section": ProfileSection.ACHIEVEMENTS.value,
            "academic_achievements": [a for a in achievements if a.get("type") == "academic"],
            "non_academic_achievements": [a for a in achievements if a.get("type") == "non_academic"],
            "awards": school_data.get("awards", []),
            "recognitions": school_data.get("recognitions", []),
            "partnerships": school_data.get("partnerships", [])
        }
    
    def _generate_challenges_section(self, swot_analysis: Dict) -> Dict:
        """Generate challenges section from SWOT analysis"""
        swot_matrix = swot_analysis.get("swot_matrix", {})
        weaknesses = swot_matrix.get("weaknesses", [])
        threats = swot_matrix.get("threats", [])
        
        return {
            "section": ProfileSection.CHALLENGES.value,
            "weaknesses": weaknesses,
            "threats": threats,
            "priority_actions": swot_analysis.get("priority_actions", [])
        }
    
    def _generate_summary(self, profile_sections: Dict) -> str:
        """Generate profile summary"""
        general = profile_sections.get(ProfileSection.GENERAL.value, {})
        academic = profile_sections.get(ProfileSection.ACADEMIC.value, {})
        
        summary = f"""
{general.get('school_name', 'School')} is a {general.get('school_level', 'educational institution')} 
located in {general.get('address', {}).get('city', 'unknown')}. 

The school serves {general.get('total_students', 0)} students with {general.get('total_teachers', 0)} teachers, 
implementing the {academic.get('curriculum', 'Kurikulum Merdeka')} curriculum.

The school has achieved a {general.get('accreditation', 'unknown')} accreditation status and maintains 
a student achievement rate of {academic.get('student_achievement_rate', 0)}%.
"""
        
        return summary.strip()
    
    def _generate_key_highlights(self, profile_sections: Dict) -> List[str]:
        """Generate key highlights from profile"""
        highlights = []
        
        general = profile_sections.get(ProfileSection.GENERAL.value, {})
        academic = profile_sections.get(ProfileSection.ACADEMIC.value, {})
        facilities = profile_sections.get(ProfileSection.FACILITIES.value, {})
        
        # General highlights
        if general.get("accreditation") == "A":
            highlights.append(f"Excellent accreditation status: {general['accreditation']}")
        
        if general.get("total_students") > 500:
            highlights.append(f"Large student population: {general['total_students']} students")
        
        # Academic highlights
        if academic.get("student_achievement_rate") > 80:
            highlights.append(f"High student achievement: {academic['student_achievement_rate']}%")
        
        if academic.get("graduation_rate") > 90:
            highlights.append(f"High graduation rate: {academic['graduation_rate']}%")
        
        # Facilities highlights
        if facilities.get("total_classrooms") > 20:
            highlights.append(f"Well-equipped with {facilities['total_classrooms']} classrooms")
        
        if len(facilities.get("laboratories", [])) > 3:
            highlights.append(f"Multiple laboratories: {len(facilities['laboratories'])} labs")
        
        return highlights
    
    def _initialize_profile_templates(self) -> Dict:
        """Initialize profile templates"""
        return {
            "general": {
                "required_fields": ["school_name", "npsn", "address", "school_level"],
                "optional_fields": ["accreditation", "principal", "establishment_date"]
            },
            "academic": {
                "required_fields": ["curriculum", "programs_offered"],
                "optional_fields": ["special_programs", "extracurricular_activities"]
            },
            "facilities": {
                "required_fields": ["building_condition", "total_classrooms"],
                "optional_fields": ["laboratories", "library", "sports_facilities"]
            },
            "human_resources": {
                "required_fields": ["total_teachers", "teacher_qualifications"],
                "optional_fields": ["professional_development", "administrative_staff"]
            }
        }
