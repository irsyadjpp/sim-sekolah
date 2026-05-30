"""
Learning Progression

This service manages learning progression tracking, analyzing how students progress
through learning sequences and identifying optimal learning paths. It provides insights
into learning velocity, bottlenecks, and acceleration opportunities.
"""

from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class LearningProgression:
    """Learning progression service for student development tracking"""
    
    def __init__(self):
        self.progression_database = {}
        self.learning_paths = {}
        self.progression_models = self._initialize_progression_models()
    
    def assess(self, student_id: str) -> Dict:
        """Comprehensive assessment of student learning progression"""
        assessment_id = f"prog_assess_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get student progression history
        progression_history = self._get_progression_history(student_id)
        
        # Analyze learning velocity
        velocity_analysis = self._analyze_learning_velocity(progression_history)
        
        # Identify progression patterns
        progression_patterns = self._identify_progression_patterns(progression_history)
        
        # Detect learning bottlenecks
        bottlenecks = self._detect_learning_bottlenecks(progression_history)
        
        # Identify acceleration opportunities
        acceleration_opportunities = self._identify_acceleration_opportunities(
            progression_history,
            bottlenecks
        )
        
        # Generate progression insights
        progression_insights = self._generate_progression_insights(
            velocity_analysis,
            progression_patterns,
            bottlenecks
        )
        
        assessment_result = {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "progression_history": progression_history,
            "velocity_analysis": velocity_analysis,
            "progression_patterns": progression_patterns,
            "learning_bottlenecks": bottlenecks,
            "acceleration_opportunities": acceleration_opportunities,
            "progression_insights": progression_insights,
            "assessed_at": datetime.utcnow().isoformat()
        }
        
        self.progression_database[assessment_id] = assessment_result
        
        return assessment_result
    
    def track_progression(self, student_id: str, learning_sequence: str, performance_data: Dict) -> Dict:
        """Track student progression through specific learning sequence"""
        tracking_id = f"prog_track_{student_id}_{learning_sequence}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get current position in sequence
        current_position = self._get_current_position(student_id, learning_sequence)
        
        # Analyze progression step
        progression_step = self._analyze_progression_step(
            current_position,
            performance_data
        )
        
        # Update progression history
        self._update_progression_history(student_id, learning_sequence, progression_step)
        
        # Calculate progression rate
        progression_rate = self._calculate_progression_rate(student_id, learning_sequence)
        
        # Identify next steps
        next_steps = self._identify_next_steps(current_position, progression_step)
        
        # Generate progression recommendations
        recommendations = self._generate_progression_recommendations(
            progression_step,
            progression_rate
        )
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "learning_sequence": learning_sequence,
            "current_position": current_position,
            "progression_step": progression_step,
            "progression_rate": progression_rate,
            "next_steps": next_steps,
            "recommendations": recommendations,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        self.progression_database[tracking_id] = tracking_result
        
        return tracking_result
    
    def predict_progression(self, student_id: str, learning_sequence: str) -> Dict:
        """Predict student progression through learning sequence"""
        prediction_id = f"prog_pred_{student_id}_{learning_sequence}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get progression history
        progression_history = self._get_progression_history(student_id, learning_sequence)
        
        # Analyze current trajectory
        current_trajectory = self._analyze_current_trajectory(progression_history)
        
        # Calculate expected completion time
        expected_completion = self._calculate_expected_completion(
            learning_sequence,
            current_trajectory
        )
        
        # Identify potential challenges
        potential_challenges = self._identify_potential_challenges(
            learning_sequence,
            progression_history
        )
        
        # Generate optimization recommendations
        optimization_recommendations = self._generate_optimization_recommendations(
            current_trajectory,
            potential_challenges
        )
        
        prediction_result = {
            "prediction_id": prediction_id,
            "student_id": student_id,
            "learning_sequence": learning_sequence,
            "current_trajectory": current_trajectory,
            "expected_completion": expected_completion,
            "potential_challenges": potential_challenges,
            "optimization_recommendations": optimization_recommendations,
            "predicted_at": datetime.utcnow().isoformat()
        }
        
        self.progression_database[prediction_id] = prediction_result
        
        return prediction_result
    
    def optimize_learning_path(self, student_id: str, subject: str, competency_area: str) -> Dict:
        """Optimize learning path based on progression analysis"""
        optimization_id = f"prog_opt_{student_id}_{subject}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get current learning path
        current_path = self._get_current_learning_path(student_id, subject, competency_area)
        
        # Analyze path effectiveness
        path_effectiveness = self._analyze_path_effectiveness(student_id, current_path)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(
            current_path,
            path_effectiveness
        )
        
        # Generate optimized path
        optimized_path = self._generate_optimized_path(
            current_path,
            optimization_opportunities
        )
        
        # Calculate expected improvement
        expected_improvement = self._calculate_expected_improvement(
            current_path,
            optimized_path,
            path_effectiveness
        )
        
        optimization_result = {
            "optimization_id": optimization_id,
            "student_id": student_id,
            "subject": subject,
            "competency_area": competency_area,
            "current_path": current_path,
            "path_effectiveness": path_effectiveness,
            "optimization_opportunities": optimization_opportunities,
            "optimized_path": optimized_path,
            "expected_improvement": expected_improvement,
            "optimized_at": datetime.utcnow().isoformat()
        }
        
        self.progression_database[optimization_id] = optimization_result
        
        return optimization_result
    
    def compare_progression(self, student_id: str, peer_group: str, timeframe: str) -> Dict:
        """Compare student progression with peer group"""
        comparison_id = f"prog_comp_{student_id}_{peer_group}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get student progression
        student_progression = self._get_progression_history(student_id, timeframe)
        
        # Get peer group progression
        peer_progression = self._get_peer_group_progression(peer_group, timeframe)
        
        # Calculate comparative metrics
        comparative_metrics = self._calculate_comparative_metrics(
            student_progression,
            peer_progression
        )
        
        # Identify strengths and areas
        strengths_and_areas = self._identify_strengths_and_areas(
            comparative_metrics,
            student_progression,
            peer_progression
        )
        
        # Generate insights
        comparison_insights = self._generate_comparison_insights(
            comparative_metrics,
            strengths_and_areas
        )
        
        comparison_result = {
            "comparison_id": comparison_id,
            "student_id": student_id,
            "peer_group": peer_group,
            "timeframe": timeframe,
            "student_progression": student_progression,
            "peer_progression": peer_progression,
            "comparative_metrics": comparative_metrics,
            "strengths_and_areas": strengths_and_areas,
            "comparison_insights": comparison_insights,
            "compared_at": datetime.utcnow().isoformat()
        }
        
        self.progression_database[comparison_id] = comparison_result
        
        return comparison_result
    
    def _get_progression_history(self, student_id: str, timeframe: Optional[str] = None) -> List[Dict]:
        """Get student progression history"""
        # In real implementation, would retrieve from database
        # For now, return placeholder data
        return [
            {
                "sequence_id": "seq_1",
                "step": 1,
                "completed_at": "2026-01-15T10:00:00Z",
                "mastery_score": 0.75,
                "time_spent": 120,
                "attempts": 1
            },
            {
                "sequence_id": "seq_1",
                "step": 2,
                "completed_at": "2026-01-22T10:00:00Z",
                "mastery_score": 0.80,
                "time_spent": 90,
                "attempts": 1
            },
            {
                "sequence_id": "seq_1",
                "step": 3,
                "completed_at": "2026-01-29T10:00:00Z",
                "mastery_score": 0.72,
                "time_spent": 150,
                "attempts": 2
            }
        ]
    
    def _analyze_learning_velocity(self, progression_history: List[Dict]) -> Dict:
        """Analyze student learning velocity"""
        if len(progression_history) < 2:
            return {
                "overall_velocity": "insufficient_data",
                "average_time_per_step": None,
                "velocity_trend": "unknown"
            }
        
        # Calculate average time per step
        total_time = sum(step.get("time_spent", 0) for step in progression_history)
        average_time = total_time / len(progression_history)
        
        # Analyze velocity trend
        time_values = [step.get("time_spent", 0) for step in progression_history]
        
        if len(time_values) >= 3:
            # Simple trend analysis
            early_avg = sum(time_values[:2]) / 2
            recent_avg = sum(time_values[-2:]) / 2
            
            if recent_avg < early_avg * 0.8:
                trend = "accelerating"
            elif recent_avg > early_avg * 1.2:
                trend = "decelerating"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Determine velocity category
        if average_time < 60:
            velocity_category = "fast"
        elif average_time < 120:
            velocity_category = "moderate"
        else:
            velocity_category = "slow"
        
        return {
            "overall_velocity": velocity_category,
            "average_time_per_step": average_time,
            "velocity_trend": trend,
            "time_range": {
                "minimum": min(time_values),
                "maximum": max(time_values),
                "variance": max(time_values) - min(time_values)
            }
        }
    
    def _identify_progression_patterns(self, progression_history: List[Dict]) -> Dict:
        """Identify patterns in student progression"""
        patterns = {
            "consistency_pattern": self._analyze_consistency_pattern(progression_history),
            "mastery_pattern": self._analyze_mastery_pattern(progression_history),
            "attempt_pattern": self._analyze_attempt_pattern(progression_history)
        }
        
        return patterns
    
    def _analyze_consistency_pattern(self, progression_history: List[Dict]) -> str:
        """Analyze consistency of progression timing"""
        if len(progression_history) < 3:
            return "insufficient_data"
        
        time_values = [step.get("time_spent", 0) for step in progression_history]
        mean_time = sum(time_values) / len(time_values)
        
        # Calculate coefficient of variation
        variance = sum((t - mean_time) ** 2 for t in time_values) / len(time_values)
        std_dev = variance ** 0.5
        cv = (std_dev / mean_time) if mean_time > 0 else 0
        
        if cv < 0.2:
            return "highly_consistent"
        elif cv < 0.4:
            return "moderately_consistent"
        else:
            return "variable"
    
    def _analyze_mastery_pattern(self, progression_history: List[Dict]) -> str:
        """Analyze pattern in mastery scores"""
        mastery_scores = [step.get("mastery_score", 0) for step in progression_history]
        
        if not mastery_scores:
            return "no_data"
        
        # Check for improvement trend
        if len(mastery_scores) >= 2:
            early_avg = sum(mastery_scores[:2]) / 2
            recent_avg = sum(mastery_scores[-2:]) / 2
            
            if recent_avg > early_avg + 0.1:
                return "improving"
            elif recent_avg < early_avg - 0.1:
                return "declining"
            else:
                return "stable"
        
        return "stable"
    
    def _analyze_attempt_pattern(self, progression_history: List[Dict]) -> str:
        """Analyze pattern in attempt counts"""
        attempts = [step.get("attempts", 1) for step in progression_history]
        
        if not attempts:
            return "no_data"
        
        avg_attempts = sum(attempts) / len(attempts)
        
        if avg_attempts <= 1.2:
            return "first_attempt_success"
        elif avg_attempts <= 2.0:
            return "occasional_retry"
        else:
            return "frequent_retry"
    
    def _detect_learning_bottlenecks(self, progression_history: List[Dict]) -> List[Dict]:
        """Detect learning bottlenecks in progression"""
        bottlenecks = []
        
        for i, step in enumerate(progression_history):
            # Check for high attempt count
            attempts = step.get("attempts", 1)
            if attempts > 2:
                bottlenecks.append({
                    "step": step.get("step", i + 1),
                    "bottleneck_type": "high_attempt_count",
                    "details": f"Step required {attempts} attempts",
                    "severity": "high" if attempts > 3 else "moderate"
                })
            
            # Check for long time spent
            time_spent = step.get("time_spent", 0)
            if time_spent > 180:  # More than 3 hours
                bottlenecks.append({
                    "step": step.get("step", i + 1),
                    "bottleneck_type": "extended_time",
                    "details": f"Step took {time_spent} minutes",
                    "severity": "high" if time_spent > 240 else "moderate"
                })
            
            # Check for low mastery despite completion
            mastery = step.get("mastery_score", 0)
            if mastery < 0.65:
                bottlenecks.append({
                    "step": step.get("step", i + 1),
                    "bottleneck_type": "low_mastery",
                    "details": f"Step completed with mastery {mastery:.2f}",
                    "severity": "high" if mastery < 0.60 else "moderate"
                })
        
        return bottlenecks
    
    def _identify_acceleration_opportunities(self, progression_history: List[Dict], bottlenecks: List[Dict]) -> List[Dict]:
        """Identify opportunities for learning acceleration"""
        opportunities = []
        
        # Identify steps where student excelled
        for step in progression_history:
            mastery = step.get("mastery_score", 0)
            attempts = step.get("attempts", 1)
            time_spent = step.get("time_spent", 0)
            
            if mastery >= 0.85 and attempts == 1 and time_spent < 60:
                opportunities.append({
                    "step": step.get("step"),
                    "opportunity_type": "skip_or_accelerate",
                    "details": f"Student showed strong mastery ({mastery:.2f}) with quick completion",
                    "recommendation": "Consider skipping similar content or accelerating progression"
                })
        
        # Identify areas for consolidation that could enable acceleration
        if len(bottlenecks) > 0:
            opportunities.append({
                "opportunity_type": "bottleneck_resolution",
                "details": f"Resolving {len(bottlenecks)} bottlenecks could enable overall acceleration",
                "recommendation": "Address bottlenecks through targeted support and practice"
            })
        
        return opportunities
    
    def _generate_progression_insights(self, velocity: Dict, patterns: Dict, bottlenecks: List[Dict]) -> List[str]:
        """Generate progression insights"""
        insights = []
        
        # Velocity insights
        velocity_cat = velocity.get("overall_velocity")
        if velocity_cat == "fast":
            insights.append("Student shows fast learning velocity, can handle accelerated pace")
        elif velocity_cat == "slow":
            insights.append("Student shows slower learning velocity, may need additional time and support")
        
        # Consistency insights
        consistency = patterns.get("consistency_pattern")
        if consistency == "highly_consistent":
            insights.append("Student shows highly consistent progression patterns")
        elif consistency == "variable":
            insights.append("Student shows variable progression patterns, may need support for consistency")
        
        # Bottleneck insights
        if len(bottlenecks) > 0:
            insights.append(f"Student has {len(bottlenecks)} learning bottlenecks that need attention")
        
        # Mastery pattern insights
        mastery_pattern = patterns.get("mastery_pattern")
        if mastery_pattern == "improving":
            insights.append("Student shows improving mastery over time")
        elif mastery_pattern == "declining":
            insights.append("Student shows declining mastery, needs intervention")
        
        return insights
    
    def _get_current_position(self, student_id: str, learning_sequence: str) -> Dict:
        """Get student's current position in learning sequence"""
        # In real implementation, would retrieve from database
        return {
            "sequence_id": learning_sequence,
            "current_step": 4,
            "total_steps": 10,
            "completion_percentage": 0.40,
            "last_completed_step": 3
        }
    
    def _analyze_progression_step(self, current_position: Dict, performance_data: Dict) -> Dict:
        """Analyze student's progression through current step"""
        score = performance_data.get("score", 0.75)
        time_spent = performance_data.get("time_spent", 90)
        attempts = performance_data.get("attempts", 1)
        
        step_analysis = {
            "step_number": current_position.get("current_step"),
            "mastery_score": score,
            "time_spent_minutes": time_spent,
            "attempts_required": attempts,
            "step_completion": self._determine_step_completion(score),
            "performance_category": self._categorize_performance(score, time_spent, attempts)
        }
        
        return step_analysis
    
    def _determine_step_completion(self, score: float) -> str:
        """Determine step completion status"""
        if score >= 0.75:
            return "completed"
        elif score >= 0.60:
            return "completed_with_review_needed"
        else:
            return "needs_remediation"
    
    def _categorize_performance(self, score: float, time_spent: int, attempts: int) -> str:
        """Categorize student performance"""
        if score >= 0.85 and attempts == 1 and time_spent < 90:
            return "excellent"
        elif score >= 0.75 and attempts <= 2:
            return "good"
        elif score >= 0.65:
            return "satisfactory"
        else:
            return "needs_improvement"
    
    def _update_progression_history(self, student_id: str, learning_sequence: str, progression_step: Dict) -> None:
        """Update student's progression history"""
        if student_id not in self.learning_paths:
            self.learning_paths[student_id] = {}
        
        if learning_sequence not in self.learning_paths[student_id]:
            self.learning_paths[student_id][learning_sequence] = []
        
        self.learning_paths[student_id][learning_sequence].append({
            "timestamp": datetime.utcnow().isoformat(),
            "step_number": progression_step.get("step_number"),
            "mastery_score": progression_step.get("mastery_score"),
            "time_spent_minutes": progression_step.get("time_spent_minutes"),
            "attempts_required": progression_step.get("attempts_required"),
            "performance_category": progression_step.get("performance_category")
        })
    
    def _calculate_progression_rate(self, student_id: str, learning_sequence: str) -> Dict:
        """Calculate progression rate for student in sequence"""
        if student_id not in self.learning_paths:
            return {"rate": "no_data", "steps_per_week": 0}
        
        if learning_sequence not in self.learning_paths[student_id]:
            return {"rate": "no_data", "steps_per_week": 0}
        
        history = self.learning_paths[student_id][learning_sequence]
        
        if len(history) < 2:
            return {"rate": "insufficient_data", "steps_per_week": 0}
        
        # Calculate steps per week
        first_timestamp = datetime.fromisoformat(history[0]["timestamp"])
        last_timestamp = datetime.fromisoformat(history[-1]["timestamp"])
        weeks_elapsed = (last_timestamp - first_timestamp).days / 7.0
        
        if weeks_elapsed <= 0:
            weeks_elapsed = 1  # Prevent division by zero
        
        steps_completed = len(history)
        steps_per_week = steps_completed / weeks_elapsed
        
        rate_category = "slow" if steps_per_week < 1 else "moderate" if steps_per_week < 3 else "fast"
        
        return {
            "rate": rate_category,
            "steps_per_week": steps_per_week,
            "total_steps_completed": steps_completed,
            "weeks_elapsed": weeks_elapsed
        }
    
    def _identify_next_steps(self, current_position: Dict, progression_step: Dict) -> List[Dict]:
        """Identify next steps in learning sequence"""
        completion_status = progression_step.get("step_completion")
        current_step = current_position.get("current_step")
        total_steps = current_position.get("total_steps", 10)
        
        next_steps = []
        
        if completion_status == "completed":
            if current_step < total_steps:
                next_steps.append({
                    "step": current_step + 1,
                    "action": "proceed_to_next_step",
                    "recommendation": "Student is ready to advance to next step"
                })
            else:
                next_steps.append({
                    "step": None,
                    "action": "sequence_complete",
                    "recommendation": "Student has completed the learning sequence"
                })
        elif completion_status == "completed_with_review_needed":
            next_steps.append({
                "step": current_step,
                "action": "review_and_reinforce",
                "recommendation": "Review current step before proceeding"
            })
        else:
            next_steps.append({
                "step": current_step,
                "action": "remediation_needed",
                "recommendation": "Provide remediation for current step"
            })
        
        return next_steps
    
    def _generate_progression_recommendations(self, progression_step: Dict, progression_rate: Dict) -> List[str]:
        """Generate recommendations based on progression analysis"""
        recommendations = []
        
        performance = progression_step.get("performance_category")
        
        if performance == "excellent":
            recommendations.append("Consider accelerating progression to maintain engagement")
            recommendations.append("Provide enrichment activities to deepen understanding")
        elif performance == "good":
            recommendations.append("Continue with current progression pace")
            recommendations.append("Monitor consistency of performance")
        elif performance == "satisfactory":
            recommendations.append("Provide additional practice and support")
            recommendations.append("Check for understanding gaps")
        else:
            recommendations.append("Provide immediate remediation and support")
            recommendations.append("Consider slowing progression pace")
        
        rate = progression_rate.get("rate")
        if rate == "slow":
            recommendations.append("Analyze reasons for slow progression and provide targeted support")
        elif rate == "fast":
            recommendations.append("Ensure deep learning despite fast pace")
        
        return recommendations
    
    def _analyze_current_trajectory(self, progression_history: List[Dict]) -> Dict:
        """Analyze current learning trajectory"""
        if len(progression_history) < 3:
            return {"trajectory": "insufficient_data", "confidence": "low"}
        
        # Analyze recent mastery scores
        recent_scores = [step.get("mastery_score", 0) for step in progression_history[-3:]]
        recent_avg = sum(recent_scores) / len(recent_scores)
        
        # Analyze trend
        if len(recent_scores) >= 2:
            trend = "improving" if recent_scores[-1] > recent_scores[0] + 0.1 else "stable"
        else:
            trend = "stable"
        
        return {
            "trajectory": trend,
            "recent_average_mastery": recent_avg,
            "confidence": "moderate" if len(progression_history) >= 5 else "low"
        }
    
    def _calculate_expected_completion(self, learning_sequence: str, trajectory: Dict) -> Dict:
        """Calculate expected completion time for learning sequence"""
        # In real implementation, would use sequence length and velocity
        trajectory_type = trajectory.get("trajectory")
        
        if trajectory_type == "improving":
            expected_weeks = 8
        elif trajectory_type == "stable":
            expected_weeks = 10
        else:
            expected_weeks = 12
        
        return {
            "expected_completion_weeks": expected_weeks,
            "confidence": trajectory.get("confidence", "low"),
            "factors": ["current_velocity", "trajectory_trend", "sequence_complexity"]
        }
    
    def _identify_potential_challenges(self, learning_sequence: str, progression_history: List[Dict]) -> List[Dict]:
        """Identify potential challenges in learning sequence"""
        challenges = []
        
        # Identify historically challenging step types
        for step in progression_history:
            if step.get("attempts", 1) > 2:
                challenges.append({
                    "challenge_type": "complexity_challenge",
                    "step": step.get("step"),
                    "reason": "High attempt count indicates difficulty"
                })
        
        return challenges
    
    def _generate_optimization_recommendations(self, trajectory: Dict, challenges: List[Dict]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        trajectory_type = trajectory.get("trajectory")
        if trajectory_type == "improving":
            recommendations.append("Continue current approach, maintain momentum")
        else:
            recommendations.append("Consider learning path optimization to improve trajectory")
        
        if len(challenges) > 0:
            recommendations.append(f"Address {len(challenges)} identified challenges")
        
        return recommendations
    
    def _get_current_learning_path(self, student_id: str, subject: str, competency_area: str) -> Dict:
        """Get student's current learning path"""
        return {
            "path_id": f"path_{subject}_{competency_area}",
            "subject": subject,
            "competency_area": competency_area,
            "current_sequence": [],
            "completion_percentage": 0.50,
            "estimated_remaining_time": "4 weeks"
        }
    
    def _analyze_path_effectiveness(self, student_id: str, current_path: Dict) -> Dict:
        """Analyze effectiveness of current learning path"""
        # Placeholder analysis
        return {
            "effectiveness_score": 0.72,
            "strengths": ["good_content_coverage", "appropriate_pacing"],
            "weaknesses": ["limited_personalization", "minimal_adaptation"]
        }
    
    def _identify_optimization_opportunities(self, current_path: Dict, effectiveness: Dict) -> List[Dict]:
        """Identify opportunities for path optimization"""
        opportunities = []
        
        effectiveness_score = effectiveness.get("effectiveness_score", 0.70)
        
        if effectiveness_score < 0.8:
            opportunities.append({
                "opportunity_type": "personalization_enhancement",
                "potential_improvement": 0.15,
                "description": "Increase personalization based on learning profile"
            })
        
        if "limited_personalization" in effectiveness.get("weaknesses", []):
            opportunities.append({
                "opportunity_type": "adaptive_pathing",
                "potential_improvement": 0.12,
                "description": "Implement adaptive pathing based on performance"
            })
        
        return opportunities
    
    def _generate_optimized_path(self, current_path: Dict, opportunities: List[Dict]) -> Dict:
        """Generate optimized learning path"""
        optimized_path = current_path.copy()
        optimized_path["optimizations_applied"] = []
        
        for opportunity in opportunities:
            optimized_path["optimizations_applied"].append({
                "opportunity": opportunity.get("opportunity_type"),
                "applied": True
            })
        
        optimized_path["expected_effectiveness"] = 0.85
        
        return optimized_path
    
    def _calculate_expected_improvement(self, current_path: Dict, optimized_path: Dict, effectiveness: Dict) -> Dict:
        """Calculate expected improvement from optimization"""
        current_score = effectiveness.get("effectiveness_score", 0.70)
        optimized_score = optimized_path.get("expected_effectiveness", 0.85)
        
        return {
            "current_effectiveness": current_score,
            "optimized_effectiveness": optimized_score,
            "expected_improvement": optimized_score - current_score,
            "improvement_percentage": ((optimized_score - current_score) / current_score) * 100 if current_score > 0 else 0
        }
    
    def _get_peer_group_progression(self, peer_group: str, timeframe: str) -> Dict:
        """Get progression data for peer group"""
        # In real implementation, would aggregate data from peer group
        return {
            "peer_group_id": peer_group,
            "group_size": 25,
            "average_progression_rate": 0.75,
            "average_mastery_score": 0.78,
            "average_velocity": "moderate"
        }
    
    def _calculate_comparative_metrics(self, student_progression: List[Dict], peer_progression: Dict) -> Dict:
        """Calculate comparative metrics between student and peer group"""
        if not student_progression:
            return {"error": "No student progression data"}
        
        # Calculate student averages
        student_avg_mastery = sum(step.get("mastery_score", 0) for step in student_progression) / len(student_progression)
        student_avg_time = sum(step.get("time_spent", 0) for step in student_progression) / len(student_progression)
        
        peer_avg_mastery = peer_progression.get("average_mastery_score", 0.75)
        peer_avg_velocity = peer_progression.get("average_velocity", "moderate")
        
        # Calculate comparison
        mastery_difference = student_avg_mastery - peer_avg_mastery
        
        return {
            "student_average_mastery": student_avg_mastery,
            "peer_average_mastery": peer_avg_mastery,
            "mastery_difference": mastery_difference,
            "mastery_percentile": self._calculate_percentile(student_avg_mastery, peer_avg_mastery),
            "relative_position": "above_average" if mastery_difference > 0.05 else "below_average" if mastery_difference < -0.05 else "average"
        }
    
    def _calculate_percentile(self, student_score: float, peer_average: float) -> str:
        """Calculate rough percentile based on difference from peer average"""
        difference = student_score - peer_average
        
        if difference >= 0.15:
            return "top_10%"
        elif difference >= 0.10:
            return "top_25%"
        elif difference >= 0.05:
            return "top_50%"
        elif difference >= -0.05:
            return "average"
        elif difference >= -0.10:
            return "bottom_25%"
        else:
            return "bottom_10%"
    
    def _identify_strengths_and_areas(self, comparative_metrics: Dict, student_progression: List[Dict], peer_progression: Dict) -> Dict:
        """Identify strengths and areas for improvement based on comparison"""
        relative_position = comparative_metrics.get("relative_position")
        
        strengths = []
        areas_for_improvement = []
        
        if relative_position == "above_average":
            strengths.append("Performance above peer group average")
        elif relative_position == "below_average":
            areas_for_improvement.append("Performance below peer group average")
        
        # Analyze specific patterns
        mastery_pattern = self._analyze_mastery_pattern(student_progression)
        if mastery_pattern == "improving":
            strengths.append("Positive mastery trajectory")
        elif mastery_pattern == "declining":
            areas_for_improvement.append("Declining mastery trend needs attention")
        
        return {
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement
        }
    
    def _generate_comparison_insights(self, comparative_metrics: Dict, strengths_and_areas: Dict) -> List[str]:
        """Generate insights from peer comparison"""
        insights = []
        
        relative_position = comparative_metrics.get("relative_position")
        percentile = comparative_metrics.get("mastery_percentile")
        
        if relative_position == "above_average":
            insights.append(f"Student performs above peer group average (estimated {percentile})")
        elif relative_position == "below_average":
            insights.append(f"Student performs below peer group average (estimated {percentile})")
        else:
            insights.append("Student performance is comparable to peer group average")
        
        strengths = strengths_and_areas.get("strengths", [])
        if strengths:
            insights.append(f"Strengths: {', '.join(strengths)}")
        
        areas = strengths_and_areas.get("areas_for_improvement", [])
        if areas:
            insights.append(f"Areas for improvement: {', '.join(areas)}")
        
        return insights
    
    def _initialize_progression_models(self) -> Dict:
        """Initialize progression models for different learning types"""
        return {
            "linear_progression": {
                "description": "Sequential, step-by-step learning progression",
                "characteristics": ["sequential", "prerequisite_based", "structured"]
            },
            "adaptive_progression": {
                "description": "Flexible progression based on performance",
                "characteristics": ["flexible", "performance_adapted", "non_linear"]
            },
            "mastery_based_progression": {
                "description": "Progression based on mastery achievement",
                "characteristics": ["mastery_threshold", "individual_pace", "competency_based"]
            },
            "spiral_progression": {
                "description": "Revisiting concepts at increasing depth",
                "characteristics": ["iterative", "deepening_complexity", "integrated"]
            }
        }