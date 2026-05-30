"""
ATP (Annual Teaching Plan) Standards for Kurikulum Merdeka

ATP standards define the structure and requirements for Annual Teaching Plans
derived from CP for each grade, semester, and subject.
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class Semester(Enum):
    """Semesters in Indonesian education system"""
    GANJIL = "ganjil"
    GENAP = "genap"


@dataclass
class ATPStructure:
    """ATP Structure according to Kurikulum Merdeka standards"""
    grade: str
    semester: str
    subject: str
    cp_id: str  # Reference to parent CP
    topics: List[Dict[str, any]] = field(default_factory=list)
    time_allocation: Dict[str, int] = field(default_factory=dict)
    learning_objectives_alignment: Dict[str, List[str]] = field(default_factory=dict)
    assessment_plan: List[str] = field(default_factory=list)


class ATPStandards:
    """ATP Standards Management"""
    
    def __init__(self):
        self.grades_semesters = {
            "1": ["ganjil", "genap"],
            "2": ["ganjil", "genap"],
            "3": ["ganjil", "genap"],
            "4": ["ganjil", "genap"],
            "5": ["ganjil", "genap"],
            "6": ["ganjil", "genap"],
            "7": ["ganjil", "genap"],
            "8": ["ganjil", "genap"],
            "9": ["ganjil", "genap"]
        }
    
    def get_standards(self, grade: str, semester: str, subject: str) -> ATPStructure:
        """Get ATP standards for specific grade, semester, and subject"""
        if grade not in self.grades_semesters:
            raise ValueError(f"Invalid grade: {grade}")
        
        if semester not in self.grades_semesters[grade]:
            raise ValueError(f"Invalid semester: {semester} for grade {grade}")
        
        return ATPStructure(
            grade=grade,
            semester=semester,
            subject=subject,
            cp_id=f"CP_{subject}_{grade}",
            topics=self._get_sample_topics(grade, semester, subject),
            time_allocation=self._get_sample_time_allocation(grade, semester, subject),
            learning_objectives_alignment=self._get_sample_objective_alignment(grade, semester, subject),
            assessment_plan=self._get_sample_assessment_plan(grade, semester, subject)
        )
    
    def validate_structure(self, atp_data: Dict) -> Dict:
        """Validate ATP structure against Kurikulum Merdeka standards"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate required fields
        required_fields = ["grade", "semester", "subject", "cp_id", "topics"]
        for field in required_fields:
            if field not in atp_data:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Missing required field: {field}")
        
        # Validate grade
        if "grade" in atp_data and atp_data["grade"] not in self.grades_semesters:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Invalid grade: {atp_data['grade']}")
        
        # Validate semester
        if "grade" in atp_data and "semester" in atp_data:
            if atp_data["grade"] in self.grades_semesters:
                if atp_data["semester"] not in self.grades_semesters[atp_data["grade"]]:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Invalid semester: {atp_data['semester']} for grade {atp_data['grade']}")
        
        # Validate topics
        if "topics" in atp_data and len(atp_data["topics"]) == 0:
            validation_result["valid"] = False
            validation_result["errors"].append("Topics cannot be empty")
        elif "topics" in atp_data and len(atp_data["topics"]) < 8:
            validation_result["warnings"].append("Low number of topics (recommended 8-12 per semester)")
        
        # Validate time allocation
        if "time_allocation" not in atp_data:
            validation_result["warnings"].append("Missing time allocation")
        
        # Validate CP reference
        if "cp_id" not in atp_data:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing CP reference (cp_id)")
        
        return validation_result
    
    def _get_sample_topics(self, grade: str, semester: str, subject: str) -> List[Dict]:
        """Get sample topics (placeholder for actual data)"""
        return [
            {"topic_id": f"{subject}_{grade}_{semester}_1", "name": f"Introduction to {subject}", "weeks": 2},
            {"topic_id": f"{subject}_{grade}_{semester}_2", "name": f"Core Concepts {subject}", "weeks": 3},
            {"topic_id": f"{subject}_{grade}_{semester}_3", "name": f"Applications {subject}", "weeks": 2},
            {"topic_id": f"{subject}_{grade}_{semester}_4", "name": f"Project-based Learning", "weeks": 2},
            {"topic_id": f"{subject}_{grade}_{semester}_5", "name": f"Assessment and Review", "weeks": 1}
        ]
    
    def _get_sample_time_allocation(self, grade: str, semester: str, subject: str) -> Dict[str, int]:
        """Get sample time allocation (placeholder for actual data)"""
        grade_hours = {
            "1": 4, "2": 4, "3": 5, "4": 5, "5": 6, "6": 6, "7": 7, "8": 7, "9": 8
        }
        return {
            "weekly_hours": grade_hours.get(grade, 5),
            "semester_hours": grade_hours.get(grade, 5) * 20,
            "topic_hours": grade_hours.get(grade, 5) * 4,
            "project_hours": 8,
            "assessment_hours": 6
        }
    
    def _get_sample_objective_alignment(self, grade: str, semester: str, subject: str) -> Dict[str, List[str]]:
        """Get sample learning objective alignment (placeholder for actual data)"""
        return {
            "topic_1": ["understand basic concepts", "identify key terms"],
            "topic_2": ["apply concepts", "analyze relationships"],
            "topic_3": ["solve problems", "evaluate solutions"],
            "topic_4": ["collaborate effectively", "demonstrate creativity"],
            "topic_5": ["assess learning", "reflect on progress"]
        }
    
    def _get_sample_assessment_plan(self, grade: str, semester: str, subject: str) -> List[str]:
        """Get sample assessment plan (placeholder for actual data)"""
        return [
            "Weekly formative assessments",
            "Mid-semester summative assessment",
            "Project-based assessment",
            "Performance tasks",
            "Self-assessment and reflection",
            "End-semester comprehensive assessment"