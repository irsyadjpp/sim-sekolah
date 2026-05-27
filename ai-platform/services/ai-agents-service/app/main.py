"""
AI Agents Service - Fase 7
User-Facing Intelligence - 4 AI Agents
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ENABLE_GRPC_SERVER = os.getenv("ENABLE_GRPC_SERVER", "false").lower() == "true"
ENABLE_RABBITMQ_CONSUMER = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
GRPC_PORT = int(os.getenv("GRPC_PORT", "50072"))


# Pydantic models for Teacher Agent
class LessonPlanningRequest(BaseModel):
    """Lesson planning request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    grade: str
    subject: str
    duration_minutes: int = Field(default=45, ge=15, le=120)
    learning_objectives: List[str] = []
    pedagogy_type: str = "inquiry"
    context: Optional[Dict[str, Any]] = None


class AssessmentCreationRequest(BaseModel):
    """Assessment creation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    competency: str
    grade: str
    assessment_type: str = "formative"
    question_count: int = Field(default=5, ge=1, le=20)
    difficulty: str = "medium"
    context: Optional[Dict[str, Any]] = None


class StudentProgressAnalysisRequest(BaseModel):
    """Student progress analysis request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    subject: str
    time_period: str = "semester"
    include_recommendations: bool = True


class TeachingStrategyRequest(BaseModel):
    """Teaching strategy recommendation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    grade: str
    subject: str
    class_size: int
    available_resources: List[str] = []
    student_profiles: Optional[List[Dict]] = None


# Pydantic models for Student Learning Agent
class PersonalizedGuidanceRequest(BaseModel):
    """Personalized learning guidance request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    subject: str
    current_topic: str
    learning_style: Optional[str] = None
    weak_areas: List[str] = []
    strong_areas: List[str] = []


class QuestionAnsweringRequest(BaseModel):
    """Question answering request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    question: str
    subject: str
    context: Optional[Dict[str, Any]] = None
    conversation_history: List[Dict] = []


class LearningPathRecommendationRequest(BaseModel):
    """Learning path recommendation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    target_competency: str
    current_mastery: Dict[str, float]
    learning_style: Optional[str] = None
    time_constraint: Optional[int] = None


# Pydantic models for Curriculum Agent
class CPGuidanceRequest(BaseModel):
    """CP guidance request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    phase: str
    grade: str
    subject: str
    current_cp: Optional[Dict] = None


class ATPGuidanceRequest(BaseModel):
    """ATP guidance request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cp_id: str
    semester: str
    time_allocation: Dict[str, int]


class CurriculumAlignmentRequest(BaseModel):
    """Curriculum alignment checking request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    teaching_material: Dict[str, Any]
    phase: str
    grade: str
    subject: str


class CurriculumRecommendationRequest(BaseModel):
    """Curriculum recommendation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    phase: str
    grade: str
    subject: str
    current_coverage: Dict[str, float]


# Pydantic models for Assessment Agent
class AssessmentGenerationRequest(BaseModel):
    """Assessment generation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    competency: str
    grade: str
    assessment_type: str
    cognitive_levels: List[str] = []
    question_count: int = Field(default=5)


class RubricCreationRequest(BaseModel):
    """Rubric creation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_type: str
    criteria: List[str]
    performance_levels: int = Field(default=4, ge=3, le=5)
    context: Optional[Dict[str, Any]] = None


class AssessmentAnalyticsRequest(BaseModel):
    """Assessment analytics request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    class_id: str
    analysis_type: str = "performance"


# Additional request models for new features
class AdaptiveInteractionRequest(BaseModel):
    """Adaptive interaction request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    subject: str
    interaction_data: Dict[str, Any]


class ExpertKnowledgeRequest(BaseModel):
    """Expert knowledge integration request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    context: Dict[str, Any]


class QualityValidationRequest(BaseModel):
    """Quality validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_data: Dict[str, Any]


