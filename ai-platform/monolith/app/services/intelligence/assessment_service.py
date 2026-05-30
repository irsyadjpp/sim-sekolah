"""
Assessment Service - Monolith Architecture
Complete assessment functionality using actual business logic
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class AssessmentEngine:
    """Assessment generation engine with complete business logic"""
    
    def __init__(self):
        self.bloom_levels = {
            "remember": "Recall facts and basic concepts",
            "understand": "Explain ideas or concepts",
            "apply": "Use information in new situations",
            "analyze": "Draw connections among ideas",
            "evaluate": "Justify a stand or decision",
            "create": "Produce new or original work"
        }
        self.quality_metrics = {
            "clarity": 0.0,
            "relevance": 0.0,
            "difficulty_match": 0.0,
            "cognitive_alignment": 0.0
        }
    
    def evaluate_competency(self, user_responses: List[Dict], competency: str) -> Dict:
        """Evaluate user competency based on assessment responses"""
        total_score = 0
        total_weight = 0
        
        for response in user_responses:
            score = response.get("score", 0)
            weight = response.get("weight", 1.0)
            total_score += score * weight
            total_weight += weight
        
        competency_score = total_score / total_weight if total_weight > 0 else 0.0
        
        # Determine competency level
        if competency_score >= 0.9:
            level = "expert"
        elif competency_score >= 0.7:
            level = "proficient"
        elif competency_score >= 0.5:
            level = "developing"
        else:
            level = "beginner"
        
        # Generate feedback
        feedback = self._generate_competency_feedback(level, competency_score)
        
        return {
            "competency": competency,
            "score": competency_score,
            "level": level,
            "feedback": feedback,
            "total_responses": len(user_responses)
        }
    
    def validate_assessment_quality(self, assessment: Dict) -> Dict:
        """Validate quality of generated assessment"""
        questions = assessment.get("questions", [])
        
        quality_scores = {
            "clarity": self._evaluate_clarity(questions),
            "relevance": self._evaluate_relevance(questions, assessment.get("topic", "")),
            "difficulty_match": self._evaluate_difficulty_match(questions, assessment.get("difficulty", "medium")),
            "cognitive_alignment": self._evaluate_cognitive_alignment(questions, assessment.get("cognitive_level", ""))
        }
        
        overall_quality = sum(quality_scores.values()) / len(quality_scores)
        
        # Generate improvement recommendations
        recommendations = self._generate_quality_recommendations(quality_scores)
        
        return {
            "overall_quality": overall_quality,
            "quality_scores": quality_scores,
            "is_acceptable": overall_quality >= 0.7,
            "recommendations": recommendations
        }
    
    def _generate_competency_feedback(self, level: str, score: float) -> List[str]:
        """Generate feedback based on competency level"""
        feedback_map = {
            "expert": [
                "Excellent mastery demonstrated",
                "Consider advanced challenges",
                "Potential for peer mentoring"
            ],
            "proficient": [
                "Strong understanding shown",
                "Ready for complex applications",
                "Consolidate with varied practice"
            ],
            "developing": [
                "Good progress being made",
                "Focus on foundational concepts",
                "Additional practice recommended"
            ],
            "beginner": [
                "Building foundational understanding",
                "Start with basic concepts",
                "Guided practice recommended"
            ]
        }
        return feedback_map.get(level, [])
    
    def _evaluate_clarity(self, questions: List[Dict]) -> float:
        """Evaluate question clarity"""
        clarity_score = 0.0
        
        for question in questions:
            question_text = question.get("question", "")
            
            # Check for clear question structure
            if len(question_text.split()) >= 5:  # Minimum word count
                clarity_score += 0.2
            
            # Check for absence of ambiguous terms
            ambiguous_terms = ["maybe", "might", "possibly", "sort of"]
            if not any(term in question_text.lower() for term in ambiguous_terms):
                clarity_score += 0.3
            
            # Check for specific context
            if "?" in question_text or "." in question_text:
                clarity_score += 0.5
        
        return min(clarity_score / len(questions), 1.0) if questions else 0.0
    
    def _evaluate_relevance(self, questions: List[Dict], topic: str) -> float:
        """Evaluate question relevance to topic"""
        if not topic:
            return 0.5  # Neutral score if no topic specified
        
        relevance_score = 0.0
        topic_lower = topic.lower()
        
        for question in questions:
            question_text = question.get("question", "").lower()
            
            # Check for topic mentions
            if topic_lower in question_text:
                relevance_score += 0.5
            
            # Check for related keywords (simplified)
            topic_words = topic_lower.split()
            if any(word in question_text for word in topic_words):
                relevance_score += 0.3
            
            # Check for conceptual relevance
            if len(question_text) > 20:  # Substantial content
                relevance_score += 0.2
        
        return min(relevance_score / len(questions), 1.0) if questions else 0.0
    
    def _evaluate_difficulty_match(self, questions: List[Dict], target_difficulty: str) -> float:
        """Evaluate if questions match target difficulty"""
        difficulty_map = {"easy": 1, "medium": 2, "hard": 3}
        target_level = difficulty_map.get(target_difficulty, 2)
        
        match_score = 0.0
        
        for question in questions:
            question_difficulty = question.get("difficulty", "medium")
            question_level = difficulty_map.get(question_difficulty, 2)
            
            # Calculate closeness to target difficulty
            diff = abs(question_level - target_level)
            if diff == 0:
                match_score += 1.0
            elif diff == 1:
                match_score += 0.5
            else:
                match_score += 0.2
        
        return match_score / len(questions) if questions else 0.0
    
    def _evaluate_cognitive_alignment(self, questions: List[Dict], target_level: str) -> float:
        """Evaluate alignment with cognitive level"""
        cognitive_verbs = {
            "remember": ["define", "list", "identify", "recall"],
            "understand": ["explain", "describe", "summarize", "interpret"],
            "apply": ["apply", "use", "implement", "execute"],
            "analyze": ["analyze", "examine", "compare", "differentiate"],
            "evaluate": ["evaluate", "assess", "judge", "critique"],
            "create": ["create", "design", "develop", "construct"]
        }
        
        target_verbs = cognitive_verbs.get(target_level, [])
        alignment_score = 0.0
        
        for question in questions:
            question_text = question.get("question", "").lower()
            
            if target_verbs:
                verb_match = any(verb in question_text for verb in target_verbs)
                alignment_score += 1.0 if verb_match else 0.3
            else:
                alignment_score += 0.5  # Neutral if no target specified
        
        return alignment_score / len(questions) if questions else 0.0
    
    def _generate_quality_recommendations(self, quality_scores: Dict) -> List[str]:
        """Generate recommendations to improve assessment quality"""
        recommendations = []
        
        if quality_scores["clarity"] < 0.7:
            recommendations.append("Improve question clarity by reducing ambiguity")
        
        if quality_scores["relevance"] < 0.7:
            recommendations.append("Ensure questions directly relate to the topic")
        
        if quality_scores["difficulty_match"] < 0.7:
            recommendations.append("Adjust question difficulty to match target level")
        
        if quality_scores["cognitive_alignment"] < 0.7:
            recommendations.append("Align questions with target cognitive level")
        
        return recommendations if recommendations else ["Assessment quality is acceptable"]
    
    def generate_assessment(self, topic: str, competency: str, grade: str, 
                           assessment_type: str, question_count: int = 5, 
                           difficulty: str = "medium") -> Dict:
        """Generate assessment questions"""
        questions = []
        
        for i in range(question_count):
            question = self._generate_question(topic, competency, difficulty, i + 1)
            questions.append(question)
        
        # Generate rubric if formative
        rubric = None
        if assessment_type == "formative":
            rubric = self._generate_rubric(assessment_type, ["accuracy", "completeness", "understanding"])
        
        return {
            "questions": questions,
            "rubric": rubric,
            "metadata": {
                "topic": topic,
                "competency": competency,
                "grade": grade,
                "assessment_type": assessment_type,
                "difficulty": difficulty,
                "total_questions": len(questions)
            }
        }
    
    def generate_hots_questions(self, topic: str, competency: str, 
                               cognitive_level: str, question_count: int = 3) -> Dict:
        """Generate HOTS (Higher Order Thinking Skills) questions"""
        questions = []
        
        for i in range(question_count):
            question = self._generate_hots_question(topic, competency, cognitive_level, i + 1)
            questions.append(question)
        
        return {
            "questions": questions,
            "metadata": {
                "topic": topic,
                "competency": competency,
                "cognitive_level": cognitive_level,
                "total_questions": len(questions),
                "bloom_description": self.bloom_levels.get(cognitive_level, "")
            }
        }
    
    def generate_rubric(self, assessment_type: str, criteria: List[str], 
                       performance_levels: int = 4) -> Dict:
        """Generate assessment rubric"""
        rubric = self._generate_rubric(assessment_type, criteria, performance_levels)
        
        return {
            "rubric": rubric,
            "metadata": {
                "assessment_type": assessment_type,
                "criteria_count": len(criteria),
                "performance_levels": performance_levels
            }
        }
    
    def _generate_question(self, topic: str, competency: str, difficulty: str, num: int) -> Dict:
        """Generate a single question"""
        templates = {
            "easy": [
                f"What is {topic}?",
                f"Define {competency} in the context of {topic}.",
                f"List the main features of {topic}."
            ],
            "medium": [
                f"Explain how {topic} relates to {competency}.",
                f"Describe the process of {topic}.",
                f"Compare and contrast different aspects of {topic}."
            ],
            "hard": [
                f"Analyze the impact of {topic} on {competency}.",
                f"Evaluate the effectiveness of {topic} in real-world scenarios.",
                f"Create a solution for a problem related to {topic}."
            ]
        }
        
        template = templates.get(difficulty, templates["medium"])[num % len(templates[difficulty])]
        
        return {
            "id": f"q{num}",
            "question": template,
            "type": "open-ended",
            "difficulty": difficulty,
            "points": 10 if difficulty == "easy" else 15 if difficulty == "medium" else 20
        }
    
    def _generate_hots_question(self, topic: str, competency: str, cognitive_level: str, num: int) -> Dict:
        """Generate a HOTS question"""
        templates = {
            "analyze": [
                f"Analyze the relationship between {topic} and {competency}.",
                f"Break down the components of {topic} and explain their interactions.",
                f"Examine the patterns in {topic} and draw conclusions."
            ],
            "evaluate": [
                f"Evaluate the importance of {topic} in achieving {competency}.",
                f"Assess the strengths and weaknesses of {topic}.",
                f"Judge the effectiveness of {topic} based on given criteria."
            ],
            "create": [
                f"Design a new approach to {topic} that improves {competency}.",
                f"Create a plan to implement {topic} in a real-world scenario.",
                f"Propose an innovative solution for challenges related to {topic}."
            ]
        }
        
        template = templates.get(cognitive_level, templates["analyze"])[num % len(templates[cognitive_level])]
        
        return {
            "id": f"hots{num}",
            "question": template,
            "type": "higher-order",
            "cognitive_level": cognitive_level,
            "points": 20
        }
    
    def _generate_rubric(self, assessment_type: str, criteria: List[str], levels: int) -> Dict:
        """Generate rubric"""
        level_names = ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsatisfactory"][:levels]
        level_scores = [100 - (i * (100 // levels)) for i in range(levels)]
        
        rubric = {
            "criteria": []
        }
        
        for criterion in criteria:
            criterion_rubric = {
                "name": criterion,
                "levels": []
            }
            
            for i, (name, score) in enumerate(zip(level_names, level_scores)):
                criterion_rubric["levels"].append({
                    "name": name,
                    "score": score,
                    "description": f"{name} performance in {criterion}"
                })
            
            rubric["criteria"].append(criterion_rubric)
        
        return rubric


class AssessmentService:
    """Assessment service with complete business logic"""
    
    def __init__(self):
        """Initialize assessment service with actual engine"""
        self.initialized = False
        self.assessment_engine = AssessmentEngine()
    
    def initialize(self):
        """Initialize assessment service"""
        try:
            logger.info("Initializing Assessment Service with actual business logic")
            self.initialized = True
            logger.info("Assessment Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Assessment Service: {e}")
            raise
    
    def generate_assessment(self, topic: str, competency: str, grade: str, 
                           assessment_type: str, question_count: int = 5, 
                           difficulty: str = "medium") -> Dict[str, Any]:
        """Generate assessment questions"""
        return self.assessment_engine.generate_assessment(topic, competency, grade, assessment_type, question_count, difficulty)
    
    def generate_hots_questions(self, topic: str, competency: str, 
                               cognitive_level: str, question_count: int = 3) -> Dict[str, Any]:
        """Generate HOTS questions"""
        return self.assessment_engine.generate_hots_questions(topic, competency, cognitive_level, question_count)
    
    def generate_rubric(self, assessment_type: str, criteria: List[str], 
                       performance_levels: int = 4) -> Dict[str, Any]:
        """Generate assessment rubric"""
        return self.assessment_engine.generate_rubric(assessment_type, criteria, performance_levels)
    
    def evaluate_competency(self, user_responses: List[Dict], competency: str) -> Dict[str, Any]:
        """Evaluate user competency based on assessment responses"""
        return self.assessment_engine.evaluate_competency(user_responses, competency)
    
    def validate_assessment_quality(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Validate quality of generated assessment"""
        return self.assessment_engine.validate_assessment_quality(assessment)
    
    def get_bloom_levels(self) -> Dict[str, str]:
        """Get Bloom's taxonomy levels"""
        return self.assessment_engine.bloom_levels
    
    def health(self) -> Dict[str, Any]:
        """Health check for assessment service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "assessment_service",
            "architecture": "monolith",
            "components": {
                "assessment_engine": "ready"
            }
        }
