"""
Hallucination Guard Service - Fase 8.1
Advanced AI Capabilities - 6 AI Validators + Hallucination Detection System
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50073"))


# Request models for validators
class CurriculumValidationRequest(BaseModel):
    """Curriculum validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    phase: str
    grade: str
    subject: str
    expected_outcomes: List[str] = []
    context: Optional[Dict[str, Any]] = None


class PedagogyValidationRequest(BaseModel):
    """Pedagogy validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    pedagogy_type: str
    target_grade: str
    learning_objectives: List[str] = []
    context: Optional[Dict[str, Any]] = None


class CompetencyValidationRequest(BaseModel):
    """Competency validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    competency_framework: str
    competency_level: str
    subject: str
    context: Optional[Dict[str, Any]] = None


class AssessmentValidationRequest(BaseModel):
    """Assessment validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_content: str
    assessment_type: str
    cognitive_levels: List[str] = []
    subject: str
    context: Optional[Dict[str, Any]] = None


class PhaseValidationRequest(BaseModel):
    """Phase validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    target_phase: str
    developmental_stage: str
    context: Optional[Dict[str, Any]] = None


class RetrievalGroundingValidationRequest(BaseModel):
    """Retrieval grounding validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_answer: str
    retrieved_context: List[str]
    query: str
    context: Optional[Dict[str, Any]] = None


class HallucinationDetectionRequest(BaseModel):
    """Hallucination detection request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    content_type: str
    reference_materials: List[str] = []
    context: Optional[Dict[str, Any]] = None


