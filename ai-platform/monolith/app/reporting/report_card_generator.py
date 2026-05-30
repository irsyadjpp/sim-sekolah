"""
Report Card Generator

This module generates comprehensive report cards for students aligned with Kurikulum Merdeka.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class GradeScale(str, Enum):
    """Grade scales for Kurikulum Merdeka"""
    DESCRIPTIVE = "descriptive"  # Very Good, Good, Fair, Needs Improvement
    NUMERIC_4 = "numeric_4"  # 1-4 scale
    NUMERIC_100 = "numeric_100"  # 0-100 scale


class ReportCardSection(str, Enum):
    """Sections of the report card"""
    STUDENT_INFO = "student_info"
    ACADEMIC_PERFORMANCE = "academic_performance"
    CHARACTER_DEVELOPMENT = "character_development"
    ATTENDANCE = "attendance"
    ACHIEVEMENTS = "achievements"
    TEACHER_COMMENTS = "teacher_comments"
    PARENT_NOTES = "parent_notes"


class ReportCardGenerator:
    """Generator for student report cards"""
    
    def __init__(self):
        self.report_card_templates = self._initialize_templates()
        self.grade_scale = GradeScale.DESCRIPTIVE
    
    def generate_report_card(
        self, 
        student_data: Dict,
        academic_data: Dict,
        character_data: Dict,
        attendance_data: Dict,
        period: str
    ) -> Dict:
        """Generate comprehensive report card"""
        report_card_id = f"report_card_{student_data.get('student_id', '')}_{period}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate each section
        student_info = self._generate_student_info(student_data)
        academic_performance = self._generate_academic_performance(academic_data)
        character_development = self._generate_character_development(character_data)
        attendance = self._generate_attendance(attendance_data)
        achievements = self._generate_achievements(student_data)
        teacher_comments = self._generate_teacher_comments(student_data, academic_data, character_data)
        
        # Calculate overall summary
        overall_summary = self._generate_overall_summary(academic_performance, character_development, attendance)
        
        report_card = {
            "report_card_id": report_card_id,
            "period": period,
            "student_info": student_info,
            "academic_performance": academic_performance,
            "character_development": character_development,
            "attendance": attendance,
            "achievements": achievements,
            "teacher_comments": teacher_comments,
            "overall_summary": overall_summary,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        return report_card
    
    def _generate_student_info(self, student_data: Dict) -> Dict:
        """Generate student information section"""
        return {
            "student_id": student_data.get("student_id", ""),
            "name": student_data.get("name", ""),
            "nisn": student_data.get("nisn", ""),
            "class": student_data.get("class", ""),
            "fase": student_data.get("fase", ""),
            "school": student_data.get("school", "")
        }
    
    def _generate_academic_performance(self, academic_data: Dict) -> Dict:
        """Generate academic performance section"""
        subjects = academic_data.get("subjects", [])
        
        subject_grades = []
        for subject in subjects:
            grade = self._calculate_grade(subject)
            subject_grades.append({
                "subject": subject.get("name", ""),
                "grade": grade,
                "grade_scale": self.grade_scale.value,
                "notes": subject.get("notes", "")
            })
        
        # Calculate overall academic performance
        overall_academic = self._calculate_overall_academic(subject_grades)
        
        return {
            "subject_grades": subject_grades,
            "overall_academic": overall_academic,
            "grade_scale": self.grade_scale.value
        }
    
    def _generate_character_development(self, character_data: Dict) -> Dict:
        """Generate character development section"""
        dimensions = character_data.get("dimensions", [])
        
        dimension_ratings = []
        for dimension in dimensions:
            rating = self._calculate_character_rating(dimension)
            dimension_ratings.append({
                "dimension": dimension.get("name", ""),
                "rating": rating,
                "description": dimension.get("description", "")
            })
        
        # Calculate overall character development
        overall_character = self._calculate_overall_character(dimension_ratings)
        
        return {
            "dimension_ratings": dimension_ratings,
            "overall_character": overall_character,
            "profil_pelajar_pancasila_aligned": True
        }
    
    def _generate_attendance(self, attendance_data: Dict) -> Dict:
        """Generate attendance section"""
        total_days = attendance_data.get("total_days", 0)
        present_days = attendance_data.get("present_days", 0)
        absent_days = attendance_data.get("absent_days", 0)
        excused_absences = attendance_data.get("excused_absences", 0)
        
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return {
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "excused_absences": excused_absences,
            "attendance_percentage": attendance_percentage,
            "attendance_status": self._determine_attendance_status(attendance_percentage)
        }
    
    def _generate_achievements(self, student_data: Dict) -> Dict:
        """Generate achievements section"""
        achievements = student_data.get("achievements", [])
        
        return {
            "achievements": achievements,
            "total_achievements": len(achievements)
        }
    
    def _generate_teacher_comments(
        self, 
        student_data: Dict, 
        academic_data: Dict, 
        character_data: Dict
    ) -> Dict:
        """Generate teacher comments section"""
        # Generate academic comment
        academic_comment = self._generate_academic_comment(academic_data)
        
        # Generate character comment
        character_comment = self._generate_character_comment(character_data)
        
        # Generate overall comment
        overall_comment = self._generate_overall_comment(student_data, academic_data, character_data)
        
        return {
            "academic_comment": academic_comment,
            "character_comment": character_comment,
            "overall_comment": overall_comment
        }
    
    def _generate_overall_summary(
        self, 
        academic_performance: Dict, 
        character_development: Dict, 
        attendance: Dict
    ) -> Dict:
        """Generate overall summary"""
        return {
            "academic_summary": academic_performance.get("overall_academic", {}),
            "character_summary": character_development.get("overall_character", {}),
            "attendance_summary": attendance.get("attendance_status", ""),
            "overall_performance": self._calculate_overall_performance(
                academic_performance,
                character_development,
                attendance
            )
        }
    
    def _calculate_grade(self, subject: Dict) -> str:
        """Calculate grade for a subject"""
        score = subject.get("score", 0)
        
        if self.grade_scale == GradeScale.DESCRIPTIVE:
            if score >= 90:
                return "Sangat Baik"
            elif score >= 75:
                return "Baik"
            elif score >= 60:
                return "Cukup"
            elif score >= 50:
                return "Perlu Bimbingan"
            else:
                return "Belum Tercapai"
        elif self.grade_scale == GradeScale.NUMERIC_4:
            if score >= 90:
                return "4"
            elif score >= 75:
                return "3"
            elif score >= 60:
                return "2"
            elif score >= 50:
                return "1"
            else:
                return "0"
        else:
            return str(score)
    
    def _calculate_character_rating(self, dimension: Dict) -> str:
        """Calculate character rating for a dimension"""
        score = dimension.get("score", 0)
        
        if score >= 0.8:
            return "Sangat Berkembang"
        elif score >= 0.6:
            return "Berkembang Sesuai Harapan"
        elif score >= 0.4:
            return "Mulai Berkembang"
        else:
            return "Perlu Bimbingan"
    
    def _calculate_overall_academic(self, subject_grades: List[Dict]) -> Dict:
        """Calculate overall academic performance"""
        if not subject_grades:
            return {"average": "N/A", "status": "No data"}
        
        # Count grade distribution
        grade_counts = {}
        for subject_grade in subject_grades:
            grade = subject_grade["grade"]
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        # Determine overall status
        if grade_counts.get("Sangat Baik", 0) >= len(subject_grades) * 0.7:
            status = "Sangat Baik"
        elif grade_counts.get("Baik", 0) + grade_counts.get("Sangat Baik", 0) >= len(subject_grades) * 0.7:
            status = "Baik"
        elif grade_counts.get("Cukup", 0) + grade_counts.get("Baik", 0) + grade_counts.get("Sangat Baik", 0) >= len(subject_grades) * 0.7:
            status = "Cukup"
        else:
            status = "Perlu Bimbingan"
        
        return {
            "grade_distribution": grade_counts,
            "status": status
        }
    
    def _calculate_overall_character(self, dimension_ratings: List[Dict]) -> Dict:
        """Calculate overall character development"""
        if not dimension_ratings:
            return {"average": "N/A", "status": "No data"}
        
        # Count rating distribution
        rating_counts = {}
        for dimension_rating in dimension_ratings:
            rating = dimension_rating["rating"]
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        # Determine overall status
        if rating_counts.get("Sangat Berkembang", 0) >= len(dimension_ratings) * 0.7:
            status = "Sangat Berkembang"
        elif rating_counts.get("Berkembang Sesuai Harapan", 0) + rating_counts.get("Sangat Berkembang", 0) >= len(dimension_ratings) * 0.7:
            status = "Berkembang Sesuai Harapan"
        elif rating_counts.get("Mulai Berkembang", 0) + rating_counts.get("Berkembang Sesuai Harapan", 0) + rating_counts.get("Sangat Berkembang", 0) >= len(dimension_ratings) * 0.7:
            status = "Mulai Berkembang"
        else:
            status = "Perlu Bimbingan"
        
        return {
            "rating_distribution": rating_counts,
            "status": status
        }
    
    def _determine_attendance_status(self, attendance_percentage: float) -> str:
        """Determine attendance status"""
        if attendance_percentage >= 95:
            return "Sangat Baik"
        elif attendance_percentage >= 85:
            return "Baik"
        elif attendance_percentage >= 75:
            return "Cukup"
        else:
            return "Perlu Perhatian"
    
    def _generate_academic_comment(self, academic_data: Dict) -> str:
        """Generate academic comment"""
        overall_academic = academic_data.get("overall_academic", {})
        status = overall_academic.get("status", "Cukup")
        
        comment_map = {
            "Sangat Baik": "Siswa menunjukkan prestasi akademik yang sangat baik di berbagai mata pelajaran.",
            "Baik": "Siswa menunjukkan prestasi akademik yang baik dengan konsistensi yang baik.",
            "Cukup": "Siswa menunjukkan prestasi akademik yang cukup, namun masih dapat ditingkatkan.",
            "Perlu Bimbingan": "Siswa memerlukan bimbingan tambahan untuk meningkatkan prestasi akademik."
        }
        
        return comment_map.get(status, "Siswa menunjukkan perkembangan akademik yang perlu ditingkatkan.")
    
    def _generate_character_comment(self, character_data: Dict) -> str:
        """Generate character comment"""
        overall_character = character_data.get("overall_character", {})
        status = overall_character.get("status", "Mulai Berkembang")
        
        comment_map = {
            "Sangat Berkembang": "Siswa menunjukkan perkembangan karakter yang sangat baik sesuai Profil Pelajar Pancasila.",
            "Berkembang Sesuai Harapan": "Siswa menunjukkan perkembangan karakter yang baik sesuai Profil Pelajar Pancasila.",
            "Mulai Berkembang": "Siswa mulai menunjukkan perkembangan karakter sesuai Profil Pelajar Pancasila.",
            "Perlu Bimbingan": "Siswa memerlukan bimbingan untuk mengembangkan karakter sesuai Profil Pelajar Pancasila."
        }
        
        return comment_map.get(status, "Siswa menunjukkan perkembangan karakter yang perlu ditingkatkan.")
    
    def _generate_overall_comment(
        self, 
        student_data: Dict, 
        academic_data: Dict, 
        character_data: Dict
    ) -> str:
        """Generate overall teacher comment"""
        name = student_data.get("name", "Siswa")
        
        overall_comment = f"{name} adalah siswa yang menunjukkan perkembangan yang baik. "
        overall_comment += "Diharapkan {name} terus meningkatkan prestasi dan karakternya."
        
        return overall_comment
    
    def _calculate_overall_performance(
        self, 
        academic_performance: Dict, 
        character_development: Dict, 
        attendance: Dict
    ) -> str:
        """Calculate overall performance"""
        academic_status = academic_performance.get("overall_academic", {}).get("status", "Cukup")
        character_status = character_development.get("overall_character", {}).get("status", "Mulai Berkembang")
        attendance_status = attendance.get("attendance_status", "Cukup")
        
        # Simple logic - in production would be more sophisticated
        if academic_status in ["Sangat Baik", "Baik"] and character_status in ["Sangat Berkembang", "Berkembang Sesuai Harapan"] and attendance_status in ["Sangat Baik", "Baik"]:
            return "Sangat Baik"
        elif academic_status in ["Baik", "Cukup"] and character_status in ["Berkembang Sesuai Harapan", "Mulai Berkembang"] and attendance_status in ["Baik", "Cukup"]:
            return "Baik"
        elif academic_status == "Cukup" and character_status == "Mulai Berkembang" and attendance_status == "Cukup":
            return "Cukup"
        else:
            return "Perlu Perhatian"
    
    def _initialize_templates(self) -> Dict:
        """Initialize report card templates"""
        return {
            "standard": {
                "sections": [
                    "student_info",
                    "academic_performance",
                    "character_development",
                    "attendance",
                    "achievements",
                    "teacher_comments"
                ],
                "grade_scale": GradeScale.DESCRIPTIVE
            },
            "elementary": {
                "sections": [
                    "student_info",
                    "academic_performance",
                    "character_development",
                    "attendance",
                    "teacher_comments"
                ],
                "grade_scale": GradeScale.DESCRIPTIVE
            }
        }
