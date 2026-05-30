"""
Student Domain - Bounded Context

This domain manages student learning experience, progress monitoring,
reflection, and self-regulation capabilities.
"""

from .learning_journal import LearningJournal
from .progress_monitoring import ProgressMonitoring
from .reflection_engine import ReflectionEngine
from .self_regulation import SelfRegulation

__all__ = [
    "StudentDomain",
    "LearningJournal",
    "ProgressMonitoring",
    "ReflectionEngine",
    "SelfRegulation"
]

class StudentDomain:
    """Main class for student domain operations"""
    
    def __init__(self):
        self.learning_journal = LearningJournal()
        self.progress_monitoring = ProgressMonitoring()
        self.reflection_engine = ReflectionEngine()
        self.self_regulation = SelfRegulation()
    
    def create_journal_entry(self, student_id: str, reflection_data: dict) -> dict:
        """Create learning journal entry"""
        return self.learning_journal.create_entry(student_id, reflection_data)
    
    def monitor_progress(self, student_id: str) -> dict:
        """Monitor student learning progress"""
        return self.progress_monitoring.monitor(student_id)
    
    def analyze_reflection(self, student_id: str, reflection: str) -> dict:
        """Analyze student reflection"""
        return self.reflection_engine.analyze(student_id, reflection)
    
    def assess_self_regulation(self, student_id: str) -> dict:
        """Assess student self-regulation competency"""
        return self.self_regulation.assess(student_id)