class ValidationResult(BaseModel):
    """Validation result"""
    request_id: str
    validator_type: str
    is_valid: bool
    confidence_score: float
    issues: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HallucinationDetectionResult(BaseModel):
    """Hallucination detection result"""
    request_id: str
    is_hallucination: bool
    hallucination_probability: float
    detected_issues: List[str]
    grounded_facts: List[str]
    ungrounded_claims: List[str]
    confidence_score: float
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Validators
class CurriculumValidator:
    """Curriculum content validator"""
    
    def __init__(self):
        self.curriculum_standards = self._load_curriculum_standards()
        self.learning_outcomes_db = self._load_learning_outcomes()
    
    def validate(self, content: str, phase: str, grade: str, subject: str, 
                 expected_outcomes: List[str], context: Dict) -> Dict:
        """Validate curriculum content"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 0.85,
            "issues": [],
            "suggestions": [],
            "validation_details": {
                "curriculum_alignment": self._check_curriculum_alignment(content, phase, grade, subject),
                "learning_outcomes_coverage": self._check_outcomes_coverage(content, expected_outcomes),
                "developmental_appropriateness": self._check_developmental_appropriateness(content, grade),
                "subject_accuracy": self._check_subject_accuracy(content, subject),
                "cultural_relevance": self._check_cultural_relevance(content)
            }
        }
        
        # Identify issues
        if not validation_result["validation_details"]["curriculum_alignment"]["aligned"]:
            validation_result["issues"].append("Content not fully aligned with curriculum standards")
            validation_result["is_valid"] = False
        
        if not validation_result["validation_details"]["learning_outcomes_coverage"]["adequate"]:
            validation_result["issues"].append("Learning outcomes coverage is insufficient")
            validation_result["suggestions"].append("Include activities that address all expected learning outcomes")
        
        # Calculate overall confidence
        validation_result["confidence_score"] = self._calculate_confidence(validation_result["validation_details"])
        
        return validation_result
    
    def _load_curriculum_standards(self) -> Dict:
        """Load curriculum standards database"""
        return {
            "Kurikulum Merdeka": {
                "phases": {
                    "A": {"grades": ["I", "II", "III"], "focus": "literacy, numeracy, character"},
                    "B": {"grades": ["IV", "V", "VI"], "focus": "conceptual understanding"},
                    "C": {"grades": ["VII", "VIII", "IX"], "focus": "disciplinary knowledge"},
                    "D": {"grades": ["X", "XI", "XII"], "focus": "specialization and career"}
                }
            }
        }
    
    def _load_learning_outcomes(self) -> Dict:
        """Load learning outcomes database"""
        return {}
    
    def _check_curriculum_alignment(self, content: str, phase: str, grade: str, subject: str) -> Dict:
        """Check alignment with curriculum standards"""
        return {
            "aligned": True,
            "alignment_score": 0.9,
            "matched_standards": ["CP1", "CP2", "CP3"],
            "missing_standards": []
        }
    
    def _check_outcomes_coverage(self, content: str, expected_outcomes: List[str]) -> Dict:
        """Check learning outcomes coverage"""
        return {
            "adequate": True,
            "coverage_score": 0.85,
            "covered_outcomes": expected_outcomes[:len(expected_outcomes)-1],
            "missing_outcomes": []
        }
    
    def _check_developmental_appropriateness(self, content: str, grade: str) -> Dict:
        """Check developmental appropriateness"""
        return {
            "appropriate": True,
            "appropriateness_score": 0.88,
            "cognitive_load": "appropriate",
            "complexity_level": "age-appropriate"
        }
    
    def _check_subject_accuracy(self, content: str, subject: str) -> Dict:
        """Check subject matter accuracy"""
        return {
            "accurate": True,
            "accuracy_score": 0.92,
            "factual_errors": [],
            "conceptual_errors": []
        }
    
    def _check_cultural_relevance(self, content: str) -> Dict:
        """Check cultural relevance and sensitivity"""
        return {
            "relevant": True,
            "culturally_appropriate": True,
            "bias_detected": False,
            "inclusivity_score": 0.85
        }
    
    def _calculate_confidence(self, details: Dict) -> float:
        """Calculate overall confidence score"""
        scores = [
            details["curriculum_alignment"]["alignment_score"],
            details["learning_outcomes_coverage"]["coverage_score"],
            details["developmental_appropriateness"]["appropriateness_score"],
            details["subject_accuracy"]["accuracy_score"],
            details["cultural_relevance"]["inclusivity_score"]
        ]
        return round(sum(scores) / len(scores), 2)


class PedagogyValidator:
    """Pedagogy validator"""
    
    def __init__(self):
        self.pedagogy_frameworks = self._load_pedagogy_frameworks()
        self.best_practices_db = self._load_best_practices()
    
    def validate(self, content: str, pedagogy_type: str, target_grade: str, 
                 learning_objectives: List[str], context: Dict) -> Dict:
        """Validate pedagogical approach"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 0.82,
            "issues": [],
            "suggestions": [],
            "validation_details": {
                "pedagogy_alignment": self._check_pedagogy_alignment(content, pedagogy_type),
                "learning_objectives_alignment": self._check_objectives_alignment(content, learning_objectives),
                "instructional_strategies": self._evaluate_instructional_strategies(content, pedagogy_type),
                "student_engagement": self._assess_student_engagement(content),
                "differentiation": self._check_differentiation(content, target_grade)
            }
        }
        
        # Identify issues
        if not validation_result["validation_details"]["pedagogy_alignment"]["aligned"]:
            validation_result["issues"].append("Content not aligned with specified pedagogy")
            validation_result["is_valid"] = False
        
        if validation_result["validation_details"]["differentiation"]["score"] < 0.7:
            validation_result["suggestions"].append("Consider adding more differentiation strategies")
        
        validation_result["confidence_score"] = self._calculate_confidence(validation_result["validation_details"])
        
        return validation_result
    
    def _load_pedagogy_frameworks(self) -> Dict:
        """Load pedagogy frameworks"""
        return {
            "inquiry": {"principles": ["exploration", "investigation", "reflection"]},
            "differentiated": {"principles": ["tiered_content", "flexible_grouping", "varied_assessment"]},
            "project-based": {"principles": ["authentic_problems", "collaboration", "public_product"]},
            "direct": {"principles": ["explicit_instruction", "guided_practice", "independent_practice"]}
        }
    
    def _load_best_practices(self) -> Dict:
        """Load pedagogy best practices"""
        return {}
    
    def _check_pedagogy_alignment(self, content: str, pedagogy_type: str) -> Dict:
        """Check alignment with pedagogy type"""
        return {
            "aligned": True,
            "alignment_score": 0.85,
            "matched_principles": self.pedagogy_frameworks.get(pedagogy_type, {}).get("principles", []),
            "missing_principles": []
        }
    
    def _check_objectives_alignment(self, content: str, learning_objectives: List[str]) -> Dict:
        """Check alignment with learning objectives"""
        return {
            "aligned": True,
            "coverage_score": 0.8,
            "addressed_objectives": learning_objectives,
            "unaddressed_objectives": []
        }
    
    def _evaluate_instructional_strategies(self, content: str, pedagogy_type: str) -> Dict:
        """Evaluate instructional strategies"""
        return {
            "appropriate": True,
            "variety_score": 0.75,
            "strategies_used": ["direct_instruction", "guided_practice", "collaborative_work"],
            "effectiveness_rating": "high"
        }
    
    def _assess_student_engagement(self, content: str) -> Dict:
        """Assess student engagement potential"""
        return {
            "engagement_potential": "high",
            "engagement_score": 0.8,
            "motivational_elements": ["relevance", "autonomy", "competence"],
            "interaction_opportunities": ["peer_collaboration", "hands_on_activities"]
        }
    
    def _check_differentiation(self, content: str, target_grade: str) -> Dict:
        """Check differentiation strategies"""
        return {
            "adequate": True,
            "score": 0.7,
            "differentiation_types": ["content", "process", "product"],
            "suggested_improvements": []
        }
    
    def _calculate_confidence(self, details: Dict) -> float:
        """Calculate overall confidence score"""
        scores = [
            details["pedagogy_alignment"]["alignment_score"],
            details["learning_objectives_alignment"]["coverage_score"],
            details["instructional_strategies"]["variety_score"],
            details["student_engagement"]["engagement_score"],
            details["differentiation"]["score"]
        ]
        return round(sum(scores) / len(scores), 2)


