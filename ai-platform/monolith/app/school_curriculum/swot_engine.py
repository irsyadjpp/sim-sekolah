"""
SWOT Analysis Engine

This module performs SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis for schools.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class SWOTCategory(str, Enum):
    """SWOT categories"""
    STRENGTHS = "strengths"
    WEAKNESSES = "weaknesses"
    OPPORTUNITIES = "opportunities"
    THREATS = "threats"


class SWOTAnalysisEngine:
    """Engine for SWOT analysis"""
    
    def __init__(self):
        self.swot_templates = self._initialize_swot_templates()
    
    def perform_swot_analysis(self, school_data: Dict, context_analysis: Dict) -> Dict:
        """Perform comprehensive SWOT analysis"""
        swot_result = {
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("school_name", ""),
            "analysis_date": datetime.utcnow().isoformat(),
            "swot_matrix": {},
            "strategic_recommendations": [],
            "priority_actions": []
        }
        
        # Analyze each SWOT category
        swot_result["swot_matrix"][SWOTCategory.STRENGTHS.value] = self._analyze_strengths(
            school_data, context_analysis
        )
        swot_result["swot_matrix"][SWOTCategory.WEAKNESSES.value] = self._analyze_weaknesses(
            school_data, context_analysis
        )
        swot_result["swot_matrix"][SWOTCategory.OPPORTUNITIES.value] = self._analyze_opportunities(
            school_data, context_analysis
        )
        swot_result["swot_matrix"][SWOTCategory.THREATS.value] = self._analyze_threats(
            school_data, context_analysis
        )
        
        # Generate strategic recommendations
        swot_result["strategic_recommendations"] = self._generate_strategic_recommendations(
            swot_result["swot_matrix"]
        )
        
        # Generate priority actions
        swot_result["priority_actions"] = self._generate_priority_actions(
            swot_result["swot_matrix"]
        )
        
        return swot_result
    
    def _analyze_strengths(self, school_data: Dict, context_analysis: Dict) -> List[Dict]:
        """Analyze school strengths"""
        strengths = []
        
        # Analyze context factors for strengths
        context_factors = context_analysis.get("context_factors", {})
        
        for factor_name, factor_data in context_factors.items():
            if factor_data.get("score", 0) >= 0.7:
                strengths.append({
                    "factor": factor_name,
                    "description": factor_data.get("description", ""),
                    "score": factor_data.get("score", 0),
                    "indicators": factor_data.get("indicators", [])
                })
        
        # Add school-specific strengths
        if school_data.get("accreditation_status") == "A":
            strengths.append({
                "factor": "accreditation",
                "description": "Excellent accreditation status",
                "score": 0.9,
                "indicators": ["Accreditation A"]
            })
        
        if school_data.get("student_achievement", 0) >= 80:
            strengths.append({
                "factor": "student_achievement",
                "description": "High student achievement",
                "score": 0.8,
                "indicators": ["Student achievement above 80%"]
            })
        
        return strengths
    
    def _analyze_weaknesses(self, school_data: Dict, context_analysis: Dict) -> List[Dict]:
        """Analyze school weaknesses"""
        weaknesses = []
        
        # Analyze context factors for weaknesses
        context_factors = context_analysis.get("context_factors", {})
        
        for factor_name, factor_data in context_factors.items():
            if factor_data.get("score", 0) < 0.5:
                weaknesses.append({
                    "factor": factor_name,
                    "description": factor_data.get("description", ""),
                    "score": factor_data.get("score", 0),
                    "indicators": factor_data.get("indicators", [])
                })
        
        # Add school-specific weaknesses
        if school_data.get("teacher_student_ratio", 0) > 30:
            weaknesses.append({
                "factor": "teacher_student_ratio",
                "description": "High teacher-student ratio",
                "score": 0.4,
                "indicators": [f"Ratio: {school_data.get('teacher_student_ratio')}"]
            })
        
        if school_data.get("budget_per_student", 0) < 1000000:
            weaknesses.append({
                "factor": "budget",
                "description": "Low budget per student",
                "score": 0.5,
                "indicators": [f"Budget: Rp {school_data.get('budget_per_student')}"]
            })
        
        return weaknesses
    
    def _analyze_opportunities(self, school_data: Dict, context_analysis: Dict) -> List[Dict]:
        """Analyze school opportunities"""
        opportunities = []
        
        # Analyze context factors for opportunities
        context_factors = context_analysis.get("context_factors", {})
        
        for factor_name, factor_data in context_factors.items():
            score = factor_data.get("score", 0)
            if 0.5 <= score < 0.7:
                opportunities.append({
                    "factor": factor_name,
                    "description": f"Opportunity to improve {factor_name}",
                    "score": score,
                    "indicators": factor_data.get("indicators", [])
                })
        
        # Add external opportunities
        opportunities.append({
            "factor": "government_support",
            "description": "Government support for education improvement",
            "score": 0.7,
            "indicators": ["Kurikulum Merdeka support", "Funding programs"]
        })
        
        opportunities.append({
            "factor": "technology_integration",
            "description": "Opportunity for technology integration",
            "score": 0.6,
            "indicators": ["Digital learning platforms", "AI tools"]
        })
        
        return opportunities
    
    def _analyze_threats(self, school_data: Dict, context_analysis: Dict) -> List[Dict]:
        """Analyze school threats"""
        threats = []
        
        # Add external threats
        threats.append({
            "factor": "competition",
            "description": "Competition from other schools",
            "score": 0.5,
            "indicators": ["Nearby schools", "Private schools"]
        })
        
        threats.append({
            "factor": "policy_changes",
            "description": "Potential policy changes affecting education",
            "score": 0.6,
            "indicators": ["Curriculum changes", "Assessment changes"]
        })
        
        if school_data.get("enrollment_trend") == "declining":
            threats.append({
                "factor": "enrollment",
                "description": "Declining student enrollment",
                "score": 0.7,
                "indicators": ["Decreasing enrollment numbers"]
            })
        
        return threats
    
    def _generate_strategic_recommendations(self, swot_matrix: Dict) -> List[str]:
        """Generate strategic recommendations based on SWOT"""
        recommendations = []
        
        strengths = swot_matrix.get(SWOTCategory.STRENGTHS.value, [])
        weaknesses = swot_matrix.get(SWOTCategory.WEAKNESSES.value, [])
        opportunities = swot_matrix.get(SWOTCategory.OPPORTUNITIES.value, [])
        threats = swot_matrix.get(SWOTCategory.THREATS.value, [])
        
        # SO strategies: Leverage strengths to pursue opportunities
        if strengths and opportunities:
            recommendations.append(
                f"SO Strategy: Leverage strengths like {strengths[0]['factor']} to pursue opportunities like {opportunities[0]['factor']}"
            )
        
        # WO strategies: Address weaknesses to pursue opportunities
        if weaknesses and opportunities:
            recommendations.append(
                f"WO Strategy: Address weaknesses like {weaknesses[0]['factor']} to pursue opportunities like {opportunities[0]['factor']}"
            )
        
        # ST strategies: Use strengths to mitigate threats
        if strengths and threats:
            recommendations.append(
                f"ST Strategy: Use strengths like {strengths[0]['factor']} to mitigate threats like {threats[0]['factor']}"
            )
        
        # WT strategies: Minimize weaknesses and avoid threats
        if weaknesses and threats:
            recommendations.append(
                f"WT Strategy: Minimize weaknesses like {weaknesses[0]['factor']} and address threats like {threats[0]['factor']}"
            )
        
        return recommendations
    
    def _generate_priority_actions(self, swot_matrix: Dict) -> List[Dict]:
        """Generate priority actions based on SWOT"""
        actions = []
        
        weaknesses = swot_matrix.get(SWOTCategory.WEAKNESSES.value, [])
        threats = swot_matrix.get(SWOTCategory.THREATS.value, [])
        
        # Prioritize addressing high-impact weaknesses
        for weakness in weaknesses:
            if weakness.get("score", 0) < 0.4:
                actions.append({
                    "action": f"Address {weakness['factor']}",
                    "priority": "high",
                    "category": "weakness",
                    "description": weakness["description"]
                })
        
        # Prioritize mitigating high-impact threats
        for threat in threats:
            if threat.get("score", 0) > 0.6:
                actions.append({
                    "action": f"Mitigate {threat['factor']}",
                    "priority": "high",
                    "category": "threat",
                    "description": threat["description"]
                })
        
        # Add medium priority actions
        for weakness in weaknesses:
            if 0.4 <= weakness.get("score", 0) < 0.5:
                actions.append({
                    "action": f"Improve {weakness['factor']}",
                    "priority": "medium",
                    "category": "weakness",
                    "description": weakness["description"]
                })
        
        return actions
    
    def _initialize_swot_templates(self) -> Dict:
        """Initialize SWOT analysis templates"""
        return {
            "strengths": [
                "Strong leadership",
                "Experienced teachers",
                "Good facilities",
                "High student achievement",
                "Strong community support"
            ],
            "weaknesses": [
                "Limited budget",
                "High teacher-student ratio",
                "Outdated equipment",
                "Lack of technology integration",
                "Limited professional development"
            ],
            "opportunities": [
                "Government funding programs",
                "Technology integration",
                "Partnerships with industry",
                "Curriculum innovation",
                "Community engagement"
            ],
            "threats": [
                "Competition from other schools",
                "Policy changes",
                "Economic downturn",
                "Declining enrollment",
                "Staff turnover"
            ]
        }
