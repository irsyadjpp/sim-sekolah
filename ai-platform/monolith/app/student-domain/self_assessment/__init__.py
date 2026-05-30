"""
Self Assessment

This module provides self-assessment capabilities for students to evaluate their learning,
aligned with Pembelajaran Mendalam principles.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class AssessmentType(str, Enum):
    """Types of self-assessments"""
    LEARNING_PROGRESS = "learning_progress"
    SKILL_DEVELOPMENT = "skill_development"
    CHARACTER_DEVELOPMENT = "character_development"
    METACOGNITIVE_AWARENESS = "metacognitive_awareness"
    GOAL_ACHIEVEMENT = "goal_achievement"


class AssessmentScale(str, Enum):
    """Assessment scales"""
    LIKERT_5 = "likert_5"  # 1-5 scale
    LIKERT_7 = "likert_7"  # 1-7 scale
    PERCENTAGE = "percentage"  # 0-100 scale
    DESCRIPTIVE = "descriptive"  # Text-based


class SelfAssessment:
    """Self-assessment service for student learning evaluation"""
    
    def __init__(self):
        self.assessment_database = {}
        self.assessment_templates = self._initialize_assessment_templates()
        self.rubric_library = self._initialize_rubric_library()
    
    def create_assessment(
        self, 
        student_id: str, 
        assessment_data: Dict
    ) -> Dict:
        """Create a self-assessment for a student"""
        assessment_id = f"self_assess_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine assessment type
        assessment_type = self._determine_assessment_type(assessment_data)
        
        # Generate assessment questions
        questions = self._generate_assessment_questions(assessment_type, assessment_data)
        
        # Create assessment structure
        assessment = self._create_assessment_structure(
            assessment_type,
            assessment_data,
            questions
        )
        
        # Add rubric for assessment
        rubric = self._get_rubric(assessment_type)
        
        # Calculate assessment score
        score = self._calculate_assessment_score(assessment, rubric)
        
        # Generate feedback
        feedback = self._generate_assessment_feedback(score, assessment_type)
        
        # Generate recommendations
        recommendations = self._generate_assessment_recommendations(score, assessment_type)
        
        assessment_result = {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "assessment_type": assessment_type.value,
            "assessment": assessment,
            "questions": questions,
            "rubric": rubric,
            "score": score,
            "feedback": feedback,
            "recommendations": recommendations,
            "created_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.assessment_database[assessment_id] = assessment_result
        
        return assessment_result
    
    def track_assessment_progress(
        self, 
        student_id: str, 
        timeframe: str = "semester"
    ) -> Dict:
        """Track self-assessment progress over time"""
        tracking_id = f"assess_track_{student_id}_{timeframe}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get assessment history
        assessment_history = self._get_assessment_history(student_id, timeframe)
        
        if not assessment_history:
            return {
                "tracking_id": tracking_id,
                "student_id": student_id,
                "error": "No assessment history found"
            }
        
        # Analyze score progression
        score_progression = self._analyze_score_progression(assessment_history)
        
        # Analyze assessment type distribution
        type_distribution = self._analyze_type_distribution(assessment_history)
        
        # Identify assessment patterns
        assessment_patterns = self._identify_assessment_patterns(assessment_history)
        
        # Generate development insights
        development_insights = self._generate_assessment_insights(
            score_progression,
            type_distribution,
            assessment_patterns
        )
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "timeframe": timeframe,
            "assessment_history": assessment_history,
            "score_progression": score_progression,
            "type_distribution": type_distribution,
            "assessment_patterns": assessment_patterns,
            "development_insights": development_insights,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        return tracking_result
    
    def generate_reflection_prompts(
        self, 
        student_id: str, 
        assessment_result: Dict
    ) -> Dict:
        """Generate reflection prompts based on self-assessment results"""
        reflection_id = f"reflect_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze assessment results
        score = assessment_result.get("score", {})
        assessment_type = assessment_result.get("assessment_type", "")
        
        # Generate reflection prompts based on score
        prompts = self._generate_score_based_prompts(score, assessment_type)
        
        # Generate strength-based prompts
        strength_prompts = self._generate_strength_prompts(assessment_result)
        
        # Generate improvement-based prompts
        improvement_prompts = self._generate_improvement_prompts(assessment_result)
        
        # Generate goal-setting prompts
        goal_prompts = self._generate_goal_prompts(assessment_result)
        
        reflection_result = {
            "reflection_id": reflection_id,
            "student_id": student_id,
            "assessment_result": assessment_result,
            "score_based_prompts": prompts,
            "strength_prompts": strength_prompts,
            "improvement_prompts": improvement_prompts,
            "goal_prompts": goal_prompts,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return reflection_result
    
    def _determine_assessment_type(self, assessment_data: Dict) -> AssessmentType:
        """Determine assessment type from data"""
        type_hint = assessment_data.get("type", "")
        
        type_map = {
            "learning": AssessmentType.LEARNING_PROGRESS,
            "skill": AssessmentType.SKILL_DEVELOPMENT,
            "character": AssessmentType.CHARACTER_DEVELOPMENT,
            "metacognitive": AssessmentType.METACOGNITIVE_AWARENESS,
            "goal": AssessmentType.GOAL_ACHIEVEMENT
        }
        
        return type_map.get(type_hint, AssessmentType.LEARNING_PROGRESS)
    
    def _generate_assessment_questions(self, assessment_type: AssessmentType, assessment_data: Dict) -> List[Dict]:
        """Generate assessment questions based on type"""
        questions_map = {
            AssessmentType.LEARNING_PROGRESS: [
                {
                    "question": "How well do you understand the material?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Very Poor", "Poor", "Fair", "Good", "Excellent"]
                },
                {
                    "question": "How confident are you in applying what you learned?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Not Confident", "Slightly Confident", "Moderately Confident", "Confident", "Very Confident"]
                },
                {
                    "question": "How much effort did you put into learning?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Very Little", "Little", "Moderate", "High", "Very High"]
                }
            ],
            AssessmentType.SKILL_DEVELOPMENT: [
                {
                    "question": "How would you rate your current skill level?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Beginner", "Novice", "Intermediate", "Advanced", "Expert"]
                },
                {
                    "question": "How much have you improved recently?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Not at all", "Slightly", "Moderately", "Significantly", "Dramatically"]
                }
            ],
            AssessmentType.CHARACTER_DEVELOPMENT: [
                {
                    "question": "How well do you demonstrate this character trait?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Rarely", "Sometimes", "Often", "Very Often", "Always"]
                },
                {
                    "question": "How important is this trait to you?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Not Important", "Slightly Important", "Moderately Important", "Important", "Very Important"]
                }
            ],
            AssessmentType.METACOGNITIVE_AWARENESS: [
                {
                    "question": "How aware are you of your thinking processes?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Not Aware", "Slightly Aware", "Moderately Aware", "Aware", "Very Aware"]
                },
                {
                    "question": "How well can you monitor your understanding?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Poorly", "Fairly", "Moderately", "Well", "Very Well"]
                }
            ],
            AssessmentType.GOAL_ACHIEVEMENT: [
                {
                    "question": "How much progress have you made toward your goal?",
                    "scale": AssessmentScale.PERCENTAGE.value,
                    "options": ["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"]
                },
                {
                    "question": "How likely are you to achieve your goal?",
                    "scale": AssessmentScale.LIKERT_5.value,
                    "options": ["Very Unlikely", "Unlikely", "Neutral", "Likely", "Very Likely"]
                }
            ]
        }
        
        return questions_map.get(assessment_type, questions_map[AssessmentType.LEARNING_PROGRESS])
    
    def _create_assessment_structure(self, assessment_type: AssessmentType, assessment_data: Dict, questions: List[Dict]) -> Dict:
        """Create assessment structure"""
        return {
            "type": assessment_type.value,
            "context": assessment_data.get("context", {}),
            "questions": questions,
            "responses": assessment_data.get("responses", {}),
            "notes": assessment_data.get("notes", "")
        }
    
    def _get_rubric(self, assessment_type: AssessmentType) -> Dict:
        """Get rubric for assessment type"""
        rubric_map = {
            AssessmentType.LEARNING_PROGRESS: {
                "excellent": {"range": "4-5", "description": "Demonstrates deep understanding and confident application"},
                "good": {"range": "3-3.9", "description": "Shows good understanding with some application"},
                "fair": {"range": "2-2.9", "description": "Basic understanding with limited application"},
                "poor": {"range": "1-1.9", "description": "Limited understanding and application"}
            },
            AssessmentType.SKILL_DEVELOPMENT: {
                "expert": {"range": "4-5", "description": "Demonstrates expert-level skill"},
                "advanced": {"range": "3-3.9", "description": "Shows advanced skill level"},
                "intermediate": {"range": "2-2.9", "description": "Intermediate skill level"},
                "beginner": {"range": "1-1.9", "description": "Beginner skill level"}
            }
        }
        
        return rubric_map.get(assessment_type, rubric_map[AssessmentType.LEARNING_PROGRESS])
    
    def _calculate_assessment_score(self, assessment: Dict, rubric: Dict) -> Dict:
        """Calculate assessment score"""
        responses = assessment.get("responses", {})
        questions = assessment.get("questions", [])
        
        if not responses:
            return {"overall_score": 0.0, "level": "no_data"}
        
        # Calculate average score from responses
        total_score = 0
        total_questions = 0
        
        for question in questions:
            question_id = f"q_{questions.index(question)}"
            response = responses.get(question_id, 0)
            
            # Convert response to numeric score
            if isinstance(response, str):
                # Convert text response to numeric
                options = question.get("options", [])
                if response in options:
                    score = options.index(response) + 1
                else:
                    score = 3  # Default to middle
            else:
                score = response
            
            total_score += score
            total_questions += 1
        
        average_score = total_score / total_questions if total_questions > 0 else 0
        
        # Determine level based on rubric
        level = self._determine_score_level(average_score, rubric)
        
        return {
            "overall_score": average_score,
            "level": level,
            "max_score": 5.0,
            "percentage": (average_score / 5.0) * 100
        }
    
    def _determine_score_level(self, score: float, rubric: Dict) -> str:
        """Determine score level from rubric"""
        if score >= 4.0:
            return "excellent"
        elif score >= 3.0:
            return "good"
        elif score >= 2.0:
            return "fair"
        else:
            return "poor"
    
    def _generate_assessment_feedback(self, score: Dict, assessment_type: AssessmentType) -> Dict:
        """Generate feedback based on assessment score"""
        level = score.get("level", "fair")
        
        feedback_map = {
            "excellent": {
                "message": "Excellent work! You demonstrate strong understanding and application.",
                "strengths": ["Deep understanding", "Confident application", "Consistent effort"],
                "areas": ["Continue current approach", "Consider helping others"]
            },
            "good": {
                "message": "Good work! You show solid understanding with room for growth.",
                "strengths": ["Good understanding", "Consistent effort"],
                "areas": ["Deepen understanding", "Increase application"]
            },
            "fair": {
                "message": "Fair progress. You show basic understanding that needs development.",
                "strengths": ["Basic understanding"],
                "areas": ["Increase effort", "Practice application", "Seek clarification"]
            },
            "poor": {
                "message": "Needs improvement. Focus on building foundational understanding.",
                "strengths": ["Willingness to assess"],
                "areas": ["Increase effort", "Seek help", "Practice fundamentals"]
            }
        }
        
        return feedback_map.get(level, feedback_map["fair"])
    
    def _generate_assessment_recommendations(self, score: Dict, assessment_type: AssessmentType) -> List[str]:
        """Generate recommendations based on assessment"""
        level = score.get("level", "fair")
        
        if level == "excellent":
            return [
                "Continue current learning approach",
                "Consider peer teaching to reinforce learning",
                "Set more challenging goals"
            ]
        elif level == "good":
            return [
                "Deepen understanding through practice",
                "Apply learning in new contexts",
                "Seek feedback to improve further"
            ]
        elif level == "fair":
            return [
                "Increase study time and effort",
                "Practice application of concepts",
                "Seek additional resources and support"
            ]
        else:
            return [
                "Focus on building foundational understanding",
                "Seek teacher guidance and support",
                "Practice regularly with feedback"
            ]
    
    def _get_assessment_history(self, student_id: str, timeframe: str) -> List[Dict]:
        """Get assessment history for student"""
        # In real implementation, would retrieve from database
        return []
    
    def _analyze_score_progression(self, assessment_history: List[Dict]) -> Dict:
        """Analyze score progression over time"""
        if len(assessment_history) < 2:
            return {"progression": "insufficient_data"}
        
        scores = [a.get("score", {}).get("overall_score", 0) for a in assessment_history]
        
        early_avg = sum(scores[:2]) / 2
        recent_avg = sum(scores[-2:]) / 2
        
        progression_type = "improving" if recent_avg > early_avg + 0.2 else "stable" if abs(recent_avg - early_avg) <= 0.2 else "declining"
        
        return {
            "progression": progression_type,
            "early_average": early_avg,
            "recent_average": recent_avg,
            "improvement": recent_avg - early_avg
        }
    
    def _analyze_type_distribution(self, assessment_history: List[Dict]) -> Dict:
        """Analyze distribution of assessment types"""
        type_counts = {}
        
        for assessment in assessment_history:
            assessment_type = assessment.get("assessment_type", "")
            type_counts[assessment_type] = type_counts.get(assessment_type, 0) + 1
        
        return {
            "type_distribution": type_counts,
            "most_common_type": max(type_counts, key=type_counts.get) if type_counts else "none"
        }
    
    def _identify_assessment_patterns(self, assessment_history: List[Dict]) -> Dict:
        """Identify patterns in assessment practice"""
        return {
            "frequency": "regular" if len(assessment_history) >= 5 else "irregular",
            "consistency": "developing",
            "trend": "improving"
        }
    
    def _generate_assessment_insights(self, score_progression: Dict, type_distribution: Dict, patterns: Dict) -> List[str]:
        """Generate insights from assessment tracking"""
        insights = []
        
        progression = score_progression.get("progression")
        if progression == "improving":
            insights.append("Self-assessment scores are improving over time")
        
        frequency = patterns.get("frequency")
        if frequency == "irregular":
            insights.append("Consider more regular self-assessment practice")
        
        return insights
    
    def _generate_score_based_prompts(self, score: Dict, assessment_type: str) -> List[str]:
        """Generate reflection prompts based on score"""
        level = score.get("level", "fair")
        
        prompts = [
            f"What contributed to your {level} performance?",
            "What strategies worked well for you?",
            "What would you do differently next time?"
        ]
        
        return prompts
    
    def _generate_strength_prompts(self, assessment_result: Dict) -> List[str]:
        """Generate prompts focused on strengths"""
        return [
            "What are your strongest areas?",
            "How can you build on your strengths?",
            "Who can help you leverage your strengths?"
        ]
    
    def _generate_improvement_prompts(self, assessment_result: Dict) -> List[str]:
        """Generate prompts focused on improvements"""
        return [
            "What areas need improvement?",
            "What specific steps will you take to improve?",
            "What resources do you need to support your improvement?"
        ]
    
    def _generate_goal_prompts(self, assessment_result: Dict) -> List[str]:
        """Generate prompts for goal setting"""
        return [
            "What goals will you set based on this assessment?",
            "How will you measure progress toward your goals?",
            "What support do you need to achieve your goals?"
        ]
    
    def _initialize_assessment_templates(self) -> Dict:
        """Initialize assessment templates"""
        return {
            "learning_progress": {
                "questions": 5,
                "scale": "likert_5",
                "time_estimated": "5 minutes"
            },
            "skill_development": {
                "questions": 4,
                "scale": "likert_5",
                "time_estimated": "4 minutes"
            },
            "character_development": {
                "questions": 6,
                "scale": "likert_5",
                "time_estimated": "6 minutes"
            }
        }
    
    def _initialize_rubric_library(self) -> Dict:
        """Initialize rubric library"""
        return {
            "likert_5": {
                "1": "Poor - Minimal demonstration",
                "2": "Fair - Basic demonstration",
                "3": "Good - Adequate demonstration",
                "4": "Very Good - Strong demonstration",
                "5": "Excellent - Outstanding demonstration"
            }
        }