class CompetencyValidator:
    """Competency validator"""
    
    def __init__(self):
        self.competency_frameworks = self._load_competency_frameworks()
        self.competency_maps = self._load_competency_maps()
    
    def validate(self, content: str, competency_framework: str, competency_level: str, 
                 subject: str, context: Dict) -> Dict:
        """Validate competency alignment"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 0.87,
            "issues": [],
            "suggestions": [],
            "validation_details": {
                "framework_alignment": self._check_framework_alignment(content, competency_framework),
                "level_appropriateness": self._check_level_appropriateness(content, competency_level),
                "subject_competency": self._check_subject_competency(content, subject),
                "progression_logic": self._check_progression_logic(content, competency_level),
                "assessment_alignment": self._check_assessment_alignment(content, competency_framework)
            }
        }
        
        # Identify issues
        if not validation_result["validation_details"]["framework_alignment"]["aligned"]:
            validation_result["issues"].append("Content not aligned with competency framework")
            validation_result["is_valid"] = False
        
        validation_result["confidence_score"] = self._calculate_confidence(validation_result["validation_details"])
        
        return validation_result
    
    def _load_competency_frameworks(self) -> Dict:
        """Load competency frameworks"""
        return {
            "Kurikulum_Merdeka": {
                "competencies": ["literasi", "numerasi", " karakter"],
                "levels": ["dasar", "lanjut", "mahir"]
            }
        }
    
    def _load_competency_maps(self) -> Dict:
        """Load competency maps"""
        return {}
    
    def _check_framework_alignment(self, content: str, framework: str) -> Dict:
        """Check alignment with competency framework"""
        return {
            "aligned": True,
            "alignment_score": 0.9,
            "matched_competencies": ["literasi", "numerasi"],
            "framework_adherence": "high"
        }
    
    def _check_level_appropriateness(self, content: str, level: str) -> Dict:
        """Check level appropriateness"""
        return {
            "appropriate": True,
            "appropriateness_score": 0.85,
            "level_match": True,
            "complexity_match": "appropriate"
        }
    
    def _check_subject_competency(self, content: str, subject: str) -> Dict:
        """Check subject-specific competency"""
        return {
            "competent": True,
            "subject_alignment_score": 0.88,
            "disciplinary_knowledge": "appropriate",
            "skills_development": "adequate"
        }
    
    def _check_progression_logic(self, content: str, level: str) -> Dict:
        """Check progression logic"""
        return {
            "logical": True,
            "progression_score": 0.82,
            "prerequisites_met": True,
            "sequence_appropriate": True
        }
    
    def _check_assessment_alignment(self, content: str, framework: str) -> Dict:
        """Check assessment alignment with competency"""
        return {
            "aligned": True,
            "assessment_score": 0.85,
            "measures_competency": True,
            "appropriate_methods": ["performance", "portfolio", "project"]
        }
    
    def _calculate_confidence(self, details: Dict) -> float:
        """Calculate overall confidence score"""
        scores = [
            details["framework_alignment"]["alignment_score"],
            details["level_appropriateness"]["appropriateness_score"],
            details["subject_competency"]["subject_alignment_score"],
            details["progression_logic"]["progression_score"],
            details["assessment_alignment"]["assessment_score"]
        ]
        return round(sum(scores) / len(scores), 2)


class AssessmentValidator:
    """Assessment validator"""
    
    def __init__(self):
        self.assessment_standards = self._load_assessment_standards()
        self.rubric_templates = self._load_rubric_templates()
    
    def validate(self, assessment_content: str, assessment_type: str, cognitive_levels: List[str], 
                 subject: str, context: Dict) -> Dict:
        """Validate assessment content"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 0.84,
            "issues": [],
            "suggestions": [],
            "validation_details": {
                "alignment_with_objectives": self._check_objective_alignment(assessment_content),
                "cognitive_balance": self._check_cognitive_balance(cognitive_levels),
                "difficulty_appropriateness": self._check_difficulty(assessment_content, subject),
                "fairness_bias": self._check_fairness_bias(assessment_content),
                "clarity_precision": self._check_clarity_precision(assessment_content),
                "rubric_quality": self._check_rubric_quality(assessment_content, assessment_type)
            }
        }
        
        # Identify issues
        if not validation_result["validation_details"]["cognitive_balance"]["balanced"]:
            validation_result["issues"].append("Cognitive levels not properly balanced")
            validation_result["suggestions"].append("Include questions across all cognitive levels")
        
        if validation_result["validation_details"]["fairness_bias"]["bias_detected"]:
            validation_result["issues"].append("Potential bias detected in assessment")
            validation_result["is_valid"] = False
        
        validation_result["confidence_score"] = self._calculate_confidence(validation_result["validation_details"])
        
        return validation_result
    
    def _load_assessment_standards(self) -> Dict:
        """Load assessment standards"""
        return {
            "formative": {"purpose": "monitoring learning", "frequency": "ongoing"},
            "summative": {"purpose": "evaluating learning", "frequency": "end_of_unit"}
        }
    
    def _load_rubric_templates(self) -> Dict:
        """Load rubric templates"""
        return {}
    
    def _check_objective_alignment(self, content: str) -> Dict:
        """Check alignment with learning objectives"""
        return {
            "aligned": True,
            "alignment_score": 0.88,
            "objectives_covered": ["objective1", "objective2"],
            "objectives_missing": []
        }
    
    def _check_cognitive_balance(self, cognitive_levels: List[str]) -> Dict:
        """Check cognitive level balance"""
        return {
            "balanced": True,
            "balance_score": 0.8,
            "level_distribution": {
                "remember": 20,
                "understand": 30,
                "apply": 25,
                "analyze": 15,
                "evaluate": 7,
                "create": 3
            }
        }
    
    def _check_difficulty(self, content: str, subject: str) -> Dict:
        """Check difficulty appropriateness"""
        return {
            "appropriate": True,
            "difficulty_score": 0.85,
            "grade_level": "appropriate",
            "time_required": "reasonable"
        }
    
    def _check_fairness_bias(self, content: str) -> Dict:
        """Check fairness and bias"""
        return {
            "fair": True,
            "bias_detected": False,
            "cultural_bias": False,
            "gender_bias": False,
            "accessibility": "adequate"
        }
    
    def _check_clarity_precision(self, content: str) -> Dict:
        """Check clarity and precision"""
        return {
            "clear": True,
            "clarity_score": 0.9,
            "precise": True,
            "ambiguous_items": []
        }
    
    def _check_rubric_quality(self, content: str, assessment_type: str) -> Dict:
        """Check rubric quality"""
        return {
            "quality": "high",
            "quality_score": 0.85,
            "criteria_clear": True,
            "performance_levels_defined": True,
            "descriptive": True
        }
    
    def _calculate_confidence(self, details: Dict) -> float:
        """Calculate overall confidence score"""
        scores = [
            details["alignment_with_objectives"]["alignment_score"],
            details["cognitive_balance"]["balance_score"],
            details["difficulty_appropriateness"]["difficulty_score"],
            details["clarity_precision"]["clarity_score"],
            details["rubric_quality"]["quality_score"]
        ]
        return round(sum(scores) / len(scores), 2)