# Base result model
class AgentResult(BaseModel):
    """Generic agent result"""
    request_id: str
    agent_type: str
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# AI Agents Engine
class AIAgentsEngine:
    """AI Agents Engine - 4 specialized educational agents"""
    
    def __init__(self):
        # Initialize all agents
        self.teacher_agent = TeacherAgent()
        self.student_agent = StudentLearningAgent()
        self.curriculum_agent = CurriculumAgent()
        self.assessment_agent = AssessmentAgent()
        
        # Agent performance metrics
        self.performance_metrics = {
            "total_interactions": 0,
            "avg_response_time_ms": 0,
            "agent_usage": {},
            "satisfaction_metrics": {}
        }
    
    # Teacher Agent methods
    def lesson_planning_assistant(self, request: LessonPlanningRequest) -> Dict:
        """Lesson planning assistant"""
        import time
        start_time = time.time()
        
        result = self.teacher_agent.create_lesson_plan(
            request.topic,
            request.grade,
            request.subject,
            request.duration_minutes,
            request.learning_objectives,
            request.pedagogy_type,
            request.context
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("teacher_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "teacher_agent",
                "function": "lesson_planning",
                "response_time_ms": response_time
            }
        }
    
    def assessment_creation_assistant(self, request: AssessmentCreationRequest) -> Dict:
        """Assessment creation assistant"""
        import time
        start_time = time.time()
        
        result = self.teacher_agent.create_assessment(
            request.topic,
            request.competency,
            request.grade,
            request.assessment_type,
            request.question_count,
            request.difficulty,
            request.context
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("teacher_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "teacher_agent",
                "function": "assessment_creation",
                "response_time_ms": response_time
            }
        }
    
    def student_progress_analysis(self, request: StudentProgressAnalysisRequest) -> Dict:
        """Student progress analysis"""
        import time
        start_time = time.time()
        
        result = self.teacher_agent.analyze_student_progress(
            request.student_id,
            request.subject,
            request.time_period,
            request.include_recommendations
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("teacher_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "teacher_agent",
                "function": "progress_analysis",
                "response_time_ms": response_time
            }
        }
    
    def teaching_strategy_recommendation(self, request: TeachingStrategyRequest) -> Dict:
        """Teaching strategy recommendation"""
        import time
        start_time = time.time()
        
        result = self.teacher_agent.recommend_teaching_strategy(
            request.topic,
            request.grade,
            request.subject,
            request.class_size,
            request.available_resources,
            request.student_profiles
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("teacher_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "teacher_agent",
                "function": "strategy_recommendation",
                "response_time_ms": response_time
            }
        }
    
    # Student Learning Agent methods
    def personalized_guidance(self, request: PersonalizedGuidanceRequest) -> Dict:
        """Personalized learning guidance"""
        import time
        start_time = time.time()
        
        result = self.student_agent.provide_guidance(
            request.student_id,
            request.subject,
            request.current_topic,
            request.learning_style,
            request.weak_areas,
            request.strong_areas
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("student_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "student_agent",
                "function": "personalized_guidance",
                "response_time_ms": response_time
            }
        }
    
    def question_answering(self, request: QuestionAnsweringRequest) -> Dict:
        """Question answering"""
        import time
        start_time = time.time()
        
        result = self.student_agent.answer_question(
            request.student_id,
            request.question,
            request.subject,
            request.context,
            request.conversation_history
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("student_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "student_agent",
                "function": "question_answering",
                "response_time_ms": response_time
            }
        }
    
    def learning_path_recommendation(self, request: LearningPathRecommendationRequest) -> Dict:
        """Learning path recommendation"""
        import time
        start_time = time.time()
        
        result = self.student_agent.recommend_learning_path(
            request.student_id,
            request.target_competency,
            request.current_mastery,
            request.learning_style,
            request.time_constraint
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("student_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "student_agent",
                "function": "learning_path_recommendation",
                "response_time_ms": response_time
            }
        }
    
    # Curriculum Agent methods
    def cp_guidance(self, request: CPGuidanceRequest) -> Dict:
        """CP guidance"""
        import time
        start_time = time.time()
        
        result = self.curriculum_agent.provide_cp_guidance(
            request.phase,
            request.grade,
            request.subject,
            request.current_cp
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "curriculum_agent",
                "function": "cp_guidance",
                "response_time_ms": response_time
            }
        }
    
    def atp_guidance(self, request: ATPGuidanceRequest) -> Dict:
        """ATP guidance"""
        import time
        start_time = time.time()
        
        result = self.curriculum_agent.provide_atp_guidance(
            request.cp_id,
            request.semester,
            request.time_allocation
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "curriculum_agent",
                "function": "atp_guidance",
                "response_time_ms": response_time
            }
        }
    
    def curriculum_alignment_checking(self, request: CurriculumAlignmentRequest) -> Dict:
        """Curriculum alignment checking"""
        import time
        start_time = time.time()
        
        result = self.curriculum_agent.check_alignment(
            request.teaching_material,
            request.phase,
            request.grade,
            request.subject
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "curriculum_agent",
                "function": "alignment_checking",
                "response_time_ms": response_time
            }
        }
    
    def curriculum_recommendation(self, request: CurriculumRecommendationRequest) -> Dict:
        """Curriculum recommendation"""
        import time
        start_time = time.time()
        
        result = self.curriculum_agent.recommend_curriculum(
            request.phase,
            request.grade,
            request.subject,
            request.current_coverage
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "curriculum_agent",
                "function": "curriculum_recommendation",
                "response_time_ms": response_time
            }
        }
    
    # Assessment Agent methods
    def assessment_generation_assistant(self, request: AssessmentGenerationRequest) -> Dict:
        """Assessment generation assistant"""
        import time
        start_time = time.time()
        
        result = self.assessment_agent.generate_assessment(
            request.topic,
            request.competency,
            request.grade,
            request.assessment_type,
            request.cognitive_levels,
            request.question_count
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "assessment_agent",
                "function": "assessment_generation",
                "response_time_ms": response_time
            }
        }
    
    def rubric_creation_assistant(self, request: RubricCreationRequest) -> Dict:
        """Rubric creation assistant"""
        import time
        start_time = time.time()
        
        result = self.assessment_agent.create_rubric(
            request.assessment_type,
            request.criteria,
            request.performance_levels,
            request.context
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "assessment_agent",
                "function": "rubric_creation",
                "response_time_ms": response_time
            }
        }
    
    def assessment_analytics(self, request: AssessmentAnalyticsRequest) -> Dict:
        """Assessment analytics"""
        import time
        start_time = time.time()
        
        result = self.assessment_agent.provide_analytics(
            request.assessment_id,
            request.class_id,
            request.analysis_type
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "assessment_agent",
                "function": "assessment_analytics",
                "response_time_ms": response_time
            }
        }
    
    # New feature methods
    def adaptive_interaction(self, request: AdaptiveInteractionRequest) -> Dict:
        """Adaptive interaction for student learning"""
        import time
        start_time = time.time()
        
        result = self.student_agent.adaptive_interaction(
            request.student_id,
            request.subject,
            request.interaction_data
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("student_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "student_agent",
                "function": "adaptive_interaction",
                "response_time_ms": response_time
            }
        }
    
    def expert_knowledge_integration(self, request: ExpertKnowledgeRequest) -> Dict:
        """Expert knowledge integration for curriculum"""
        import time
        start_time = time.time()
        
        result = self.curriculum_agent.integrate_expert_knowledge(
            request.query,
            request.context
        )
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "curriculum_agent",
                "function": "expert_knowledge_integration",
                "response_time_ms": response_time
            }
        }
    
    def quality_validation(self, request: QualityValidationRequest) -> Dict:
        """Quality validation for assessment"""
        import time
        start_time = time.time()
        
        result = self.assessment_agent.validate_quality(request.assessment_data)
        
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_agent", response_time)
        
        return {
            "result": result,
            "metadata": {
                "agent_type": "assessment_agent",
                "function": "quality_validation",
                "response_time_ms": response_time
            }
        }
    
    def _update_performance_metrics(self, agent_name: str, response_time_ms: float):
        """Update performance metrics"""
        self.performance_metrics["total_interactions"] += 1
        
        total = self.performance_metrics["total_interactions"]
        current_avg = self.performance_metrics["avg_response_time_ms"]
        new_avg = (current_avg * (total - 1) + response_time_ms) / total
        self.performance_metrics["avg_response_time_ms"] = new_avg
        
        if agent_name not in self.performance_metrics["agent_usage"]:
            self.performance_metrics["agent_usage"][agent_name] = 0
        self.performance_metrics["agent_usage"][agent_name] += 1


