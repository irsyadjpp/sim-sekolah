"""
Application Dimension

This module handles the Application dimension of Pembelajaran Mendalam (Deep Learning).
Application is the second dimension where students apply understanding in authentic contexts.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ApplicationLevel(str, Enum):
    """Levels of application according to Pembelajaran Mendalam"""
    FAMILIAR = "familiar"  # Application in familiar contexts
    NOVEL = "novel"  # Application in new contexts
    COMPLEX = "complex"  # Application in complex, multi-faceted situations
    CREATIVE = "creative"  # Creative application and innovation


class ApplicationContext(str, Enum):
    """Types of application contexts"""
    ACADEMIC = "academic"  # Within academic settings
    REAL_WORLD = "real_world"  # In real-world situations
    PERSONAL = "personal"  # Personal life applications
    SOCIAL = "social"  # Social and community applications
    PROFESSIONAL = "professional"  # Professional/career applications


class ApplicationDimension:
    """Handler for Application dimension of Pembelajaran Mendalam"""
    
    def __init__(self):
        self.application_database = {}
        self.context_framework = self._initialize_context_framework()
    
    def assess_application(
        self, 
        student_id: str, 
        learning_context: Dict,
        evidence: Dict
    ) -> Dict:
        """Assess student's application level"""
        assessment_id = f"apply_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze application across contexts
        context_scores = {}
        for context in ApplicationContext:
            context_scores[context.value] = self._assess_context(
                context, 
                learning_context, 
                evidence
            )
        
        # Calculate overall application level
        overall_level = self._determine_application_level(context_scores)
        
        # Generate application profile
        application_profile = self._generate_application_profile(
            context_scores,
            overall_level
        )
        
        # Generate feedback
        feedback = self._generate_application_feedback(application_profile)
        
        # Generate recommendations
        recommendations = self._generate_application_recommendations(
            application_profile
        )
        
        assessment_result = {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "learning_context": learning_context,
            "context_scores": context_scores,
            "overall_level": overall_level.value,
            "application_profile": application_profile,
            "feedback": feedback,
            "recommendations": recommendations,
            "assessed_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.application_database[assessment_id] = assessment_result
        
        return assessment_result
    
    def track_application_progression(
        self, 
        student_id: str, 
        timeframe: str = "semester"
    ) -> Dict:
        """Track application progression over time"""
        tracking_id = f"apply_track_{student_id}_{timeframe}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get application history
        application_history = self._get_application_history(student_id, timeframe)
        
        if not application_history:
            return {
                "tracking_id": tracking_id,
                "student_id": student_id,
                "error": "No application history found"
            }
        
        # Analyze level progression
        level_progression = self._analyze_level_progression(application_history)
        
        # Analyze context development
        context_development = self._analyze_context_development(application_history)
        
        # Generate progression insights
        progression_insights = self._generate_progression_insights(
            level_progression,
            context_development
        )
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "timeframe": timeframe,
            "application_history": application_history,
            "level_progression": level_progression,
            "context_development": context_development,
            "progression_insights": progression_insights,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        return tracking_result
    
    def generate_application_activities(
        self, 
        learning_context: Dict,
        target_level: ApplicationLevel,
        target_context: ApplicationContext
    ) -> Dict:
        """Generate activities to develop application at target level and context"""
        activity_id = f"apply_act_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate activities based on target level and context
        activities = self._generate_level_context_activities(target_level, target_context, learning_context)
        
        # Generate scaffolding strategies
        scaffolding = self._generate_scaffolding_strategies(target_level, target_context)
        
        # Generate assessment tasks
        assessment_tasks = self._generate_assessment_tasks(target_level, target_context)
        
        activity_result = {
            "activity_id": activity_id,
            "learning_context": learning_context,
            "target_level": target_level.value,
            "target_context": target_context.value,
            "activities": activities,
            "scaffolding": scaffolding,
            "assessment_tasks": assessment_tasks,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return activity_result
    
    def _assess_context(
        self, 
        context: ApplicationContext, 
        learning_context: Dict, 
        evidence: Dict
    ) -> Dict:
        """Assess application in a specific context"""
        context_data = evidence.get(context.value, {})
        
        # Calculate context score
        score = self._calculate_context_score(context, context_data)
        
        # Determine context level
        level = self._determine_context_level(score)
        
        # Generate context feedback
        feedback = self._generate_context_feedback(context, level)
        
        return {
            "context": context.value,
            "score": score,
            "level": level,
            "feedback": feedback,
            "evidence": context_data
        }
    
    def _calculate_context_score(self, context: ApplicationContext, context_data: Dict) -> float:
        """Calculate score for a context"""
        # Simplified calculation - in production would use more sophisticated analysis
        quality = context_data.get("quality", "moderate")
        complexity = context_data.get("complexity", "moderate")
        
        quality_scores = {
            "low": 0.2,
            "moderate": 0.5,
            "high": 0.8,
            "excellent": 1.0
        }
        
        complexity_scores = {
            "simple": 0.3,
            "moderate": 0.6,
            "complex": 0.9
        }
        
        quality_score = quality_scores.get(quality, 0.5)
        complexity_score = complexity_scores.get(complexity, 0.6)
        
        return (quality_score + complexity_score) / 2.0
    
    def _determine_context_level(self, score: float) -> str:
        """Determine level from score"""
        if score >= 0.8:
            return "creative"
        elif score >= 0.6:
            return "complex"
        elif score >= 0.4:
            return "novel"
        else:
            return "familiar"
    
    def _generate_context_feedback(self, context: ApplicationContext, level: str) -> str:
        """Generate feedback for context"""
        feedback_map = {
            "creative": f"Excellent application in {context.value} context - shows creativity",
            "complex": f"Strong application in {context.value} context - handles complexity well",
            "novel": f"Good application in {context.value} context - demonstrates transfer",
            "familiar": f"Basic application in {context.value} context - needs development"
        }
        
        return feedback_map.get(level, "Continue developing application in this context")
    
    def _determine_application_level(self, context_scores: Dict) -> ApplicationLevel:
        """Determine overall application level from context scores"""
        scores = [score_data["score"] for score_data in context_scores.values()]
        
        if not scores:
            return ApplicationLevel.FAMILIAR
        
        average_score = sum(scores) / len(scores)
        
        if average_score >= 0.8:
            return ApplicationLevel.CREATIVE
        elif average_score >= 0.6:
            return ApplicationLevel.COMPLEX
        elif average_score >= 0.4:
            return ApplicationLevel.NOVEL
        else:
            return ApplicationLevel.FAMILIAR
    
    def _generate_application_profile(self, context_scores: Dict, overall_level: ApplicationLevel) -> Dict:
        """Generate application profile"""
        return {
            "overall_level": overall_level.value,
            "context_breakdown": {
                context: score_data["level"]
                for context, score_data in context_scores.items()
            },
            "strengths": [
                context for context, score_data in context_scores.items()
                if score_data["score"] >= 0.7
            ],
            "areas_for_development": [
                context for context, score_data in context_scores.items()
                if score_data["score"] < 0.5
            ]
        }
    
    def _generate_application_feedback(self, profile: Dict) -> Dict:
        """Generate feedback on application"""
        level = profile["overall_level"]
        
        feedback_map = {
            "creative": {
                "message": "Creative application demonstrated",
                "praise": "Excellent ability to apply concepts creatively in various contexts",
                "encouragement": "Continue to innovate and create new applications"
            },
            "complex": {
                "message": "Complex-level application achieved",
                "praise": "Strong ability to handle complex application scenarios",
                "encouragement": "Work toward creative application"
            },
            "novel": {
                "message": "Novel application developing",
                "praise": "Good ability to apply concepts in new contexts",
                "encouragement": "Practice handling more complex situations"
            },
            "familiar": {
                "message": "Familiar-level application",
                "praise": "Basic application in familiar contexts demonstrated",
                "encouragement": "Practice applying in new and varied contexts"
            }
        }
        
        return feedback_map.get(level, feedback_map["novel"])
    
    def _generate_application_recommendations(self, profile: Dict) -> List[str]:
        """Generate recommendations for application development"""
        level = profile["overall_level"]
        areas = profile.get("areas_for_development", [])
        
        recommendations = []
        
        if level == "familiar":
            recommendations.append("Practice applying concepts in new contexts")
            recommendations.append("Apply learning in real-world situations")
            recommendations.append("Try novel applications of concepts")
        elif level == "novel":
            recommendations.append("Practice handling complex application scenarios")
            recommendations.append("Apply in multiple contexts simultaneously")
            recommendations.append("Develop creative applications")
        elif level == "complex":
            recommendations.append("Create innovative applications")
            recommendations.append("Apply in unfamiliar and challenging contexts")
            recommendations.append("Develop original solutions")
        
        for area in areas:
            recommendations.append(f"Develop application in {area} context")
        
        return recommendations
    
    def _get_application_history(self, student_id: str, timeframe: str) -> List[Dict]:
        """Get application assessment history"""
        # In real implementation, would retrieve from database
        return []
    
    def _analyze_level_progression(self, application_history: List[Dict]) -> Dict:
        """Analyze progression of application levels"""
        if len(application_history) < 2:
            return {"progression": "insufficient_data"}
        
        levels = [a.get("overall_level", "familiar") for a in application_history]
        
        level_order = ["familiar", "novel", "complex", "creative"]
        
        early_level_index = level_order.index(levels[0]) if levels[0] in level_order else 0
        recent_level_index = level_order.index(levels[-1]) if levels[-1] in level_order else 0
        
        progression_type = "improving" if recent_level_index > early_level_index else "stable" if recent_level_index == early_level_index else "declining"
        
        return {
            "progression": progression_type,
            "early_level": levels[0],
            "recent_level": levels[-1],
            "level_improvement": recent_level_index - early_level_index
        }
    
    def _analyze_context_development(self, application_history: List[Dict]) -> Dict:
        """Analyze development across application contexts"""
        context_progress = {}
        
        for context in ApplicationContext:
            context_name = context.value
            scores = [
                a.get("context_scores", {}).get(context_name, {}).get("score", 0.5)
                for a in application_history
            ]
            
            if scores:
                context_progress[context_name] = {
                    "average": sum(scores) / len(scores),
                    "trend": "improving" if len(scores) >= 2 and scores[-1] > scores[0] else "stable"
                }
        
        return context_progress
    
    def _generate_progression_insights(self, level_progression: Dict, context_development: Dict) -> List[str]:
        """Generate insights from application progression"""
        insights = []
        
        progression = level_progression.get("progression")
        if progression == "improving":
            insights.append("Application level is improving over time")
        elif progression == "stable":
            insights.append("Application level is stable - consider new challenges")
        
        for context, data in context_development.items():
            if data.get("trend") == "improving":
                insights.append(f"Application in {context} is developing well")
            elif data.get("trend") == "stable":
                insights.append(f"Application in {context} needs targeted development")
        
        return insights
    
    def _generate_level_context_activities(self, target_level: ApplicationLevel, target_context: ApplicationContext, learning_context: Dict) -> List[Dict]:
        """Generate activities for target level and context"""
        subject = learning_context.get("subject", "subject")
        
        activities = [
            {
                "activity": f"Apply {subject} in {target_context.value} context",
                "description": f"Practice applying {subject} concepts in {target_context.value} situations",
                "level": target_level.value,
                "duration": "20 minutes"
            },
            {
                "activity": "Problem-solving application",
                "description": f"Solve {subject} problems in {target_context.value} context",
                "level": target_level.value,
                "duration": "25 minutes"
            }
        ]
        
        return activities
    
    def _generate_scaffolding_strategies(self, target_level: ApplicationLevel, target_context: ApplicationContext) -> List[str]:
        """Generate scaffolding strategies for target level and context"""
        scaffolding = [
            f"Provide examples of {target_level.value} application in {target_context.value} context",
            f"Guide application process in {target_context.value} situations",
            f"Support reflection on application in {target_context.value} context"
        ]
        
        return scaffolding
    
    def _generate_assessment_tasks(self, target_level: ApplicationLevel, target_context: ApplicationContext) -> List[Dict]:
        """Generate assessment tasks for target level and context"""
        tasks = [
            {
                "task": f"Application task in {target_context.value} context",
                "level": target_level.value,
                "focus": "application"
            },
            {
                "task": "Problem-solving assessment",
                "level": target_level.value,
                "focus": "problem_solving"
            }
        ]
        
        return tasks
    
    def _initialize_context_framework(self) -> Dict:
        """Initialize application context framework"""
        return {
            ApplicationContext.ACADEMIC.value: {
                "description": "Application within academic and school settings",
                "examples": ["classroom projects", "academic presentations", "research projects"]
            },
            ApplicationContext.REAL_WORLD.value: {
                "description": "Application in real-world, everyday situations",
                "examples": ["community projects", "practical problems", "authentic tasks"]
            },
            ApplicationContext.PERSONAL.value: {
                "description": "Application in personal life and interests",
                "examples": ["personal projects", "hobbies", "personal goals"]
            },
            ApplicationContext.SOCIAL.value: {
                "description": "Application in social and community contexts",
                "examples": ["community service", "social projects", "collaborative work"]
            },
            ApplicationContext.PROFESSIONAL.value: {
                "description": "Application in professional and career contexts",
                "examples": ["career exploration", "professional projects", "workplace applications"]
            }
        }