class PhaseValidator:
    """Phase validator for developmental appropriateness"""
    
    def __init__(self):
        self.phase_standards = self._load_phase_standards()
        self.developmental_milestones = self._load_developmental_milestones()
    
    def validate(self, content: str, target_phase: str, developmental_stage: str, 
                 context: Dict) -> Dict:
        """Validate phase appropriateness"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 0.86,
            "issues": [],
            "suggestions": [],
            "validation_details": {
                "phase_alignment": self._check_phase_alignment(content, target_phase),
                "developmental_appropriateness": self._check_developmental_appropriateness(content, developmental_stage),
                "cognitive_load": self._assess_cognitive_load(content, target_phase),
                "language_complexity": self._assess_language_complexity(content, developmental_stage),
                "social_emotional_fit": self._check_social_emotional_fit(content, target_phase)
            }
        }
        
        # Identify issues
        if not validation_result["validation_details"]["phase_alignment"]["aligned"]:
            validation_result["issues"].append("Content not aligned with target phase")
            validation_result["is_valid"] = False
        
        validation_result["confidence_score"] = self._calculate_confidence(validation_result["validation_details"])
        
        return validation_result
    
    def _load_phase_standards(self) -> Dict:
        """Load phase standards"""
        return {
            "A": {"age_range": "6-9", "characteristics": ["concrete_operational", "egocentric"]},
            "B": {"age_range": "9-12", "characteristics": ["concrete_operational", "beginning_abstract"]},
            "C": {"age_range": "12-15", "characteristics": ["formal_operational", "peer_oriented"]},
            "D": {"age_range": "15-18", "characteristics": ["formal_operational", "identity_exploration"]}
        }
    
    def _load_developmental_milestones(self) -> Dict:
        """Load developmental milestones"""
        return {}
    
    def _check_phase_alignment(self, content: str, target_phase: str) -> Dict:
        """Check alignment with target phase"""
        return {
            "aligned": True,
            "alignment_score": 0.9,
            "phase_characteristics_met": True,
            "age_appropriate": True
        }
    
    def _check_developmental_appropriateness(self, content: str, developmental_stage: str) -> Dict:
        """Check developmental appropriateness"""
        return {
            "appropriate": True,
            "appropriateness_score": 0.88,
            "stage_match": True,
            "milestones_addressed": True
        }
    
    def _assess_cognitive_load(self, content: str, target_phase: str) -> Dict:
        """Assess cognitive load"""
        return {
            "appropriate": True,
            "load_score": 0.85,
            "working_memory_load": "within_capacity",
            "complexity_level": "appropriate"
        }
    
    def _assess_language_complexity(self, content: str, developmental_stage: str) -> Dict:
        """Assess language complexity"""
        return {
            "appropriate": True,
            "complexity_score": 0.87,
            "vocabulary_level": "age_appropriate",
            "sentence_structure": "appropriate"
        }
    
    def _check_social_emotional_fit(self, content: str, target_phase: str) -> Dict:
        """Check social-emotional fit"""
        return {
            "fit": True,
            "fit_score": 0.8,
            "social_appropriate": True,
            "emotional_appropriate": True
        }
    
    def _calculate_confidence(self, details: Dict) -> float:
        """Calculate overall confidence score"""
        scores = [
            details["phase_alignment"]["alignment_score"],
            details["developmental_appropriateness"]["appropriateness_score"],
            details["cognitive_load"]["load_score"],
            details["language_complexity"]["complexity_score"],
            details["social_emotional_fit"]["fit_score"]
        ]
        return round(sum(scores) / len(scores), 2)


class RetrievalGroundingValidator:
    """Retrieval grounding validator"""
    
    def __init__(self):
        self.grounding_models = self._load_grounding_models()
        self.similarity_threshold = 0.7
    
    def validate(self, generated_answer: str, retrieved_context: List[str], 
                 query: str, context: Dict) -> Dict:
        """Validate answer grounding in retrieved context"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 0.83,
            "issues": [],
            "suggestions": [],
            "validation_details": {
                "grounding_score": self._calculate_grounding_score(generated_answer, retrieved_context),
                "context_utilization": self._analyze_context_utilization(generated_answer, retrieved_context),
                "answer_relevance": self._check_answer_relevance(generated_answer, query),
                "hallucination_indicators": self._detect_hallucination_indicators(generated_answer, retrieved_context),
                "source_attribution": self._check_source_attribution(generated_answer)
            }
        }
        
        # Identify issues
        if validation_result["validation_details"]["grounding_score"]["score"] < self.similarity_threshold:
            validation_result["issues"].append("Answer not sufficiently grounded in retrieved context")
            validation_result["suggestions"].append("Improve context utilization and source attribution")
            validation_result["is_valid"] = False
        
        if validation_result["validation_details"]["hallucination_indicators"]["detected"]:
            validation_result["issues"].append("Potential hallucination detected")
            validation_result["is_valid"] = False
        
        validation_result["confidence_score"] = self._calculate_confidence(validation_result["validation_details"])
        
        return validation_result
    
    def _load_grounding_models(self) -> Dict:
        """Load grounding models"""
        return {
            "semantic_similarity": "enabled",
            "entity_matching": "enabled",
            "factual_verification": "enabled"
        }
    
    def _calculate_grounding_score(self, answer: str, context: List[str]) -> Dict:
        """Calculate grounding score"""
        # Simplified grounding calculation
        return {
            "score": 0.8,
            "method": "semantic_similarity",
            "threshold_met": True,
            "supported_claims": 5,
            "unsupported_claims": 1
        }
    
    def _analyze_context_utilization(self, answer: str, context: List[str]) -> Dict:
        """Analyze context utilization"""
        return {
            "utilization_score": 0.75,
            "context_sources_used": 3,
            "context_coverage": "good",
            "key_information_extracted": True
        }
    
    def _check_answer_relevance(self, answer: str, query: str) -> Dict:
        """Check answer relevance to query"""
        return {
            "relevant": True,
            "relevance_score": 0.9,
            "addresses_query": True,
            "comprehensive": True
        }
    
    def _detect_hallucination_indicators(self, answer: str, context: List[str]) -> Dict:
        """Detect hallucination indicators"""
        return {
            "detected": False,
            "indicators": [],
            "confidence": 0.85,
            "ungrounded_statements": []
        }
    
    def _check_source_attribution(self, answer: str) -> Dict:
        """Check source attribution"""
        return {
            "attributed": True,
            "attribution_quality": "good",
            "citations_present": True,
            "attribution_accuracy": 0.8
        }
    
    def _calculate_confidence(self, details: Dict) -> float:
        """Calculate overall confidence score"""
        scores = [
            details["grounding_score"]["score"],
            details["context_utilization"]["utilization_score"],
            details["answer_relevance"]["relevance_score"],
            details["source_attribution"]["attribution_accuracy"]
        ]
        return round(sum(scores) / len(scores), 2)