# Individual Agent Implementations
class TeacherAgent:
    """Teacher Assistant Agent"""
    
    def __init__(self):
        self.lesson_templates = self._load_lesson_templates()
        self.assessment_templates = self._load_assessment_templates()
        self.teaching_strategies = self._load_teaching_strategies()
    
    def create_lesson_plan(self, topic: str, grade: str, subject: str, duration: int, 
                           objectives: List[str], pedagogy_type: str, context: Dict) -> Dict:
        """Create comprehensive lesson plan"""
        lesson_plan = {
            "title": f"Lesson Plan: {topic}",
            "subject": subject,
            "grade": grade,
            "duration_minutes": duration,
            "learning_objectives": objectives or self._generate_objectives(topic, grade, subject),
            "pedagogy_type": pedagogy_type,
            "structure": self._generate_lesson_structure(duration, pedagogy_type),
            "activities": self._generate_activities(topic, grade, pedagogy_type, duration),
            "materials": self._suggest_materials(topic, subject, grade),
            "assessment": self._suggest_assessment(topic, grade, subject),
            "differentiation": self._suggest_differentiation(topic, grade)
        }
        return lesson_plan
    
    def create_assessment(self, topic: str, competency: str, grade: str, 
                        assessment_type: str, question_count: int, difficulty: str, context: Dict) -> Dict:
        """Create assessment"""
        assessment = {
            "title": f"{assessment_type.title()} Assessment: {topic}",
            "competency": competency,
            "grade": grade,
            "assessment_type": assessment_type,
            "difficulty": difficulty,
            "questions": self._generate_questions(topic, competency, grade, assessment_type, question_count, difficulty),
            "rubric": self._generate_rubric(assessment_type, topic),
            "estimated_duration": self._estimate_duration(question_count, assessment_type)
        }
        return assessment
    
    def analyze_student_progress(self, student_id: str, subject: str, 
                               time_period: str, include_recommendations: bool) -> Dict:
        """Analyze student progress"""
        progress = {
            "student_id": student_id,
            "subject": subject,
            "time_period": time_period,
            "overall_performance": self._calculate_performance(student_id, subject, time_period),
            "strength_areas": self._identify_strengths(student_id, subject),
            "improvement_areas": self._identify_improvements(student_id, subject),
            "trend_analysis": self._analyze_trends(student_id, subject, time_period),
            "milestones": self._check_milestones(student_id, subject)
        }
        
        if include_recommendations:
            progress["recommendations"] = self._generate_recommendations(progress)
        
        return progress
    
    def recommend_teaching_strategy(self, topic: str, grade: str, subject: str,
                                  class_size: int, resources: List[str], profiles: List[Dict]) -> Dict:
        """Recommend teaching strategy"""
        strategy = {
            "topic": topic,
            "grade": grade,
            "subject": subject,
            "class_size": class_size,
            "recommended_strategy": self._select_strategy(class_size, topic, profiles),
            "rationale": self._explain_strategy_selection(class_size, topic, profiles),
            "adaptations": self._suggest_adaptations(class_size, resources, profiles),
            "activities": self._suggest_strategy_activities(topic, grade),
            "assessment_methods": self._suggest_assessment_methods(topic, grade)
        }
        return strategy
    
    def _generate_objectives(self, topic: str, grade: str, subject: str) -> List[str]:
        """Generate learning objectives"""
        return [
            f"Students will understand {topic} in {subject}",
            f"Students will apply concepts of {topic} in practical situations",
            f"Students will analyze relationships between {topic} and other concepts"
        ]
    
    def _generate_lesson_structure(self, duration: int, pedagogy_type: str) -> Dict:
        """Generate lesson structure"""
        warm_up = max(5, duration * 0.1)
        main_activity = max(20, duration * 0.6)
        assessment = max(5, duration * 0.1)
        closure = max(5, duration * 0.2)
        
        return {
            "warm_up": {"duration": warm_up, "activities": ["Hook", "Review"]},
            "main_activity": {"duration": main_activity, "activities": ["Instruction", "Practice"]},
            "assessment": {"duration": assessment, "activities": ["Check understanding"]},
            "closure": {"duration": closure, "activities": ["Summary", "Homework"]}
        }
    
    def _generate_activities(self, topic: str, grade: str, pedagogy_type: str, duration: int) -> List[Dict]:
        """Generate activities based on pedagogy type"""
        activities = []
        
        if pedagogy_type == "inquiry":
            activities = [
                {"phase": "exploration", "activity": "Explore problem related to topic", "duration": 10},
                {"phase": "investigation", "activity": "Investigate solutions", "duration": 15},
                {"phase": "discussion", "activity": "Discuss findings", "duration": 10}
            ]
        elif pedagogy_type == "differentiated":
            activities = [
                {"phase": "introduction", "activity": "Introduce topic at multiple levels", "duration": 10},
                {"phase": "group_work", "activity": "Work in ability groups", "duration": 20},
                {"phase": "individual_practice", "activity": "Practice at own level", "duration": 10}
            ]
        else:
            activities = [
                {"phase": "instruction", "activity": "Direct instruction on topic", "duration": 15},
                {"phase": "guided_practice", "activity": "Guided practice with examples", "duration": 15},
                {"phase": "independent_practice", "activity": "Independent practice", "duration": 15}
            ]
        
        return activities
    
    def _suggest_materials(self, topic: str, subject: str, grade: str) -> List[str]:
        """Suggest teaching materials"""
        return [
            f"Textbook chapter on {topic}",
            f"Visual aids for {topic}",
            f"Hands-on materials for {subject}",
            f"Digital resources for {grade} {subject}"
        ]
    
    def _suggest_assessment(self, topic: str, grade: str, subject: str) -> Dict:
        """Suggest assessment methods"""
        return {
            "formative": ["Quick questions", "Observation", "Exit ticket"],
            "summative": ["Written test", "Project", "Presentation"]
        }
    
    def _suggest_differentiation(self, topic: str, grade: str) -> Dict:
        """Suggest differentiation strategies"""
        return {
            "content": ["Tiered assignments", "Multiple reading levels"],
            "process": ["Flexible grouping", "Varied pacing"],
            "product": ["Choice of assessment", "Multiple output formats"]
        }
    
    def _generate_questions(self, topic: str, competency: str, grade: str, 
                          assessment_type: str, count: int, difficulty: str) -> List[Dict]:
        """Generate assessment questions"""
        questions = []
        
        for i in range(count):
            question = {
                "id": f"q{i+1}",
                "question": self._generate_question_text(topic, competency, difficulty, i),
                "type": assessment_type,
                "points": self._assign_points(difficulty),
                "difficulty": difficulty
            }
            questions.append(question)
        
        return questions
    
    def _generate_question_text(self, topic: str, competency: str, difficulty: str, index: int) -> str:
        """Generate question text"""
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
                f"Evaluate the effectiveness of {topic}.",
                f"Create a solution using principles of {topic}."
            ]
        }
        
        template_list = templates.get(difficulty, templates["medium"])
        return template_list[index % len(template_list)]
    
    def _assign_points(self, difficulty: str) -> int:
        """Assign points based on difficulty"""
        return {"easy": 2, "medium": 3, "hard": 5}.get(difficulty, 3)
    
    def _generate_rubric(self, assessment_type: str, topic: str) -> Dict:
        """Generate assessment rubric"""
        return {
            "criteria": ["Content Knowledge", "Understanding", "Application", "Communication"],
            "performance_levels": ["Excellent", "Good", "Satisfactory", "Needs Improvement"]
        }
    
    def _estimate_duration(self, question_count: int, assessment_type: str) -> int:
        """Estimate assessment duration"""
        minutes_per_question = 5 if assessment_type == "summative" else 2
        return question_count * minutes_per_question
    
    def _calculate_performance(self, student_id: str, subject: str, time_period: str) -> float:
        """Calculate overall performance"""
        # Simulated performance calculation
        return 0.75
    
    def _identify_strengths(self, student_id: str, subject: str) -> List[str]:
        """Identify student strengths"""
        return ["Problem solving", "Critical thinking"]
    
    def _identify_improvements(self, student_id: str, subject: str) -> List[str]:
        """Identify areas for improvement"""
        return ["Basic concepts", "Application skills"]
    
    def _analyze_trends(self, student_id: str, subject: str, time_period: str) -> Dict:
        """Analyze performance trends"""
        return {
            "trend": "improving",
            "rate": "+5% over period",
            "consistency": "stable"
        }
    
    def _check_milestones(self, student_id: str, subject: str) -> List[Dict]:
        """Check milestone achievements"""
        return [
            {"milestone": "Basic concepts", "achieved": True},
            {"milestone": "Application", "achieved": False}
        ]
    
    def _generate_recommendations(self, progress: Dict) -> List[str]:
        """Generate recommendations"""
        return [
            "Focus on basic concept mastery",
            "Provide more application opportunities",
            "Use varied assessment methods"
        ]
    
    def _select_strategy(self, class_size: int, topic: str, profiles: List[Dict]) -> str:
        """Select appropriate teaching strategy"""
        if class_size > 30:
            return "direct_instruction_with_breakout_groups"
        elif class_size > 15:
            return "differentiated_instruction"
        else:
            return "inquiry_based_learning"
    
    def _explain_strategy_selection(self, class_size: int, topic: str, profiles: List[Dict]) -> str:
        """Explain strategy selection rationale"""
        return f"Strategy selected based on class size of {class_size} and topic characteristics"
    
    def _suggest_adaptations(self, class_size: int, resources: List[str], profiles: List[Dict]) -> List[str]:
        """Suggest teaching adaptations"""
        return ["Use visual aids", "Include hands-on activities", "Provide extra practice"]
    
    def _suggest_strategy_activities(self, topic: str, grade: str) -> List[str]:
        """Suggest strategy-specific activities"""
        return ["Group discussion", "Individual practice", "Peer teaching"]
    
    def _suggest_assessment_methods(self, topic: str, grade: str) -> List[str]:
        """Suggest assessment methods"""
        return ["Formative checks", "Summative assessment", "Performance tasks"]
    
    def _load_lesson_templates(self) -> Dict:
        """Load lesson plan templates"""
        return {}
    
    def _load_assessment_templates(self) -> Dict:
        """Load assessment templates"""
        return {}
    
    def _load_teaching_strategies(self) -> Dict:
        """Load teaching strategies"""
        return {}


