"""
Contextual Learning Validator

This module validates whether learning activities and materials demonstrate contextual learning
according to Pembelajaran Mendalam principles.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ContextualLearningIndicator(str, Enum):
    """Indicators of contextual learning"""
    LOCAL_CONTEXT = "local_context"  # Uses local context and culture
    REAL_WORLD_RELEVANCE = "real_world_relevance"  # Relevant to real-world situations
    CULTURAL_INTEGRATION = "cultural_integration"  # Integrates cultural elements
    COMMUNITY_CONNECTION = "community_connection"  # Connects to community
    ENVIRONMENTAL_AWARENESS = "environmental_awareness"  # Includes environmental context
    SITUATIONAL_AUTHENTICITY = "situational_authenticity"  # Uses authentic situations


class ValidationStatus(str, Enum):
    """Validation status"""
    VALID = "valid"
    PARTIALLY_VALID = "partially_valid"
    INVALID = "invalid"
    NEEDS_IMPROVEMENT = "needs_improvement"


class ContextualLearningValidator:
    """Validator for contextual learning principles"""
    
    def __init__(self):
        self.validation_criteria = self._initialize_validation_criteria()
        self.validation_database = {}
    
    def validate_learning_activity(
        self, 
        activity_data: Dict
    ) -> Dict:
        """Validate a learning activity for contextual learning"""
        validation_id = f"cl_validate_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Assess each contextual learning indicator
        indicator_assessments = {}
        for indicator in ContextualLearningIndicator:
            indicator_assessments[indicator.value] = self._assess_indicator(
                indicator,
                activity_data
            )
        
        # Calculate overall validation score
        overall_score = self._calculate_overall_score(indicator_assessments)
        
        # Determine validation status
        validation_status = self._determine_validation_status(overall_score)
        
        # Generate validation feedback
        feedback = self._generate_validation_feedback(
            indicator_assessments,
            validation_status
        )
        
        # Generate improvement recommendations
        recommendations = self._generate_improvement_recommendations(
            indicator_assessments
        )
        
        validation_result = {
            "validation_id": validation_id,
            "activity_data": activity_data,
            "indicator_assessments": indicator_assessments,
            "overall_score": overall_score,
            "validation_status": validation_status.value,
            "feedback": feedback,
            "recommendations": recommendations,
            "validated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.validation_database[validation_id] = validation_result
        
        return validation_result
    
    def validate_learning_material(
        self, 
        material_data: Dict
    ) -> Dict:
        """Validate learning material for contextual learning"""
        validation_id = f"cl_material_validate_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Assess each contextual learning indicator
        indicator_assessments = {}
        for indicator in ContextualLearningIndicator:
            indicator_assessments[indicator.value] = self._assess_material_indicator(
                indicator,
                material_data
            )
        
        # Calculate overall validation score
        overall_score = self._calculate_overall_score(indicator_assessments)
        
        # Determine validation status
        validation_status = self._determine_validation_status(overall_score)
        
        # Generate validation feedback
        feedback = self._generate_validation_feedback(
            indicator_assessments,
            validation_status
        )
        
        # Generate improvement recommendations
        recommendations = self._generate_improvement_recommendations(
            indicator_assessments
        )
        
        validation_result = {
            "validation_id": validation_id,
            "material_data": material_data,
            "indicator_assessments": indicator_assessments,
            "overall_score": overall_score,
            "validation_status": validation_status.value,
            "feedback": feedback,
            "recommendations": recommendations,
            "validated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.validation_database[validation_id] = validation_result
        
        return validation_result
    
    def validate_batch_activities(
        self, 
        activities: List[Dict]
    ) -> Dict:
        """Validate a batch of learning activities"""
        batch_id = f"cl_batch_validate_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Validate each activity
        individual_validations = [
            self.validate_learning_activity(activity)
            for activity in activities
        ]
        
        # Calculate batch statistics
        batch_statistics = self._calculate_batch_statistics(individual_validations)
        
        # Identify common patterns
        common_patterns = self._identify_common_patterns(individual_validations)
        
        # Generate batch recommendations
        batch_recommendations = self._generate_batch_recommendations(batch_statistics)
        
        batch_result = {
            "batch_id": batch_id,
            "total_activities": len(activities),
            "individual_validations": individual_validations,
            "batch_statistics": batch_statistics,
            "common_patterns": common_patterns,
            "batch_recommendations": batch_recommendations,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        return batch_result
    
    def _assess_indicator(
        self, 
        indicator: ContextualLearningIndicator, 
        activity_data: Dict
    ) -> Dict:
        """Assess a contextual learning indicator for an activity"""
        indicator_data = activity_data.get(indicator.value, {})
        
        # Calculate indicator score
        score = self._calculate_indicator_score(indicator, indicator_data)
        
        # Determine indicator level
        level = self._determine_indicator_level(score)
        
        # Generate indicator feedback
        feedback = self._generate_indicator_feedback(indicator, level)
        
        return {
            "indicator": indicator.value,
            "score": score,
            "level": level,
            "feedback": feedback,
            "evidence": indicator_data
        }
    
    def _assess_material_indicator(
        self, 
        indicator: ContextualLearningIndicator, 
        material_data: Dict
    ) -> Dict:
        """Assess a contextual learning indicator for a material"""
        indicator_data = material_data.get(indicator.value, {})
        
        # Calculate indicator score
        score = self._calculate_material_indicator_score(indicator, indicator_data)
        
        # Determine indicator level
        level = self._determine_indicator_level(score)
        
        # Generate indicator feedback
        feedback = self._generate_indicator_feedback(indicator, level)
        
        return {
            "indicator": indicator.value,
            "score": score,
            "level": level,
            "feedback": feedback,
            "evidence": indicator_data
        }
    
    def _calculate_indicator_score(self, indicator: ContextualLearningIndicator, indicator_data: Dict) -> float:
        """Calculate score for an activity indicator"""
        # Simplified calculation - in production would use more sophisticated analysis
        presence = indicator_data.get("presence", "none")
        quality = indicator_data.get("quality", "low")
        
        presence_scores = {
            "none": 0.0,
            "minimal": 0.3,
            "moderate": 0.6,
            "strong": 0.9,
            "excellent": 1.0
        }
        
        quality_scores = {
            "low": 0.2,
            "moderate": 0.5,
            "high": 0.8,
            "excellent": 1.0
        }
        
        presence_score = presence_scores.get(presence, 0.0)
        quality_score = quality_scores.get(quality, 0.5)
        
        # Weight presence more heavily
        return (presence_score * 0.7) + (quality_score * 0.3)
    
    def _calculate_material_indicator_score(self, indicator: ContextualLearningIndicator, indicator_data: Dict) -> float:
        """Calculate score for a material indicator"""
        # Similar to activity indicator but adapted for materials
        presence = indicator_data.get("presence", "none")
        integration = indicator_data.get("integration", "low")
        
        presence_scores = {
            "none": 0.0,
            "minimal": 0.3,
            "moderate": 0.6,
            "strong": 0.9,
            "excellent": 1.0
        }
        
        integration_scores = {
            "low": 0.2,
            "moderate": 0.5,
            "high": 0.8,
            "excellent": 1.0
        }
        
        presence_score = presence_scores.get(presence, 0.0)
        integration_score = integration_scores.get(integration, 0.5)
        
        return (presence_score * 0.6) + (integration_score * 0.4)
    
    def _determine_indicator_level(self, score: float) -> str:
        """Determine level from score"""
        if score >= 0.8:
            return "excellent"
        elif score >= 0.6:
            return "good"
        elif score >= 0.4:
            return "moderate"
        elif score >= 0.2:
            return "minimal"
        else:
            return "none"
    
    def _generate_indicator_feedback(self, indicator: ContextualLearningIndicator, level: str) -> str:
        """Generate feedback for indicator"""
        feedback_map = {
            "excellent": f"Excellent demonstration of {indicator.value}",
            "good": f"Good demonstration of {indicator.value}",
            "moderate": f"Moderate demonstration of {indicator.value}",
            "minimal": f"Minimal demonstration of {indicator.value}",
            "none": f"No demonstration of {indicator.value}"
        }
        
        return feedback_map.get(level, "Continue developing this indicator")
    
    def _calculate_overall_score(self, indicator_assessments: Dict) -> float:
        """Calculate overall validation score"""
        scores = [assessment["score"] for assessment in indicator_assessments.values()]
        
        if not scores:
            return 0.0
        
        return sum(scores) / len(scores)
    
    def _determine_validation_status(self, overall_score: float) -> ValidationStatus:
        """Determine validation status from score"""
        if overall_score >= 0.8:
            return ValidationStatus.VALID
        elif overall_score >= 0.6:
            return ValidationStatus.PARTIALLY_VALID
        elif overall_score >= 0.4:
            return ValidationStatus.NEEDS_IMPROVEMENT
        else:
            return ValidationStatus.INVALID
    
    def _generate_validation_feedback(
        self, 
        indicator_assessments: Dict, 
        validation_status: ValidationStatus
    ) -> Dict:
        """Generate validation feedback"""
        strengths = [
            indicator for indicator, assessment in indicator_assessments.items()
            if assessment["score"] >= 0.7
        ]
        
        weaknesses = [
            indicator for indicator, assessment in indicator_assessments.items()
            if assessment["score"] < 0.4
        ]
        
        feedback_map = {
            ValidationStatus.VALID: {
                "message": "Activity demonstrates contextual learning principles",
                "strengths": strengths,
                "weaknesses": weaknesses,
                "overall": "Excellent alignment with contextual learning"
            },
            ValidationStatus.PARTIALLY_VALID: {
                "message": "Activity partially demonstrates contextual learning",
                "strengths": strengths,
                "weaknesses": weaknesses,
                "overall": "Good alignment with some improvements needed"
            },
            ValidationStatus.NEEDS_IMPROVEMENT: {
                "message": "Activity needs improvement for contextual learning",
                "strengths": strengths,
                "weaknesses": weaknesses,
                "overall": "Moderate alignment requiring development"
            },
            ValidationStatus.INVALID: {
                "message": "Activity does not demonstrate contextual learning",
                "strengths": strengths,
                "weaknesses": weaknesses,
                "overall": "Poor alignment requiring significant revision"
            }
        }
        
        return feedback_map.get(validation_status, feedback_map[ValidationStatus.NEEDS_IMPROVEMENT])
    
    def _generate_improvement_recommendations(self, indicator_assessments: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        for indicator, assessment in indicator_assessments.items():
            if assessment["score"] < 0.5:
                recommendations.append(f"Enhance {indicator} in the activity")
        
        if not recommendations:
            recommendations.append("Continue current approach to contextual learning")
        
        return recommendations
    
    def _calculate_batch_statistics(self, validations: List[Dict]) -> Dict:
        """Calculate statistics for batch validation"""
        total = len(validations)
        
        valid_count = sum(1 for v in validations if v["validation_status"] == ValidationStatus.VALID.value)
        partially_valid_count = sum(1 for v in validations if v["validation_status"] == ValidationStatus.PARTIALLY_VALID.value)
        needs_improvement_count = sum(1 for v in validations if v["validation_status"] == ValidationStatus.NEEDS_IMPROVEMENT.value)
        invalid_count = sum(1 for v in validations if v["validation_status"] == ValidationStatus.INVALID.value)
        
        average_score = sum(v["overall_score"] for v in validations) / total if total > 0 else 0.0
        
        return {
            "total_activities": total,
            "valid_count": valid_count,
            "partially_valid_count": partially_valid_count,
            "needs_improvement_count": needs_improvement_count,
            "invalid_count": invalid_count,
            "average_score": average_score,
            "valid_percentage": (valid_count / total * 100) if total > 0 else 0
        }
    
    def _identify_common_patterns(self, validations: List[Dict]) -> Dict:
        """Identify common patterns across validations"""
        indicator_scores = {}
        
        for validation in validations:
            for indicator, assessment in validation["indicator_assessments"].items():
                if indicator not in indicator_scores:
                    indicator_scores[indicator] = []
                indicator_scores[indicator].append(assessment["score"])
        
        common_patterns = {}
        for indicator, scores in indicator_scores.items():
            average = sum(scores) / len(scores)
            common_patterns[indicator] = {
                "average_score": average,
                "level": "strong" if average >= 0.7 else "moderate" if average >= 0.5 else "weak"
            }
        
        return common_patterns
    
    def _generate_batch_recommendations(self, batch_statistics: Dict) -> List[str]:
        """Generate batch-level recommendations"""
        recommendations = []
        
        valid_percentage = batch_statistics.get("valid_percentage", 0)
        
        if valid_percentage >= 80:
            recommendations.append("Overall strong alignment with contextual learning")
        elif valid_percentage >= 60:
            recommendations.append("Good alignment with some activities needing improvement")
        elif valid_percentage >= 40:
            recommendations.append("Moderate alignment requiring targeted improvements")
        else:
            recommendations.append("Significant revision needed across activities")
        
        return recommendations
    
    def _initialize_validation_criteria(self) -> Dict:
        """Initialize validation criteria for contextual learning"""
        return {
            ContextualLearningIndicator.LOCAL_CONTEXT.value: {
                "description": "Uses local context and culture",
                "criteria": ["incorporates local culture", "uses local examples", "reflects local context"]
            },
            ContextualLearningIndicator.REAL_WORLD_RELEVANCE.value: {
                "description": "Relevant to real-world situations",
                "criteria": ["real-world applications", "authentic problems", "practical contexts"]
            },
            ContextualLearningIndicator.CULTURAL_INTEGRATION.value: {
                "description": "Integrates cultural elements",
                "criteria": ["cultural references", "cultural practices", "cultural values"]
            },
            ContextualLearningIndicator.COMMUNITY_CONNECTION.value: {
                "description": "Connects to community",
                "criteria": ["community involvement", "local community resources", "community issues"]
            },
            ContextualLearningIndicator.ENVIRONMENTAL_AWARENESS.value: {
                "description": "Includes environmental context",
                "criteria": ["environmental issues", "local environment", "sustainability"]
            },
            ContextualLearningIndicator.SITUATIONAL_AUTHENTICITY.value: {
                "description": "Uses authentic situations",
                "criteria": ["authentic scenarios", "real situations", "genuine contexts"]
            }
        }
