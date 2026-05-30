"""
Assessment Domain - Bounded Context

This domain manages assessment generation, rubric creation, evaluation,
and student progress tracking capabilities.
"""

from .assessment_generation import AssessmentGeneration
from .rubric_creation import RubricCreation
from .evaluation import Evaluation
from .progress_tracking import ProgressTracking

__all__ = [
    "AssessmentDomain",
    "AssessmentGeneration",
    "RubricCreation",
    "Evaluation",
    "ProgressTracking"
]

class AssessmentDomain:
    """Main class for assessment domain operations"""
    
    def __init__(self):
        self.assessment_generation = AssessmentGeneration()
        self.rubric_creation = RubricCreation()
        self.evaluation = Evaluation()
        self.progress_tracking = ProgressTracking()
    
    def generate_assessment(self, context: dict) -> dict:
        """Generate assessment based on context"""
        return self.assessment_generation.generate(context)
    
    def create_rubric(self, learning_objectives: list, criteria: dict) -> dict:
        """Create assessment rubric"""
        return self.rubric_creation.create(learning_objectives, criteria)
    
    def evaluate_student_work(self, student_id: str, assessment_data: dict) -> dict:
        """Evaluate student work against criteria"""
        return self.evaluation.evaluate(student_id, assessment_data)
    
    def track_progress(self, student_id: str, assessment_results: list) -> dict:
        """Track student progress across assessments"""
        return self.progress_tracking.track(student_id, assessment_results)