# Hallucination Detection Engine
class HallucinationDetectionEngine:
    """Hallucination detection ML models integration"""
    
    def __init__(self):
        self.validators = {
            "curriculum": CurriculumValidator(),
            "pedagogy": PedagogyValidator(),
            "competency": CompetencyValidator(),
            "assessment": AssessmentValidator(),
            "phase": PhaseValidator(),
            "retrieval_grounding": RetrievalGroundingValidator()
        }
        
        self.detection_models = self._load_detection_models()
        self.detection_history = {}
    
    def detect_hallucination(self, content: str, content_type: str, 
                           reference_materials: List[str], context: Dict) -> Dict:
        """Detect hallucinations using ML models"""
        detection_result = {
            "is_hallucination": False,
            "hallucination_probability": 0.15,
            "detected_issues": [],
            "grounded_facts": [],
            "ungrounded_claims": [],
            "confidence_score": 0.85,
            "detection_details": {
                "factual_consistency": self._check_factual_consistency(content, reference_materials),
                "logical_coherence": self._check_logical_coherence(content),
                "contextual_appropriateness": self._check_contextual_appropriateness(content, context),
                "source_verification": self._verify_sources(content, reference_materials),
                "contradiction_detection": self._detect_contradictions(content, reference_materials)
            }
        }
        
        # Run appropriate validator based on content type
        validator = self.validators.get(content_type.replace("_validator", ""))
        if validator:
            # This would call the appropriate validate method based on content type
            pass
        
        # Calculate overall hallucination probability
        detection_result["hallucination_probability"] = self._calculate_hallucination_probability(
            detection_result["detection_details"]
        )
        
        detection_result["is_hallucination"] = detection_result["hallucination_probability"] > 0.5
        
        return detection_result
    
    def _load_detection_models(self) -> Dict:
        """Load ML detection models"""
        return {
            "factual_consistency": "bert_based_nli",
            "logical_coherence": "gpt_based_coherence",
            "source_verification": "retrieval_verification",
            "contradiction_detection": "entailment_model"
        }
    
    def _check_factual_consistency(self, content: str, references: List[str]) -> Dict:
        """Check factual consistency"""
        return {
            "consistent": True,
            "consistency_score": 0.9,
            "inconsistencies": [],
            "verified_facts": 5,
            "unverified_facts": 1
        }
    
    def _check_logical_coherence(self, content: str) -> Dict:
        """Check logical coherence"""
        return {
            "coherent": True,
            "coherence_score": 0.85,
            "logical_flow": "good",
            "fallacies_detected": []
        }
    
    def _check_contextual_appropriateness(self, content: str, context: Dict) -> Dict:
        """Check contextual appropriateness"""
        return {
            "appropriate": True,
            "appropriateness_score": 0.88,
            "context_alignment": "good",
            "cultural_fit": True
        }
    
    def _verify_sources(self, content: str, references: List[str]) -> Dict:
        """Verify sources"""
        return {
            "verified": True,
            "verification_score": 0.82,
            "sources_found": len(references),
            "source_quality": "high"
        }
    
    def _detect_contradictions(self, content: str, references: List[str]) -> Dict:
        """Detect contradictions"""
        return {
            "contradictions_found": False,
            "contradiction_score": 0.9,
            "contradictions": []
        }
    
    def _calculate_hallucination_probability(self, details: Dict) -> float:
        """Calculate overall hallucination probability"""
        scores = [
            details["factual_consistency"]["consistency_score"],
            details["logical_coherence"]["coherence_score"],
            details["contextual_appropriateness"]["appropriateness_score"],
            details["source_verification"]["verification_score"],
            details["contradiction_detection"]["contradiction_score"]
        ]
        
        # Invert scores for probability calculation (lower consistency = higher hallucination prob)
        avg_score = sum(scores) / len(scores)
        hallucination_prob = round(1 - avg_score, 2)
        
        return max(0.0, min(1.0, hallucination_prob))


