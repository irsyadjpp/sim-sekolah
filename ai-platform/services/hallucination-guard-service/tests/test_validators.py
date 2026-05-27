"""
Tests for Hallucination Guard Service
"""
import pytest
from datetime import datetime
from app.main import (
    HallucinationGuardEngine,
    CurriculumValidator,
    PedagogyValidator,
    CompetencyValidator,
    AssessmentValidator,
    PhaseValidator,
    RetrievalGroundingValidator,
    HallucinationDetectionEngine,
    CurriculumValidationRequest,
    PedagogyValidationRequest,
    CompetencyValidationRequest,
    AssessmentValidationRequest,
    PhaseValidationRequest,
    RetrievalGroundingValidationRequest,
    HallucinationDetectionRequest
)


@pytest.fixture
def hallucination_guard_engine():
    """Create hallucination guard engine fixture"""
    return HallucinationGuardEngine()


@pytest.fixture
def curriculum_validator():
    """Create curriculum validator fixture"""
    return CurriculumValidator()


@pytest.fixture
def pedagogy_validator():
    """Create pedagogy validator fixture"""
    return PedagogyValidator()


@pytest.fixture
def competency_validator():
    """Create competency validator fixture"""
    return CompetencyValidator()


@pytest.fixture
def assessment_validator():
    """Create assessment validator fixture"""
    return AssessmentValidator()


@pytest.fixture
def phase_validator():
    """Create phase validator fixture"""
    return PhaseValidator()


@pytest.fixture
def retrieval_grounding_validator():
    """Create retrieval grounding validator fixture"""
    return RetrievalGroundingValidator()


@pytest.fixture
def hallucination_detection_engine():
    """Create hallucination detection engine fixture"""
    return HallucinationDetectionEngine()


class TestCurriculumValidator:
    """Tests for Curriculum Validator"""

    def test_validate_curriculum_content(self, curriculum_validator):
        """Test curriculum validation"""
        result = curriculum_validator.validate(
            content="Students will learn about photosynthesis...",
            phase="C",
            grade="VII",
            subject="Science",
            expected_outcomes=["Understand photosynthesis process"],
            context={}
        )
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "issues" in result
        assert "suggestions" in result
        assert "validation_details" in result
        assert result["validation_details"]["curriculum_alignment"]["aligned"] == True

    def test_curriculum_alignment_check(self, curriculum_validator):
        """Test curriculum alignment checking"""
        alignment = curriculum_validator._check_curriculum_alignment(
            content="Photosynthesis lesson content",
            phase="C",
            grade="VII",
            subject="Science"
        )
        
        assert "aligned" in alignment
        assert "alignment_score" in alignment
        assert alignment["aligned"] == True
        assert alignment["alignment_score"] >= 0.0
        assert alignment["alignment_score"] <= 1.0


class TestPedagogyValidator:
    """Tests for Pedagogy Validator"""

    def test_validate_pedagogy_content(self, pedagogy_validator):
        """Test pedagogy validation"""
        result = pedagogy_validator.validate(
            content="Inquiry-based learning activity...",
            pedagogy_type="inquiry",
            target_grade="VII",
            learning_objectives ["Understand scientific inquiry"],
            context={}
        )
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "validation_details" in result
        assert result["validation_details"]["pedagogy_alignment"]["aligned"] == True

    def test_pedagogy_alignment_check(self, pedagogy_validator):
        """Test pedagogy alignment checking"""
        alignment = pedagogy_validator._check_pedagogy_alignment(
            content="Inquiry-based activity",
            pedagogy_type="inquiry"
        )
        
        assert "aligned" in alignment
        assert "alignment_score" in alignment
        assert alignment["aligned"] == True


class TestCompetencyValidator:
    """Tests for Competency Validator"""

    def test_validate_competency_content(self, competency_validator):
        """Test competency validation"""
        result = competency_validator.validate(
            content="Competency development activities...",
            competency_framework="Kurikulum Merdeka",
            competency_level="lanjut",
            subject="Mathematics",
            context={}
        )
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "validation_details" in result
        assert result["validation_details"]["framework_alignment"]["aligned"] == True

    def test_framework_alignment_check(self, competency_validator):
        """Test framework alignment checking"""
        alignment = competency_validator._check_framework_alignment(
            content="Competency content",
            framework="Kurikulum_Merdeka"
        )
        
        assert "aligned" in alignment
        assert "alignment_score" in alignment
        assert alignment["aligned"] == True


class TestAssessmentValidator:
    """Tests for Assessment Validator"""

    def test_validate_assessment_content(self, assessment_validator):
        """Test assessment validation"""
        result = assessment_validator.validate(
            assessment_content="Multiple choice questions...",
            assessment_type="formative",
            cognitive_levels=["understand", "apply"],
            subject="Science",
            context={}
        )
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "validation_details" in result
        assert result["validation_details"]["fairness_bias"]["fair"] == True

    def test_cognitive_balance_check(self, assessment_validator):
        """Test cognitive balance checking"""
        balance = assessment_validator._check_cognitive_balance(
            cognitive_levels=["understand", "apply", "analyze"]
        )
        
        assert "balanced" in balance
        assert "balance_score" in balance
        assert "level_distribution" in balance
        assert balance["balanced"] == True


