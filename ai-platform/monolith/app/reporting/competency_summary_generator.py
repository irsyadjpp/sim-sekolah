"""
Competency Summary Generator

This module generates competency summaries for students aligned with Kurikulum Merdeka.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class CompetencyDomain(str, Enum):
    """Domains of competency"""
    ACADEMIC = "academic"
    CHARACTER = "character"
    SKILLS = "skills"
    SOCIAL_EMOTIONAL = "social_emotional"
    METACOGNITIVE = "metacognitive"


class CompetencyLevel(str, Enum):
    """Levels of competency"""
    EXCELLENT = "excellent"
    PROFICIENT = "proficient"
    DEVELOPING = "developing"
    EMERGING = "emerging"
    NEEDS_SUPPORT = "needs_support"


class CompetencySummaryGenerator:
    """Generator for competency summaries"""
    
    def __init__(self):
        self.competency_framework = self._initialize_competency_framework()
        self.summary_database = {}
    
    def generate_competency_summary(
        self, 
        student_data: Dict,
        competency_data: Dict
    ) -> Dict:
        """Generate comprehensive competency summary"""
        summary_id = f"comp_summary_{student_data.get('student_id', '')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate competency assessment for each domain
        domain_assessments = {}
        for domain in CompetencyDomain:
            domain_assessments[domain.value] = self._assess_domain(
                domain,
                competency_data.get(domain.value, {})
            )
        
        # Calculate overall competency level
        overall_competency = self._calculate_overall_competency(domain_assessments)
        
        # Generate competency profile
        competency_profile = self._generate_competency_profile(domain_assessments)
        
        # Generate recommendations
        recommendations = self._generate_competency_recommendations(domain_assessments)
        
        # Generate summary narrative
        summary_narrative = self._generate_summary_narrative(
            student_data,
            competency_profile,
            recommendations
        )
        
        summary_result = {
            "summary_id": summary_id,
            "student_id": student_data.get("student_id", ""),
            "student_name": student_data.get("name", ""),
            "domain_assessments": domain_assessments,
            "overall_competency": overall_competency,
            "competency_profile": competency_profile,
            "recommendations": recommendations,
            "summary_narrative": summary_narrative,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.summary_database[summary_id] = summary_result
        
        return summary_result
    
    def generate_class_competency_summary(
        self, 
        class_data: Dict,
        students_competency_data: List[Dict]
    ) -> Dict:
        """Generate competency summary for a class"""
        summary_id = f"class_comp_summary_{class_data.get('class_id', '')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Aggregate competency data for class
        class_competency = self._aggregate_class_competency(students_competency_data)
        
        # Identify class strengths and areas for development
        class_analysis = self._analyze_class_competency(class_competency)
        
        # Generate class recommendations
        class_recommendations = self._generate_class_recommendations(class_analysis)
        
        summary_result = {
            "summary_id": summary_id,
            "class_id": class_data.get("class_id", ""),
            "class_name": class_data.get("class_name", ""),
            "total_students": len(students_competency_data),
            "class_competency": class_competency,
            "class_analysis": class_analysis,
            "class_recommendations": class_recommendations,
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        return summary_result
    
    def track_competency_progression(
        self, 
        student_id: str, 
        timeframe: str = "semester"
    ) -> Dict:
        """Track competency progression over time"""
        tracking_id = f"comp_track_{student_id}_{timeframe}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get competency history
        competency_history = self._get_competency_history(student_id, timeframe)
        
        if not competency_history:
            return {
                "tracking_id": tracking_id,
                "student_id": student_id,
                "error": "No competency history found"
            }
        
        # Analyze domain progression
        domain_progression = self._analyze_domain_progression(competency_history)
        
        # Analyze overall progression
        overall_progression = self._analyze_overall_progression(competency_history)
        
        # Generate progression insights
        progression_insights = self._generate_progression_insights(
            domain_progression,
            overall_progression
        )
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "timeframe": timeframe,
            "competency_history": competency_history,
            "domain_progression": domain_progression,
            "overall_progression": overall_progression,
            "progression_insights": progression_insights,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        return tracking_result
    
    def _assess_domain(self, domain: CompetencyDomain, domain_data: Dict) -> Dict:
        """Assess competency in a specific domain"""
        # Calculate domain score
        score = self._calculate_domain_score(domain_data)
        
        # Determine competency level
        level = self._determine_competency_level(score)
        
        # Identify strengths within domain
        strengths = domain_data.get("strengths", [])
        
        # Identify areas for development within domain
        areas_for_development = domain_data.get("areas_for_development", [])
        
        return {
            "domain": domain.value,
            "score": score,
            "level": level,
            "strengths": strengths,
            "areas_for_development": areas_for_development
        }
    
    def _calculate_domain_score(self, domain_data: Dict) -> float:
        """Calculate competency score for a domain"""
        # Simplified calculation - in production would use more sophisticated analysis
        indicators = domain_data.get("indicators", {})
        
        if not indicators:
            return 0.5
        
        scores = [indicators.get(indicator, 0.5) for indicator in indicators.keys()]
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def _determine_competency_level(self, score: float) -> CompetencyLevel:
        """Determine competency level from score"""
        if score >= 0.9:
            return CompetencyLevel.EXCELLENT
        elif score >= 0.75:
            return CompetencyLevel.PROFICIENT
        elif score >= 0.5:
            return CompetencyLevel.DEVELOPING
        elif score >= 0.3:
            return CompetencyLevel.EMERGING
        else:
            return CompetencyLevel.NEEDS_SUPPORT
    
    def _calculate_overall_competency(self, domain_assessments: Dict) -> Dict:
        """Calculate overall competency level"""
        scores = [assessment["score"] for assessment in domain_assessments.values()]
        
        if not scores:
            return {"level": CompetencyLevel.DEVELOPING.value, "score": 0.5}
        
        average_score = sum(scores) / len(scores)
        level = self._determine_competency_level(average_score)
        
        return {
            "level": level.value,
            "score": average_score,
            "domain_scores": domain_assessments
        }
    
    def _generate_competency_profile(self, domain_assessments: Dict) -> Dict:
        """Generate competency profile"""
        strengths = []
        areas_for_development = []
        
        for domain, assessment in domain_assessments.items():
            if assessment["score"] >= 0.7:
                strengths.append({
                    "domain": domain,
                    "strengths": assessment["strengths"]
                })
            elif assessment["score"] < 0.5:
                areas_for_development.append({
                    "domain": domain,
                    "areas": assessment["areas_for_development"]
                })
        
        return {
            "strengths": strengths,
            "areas_for_development": areas_for_development,
            "overall_balance": self._assess_competency_balance(domain_assessments)
        }
    
    def _assess_competency_balance(self, domain_assessments: Dict) -> str:
        """Assess balance across competency domains"""
        scores = [assessment["score"] for assessment in domain_assessments.values()]
        
        if not scores:
            return "no_data"
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score - min_score <= 0.2:
            return "balanced"
        elif max_score - min_score <= 0.4:
            return "moderately_balanced"
        else:
            return "unbalanced"
    
    def _generate_competency_recommendations(self, domain_assessments: Dict) -> List[str]:
        """Generate competency development recommendations"""
        recommendations = []
        
        for domain, assessment in domain_assessments.items():
            if assessment["score"] < 0.5:
                recommendations.append(f"Fokus pada pengembangan kompetensi di domain {domain}")
        
        if not recommendations:
            recommendations.append("Lanjutkan pengembangan kompetensi yang seimbang di semua domain")
        
        return recommendations
    
    def _generate_summary_narrative(
        self, 
        student_data: Dict, 
        competency_profile: Dict, 
        recommendations: List[str]
    ) -> str:
        """Generate summary narrative"""
        name = student_data.get("name", "Siswa")
        
        narrative = f"{name} menunjukkan kompetensi yang berkembang dengan baik. "
        
        strengths = competency_profile.get("strengths", [])
        if strengths:
            narrative += "Kekuatan kompetensi meliputi: "
            for strength in strengths[:2]:
                narrative += f"{strength['domain']}, "
            narrative = narrative.rstrip(", ") + ". "
        
        areas = competency_profile.get("areas_for_development", [])
        if areas:
            narrative += "Area yang perlu dikembangkan meliputi: "
            for area in areas[:2]:
                narrative += f"{area['domain']}, "
            narrative = narrative.rstrip(", ") + ". "
        
        if recommendations:
            narrative += " ".join(recommendations[:2])
        
        return narrative
    
    def _aggregate_class_competency(self, students_competency_data: List[Dict]) -> Dict:
        """Aggregate competency data for a class"""
        domain_scores = {}
        
        for student_data in students_competency_data:
            domain_assessments = student_data.get("domain_assessments", {})
            for domain, assessment in domain_assessments.items():
                if domain not in domain_scores:
                    domain_scores[domain] = []
                domain_scores[domain].append(assessment["score"])
        
        class_competency = {}
        for domain, scores in domain_scores.items():
            class_competency[domain] = {
                "average": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores),
                "count": len(scores)
            }
        
        return class_competency
    
    def _analyze_class_competency(self, class_competency: Dict) -> Dict:
        """Analyze class competency"""
        class_strengths = []
        class_development_areas = []
        
        for domain, data in class_competency.items():
            if data["average"] >= 0.7:
                class_strengths.append(domain)
            elif data["average"] < 0.5:
                class_development_areas.append(domain)
        
        return {
            "class_strengths": class_strengths,
            "class_development_areas": class_development_areas,
            "overall_class_level": self._determine_class_level(class_competency)
        }
    
    def _determine_class_level(self, class_competency: Dict) -> str:
        """Determine overall class competency level"""
        averages = [data["average"] for data in class_competency.values()]
        
        if not averages:
            return "no_data"
        
        average = sum(averages) / len(averages)
        
        if average >= 0.8:
            return "excellent"
        elif average >= 0.6:
            return "proficient"
        elif average >= 0.5:
            return "developing"
        else:
            return "needs_support"
    
    def _generate_class_recommendations(self, class_analysis: Dict) -> List[str]:
        """Generate class-level recommendations"""
        recommendations = []
        
        development_areas = class_analysis.get("class_development_areas", [])
        for area in development_areas:
            recommendations.append(f"Fokus pada pengembangan kelas di domain {area}")
        
        if not recommendations:
            recommendations.append("Lanjutkan pengembangan kelas yang seimbang di semua domain")
        
        return recommendations
    
    def _get_competency_history(self, student_id: str, timeframe: str) -> List[Dict]:
        """Get competency history for student"""
        # In real implementation, would retrieve from database
        return []
    
    def _analyze_domain_progression(self, competency_history: List[Dict]) -> Dict:
        """Analyze progression across competency domains"""
        domain_progression = {}
        
        for domain in CompetencyDomain:
            domain_name = domain.value
            scores = [
                h.get("domain_assessments", {}).get(domain_name, {}).get("score", 0.5)
                for h in competency_history
            ]
            
            if scores:
                domain_progression[domain_name] = {
                    "early_score": scores[0],
                    "recent_score": scores[-1],
                    "improvement": scores[-1] - scores[0],
                    "trend": "improving" if scores[-1] > scores[0] else "stable" if scores[-1] == scores[0] else "declining"
                }
        
        return domain_progression
    
    def _analyze_overall_progression(self, competency_history: List[Dict]) -> Dict:
        """Analyze overall competency progression"""
        if len(competency_history) < 2:
            return {"progression": "insufficient_data"}
        
        overall_scores = [h.get("overall_competency", {}).get("score", 0.5) for h in competency_history]
        
        early_score = overall_scores[0]
        recent_score = overall_scores[-1]
        
        progression_type = "improving" if recent_score > early_score + 0.1 else "stable" if abs(recent_score - early_score) <= 0.1 else "declining"
        
        return {
            "progression": progression_type,
            "early_score": early_score,
            "recent_score": recent_score,
            "improvement": recent_score - early_score
        }
    
    def _generate_progression_insights(self, domain_progression: Dict, overall_progression: Dict) -> List[str]:
        """Generate insights from competency progression"""
        insights = []
        
        progression = overall_progression.get("progression")
        if progression == "improving":
            insights.append("Kompetensi siswa meningkat seiring waktu")
        elif progression == "stable":
            insights.append("Kompetensi siswa stabil - pertimbangkan tantangan baru")
        elif progression == "declining":
            insights.append("Kompetensi siswa menurun - perlu intervensi")
        
        for domain, data in domain_progression.items():
            if data.get("trend") == "improving":
                insights.append(f"Kompetensi di domain {domain} meningkat dengan baik")
            elif data.get("trend") == "declining":
                insights.append(f"Kompetensi di domain {domain} perlu perhatian")
        
        return insights
    
    def _initialize_competency_framework(self) -> Dict:
        """Initialize competency framework"""
        return {
            CompetencyDomain.ACADEMIC.value: {
                "description": "Kompetensi akademik dalam mata pelajaran",
                "indicators": ["pemahaman_konsep", "aplikasi", "analisis", "evaluasi"]
            },
            CompetencyDomain.CHARACTER.value: {
                "description": "Kompetensi karakter sesuai Profil Pelajar Pancasila",
                "indicators": ["beriman", "berkebinekaan", "gotong_royong", "kreatif", "mandiri", "bernalir_kritis"]
            },
            CompetencyDomain.SKILLS.value: {
                "description": "Kompetensi keterampilan",
                "indicators": ["komunikasi", "kolaborasi", "pemecahan_masalah", "kreativitas"]
            },
            CompetencyDomain.SOCIAL_EMOTIONAL.value: {
                "description": "Kompetensi sosial emosional",
                "indicators": ["kesadaran_diri", "pengelolaan_emosi", "empati", "hubungan_sosial"]
            },
            CompetencyDomain.METACOGNITIVE.value: {
                "description": "Kompetensi metakognitif",
                "indicators": ["perencanaan", "monitoring", "evaluasi", "regulasi"]
            }
        }
