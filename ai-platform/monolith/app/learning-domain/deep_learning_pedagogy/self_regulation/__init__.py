"""
Self-Regulation Module

This module provides self-regulation tracking and assessment for autonomous learning,
which is a key component of "Pembelajaran Mendalam" framework.
"""

from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class SelfRegulationLevel(Enum):
    """Self-regulation development levels"""
    EMERGING = "emerging"         # Beginning to develop self-regulation
    DEVELOPING = "developing"     # Some self-regulation skills present
    PROFICIENT = "proficient"     # Strong self-regulation
    EXPERT = "expert"             # Advanced self-regulation


class SelfRegulation:
    """Self-regulation tracking and assessment engine"""
    
    def __init__(self):
        self.self_regulation_database = {}
        self.goal_tracking = {}
    
    def assess(self, student_id: str, self_regulation_data: Dict) -> Dict:
        """Assess student self-regulation competency"""
        assessment = {
            "student_id": student_id,
            "goal_setting_score": self._assess_goal_setting(self_regulation_data),
            "planning_score": self._assess_planning(self_regulation_data),
            "monitoring_score": self._assess_monitoring(self_regulation_data),
            "strategy_adjustment_score": self._assess_strategy_adjustment(self_regulation_data),
            "overall_competency": self._determine_competency_level(self_regulation_data),
            "strengths": self._identify_strengths(self_regulation_data),
            "areas_for_improvement": self._identify_improvements(self_regulation_data),
            "recommendations": self._generate_regulation_recommendations(self_regulation_data)
        }
        
        return assessment
    
    def track_goal_achievement(self, student_id: str, goal_data: Dict) -> Dict:
        """Track student goal achievement over time"""
        goal_id = f"goal_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        goal_entry = {
            "goal_id": goal_id,
            "student_id": student_id,
            "goal": goal_data.get("goal"),
            "target_achievement": goal_data.get("target_achievement"),
            "current_progress": goal_data.get("current_progress", 0),
            "deadline": goal_data.get("deadline"),
            "strategies_used": goal_data.get("strategies", []),
            "challenges_encountered": goal_data.get("challenges", []),
            "adjustments_made": goal_data.get("adjustments", []),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.goal_tracking[goal_id] = goal_entry
        
        return {
            "goal_id": goal_id,
            "progress_percentage": (goal_entry["current_progress"] / goal_entry["target_achievement"]) * 100,
            "on_track": goal_entry["current_progress"] >= self._calculate_expected_progress(goal_entry),
            "suggestions": self._generate_goal_suggestions(goal_entry)
        }
    
    def monitor_progress(self, student_id: str, progress_data: Dict) -> Dict:
        """Monitor learning progress and suggest adjustments"""
        monitoring = {
            "student_id": student_id,
            "current_mastery": progress_data.get("current_mastery", 0.5),
            "target_mastery": progress_data.get("target_mastery", 0.8),
            "learning_rate": self._calculate_learning_rate(progress_data),
            "engagement_level": progress_data.get("engagement_level", "medium"),
            "adjustment_recommendations": self._generate_adjustment_recommendations(progress_data),
            "intervention_suggestions": self._generate_intervention_suggestions(progress_data)
        }
        
        return monitoring
    
    def _assess_goal_setting(self, data: Dict) -> float:
        """Assess goal-setting quality (0.0 to 1.0)"""
        goal = data.get("goal", "")
        
        # SMART criteria check
        has_specificity = len(goal.split()) > 5
        has_measurability = any(metric in goal.lower() for metric in ["%", "score", "grade", "complete", "achieve"])
        has_achievability = "impossible" not in goal.lower()
        has_relevance = "relevant" in goal.lower() or "important" in goal.lower()
        has_timeliness = "week" in goal.lower() or "day" in goal.lower() or "month" in goal.lower()
        
        smart_score = sum([has_specificity, has_measurability, has_achievability, has_relevance, has_timeliness]) / 5
        return round(smart_score, 2)
    
    def _assess_planning(self, data: Dict) -> float:
        """Assess planning quality (0.0 to 1.0)"""
        plan = data.get("plan", "")
        planning_elements = data.get("planning_elements", [])
        
        if len(planning_elements) == 0:
            return 0.0
        
        plan_quality = len(planning_elements) / 10  # Assuming 10 planning elements is excellent
        return round(min(1.0, plan_quality), 2)
    
    def _assess_monitoring(self, data: Dict) -> float:
        """Assess self-monitoring quality (0.0 to 1.0)"""
        monitoring_frequency = data.get("monitoring_frequency", "never")
        monitoring_indicators = data.get("monitoring_indicators", [])
        
        frequency_scores = {
            "never": 0.0,
            "rarely": 0.3,
            "sometimes": 0.5,
            "often": 0.8,
            "always": 0.9
        }
        
        frequency_score = frequency_scores.get(monitoring_frequency, 0.5)
        indicator_score = min(1.0, len(monitoring_indicators) / 5)
        
        overall_score = (frequency_score * 0.6) + (indicator_score * 0.4)
        return round(overall_score, 2)
    
    def _assess_strategy_adjustment(self, data: Dict) -> float:
        """Assess strategy adjustment capability (0.0 to 1.0)"""
        adjustments = data.get("adjustments_made", 0)
        effectiveness = data.get("adjustment_effectiveness", 0.5)
        
        adjustment_score = min(1.0, adjustments / 10)  # 10 adjustments is excellent
        effectiveness_score = effectiveness
        
        overall_score = (adjustment_score * 0.5) + (effectiveness_score * 0.5)
        return round(overall_score, 2)
    
    def _determine_competency_level(self, data: Dict) -> str:
        """Determine overall self-regulation competency level"""
        goal_score = self._assess_goal_setting(data)
        planning_score = self._assess_planning(data)
        monitoring_score = self._assess_monitoring(data)
        adjustment_score = self._assess_strategy_adjustment(data)
        
        overall_score = (goal_score + planning_score + monitoring_score + adjustment_score) / 4
        
        if overall_score >= 0.8:
            return "expert"
        elif overall_score >= 0.6:
            return "proficient"
        elif overall_score >= 0.4:
            return "developing"
        else:
            return "emerging"
    
    def _identify_strengths(self, data: Dict) -> List[str]:
        """Identify student's self-regulation strengths"""
        strengths = []
        
        if self._assess_goal_setting(data) >= 0.7:
            strengths.append("Strong goal-setting skills")
        
        if self._assess_planning(data) >= 0.7:
            strengths.append("Effective planning")
        
        if self._assess_monitoring(data) >= 0.7:
            strengths.append("Good self-monitoring")
        
        if self._assess_strategy_adjustment(data) >= 0.7:
            strengths.append("Adaptive strategy adjustment")
        
        return strengths
    
    def _identify_improvements(self, data: Dict) -> List[str]:
        """Identify areas for self-regulation improvement"""
        improvements = []
        
        if self._assess_goal_setting(data) < 0.5:
            improvements.append("Work on SMART goal-setting")
        
        if self._assess_planning(data) < 0.5:
            improvements.append("Improve planning strategies")
        
        if self._assess_monitoring(data) < 0.5:
            improvements.append("Increase self-monitoring frequency")
        
        if self._assess_strategy_adjustment(data) < 0.5:
            improvements.append("Practice adjusting strategies when needed")
        
        return improvements
    
    def _generate_regulation_recommendations(self, data: Dict) -> List[str]:
        """Generate self-regulation recommendations"""
        recommendations = []
        
        competency = self._determine_competency_level(data)
        
        if competency in ["emerging", "developing"]:
            recommendations.append("Start with simple, short-term goals")
            recommendations.append("Use planning templates and checklists")
            recommendations.append("Set regular monitoring reminders")
        elif competency in ["proficient", "expert"]:
            recommendations.append("Challenge yourself with complex goals")
            recommendations.push("Teach self-regulation strategies to others")
            recommendations.append("Reflect on your self-regulation process")
        
        return recommendations
    
    def _calculate_expected_progress(self, goal_entry: Dict) -> float:
        """Calculate expected progress towards goal"""
        if "deadline" not in goal_entry:
            return goal_entry["current_progress"]
        
        # Simplified calculation - in production would be more complex
        days_created = 7  # Assume goals are created 7 days ago
        deadline_days = 30  # Assume 30-day deadline
        expected_progress = (days_created / deadline_days) * goal_entry["target_achievement"]
        
        return expected_progress
    
    def _generate_goal_suggestions(self, goal_entry: Dict) -> List[str]:
        """Generate suggestions for goal achievement"""
        suggestions = []
        
        progress = goal_entry["current_progress"] / goal_entry["target_achievement"]
        
        if progress < 0.25:
            suggestions.append("Break goal into smaller steps")
            suggestions.append("Identify and remove obstacles")
        elif progress < 0.5:
            suggestions.append("Review and adjust your strategies")
            suggestions.append("Seek help from peers or teachers")
        elif progress < 0.75:
            suggestions.append("Maintain current approach")
            suggestions.append("Focus on final push to completion")
        else:
            suggestions.append("Prepare for goal completion")
            suggestions.append("Plan next steps after achievement")
        
        return suggestions
    
    def _calculate_learning_rate(self, progress_data: Dict) -> str:
        """Calculate learning rate"""
        current_mastery = progress_data.get("current_mastery", 0.5)
        # In production would compare with previous mastery data
        return "steady" if current_mastery > 0.6 else "needs_acceleration"
    
    def _generate_adjustment_recommendations(self, progress_data: Dict) -> List[str]:
        """Generate learning adjustment recommendations"""
        recommendations = []
        
        learning_rate = self._calculate_learning_rate(progress_data)
        current_mastery = progress_data.get("current_mastery", 0.5)
        target_mastery = progress_data.get("target_mastery", 0.8)
        
        if learning_rate == "needs_acceleration":
            recommendations.append("Increase study time or intensity")
            recommendations.append("Use different learning strategies")
            recommendations.append("Seek additional support or resources")
        
        if current_mastery < target_mastery * 0.7:
            recommendations.append("Review foundational concepts")
            recommendations.append("Practice with more problems")
            recommendations.append("Connect with peer learning groups")
        
        return recommendations
    
    def _generate_intervention_suggestions(self, progress_data: Dict) -> List[str]:
        """Generate intervention suggestions if needed"""
        suggestions = []
        
        current_mastery = progress_data.get("current_mastery", 0.5)
        target_mastery = progress_data.get("target_mastery", 0.8)
        
        if current_mastery < target_mastery * 0.5:
            suggestions.append("Consider one-on-one tutoring")
            suggestions.append("Schedule additional practice sessions")
            suggestions.append("Modify learning approach based on learning style")
        
        return suggestions
    
    def get_competency_level(self, student_id: str) -> str:
        """Get self-regulation competency level for student"""
        # Placeholder - would retrieve from database
        return "developing"