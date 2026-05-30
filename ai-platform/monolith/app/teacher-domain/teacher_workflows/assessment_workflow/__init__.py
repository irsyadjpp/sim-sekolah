"""
Assessment Workflow

This workflow guides teachers through creating assessments aligned with Kurikulum Merdeka
standards, including rubrics, performance tasks, and formative assessments.
"""

from typing import Dict, List, Optional
from datetime import datetime


class AssessmentWorkflow:
    """Assessment creation workflow orchestrator"""
    
    def __init__(self):
        self.workflow_steps = [
            "select_assessment_type",
            "define_assessment_context",
            "create_assessment_tasks",
            "generate_rubric",
            "align_with_standards",
            "review_and_finalize"
        ]
        
        self.current_step = "select_assessment_type"
        self.workflow_state = {}
    
    def get_workflow_definition(self) -> dict:
        """Get complete workflow definition"""
        return {
            "workflow_name": "Assessment Creation",
            "description": "Create assessments aligned with Kurikulum Merdeka standards",
            "estimated_time": "20 minutes",
            "steps": [
                {
                    "step_id": "select_assessment_type",
                    "name": "Select Assessment Type",
                    "description": "Choose formative, summative, performance, or project assessment",
                    "estimated_time": "2 minutes",
                    "required": True
                },
                {
                    "step_id": "define_assessment_context",
                    "name": "Define Assessment Context",
                    "description": "Specify grade, subject, learning objectives, and time allocation",
                    "estimated_time": "3 minutes",
                    "required": True
                },
                {
                    "step_id": "create_assessment_tasks",
                    "name": "Create Assessment Tasks",
                    "description": "Design assessment tasks and questions",
                    "estimated_time": "8 minutes",
                    "required": True
                },
                {
                    "step_id": "generate_rubric",
                    "name": "Generate Rubric",
                    "description": "Create or generate assessment rubric",
                    "estimated_time": "4 minutes",
                    "required": False
                },
                {
                    "step_id": "align_with_standards",
                    "name": "Align with Standards",
                    "description": "Ensure alignment with learning objectives and standards",
                    "estimated_time": "2 minutes",
                    "required": True
                },
                {
                    "step_id": "review_and_finalize",
                    "name": "Review and Finalize",
                    "description": "Review assessment and make final adjustments",
                    "estimated_time": "1 minute",
                    "required": True
                }
            ],
            "total_estimated_time": "20 minutes",
            "success_metrics": {
                "completion_rate_target": 80,
                "time_target_minutes": 20,
                "alignment_score_target": 90
            }
        }
    
    def start(self, context: Dict) -> Dict:
        """Start assessment creation workflow"""
        self.workflow_state = {
            "workflow_id": f"assessment_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "started_at": datetime.utcnow().isoformat(),
            "current_step": "select_assessment_type",
            "context": context,
            "progress": 0.0
        }
        
        return {
            "workflow_id": self.workflow_state["workflow_id"],
            "status": "started",
            "current_step": self.current_step,
            "next_step": self._get_next_step(),
            "available_types": self._get_assessment_types(),
            "estimated_completion_time": "20 minutes"
        }
    
    def _get_assessment_types(self) -> List[Dict]:
        """Get available assessment types"""
        return [
            {
                "type_id": "formative",
                "name": "Formative Assessment",
                "description": "Ongoing assessment to monitor learning progress",
                "time_frame": "During learning process"
            },
            {
                "type_id": "summative",
                "name": "Summative Assessment",
                "description": "End-of-unit assessment to evaluate learning outcomes",
                "time_frame": "End of unit/semester"
            },
            {
                "type_id": "performance",
                "name": "Performance Assessment",
                "description": "Assessment through practical application",
                "time_frame": "During learning process"
            },
            {
                "type_id": "project",
                "name": "Project-Based Assessment",
                "description": "Assessment through project completion",
                "time_frame": "Extended period"
            }
        ]
    
    def _get_next_step(self) -> Optional[str]:
        """Get next step in workflow"""
        current_index = self.workflow_steps.index(self.current_step)
        if current_index < len(self.workflow_steps) - 1:
            return self.workflow_steps[current_index + 1]
        return None