"""
ATP Generation - Annual Teaching Plan Generation

This service generates Annual Teaching Plans (ATP) from Curriculum Programs (CP)
with automatic time allocation and distribution across semesters and weeks.
"""

from typing import Dict, List, Optional
from datetime import datetime


class ATPGeneration:
    """Annual Teaching Plan generation for Kurikulum Merdeka"""
    
    def __init__(self):
        self.atp_database = {}
        self.semester_structure = {
            "1": {"weeks": 20, "learning_hours": 600},  # 30 hours/week
            "2": {"weeks": 20, "learning_hours": 600}
        }
        self.subject_hour_allocation = {
            "IPA": 4,  # hours per week
            "Matematika": 5,
            "Bahasa Indonesia": 4,
            "PPKn": 2,
            "IPS": 3,
            "Seni Budaya": 2
        }
    
    def generate_atp(self, cp_id: str, grade: str, semester: str, subject: str) -> Dict:
        """Generate Annual Teaching Plan from CP"""
        atp_id = f"atp_{grade}_{semester}_{subject}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Validate semester
        if semester not in self.semester_structure:
            return {"error": f"Invalid semester: {semester}. Valid semesters: {list(self.semester_structure.keys())}"}
        
        semester_info = self.semester_structure[semester]
        
        # Get subject hour allocation
        hours_per_week = self.subject_hour_allocation.get(subject, 4)
        
        # Calculate total hours for subject in semester
        total_hours = semester_info["weeks"] * hours_per_week
        
        # Distribute learning objectives across weeks
        # Note: In real implementation, this would integrate with CP and standards-domain
        weekly_plan = self._distribute_weekly_plan(grade, semester, subject, total_hours)
        
        # Validate time allocation
        allocation_validation = self._validate_time_allocation(weekly_plan, total_hours)
        
        atp_data = {
            "atp_id": atp_id,
            "cp_id": cp_id,
            "grade": grade,
            "semester": semester,
            "subject": subject,
            "semester_info": semester_info,
            "hours_per_week": hours_per_week,
            "total_hours": total_hours,
            "weekly_plan": weekly_plan,
            "allocation_validation": allocation_validation,
            "created_at": datetime.utcnow().isoformat(),
            "status": "draft"
        }
        
        self.atp_database[atp_id] = atp_data
        
        return atp_data
    
    def validate_atp(self, atp_id: str) -> Dict:
        """Validate ATP against Kurikulum Merdeka standards"""
        if atp_id not in self.atp_database:
            return {"error": "ATP not found"}
        
        atp = self.atp_database[atp_id]
        
        validation = self._validate_time_allocation(
            atp["weekly_plan"],
            atp["total_hours"]
        )
        
        return validation
    
    def update_weekly_plan(self, atp_id: str, week_number: int, updates: Dict) -> Dict:
        """Update specific week in ATP"""
        if atp_id not in self.atp_database:
            return {"error": "ATP not found"}
        
        atp = self.atp_database[atp_id]
        
        # Find and update the week
        for week in atp["weekly_plan"]:
            if week["week_number"] == week_number:
                week.update(updates)
                break
        
        # Re-validate after update
        validation = self._validate_time_allocation(atp["weekly_plan"], atp["total_hours"])
        atp["allocation_validation"] = validation
        atp["updated_at"] = datetime.utcnow().isoformat()
        
        return {
            "atp_id": atp_id,
            "week_number": week_number,
            "validation": validation
        }
    
    def _distribute_weekly_plan(self, grade: str, semester: str, subject: str, total_hours: int) -> List[Dict]:
        """Distribute learning objectives across weeks"""
        weekly_plan = []
        weeks = self.semester_structure[semester]["weeks"]
        
        # In real implementation, this would distribute actual learning objectives from CP
        # For now, create a structure with placeholders
        for week_num in range(1, weeks + 1):
            week_hours = total_hours // weeks  # Equal distribution for now
            
            weekly_plan.append({
                "week_number": week_num,
                "learning_hours": week_hours,
                "learning_objectives": [],  # Would come from CP
                "activities": [],  # Would come from curriculum planning
                "assessment": [],  # Would come from assessment planning
                "reflection_components": self._add_weekly_reflection(week_num)
            })
        
        return weekly_plan
    
    def _add_weekly_reflection(self, week_number: int) -> Dict:
        """Add reflection components for weekly plan"""
        return {
            "before_learning": f"Reflection prompt before week {week_number} learning",
            "during_learning": f"Reflection prompt during week {week_number} activities",
            "after_learning": f"Reflection prompt after week {week_number} completion"
        }
    
    def _validate_time_allocation(self, weekly_plan: List[Dict], total_hours: int) -> Dict:
        """Validate time allocation against Kurikulum Merdeka requirements"""
        allocated_hours = sum(week["learning_hours"] for week in weekly_plan)
        
        validation = {
            "valid": True,
            "allocated_hours": allocated_hours,
            "required_hours": total_hours,
            "difference": allocated_hours - total_hours,
            "issues": [],
            "recommendations": []
        }
        
        if abs(allocated_hours - total_hours) > 5:  # Allow small discrepancy
            validation["valid"] = False
            validation["issues"].append(f"Time allocation mismatch: {allocated_hours} vs required {total_hours}")
        
        if allocated_hours > total_hours:
            validation["recommendations"].append("Reduce some learning hours to meet requirements")
        elif allocated_hours < total_hours:
            validation["recommendations"].append("Increase learning hours to meet requirements")
        
        return validation