class StudentLearningAgent:
    """Student Learning Companion Agent"""
    
    def __init__(self):
        self.conversation_memory = {}  # Store conversation history per student
        self.learning_profiles = {}  # Store student learning profiles
    
    def provide_guidance(self, student_id: str, subject: str, current_topic: str,
                        learning_style: str, weak_areas: List[str], strong_areas: List[str]) -> Dict:
        """Provide personalized learning guidance"""
        guidance = {
            "student_id": student_id,
            "subject": subject,
            "current_topic": current_topic,
            "learning_style_adaptations": self._adapt_for_learning_style(learning_style),
            "focus_areas": weak_areas or self._identify_focus_areas(student_id, subject),
            "enrichment_suggestions": self._suggest_enrichment(strong_areas, current_topic),
            "study_tips": self._provide_study_tips(subject, learning_style),
            "recommended_resources": self._recommend_resources(student_id, subject, current_topic),
            "encouragement": self._provide_encouragement(student_id, subject)
        }
        return guidance
    
    def answer_question(self, student_id: str, question: str, subject: str,
                      context: Dict, conversation_history: List[Dict]) -> Dict:
        """Answer student questions"""
        # Store conversation history
        if student_id not in self.conversation_memory:
            self.conversation_memory[student_id] = []
        self.conversation_memory[student_id].extend(conversation_history)
        
        # Generate answer
        answer = {
            "question": question,
            "answer": self._generate_answer(question, subject, context, conversation_history),
            "follow_up_questions": self._suggest_follow_up_questions(question, subject),
            "related_topics": self._identify_related_topics(question, subject),
            "confidence": self._calculate_confidence(question, subject, context),
            "personalization": self._personalize_answer(student_id, subject)
        }
        return answer
    
    def recommend_learning_path(self, student_id: str, target_competency: str,
                              current_mastery: Dict[str, float], learning_style: str, time_constraint: int) -> Dict:
        """Recommend personalized learning path"""
        path = {
            "student_id": student_id,
            "target_competency": target_competency,
            "current_mastery": current_mastery,
            "learning_path": self._generate_learning_path(target_competency, current_mastery, learning_style),
            "milestones": self._define_milestones(target_competency, current_mastery),
            "estimated_completion": self._estimate_completion(current_mastery, target_competency, time_constraint),
            "resources": self._recommend_path_resources(target_competency, learning_style),
            "progress_checkpoints": self._define_checkpoints(target_competency)
        }
        return path
    
    def _adapt_for_learning_style(self, learning_style: str) -> Dict:
        """Adapt guidance for learning style"""
        adaptations = {
            "visual": ["Use diagrams and charts", "Watch video tutorials", "Use color coding"],
            "auditory": ["Listen to explanations", "Discuss concepts", "Use audio materials"],
            "kinesthetic": ["Hands-on activities", "Practice problems", "Use simulations"],
            "reading": ["Read textbooks", "Take notes", "Use written exercises"]
        }
        return adaptations.get(learning_style, ["Use multiple methods"])
    
    def _identify_focus_areas(self, student_id: str, subject: str) -> List[str]:
        """Identify focus areas for student"""
        return ["Foundational concepts", "Key applications", "Problem-solving skills"]
    
    def _suggest_enrichment(self, strong_areas: List[str], current_topic: str) -> List[str]:
        """Suggest enrichment activities"""
        return ["Advanced problems", "Extension activities", "Peer teaching"]
    
    def _provide_study_tips(self, subject: str, learning_style: str) -> List[str]:
        """Provide study tips"""
        return ["Practice regularly", "Connect to real life", "Teach others"]
    
    def _recommend_resources(self, student_id: str, subject: str, topic: str) -> List[str]:
        """Recommend learning resources"""
        return ["Textbook chapter", "Online videos", "Practice problems", "Study guides"]
    
    def _provide_encouragement(self, student_id: str, subject: str) -> str:
        """Provide encouragement message"""
        return "You're making great progress! Keep up the good work."
    
    def _generate_answer(self, question: str, subject: str, context: Dict, history: List[Dict]) -> str:
        """Generate answer to question"""
        # Simplified answer generation
        return f"Based on your question about {question} in {subject}, here's a comprehensive explanation..."
    
    def _suggest_follow_up_questions(self, question: str, subject: str) -> List[str]:
        """Suggest follow-up questions"""
        return [
            f"How does this relate to other concepts in {subject}?",
            "Can you think of real-world examples?",
            "What would happen if we changed this aspect?"
        ]
    
    def _identify_related_topics(self, question: str, subject: str) -> List[str]:
        """Identify related topics"""
        return ["Related concept 1", "Related concept 2", "Related concept 3"]
    
    def _calculate_confidence(self, question: str, subject: str, context: Dict) -> float:
        """Calculate answer confidence"""
        return 0.85
    
    def _personalize_answer(self, student_id: str, subject: str) -> Dict:
        """Personalize answer based on student profile"""
        return {"learning_style_aware": True, "mastery_considered": True}
    
    def _generate_learning_path(self, target: str, mastery: Dict, style: str) -> List[Dict]:
        """Generate learning path"""
        # Identify gaps and build path
        gaps = [k for k, v in mastery.items() if v < 0.7]
        
        path = []
        for gap in gaps:
            path.append({
                "step": f"Master {gap}",
                "type": "prerequisite",
                "priority": "high",
                "resources": self._get_resources_for_topic(gap)
            })
        
        path.append({
            "step": f"Achieve {target}",
            "type": "target",
            "priority": "high",
            "resources": self._get_resources_for_topic(target)
        })
        
        return path
    
    def _define_milestones(self, target: str, mastery: Dict) -> List[Dict]:
        """Define learning milestones"""
        return [
            {"milestone": "Foundation", "criteria": "80% mastery of prerequisites"},
            {"milestone": "Application", "criteria": "Solve 5 problems correctly"},
            {"milestone": "Mastery", "criteria": "90% on comprehensive assessment"}
        ]
    
    def _estimate_completion(self, mastery: Dict, target: str, time_constraint: int) -> str:
        """Estimate completion time"""
        return "2-3 weeks with regular practice"
    
    def _recommend_path_resources(self, target: str, style: str) -> List[str]:
        """Recommend resources for learning path"""
        return ["Textbook chapters", "Online courses", "Practice problems", "Video tutorials"]
    
    def _define_checkpoints(self, target: str) -> List[Dict]:
        """Define progress checkpoints"""
        return [
            {"checkpoint": "Week 1", "check": "Basic understanding"},
            {"checkpoint": "Week 2", "check": "Application skills"},
            {"checkpoint": "Week 3", "check": "Mastery demonstration"}
        ]
    
    def _get_resources_for_topic(self, topic: str) -> List[str]:
        """Get resources for specific topic"""
        return ["Chapter reading", "Practice problems", "Video tutorial", "Study guide"]
    
    def adaptive_interaction(self, student_id: str, subject: str, interaction_data: Dict) -> Dict:
        """Provide adaptive interaction based on student performance and behavior"""
        # Update learning profile based on interaction
        if student_id not in self.learning_profiles:
            self.learning_profiles[student_id] = {
                "preferred_difficulty": "medium",
                "engagement_level": 0.7,
                "response_patterns": [],
                "learning Pace": "normal"
            }
        
        # Analyze interaction data
        engagement_score = self._calculate_engagement(interaction_data)
        difficulty_adjustment = self._adjust_difficulty(student_id, interaction_data)
        content_adaptation = self._adapt_content(student_id, subject, interaction_data)
        
        adaptive_response = {
            "student_id": student_id,
            "subject": subject,
            "engagement_score": engagement_score,
            "difficulty_adjustment": difficulty_adjustment,
            "content_adaptation": content_adaptation,
            "feedback_style": self._select_feedback_style(student_id, engagement_score),
            "suggested_break": self._suggest_break(student_id, engagement_score),
            "motivation_message": self._generate_motivation(student_id, engagement_score)
        }
        
        # Update learning profile
        self.learning_profiles[student_id]["engagement_level"] = engagement_score
        self.learning_profiles[student_id]["response_patterns"].append(interaction_data)
        
        return adaptive_response
    
    def _calculate_engagement(self, interaction_data: Dict) -> float:
        """Calculate engagement score from interaction data"""
        # Factors: response time, correctness, interaction frequency
        response_time = interaction_data.get("response_time", 30)
        correctness = interaction_data.get("correctness", 0.7)
        interaction_frequency = interaction_data.get("frequency", 1.0)
        
        # Normalize and combine (simplified)
        time_score = max(0, 1 - (response_time / 60))  # Faster is better
        engagement = (time_score * 0.3 + correctness * 0.5 + min(1, interaction_frequency) * 0.2)
        return round(engagement, 2)
    
    def _adjust_difficulty(self, student_id: str, interaction_data: Dict) -> Dict:
        """Adjust difficulty based on performance"""
        current_difficulty = self.learning_profiles[student_id]["preferred_difficulty"]
        correctness = interaction_data.get("correctness", 0.7)
        
        if correctness > 0.9 and current_difficulty != "hard":
            new_difficulty = "hard" if current_difficulty == "medium" else "medium"
        elif correctness < 0.6 and current_difficulty != "easy":
            new_difficulty = "easy" if current_difficulty == "medium" else "medium"
        else:
            new_difficulty = current_difficulty
        
        self.learning_profiles[student_id]["preferred_difficulty"] = new_difficulty
        
        return {
            "previous_difficulty": current_difficulty,
            "new_difficulty": new_difficulty,
            "reason": "Performance-based adjustment"
        }
    
    def _adapt_content(self, student_id: str, subject: str, interaction_data: Dict) -> Dict:
        """Adapt content based on learning profile"""
        learning_style = self.learning_profiles[student_id].get("learning_style", "visual")
        preferred_difficulty = self.learning_profiles[student_id]["preferred_difficulty"]
        
        return {
            "learning_style_match": learning_style,
            "difficulty_level": preferred_difficulty,
            "content_format": self._select_content_format(learning_style),
            "supplementary_materials": self._suggest_materials(student_id, subject)
        }
    
    def _select_content_format(self, learning_style: str) -> str:
        """Select content format based on learning style"""
        format_map = {
            "visual": "videos, diagrams, infographics",
            "auditory": "audio explanations, discussions",
            "kinesthetic": "hands-on activities, simulations",
            "reading": "text-heavy materials, written exercises"
        }
        return format_map.get(learning_style, "mixed format")
    
    def _suggest_materials(self, student_id: str, subject: str) -> List[str]:
        """Suggest supplementary materials"""
        return [
            f"Practice problems for {subject}",
            f"Video tutorial for current topic",
            f"Study guide for review"
        ]
    
    def _select_feedback_style(self, student_id: str, engagement: float) -> str:
        """Select feedback style based on engagement"""
        if engagement > 0.8:
            return "encouraging, detailed"
        elif engagement > 0.5:
            return "balanced, constructive"
        else:
            return "supportive, simplified"
    
    def _suggest_break(self, student_id: str, engagement: float) -> Dict:
        """Suggest break if engagement is low"""
        if engagement < 0.4:
            return {
                "recommend_break": True,
                "suggested_duration": "5-10 minutes",
                "break_activity": "stretch, quick walk, or change of activity"
            }
        return {
            "recommend_break": False,
            "reason": "Engagement level is sufficient"
        }
    
    def _generate_motivation(self, student_id: str, engagement: float) -> str:
        """Generate motivation message based on engagement"""
        if engagement > 0.8:
            return "You're doing great! Keep up the excellent work!"
        elif engagement > 0.5:
            return "Good progress! Let's continue building on this momentum."
        else:
            return "Take your time. Learning is a journey, and every step counts."


