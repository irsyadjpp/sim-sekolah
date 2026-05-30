"""
Teacher Workflows Module

This module contains all teacher workflows that guide teachers through their core tasks:
- Modul Ajar creation workflow
- CP → ATP workflow  
- Assessment workflow
- Remediation workflow
"""

from .modul_ajar_workflow import ModulAjarWorkflow
from .cp_atp_workflow import CPATPWorkflow
from .assessment_workflow import AssessmentWorkflow
from .remediation_workflow import RemediationWorkflow

__all__ = [
    "TeacherWorkflows",
    "ModulAjarWorkflow",
    "CPATPWorkflow", 
    "AssessmentWorkflow",
    "RemediationWorkflow"
]

class TeacherWorkflows:
    """Main orchestrator for all teacher workflows"""
    
    def __init__(self):
        self.modul_ajar_workflow = ModulAjarWorkflow()
        self.cp_atp_workflow = CPATPWorkflow()
        self.assessment_workflow = AssessmentWorkflow()
        self.remediation_workflow = RemediationWorkflow()
    
    def get_modul_ajar_workflow(self) -> dict:
        """Get Modul Ajar creation workflow definition"""
        return self.modul_ajar_workflow.get_workflow_definition()
    
    def get_cp_atp_workflow(self) -> dict:
        """Get CP → ATP workflow definition"""
        return self.cp_atp_workflow.get_workflow_definition()
    
    def get_assessment_workflow(self) -> dict:
        """Get assessment workflow definition"""
        return self.assessment_workflow.get_workflow_definition()
    
    def get_remediation_workflow(self) -> dict:
        """Get remediation workflow definition"""
        return self.remediation_workflow.get_workflow_definition()
    
    def start_workflow(self, workflow_type: str, context: dict) -> dict:
        """Start a specific workflow with context"""
        if workflow_type == "modul_ajar":
            return self.modul_ajar_workflow.start(context)
        elif workflow_type == "cp_atp":
            return self.cp_atp_workflow.start(context)
        elif workflow_type == "assessment":
            return self.assessment_workflow.start(context)
        elif workflow_type == "remediation":
            return self.remediation_workflow.start(context)
        else:
            return {"error": f"Unknown workflow type: {workflow_type}"}