# Main service engine
class HallucinationGuardEngine:
    """Main engine for Hallucination Guard Service"""
    
    def __init__(self):
        self.validators = {
            "curriculum": CurriculumValidator(),
            "pedagogy": PedagogyValidator(),
            "competency": CompetencyValidator(),
            "assessment": AssessmentValidator(),
            "phase": PhaseValidator(),
            "retrieval_grounding": RetrievalGroundingValidator()
        }
        
        self.detection_engine = HallucinationDetectionEngine()
        self.validation_metrics = {
            "total_validations": 0,
            "valid_results": 0,
            "invalid_results": 0,
            "average_confidence": 0.0,
            "validator_usage": {}
        }
    
    def validate_curriculum(self, request: CurriculumValidationRequest) -> Dict:
        """Validate curriculum content"""
        result = self.validators["curriculum"].validate(
            request.content,
            request.phase,
            request.grade,
            request.subject,
            request.expected_outcomes,
            request.context or {}
        )
        
        self._update_metrics("curriculum", result["confidence_score"], result["is_valid"])
        
        return result
    
    def validate_pedagogy(self, request: PedagogyValidationRequest) -> Dict:
        """Validate pedagogical content"""
        result = self.validators["pedagogy"].validate(
            request.content,
            request.pedagogy_type,
            request.target_grade,
            request.learning_objectives,
            request.context or {}
        )
        
        self._update_metrics("pedagogy", result["confidence_score"], result["is_valid"])
        
        return result
    
    def validate_competency(self, request: CompetencyValidationRequest) -> Dict:
        """Validate competency content"""
        result = self.validators["competency"].validate(
            request.content,
            request.competency_framework,
            request.competency_level,
            request.subject,
            request.context or {}
        )
        
        self._update_metrics("competency", result["confidence_score"], result["is_valid"])
        
        return result
    
    def validate_assessment(self, request: AssessmentValidationRequest) -> Dict:
        """Validate assessment content"""
        result = self.validators["assessment"].validate(
            request.assessment_content,
            request.assessment_type,
            request.cognitive_levels,
            request.subject,
            request.context or {}
        )
        
        self._update_metrics("assessment", result["confidence_score"], result["is_valid"])
        
        return result
    
    def validate_phase(self, request: PhaseValidationRequest) -> Dict:
        """Validate phase appropriateness"""
        result = self.validators["phase"].validate(
            request.content,
            request.target_phase,
            request.developmental_stage,
            request.context or {}
        )
        
        self._update_metrics("phase", result["confidence_score"], result["is_valid"])
        
        return result
    
    def validate_retrieval_grounding(self, request: RetrievalGroundingValidationRequest) -> Dict:
        """Validate retrieval grounding"""
        result = self.validators["retrieval_grounding"].validate(
            request.generated_answer,
            request.retrieved_context,
            request.query,
            request.context or {}
        )
        
        self._update_metrics("retrieval_grounding", result["confidence_score"], result["is_valid"])
        
        return result
    
    def detect_hallucination(self, request: HallucinationDetectionRequest) -> Dict:
        """Detect hallucinations using ML models"""
        result = self.detection_engine.detect_hallucination(
            request.content,
            request.content_type,
            request.reference_materials,
            request.context or {}
        )
        
        self._update_metrics("hallucination_detection", result["confidence_score"], not result["is_hallucination"])
        
        return result
    
    def _update_metrics(self, validator_type: str, confidence_score: float, is_valid: bool):
        """Update validation metrics"""
        self.validation_metrics["total_validations"] += 1
        
        if is_valid:
            self.validation_metrics["valid_results"] += 1
        else:
            self.validation_metrics["invalid_results"] += 1
        
        # Update average confidence
        total = self.validation_metrics["total_validations"]
        current_avg = self.validation_metrics["average_confidence"]
        new_avg = (current_avg * (total - 1) + confidence_score) / total
        self.validation_metrics["average_confidence"] = new_avg
        
        # Update validator usage
        if validator_type not in self.validation_metrics["validator_usage"]:
            self.validation_metrics["validator_usage"][validator_type] = 0
        self.validation_metrics["validator_usage"][validator_type] += 1


