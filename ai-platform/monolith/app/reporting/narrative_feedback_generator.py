"""
Narrative Feedback Generator

This module generates narrative feedback for students aligned with Kurikulum Merdeka principles.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class FeedbackType(str, Enum):
    """Types of narrative feedback"""
    ACADEMIC = "academic"
    CHARACTER = "character"
    OVERALL = "overall"
    GOAL_ORIENTED = "goal_oriented"
    GROWTH_ORIENTED = "growth_oriented"


class FeedbackTone(str, Enum):
    """Tone of narrative feedback"""
    ENCOURAGING = "encouraging"
    CONSTRUCTIVE = "constructive"
    SUPPORTIVE = "supportive"
    CHALLENGING = "challenging"


class NarrativeFeedbackGenerator:
    """Generator for narrative feedback"""
    
    def __init__(self):
        self.feedback_templates = self._initialize_feedback_templates()
        self.feedback_database = {}
    
    def generate_feedback(
        self, 
        student_data: Dict,
        performance_data: Dict,
        feedback_type: FeedbackType,
        feedback_tone: FeedbackTone = FeedbackTone.CONSTRUCTIVE
    ) -> Dict:
        """Generate narrative feedback for a student"""
        feedback_id = f"feedback_{student_data.get('student_id', '')}_{feedback_type.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate feedback based on type
        if feedback_type == FeedbackType.ACADEMIC:
            feedback = self._generate_academic_feedback(student_data, performance_data, feedback_tone)
        elif feedback_type == FeedbackType.CHARACTER:
            feedback = self._generate_character_feedback(student_data, performance_data, feedback_tone)
        elif feedback_type == FeedbackType.OVERALL:
            feedback = self._generate_overall_feedback(student_data, performance_data, feedback_tone)
        elif feedback_type == FeedbackType.GOAL_ORIENTED:
            feedback = self._generate_goal_oriented_feedback(student_data, performance_data, feedback_tone)
        elif feedback_type == FeedbackType.GROWTH_ORIENTED:
            feedback = self._generate_growth_oriented_feedback(student_data, performance_data, feedback_tone)
        else:
            feedback = self._generate_overall_feedback(student_data, performance_data, feedback_tone)
        
        feedback_result = {
            "feedback_id": feedback_id,
            "student_id": student_data.get("student_id", ""),
            "student_name": student_data.get("name", ""),
            "feedback_type": feedback_type.value,
            "feedback_tone": feedback_tone.value,
            "feedback": feedback,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.feedback_database[feedback_id] = feedback_result
        
        return feedback_result
    
    def generate_parent_feedback(
        self, 
        student_data: Dict,
        performance_data: Dict
    ) -> Dict:
        """Generate feedback for parents"""
        feedback_id = f"parent_feedback_{student_data.get('student_id', '')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate parent-friendly feedback
        feedback = self._generate_parent_feedback_content(student_data, performance_data)
        
        feedback_result = {
            "feedback_id": feedback_id,
            "student_id": student_data.get("student_id", ""),
            "student_name": student_data.get("name", ""),
            "feedback": feedback,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        return feedback_result
    
    def generate_batch_feedback(
        self, 
        students_data: List[Dict],
        feedback_type: FeedbackType,
        feedback_tone: FeedbackTone = FeedbackTone.CONSTRUCTIVE
    ) -> Dict:
        """Generate narrative feedback for multiple students"""
        batch_id = f"batch_feedback_{feedback_type.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate feedback for each student
        individual_feedbacks = []
        for student_data in students_data:
            # Get performance data for student (simplified - in production would retrieve from database)
            performance_data = student_data.get("performance_data", {})
            
            feedback = self.generate_feedback(
                student_data,
                performance_data,
                feedback_type,
                feedback_tone
            )
            individual_feedbacks.append(feedback)
        
        batch_result = {
            "batch_id": batch_id,
            "feedback_type": feedback_type.value,
            "feedback_tone": feedback_tone.value,
            "total_students": len(students_data),
            "individual_feedbacks": individual_feedbacks,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return batch_result
    
    def _generate_academic_feedback(
        self, 
        student_data: Dict, 
        performance_data: Dict, 
        feedback_tone: FeedbackTone
    ) -> Dict:
        """Generate academic feedback"""
        name = student_data.get("name", "Siswa")
        academic_performance = performance_data.get("academic", {})
        strengths = academic_performance.get("strengths", [])
        areas_for_improvement = academic_performance.get("areas_for_improvement", [])
        
        # Generate opening statement based on tone
        opening = self._generate_opening_statement(name, feedback_tone)
        
        # Generate strengths section
        strengths_text = self._generate_strengths_text(strengths)
        
        # Generate areas for improvement section
        improvement_text = self._generate_improvement_text(areas_for_improvement, feedback_tone)
        
        # Generate closing statement
        closing = self._generate_closing_statement(name, feedback_tone)
        
        feedback = {
            "opening": opening,
            "strengths": strengths_text,
            "areas_for_improvement": improvement_text,
            "closing": closing,
            "full_feedback": f"{opening} {strengths_text} {improvement_text} {closing}"
        }
        
        return feedback
    
    def _generate_character_feedback(
        self, 
        student_data: Dict, 
        performance_data: Dict, 
        feedback_tone: FeedbackTone
    ) -> Dict:
        """Generate character development feedback"""
        name = student_data.get("name", "Siswa")
        character_performance = performance_data.get("character", {})
        developed_dimensions = character_performance.get("developed_dimensions", [])
        developing_dimensions = character_performance.get("developing_dimensions", [])
        
        # Generate opening statement
        opening = f"{name} menunjukkan perkembangan karakter yang positif."
        
        # Generate developed dimensions section
        developed_text = self._generate_developed_dimensions_text(developed_dimensions)
        
        # Generate developing dimensions section
        developing_text = self._generate_developing_dimensions_text(developing_dimensions, feedback_tone)
        
        # Generate closing statement
        closing = f"Diharapkan {name} terus mengembangkan karakter sesuai Profil Pelajar Pancasila."
        
        feedback = {
            "opening": opening,
            "developed_dimensions": developed_text,
            "developing_dimensions": developing_text,
            "closing": closing,
            "full_feedback": f"{opening} {developed_text} {developing_text} {closing}"
        }
        
        return feedback
    
    def _generate_overall_feedback(
        self, 
        student_data: Dict, 
        performance_data: Dict, 
        feedback_tone: FeedbackTone
    ) -> Dict:
        """Generate overall feedback"""
        name = student_data.get("name", "Siswa")
        
        # Combine academic and character feedback
        academic_feedback = self._generate_academic_feedback(student_data, performance_data, feedback_tone)
        character_feedback = self._generate_character_feedback(student_data, performance_data, feedback_tone)
        
        # Generate overall summary
        overall_summary = self._generate_overall_summary(student_data, performance_data)
        
        feedback = {
            "academic_feedback": academic_feedback,
            "character_feedback": character_feedback,
            "overall_summary": overall_summary,
            "full_feedback": f"{overall_summary} {academic_feedback['full_feedback']} {character_feedback['full_feedback']}"
        }
        
        return feedback
    
    def _generate_goal_oriented_feedback(
        self, 
        student_data: Dict, 
        performance_data: Dict, 
        feedback_tone: FeedbackTone
    ) -> Dict:
        """Generate goal-oriented feedback"""
        name = student_data.get("name", "Siswa")
        goals = performance_data.get("goals", [])
        goal_progress = performance_data.get("goal_progress", {})
        
        # Generate goal progress feedback
        goal_feedback = self._generate_goal_progress_text(goals, goal_progress)
        
        # Generate goal-setting recommendations
        goal_recommendations = self._generate_goal_recommendations(goal_progress, feedback_tone)
        
        feedback = {
            "goal_progress": goal_feedback,
            "goal_recommendations": goal_recommendations,
            "full_feedback": f"{name} telah membuat kemajuan dalam mencapai tujuan pembelajaran. {goal_feedback} {goal_recommendations}"
        }
        
        return feedback
    
    def _generate_growth_oriented_feedback(
        self, 
        student_data: Dict, 
        performance_data: Dict, 
        feedback_tone: FeedbackTone
    ) -> Dict:
        """Generate growth-oriented feedback"""
        name = student_data.get("name", "Siswa")
        growth_data = performance_data.get("growth", {})
        
        # Generate growth feedback
        growth_feedback = self._generate_growth_text(growth_data)
        
        # Generate growth recommendations
        growth_recommendations = self._generate_growth_recommendations(growth_data, feedback_tone)
        
        feedback = {
            "growth_feedback": growth_feedback,
            "growth_recommendations": growth_recommendations,
            "full_feedback": f"{name} menunjukkan pertumbuhan yang positif. {growth_feedback} {growth_recommendations}"
        }
        
        return feedback
    
    def _generate_parent_feedback_content(
        self, 
        student_data: Dict, 
        performance_data: Dict
    ) -> Dict:
        """Generate parent-friendly feedback"""
        name = student_data.get("name", "Ananda")
        
        # Generate academic summary for parents
        academic_summary = self._generate_parent_academic_summary(performance_data)
        
        # Generate character summary for parents
        character_summary = self._generate_parent_character_summary(performance_data)
        
        # Generate recommendations for parents
        parent_recommendations = self._generate_parent_recommendations(performance_data)
        
        feedback = {
            "academic_summary": academic_summary,
            "character_summary": character_summary,
            "parent_recommendations": parent_recommendations,
            "full_feedback": f"Kepada Orang Tua/Wali {name}, {academic_summary} {character_summary} {parent_recommendations}"
        }
        
        return feedback
    
    def _generate_opening_statement(self, name: str, feedback_tone: FeedbackTone) -> str:
        """Generate opening statement based on tone"""
        tone_map = {
            FeedbackTone.ENCOURAGING: f"{name} telah menunjukkan kemajuan yang sangat baik.",
            FeedbackTone.CONSTRUCTIVE: f"{name} menunjukkan kemajuan yang baik dengan beberapa area yang dapat ditingkatkan.",
            FeedbackTone.SUPPORTIVE: f"{name} didukung untuk terus berkembang dan belajar.",
            FeedbackTone.CHALLENGING: f"{name} ditantang untuk mencapai potensi maksimalnya."
        }
        
        return tone_map.get(feedback_tone, tone_map[FeedbackTone.CONSTRUCTIVE])
    
    def _generate_strengths_text(self, strengths: List[str]) -> str:
        """Generate strengths text"""
        if not strengths:
            return "Siswa menunjukkan kekuatan dalam berbagai area."
        
        strengths_text = "Kekuatan siswa meliputi: " + ", ".join(strengths[:3]) + "."
        return strengths_text
    
    def _generate_improvement_text(self, areas: List[str], feedback_tone: FeedbackTone) -> str:
        """Generate areas for improvement text"""
        if not areas:
            return "Siswa terus menunjukkan perkembangan yang positif."
        
        if feedback_tone == FeedbackTone.ENCOURAGING:
            improvement_text = "Area yang dapat dikembangkan meliputi: " + ", ".join(areas[:2]) + "."
        else:
            improvement_text = "Area yang perlu ditingkatkan meliputi: " + ", ".join(areas[:2]) + "."
        
        return improvement_text
    
    def _generate_closing_statement(self, name: str, feedback_tone: FeedbackTone) -> str:
        """Generate closing statement based on tone"""
        tone_map = {
            FeedbackTone.ENCOURAGING: f"Diharapkan {name} terus mempertahankan kinerja yang baik.",
            FeedbackTone.CONSTRUCTIVE: f"Dengan dukungan yang tepat, {name} akan terus berkembang.",
            FeedbackTone.SUPPORTIVE: f"{name} didukung untuk terus belajar dan berkembang.",
            FeedbackTone.CHALLENGING: f"{name} memiliki potensi untuk mencapai hasil yang lebih baik."
        }
        
        return tone_map.get(feedback_tone, tone_map[FeedbackTone.CONSTRUCTIVE])
    
    def _generate_developed_dimensions_text(self, dimensions: List[str]) -> str:
        """Generate developed dimensions text"""
        if not dimensions:
            return "Siswa menunjukkan perkembangan karakter yang baik."
        
        return "Dimensi karakter yang telah berkembang dengan baik meliputi: " + ", ".join(dimensions[:3]) + "."
    
    def _generate_developing_dimensions_text(self, dimensions: List[str], feedback_tone: FeedbackTone) -> str:
        """Generate developing dimensions text"""
        if not dimensions:
            return "Siswa menunjukkan perkembangan karakter yang seimbang."
        
        return "Dimensi karakter yang sedang dikembangkan meliputi: " + ", ".join(dimensions[:2]) + "."
    
    def _generate_overall_summary(self, student_data: Dict, performance_data: Dict) -> str:
        """Generate overall summary"""
        name = student_data.get("name", "Siswa")
        return f"{name} adalah siswa yang menunjukkan perkembangan yang baik secara akademik dan karakter."
    
    def _generate_goal_progress_text(self, goals: List[Dict], goal_progress: Dict) -> str:
        """Generate goal progress text"""
        if not goals:
            return "Siswa belum menetapkan tujuan pembelajaran spesifik."
        
        achieved_goals = [g for g in goals if goal_progress.get(g.get("id", ""), {}).get("status") == "achieved"]
        
        if achieved_goals:
            return f"Siswa telah mencapai {len(achieved_goals)} dari {len(goals)} tujuan yang ditetapkan."
        else:
            return f"Siswa sedang bekerja menuju {len(goals)} tujuan pembelajaran."
    
    def _generate_goal_recommendations(self, goal_progress: Dict, feedback_tone: FeedbackTone) -> str:
        """Generate goal recommendations"""
        return "Siswa disarankan untuk menetapkan tujuan yang spesifik, terukur, dan dapat dicapai."
    
    def _generate_growth_text(self, growth_data: Dict) -> str:
        """Generate growth text"""
        growth_areas = growth_data.get("growth_areas", [])
        
        if not growth_areas:
            return "Siswa menunjukkan pertumbuhan yang positif dalam berbagai aspek."
        
        return "Siswa menunjukkan pertumbuhan dalam: " + ", ".join(growth_areas[:3]) + "."
    
    def _generate_growth_recommendations(self, growth_data: Dict, feedback_tone: FeedbackTone) -> str:
        """Generate growth recommendations"""
        return "Siswa disarankan untuk terus merefleksikan pertumbuhan dan menetapkan tujuan pengembangan."
    
    def _generate_parent_academic_summary(self, performance_data: Dict) -> str:
        """Generate academic summary for parents"""
        academic = performance_data.get("academic", {})
        status = academic.get("status", "Cukup")
        
        return f"Ananda menunjukkan prestasi akademik yang {status}."
    
    def _generate_parent_character_summary(self, performance_data: Dict) -> str:
        """Generate character summary for parents"""
        character = performance_data.get("character", {})
        status = character.get("status", "Mulai Berkembang")
        
        return f"Dalam hal karakter, ananda menunjukkan perkembangan yang {status} sesuai Profil Pelajar Pancasila."
    
    def _generate_parent_recommendations(self, performance_data: Dict) -> str:
        """Generate recommendations for parents"""
        return "Orang tua diharapkan terus mendukung dan memantau perkembangan ananda di rumah."
    
    def _initialize_feedback_templates(self) -> Dict:
        """Initialize feedback templates"""
        return {
            FeedbackType.ACADEMIC: {
                "structure": ["opening", "strengths", "areas_for_improvement", "closing"],
                "tone_options": ["encouraging", "constructive", "supportive"]
            },
            FeedbackType.CHARACTER: {
                "structure": ["opening", "developed_dimensions", "developing_dimensions", "closing"],
                "tone_options": ["encouraging", "constructive", "supportive"]
            },
            FeedbackType.OVERALL: {
                "structure": ["overall_summary", "academic_feedback", "character_feedback"],
                "tone_options": ["constructive", "supportive"]
            }
        }
