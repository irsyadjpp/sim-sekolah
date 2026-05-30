"""
Character Assessment

This service provides comprehensive character assessment capabilities, assessing
student character development across Profil Pelajar Pancasila dimensions and other
character traits relevant to Pembelajaran Mendalam.
"""

from typing import Dict, List, Optional
from datetime import datetime


class CharacterAssessment:
    """Character assessment service for student character development"""
    
    def __init__(self):
        self.assessment_database = {}
        self.character_traits = self._initialize_character_traits()
        self.assessment_rubric = self._initialize_assessment_rubric()
    
    def assess(self, student_id: str, context: Dict) -> Dict:
        """Comprehensive character assessment for student"""
        assessment_id = f"char_assess_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Assess Profil Pelajar Pancasila dimensions
        ppp_assessment = self._assess_profil_pelajar_pancasila(student_id, context)
        
        # Assess other character traits
        trait_assessment = self._assess_character_traits(student_id, context)
        
        # Analyze character development trajectory
        trajectory_analysis = self._analyze_development_trajectory(student_id)
        
        # Identify character strengths
        strengths = self._identify_character_strengths(ppp_assessment, trait_assessment)
        
        # Identify areas for development
        areas_for_development = self._identify_development_areas(ppp_assessment, trait_assessment)
        
        # Generate development recommendations
        recommendations = self._generate_development_recommendations(
            student_id, 
            strengths, 
            areas_for_development
        )
        
        assessment_result = {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "context": context,
            "profil_pelajar_pancasila_assessment": ppp_assessment,
            "character_traits_assessment": trait_assessment,
            "trajectory_analysis": trajectory_analysis,
            "character_strengths": strengths,
            "areas_for_development": areas_for_development,
            "recommendations": recommendations,
            "assessed_at": datetime.utcnow().isoformat()
        }
        
        self.assessment_database[assessment_id] = assessment_result
        
        return assessment_result
    
    def recommend_development(self, student_id: str) -> Dict:
        """Recommend character development activities based on assessment"""
        # Get latest assessment
        latest_assessment = self._get_latest_assessment(student_id)
        
        if not latest_assessment:
            return {
                "student_id": student_id,
                "error": "No assessment found. Please conduct character assessment first."
            }
        
        areas_for_development = latest_assessment.get("areas_for_development", [])
        
        recommendations = []
        
        for area in areas_for_development:
            dimension_code = area.get("dimension_code")
            dimension_name = area.get("dimension_name")
            
            if dimension_code:
                activities = self._generate_development_activities(dimension_code)
                recommendations.append({
                    "dimension_code": dimension_code,
                    "dimension_name": dimension_name,
                    "priority": area.get("priority", "medium"),
                    "activities": activities
                })
        
        return {
            "student_id": student_id,
            "assessment_id": latest_assessment.get("assessment_id"),
            "development_recommendations": recommendations,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def track_assessment_progress(self, student_id: str) -> Dict:
        """Track character assessment progress over time"""
        student_assessments = [
            assess for assess in self.assessment_database.values()
            if assess.get("student_id") == student_id
        ]
        
        if not student_assessments:
            return {
                "student_id": student_id,
                "error": "No assessments found for student"
            }
        
        # Sort by assessment date
        student_assessments.sort(key=lambda x: x.get("assessed_at", ""))
        
        # Track progress across dimensions
        progress_data = self._calculate_assessment_progress(student_assessments)
        
        return {
            "student_id": student_id,
            "total_assessments": len(student_assessments),
            "first_assessment": student_assessments[0].get("assessed_at"),
            "latest_assessment": student_assessments[-1].get("assessed_at"),
            "progress_data": progress_data,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _assess_profil_pelajar_pancasila(self, student_id: str, context: Dict) -> Dict:
        """Assess Profil Pelajar Pancasila dimensions"""
        dimensions = ["beriman", "berkebinekaan", "gotong_royong", "mandiri", "bernah_kritar", "kreatif"]
        
        dimension_scores = {}
        
        for dimension in dimensions:
            # In real implementation, this would assess from actual student data
            dimension_scores[dimension] = {
                "dimension_code": dimension,
                "mastery_level": "developing",
                "score": 0.65,
                "indicators_assessed": [],
                "strengths": [],
                "areas_for_improvement": []
            }
        
        overall_score = self._calculate_ppp_overall_score(dimension_scores)
        
        return {
            "dimensions": dimension_scores,
            "overall_score": overall_score,
            "strongest_dimension": "mandiri",
            "weakest_dimension": "beriman"
        }
    
    def _assess_character_traits(self, student_id: str, context: Dict) -> Dict:
        """Assess other character traits beyond Profil Pelajar Pancasila"""
        trait_scores = {}
        
        for trait_code, trait_info in self.character_traits.items():
            trait_scores[trait_code] = {
                "trait_name": trait_info["name"],
                "description": trait_info["description"],
                "mastery_level": "developing",
                "score": 0.65,
                "indicators": []
            }
        
        return {
            "traits": trait_scores,
            "overall_score": 0.68
        }
    
    def _analyze_development_trajectory(self, student_id: str) -> Dict:
        """Analyze character development trajectory over time"""
        # Placeholder - would analyze historical data
        return {
            "trajectory": "improving",
            "growth_rate": 0.15,
            "predicted_development": "on_track",
            "key_inflection_points": []
        }
    
    def _identify_character_strengths(self, ppp_assessment: Dict, trait_assessment: Dict) -> List[Dict]:
        """Identify character strengths from assessments"""
        strengths = []
        
        # From Profil Pelajar Pancasila
        ppp_dimensions = ppp_assessment.get("dimensions", {})
        
        for dimension_code, dimension_data in ppp_dimensions.items():
            if dimension_data.get("score", 0) >= 0.75:
                strengths.append({
                    "type": "profil_pelajar_pancasila",
                    "code": dimension_code,
                    "score": dimension_data.get("score"),
                    "mastery_level": dimension_data.get("mastery_level")
                })
        
        # From character traits
        traits = trait_assessment.get("traits", {})
        
        for trait_code, trait_data in traits.items():
            if trait_data.get("score", 0) >= 0.75:
                strengths.append({
                    "type": "character_trait",
                    "code": trait_code,
                    "name": trait_data.get("trait_name"),
                    "score": trait_data.get("score")
                })
        
        return strengths
    
    def _identify_development_areas(self, ppp_assessment: Dict, trait_assessment: Dict) -> List[Dict]:
        """Identify areas requiring development"""
        areas = []
        
        # From Profil Pelajar Pancasila
        ppp_dimensions = ppp_assessment.get("dimensions", {})
        
        for dimension_code, dimension_data in ppp_dimensions.items():
            if dimension_data.get("score", 0) < 0.70:
                areas.append({
                    "type": "profil_pelajar_pancasila",
                    "code": dimension_code,
                    "current_score": dimension_data.get("score"),
                    "target_score": 0.80,
                    "priority": "high" if dimension_data.get("score", 0) < 0.60 else "medium"
                })
        
        # From character traits
        traits = trait_assessment.get("traits", {})
        
        for trait_code, trait_data in traits.items():
            if trait_data.get("score", 0) < 0.70:
                areas.append({
                    "type": "character_trait",
                    "code": trait_code,
                    "name": trait_data.get("trait_name"),
                    "current_score": trait_data.get("score"),
                    "target_score": 0.80,
                    "priority": "medium"
                })
        
        return areas
    
    def _generate_development_recommendations(self, student_id: str, strengths: List[Dict], areas: List[Dict]) -> List[Dict]:
        """Generate character development recommendations"""
        recommendations = []
        
        # Recommendations based on strengths (to leverage them)
        for strength in strengths[:2]:  # Top 2 strengths
            recommendations.append({
                "type": "leverage_strength",
                "focus": strength,
                "recommendation": f"Use {strength.get('code', 'this strength')} to support development in other areas"
            })
        
        # Recommendations based on development areas
        for area in areas[:3]:  # Top 3 areas
            recommendations.append({
                "type": "address_weakness",
                "focus": area,
                "recommendation": f"Focus on developing {area.get('code', 'this area')} through targeted activities"
            })
        
        return recommendations
    
    def _generate_development_activities(self, dimension_code: str) -> List[Dict]:
        """Generate development activities for specific dimension"""
        # Placeholder activities - would be more comprehensive in real implementation
        return [
            {
                "activity_id": f"dev_{dimension_code}_1",
                "name": f"Reflection activity for {dimension_code}",
                "description": "Individual reflection exercise",
                "duration_minutes": 15,
                "context": "individual"
            },
            {
                "activity_id": f"dev_{dimension_code}_2",
                "name": f"Collaborative activity for {dimension_code}",
                "description": "Group work to practice the dimension",
                "duration_minutes": 30,
                "context": "group"
            }
        ]
    
    def _get_latest_assessment(self, student_id: str) -> Optional[Dict]:
        """Get the latest assessment for student"""
        student_assessments = [
            assess for assess in self.assessment_database.values()
            if assess.get("student_id") == student_id
        ]
        
        if not student_assessments:
            return None
        
        # Sort by assessment date and return latest
        student_assessments.sort(key=lambda x: x.get("assessed_at", ""))
        return student_assessments[-1]
    
    def _calculate_assessment_progress(self, assessments: List[Dict]) -> Dict:
        """Calculate progress across assessments"""
        # Placeholder - would analyze actual progress
        return {
            "overall_improvement": 0.10,
            "dimension_progress": {},
            "trait_progress": {}
        }
    
    def _calculate_ppp_overall_score(self, dimension_scores: Dict) -> float:
        """Calculate overall Profil Pelajar Pancasila score"""
        if not dimension_scores:
            return 0.0
        
        total_score = sum(
            dim_data.get("score", 0) 
            for dim_data in dimension_scores.values()
        )
        
        return total_score / len(dimension_scores)
    
    def _initialize_character_traits(self) -> Dict:
        """Initialize character traits beyond Profil Pelajar Pancasila"""
        return {
            "resilience": {
                "code": "resilience",
                "name": "Resilience",
                "description": "Ability to bounce back from challenges"
            },
            "empathy": {
                "code": "empathy",
                "name": "Empathy",
                "description": "Understanding and sharing others' feelings"
            },
            "self_control": {
                "code": "self_control",
                "name": "Self-Control",
                "description": "Ability to regulate emotions and behaviors"
            },
            "gratitude": {
                "code": "gratitude",
                "name": "Gratitude",
                "description": "Appreciation of positive aspects of life"
            },
            "curiosity": {
                "code": "curiosity",
                "name": "Curiosity",
                "description": "Desire to learn and explore"
            }
        }
    
    def _initialize_assessment_rubric(self) -> Dict:
        """Initialize assessment rubric for character assessment"""
        return {
            "mastery_levels": {
                "emerging": {"range": [0.0, 0.40], "description": "Just beginning to develop"},
                "developing": {"range": [0.40, 0.70], "description": "Making progress but needs support"},
                "proficient": {"range": [0.70, 0.90], "description": "Demonstrates consistently"},
                "exemplary": {"range": [0.90, 1.0], "description": "Exceeds expectations consistently"}
            }
        }