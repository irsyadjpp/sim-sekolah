"""
School Improvement Recommendation

This module generates improvement recommendations for schools based on evaluation results.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationCategory(str, Enum):
    """Categories of recommendations"""
    ACADEMIC = "academic"
    MANAGEMENT = "management"
    INFRASTRUCTURE = "infrastructure"
    TEACHER_DEVELOPMENT = "teacher_development"
    COMMUNITY = "community"
    POLICY = "policy"


class ImprovementRecommendation:
    """Generator for school improvement recommendations"""
    
    def __init__(self):
        self.recommendation_framework = self._initialize_recommendation_framework()
        self.recommendation_database = {}
    
    def generate_recommendations(
        self, 
        school_evaluation: Dict
    ) -> Dict:
        """Generate improvement recommendations based on school evaluation"""
        recommendation_id = f"improve_rec_{school_evaluation.get('school_id', '')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze evaluation results
        areas_for_improvement = school_evaluation.get("areas_for_improvement", [])
        dimension_evaluations = school_evaluation.get("dimension_evaluations", {})
        
        # Generate recommendations for each area
        recommendations = []
        for area in areas_for_improvement:
            recommendation = self._generate_area_recommendation(area, dimension_evaluations)
            recommendations.append(recommendation)
        
        # Prioritize recommendations
        prioritized_recommendations = self._prioritize_recommendations(recommendations)
        
        # Generate action plan
        action_plan = self._generate_action_plan(prioritized_recommendations)
        
        # Generate timeline
        timeline = self._generate_timeline(prioritized_recommendations)
        
        # Generate resource requirements
        resource_requirements = self._generate_resource_requirements(prioritized_recommendations)
        
        recommendation_result = {
            "recommendation_id": recommendation_id,
            "school_id": school_evaluation.get("school_id", ""),
            "school_name": school_evaluation.get("school_name", ""),
            "evaluation_id": school_evaluation.get("evaluation_id", ""),
            "recommendations": prioritized_recommendations,
            "action_plan": action_plan,
            "timeline": timeline,
            "resource_requirements": resource_requirements,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.recommendation_database[recommendation_id] = recommendation_result
        
        return recommendation_result
    
    def generate_strategic_recommendations(
        self, 
        school_data: Dict,
        swot_analysis: Dict
    ) -> Dict:
        """Generate strategic recommendations based on SWOT analysis"""
        recommendation_id = f"strategic_rec_{school_data.get('school_id', '')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate SO strategies (Strengths-Opportunities)
        so_strategies = self._generate_so_strategies(swot_analysis)
        
        # Generate WO strategies (Weaknesses-Opportunities)
        wo_strategies = self._generate_wo_strategies(swot_analysis)
        
        # Generate ST strategies (Strengths-Threats)
        st_strategies = self._generate_st_strategies(swot_analysis)
        
        # Generate WT strategies (Weaknesses-Threats)
        wt_strategies = self._generate_wt_strategies(swot_analysis)
        
        strategic_recommendations = {
            "so_strategies": so_strategies,
            "wo_strategies": wo_strategies,
            "st_strategies": st_strategies,
            "wt_strategies": wt_strategies
        }
        
        recommendation_result = {
            "recommendation_id": recommendation_id,
            "school_id": school_data.get("school_id", ""),
            "school_name": school_data.get("name", ""),
            "strategic_recommendations": strategic_recommendations,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        return recommendation_result
    
    def track_recommendation_progress(
        self, 
        school_id: str,
        recommendation_id: str
    ) -> Dict:
        """Track progress of recommendation implementation"""
        tracking_id = f"rec_track_{school_id}_{recommendation_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get recommendation data
        recommendation_data = self.recommendation_database.get(recommendation_id, {})
        
        if not recommendation_data:
            return {
                "tracking_id": tracking_id,
                "school_id": school_id,
                "error": "Recommendation not found"
            }
        
        # Get implementation status
        implementation_status = self._get_implementation_status(school_id, recommendation_id)
        
        # Calculate completion percentage
        completion_percentage = self._calculate_completion_percentage(implementation_status)
        
        # Generate progress insights
        progress_insights = self._generate_progress_insights(implementation_status)
        
        tracking_result = {
            "tracking_id": tracking_id,
            "school_id": school_id,
            "recommendation_id": recommendation_id,
            "implementation_status": implementation_status,
            "completion_percentage": completion_percentage,
            "progress_insights": progress_insights,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        return tracking_result
    
    def _generate_area_recommendation(self, area: str, dimension_evaluations: Dict) -> Dict:
        """Generate recommendation for a specific area"""
        # Determine category from area
        category = self._determine_category(area)
        
        # Determine priority
        priority = self._determine_priority(area, dimension_evaluations)
        
        # Generate recommendation text
        recommendation_text = self._generate_recommendation_text(area, category)
        
        # Generate action steps
        action_steps = self._generate_action_steps(area, category)
        
        return {
            "area": area,
            "category": category.value,
            "priority": priority.value,
            "recommendation": recommendation_text,
            "action_steps": action_steps
        }
    
    def _determine_category(self, area: str) -> RecommendationCategory:
        """Determine recommendation category from area"""
        area_lower = area.lower()
        
        if "akademik" in area_lower or "prestasi" in area_lower:
            return RecommendationCategory.ACADEMIC
        elif "manajemen" in area_lower or "administrasi" in area_lower:
            return RecommendationCategory.MANAGEMENT
        elif "infrastruktur" in area_lower or "fasilitas" in area_lower:
            return RecommendationCategory.INFRASTRUCTURE
        elif "guru" in area_lower or "teacher" in area_lower:
            return RecommendationCategory.TEACHER_DEVELOPMENT
        elif "komunitas" in area_lower or "ortu" in area_lower:
            return RecommendationCategory.COMMUNITY
        else:
            return RecommendationCategory.POLICY
    
    def _determine_priority(self, area: str, dimension_evaluations: Dict) -> RecommendationPriority:
        """Determine priority for recommendation"""
        # Extract dimension from area
        dimension = area.split(":")[0].strip() if ":" in area else area
        
        # Get dimension score
        dimension_score = dimension_evaluations.get(dimension, {}).get("score", 0.5)
        
        if dimension_score < 0.3:
            return RecommendationPriority.CRITICAL
        elif dimension_score < 0.5:
            return RecommendationPriority.HIGH
        elif dimension_score < 0.7:
            return RecommendationPriority.MEDIUM
        else:
            return RecommendationPriority.LOW
    
    def _generate_recommendation_text(self, area: str, category: RecommendationCategory) -> str:
        """Generate recommendation text"""
        recommendation_templates = {
            RecommendationCategory.ACADEMIC: f"Perbaikan diperlukan di area {area} untuk meningkatkan kinerja akademik.",
            RecommendationCategory.MANAGEMENT: f"Perbaikan manajemen diperlukan di area {area}.",
            RecommendationCategory.INFRASTRUCTURE: f"Peningkatan infrastruktur diperlukan di area {area}.",
            RecommendationCategory.TEACHER_DEVELOPMENT: f"Pengembangan guru diperlukan di area {area}.",
            RecommendationCategory.COMMUNITY: f"Peningkatan keterlibatan komunitas diperlukan di area {area}.",
            RecommendationCategory.POLICY: f"Perbaikan kebijakan diperlukan di area {area}."
        }
        
        return recommendation_templates.get(category, f"Perbaikan diperlukan di area {area}.")
    
    def _generate_action_steps(self, area: str, category: RecommendationCategory) -> List[str]:
        """Generate action steps for recommendation"""
        action_steps_map = {
            RecommendationCategory.ACADEMIC: [
                "Analisis akar masalah",
                "Kembangkan rencana perbaikan",
                "Implementasi intervensi",
                "Monitoring dan evaluasi"
            ],
            RecommendationCategory.MANAGEMENT: [
                "Review proses manajemen",
                "Kembangkan SOP baru",
                "Pelatihan staf",
                "Implementasi dan monitoring"
            ],
            RecommendationCategory.INFRASTRUCTURE: [
                "Assessment kebutuhan",
                "Anggaran dan perencanaan",
                "Pengadaan dan pembangunan",
                "Maintenance dan evaluasi"
            ],
            RecommendationCategory.TEACHER_DEVELOPMENT: [
                "Identifikasi kebutuhan pelatihan",
                "Kembangkan program pelatihan",
                "Implementasi pelatihan",
                "Evaluasi dampak"
            ],
            RecommendationCategory.COMMUNITY: [
                "Identifikasi stakeholder",
                "Kembangkan strategi keterlibatan",
                "Implementasi program",
                "Evaluasi keterlibatan"
            ],
            RecommendationCategory.POLICY: [
                "Review kebijakan existing",
                "Kembangkan kebijakan baru",
                "Sosialisasi kebijakan",
                "Implementasi dan monitoring"
            ]
        }
        
        return action_steps_map.get(category, action_steps_map[RecommendationCategory.POLICY])
    
    def _prioritize_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Prioritize recommendations by priority level"""
        priority_order = {
            RecommendationPriority.CRITICAL.value: 0,
            RecommendationPriority.HIGH.value: 1,
            RecommendationPriority.MEDIUM.value: 2,
            RecommendationPriority.LOW.value: 3
        }
        
        return sorted(
            recommendations,
            key=lambda x: priority_order.get(x["priority"], 4)
        )
    
    def _generate_action_plan(self, recommendations: List[Dict]) -> Dict:
        """Generate action plan from recommendations"""
        phases = {
            "immediate": [],
            "short_term": [],
            "medium_term": [],
            "long_term": []
        }
        
        for recommendation in recommendations:
            priority = recommendation["priority"]
            
            if priority == RecommendationPriority.CRITICAL.value:
                phases["immediate"].append(recommendation)
            elif priority == RecommendationPriority.HIGH.value:
                phases["short_term"].append(recommendation)
            elif priority == RecommendationPriority.MEDIUM.value:
                phases["medium_term"].append(recommendation)
            else:
                phases["long_term"].append(recommendation)
        
        return phases
    
    def _generate_timeline(self, recommendations: List[Dict]) -> Dict:
        """Generate timeline for recommendations"""
        timeline = {
            "immediate": "0-3 bulan",
            "short_term": "3-6 bulan",
            "medium_term": "6-12 bulan",
            "long_term": "1-3 tahun"
        }
        
        return timeline
    
    def _generate_resource_requirements(self, recommendations: List[Dict]) -> Dict:
        """Generate resource requirements for recommendations"""
        resources = {
            "human_resources": [],
            "financial_resources": [],
            "material_resources": [],
            "time_resources": []
        }
        
        for recommendation in recommendations:
            category = recommendation["category"]
            
            if category == RecommendationCategory.ACADEMIC.value:
                resources["human_resources"].append("Guru mata pelajaran")
                resources["financial_resources"].append("Dana pembelajaran")
            elif category == RecommendationCategory.INFRASTRUCTURE.value:
                resources["financial_resources"].append("Dana pembangunan")
                resources["material_resources"].append("Peralatan dan fasilitas")
            elif category == RecommendationCategory.TEACHER_DEVELOPMENT.value:
                resources["human_resources"].append("Trainer dan fasilitator")
                resources["financial_resources"].append("Dana pelatihan")
        
        return resources
    
    def _generate_so_strategies(self, swot_analysis: Dict) -> List[str]:
        """Generate SO strategies (Strengths-Opportunities)"""
        strengths = swot_analysis.get("strengths", [])
        opportunities = swot_analysis.get("opportunities", [])
        
        strategies = []
        if strengths and opportunities:
            strategies.append(f"Manfaatkan {strengths[0]} untuk memanfaatkan {opportunities[0]}")
            strategies.append("Kembangkan program berbasis kekuatan untuk memaksimalkan peluang")
        
        return strategies
    
    def _generate_wo_strategies(self, swot_analysis: Dict) -> List[str]:
        """Generate WO strategies (Weaknesses-Opportunities)"""
        weaknesses = swot_analysis.get("weaknesses", [])
        opportunities = swot_analysis.get("opportunities", [])
        
        strategies = []
        if weaknesses and opportunities:
            strategies.append(f"Perbaiki {weaknesses[0]} untuk memanfaatkan {opportunities[0]}")
            strategies.append("Kembangkan strategi untuk mengatasi kelemahan melalui peluang")
        
        return strategies
    
    def _generate_st_strategies(self, swot_analysis: Dict) -> List[str]:
        """Generate ST strategies (Strengths-Threats)"""
        strengths = swot_analysis.get("strengths", [])
        threats = swot_analysis.get("threats", [])
        
        strategies = []
        if strengths and threats:
            strategies.append(f"Gunakan {strengths[0]} untuk mengatasi {threats[0]}")
            strategies.append("Kembangkan strategi pertahanan berbasis kekuatan")
        
        return strategies
    
    def _generate_wt_strategies(self, swot_analysis: Dict) -> List[str]:
        """Generate WT strategies (Weaknesses-Threats)"""
        weaknesses = swot_analysis.get("weaknesses", [])
        threats = swot_analysis.get("threats", [])
        
        strategies = []
        if weaknesses and threats:
            strategies.append(f"Minimalkan {weaknesses[0]} untuk mengurangi dampak {threats[0]}")
            strategies.append("Kembangkan strategi mitigasi untuk kelemahan dan ancaman")
        
        return strategies
    
    def _get_implementation_status(self, school_id: str, recommendation_id: str) -> Dict:
        """Get implementation status for recommendations"""
        # In real implementation, would retrieve from database
        return {}
    
    def _calculate_completion_percentage(self, implementation_status: Dict) -> float:
        """Calculate completion percentage"""
        # Simplified calculation
        return 0.0
    
    def _generate_progress_insights(self, implementation_status: Dict) -> List[str]:
        """Generate progress insights"""
        return ["Implementasi rekomendasi sedang berlangsung"]
    
    def _initialize_recommendation_framework(self) -> Dict:
        """Initialize recommendation framework"""
        return {
            RecommendationCategory.ACADEMIC: {
                "description": "Rekomendasi akademik",
                "focus_areas": ["prestasi", "kurikulum", "assessment"]
            },
            RecommendationCategory.MANAGEMENT: {
                "description": "Rekomendasi manajemen",
                "focus_areas": ["kepemimpinan", "administrasi", "perencanaan"]
            },
            RecommendationCategory.INFRASTRUCTURE: {
                "description": "Rekomendasi infrastruktur",
                "focus_areas": ["fasilitas", "peralatan", "maintenance"]
            },
            RecommendationCategory.TEACHER_DEVELOPMENT: {
                "description": "Rekomendasi pengembangan guru",
                "focus_areas": ["pelatihan", "profesionalisme", "kompetensi"]
            },
            RecommendationCategory.COMMUNITY: {
                "description": "Rekomendasi komunitas",
                "focus_areas": ["keterlibatan_ortu", "kerjasama", "transparansi"]
            },
            RecommendationCategory.POLICY: {
                "description": "Rekomendasi kebijakan",
                "focus_areas": ["kurikulum", "disiplin", "evaluasi"]
            }
        }
