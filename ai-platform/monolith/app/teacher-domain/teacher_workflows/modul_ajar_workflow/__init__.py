"""
Modul Ajar Creation Workflow

This workflow guides teachers through the complete process of creating teaching modules
aligned with Kurikulum Merdeka standards and Pembelajaran Mendalam principles.
"""

from typing import Dict, List, Optional
from datetime import datetime


class ModulAjarWorkflow:
    """Modul Ajar creation workflow orchestrator"""
    
    def __init__(self):
        self.workflow_steps = [
            "select_template",
            "select_grade_subject",
            "define_learning_objectives", 
            "design_activities",
            "integrate_reflection",
            "plan_assessment",
            "align_with_standards",
            "review_and_finalize"
        ]
        
        self.current_step = "select_template"
        self.workflow_state = {}
    
    def get_workflow_definition(self) -> dict:
        """Get complete workflow definition"""
        return {
            "workflow_name": "Modul Ajar Creation",
            "description": "Create teaching modules aligned with Kurikulum Merdeka standards",
            "estimated_time": "30 minutes",
            "steps": [
                {
                    "step_id": "select_template",
                    "name": "Select Template",
                    "description": "Choose Modul Ajar template for subject and grade",
                    "estimated_time": "2 minutes",
                    "required": True
                },
                {
                    "step_id": "select_grade_subject",
                    "name": "Select Grade and Subject",
                    "description": "Specify target grade and subject",
                    "estimated_time": "1 minute",
                    "required": True
                },
                {
                    "step_id": "define_learning_objectives",
                    "name": "Define Learning Objectives",
                    "description": "Select or create learning objectives aligned with CP",
                    "estimated_time": "8 minutes",
                    "required": True
                },
                {
                    "step_id": "design_activities",
                    "name": "Design Learning Activities",
                    "description": "Create engaging learning activities with inquiry and collaboration",
                    "estimated_time": "10 minutes",
                    "required": True
                },
                {
                    "step_id": "integrate_reflection",
                    "name": "Integrate Reflection Components",
                    "description": "Add reflection prompts and self-assessment",
                    "estimated_time": "3 minutes",
                    "required": False  # Recommended but optional
                },
                {
                    "step_id": "plan_assessment",
                    "name": "Plan Assessment",
                    "description": "Design formative and summative assessments",
                    "estimated_time": "3 minutes",
                    "required": True
                },
                {
                    "step_id": "align_with_standards",
                    "name": "Align with Standards",
                    "description": "Ensure alignment with Kurikulum Merdeka and Profil Pelajar Pancasila",
                    "estimated_time": "2 minutes",
                    "required": True
                },
                {
                    "step_id": "review_and_finalize",
                    "name": "Review and Finalize",
                    "description": "Review Modul Ajar and make final adjustments",
                    "estimated_time": "1 minute",
                    "required": True
                }
            ],
            "total_estimated_time": "30 minutes",
            "success_metrics": {
                "completion_rate_target": 80,
                "time_target_minutes": 30,
                "satisfaction_target": 85
            }
        }
    
    def start(self, context: Dict) -> Dict:
        """Start Modul Ajar creation workflow"""
        self.workflow_state = {
            "workflow_id": f"modul_ajar_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "started_at": datetime.utcnow().isoformat(),
            "current_step": "select_template",
            "context": context,
            "progress": 0.0
        }
        
        return {
            "workflow_id": self.workflow_state["workflow_id"],
            "status": "started",
            "current_step": self.current_step,
            "next_step": self._get_next_step(),
            "available_templates": self._get_available_templates(context),
            "estimated_completion_time": "30 minutes"
        }
    
    def proceed_to_next_step(self, step_data: Dict) -> Dict:
        """Proceed to next workflow step with data"""
        if not self.workflow_state:
            return {"error": "Workflow not started"}
        
        self.current_step = self._get_next_step()
        
        # Validate step data
        validation_result = self._validate_step_data(self.current_step, step_data)
        if not validation_result["valid"]:
            return {
                "error": "Step data validation failed",
                "validation_errors": validation_result["errors"]
            }
        
        # Update workflow state
        self.workflow_state[self.current_step] = step_data
        self.workflow_state["current_step"] = self.current_step
        self.workflow_state["progress"] = self._calculate_progress()
        
        return {
            "workflow_id": self.workflow_state["workflow_id"],
            "current_step": self.current_step,
            "progress": self.workflow_state["progress"],
            "next_step": self._get_next_step(),
            "recommendations": self._get_step_recommendations(self.current_step)
        }
    
    def complete_workflow(self) -> Dict:
        """Complete workflow and generate final Modul Ajar"""
        final_modul_ajar = self._generate_final_modul_ajar()
        
        self.workflow_state["completed_at"] = datetime.utcnow().isoformat()
        self.workflow_state["status"] = "completed"
        self.workflow_state["final_modul_ajar"] = final_modul_ajar
        
        return {
            "workflow_id": self.workflow_state["workflow_id"],
            "status": "completed",
            "modul_ajar": final_modul_ajar,
            "completion_time": self._calculate_completion_time(),
            "success": True
        }
    
    def _get_next_step(self) -> Optional[str]:
        """Get next step in workflow"""
        current_index = self.workflow_steps.index(self.current_step)
        if current_index < len(self.workflow_steps) - 1:
            return self.workflow_steps[current_index + 1]
        return None  # Workflow complete
    
    def _get_available_templates(self, context: Dict) -> List[Dict]:
        """Get available Modul Ajar templates based on context"""
        subject = context.get("subject", "General")
        grade = context.get("grade", "General")
        
        return [
            {
                "template_id": f"{subject}_{grade}_basic",
                "name": f"Basic {subject} Template - Grade {grade}",
                "description": "Standard template with essential sections",
                "sections": ["introduction", "learning_objectives", "activities", "assessment", "reflection"]
            },
            {
                "template_id": f"{subject}_{grade}_inquiry",
                "name": f"Inquiry-Based {subject} Template - Grade {grade}",
                "description": "Template emphasizing inquiry and exploration",
                "sections": ["introduction", "learning_objectives", "inquiry_activities", "assessment", "reflection"]
            },
            {
                "template_id": f"{subject}_{grade}_project",
                "name": f"Project-Based {subject} Template - Grade {grade}",
                "description": "Template for project-based learning",
                "sections": ["project_overview", "learning_objectives", "project_phases", "assessment", "reflection"]
            }
        ]
    
    def _validate_step_data(self, step: str, data: Dict) -> Dict:
        """Validate data for specific step"""
        validation_result = {"valid": True, "errors": []}
        
        if step == "define_learning_objectives":
            if "learning_objectives" not in data or len(data["learning_objectives"]) < 3:
                validation_result["valid"] = False
                validation_result["errors"].append("At least 3 learning objectives required")
        
        elif step == "design_activities":
            if "activities" not in data or len(data["activities"]) < 2:
                validation_result["valid"] = False
                validation_result["errors"].append("At least 2 activities required")
        
        elif step == "plan_assessment":
            if "assessment" not in data or len(data["assessment"]) < 1:
                validation_result["valid"] = False
                validation_result["errors"].append("Assessment plan required")
        
        return validation_result
    
    def _get_step_recommendations(self, step: str) -> List[str]:
        """Get recommendations for specific step"""
        recommendations = {
            "design_activities": [
                "Include inquiry-based activities to promote critical thinking",
                "Add collaborative activities to develop social skills",
                "Ensure activities cater to different learning styles"
            ],
            "integrate_reflection": [
                "Add reflection prompts before, during, and after learning",
                "Include self-assessment opportunities",
                "Connect reflection to Profil Pelajar Pancasila dimensions"
            ],
            "plan_assessment": [
                "Include both formative and summative assessments",
                "Add peer assessment opportunities",
                "Align assessment criteria with learning objectives"
            ]
        }
        
        return recommendations.get(step, [])
    
    def _calculate_progress(self) -> float:
        """Calculate workflow progress percentage"""
        completed_steps = sum(1 for step in self.workflow_steps if step in self.workflow_state)
        return (completed_steps / len(self.workflow_steps)) * 100
    
    def _calculate_completion_time(self) -> str:
        """Calculate actual completion time"""
        if "started_at" in self.workflow_state and "completed_at" in self.workflow_state:
            start = datetime.fromisoformat(self.workflow_state["started_at"])
            end = datetime.fromisoformat(self.workflow_state["completed_at"])
            duration = end - start
            return str(duration)
        return "Unknown"
    
    def _generate_final_modul_ajar(self) -> Dict:
        """Generate final Modul Ajar from workflow state"""
        return {
            "modul_ajar_id": self.workflow_state["workflow_id"],
            "template": self.workflow_state.get("select_template", {}),
            "grade_subject": self.workflow_state.get("select_grade_subject", {}),
            "learning_objectives": self.workflow_state.get("define_learning_objectives", []),
            "activities": self.workflow_state.get("design_activities", []),
            "reflection": self.workflow_state.get("integrate_reflection", {}),
            "assessment": self.workflow_state.get("plan_assessment", {}),
            "alignment": self.workflow_state.get("align_with_standards", {}),
            "created_at": datetime.utcnow().isoformat(),
            "alignment_score": self._calculate_alignment_score()
        }
    
    def _calculate_alignment_score(self) -> float:
        """Calculate alignment score with Kurikulum Merdeka standards"""
        # Placeholder for actual alignment calculation
        return 0.85