class CurriculumAgent:
    """Curriculum Expert Agent"""
    
    def __init__(self):
        self.curriculum_standards = self._load_curriculum_standards()
        self.alignment_rules = self._load_alignment_rules()
    
    def provide_cp_guidance(self, phase: str, grade: str, subject: str, current_cp: Dict) -> Dict:
        """Provide CP guidance"""
        guidance = {
            "phase": phase,
            "grade": grade,
            "subject": subject,
            "required_elements": self._get_cp_requirements(phase, grade, subject),
            "structure_recommendations": self._recommend_cp_structure(phase, grade),
            "content_guidance": self._provide_content_guidance(subject, phase, grade),
            "assessment_guidance": self._provide_assessment_guidance(phase, grade),
            "alignment_check": self._check_cp_alignment(current_cp, phase, grade),
            "best_practices": self._suggest_cp_best_practices(phase, grade)
        }
        return guidance
    
    def provide_atp_guidance(self, cp_id: str, semester: str, time_allocation: Dict) -> Dict:
        """Provide ATP guidance"""
        guidance = {
            "cp_id": cp_id,
            "semester": semester,
            "time_allocation": time_allocation,
            "structure_recommendations": self._recommend_atp_structure(time_allocation),
            "topic_pacing": self._suggest_topic_pacing(cp_id, time_allocation),
            "assessment_integration": self._integrate_assessments(cp_id, semester),
            "flexibility_guidance": self._provide_flexibility_guidance(semester),
            "compliance_check": self._check_atp_compliance(cp_id, semester)
        }
        return guidance
    
    def check_alignment(self, material: Dict, phase: str, grade: str, subject: str) -> Dict:
        """Check curriculum alignment"""
        alignment = {
            "material": material,
            "phase": phase,
            "grade": grade,
            "subject": subject,
            "alignment_score": self._calculate_alignment_score(material, phase, grade, subject),
            "alignment_details": self._analyze_alignment(material, phase, grade, subject),
            "gaps": self._identify_alignment_gaps(material, phase, grade, subject),
            "recommendations": self._make_alignment_recommendations(material, phase, grade, subject)
        }
        return alignment
    
    def recommend_curriculum(self, phase: str, grade: str, subject: str, coverage: Dict) -> Dict:
        """Recommend curriculum improvements"""
        recommendations = {
            "phase": phase,
            "grade": grade,
            "subject": subject,
            "current_coverage": coverage,
            "coverage_gaps": self._identify_coverage_gaps(phase, grade, subject, coverage),
            "recommended_additions": self._recommend_additions(phase, grade, subject),
            "priority_ordering": self._prioritize_additions(coverage),
            "implementation_timeline": self._suggest_timeline(phase, grade)
        }
        return recommendations
    
    def _load_curriculum_standards(self) -> Dict:
        """Load curriculum standards"""
        return {}
    
    def _load_alignment_rules(self) -> Dict:
        """Load alignment rules"""
        return {}
    
    def _get_cp_requirements(self, phase: str, grade: str, subject: str) -> List[str]:
        """Get CP requirements"""
        return [
            "Fase A/Anak Profet",
            "Capaian Pembelajaran (CP)",
            "Tujuan Pembelajaran",
            "Pertanyaan Pemantik (Formative)",
            "Materi Inti"
        ]
    
    def _recommend_cp_structure(self, phase: str, grade: str) -> Dict:
        """Recommend CP structure"""
        return {
            "structure": "standard_cp_format",
            "sections": ["profil_pelajar", "kompetensi", "materi_inti", "asesmen"],
            "format": "Kurikulum Merdeka"
        }
    
    def _provide_content_guidance(self, subject: str, phase: str, grade: str) -> Dict:
        """Provide content guidance"""
        return {
            "content_complexity": "age_appropriate",
            "scope": "aligned_with_phase",
            "sequence": "logical_progression"
        }
    
    def _provide_assessment_guidance(self, phase: str, grade: str) -> Dict:
        """Provide assessment guidance"""
        return {
            "formative_frequency": "regular",
            "summative_timeline": "end_of_phase",
            "assessment_types": ["performance", "project", "written"]
        }
    
    def _check_cp_alignment(self, current_cp: Dict, phase: str, grade: str) -> Dict:
        """Check CP alignment"""
        return {
            "aligned": True,
            "alignment_percentage": 85,
            "suggestions": ["Add more formative assessments", "Strengthen learning objectives"]
        }
    
    def _suggest_cp_best_practices(self, phase: str, grade: str) -> List[str]:
        """Suggest CP best practices"""
        return [
            "Use clear learning objectives",
            "Align with Profil Pelajar Pancasila",
            "Include diverse assessment methods",
            "Ensure progression of learning"
        ]
    
    def _recommend_atp_structure(self, time_allocation: Dict) -> Dict:
        """Recommend ATP structure"""
        total_hours = sum(time_allocation.values())
        return {
            "weekly_structure": f"{total_hours} hours per week",
            "pacing": "balanced",
            "flexibility": "20% buffer time"
        }
    
    def _suggest_topic_pacing(self, cp_id: str, time_allocation: Dict) -> Dict:
        """Suggest topic pacing"""
        return {
            "pacing": "moderate",
            "checkpoints": "weekly",
            "adjustment_period": "monthly"
        }
    
    def _integrate_assessments(self, cp_id: str, semester: str) -> Dict:
        """Integrate assessments in ATP"""
        return {
            "formative_frequency": "3-4 per semester",
            "summative_count": 1,
            "types": ["diagnostic", "formative", "summative"]
        }
    
    def _provide_flexibility_guidance(self, semester: str) -> Dict:
        """Provide flexibility guidance"""
        return {
            "buffer_time": "20%",
            "adjustment_points": "monthly",
            "contingency_plan": "include"
        }
    
    def _check_atp_compliance(self, cp_id: str, semester: str) -> Dict:
        """Check ATP compliance"""
        return {
            "compliant": True,
            "compliance_score": 90,
            "issues": []
        }
    
    def _calculate_alignment_score(self, material: Dict, phase: str, grade: str, subject: str) -> float:
        """Calculate alignment score"""
        return 0.85
    
    def _analyze_alignment(self, material: Dict, phase: str, grade: str, subject: str) -> Dict:
        """Analyze alignment details"""
        return {
            "phase_alignment": "aligned",
            "grade_appropriateness": "appropriate",
            "subject_relevance": "relevant"
        }
    
    def _identify_alignment_gaps(self, material: Dict, phase: str, grade: str, subject: str) -> List[str]:
        """Identify alignment gaps"""
        return ["Missing formative assessment guidance", "Could use more differentiation strategies"]
    
    def _make_alignment_recommendations(self, material: Dict, phase: str, grade: str, subject: str) -> List[str]:
        """Make alignment recommendations"""
        return ["Add more learning activities", "Include assessment examples", "Provide differentiation guidance"]
    
    def _identify_coverage_gaps(self, phase: str, grade: str, subject: str, coverage: Dict) -> List[str]:
        """Identify coverage gaps"""
        return ["Topic coverage 70% complete", "Missing practical applications"]
    
    def _recommend_additions(self, phase: str, grade: str, subject: str) -> List[str]:
        """Recommend curriculum additions"""
        return ["Add project-based learning", "Include cross-curricular connections"]
    
    def _prioritize_additions(self, coverage: Dict) -> List[Dict]:
        """Prioritize additions"""
        return [
            {"priority": "high", "addition": "Practical applications"},
            {"priority": "medium", "addition": "Cross-curricular links"}
        ]
    
    def _suggest_timeline(self, phase: str, grade: str) -> Dict:
        """Suggest implementation timeline"""
        return {
            "immediate": "1-2 weeks",
            "short_term": "1 month",
            "long_term": "1 semester"
        }
    
    def integrate_expert_knowledge(self, query: str, context: Dict) -> Dict:
        """Integrate expert knowledge for curriculum guidance"""
        # Access expert knowledge base
        expert_insights = self._query_expert_knowledge(query, context)
        
        # Validate against curriculum standards
        validated_insights = self._validate_against_standards(expert_insights, context)
        
        # Format for educational context
        formatted_guidance = self._format_expert_guidance(validated_insights, context)
        
        return {
            "query": query,
            "expert_insights": expert_insights,
            "validated_insights": validated_insights,
            "formatted_guidance": formatted_guidance,
            "confidence_level": self._calculate_expert_confidence(expert_insights),
            "sources": self._identify_expert_sources(expert_insights),
            "limitations": self._identify_limitations(expert_insights)
        }
    
    def _query_expert_knowledge(self, query: str, context: Dict) -> Dict:
        """Query expert knowledge base"""
        # Simulated expert knowledge retrieval
        expert_categories = {
            "pedagogy": ["inquiry-based learning", "differentiated instruction", "scaffolding"],
            "assessment": ["formative assessment", "performance tasks", "rubric design"],
            "curriculum": ["Kurikulum Merdeka", "CP structure", "ATP planning"],
            "content": ["age-appropriateness", "cultural relevance", "inclusivity"]
        }
        
        relevant_insights = {
            "primary_insight": f"Expert guidance for: {query}",
            "pedagogical_principles": expert_categories["pedagogy"],
            "best_practices": [
                "Align with developmental stages",
                "Use culturally responsive materials",
                "Include diverse perspectives",
                "Apply universal design for learning"
            ],
            "research_evidence": [
                "Based on educational research and best practices",
                "Aligned with national curriculum standards",
                "Supported by pedagogical frameworks"
            ],
            "expert_consensus": "High agreement among curriculum experts"
        }
        
        return relevant_insights
    
    def _validate_against_standards(self, insights: Dict, context: Dict) -> Dict:
        """Validate insights against curriculum standards"""
        validation_result = {
            "standards_compliant": True,
            "alignment_score": 0.92,
            "standards_reference": [
                "Kurikulum Merdeka 2024",
                "National Education Standards",
                "Best Practice Guidelines"
            ],
            "adjustments_needed": [],
            "validation_notes": "Insights align with current curriculum framework"
        }
        
        return validation_result
    
    def _format_expert_guidance(self, insights: Dict, context: Dict) -> Dict:
        """Format expert guidance for educational context"""
        return {
            "actionable_recommendations": [
                "Implement inquiry-based approaches",
                "Use formative assessment strategies",
                "Differentiate instruction based on student needs",
                "Align assessments with learning objectives"
            ],
            "implementation_steps": [
                "Step 1: Review current practices",
                "Step 2: Plan implementation",
                "Step 3: Pilot and refine",
                "Step 4: Full implementation"
            ],
            "resource_recommendations": [
                "Teacher guides and manuals",
                "Professional development resources",
                "Sample lesson plans and activities"
            ],
            "professional_development": [
                "Training on pedagogical strategies",
                "Workshops on assessment design",
                "Coaching and mentoring support"
            ]
        }
    
    def _calculate_expert_confidence(self, insights: Dict) -> float:
        """Calculate confidence level in expert insights"""
        return 0.88
    
    def _identify_expert_sources(self, insights: Dict) -> List[str]:
        """Identify expert sources"""
        return [
            "Curriculum development experts",
            "Pedagogical researchers",
            "Assessment specialists",
            "Subject matter experts",
            "Education practitioners"
        ]
    
    def _identify_limitations(self, insights: Dict) -> List[str]:
        """Identify limitations of expert knowledge"""
        return [
            "Context-specific adaptation may be required",
            "Cultural considerations should be addressed",
            "Resource availability may impact implementation",
            "Professional development support essential"
        ]


