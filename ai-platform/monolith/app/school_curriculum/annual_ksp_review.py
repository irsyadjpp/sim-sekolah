"""
Annual KSP Review

This module handles annual review and evaluation of KSP (Kurikulum Satuan Pendidikan).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ReviewStatus(str, Enum):
    """Review status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REVISION = "needs_revision"


class ReviewAspect(str, Enum):
    """Aspects of KSP review"""
    IMPLEMENTATION = "implementation"
    EFFECTIVENESS = "effectiveness"
    ALIGNMENT = "alignment"
    CHALLENGES = "challenges"
    IMPROVEMENTS = "improvements"


class AnnualKSPReview:
    """Handler for annual KSP review"""
    
    def __init__(self):
        self.review_templates = self._initialize_review_templates()
        self.review_data: Dict[str, Dict] = {}
    
    def initiate_annual_review(
        self, 
        school_id: str, 
        school_name: str,
        year: str
    ) -> Dict:
        """Initiate annual KSP review"""
        review = {
            "review_id": f"REVIEW_{school_id}_{year}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "school_id": school_id,
            "school_name": school_name,
            "review_year": year,
            "review_status": ReviewStatus.PENDING.value,
            "initiated_date": datetime.utcnow().isoformat(),
            "review_aspects": {},
            "findings": {},
            "recommendations": [],
            "action_plan": []
        }
        
        # Initialize review aspects
        for aspect in ReviewAspect:
            review["review_aspects"][aspect.value] = {
                "status": ReviewStatus.PENDING.value,
                "data": {},
                "findings": []
            }
        
        self.review_data[review["review_id"]] = review
        
        return review
    
    def conduct_implementation_review(
        self, 
        review_id: str,
        implementation_data: Dict
    ) -> Dict:
        """Conduct implementation review"""
        if review_id not in self.review_data:
            return {"error": "Review not found"}
        
        review = self.review_data[review_id]
        
        implementation_review = {
            "status": ReviewStatus.IN_PROGRESS.value,
            "data": implementation_data,
            "findings": self._analyze_implementation(implementation_data)
        }
        
        review["review_aspects"][ReviewAspect.IMPLEMENTATION.value] = implementation_review
        review["review_status"] = ReviewStatus.IN_PROGRESS.value
        
        return implementation_review
    
    def conduct_effectiveness_review(
        self, 
        review_id: str,
        effectiveness_data: Dict
    ) -> Dict:
        """Conduct effectiveness review"""
        if review_id not in self.review_data:
            return {"error": "Review not found"}
        
        review = self.review_data[review_id]
        
        effectiveness_review = {
            "status": ReviewStatus.IN_PROGRESS.value,
            "data": effectiveness_data,
            "findings": self._analyze_effectiveness(effectiveness_data)
        }
        
        review["review_aspects"][ReviewAspect.EFFECTIVENESS.value] = effectiveness_review
        review["review_status"] = ReviewStatus.IN_PROGRESS.value
        
        return effectiveness_review
    
    def conduct_alignment_review(
        self, 
        review_id: str,
        alignment_data: Dict
    ) -> Dict:
        """Conduct alignment review"""
        if review_id not in self.review_data:
            return {"error": "Review not found"}
        
        review = self.review_data[review_id]
        
        alignment_review = {
            "status": ReviewStatus.IN_PROGRESS.value,
            "data": alignment_data,
            "findings": self._analyze_alignment(alignment_data)
        }
        
        review["review_aspects"][ReviewAspect.ALIGNMENT.value] = alignment_review
        review["review_status"] = ReviewStatus.IN_PROGRESS.value
        
        return alignment_review
    
    def conduct_challenges_review(
        self, 
        review_id: str,
        challenges_data: Dict
    ) -> Dict:
        """Conduct challenges review"""
        if review_id not in self.review_data:
            return {"error": "Review not found"}
        
        review = self.review_data[review_id]
        
        challenges_review = {
            "status": ReviewStatus.IN_PROGRESS.value,
            "data": challenges_data,
            "findings": self._analyze_challenges(challenges_data)
        }
        
        review["review_aspects"][ReviewAspect.CHALLENGES.value] = challenges_review
        review["review_status"] = ReviewStatus.IN_PROGRESS.value
        
        return challenges_review
    
    def conduct_improvements_review(
        self, 
        review_id: str,
        improvements_data: Dict
    ) -> Dict:
        """Conduct improvements review"""
        if review_id not in self.review_data:
            return {"error": "Review not found"}
        
        review = self.review_data[review_id]
        
        improvements_review = {
            "status": ReviewStatus.IN_PROGRESS.value,
            "data": improvements_data,
            "findings": self._analyze_improvements(improvements_data)
        }
        
        review["review_aspects"][ReviewAspect.IMPROVEMENTS.value] = improvements_review
        review["review_status"] = ReviewStatus.IN_PROGRESS.value
        
        return improvements_review
    
    def complete_review(self, review_id: str) -> Dict:
        """Complete annual review and generate final report"""
        if review_id not in self.review_data:
            return {"error": "Review not found"}
        
        review = self.review_data[review_id]
        
        # Generate findings
        review["findings"] = self._generate_overall_findings(review["review_aspects"])
        
        # Generate recommendations
        review["recommendations"] = self._generate_recommendations(review["findings"])
        
        # Generate action plan
        review["action_plan"] = self._generate_action_plan(review["recommendations"])
        
        # Update status
        review["review_status"] = ReviewStatus.COMPLETED.value
        review["completed_date"] = datetime.utcnow().isoformat()
        
        return review
    
    def _analyze_implementation(self, implementation_data: Dict) -> List[str]:
        """Analyze implementation data"""
        findings = []
        
        completion_rate = implementation_data.get("completion_rate", 0)
        if completion_rate < 0.7:
            findings.append(f"Low implementation completion rate: {completion_rate*100}%")
        elif completion_rate >= 0.9:
            findings.append(f"Excellent implementation completion rate: {completion_rate*100}%")
        
        teacher_participation = implementation_data.get("teacher_participation", 0)
        if teacher_participation < 0.8:
            findings.append(f"Low teacher participation: {teacher_participation*100}%")
        
        return findings
    
    def _analyze_effectiveness(self, effectiveness_data: Dict) -> List[str]:
        """Analyze effectiveness data"""
        findings = []
        
        student_achievement = effectiveness_data.get("student_achievement", 0)
        if student_achievement < 0.6:
            findings.append(f"Low student achievement: {student_achievement*100}%")
        elif student_achievement >= 0.8:
            findings.append(f"High student achievement: {student_achievement*100}%")
        
        learning_outcomes = effectiveness_data.get("learning_outcomes", 0)
        if learning_outcomes >= 0.8:
            findings.append(f"Positive learning outcomes: {learning_outcomes*100}%")
        
        return findings
    
    def _analyze_alignment(self, alignment_data: Dict) -> List[str]:
        """Analyze alignment data"""
        findings = []
        
        kurikulum_alignment = alignment_data.get("kurikulum_alignment", 0)
        if kurikulum_alignment < 0.7:
            findings.append(f"Low alignment with Kurikulum Merdeka: {kurikulum_alignment*100}%")
        elif kurikulum_alignment >= 0.9:
            findings.append(f"Excellent alignment with Kurikulum Merdeka: {kurikulum_alignment*100}%")
        
        vision_alignment = alignment_data.get("vision_alignment", 0)
        if vision_alignment >= 0.8:
            findings.append(f"Good alignment with school vision: {vision_alignment*100}%")
        
        return findings
    
    def _analyze_challenges(self, challenges_data: Dict) -> List[str]:
        """Analyze challenges data"""
        findings = []
        
        challenges = challenges_data.get("challenges", [])
        if challenges:
            findings.append(f"Identified {len(challenges)} key challenges")
            for challenge in challenges[:3]:
                findings.append(f"Challenge: {challenge.get('description', '')}")
        
        return findings
    
    def _analyze_improvements(self, improvements_data: Dict) -> List[str]:
        """Analyze improvements data"""
        findings = []
        
        improvements = improvements_data.get("improvements", [])
        if improvements:
            findings.append(f"Implemented {len(improvements)} improvements")
            for improvement in improvements[:3]:
                findings.append(f"Improvement: {improvement.get('description', '')}")
        
        return findings
    
    def _generate_overall_findings(self, review_aspects: Dict) -> Dict:
        """Generate overall findings from all review aspects"""
        overall_findings = {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "overall_score": 0.0
        }
        
        scores = []
        
        for aspect_name, aspect_data in review_aspects.items():
            findings = aspect_data.get("findings", [])
            
            # Categorize findings
            for finding in findings:
                if "excellent" in finding.lower() or "high" in finding.lower() or "positive" in finding.lower():
                    overall_findings["strengths"].append(finding)
                elif "low" in finding.lower() or "challenge" in finding.lower():
                    overall_findings["weaknesses"].append(finding)
                else:
                    overall_findings["opportunities"].append(finding)
        
        # Calculate overall score (simplified)
        total_findings = len(overall_findings["strengths"]) + len(overall_findings["weaknesses"])
        if total_findings > 0:
            overall_findings["overall_score"] = len(overall_findings["strengths"]) / total_findings
        
        return overall_findings
    
    def _generate_recommendations(self, findings: Dict) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []
        
        # Address weaknesses
        for weakness in findings["weaknesses"]:
            recommendations.append(f"Address: {weakness}")
        
        # Leverage strengths
        for strength in findings["strengths"]:
            recommendations.append(f"Leverage: {strength}")
        
        # Pursue opportunities
        for opportunity in findings["opportunities"]:
            recommendations.append(f"Explore: {opportunity}")
        
        return recommendations
    
    def _generate_action_plan(self, recommendations: List[str]) -> List[Dict]:
        """Generate action plan from recommendations"""
        action_plan = []
        
        for i, recommendation in enumerate(recommendations[:5]):
            action_plan.append({
                "action_id": f"ACTION_{i+1}",
                "recommendation": recommendation,
                "priority": "high" if i < 2 else "medium",
                "responsible": "School Principal",
                "timeline": "3-6 months",
                "status": "pending"
            })
        
        return action_plan
    
    def _initialize_review_templates(self) -> Dict:
        """Initialize review templates"""
        return {
            "implementation": {
                "required_data": ["completion_rate", "teacher_participation", "resource_utilization"],
                "optional_data": ["challenges", "successes"]
            },
            "effectiveness": {
                "required_data": ["student_achievement", "learning_outcomes", "satisfaction"],
                "optional_data": ["comparative_data"]
            },
            "alignment": {
                "required_data": ["kurikulum_alignment", "vision_alignment", "standards_alignment"],
                "optional_data": ["stakeholder_feedback"]
            }
        }
