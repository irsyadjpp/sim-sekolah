"""
School Evaluation Engine

This module handles comprehensive school evaluation aligned with Indonesian education standards.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class EvaluationDimension(str, Enum):
    """Dimensions of school evaluation"""
    ACADEMIC_PERFORMANCE = "academic_performance"
    TEACHER_QUALITY = "teacher_quality"
    LEARNING_ENVIRONMENT = "learning_environment"
    SCHOOL_MANAGEMENT = "school_management"
    COMMUNITY_ENGAGEMENT = "community_engagement"
    INFRASTRUCTURE = "infrastructure"


class EvaluationStandard(str, Enum):
    """Evaluation standards"""
    EXCELLENT = "excellent"
    VERY_GOOD = "very_good"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_IMPROVEMENT = "needs_improvement"


class EvaluationEngine:
    """Engine for comprehensive school evaluation"""
    
    def __init__(self):
        self.evaluation_criteria = self._initialize_evaluation_criteria()
        self.evaluation_database = {}
    
    def evaluate_school(
        self, 
        school_data: Dict,
        evaluation_period: str
    ) -> Dict:
        """Evaluate school comprehensively"""
        evaluation_id = f"school_eval_{school_data.get('school_id', '')}_{evaluation_period}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Evaluate each dimension
        dimension_evaluations = {}
        for dimension in EvaluationDimension:
            dimension_evaluations[dimension.value] = self._evaluate_dimension(
                dimension,
                school_data.get(dimension.value, {})
            )
        
        # Calculate overall school rating
        overall_rating = self._calculate_overall_rating(dimension_evaluations)
        
        # Generate evaluation summary
        evaluation_summary = self._generate_evaluation_summary(
            dimension_evaluations,
            overall_rating
        )
        
        # Identify strengths and areas for improvement
        strengths = self._identify_strengths(dimension_evaluations)
        areas_for_improvement = self._identify_areas_for_improvement(dimension_evaluations)
        
        evaluation_result = {
            "evaluation_id": evaluation_id,
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("name", ""),
            "evaluation_period": evaluation_period,
            "dimension_evaluations": dimension_evaluations,
            "overall_rating": overall_rating,
            "evaluation_summary": evaluation_summary,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "evaluated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.evaluation_database[evaluation_id] = evaluation_result
        
        return evaluation_result
    
    def track_evaluation_progression(
        self, 
        school_id: str, 
        timeframe: str = "year"
    ) -> Dict:
        """Track school evaluation progression over time"""
        tracking_id = f"eval_track_{school_id}_{timeframe}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get evaluation history
        evaluation_history = self._get_evaluation_history(school_id, timeframe)
        
        if not evaluation_history:
            return {
                "tracking_id": tracking_id,
                "school_id": school_id,
                "error": "No evaluation history found"
            }
        
        # Analyze rating progression
        rating_progression = self._analyze_rating_progression(evaluation_history)
        
        # Analyze dimension progression
        dimension_progression = self._analyze_dimension_progression(evaluation_history)
        
        # Generate progression insights
        progression_insights = self._generate_progression_insights(
            rating_progression,
            dimension_progression
        )
        
        tracking_result = {
            "tracking_id": tracking_id,
            "school_id": school_id,
            "timeframe": timeframe,
            "evaluation_history": evaluation_history,
            "rating_progression": rating_progression,
            "dimension_progression": dimension_progression,
            "progression_insights": progression_insights,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        return tracking_result
    
    def evaluate_dimension(
        self, 
        dimension: EvaluationDimension, 
        dimension_data: Dict
    ) -> Dict:
        """Evaluate a specific school dimension"""
        # Calculate dimension score
        score = self._calculate_dimension_score(dimension_data)
        
        # Determine evaluation standard
        standard = self._determine_evaluation_standard(score)
        
        # Identify dimension strengths
        strengths = dimension_data.get("strengths", [])
        
        # Identify dimension areas for improvement
        areas_for_improvement = dimension_data.get("areas_for_improvement", [])
        
        return {
            "dimension": dimension.value,
            "score": score,
            "standard": standard.value,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement
        }
    
    def _calculate_dimension_score(self, dimension_data: Dict) -> float:
        """Calculate score for a dimension"""
        indicators = dimension_data.get("indicators", {})
        
        if not indicators:
            return 0.5
        
        scores = [indicators.get(indicator, 0.5) for indicator in indicators.keys()]
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def _determine_evaluation_standard(self, score: float) -> EvaluationStandard:
        """Determine evaluation standard from score"""
        if score >= 0.9:
            return EvaluationStandard.EXCELLENT
        elif score >= 0.8:
            return EvaluationStandard.VERY_GOOD
        elif score >= 0.7:
            return EvaluationStandard.GOOD
        elif score >= 0.5:
            return EvaluationStandard.FAIR
        else:
            return EvaluationStandard.NEEDS_IMPROVEMENT
    
    def _calculate_overall_rating(self, dimension_evaluations: Dict) -> Dict:
        """Calculate overall school rating"""
        scores = [evaluation["score"] for evaluation in dimension_evaluations.values()]
        
        if not scores:
            return {"standard": EvaluationStandard.FAIR.value, "score": 0.5}
        
        average_score = sum(scores) / len(scores)
        standard = self._determine_evaluation_standard(average_score)
        
        return {
            "standard": standard.value,
            "score": average_score,
            "dimension_scores": dimension_evaluations
        }
    
    def _generate_evaluation_summary(
        self, 
        dimension_evaluations: Dict, 
        overall_rating: Dict
    ) -> str:
        """Generate evaluation summary"""
        standard = overall_rating["standard"]
        
        summary_map = {
            EvaluationStandard.EXCELLENT.value: "Sekolah menunjukkan kinerja yang sangat baik di semua dimensi evaluasi.",
            EvaluationStandard.VERY_GOOD.value: "Sekolah menunjukkan kinerja yang sangat baik dengan beberapa area yang dapat ditingkatkan.",
            EvaluationStandard.GOOD.value: "Sekolah menunjukkan kinerja yang baik dengan beberapa area yang perlu ditingkatkan.",
            EvaluationStandard.FAIR.value: "Sekolah menunjukkan kinerja yang cukup dengan beberapa area yang memerlukan perhatian.",
            EvaluationStandard.NEEDS_IMPROVEMENT.value: "Sekolah memerlukan perbaikan signifikan di berbagai dimensi."
        }
        
        return summary_map.get(standard, summary_map[EvaluationStandard.FAIR.value])
    
    def _identify_strengths(self, dimension_evaluations: Dict) -> List[str]:
        """Identify school strengths"""
        strengths = []
        
        for dimension, evaluation in dimension_evaluations.items():
            if evaluation["score"] >= 0.7:
                for strength in evaluation["strengths"]:
                    strengths.append(f"{dimension}: {strength}")
        
        return strengths
    
    def _identify_areas_for_improvement(self, dimension_evaluations: Dict) -> List[str]:
        """Identify areas for improvement"""
        areas = []
        
        for dimension, evaluation in dimension_evaluations.items():
            if evaluation["score"] < 0.6:
                for area in evaluation["areas_for_improvement"]:
                    areas.append(f"{dimension}: {area}")
        
        return areas
    
    def _get_evaluation_history(self, school_id: str, timeframe: str) -> List[Dict]:
        """Get evaluation history for school"""
        # In real implementation, would retrieve from database
        return []
    
    def _analyze_rating_progression(self, evaluation_history: List[Dict]) -> Dict:
        """Analyze progression of overall ratings"""
        if len(evaluation_history) < 2:
            return {"progression": "insufficient_data"}
        
        standards = [e.get("overall_rating", {}).get("standard", "fair") for e in evaluation_history]
        
        standard_order = ["needs_improvement", "fair", "good", "very_good", "excellent"]
        
        early_standard_index = standard_order.index(standards[0]) if standards[0] in standard_order else 2
        recent_standard_index = standard_order.index(standards[-1]) if standards[-1] in standard_order else 2
        
        progression_type = "improving" if recent_standard_index > early_standard_index else "stable" if recent_standard_index == early_standard_index else "declining"
        
        return {
            "progression": progression_type,
            "early_standard": standards[0],
            "recent_standard": standards[-1],
            "standard_improvement": recent_standard_index - early_standard_index
        }
    
    def _analyze_dimension_progression(self, evaluation_history: List[Dict]) -> Dict:
        """Analyze progression across dimensions"""
        dimension_progression = {}
        
        for dimension in EvaluationDimension:
            dimension_name = dimension.value
            scores = [
                e.get("dimension_evaluations", {}).get(dimension_name, {}).get("score", 0.5)
                for e in evaluation_history
            ]
            
            if scores:
                dimension_progression[dimension_name] = {
                    "early_score": scores[0],
                    "recent_score": scores[-1],
                    "improvement": scores[-1] - scores[0],
                    "trend": "improving" if scores[-1] > scores[0] else "stable" if scores[-1] == scores[0] else "declining"
                }
        
        return dimension_progression
    
    def _generate_progression_insights(self, rating_progression: Dict, dimension_progression: Dict) -> List[str]:
        """Generate insights from evaluation progression"""
        insights = []
        
        progression = rating_progression.get("progression")
        if progression == "improving":
            insights.append("Kinerja sekolah meningkat seiring waktu")
        elif progression == "stable":
            insights.append("Kinerja sekolah stabil - pertimbangkan inisiatif baru")
        elif progression == "declining":
            insights.append("Kinerja sekolah menurun - perlu intervensi")
        
        for dimension, data in dimension_progression.items():
            if data.get("trend") == "improving":
                insights.append(f"Dimensi {dimension} meningkat dengan baik")
            elif data.get("trend") == "declining":
                insights.append(f"Dimensi {dimension} perlu perhatian")
        
        return insights
    
    def _initialize_evaluation_criteria(self) -> Dict:
        """Initialize evaluation criteria"""
        return {
            EvaluationDimension.ACADEMIC_PERFORMANCE.value: {
                "description": "Kinerja akademik sekolah",
                "indicators": ["prestasi_siswa", "kelulusan", "pencapaian_kurikulum"]
            },
            EvaluationDimension.TEACHER_QUALITY.value: {
                "description": "Kualitas guru dan staf pengajar",
                "indicators": ["kualifikasi_guru", "kompetensi_pedagogik", "profesionalisme"]
            },
            EvaluationDimension.LEARNING_ENVIRONMENT.value: {
                "description": "Lingkungan pembelajaran",
                "indicators": ["iklim_sekolah", "budaya_belajar", "disiplin"]
            },
            EvaluationDimension.SCHOOL_MANAGEMENT.value: {
                "description": "Manajemen sekolah",
                "indicators": ["kepemimpinan", "administrasi", "perencanaan"]
            },
            EvaluationDimension.COMMUNITY_ENGAGEMENT.value: {
                "description": "Keterlibatan komunitas",
                "indicators": ["keterlibatan_ortu", "kerjasama_komunitas", "transparansi"]
            },
            EvaluationDimension.INFRASTRUCTURE.value: {
                "description": "Infrastruktur dan fasilitas",
                "indicators": ["fasilitas_pembelajaran", "peralatan", "kondisi_gedung"]
            }
        }
