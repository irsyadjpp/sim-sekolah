"""
CP → ATP Workflow

This workflow helps teachers create Annual Teaching Plans (ATP) based on Curriculum Programs (CP),
ensuring alignment with Kurikulum Merdeka standards and optimal time allocation.
"""

from typing import Dict, List, Optional
from datetime import datetime


class CPATPWorkflow:
    """CP → ATP creation workflow orchestrator"""
    
    def __init__(self):
        self.workflow_steps = [
            "select_or_create_cp",
            "generate_atp_from_cp",
            "validate_time_allocation",
            "organize_topics",
            "add_assessment_plan",
            "review_and_optimize"
        ]
        
        self.current_step = "select_or_create_cp"
        self.workflow_state = {}
    
    def get_workflow_definition(self) -> dict:
        """Get complete workflow definition"""
        return {
            "workflow_name": "CP → ATP Creation",
            "description": "Create Annual Teaching Plans based on Curriculum Programs",
            "estimated_time": "15 minutes",
            "steps": [
                {
                    "step_id": "select_or_create_cp",
                    "name": "Select or Create CP",
                    "description": "Select existing CP or create new Curriculum Program",
                    "estimated_time": "3 minutes",
                    "required": True
                },
                {
                    "step_id": "generate_atp_from_cp",
                    "name": "Generate ATP from CP",
                    "description": "Automatically generate ATP structure from CP",
                    "estimated_time": "2 minutes",
                    "required": True
                },
                {
                    "step_id": "validate_time_allocation",
                    "name": "Validate Time Allocation",
                    "description": "Review and optimize time allocation per topic",
                    "estimated_time": "3 minutes",
                    "required": True
                },
                {
                    "step_id": "organize_topics",
                    "name": "Organize Topics",
                    "description": "Organize and sequence topics for the semester",
                    "estimated_time": "3 minutes",
                    "required": True
                },
                {
                    "step_id": "add_assessment_plan",
                    "name": "Add Assessment Plan",
                    "description": "Define assessment schedule and methods",
                    "estimated_time": "2 minutes",
                    "required": True
                },
                {
                    "step_id": "review_and_optimize",
                    "name": "Review and Optimize",
                    "description": "Review ATP and make final optimizations",
                    "estimated_time": "2 minutes",
                    "required": True
                }
            ],
            "total_estimated_time": "15 minutes",
            "success_metrics": {
                "completion_rate_target": 85,
                "time_target_minutes": 15,
                "alignment_score_target": 95
            }
        }
    
    def start(self, context: Dict) -> Dict:
        """Start CP → ATP workflow"""
        self.workflow_state = {
            "workflow_id": f"cp_atp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "started_at": datetime.utcnow().isoformat(),
            "current_step": "select_or_create_cp",
            "context": context,
            "progress": 0.0
        }
        
        return {
            "workflow_id": self.workflow_state["workflow_id"],
            "status": "started",
            "current_step": self.current_step,
            "next_step": self._get_next_step(),
            "available_cps": self._get_available_cps(context),
            "estimated_completion_time": "15 minutes"
        }
    
    def generate_atp_from_cp(self, cp_data: Dict, grade: str, semester: str) -> Dict:
        """Generate ATP structure from CP data"""
        atp_structure = {
            "atp_id": f"ATP_{cp_data.get('subject', 'unknown')}_{grade}_{semester}",
            "grade": grade,
            "semester": semester,
            "subject": cp_data.get("subject", "unknown"),
            "cp_id": cp_data.get("id", "unknown"),
            "learning_objectives": cp_data.get("learning_objectives", []),
            "topics": self._generate_topics_from_objectives(cp_data.get("learning_objectives", [])),
            "time_allocation": self._calculate_time_allocation(grade, semester),
            "assessment_plan": self._generate_assessment_plan(grade, semester),
            "alignment_score": 0.0
        }
        
        return atp_structure
    
    def validate_time_allocation(self, atp_data: Dict) -> Dict:
        """Validate time allocation in ATP"""
        validation_result = {
            "valid": True,
            "issues": [],
            "recommendations": []
        }
        
        time_alloc = atp_data.get("time_allocation", {})
        
        if "weekly_hours" not in time_alloc:
            validation_result["valid"] = False
            validation_result["issues"].append("Missing weekly hours allocation")
        
        if "semester_hours" not in time_alloc:
            validation_result["valid"] = False
            validation_result["issues"].append("Missing semester hours allocation")
        
        # Check total topic hours
        total_topic_hours = sum(topic.get("weeks", 0) * time_alloc.get("weekly_hours", 5) 
                              for topic in atp_data.get("topics", []))
        
        semester_hours = time_alloc.get("semester_hours", 100)
        
        if abs(total_topic_hours - semester_hours) > 10:
            validation_result["issues"].append(f"Topic hours ({total_topic_hours}) don't match semester hours ({semester_hours})")
            validation_result["recommendations"].append("Adjust topic weeks to match semester allocation")
        
        return validation_result
    
    def _get_available_cps(self, context: Dict) -> List[Dict]:
        """Get available CPs based on context"""
        subject = context.get("subject", "General")
        phase = context.get("phase", "A")
        
        return [
            {
                "cp_id": f"CP_{subject}_{phase}",
                "name": f"CP {subject} Fase {phase}",
                "phase": phase,
                "subject": subject,
                "learning_objectives_count": 5
            }
        ]
    
    def _generate_topics_from_objectives(self, objectives: List[str]) -> List[Dict]:
        """Generate topics from learning objectives"""
        topics = []
        
        # Group objectives into topics
        for i, objective in enumerate(objectives):
            topic_id = f"topic_{i+1}"
            topics.append({
                "topic_id": topic_id,
                "name": f"Topic {i+1}: {objective[:50]}...",
                "objectives": [objective],
                "weeks": 2,  # Default 2 weeks per topic
                "sequence": i + 1
            })
        
        return topics
    
    def _calculate_time_allocation(self, grade: str, semester: str) -> Dict:
        """Calculate time allocation based on grade and semester"""
        grade_hours = {
            "1": 4, "2": 4, "3": 5, "4": 5, "5": 6, "6": 6, "7": 7, "8": 7, "9": 8
        }
        
        weekly_hours = grade_hours.get(grade, 5)
        semester_hours = weekly_hours * 20  # 20 weeks per semester
        
        return {
            "weekly_hours": weekly_hours,
            "semester_hours": semester_hours,
            "per_topic_hours": weekly_hours * 2,
            "assessment_hours": semester_hours * 0.1,
            "project_hours": semester_hours * 0.15
        }
    
    def _generate_assessment_plan(self, grade: str, semester: str) -> List[Dict]:
        """Generate assessment plan for semester"""
        return [
            {
                "assessment_id": f"assessment_formative_1",
                "name": "Formative Assessment 1",
                "type": "formative",
                "week": 4,
                "weight": 0.2
            },
            {
                "assessment_id": f"assessment_mid",
                "name": "Mid-Semester Assessment",
                "type": "summative",
                "week": 10,
                "weight": 0.3
            },
            {
                "assessment_id": f"assessment_formative_2",
                "name": "Formative Assessment 2",
                "type": "formative",
                "week": 15,
                "weight": 0.2
            },
            {
                "assessment_id": f"assessment_final",
                "name": "Final Assessment",
                "type": "summative",
                "week": 20,
                "weight": 0.3
            }
        ]
    
    def _get_next_step(self) -> Optional[str]:
        """Get next step in workflow"""
        current_index = self.workflow_steps.index(self.current_step)
        if current_index < len(self.workflow_steps) - 1:
            return self.workflow_steps[current_index + 1]
        return None