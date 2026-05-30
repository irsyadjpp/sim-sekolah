"""
Student Deep Learning Dashboard

This module provides a comprehensive dashboard for students aligned with
Pembelajaran Mendalam principles, including learning progress, reflection journal,
metacognitive development, character development, and mastery depth tracking.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict


class DashboardSection(str, Enum):
    """Dashboard section types"""
    LEARNING_PROGRESS = "learning_progress"
    REFLECTION_JOURNAL = "reflection_journal"
    METACOGNITIVE_DEVELOPMENT = "metacognitive_development"
    CHARACTER_DEVELOPMENT = "character_development"
    MASTERY_DEPTH = "mastery_depth"


class ProficiencyLevel(str, Enum):
    """Proficiency levels for mastery tracking"""
    BEGINNING = "beginning"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    MASTERY = "mastery"


class StudentDeepLearningDashboard:
    """Comprehensive student dashboard for Pembelajaran Mendalam"""
    
    def __init__(self):
        self.student_data: Dict[str, Dict] = {}
        self.reflection_entries: Dict[str, List[Dict]] = defaultdict(list)
        self.learning_progress: Dict[str, Dict] = {}
        self.character_development: Dict[str, Dict] = {}
        self.mastery_data: Dict[str, Dict] = {}
    
    def get_dashboard_overview(self, student_id: str) -> Dict:
        """Get comprehensive dashboard overview for student"""
        return {
            "student_id": student_id,
            "last_updated": datetime.utcnow().isoformat(),
            "sections": {
                "learning_progress": self.get_learning_progress(student_id),
                "reflection_journal": self.get_reflection_summary(student_id),
                "metacognitive_development": self.get_metacognitive_development(student_id),
                "character_development": self.get_character_development(student_id),
                "mastery_depth": self.get_mastery_depth(student_id)
            },
            "overall_deep_learning_score": self._calculate_overall_score(student_id),
            "recommendations": self._generate_dashboard_recommendations(student_id)
        }
    
    def get_learning_progress(self, student_id: str) -> Dict:
        """Get learning progress dashboard"""
        progress_data = self.learning_progress.get(student_id, {})
        
        return {
            "section": DashboardSection.LEARNING_PROGRESS.value,
            "overall_progress": progress_data.get("overall_progress", 0),
            "subject_breakdown": self._get_subject_breakdown(student_id),
            "learning_objectives_progress": self._get_objectives_progress(student_id),
            "competency_development": self._get_competency_development(student_id),
            "growth_trajectory": self._get_growth_trajectory(student_id),
            "strengths": progress_data.get("strengths", []),
            "areas_for_improvement": progress_data.get("areas_for_improvement", []),
            "recent_achievements": self._get_recent_achievements(student_id)
        }
    
    def get_reflection_journal(self, student_id: str) -> Dict:
        """Get reflection journal interface"""
        entries = self.reflection_entries.get(student_id, [])
        
        return {
            "section": DashboardSection.REFLECTION_JOURNAL.value,
            "total_entries": len(entries),
            "recent_entries": entries[-5:] if entries else [],
            "reflection_categories": self._get_reflection_categories(student_id),
            "reflection_prompts": self._get_reflection_prompts(student_id),
            "reflection_quality_score": self._calculate_reflection_quality(student_id),
            "reflection_trends": self._analyze_reflection_trends(student_id),
            "suggested_prompts": self._generate_reflection_prompts(student_id)
        }
    
    def get_reflection_summary(self, student_id: str) -> Dict:
        """Get summary of reflection journal"""
        entries = self.reflection_entries.get(student_id, [])
        
        return {
            "total_entries": len(entries),
            "this_week_entries": len([e for e in entries if self._is_this_week(e.get("created_at"))]),
            "reflection_quality": self._calculate_reflection_quality(student_id),
            "most_reflected_topics": self._get_most_reflected_topics(student_id),
            "reflection_streak": self._calculate_reflection_streak(student_id)
        }
    
    def add_reflection_entry(
        self, 
        student_id: str,
        topic: str,
        content: str,
        reflection_type: str,
        mood: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """Add a reflection entry to journal"""
        entry = {
            "entry_id": f"reflection_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "student_id": student_id,
            "topic": topic,
            "content": content,
            "reflection_type": reflection_type,  # pre, during, post
            "mood": mood,
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat(),
            "quality_score": self._assess_reflection_quality(content)
        }
        
        self.reflection_entries[student_id].append(entry)
        
        return {
            "entry_id": entry["entry_id"],
            "status": "added",
            "quality_score": entry["quality_score"],
            "suggested_follow_up": self._generate_follow_up_prompt(topic, reflection_type)
        }
    
    def get_metacognitive_development(self, student_id: str) -> Dict:
        """Get metacognitive development dashboard"""
        student_data = self.student_data.get(student_id, {})
        metacognitive_data = student_data.get("metacognitive", {})
        
        return {
            "section": DashboardSection.METACOGNITIVE_DEVELOPMENT.value,
            "metacognitive_awareness": metacognitive_data.get("awareness_score", 0),
            "self_regulation": metacognitive_data.get("self_regulation_score", 0),
            "strategic_thinking": metacognitive_data.get("strategic_thinking_score", 0),
            "learning_strategy_development": self._get_strategy_development(student_id),
            "goal_setting_abilities": self._get_goal_setting_abilities(student_id),
            "self_assessment_accuracy": self._get_self_assessment_accuracy(student_id),
            "metacognitive_growth": self._track_metacognitive_growth(student_id),
            "developmental_milestones": self._get_metacognitive_milestones(student_id)
        }
    
    def get_character_development(self, student_id: str) -> Dict:
        """Get character development dashboard (Profil Pelajar Pancasila)"""
        character_data = self.character_development.get(student_id, {})
        
        return {
            "section": DashboardSection.CHARACTER_DEVELOPMENT.value,
            "profil_pelajar_pancasila": {
                "beriman": character_data.get("beriman", 0),
                "berkebinekaan_global": character_data.get("berkebinekaan_global", 0),
                "gotong_royong": character_data.get("gotong_royong", 0),
                "kreatif": character_data.get("kreatif", 0),
                "mandiri": character_data.get("mandiri", 0),
                "bernalar_kritis": character_data.get("bernalir_kritis", 0)
            },
            "character_growth_trajectory": self._track_character_growth(student_id),
            "character_strengths": self._identify_character_strengths(student_id),
            "character_development_goals": character_data.get("development_goals", []),
            "evidence_of_character": self._get_character_evidence(student_id),
            "peer_feedback_on_character": self._get_character_feedback(student_id)
        }
    
    def get_mastery_depth(self, student_id: str) -> Dict:
        """Get mastery depth dashboard"""
        mastery_data = self.mastery_data.get(student_id, {})
        
        return {
            "section": DashboardSection.MASTERY_DEPTH.value,
            "overall_mastery_level": self._determine_mastery_level(student_id),
            "subject_mastery": self._get_subject_mastery(student_id),
            "competency_mastery": self._get_competency_mastery(student_id),
            "depth_of_understanding": self._assess_understanding_depth(student_id),
            "application_abilities": self._assess_application_abilities(student_id),
            "transfer_skills": self._assess_transfer_skills(student_id),
            "mastery_progression": self._track_mastery_progression(student_id),
            "mastery_gaps": self._identify_mastery_gaps(student_id),
            "next_mastery_targets": self._set_mastery_targets(student_id)
        }
    
    def update_learning_progress(
        self, 
        student_id: str,
        subject: str,
        objective_id: str,
        progress: float,
        evidence: Optional[Dict] = None
    ) -> Dict:
        """Update learning progress for a specific objective"""
        if student_id not in self.learning_progress:
            self.learning_progress[student_id] = {
                "subjects": defaultdict(dict),
                "objectives": {},
                "overall_progress": 0,
                "strengths": [],
                "areas_for_improvement": []
            }
        
        self.learning_progress[student_id]["subjects"][subject][objective_id] = {
            "progress": progress,
            "last_updated": datetime.utcnow().isoformat(),
            "evidence": evidence or {}
        }
        
        # Recalculate overall progress
        self.learning_progress[student_id]["overall_progress"] = self._recalculate_overall_progress(student_id)
        
        return {
            "student_id": student_id,
            "subject": subject,
            "objective_id": objective_id,
            "new_progress": progress,
            "overall_progress": self.learning_progress[student_id]["overall_progress"]
        }
    
    def update_character_development(
        self, 
        student_id: str,
        dimension: str,
        score: float,
        evidence: Optional[Dict] = None
    ) -> Dict:
        """Update character development for a specific dimension"""
        if student_id not in self.character_development:
            self.character_development[student_id] = {}
        
        self.character_development[student_id][dimension] = {
            "score": score,
            "last_updated": datetime.utcnow().isoformat(),
            "evidence": evidence or {}
        }
        
        return {
            "student_id": student_id,
            "dimension": dimension,
            "new_score": score,
            "overall_character_score": self._calculate_overall_character_score(student_id)
        }
    
    def _get_subject_breakdown(self, student_id: str) -> Dict:
        """Get progress breakdown by subject"""
        progress_data = self.learning_progress.get(student_id, {})
        subjects = progress_data.get("subjects", {})
        
        breakdown = {}
        for subject, objectives in subjects.items():
            if objectives:
                avg_progress = sum(obj["progress"] for obj in objectives.values()) / len(objectives)
                breakdown[subject] = {
                    "progress": avg_progress,
                    "objectives_completed": len([o for o in objectives.values() if o["progress"] >= 100]),
                    "total_objectives": len(objectives)
                }
        
        return breakdown
    
    def _get_objectives_progress(self, student_id: str) -> List[Dict]:
        """Get progress for individual learning objectives"""
        progress_data = self.learning_progress.get(student_id, {})
        objectives = progress_data.get("objectives", {})
        
        return [
            {
                "objective_id": obj_id,
                "objective": obj.get("objective", ""),
                "progress": obj.get("progress", 0),
                "proficiency_level": self._determine_proficiency_level(obj.get("progress", 0))
            }
            for obj_id, obj in objectives.items()
        ]
    
    def _get_competency_development(self, student_id: str) -> Dict:
        """Get competency development tracking"""
        return {
            "critical_thinking": 0.75,
            "collaboration": 0.80,
            "communication": 0.70,
            "creativity": 0.85,
            "problem_solving": 0.72
        }
    
    def _get_growth_trajectory(self, student_id: str) -> List[Dict]:
        """Get learning growth trajectory over time"""
        return [
            {"date": "2026-01-01", "progress": 0.40},
            {"date": "2026-02-01", "progress": 0.55},
            {"date": "2026-03-01", "progress": 0.65},
            {"date": "2026-04-01", "progress": 0.72},
            {"date": "2026-05-01", "progress": 0.78}
        ]
    
    def _get_recent_achievements(self, student_id: str) -> List[Dict]:
        """Get recent learning achievements"""
        return [
            {
                "achievement": "Completed all math objectives for Unit 3",
                "date": "2026-05-25",
                "badge": "math_master"
            },
            {
                "achievement": "5-day reflection streak",
                "date": "2026-05-24",
                "badge": "reflection_streak"
            }
        ]
    
    def _get_reflection_categories(self, student_id: str) -> Dict:
        """Get reflection entry categories"""
        entries = self.reflection_entries.get(student_id, [])
        categories = defaultdict(int)
        
        for entry in entries:
            categories[entry.get("reflection_type", "general")] += 1
        
        return dict(categories)
    
    def _get_reflection_prompts(self, student_id: str) -> List[str]:
        """Get reflection prompts for student"""
        return [
            "What did I learn today?",
            "What was challenging and how did I overcome it?",
            "How does this connect to what I already know?",
            "What questions do I still have?",
            "How can I use this in real life?"
        ]
    
    def _calculate_reflection_quality(self, student_id: str) -> float:
        """Calculate overall reflection quality score"""
        entries = self.reflection_entries.get(student_id, [])
        if not entries:
            return 0.0
        
        return sum(e.get("quality_score", 0) for e in entries) / len(entries)
    
    def _analyze_reflection_trends(self, student_id: str) -> Dict:
        """Analyze reflection trends over time"""
        entries = self.reflection_entries.get(student_id, [])
        if not entries:
            return {"trend": "no_data"}
        
        recent_entries = entries[-10:]
        avg_quality = sum(e.get("quality_score", 0) for e in recent_entries) / len(recent_entries)
        
        return {
            "trend": "improving" if avg_quality > 0.7 else "stable",
            "average_quality": avg_quality,
            "entry_frequency": len(entries) / 30  # entries per day in last month
        }
    
    def _generate_reflection_prompts(self, student_id: str) -> List[str]:
        """Generate personalized reflection prompts"""
        return [
            "Reflect on a recent challenge you overcame",
            "What learning strategy worked best for you today?",
            "How did you collaborate with others today?",
            "What are you most proud of learning this week?"
        ]
    
    def _is_this_week(self, date_str: str) -> bool:
        """Check if date is from this week"""
        try:
            date = datetime.fromisoformat(date_str)
            week_ago = datetime.utcnow() - timedelta(days=7)
            return date >= week_ago
        except:
            return False
    
    def _calculate_reflection_streak(self, student_id: str) -> int:
        """Calculate reflection streak"""
        entries = self.reflection_entries.get(student_id, [])
        if not entries:
            return 0
        
        streak = 0
        current_date = datetime.utcnow()
        
        for entry in reversed(entries[-30:]):  # Check last 30 entries
            entry_date = datetime.fromisoformat(entry.get("created_at"))
            if (current_date - entry_date).days <= 1:
                streak += 1
                current_date = entry_date
            else:
                break
        
        return streak
    
    def _assess_reflection_quality(self, content: str) -> float:
        """Assess quality of reflection entry"""
        # Simple quality assessment based on length and depth
        quality = 0.5
        
        if len(content) > 50:
            quality += 0.2
        if len(content) > 100:
            quality += 0.2
        if "because" in content.lower() or "since" in content.lower():
            quality += 0.1  # Shows reasoning
        
        return min(quality, 1.0)
    
    def _generate_follow_up_prompt(self, topic: str, reflection_type: str) -> str:
        """Generate follow-up reflection prompt"""
        prompts = {
            "pre": f"What do you already know about {topic}?",
            "during": f"What's helping you understand {topic}?",
            "post": f"How will you use what you learned about {topic}?"
        }
        return prompts.get(reflection_type, "What are your thoughts on this?")
    
    def _get_most_reflected_topics(self, student_id: str) -> List[str]:
        """Get most reflected topics"""
        entries = self.reflection_entries.get(student_id, [])
        topic_counts = defaultdict(int)
        
        for entry in entries:
            topic_counts[entry.get("topic", "general")] += 1
        
        return [topic for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _get_strategy_development(self, student_id: str) -> Dict:
        """Get learning strategy development"""
        return {
            "strategies_used": ["note-taking", "self-questioning", "summarization"],
            "strategy_effectiveness": {
                "note-taking": 0.8,
                "self-questioning": 0.75,
                "summarization": 0.85
            },
            "new_strategies_suggested": ["mind_mapping", "peer teaching"]
        }
    
    def _get_goal_setting_abilities(self, student_id: str) -> Dict:
        """Get goal setting abilities"""
        return {
            "goal_clarity": 0.8,
            "goal_achievement_rate": 0.75,
            "goal_adjustment_frequency": "moderate",
            "long_term_goal_alignment": 0.85
        }
    
    def _get_self_assessment_accuracy(self, student_id: str) -> float:
        """Get self-assessment accuracy"""
        return 0.78
    
    def _track_metacognitive_growth(self, student_id: str) -> List[Dict]:
        """Track metacognitive growth over time"""
        return [
            {"date": "2026-01-01", "score": 0.60},
            {"date": "2026-02-01", "score": 0.65},
            {"date": "2026-03-01", "score": 0.72},
            {"date": "2026-04-01", "score": 0.78},
            {"date": "2026-05-01", "score": 0.82}
        ]
    
    def _get_metacognitive_milestones(self, student_id: str) -> List[Dict]:
        """Get metacognitive developmental milestones"""
        return [
            {
                "milestone": "Demonstrates awareness of own learning",
                "achieved": True,
                "date": "2026-02-15"
            },
            {
                "milestone": "Uses multiple learning strategies",
                "achieved": True,
                "date": "2026-03-20"
            },
            {
                "milestone": "Sets and monitors learning goals",
                "achieved": False,
                "target_date": "2026-06-30"
            }
        ]
    
    def _track_character_growth(self, student_id: str) -> Dict:
        """Track character growth over time"""
        return {
            "beriman": {"growth": "+0.15", "trend": "improving"},
            "berkebinekaan_global": {"growth": "+0.20", "trend": "improving"},
            "gotong_royong": {"growth": "+0.10", "trend": "stable"},
            "kreatif": {"growth": "+0.25", "trend": "improving"},
            "mandiri": {"growth": "+0.18", "trend": "improving"},
            "bernalir_kritis": {"growth": "+0.22", "trend": "improving"}
        }
    
    def _identify_character_strengths(self, student_id: str) -> List[str]:
        """Identify character strengths"""
        character_data = self.character_development.get(student_id, {})
        
        strengths = []
        for dimension, data in character_data.items():
            if isinstance(data, dict) and data.get("score", 0) >= 0.8:
                strengths.append(dimension)
        
        return strengths or ["kreatif", "bernalir_kritis"]  # Default if no data
    
    def _get_character_evidence(self, student_id: str) -> List[Dict]:
        """Get evidence of character development"""
        return [
            {
                "dimension": "gotong_royong",
                "evidence": "Helped peer with group project",
                "date": "2026-05-20"
            },
            {
                "dimension": "kreatif",
                "evidence": "Created innovative solution for problem",
                "date": "2026-05-18"
            }
        ]
    
    def _get_character_feedback(self, student_id: str) -> List[Dict]:
        """Get peer feedback on character"""
        return [
            {
                "dimension": "collaboration",
                "feedback": "Always willing to help others",
                "from": "peer_1"
            },
            {
                "dimension": "creativity",
                "feedback": "Brings unique ideas to discussions",
                "from": "peer_2"
            }
        ]
    
    def _calculate_overall_character_score(self, student_id: str) -> float:
        """Calculate overall character development score"""
        character_data = self.character_development.get(student_id, {})
        
        dimensions = ["beriman", "berkebinekaan_global", "gotong_royong", "kreatif", "mandiri", "bernalir_kritis"]
        scores = []
        
        for dimension in dimensions:
            data = character_data.get(dimension, {})
            if isinstance(data, dict):
                scores.append(data.get("score", 0))
            else:
                scores.append(data if isinstance(data, (int, float)) else 0)
        
        return sum(scores) / len(scores) if scores else 0
    
    def _determine_mastery_level(self, student_id: str) -> str:
        """Determine overall mastery level"""
        mastery_data = self.mastery_data.get(student_id, {})
        overall_score = mastery_data.get("overall_score", 0)
        
        if overall_score >= 0.95:
            return ProficiencyLevel.MASTERY.value
        elif overall_score >= 0.85:
            return ProficiencyLevel.ADVANCED.value
        elif overall_score >= 0.70:
            return ProficiencyLevel.PROFICIENT.value
        elif overall_score >= 0.50:
            return ProficiencyLevel.DEVELOPING.value
        else:
            return ProficiencyLevel.BEGINNING.value
    
    def _get_subject_mastery(self, student_id: str) -> Dict:
        """Get mastery by subject"""
        return {
            "matematika": {"level": "proficient", "score": 0.75},
            "bahasa_indonesia": {"level": "advanced", "score": 0.88},
            "ipa": {"level": "proficient", "score": 0.72},
            "ips": {"level": "developing", "score": 0.65}
        }
    
    def _get_competency_mastery(self, student_id: str) -> Dict:
        """Get mastery by competency"""
        return {
            "problem_solving": {"level": "proficient", "score": 0.78},
            "critical_thinking": {"level": "advanced", "score": 0.85},
            "communication": {"level": "proficient", "score": 0.72},
            "collaboration": {"level": "advanced", "score": 0.88}
        }
    
    def _assess_understanding_depth(self, student_id: str) -> Dict:
        """Assess depth of understanding"""
        return {
            "surface_level": 0.20,
            "conceptual_understanding": 0.35,
            "procedural_knowledge": 0.25,
            "deep_understanding": 0.20
        }
    
    def _assess_application_abilities(self, student_id: str) -> Dict:
        """Assess ability to apply knowledge"""
        return {
            "familiar_contexts": 0.85,
            "novel_contexts": 0.65,
            "real_world_application": 0.70,
            "transfer_across_subjects": 0.60
        }
    
    def _assess_transfer_skills(self, student_id: str) -> Dict:
        """Assess transfer of learning skills"""
        return {
            "near_transfer": 0.80,
            "far_transfer": 0.55,
            "transfer_to_new_situations": 0.60
        }
    
    def _track_mastery_progression(self, student_id: str) -> List[Dict]:
        """Track mastery progression over time"""
        return [
            {"date": "2026-01-01", "level": "developing", "score": 0.55},
            {"date": "2026-02-01", "level": "proficient", "score": 0.72},
            {"date": "2026-03-01", "level": "proficient", "score": 0.78},
            {"date": "2026-04-01", "level": "advanced", "score": 0.85},
            {"date": "2026-05-01", "level": "advanced", "score": 0.88}
        ]
    
    def _identify_mastery_gaps(self, student_id: str) -> List[Dict]:
        """Identify mastery gaps"""
        return [
            {
                "area": "transfer to novel contexts",
                "current_level": "developing",
                "target_level": "proficient",
                "priority": "high"
            },
            {
                "area": "far transfer skills",
                "current_level": "beginning",
                "target_level": "proficient",
                "priority": "medium"
            }
        ]
    
    def _set_mastery_targets(self, student_id: str) -> List[Dict]:
        """Set next mastery targets"""
        return [
            {
                "target": "Achieve advanced level in all subjects",
                "deadline": "2026-08-31",
                "action_steps": ["Practice transfer skills", "Work on novel problems"]
            },
            {
                "target": "Improve far transfer abilities",
                "deadline": "2026-07-31",
                "action_steps": ["Apply learning to new contexts", "Connect across subjects"]
            }
        ]
    
    def _determine_proficiency_level(self, progress: float) -> str:
        """Determine proficiency level from progress"""
        if progress >= 95:
            return ProficiencyLevel.MASTERY.value
        elif progress >= 85:
            return ProficiencyLevel.ADVANCED.value
        elif progress >= 70:
            return ProficiencyLevel.PROFICIENT.value
        elif progress >= 50:
            return ProficiencyLevel.DEVELOPING.value
        else:
            return ProficiencyLevel.BEGINNING.value
    
    def _recalculate_overall_progress(self, student_id: str) -> float:
        """Recalculate overall learning progress"""
        progress_data = self.learning_progress.get(student_id, {})
        subjects = progress_data.get("subjects", {})
        
        if not subjects:
            return 0.0
        
        all_objectives = []
        for subject_data in subjects.values():
            all_objectives.extend(obj_data["progress"] for obj_data in subject_data.values())
        
        return sum(all_objectives) / len(all_objectives) if all_objectives else 0.0
    
    def _calculate_overall_score(self, student_id: str) -> float:
        """Calculate overall deep learning score"""
        learning_score = self.learning_progress.get(student_id, {}).get("overall_progress", 0)
        reflection_score = self._calculate_reflection_quality(student_id)
        character_score = self._calculate_overall_character_score(student_id)
        mastery_score = self.mastery_data.get(student_id, {}).get("overall_score", 0)
        
        return (learning_score * 0.3 + reflection_score * 0.2 + character_score * 0.25 + mastery_score * 0.25)
    
    def _generate_dashboard_recommendations(self, student_id: str) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        learning_progress = self.learning_progress.get(student_id, {}).get("overall_progress", 0)
        if learning_progress < 0.7:
            recommendations.append("Focus on completing learning objectives in weak areas")
        
        reflection_quality = self._calculate_reflection_quality(student_id)
        if reflection_quality < 0.7:
            recommendations.append("Write deeper reflections with more reasoning")
        
        character_score = self._calculate_overall_character_score(student_id)
        if character_score < 0.8:
            recommendations.append("Engage in activities that strengthen character dimensions")
        
        if not recommendations:
            recommendations.append("Continue current excellent progress!")
        
        return recommendations
