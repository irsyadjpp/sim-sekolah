"""
AI Agents Module

This module provides specialized AI agents for different domains:
- Teacher agent for teacher workflow assistance
- Student agent for student learning support
- Curriculum agent for curriculum planning
- Assessment agent for assessment generation and evaluation
"""

from .teacher_agent import TeacherAgent
from .student_agent import StudentAgent
from .curriculum_agent import CurriculumAgent
from .assessment_agent import AssessmentAgent

__all__ = [
    "AgentManager",
    "TeacherAgent",
    "StudentAgent", 
    "CurriculumAgent",
    "AssessmentAgent"
]

class AgentManager:
    """Main orchestrator for all AI agents"""
    
    def __init__(self):
        self.teacher_agent = TeacherAgent()
        self.student_agent = StudentAgent()
        self.curriculum_agent = CurriculumAgent()
        self.assessment_agent = AssessmentAgent()
    
    def get_agent(self, agent_type: str):
        """Get specific agent by type"""
        agents = {
            "teacher": self.teacher_agent,
            "student": self.student_agent,
            "curriculum": self.curriculum_agent,
            "assessment": self.assessment_agent
        }
        return agents.get(agent_type)
    
    def coordinate_agents(self, task: str, context: dict):
        """Coordinate multiple agents for complex tasks"""
        result = {
            "task": task,
            "context": context,
            "agent_results": []
        }
        
        if task == "create_modul_ajar":
            result["agent_results"].append(self.curriculum_agent.generate_modul_ajar(context))
            result["agent_results"].append(self.teacher_agent.assist_planning(context))
        elif task == "student_assessment":
            result["agent_results"].append(self.student_agent.assess_progress(context))
            result["agent_results"].append(self.assessment_agent.evaluate_student(context))
        
        return result