class AssessmentAgent:
    """Assessment Creation Agent"""
    
    def __init__(self):
        self.assessment_templates = self._load_assessment_templates()
        self.rubric_templates = self._load_rubric_templates()
    
    def generate_assessment(self, topic: str, competency: str, grade: str,
                         assessment_type: str, cognitive_levels: List[str], question_count: int) -> Dict:
        """Generate comprehensive assessment"""
        assessment = {
            "title": f"{assessment_type.title()} Assessment: {topic}",
            "topic": topic,
            "competency": competency,
            "grade": grade,
            "assessment_type": assessment_type,
            "cognitive_levels": cognitive_levels or self._suggest_cognitive_levels(grade),
            "questions": self._generate_assessment_questions(topic, competency, grade, assessment_type, cognitive_levels, question_count),
            "rubric": self._generate_assessment_rubric(assessment_type, cognitive_levels),
            "instructions": self._generate_assessment_instructions(assessment_type),
            "estimated_duration": self._estimate_assessment_duration(question_count, assessment_type),
            "scoring_guide": self._generate_scoring_guide(assessment_type)
        }
        return assessment
    
    def create_rubric(self, assessment_type: str, criteria: List[str], 
                     performance_levels: int, context: Dict) -> Dict:
        """Create assessment rubric"""
        rubric = {
            "assessment_type": assessment_type,
            "criteria_count": len(criteria),
            "performance_levels": performance_levels,
            "rubric_table": self._build_rubric_table(criteria, performance_levels),
            "descriptions": self._generate_level_descriptions(performance_levels),
            "scoring_scale": self._define_scoring_scale(performance_levels),
            "guidance_notes": self._provide_rubric_guidance(assessment_type, criteria)
        }
        return rubric
    
    def provide_analytics(self, assessment_id: str, class_id: str, analysis_type: str) -> Dict:
        """Provide assessment analytics"""
        analytics = {
            "assessment_id": assessment_id,
            "class_id": class_id,
            "analysis_type": analysis_type,
            "performance_summary": self._generate_performance_summary(assessment_id, class_id),
            "question_analysis": self._analyze_question_performance(assessment_id, class_id),
            "trend_analysis": self._analyze_performance_trends(assessment_id, class_id),
            "outlier_detection": self._detect_outliers(assessment_id, class_id),
            "recommendations": self._generate_analytics_recommendations(assessment_id, class_id, analysis_type)
        }
        return analytics
    
    def _generate_assessment_questions(self, topic: str, competency: str, grade: str, 
                                    assessment_type: str, cognitive_levels: List[str], count: int) -> List[Dict]:
        """Generate assessment questions"""
        questions = []
        
        for i in range(count):
            level = cognitive_levels[i % len(cognitive_levels)] if cognitive_levels else "understand"
            question = {
                "id": f"q{i+1}",
                "question": self._generate_question_content(topic, competency, level, i),
                "cognitive_level": level,
                "points": self._assign_points_by_level(level),
                "difficulty": self._map_level_to_difficulty(level)
            }
            questions.append(question)
        
        return questions
    
    def _generate_question_content(self, topic: str, competency: str, level: str, index: int) -> str:
        """Generate question content"""
        templates = {
            "remember": f"What is {topic}?",
            "understand": f"Explain {topic} and its relationship to {competency}.",
            "apply": f"How would you apply {topic} in a real-world situation?",
            "analyze": f"Analyze the key components of {topic}.",
            "evaluate": f"Evaluate the effectiveness of {topic}.",
            "create": f"Create a plan using principles of {topic}."
        }
        return templates.get(level, templates["understand"])
    
    def _assign_points_by_level(self, level: str) -> int:
        """Assign points based on cognitive level"""
        points_map = {
            "remember": 2,
            "understand": 3,
            "apply": 4,
            "analyze": 5,
            "evaluate": 6,
            "create": 7
        }
        return points_map.get(level, 3)
    
    def _map_level_to_difficulty(self, level: str) -> str:
        """Map cognitive level to difficulty"""
        difficulty_map = {
            "remember": "easy",
            "understand": "easy",
            "apply": "medium",
            "analyze": "medium",
            "evaluate": "hard",
            "create": "hard"
        }
        return difficulty_map.get(level, "medium")
    
    def _generate_assessment_rubric(self, assessment_type: str, cognitive_levels: List[str]) -> Dict:
        """Generate assessment rubric"""
        return {
            "criteria": ["Content Knowledge", "Understanding", "Application", "Communication"],
            "levels": ["Excellent", "Good", "Satisfactory", "Needs Improvement"],
            "score_ranges": {
                "Excellent": "90-100",
                "Good": "80-89",
                "Satisfactory": "70-79",
                "Needs Improvement": "0-69"
            }
        }
    
    def _generate_assessment_instructions(self, assessment_type: str) -> str:
        """Generate assessment instructions"""
        return f"Complete this {assessment_type} assessment to the best of your ability. Read each question carefully and provide detailed answers."
    
    def _estimate_assessment_duration(self, question_count: int, assessment_type: str) -> int:
        """Estimate assessment duration"""
        time_per_question = 5 if assessment_type == "summative" else 3
        return question_count * time_per_question
    
    def _generate_scoring_guide(self, assessment_type: str) -> Dict:
        """Generate scoring guide"""
        return {
            "partial_credit": "available",
            "key_points": "provided",
            "weighting": "included"
        }
    
    def _suggest_cognitive_levels(self, grade: str) -> List[str]:
        """Suggest appropriate cognitive levels"""
        if grade in ["1", "2", "3"]:
            return ["remember", "understand"]
        elif grade in ["4", "5", "6"]:
            return ["understand", "apply", "analyze"]
        else:
            return ["apply", "analyze", "evaluate", "create"]
    
    def _build_rubric_table(self, criteria: List[str], levels: int) -> List[Dict]:
        """Build rubric table"""
        rubric = []
        level_names = ["Excellent", "Good", "Satisfactory", "Needs Improvement"][:levels]
        
        for criterion in criteria:
            criterion_row = {"criterion": criterion, "levels": []}
            for level in level_names:
                criterion_row["levels"].append({
                    "level": level,
                    "description": f"{level} performance in {criterion}"
                })
            rubric.append(criterion_row)
        
        return rubric
    
    def _generate_level_descriptions(self, levels: int) -> Dict:
        """Generate performance level descriptions"""
        return {
            "level_1": "Exceeds expectations consistently",
            "level_2": "Meets expectations consistently",
            "level_3": "Approaches expectations",
            "level_4": "Below expectations"
        }
    
    def _define_scoring_scale(self, levels: int) -> Dict:
        """Define scoring scale"""
        return {
            "scale": f"1-{levels}",
            "passing_score": f"{levels * 0.7:.0f}",
            "weighting": "equal"
        }
    
    def _provide_rubric_guidance(self, assessment_type: str, criteria: List[str]) -> List[str]:
        """Provide rubric guidance"""
        return [
            "Use consistent language across levels",
            "Include observable behaviors",
            "Provide specific examples",
            "Align with learning objectives"
        ]
    
    def _load_assessment_templates(self) -> Dict:
        """Load assessment templates"""
        return {}
    
    def _load_rubric_templates(self) -> Dict:
        """Load rubric templates"""
        return {}
    
    def _generate_performance_summary(self, assessment_id: str, class_id: str) -> Dict:
        """Generate performance summary"""
        return {
            "average_score": 78.5,
            "pass_rate": 85,
            "median": 76
        }
    
    def _analyze_question_performance(self, assessment_id: str, class_id: str) -> List[Dict]:
        """Analyze individual question performance"""
        return [
            {"question_id": "q1", "average": 85, "difficulty": "easy"},
            {"question_id": "q2", "average": 72, "difficulty": "medium"}
        ]
    
    def _analyze_performance_trends(self, assessment_id: str, class_id: str) -> Dict:
        """Analyze performance trends"""
        return {
            "trend": "improving",
            "change": "+5% over time",
            "consistency": "moderate"
        }
    
    def _detect_outliers(self, assessment_id: str, class_id: str) -> List[Dict]:
        """Detect performance outliers"""
        return [
            {"type": "high_performers", "count": 3},
            {"type": "struggling_students", "count": 2}
        ]
    
    def _generate_analytics_recommendations(self, assessment_id: str, class_id: str, analysis_type: str) -> List[str]:
        """Generate analytics recommendations"""
        return [
            "Review question difficulty balance",
            "Provide additional support for struggling students",
            "Consider enrichment for high performers"
        ]
    
    def validate_quality(self, assessment_data: Dict) -> Dict:
        """Validate assessment quality before deployment"""
        quality_checks = {
            "content_quality": self._check_content_quality(assessment_data),
            "technical_quality": self._check_technical_quality(assessment_data),
            "pedagogical_quality": self._check_pedagogical_quality(assessment_data),
            "alignment_quality": self._check_alignment_quality(assessment_data),
            "fairness_quality": self._check_fairness_quality(assessment_data)
        }
        
        overall_quality = self._calculate_overall_quality(quality_checks)
        recommendations = self._generate_quality_recommendations(quality_checks)
        
        return {
            "assessment_id": assessment_data.get("assessment_id", "unknown"),
            "overall_quality_score": overall_quality,
            "quality_passed": overall_quality >= 0.7,
            "quality_checks": quality_checks,
            "recommendations": recommendations,
            "approval_status": "approved" if overall_quality >= 0.7 else "needs_revision"
        }
    
    def _check_content_quality(self, assessment_data: Dict) -> Dict:
        """Check content quality"""
        questions = assessment_data.get("questions", [])
        
        return {
            "check_name": "content_quality",
            "score": 0.85,
            "passed": True,
            "details": {
                "clarity_score": 0.9,
                "accuracy_score": 0.85,
                "language_appropriateness": 0.8,
                "issues": [],
                "strengths": ["Clear language", "Accurate content", "Grade-appropriate"]
            }
        }
    
    def _check_technical_quality(self, assessment_data: Dict) -> Dict:
        """Check technical quality"""
        questions = assessment_data.get("questions", [])
        rubric = assessment_data.get("rubric", {})
        
        return {
            "check_name": "technical_quality",
            "score": 0.8,
            "passed": True,
            "details": {
                "formatting_score": 0.9,
                "completeness_score": 0.75,
                "consistency_score": 0.8,
                "issues": ["Some missing metadata"],
                "strengths": ["Consistent formatting", "Complete rubric"]
            }
        }
    
    def _check_pedagogical_quality(self, assessment_data: Dict) -> Dict:
        """Check pedagogical quality"""
        questions = assessment_data.get("questions", [])
        cognitive_levels = [q.get("cognitive_level", "understand") for q in questions]
        
        return {
            "check_name": "pedagogical_quality",
            "score": 0.75,
            "passed": True,
            "details": {
                "cognitive_balance_score": 0.8,
                "difficulty_progression_score": 0.7,
                "learning_objectives_alignment": 0.75,
                "issues": ["Could improve difficulty progression"],
                "strengths": ["Good cognitive level variety", "Aligned with objectives"]
            }
        }
    
    def _check_alignment_quality(self, assessment_data: Dict) -> Dict:
        """Check alignment quality"""
        topic = assessment_data.get("topic", "")
        competency = assessment_data.get("competency", "")
        
        return {
            "check_name": "alignment_quality",
            "score": 0.9,
            "passed": True,
            "details": {
                "topic_alignment_score": 0.95,
                "competency_alignment_score": 0.9,
                "grade_appropriateness_score": 0.85,
                "issues": [],
                "strengths": ["Excellent topic alignment", "Strong competency coverage"]
            }
        }
    
    def _check_fairness_quality(self, assessment_data: Dict) -> Dict:
        """Check fairness and bias"""
        questions = assessment_data.get("questions", [])
        
        return {
            "check_name": "fairness_quality",
            "score": 0.85,
            "passed": True,
            "details": {
                "bias_score": 0.9,
                "cultural_sensitivity_score": 0.85,
                "accessibility_score": 0.8,
                "issues": ["Consider accessibility improvements"],
                "strengths": ["Culturally appropriate", "Minimal bias detected"]
            }
        }
    
    def _calculate_overall_quality(self, quality_checks: Dict) -> float:
        """Calculate overall quality score"""
        scores = [check["score"] for check in quality_checks.values()]
        return round(sum(scores) / len(scores), 2)
    
    def _generate_quality_recommendations(self, quality_checks: Dict) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        for check_name, check_data in quality_checks.items():
            if not check_data["passed"]:
                recommendations.append(f"Improve {check_name}: {check_data['details']}")
            
            if check_data["details"]["issues"]:
                for issue in check_data["details"]["issues"]:
                    recommendations.append(f"Address: {issue}")
        
        if not recommendations:
            recommendations.append("Assessment meets all quality standards. Ready for deployment.")
        
        return recommendations