class TestPhaseValidator:
    """Tests for Phase Validator"""

    def test_validate_phase_content(self, phase_validator):
        """Test phase validation"""
        result = phase_validator.validate(
            content="Age-appropriate learning activities...",
            target_phase="C",
            developmental_stage="formal_operational",
            context={}
        )
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "validation_details" in result
        assert result["validation_details"]["phase_alignment"]["aligned"] == True

    def test_phase_alignment_check(self, phase_validator):
        """Test phase alignment checking"""
        alignment = phase_validator._check_phase_alignment(
            content="Age-appropriate content",
            target_phase="C"
        )
        
        assert "aligned" in alignment
        assert "alignment_score" in alignment
        assert alignment["aligned"] == True


class TestRetrievalGroundingValidator:
    """Tests for Retrieval Grounding Validator"""

    def test_validate_retrieval_grounding(self, retrieval_grounding_validator):
        """Test retrieval grounding validation"""
        result = retrieval_grounding_validator.validate(
            generated_answer="Photosynthesis converts light energy to chemical energy...",
            retrieved_context=["Photosynthesis is the process by which plants convert light energy"],
            query="What is photosynthesis?",
            context={}
        )
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "validation_details" in result
        assert "grounding_score" in result["validation_details"]

    def test_grounding_score_calculation(self, retrieval_grounding_validator):
        """Test grounding score calculation"""
        score = retrieval_grounding_validator._calculate_grounding_score(
            answer="Photosynthesis occurs in chloroplasts",
            context=["Chloroplasts are the site of photosynthesis"]
        )
        
        assert "score" in score
        assert "method" in score
        assert "supported_claims" in score
        assert score["score"] >= 0.0
        assert score["score"] <= 1.0


class TestHallucinationDetectionEngine:
    """Tests for Hallucination Detection Engine"""

    def test_detect_hallucination(self, hallucination_detection_engine):
        """Test hallucination detection"""
        result = hallucination_detection_engine.detect_hallucination(
            content="Photosynthesis occurs in mitochondria...",
            content_type="science_explanation",
            reference_materials=["Photosynthesis occurs in chloroplasts"],
            context={}
        )
        
        assert "is_hallucination" in result
        assert "hallucination_probability" in result
        assert "detected_issues" in result
        assert "confidence_score" in result
        assert "detection_details" in result

    def test_factual_consistency_check(self, hallucination_detection_engine):
        """Test factual consistency checking"""
        consistency = hallucination_detection_engine._check_factual_consistency(
            content="Photosynthesis occurs in chloroplasts",
            references=["Chloroplasts are where photosynthesis occurs"]
        )
        
        assert "consistent" in consistency
        assert "consistency_score" in consistency
        assert consistency["consistent"] == True

    def test_hallucination_probability_calculation(self, hallucination_detection_engine):
        """Test hallucination probability calculation"""
        details = {
            "factual_consistency": {"consistency_score": 0.9},
            "logical_coherence": {"coherence_score": 0.85},
            "contextual_appropriateness": {"appropriateness_score": 0.88},
            "source_verification": {"verification_score": 0.82},
            "contradiction_detection": {"contradiction_score": 0.9}
        }
        
        probability = hallucination_detection_engine._calculate_hallucination_probability(details)
        
        assert probability >= 0.0
        assert probability <= 1.0


class TestHallucinationGuardEngine:
    """Tests for Hallucination Guard Engine"""

    def test_validate_curriculum(self, hallucination_guard_engine):
        """Test curriculum validation through engine"""
        request = CurriculumValidationRequest(
            content="Photosynthesis lesson content",
            phase="C",
            grade="VII",
            subject="Science",
            expected_outcomes=["Understand photosynthesis"]
        )
        
        result = hallucination_guard_engine.validate_curriculum(request)
        
        assert "is_valid" in result
        assert "confidence_score" in result
        assert "validation_details" in result

    def test_detect_hallucination_engine(self, hallucination_guard_engine):
        """Test hallucination detection through engine"""
        request = HallucinationDetectionRequest(
            content="Photosynthesis occurs in chloroplasts",
            content_type="science_explanation",
            reference_materials=["Chloroplasts are the site of photosynthesis"]
        )
        
        result = hallucination_guard_engine.detect_hallucination(request)
        
        assert "is_hallucination" in result
        assert "hallucination_probability" in result
        assert "confidence_score" in result

    def test_metrics_tracking(self, hallucination_guard_engine):
        """Test metrics tracking"""
        initial_total = hallucination_guard_engine.validation_metrics["total_validations"]
        
        request = CurriculumValidationRequest(
            content="Test content",
            phase="C",
            grade="VII",
            subject="Science"
        )
        
        hallucination_guard_engine.validate_curriculum(request)
        
        assert hallucination_guard_engine.validation_metrics["total_validations"] == initial_total + 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
