"""
Teacher Domain - Primary User Bounded Context

This domain focuses on teacher workflows, which is critical for platform adoption.
Teachers are the primary users, and their workflows should drive the architecture design.
"""

from .teacher_workflows import TeacherWorkflows
from .planning_assistant import PlanningAssistant
from .resource_recommendation import ResourceRecommendation

__all__ = [
    "TeacherDomain",
    "TeacherWorkflows",
    "PlanningAssistant", 
    "ResourceRecommendation"
]

class TeacherDomain:
    """Main class for teacher domain operations"""
    
    def __init__(self):
        self.workflows = TeacherWorkflows()
        self.planning_assistant = PlanningAssistant()
        self.resource_recommendation = ResourceRecommendation()
    
    def get_modul_ajar_workflow(self) -> dict:
        """Get Modul Ajar creation workflow"""
        return self.workflows.get_modul_ajar_workflow()
    
    def get_cp_atp_workflow(self) -> dict:
        """Get CP → ATP workflow"""
        return self.workflows.get_cp_atp_workflow()
    
    def get_assessment_workflow(self) -> dict:
        """Get assessment workflow"""
        return self.workflows.get_assessment_workflow()
    
    def get_remediation_workflow(self) -> dict:
        """Get remediation workflow"""
        return self.workflows.get_remediation_workflow()
    
    def assist_planning(self, planning_data: dict) -> dict:
        """Assist teacher with lesson planning"""
        return self.planning_assistant.assist(planning_data)
    
    def recommend_resources(self, context: dict) -> dict:
        """Recommend resources for specific context"""
        return self.resource_recommendation.recommend(context)