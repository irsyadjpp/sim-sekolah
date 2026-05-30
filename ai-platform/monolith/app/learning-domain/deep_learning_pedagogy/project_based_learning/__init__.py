"""
Project-Based Learning Module

This module provides P5 (Profil Pelajar Pancasila) project orchestration and management,
aligned with Kurikulum Merdeka's emphasis on project-based learning and character development.
"""

from typing import Dict, List, Optional
from datetime import datetime


class ProjectBasedLearning:
    """Project-based learning orchestrator for P5 and collaborative learning"""
    
    def __init__(self):
        self.project_database = {}
        self.collaboration_analytics = {}
    
    def orchestrate(self, project_data: Dict) -> Dict:
        """Orchestrate project-based learning project"""
        project_id = f"project_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        project = {
            "project_id": project_id,
            "name": project_data.get("name", "Untitled Project"),
            "description": project_data.get("description", ""),
            "profil_pelajar_dimensions": project_data.get("profil_pelajar_dimensions", []),
            "subject": project_data.get("subject", ""),
            "grade": project_data.get("grade", ""),
            "phases": self._generate_project_phases(project_data),
            "collaboration_groups": self._generate_collaboration_groups(project_data),
            "assessment_criteria": self._generate_assessment_criteria(project_data),
            "timeline": self._generate_timeline(project_data),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.project_database[project_id] = project
        
        return {
            "project_id": project_id,
            "status": "initialized",
            "phases": project["phases"],
            "collaboration_groups": project["collaboration_groups"],
            "timeline": project["timeline"]
        }
    
    def assess_collaboration(self, project_id: str, student_data: Dict) -> Dict:
        """Assess student collaboration quality"""
        project = self.project_database.get(project_id)
        if not project:
            return {"error": "Project not found"}
        
        collaboration_data = student_data.get("collaboration", {})
        
        assessment = {
            "communication_score": self._assess_communication(collaboration_data),
            "cooperation_score": self._assess_cooperation(collaboration_data),
            "contribution_score": self._assess_contribution(collaboration_data),
            "collaboration_quality": self._determine_collaboration_quality(collaboration_data),
            "profil_pelajar_alignment": self._check_profil_pelajar_alignment(project, student_data)
        }
        
        return assessment
    
    def evaluate_outcome(self, project_id: str, student_work: Dict) -> Dict:
        """Evaluate project outcome and student achievement"""
        project = self.project_database.get(project_id)
        if not project:
            return {"error": "Project not found"}
        
        evaluation = {
            "project_id": project_id,
            "achievement_level": self._assess_achievement(student_work),
            "competency_mastery": self._assess_competency_mastery(student_work, project),
            "character_development": self._assess_character_development(student_work, project),
            "reflection_quality": self._assess_project_reflection(student_work),
            "overall_score": self._calculate_project_score(student_work, project)
        }
        
        return evaluation
    
    def _generate_project_phases(self, project_data: Dict) -> List[Dict]:
        """Generate project phases"""
        return [
            {
                "phase_id": "exploration",
                "name": "Exploration Phase",
                "description": "Explore project topic and identify questions",
                "duration_weeks": 1,
                "activities": ["research", "question_formulation", "planning"]
            },
            {
                "phase_id": "development",
                "name": "Development Phase",
                "description": "Develop project solution or product",
                "duration_weeks": 2,
                "activities": ["design", "implementation", "testing"]
            },
            {
                "phase_id": "presentation",
                "name": "Presentation Phase",
                "description": "Present project and receive feedback",
                "duration_weeks": 1,
                "activities": ["preparation", "presentation", "reflection"]
            }
        ]
    
    def _generate_collaboration_groups(self, project_data: Dict) -> List[Dict]:
        """Generate collaboration groups"""
        group_size = project_data.get("group_size", 4)
        total_students = project_data.get("total_students", 20)
        
        groups = []
        for i in range(0, total_students, group_size):
            groups.append({
                "group_id": f"group_{i+1}",
                "members": range(i, min(i + group_size, total_students)),
                "role_assignments": self._assign_roles(group_size)
            })
        
        return groups
    
    def _generate_assessment_criteria(self, project_data: Dict) -> Dict:
        """Generate assessment criteria"""
        return {
            "collaboration_criteria": [
                "Active participation in group discussions",
                "Contribution to group work",
                "Communication with team members",
                "Conflict resolution"
            ],
            "product_criteria": [
                "Quality of final product",
                "Innovation and creativity",
                "Alignment with project goals",
                "Technical proficiency"
            ],
            "reflection_criteria": [
                "Learning reflection",
                "Process documentation",
                "Self-assessment",
                "Peer assessment"
            ],
            "profil_pelajar_criteria": self._get_profil_pelajar_criteria(project_data.get("profil_pelajar_dimensions", []))
        }
    
    def _generate_timeline(self, project_data: Dict) -> Dict:
        """Generate project timeline"""
        return {
            "total_weeks": project_data.get("duration_weeks", 4),
            "start_date": project_data.get("start_date"),
            "milestone_dates": [
                {"milestone": "exploration_complete", "week": 1},
                {"milestone": "development_complete", "week": 3},
                {"milestone": "presentation_complete", "week": 4}
            ]
        }
    
    def _assign_roles(self, group_size: int) -> List[str]:
        """Assign roles to group members"""
        roles = ["leader", "researcher", "designer", "presenter", "evaluator", "documenter"]
        return roles[:group_size]
    
    def _assess_communication(self, collaboration_data: Dict) -> float:
        """Assess communication quality (0.0 to 1.0)"""
        communication_quality = collaboration_data.get("communication_quality", "medium")
        quality_scores = {"low": 0.3, "medium": 0.6, "high": 0.9}
        return quality_scores.get(communication_quality, 0.5)
    
    def _assess_cooperation(self, collaboration_data: Dict) -> float:
        """Assess cooperation quality (0.0 to 1.0)"""
        cooperation_quality = collaboration_data.get("cooperation_quality", "medium")
        quality_scores = {"low": 0.3, "medium": 0.6, "high": 0.9}
        return quality_scores.get(cooperation_quality, 0.5)
    
    def _assess_contribution(self, collaboration_data: Dict) -> float:
        """Assess contribution level (0.0 to 1.0)"""
        contribution_level = collaboration_data.get("contribution_level", "medium")
        quality_scores = {"low": 0.3, "medium": 0.6, "high": 0.9}
        return quality_scores.get(contribution_level, 0.5)
    
    def _determine_collaboration_quality(self, collaboration_data: Dict) -> str:
        """Determine overall collaboration quality"""
        comm_score = self._assess_communication(collaboration_data)
        coop_score = self._assess_cooperation(collaboration_data)
        contrib_score = self._assess_contribution(collaboration_data)
        
        overall_score = (comm_score + coop_score + contrib_score) / 3
        
        if overall_score >= 0.8:
            return "excellent"
        elif overall_score >= 0.6:
            return "good"
        elif overall_score >= 0.4:
            return "satisfactory"
        else:
            return "needs_improvement"
    
    def _check_profil_pelajar_alignment(self, project: Dict, student_data: Dict) -> Dict:
        """Check alignment with Profil Pelajar Pancasila"""
        project_dimensions = project.get("profil_pelajar_dimensions", [])
        student_development = student_data.get("character_development", {})
        
        alignment = {}
        for dimension in project_dimensions:
            if dimension in student_development:
                alignment[dimension] = student_development[dimension].get("level", "developing")
            else:
                alignment[dimension] = "not_assessed"
        
        return alignment
    
    def _assess_achievement(self, student_work: Dict) -> str:
        """Assess achievement level"""
        quality_score = student_work.get("quality_score", 0.5)
        innovation_score = student_work.get("innovation_score", 0.5)
        overall_score = (quality_score + innovation_score) / 2
        
        if overall_score >= 0.8:
            return "excellent"
        elif overall_score >= 0.6:
            return "proficient"
        elif overall_score >= 0.4:
            return "developing"
        else:
            return "emerging"
    
    def _assess_competency_mastery(self, student_work: Dict, project: Dict) -> Dict:
        """Assess competency mastery"""
        return {
            "competency_coverage": 0.75,  # Placeholder
            "mastery_levels": {"proficient": 0.6, "developing": 0.3, "emerging": 0.1}
        }
    
    def _assess_character_development(self, student_work: Dict, project: Dict) -> Dict:
        """Assess character development"""
        return {
            "gotong_royong": "developing",
            "kreatif": "proficient",
            "bernal_kritis": "developing"
        }
    
    def _assess_project_reflection(self, student_work: Dict) -> str:
        """Assess quality of project reflection"""
        reflection_quality = student_work.get("reflection_quality", "medium")
        return reflection_quality
    
    def _calculate_project_score(self, student_work: Dict, project: Dict) -> float:
        """Calculate overall project score"""
        return student_work.get("overall_score", 0.75)
    
    def _get_profil_pelajar_criteria(self, dimensions: List[str]) -> Dict:
        """Get Profil Pelajar Pancasila assessment criteria"""
        criteria = {}
        for dimension in dimensions:
            criteria[dimension] = ["alignment", "development", "reflection"]
        return criteria
    
    def get_skills_level(self, student_id: str) -> str:
        """Get project-based learning skills level for student"""
        return "proficient"