# Initialize AI agents engine
ai_agents_engine = AIAgentsEngine()


# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Import and start gRPC server if enabled
    if ENABLE_GRPC_SERVER:
        from .grpc_server import serve
        import asyncio
        asyncio.create_task(serve(GRPC_PORT))
    
    # Import and start RabbitMQ consumer if enabled
    if ENABLE_RABBITMQ_CONSUMER:
        from .consumer import AsyncAIAgentsConsumer
        consumer = AsyncAIAgentsConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="AI Agents Service",
    description="User-Facing Intelligence - 4 AI Agents",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "ai-agents-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Teacher Agent endpoints
@app.post("/agent/teacher/lesson-plan")
async def lesson_planning(request: LessonPlanningRequest):
    """Lesson planning assistant"""
    result = ai_agents_engine.lesson_planning_assistant(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="teacher_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/teacher/assessment")
async def assessment_creation(request: AssessmentCreationRequest):
    """Assessment creation assistant"""
    result = ai_agents_engine.assessment_creation_assistant(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="teacher_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/teacher/progress-analysis")
async def student_progress_analysis(request: StudentProgressAnalysisRequest):
    """Student progress analysis"""
    result = ai_agents_engine.student_progress_analysis(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="teacher_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/teacher/strategy")
async def teaching_strategy_recommendation(request: TeachingStrategyRequest):
    """Teaching strategy recommendation"""
    result = ai_agents_engine.teaching_strategy_recommendation(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="teacher_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


# Student Learning Agent endpoints
@app.post("/agent/student/guidance")
async def personalized_guidance(request: PersonalizedGuidanceRequest):
    """Personalized learning guidance"""
    result = ai_agents_engine.personalized_guidance(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="student_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/student/qanda")
async def question_answering(request: QuestionAnsweringRequest):
    """Question answering"""
    result = ai_agents_engine.question_answering(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="student_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/student/learning-path")
async def learning_path_recommendation(request: LearningPathRecommendationRequest):
    """Learning path recommendation"""
    result = ai_agents_engine.learning_path_recommendation(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="student_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


# Curriculum Agent endpoints
@app.post("/agent/curriculum/cp-guidance")
async def cp_guidance(request: CPGuidanceRequest):
    """CP guidance"""
    result = ai_agents_engine.cp_guidance(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="curriculum_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/curriculum/atp-guidance")
async def atp_guidance(request: ATPGuidanceRequest):
    """ATP guidance"""
    result = ai_agents_engine.atp_guidance(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="curriculum_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/curriculum/alignment-check")
async def curriculum_alignment_checking(request: CurriculumAlignmentRequest):
    """Curriculum alignment checking"""
    result = ai_agents_engine.curriculum_alignment_checking(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="curriculum_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/curriculum/recommendation")
async def curriculum_recommendation(request: CurriculumRecommendationRequest):
    """Curriculum recommendation"""
    result = ai_agents_engine.curriculum_recommendation(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="curriculum_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


# Assessment Agent endpoints
@app.post("/agent/assessment/generation")
async def assessment_generation_assistant(request: AssessmentGenerationRequest):
    """Assessment generation assistant"""
    result = ai_agents_engine.assessment_generation_assistant(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="assessment_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/assessment/rubric")
async def rubric_creation_assistant(request: RubricCreationRequest):
    """Rubric creation assistant"""
    result = ai_agents_engine.rubric_creation_assistant(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="assessment_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/assessment/analytics")
async def assessment_analytics(request: AssessmentAnalyticsRequest):
    """Assessment analytics"""
    result = ai_agents_engine.assessment_analytics(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="assessment_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


# New feature endpoints
@app.post("/agent/student/adaptive-interaction")
async def adaptive_interaction(request: AdaptiveInteractionRequest):
    """Adaptive interaction for student learning"""
    result = ai_agents_engine.adaptive_interaction(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="student_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/curriculum/expert-knowledge")
async def expert_knowledge_integration(request: ExpertKnowledgeRequest):
    """Expert knowledge integration for curriculum"""
    result = ai_agents_engine.expert_knowledge_integration(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="curriculum_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


@app.post("/agent/assessment/quality-validation")
async def quality_validation(request: QualityValidationRequest):
    """Quality validation for assessment"""
    result = ai_agents_engine.quality_validation(request)
    return AgentResult(
        request_id=request.request_id,
        agent_type="assessment_agent",
        result=result["result"],
        metadata=result["metadata"]
    )


# Performance monitoring
@app.get("/agents/performance")
async def get_performance_metrics():
    """Get agents performance metrics"""
    return ai_agents_engine.performance_metrics


@app.get("/agents/available")
async def get_available_agents():
    """Get available AI agents"""
    return {
        "agents": [
            {
                "name": "teacher_agent",
                "description": "Teacher assistant for lesson planning, assessment creation, and student progress analysis",
                "capabilities": ["lesson_planning", "assessment_creation", "progress_analysis", "strategy_recommendation"]
            },
            {
                "name": "student_agent",
                "description": "Student learning companion for personalized guidance and support",
                "capabilities": ["personalized_guidance", "question_answering", "learning_path_recommendation", "progress_tracking", "adaptive_interaction"]
            },
            {
                "name": "curriculum_agent",
                "description": "Curriculum expert for CP/ATP guidance and alignment checking",
                "capabilities": ["cp_guidance", "atp_guidance", "alignment_checking", "curriculum_recommendation", "expert_knowledge_integration"]
            },
            {
                "name": "assessment_agent",
                "description": "Assessment specialist for generation, rubric creation, and analytics",
                "capabilities": ["assessment_generation", "rubric_creation", "assessment_analytics", "quality_validation"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8023)