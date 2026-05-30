"""
School Context Analysis

This module analyzes the context of a school for KSP (Kurikulum Satuan Pendidikan) development.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ContextFactor(str, Enum):
    """Types of school context factors"""
    GEOGRAPHICAL = "geographical"
    DEMOGRAPHIC = "demographic"
    ECONOMIC = "economic"
    CULTURAL = "cultural"
    INFRASTRUCTURE = "infrastructure"
    HUMAN_RESOURCES = "human_resources"


class SchoolContextAnalysis:
    """Analyzer for school context"""
    
    def __init__(self):
        self.context_factors = self._initialize_context_factors()
        self.analysis_data: Dict[str, Dict] = {}
    
    def analyze_school_context(self, school_data: Dict) -> Dict:
        """Analyze comprehensive school context"""
        analysis = {
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("school_name", ""),
            "analysis_date": datetime.utcnow().isoformat(),
            "context_factors": {},
            "strengths": [],
            "challenges": [],
            "opportunities": [],
            "recommendations": []
        }
        
        # Analyze each context factor
        for factor in ContextFactor:
            factor_analysis = self._analyze_factor(school_data, factor)
            analysis["context_factors"][factor.value] = factor_analysis
        
        # Identify strengths, challenges, and opportunities
        analysis["strengths"] = self._identify_strengths(analysis["context_factors"])
        analysis["challenges"] = self._identify_challenges(analysis["context_factors"])
        analysis["opportunities"] = self._identify_opportunities(analysis["context_factors"])
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(
            analysis["strengths"],
            analysis["challenges"],
            analysis["opportunities"]
        )
        
        return analysis
    
    def _analyze_factor(self, school_data: Dict, factor: ContextFactor) -> Dict:
        """Analyze a specific context factor"""
        factor_analysis = {
            "factor": factor.value,
            "status": "unknown",
            "score": 0.5,
            "description": "",
            "indicators": []
        }
        
        if factor == ContextFactor.GEOGRAPHICAL:
            factor_analysis = self._analyze_geographical_context(school_data)
        elif factor == ContextFactor.DEMOGRAPHIC:
            factor_analysis = self._analyze_demographic_context(school_data)
        elif factor == ContextFactor.ECONOMIC:
            factor_analysis = self._analyze_economic_context(school_data)
        elif factor == ContextFactor.CULTURAL:
            factor_analysis = self._analyze_cultural_context(school_data)
        elif factor == ContextFactor.INFRASTRUCTURE:
            factor_analysis = self._analyze_infrastructure_context(school_data)
        elif factor == ContextFactor.HUMAN_RESOURCES:
            factor_analysis = self._analyze_human_resources_context(school_data)
        
        return factor_analysis
    
    def _analyze_geographical_context(self, school_data: Dict) -> Dict:
        """Analyze geographical context"""
        location = school_data.get("location", {})
        
        return {
            "factor": ContextFactor.GEOGRAPHICAL.value,
            "status": "analyzed",
            "score": 0.7,
            "description": f"School located in {location.get('province', 'unknown')}, {location.get('city', 'unknown')}",
            "indicators": [
                f"Province: {location.get('province', 'unknown')}",
                f"City: {location.get('city', 'unknown')}",
                f"Area type: {location.get('area_type', 'unknown')}"
            ]
        }
    
    def _analyze_demographic_context(self, school_data: Dict) -> Dict:
        """Analyze demographic context"""
        demographics = school_data.get("demographics", {})
        
        return {
            "factor": ContextFactor.DEMOGRAPHIC.value,
            "status": "analyzed",
            "score": 0.6,
            "description": f"Student population: {demographics.get('total_students', 'unknown')}",
            "indicators": [
                f"Total students: {demographics.get('total_students', 'unknown')}",
                f"Student diversity: {demographics.get('diversity', 'unknown')}",
                f"Special needs: {demographics.get('special_needs', 'unknown')}"
            ]
        }
    
    def _analyze_economic_context(self, school_data: Dict) -> Dict:
        """Analyze economic context"""
        economic = school_data.get("economic", {})
        
        return {
            "factor": ContextFactor.ECONOMIC.value,
            "status": "analyzed",
            "score": 0.5,
            "description": f"Economic status: {economic.get('status', 'unknown')}",
            "indicators": [
                f"Economic level: {economic.get('status', 'unknown')}",
                f"Parent occupation: {economic.get('parent_occupation', 'unknown')}",
                f"School funding: {economic.get('funding', 'unknown')}"
            ]
        }
    
    def _analyze_cultural_context(self, school_data: Dict) -> Dict:
        """Analyze cultural context"""
        cultural = school_data.get("cultural", {})
        
        return {
            "factor": ContextFactor.CULTURAL.value,
            "status": "analyzed",
            "score": 0.7,
            "description": f"Cultural background: {cultural.get('background', 'unknown')}",
            "indicators": [
                f"Local culture: {cultural.get('local_culture', 'unknown')}",
                f"Language: {cultural.get('language', 'unknown')}",
                f"Traditions: {cultural.get('traditions', 'unknown')}"
            ]
        }
    
    def _analyze_infrastructure_context(self, school_data: Dict) -> Dict:
        """Analyze infrastructure context"""
        infrastructure = school_data.get("infrastructure", {})
        
        return {
            "factor": ContextFactor.INFRASTRUCTURE.value,
            "status": "analyzed",
            "score": 0.6,
            "description": f"Infrastructure quality: {infrastructure.get('quality', 'unknown')}",
            "indicators": [
                f"Building condition: {infrastructure.get('building_condition', 'unknown')}",
                f"Classrooms: {infrastructure.get('classrooms', 'unknown')}",
                f"Facilities: {infrastructure.get('facilities', 'unknown')}"
            ]
        }
    
    def _analyze_human_resources_context(self, school_data: Dict) -> Dict:
        """Analyze human resources context"""
        hr = school_data.get("human_resources", {})
        
        return {
            "factor": ContextFactor.HUMAN_RESOURCES.value,
            "status": "analyzed",
            "score": 0.7,
            "description": f"Teacher quality: {hr.get('teacher_quality', 'unknown')}",
            "indicators": [
                f"Total teachers: {hr.get('total_teachers', 'unknown')}",
                f"Teacher qualifications: {hr.get('qualifications', 'unknown')}",
                f"Teacher experience: {hr.get('experience', 'unknown')}"
            ]
        }
    
    def _identify_strengths(self, context_factors: Dict) -> List[str]:
        """Identify school strengths from context analysis"""
        strengths = []
        
        for factor_name, factor_data in context_factors.items():
            if factor_data.get("score", 0) >= 0.7:
                strengths.append(f"Strong {factor_name}: {factor_data.get('description', '')}")
        
        return strengths
    
    def _identify_challenges(self, context_factors: Dict) -> List[str]:
        """Identify school challenges from context analysis"""
        challenges = []
        
        for factor_name, factor_data in context_factors.items():
            if factor_data.get("score", 0) < 0.5:
                challenges.append(f"Challenge in {factor_name}: {factor_data.get('description', '')}")
        
        return challenges
    
    def _identify_opportunities(self, context_factors: Dict) -> List[str]:
        """Identify opportunities from context analysis"""
        opportunities = []
        
        # Look for factors with moderate scores that can be improved
        for factor_name, factor_data in context_factors.items():
            score = factor_data.get("score", 0)
            if 0.5 <= score < 0.7:
                opportunities.append(f"Opportunity to improve {factor_name}")
        
        return opportunities
    
    def _generate_recommendations(
        self, 
        strengths: List[str], 
        challenges: List[str], 
        opportunities: List[str]
    ) -> List[str]:
        """Generate recommendations based on context analysis"""
        recommendations = []
        
        # Leverage strengths
        if strengths:
            recommendations.append(f"Leverage strengths: {', '.join(strengths[:2])}")
        
        # Address challenges
        if challenges:
            recommendations.append(f"Address challenges: {', '.join(challenges[:2])}")
        
        # Pursue opportunities
        if opportunities:
            recommendations.append(f"Pursue opportunities: {', '.join(opportunities[:2])}")
        
        return recommendations
    
    def _initialize_context_factors(self) -> Dict:
        """Initialize context factor definitions"""
        return {
            ContextFactor.GEOGRAPHICAL.value: {
                "description": "Geographical location and environment",
                "indicators": ["province", "city", "area_type", "accessibility"]
            },
            ContextFactor.DEMOGRAPHIC.value: {
                "description": "Student and community demographics",
                "indicators": ["total_students", "diversity", "special_needs", "age_distribution"]
            },
            ContextFactor.ECONOMIC.value: {
                "description": "Economic conditions of school community",
                "indicators": ["status", "parent_occupation", "funding", "resources"]
            },
            ContextFactor.CULTURAL.value: {
                "description": "Cultural background and traditions",
                "indicators": ["local_culture", "language", "traditions", "values"]
            },
            ContextFactor.INFRASTRUCTURE.value: {
                "description": "Physical infrastructure and facilities",
                "indicators": ["building_condition", "classrooms", "facilities", "equipment"]
            },
            ContextFactor.HUMAN_RESOURCES.value: {
                "description": "Teachers and staff quality",
                "indicators": ["total_teachers", "qualifications", "experience", "training"]
            }
        }
