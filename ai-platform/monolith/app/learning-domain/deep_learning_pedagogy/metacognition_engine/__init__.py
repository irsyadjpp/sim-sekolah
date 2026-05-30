"""
Metacognition Engine Module

This module provides metacognitive development tracking and analysis for "Pembelajaran Mendalam" framework.
Metacognition is a CORE component - understanding how students think about their thinking.
"""

from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class MetacognitiveLevel(Enum):
    """Metacognitive development levels"""
    AWARE = "aware"           # Basic awareness of thinking
    MONITORING = "monitoring"  # Can monitor own thinking
    EVALUATING = "evaluating"  # Can evaluate thinking strategies
    REGULATING = "regulating"  # Can regulate and adjust thinking


class LearningStrategy(Enum):
    """Learning strategy types"""
    REHEARSAL = "rehearsal"
    ELABORATION = "elaboration"
    ORGANIZATION = "organization"
    COMPREHENSION_MONITORING = "comprehension_monitoring"


class MetacognitionEngine:
    """Metacognitive development tracking and analysis engine"""
    
    def __init__(self):
        self.metacognitive_database = {}  # Store metacognitive entries
        self.strategy_effectiveness = {}  # Track strategy effectiveness
        self.student_profiles = {}  # Student metacognitive profiles
    
    def track(self, student_id: str, metacognitive_data: Dict) -> Dict:
        """Track student metacognitive development"""
        entry_id = f"meta_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        entry = {
            "entry_id": entry_id,
            "student_id": student_id,
            "timestamp": datetime.utcnow().isoformat(),
            "strategy_used": metacognitive_data.get("strategy_used"),
            "awareness_level": self._assess_awareness(metacognitive_data),
            "monitoring_quality": self._assess_monitoring(metacognitive_data),
            "evaluation_quality": self._assess_evaluation(metacognitive_data),
            "regulation_quality": self._assess_regulation(metacognitive_data),
            "context": metacognitive_data.get("context", {}),
            "effectiveness": metacognitive_data.get("effectiveness", 0.5)
        }
        
        self.metacognitive_database[entry_id] = entry
        
        # Update student profile
        self._update_student_profile(student_id, entry)
        
        return {
            "entry_id": entry_id,
            "metacognitive_level": self._determine_development_level(student_id),
            "strategy_effectiveness": entry["effectiveness"],
            "recommendations": self._generate_strategy_recommendations(student_id, metacognitive_data)
        }
    
    def analyze_metacognitive_patterns(self, student_id: str) -> Dict:
        """Analyze metacognitive patterns over time"""
        student_entries = [
            entry for entry in self.metacognitive_database.values()
            if entry.get("student_id") == student_id
        ]
        
        if len(student_entries) == 0:
            return {
                "student_id": student_id,
                "pattern": "insufficient_data",
                "recommendations": ["Start tracking metacognitive awareness"]
            }
        
        # Analyze strategy usage patterns
        strategy_usage = {}
        for entry in student_entries:
            strategy = entry.get("strategy_used")
            if strategy:
                strategy_usage[strategy] = strategy_usage.get(strategy, 0) + 1
        
        # Analyze effectiveness patterns
        effectiveness_by_strategy = {}
        for strategy in strategy_usage:
            strategy_entries = [e for e in student_entries if e.get("strategy_used") == strategy]
            avg_effectiveness = sum(e.get("effectiveness", 0) for e in strategy_entries) / len(strategy_entries)
            effectiveness_by_strategy[strategy] = avg_effectiveness
        
        # Analyze developmental progression
        awareness_progression = [e.get("awareness_level", 0) for e in student_entries]
        monitoring_progression = [e.get("monitoring_quality", 0) for e in student_entries]
        
        return {
            "student_id": student_id,
            "strategy_usage": strategy_usage,
            "strategy_effectiveness": effectiveness_by_strategy,
            "awareness_trend": "improving" if len(awareness_progression) > 1 else "stable",
            "monitoring_trend": "improving" if len(monitoring_progression) > 1 else "stable",
            "total_entries": len(student_entries)
        }
    
    def recommend_strategy(self, context: Dict) -> Dict:
        """Recommend optimal learning strategy based on context"""
        task_type = context.get("task_type", "general")
        difficulty_level = context.get("difficulty", "medium")
        student_level = context.get("student_metacognitive_level", "developing")
        
        recommendations = []
        
        if difficulty_level == "easy" and student_level == "developing":
            recommendations.append({
                "strategy": "comprehension_monitoring",
                "reasoning": "Helps build awareness of understanding",
                "estimated_effectiveness": 0.7
            })
        
        if difficulty_level == "medium":
            recommendations.append({
                "strategy": "elaboration",
                "reasoning": "Connects new information to existing knowledge",
                "estimated_effectiveness": 0.8
            })
        
        if task_type in ["problem_solving", "analysis"]:
            recommendations.append({
                "strategy": "organization",
                "reasoning": "Helps structure complex problems",
                "estimated_effectiveness": 0.75
            })
        
        if difficulty_level == "hard" or student_level == "advanced":
            recommendations.append({
                "strategy": "comprehension_monitoring",
                "reasoning": "Monitor and adjust understanding in real-time",
                "estimated_effectiveness": 0.85
            })
        
        return {
            "recommended_strategies": recommendations,
            "context": context,
            "rationale": "Based on task difficulty and student metacognitive level"
        }
    
    def _assess_awareness(self, data: Dict) -> float:
        """Assess metacognitive awareness (0.0 to 1.0)"""
        reflection_text = data.get("reflection", "")
        awareness_indicators = ["i noticed", "i realized", "i became aware", "i recognized"]
        
        awareness_count = sum(1 for indicator in awareness_indicators if indicator in reflection_text.lower())
        return min(1.0, awareness_count * 0.25)
    
    def _assess_monitoring(self, data: Dict) -> float:
        """Assess monitoring quality (0.0 to 1.0)"""
        monitoring_text = data.get("monitoring", "")
        monitoring_indicators = ["i checked", "i monitored", "i tracked", "i observed"]
        
        monitoring_count = sum(1 for indicator in monitoring_indicators if indicator in monitoring_text.lower())
        return min(1.0, monitoring_count * 0.25)
    
    def _assess_evaluation(self, data: Dict) -> float:
        """Assess evaluation quality (0.0 to 1.0)"""
        evaluation_text = data.get("evaluation", "")
        evaluation_indicators = ["i evaluated", "i judged", "i assessed", "successful", "unsuccessful"]
        
        evaluation_count = sum(1 for indicator in evaluation_indicators if indicator in evaluation_text.lower())
        return min(1.0, evaluation_count * 0.25)
    
    def _assess_regulation(self, data: Dict) -> float:
        """Assess regulation quality (0.0 to 1.0)"""
        regulation_text = data.get("regulation", "")
        regulation_indicators = ["i adjusted", "i changed", "i modified", "i tried different approach"]
        
        regulation_count = sum(1 for indicator in regulation_indicators if indicator in regulation_text.lower())
        return min(1.0, regulation_count * 0.25)
    
    def _determine_development_level(self, student_id: str) -> str:
        """Determine metacognitive development level"""
        if student_id not in self.student_profiles:
            return "aware"
        
        profile = self.student_profiles[student_id]
        avg_awareness = profile.get("average_awareness", 0.3)
        avg_monitoring = profile.get("average_monitoring", 0.3)
        avg_evaluation = profile.get("average_evaluation", 0.2)
        avg_regulation = profile.get("average_regulation", 0.1)
        
        overall_score = (avg_awareness + avg_monitoring + avg_evaluation + avg_regulation) / 4
        
        if overall_score >= 0.8:
            return "regulating"
        elif overall_score >= 0.6:
            return "evaluating"
        elif overall_score >= 0.4:
            return "monitoring"
        else:
            return "aware"
    
    def _update_student_profile(self, student_id: str, entry: Dict):
        """Update student metacognitive profile"""
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = {
                "student_id": student_id,
                "entries": [],
                "average_awareness": 0.0,
                "average_monitoring": 0.0,
                "average_evaluation": 0.0,
                "average_regulation": 0.0
            }
        
        profile = self.student_profiles[student_id]
        profile["entries"].append(entry)
        
        # Update averages
        entries = profile["entries"]
        profile["average_awareness"] = sum(e["awareness_level"] for e in entries) / len(entries)
        profile["average_monitoring"] = sum(e["monitoring_quality"] for e in entries) / len(entries)
        profile["average_evaluation"] = sum(e["evaluation_quality"] for e in entries) / len(entries)
        profile["average_regulation"] = sum(e["regulation_quality"] for e in entries) / len(entries)
    
    def _generate_strategy_recommendations(self, student_id: str, current_data: Dict) -> List[str]:
        """Generate personalized strategy recommendations"""
        recommendations = []
        
        if student_id in self.student_profiles:
            profile = self.student_profiles[student_id]
            
            if profile["average_awareness"] < 0.5:
                recommendations.append("Practice metacognitive awareness by thinking about your thinking")
            
            if profile["average_monitoring"] < 0.5:
                recommendations.append("Use comprehension monitoring strategies to track understanding")
            
            if profile["average_regulation"] < 0.5:
                recommendations.append("Practice adjusting your strategies when they're not working")
        
        return recommendations
    
    def get_development_level(self, student_id: str) -> str:
        """Get metacognitive development level for student"""
        return self._determine_development_level(student_id)