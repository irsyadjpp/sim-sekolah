"""
Reflection Engine Module

This module provides reflection analysis and management for "Pembelajaran Mendalam" framework.
Reflection is a CORE component of deep learning according to Indonesian government documentation.
"""

from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class ReflectionType(Enum):
    """Types of reflection in learning process"""
    BEFORE_LEARNING = "before"  # Pre-learning reflection
    DURING_LEARNING = "during"  # In-process reflection
    AFTER_LEARNING = "after"    # Post-learning reflection


class ReflectionDepth(Enum):
    """Depth levels of reflection"""
    SURFACE = "surface"      # Basic description
    INTERMEDIATE = "intermediate"  # Making connections
    DEEP = "deep"            # Critical analysis and synthesis


class ReflectionEngine:
    """Reflection analysis and management engine"""
    
    def __init__(self):
        self.reflection_database = {}  # Store reflection entries
        self.reflection_patterns = {
            "cognitive": ["analyzed", "evaluated", "synthesized", "questioned"],
            "emotional": ["felt", "experienced", "reacted", "connected"],
            "metacognitive": ["realized", "planned", "monitored", "adjusted"],
            "social": ["collaborated", "communicated", "received_feedback", "contributed"]
        }
    
    def analyze(self, reflection_data: Dict) -> Dict:
        """Analyze reflection content and depth"""
        reflection_text = reflection_data.get("text", "")
        
        analysis = {
            "reflection_id": f"reflection_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "reflection_type": reflection_data.get("type", "after"),
            "depth": self._assess_depth(reflection_text),
            "patterns_detected": self._detect_patterns(reflection_text),
            "quality_score": self._calculate_quality_score(reflection_text),
            "suggestions": self._generate_improvement_suggestions(reflection_text),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return analysis
    
    def track_student_development(self, student_id: str) -> Dict:
        """Track reflection development over time"""
        student_reflections = [
            ref for ref in self.reflection_database.values() 
            if ref.get("student_id") == student_id
        ]
        
        if len(student_reflections) == 0:
            return {
                "student_id": student_id,
                "development_level": "beginner",
                "trend": "insufficient_data",
                "total_reflections": 0
            }
        
        # Analyze progression
        depth_progression = [ref.get("depth") for ref in student_reflections]
        quality_progression = [ref.get("quality_score", 0) for ref in student_reflections]
        
        avg_depth = self._calculate_most_common(depth_progression)
        avg_quality = sum(quality_progression) / len(quality_progression)
        
        # Determine development level
        if avg_quality >= 0.8 and avg_depth == "deep":
            development_level = "advanced"
        elif avg_quality >= 0.6 and avg_depth in ["intermediate", "deep"]:
            development_level = "developing"
        else:
            development_level = "emerging"
        
        return {
            "student_id": student_id,
            "development_level": development_level,
            "total_reflections": len(student_reflections),
            "average_depth": avg_depth,
            "average_quality_score": avg_quality,
            "trend": "improving" if len(quality_progression) > 1 and quality_progression[-1] > quality_progression[0] else "stable"
        }
    
    def generate_reflection_prompt(self, context: Dict) -> str:
        """Generate AI-powered reflection prompt based on context"""
        subject = context.get("subject", "this subject")
        activity = context.get("activity", "learning activity")
        learning_objective = context.get("learning_objective", "the learning objective")
        reflection_type = context.get("reflection_type", "after")
        
        if reflection_type == "before":
            prompt = f"""
            Before you begin the {activity} in {subject}:
            
            1. What do you already know about {learning_objective}?
            2. What challenges do you anticipate?
            3. What strategies will you use to overcome challenges?
            4. How will you know if you're successful?
            """
        elif reflection_type == "during":
            prompt = f"""
            While working on the {activity} in {subject}:
            
            1. What is working well for you?
            2. What challenges are you facing?
            3. What strategies are you using?
            4. How are you feeling about your progress?
            """
        else:  # after learning
            prompt = f"""
            After completing the {activity} in {subject}:
            
            1. What did you learn about {learning_objective}?
            2. What strategies were most effective?
            3. What would you do differently next time?
            4. How can you apply this learning in other situations?
            """
        
        return prompt.strip()
    
    def _assess_depth(self, text: str) -> str:
        """Assess reflection depth based on text analysis"""
        text_lower = text.lower()
        
        deep_indicators = ["analyze", "evaluate", "synthesize", "critique", "because", "however", "although", "relate", "connect"]
        intermediate_indicators = ["describe", "explain", "understand", "identify", "explain why"]
        surface_indicators = ["i think", "i feel", "good", "bad", "nice", "interesting"]
        
        deep_count = sum(1 for indicator in deep_indicators if indicator in text_lower)
        intermediate_count = sum(1 for indicator in intermediate_indicators if indicator in text_lower)
        surface_count = sum(1 for indicator in surface_indicators if indicator in text_lower)
        
        if deep_count >= 2:
            return "deep"
        elif intermediate_count >= 2:
            return "intermediate"
        else:
            return "surface"
    
    def _detect_patterns(self, text: str) -> List[str]:
        """Detect reflection patterns in text"""
        detected_patterns = []
        text_lower = text.lower()
        
        for pattern_type, keywords in self.reflection_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_patterns.append(pattern_type)
        
        return detected_patterns
    
    def _calculate_quality_score(self, text: str) -> float:
        """Calculate reflection quality score (0.0 to 1.0)"""
        word_count = len(text.split())
        sentence_count = max(1, text.count("."))
        
        # Length assessment
        if word_count < 10:
            length_score = 0.3
        elif word_count < 30:
            length_score = 0.6
        elif word_count < 50:
            length_score = 0.8
        else:
            length_score = 0.9
        
        # Pattern assessment
        patterns = self._detect_patterns(text)
        pattern_score = min(1.0, len(patterns) * 0.25)
        
        # Depth assessment
        depth = self._assess_depth(text)
        depth_scores = {"surface": 0.3, "intermediate": 0.6, "deep": 0.9}
        depth_score = depth_scores.get(depth, 0.5)
        
        overall_score = (length_score * 0.4) + (pattern_score * 0.3) + (depth_score * 0.3)
        return round(overall_score, 2)
    
    def _generate_improvement_suggestions(self, text: str) -> List[str]:
        """Generate suggestions to improve reflection quality"""
        suggestions = []
        text_lower = text.lower()
        depth = self._assess_depth(text)
        
        if depth == "surface":
            suggestions.append("Try to include more analysis - ask 'why' and 'how' questions")
            suggestions.append("Connect your learning to other subjects or experiences")
        
        if "because" not in text_lower and "however" not in text_lower:
            suggestions.append("Add reasoning words like 'because' or 'however' to deepen your reflection")
        
        word_count = len(text.split())
        if word_count < 20:
            suggestions.append("Expand your reflection with more details and examples")
        
        patterns = self._detect_patterns(text)
        if "metacognitive" not in patterns:
            suggestions.append("Consider what strategies worked and how you can improve them")
        
        return suggestions
    
    def _calculate_most_common(self, items: List) -> str:
        """Calculate most common item in list"""
        if not items:
            return "intermediate"
        
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        
        return max(counts, key=counts.get)
    
    def get_development_level(self, student_id: str) -> str:
        """Get reflection development level for student"""
        development_data = self.track_student_development(student_id)
        return development_data.get("development_level", "beginner")