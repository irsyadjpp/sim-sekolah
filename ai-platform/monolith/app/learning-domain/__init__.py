"""
Learning Domain - Bounded Context

This domain manages adaptive learning, differentiated learning, mastery tracking,
and learning progression for personalized education.
"""

from .adaptive_learning import AdaptiveLearning
from .differentiated_learning import DifferentiatedLearning
from .mastery_tracking import MasteryTracking
from .progression import LearningProgression

__all__ = [
    "LearningDomain",
    "AdaptiveLearning",
    "DifferentiatedLearning",
    "MasteryTracking",
    "LearningProgression"
]

class LearningDomain:
    """Main class for learning domain operations"""
    
    def __init__(self):
        self.adaptive_learning = AdaptiveLearning()
        self.differentiated_learning = DifferentiatedLearning()
        self.mastery_tracking = MasteryTracking()
        self.progression = LearningProgression()
    
    def personalize_learning(self, student_id: str, context: dict) -> dict:
        """Personalize learning path for student"""
        return self.adaptive_learning.personalize(student_id, context)
    
    def differentiate_content(self, student_group: str, content: dict) -> dict:
        """Differentiate content for student group"""
        return self.differentiated_learning.differentiate(student_group, content)
    
    def track_mastery(self, student_id: str, competency: str) -> dict:
        """Track student mastery of competency"""
        return self.mastery_tracking.track(student_id, competency)
    
    def assess_progression(self, student_id: str) -> dict:
        """Assess learning progression over time"""
        return self.progression.assess(student_id)