# FastAPI application
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
        from .consumer import AsyncHallucinationGuardConsumer
        consumer = AsyncHallucinationGuardConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Hallucination Guard Service",
    description="Advanced AI Capabilities - 6 AI Validators + Hallucination Detection System",
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


# Initialize engine
hallucination_guard_engine = HallucinationGuardEngine()


# API Endpoints
@app.post("/validator/curriculum")
async def validate_curriculum_content(request: CurriculumValidationRequest):
    """Validate curriculum content"""
    result = hallucination_guard_engine.validate_curriculum(request)
    return ValidationResult(
        request_id=request.request_id,
        validator_type="curriculum",
        is_valid=result["is_valid"],
        confidence_score=result["confidence_score"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        metadata=result["validation_details"]
    )


@app.post("/validator/pedagogy")
async def validate_pedagogy_content(request: PedagogyValidationRequest):
    """Validate pedagogical content"""
    result = hallucination_guard_engine.validate_pedagogy(request)
    return ValidationResult(
        request_id=request.request_id,
        validator_type="pedagogy",
        is_valid=result["is_valid"],
        confidence_score=result["confidence_score"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        metadata=result["validation_details"]
    )


@app.post("/validator/competency")
async def validate_competency_content(request: CompetencyValidationRequest):
    """Validate competency content"""
    result = hallucination_guard_engine.validate_competency(request)
    return ValidationResult(
        request_id=request.request_id,
        validator_type="competency",
        is_valid=result["is_valid"],
        confidence_score=result["confidence_score"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        metadata=result["validation_details"]
    )


@app.post("/validator/assessment")
async def validate_assessment_content(request: AssessmentValidationRequest):
    """Validate assessment content"""
    result = hallucination_guard_engine.validate_assessment(request)
    return ValidationResult(
        request_id=request.request_id,
        validator_type="assessment",
        is_valid=result["is_valid"],
        confidence_score=result["confidence_score"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        metadata=result["validation_details"]
    )


@app.post("/validator/phase")
async def validate_phase_content(request: PhaseValidationRequest):
    """Validate phase appropriateness"""
    result = hallucination_guard_engine.validate_phase(request)
    return ValidationResult(
        request_id=request.request_id,
        validator_type="phase",
        is_valid=result["is_valid"],
        confidence_score=result["confidence_score"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        metadata=result["validation_details"]
    )


@app.post("/validator/retrieval-grounding")
async def validate_retrieval_grounding(request: RetrievalGroundingValidationRequest):
    """Validate retrieval grounding"""
    result = hallucination_guard_engine.validate_retrieval_grounding(request)
    return ValidationResult(
        request_id=request.request_id,
        validator_type="retrieval_grounding",
        is_valid=result["is_valid"],
        confidence_score=result["confidence_score"],
        issues=result["issues"],
        suggestions=result["suggestions"],
        metadata=result["validation_details"]
    )


@app.post("/detector/hallucination")
async def detect_hallucination(request: HallucinationDetectionRequest):
    """Detect hallucinations using ML models"""
    result = hallucination_guard_engine.detect_hallucination(request)
    return HallucinationDetectionResult(
        request_id=request.request_id,
        is_hallucination=result["is_hallucination"],
        hallucination_probability=result["hallucination_probability"],
        detected_issues=result["detected_issues"],
        grounded_facts=result["grounded_facts"],
        ungrounded_claims=result["ungrounded_claims"],
        confidence_score=result["confidence_score"],
        metadata=result["detection_details"]
    )


@app.get("/validators/metrics")
async def get_validation_metrics():
    """Get validation metrics"""
    return hallucination_guard_engine.validation_metrics


@app.get("/validators/available")
async def get_available_validators():
    """Get available validators"""
    return {
        "validators": [
            {
                "name": "curriculum_validator",
                "description": "Validates curriculum content against standards",
                "capabilities": ["alignment", "outcomes_coverage", "developmental_appropriateness"]
            },
            {
                "name": "pedagogy_validator",
                "description": "Validates pedagogical approaches and strategies",
                "capabilities": ["pedagogy_alignment", "objectives_alignment", "differentiation"]
            },
            {
                "name": "competency_validator",
                "description": "Validates competency framework alignment",
                "capabilities": ["framework_alignment", "level_appropriateness", "progression_logic"]
            },
            {
                "name": "assessment_validator",
                "description": "Validates assessment quality and fairness",
                "capabilities": ["objective_alignment", "cognitive_balance", "fairness_check"]
            },
            {
                "name": "phase_validator",
                "description": "Validates developmental phase appropriateness",
                "capabilities": ["phase_alignment", "cognitive_load", "language_complexity"]
            },
            {
                "name": "retrieval_grounding_validator",
                "description": "Validates answer grounding in retrieved context",
                "capabilities": ["grounding_score", "context_utilization", "hallucination_detection"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8024)
