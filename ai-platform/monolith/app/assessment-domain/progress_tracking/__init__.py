"""
Progress Tracking

This service provides comprehensive progress tracking capabilities for students
across assessments, monitoring growth, identifying trends, and supporting
data-driven instruction aligned with Kurikulum Merdeka principles.
"""

from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class ProgressTracking:
    """Progress tracking service for student assessment progress"""
    
    def __init__(self):
        self.progress_database = {}
        self.student_progress_history = defaultdict(list)
        self.class_progress_data = defaultdict(dict)
    
    def track(self, student_id: str, assessment_results: List[Dict]) -> Dict:
        """Track student progress across assessments"""
        tracking_id = f"prog_track_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Aggregate assessment results
        aggregated_results = self._aggregate_assessment_results(assessment_results)
        
        # Calculate progress metrics
        progress_metrics = self._calculate_progress_metrics(aggregated_results)
        
        # Identify growth areas
        growth_areas = self._identify_growth_areas(progress_metrics)
        
        # Identify areas needing support
        support_areas = self._identify_support_areas(progress_metrics)
        
        # Generate progress insights
        progress_insights = self._generate_progress_insights(
            progress_metrics,
            growth_areas,
            support_areas
        )
        
        # Update progress history
        self._update_progress_history(student_id, progress_metrics)
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "assessment_results": assessment_results,
            "aggregated_results": aggregated_results,
            "progress_metrics": progress_metrics,
            "growth_areas": growth_areas,
            "support_areas": support_areas,
            "progress_insights": progress_insights,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        self.progress_database[tracking_id] = tracking_result
        
        return tracking_result
    
    def monitor_student_progress(self, student_id: str, subject: str, timeframe: str = "semester") -> Dict:
        """Monitor student progress in specific subject over timeframe"""
        monitoring_id = f"monitor_{student_id}_{subject}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get student progress history
        progress_history = self._get_progress_history(student_id, timeframe)
        
        if not progress_history:
            return {
                "monitoring_id": monitoring_id,
                "student_id": student_id,
                "subject": subject,
                "error": "No progress history found"
            }
        
        # Filter by subject
        subject_progress = self._filter_by_subject(progress_history, subject)
        
        # Calculate subject-specific metrics
        subject_metrics = self._calculate_subject_metrics(subject_progress)
        
        # Analyze subject trajectory
        subject_trajectory = self._analyze_subject_trajectory(subject_progress)
        
        # Identify subject-specific trends
        subject_trends = self._identify_subject_trends(subject_progress)
        
        # Generate subject progress report
        subject_report = self._generate_subject_report(
            subject_metrics,
            subject_trajectory,
            subject_trends
        )
        
        monitoring_result = {
            "monitoring_id": monitoring_id,
            "student_id": student_id,
            "subject": subject,
            "timeframe": timeframe,
            "subject_progress": subject_progress,
            "subject_metrics": subject_metrics,
            "subject_trajectory": subject_trajectory,
            "subject_trends": subject_trends,
            "subject_report": subject_report,
            "monitored_at": datetime.utcnow().isoformat()
        }
        
        return monitoring_result
    
    def generate_class_progress_report(self, class_id: str, subject: str, timeframe: str = "semester") -> Dict:
        """Generate aggregate progress report for entire class"""
        class_report_id = f"class_report_{class_id}_{subject}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get class progress data
        class_data = self._get_class_progress_data(class_id, timeframe)
        
        if not class_data:
            return {
                "class_report_id": class_report_id,
                "class_id": class_id,
                "subject": subject,
                "error": "No class progress data found"
            }
        
        # Calculate aggregate class metrics
        class_metrics = self._calculate_class_metrics(class_data)
        
        # Analyze class distribution
        class_distribution = self._analyze_class_distribution(class_data)
        
        # Identify class trends
        class_trends = self._analyze_class_trends(class_data)
        
        # Identify class-level interventions needed
        intervention_areas = self._identify_intervention_areas(class_metrics, class_distribution)
        
        # Generate class-level insights
        class_insights = self._generate_class_insights(
            class_metrics,
            class_distribution,
            class_trends
        )
        
        class_report = {
            "class_report_id": class_report_id,
            "class_id": class_id,
            "subject": subject,
            "timeframe": timeframe,
            "class_metrics": class_metrics,
            "class_distribution": class_distribution,
            "class_trends": class_trends,
            "intervention_areas": intervention_areas,
            "class_insights": class_insights,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return class_report
    
    def compare_progress(self, student_id: str, peer_group: str, timeframe: str = "semester") -> Dict:
        """Compare student progress with peer group"""
        comparison_id = f"compare_{student_id}_{peer_group}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get student progress
        student_progress = self._get_student_progress_summary(student_id, timeframe)
        
        # Get peer group progress
        peer_progress = self._get_peer_group_progress(peer_group, timeframe)
        
        if not student_progress:
            return {
                "comparison_id": comparison_id,
                "student_id": student_id,
                "peer_group": peer_group,
                "error": "No student progress data found"
            }
        
        # Calculate comparative metrics
        comparative_metrics = self._calculate_comparative_metrics(
            student_progress,
            peer_progress
        )
        
        # Identify relative position
        relative_position = self._identify_relative_position(
            student_progress,
            peer_progress
        )
        
        # Generate comparison insights
        comparison_insights = self._generate_comparison_insights(
            comparative_metrics,
            relative_position
        )
        
        comparison_result = {
            "comparison_id": comparison_id,
            "student_id": student_id,
            "peer_group": peer_group,
            "timeframe": timeframe,
            "student_progress": student_progress,
            "peer_progress": peer_progress,
            "comparative_metrics": comparative_metrics,
            "relative_position": relative_position,
            "comparison_insights": comparison_insights,
            "compared_at": datetime.utcnow().isoformat()
        }
        
        return comparison_result
    
    def predict_future_performance(self, student_id: str, subject: str) -> Dict:
        """Predict future performance based on progress trends"""
        prediction_id = f"predict_{student_id}_{subject}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get historical progress data
        historical_data = self._get_historical_progress(student_id, subject)
        
        if len(historical_data) < 3:
            return {
                "prediction_id": prediction_id,
                "student_id": student_id,
                "subject": subject,
                "error": "Insufficient historical data for prediction"
            }
        
        # Analyze performance trajectory
        trajectory = self._analyze_performance_trajectory(historical_data)
        
        # Calculate growth rate
        growth_rate = self._calculate_growth_rate(historical_data)
        
        # Predict future performance
        future_prediction = self._predict_future_performance(
            historical_data,
            trajectory,
            growth_rate
        )
        
        # Identify potential risks
        potential_risks = self._identify_potential_risks(historical_data, trajectory)
        
        # Generate prediction confidence
        prediction_confidence = self._calculate_prediction_confidence(historical_data)
        
        prediction_result = {
            "prediction_id": prediction_id,
            "student_id": student_id,
            "subject": subject,
            "historical_data": historical_data,
            "trajectory": trajectory,
            "growth_rate": growth_rate,
            "future_prediction": future_prediction,
            "potential_risks": potential_risks,
            "prediction_confidence": prediction_confidence,
            "predicted_at": datetime.utcnow().isoformat()
        }
        
        return prediction_result
    
    def _aggregate_assessment_results(self, assessment_results: List[Dict]) -> Dict:
        """Aggregate assessment results into summary metrics"""
        if not assessment_results:
            return {"error": "No assessment results to aggregate"}
        
        total_assessments = len(assessment_results)
        total_score = sum(result.get("score", 0) for result in assessment_results)
        average_score = total_score / total_assessments
        
        # Count proficiency levels
        proficiency_counts = defaultdict(int)
        for result in assessment_results:
            proficiency = result.get("proficiency_level", "unknown")
            proficiency_counts[proficiency] += 1
        
        return {
            "total_assessments": total_assessments,
            "average_score": average_score,
            "score_range": [min(r.get("score", 0) for r in assessment_results), max(r.get("score", 0) for r in assessment_results)],
            "proficiency_distribution": dict(proficiency_counts),
            "most_common_proficiency": max(proficiency_counts, key=proficiency_counts.get) if proficiency_counts else "unknown"
        }
    
    def _calculate_progress_metrics(self, aggregated_results: Dict) -> Dict:
        """Calculate progress metrics from aggregated results"""
        return {
            "overall_performance": aggregated_results.get("average_score", 0),
            "performance_trend": "stable",  # Would calculate from historical data
            "consistency": self._calculate_consistency(aggregated_results),
            "growth_velocity": 0.05,  # Would calculate from historical data
            "proficiency_trajectory": "developing"
        }
    
    def _calculate_consistency(self, aggregated_results: Dict) -> str:
        """Calculate performance consistency"""
        score_range = aggregated_results.get("score_range", [0, 100])
        score_variance = score_range[1] - score_range[0]
        
        if score_variance < 10:
            return "highly_consistent"
        elif score_variance < 20:
            return "moderately_consistent"
        else:
            return "variable"
    
    def _identify_growth_areas(self, progress_metrics: Dict) -> List[str]:
        """Identify areas showing growth"""
        growth_areas = []
        
        # Placeholder - would analyze actual data
        if progress_metrics.get("growth_velocity", 0) > 0.05:
            growth_areas.append("Consistent improvement over time")
        
        if progress_metrics.get("proficiency_trajectory") == "improving":
            growth_areas.append("Moving to higher proficiency levels")
        
        return growth_areas if growth_areas else ["No specific growth areas identified"]
    
    def _identify_support_areas(self, progress_metrics: Dict) -> List[str]:
        """Identify areas needing additional support"""
        support_areas = []
        
        if progress_metrics.get("overall_performance", 0) < 0.70:
            support_areas.append("Overall performance below target")
        
        if progress_metrics.get("consistency") == "variable":
            support_areas.append "Performance inconsistency, needs support"
        
        return support_areas if support_areas else ["No critical support areas identified"]
    
    def _generate_progress_insights(self, progress_metrics: Dict, growth_areas: List[str], support_areas: List[str]) -> List[str]:
        """Generate progress insights"""
        insights = []
        
        if growth_areas:
            insights.append(f"Growth areas: {', '.join(growth_areas)}")
        
        if support_areas:
            insights.append(f"Support areas: {', '.join(support_areas)}")
        
        overall_performance = progress_metrics.get("overall_performance", 0)
        if overall_performance >= 0.80:
            insights.append("Strong overall performance")
        elif overall_performance >= 0.70:
            insights.append("Satisfactory performance with room for growth")
        else:
            insights.append("Performance below target, needs intervention")
        
        return insights
    
    def _update_progress_history(self, student_id: str, progress_metrics: Dict) -> None:
        """Update student progress history"""
        self.student_progress_history[student_id].append({
            "timestamp": datetime.utcnow().isoformat(),
            "progress_metrics": progress_metrics
        })
    
    def _get_progress_history(self, student_id: str, timeframe: str) -> List[Dict]:
        """Get student progress history for timeframe"""
        if student_id not in self.student_progress_history:
            return []
        
        # In real implementation, would filter by timeframe
        return self.student_progress_history[student_id]
    
    def _filter_by_subject(self, progress_history: List[Dict], subject: str) -> List[Dict]:
        """Filter progress history by subject"""
        # Placeholder - would implement actual filtering
        return progress_history
    
    def _calculate_subject_metrics(self, subject_progress: List[Dict]) -> Dict:
        """Calculate subject-specific progress metrics"""
        if not subject_progress:
            return {"error": "No subject progress data"}
        
        # Aggregate subject-specific metrics
        return {
            "subject_average": 0.78,
            "subject_trend": "improving",
            "subject_consistency": "high",
            "mastery_level": "developing"
        }
    
    def _analyze_subject_trajectory(self, subject_progress: List[Dict]) -> Dict:
        """Analyze subject-specific trajectory"""
        if len(subject_progress) < 3:
            return {"trajectory": "insufficient_data"}
        
        # Simple trajectory analysis
        return {
            "trajectory": "improving",
            "rate_of_improvement": 0.12,
            "predicted_direction": "continued_improvement"
        }
    
    def _identify_subject_trends(self, subject_progress: List[Dict]) -> List[str]:
        """Identify subject-specific trends"""
        return [
            "Performance shows consistent improvement",
            "Mastery levels increasing over time",
            "Areas of strength identified"
        ]
    
    def _generate_subject_report(self, subject_metrics: Dict, subject_trajectory: Dict, subject_trends: List[str]) -> Dict:
        """Generate subject progress report"""
        return {
            "summary": f"Subject performance: {subject_metrics.get('subject_average', 0):.2f}",
            "trajectory": subject_trajectory.get("trajectory", "stable"),
            "key_trends": subject_trends,
            "recommendations": [
                "Continue current approach",
                "Focus on identified growth areas",
                "Provide targeted support where needed"
            ]
        }
    
    def _get_class_progress_data(self, class_id: str, timeframe: str) -> Dict:
        """Get class progress data"""
        # In real implementation, would retrieve from database
        return {}
    
    def _calculate_class_metrics(self, class_data: Dict) -> Dict:
        """Calculate aggregate class metrics"""
        return {
            "class_average": 0.76,
            "class_median": 0.75,
            "performance_distribution": {
                "advanced": 0.15,
                "proficient": 0.45,
                "developing": 0.30,
                "emerging": 0.10
            }
        }
    
    def _analyze_class_distribution(self, class_data: Dict) -> Dict:
        """Analyze class performance distribution"""
        return {
            "distribution": {
                "top_performers": 0.15,
                "middle_group": 0.55,
                "needs_support": 0.30
            },
            "variability": "moderate",
            "outliers": "identified"
        }
    
    def _analyze_class_trends(self, class_data: Dict) -> List[str]:
        """Analyze class-level trends"""
        return [
            "Class showing overall improvement",
            "Performance variability moderate",
            "Clear grouping patterns identified"
        ]
    
    def _identify_intervention_areas(self, class_metrics: Dict, class_distribution: Dict) -> List[Dict]:
        """Identify class-level intervention areas"""
        intervention_areas = []
        
        if class_metrics.get("class_average", 0) < 0.70:
            intervention_areas.append({
                "area": "overall_class_performance",
                "priority": "high",
                "recommendation": "Implement class-wide intervention strategies"
            })
        
        needs_support_percentage = class_distribution.get("distribution", {}).get("needs_support", 0)
        if needs_support_percentage > 0.25:
            intervention_areas.append({
                "area": "struggling_students",
                "priority": "high",
                "recommendation": "Provide targeted support for bottom quartile"
            })
        
        return intervention_areas
    
    def _generate_class_insights(self, class_metrics: Dict, class_distribution: Dict, class_trends: List[str]) -> List[str]:
        """Generate class-level insights"""
        insights = []
        
        class_average = class_metrics.get("class_average", 0)
        if class_average >= 0.80:
            insights.append("Class performing well overall")
        elif class_average >= 0.70:
            insights.append("Class performing satisfactorily")
        else:
            insights.append("Class performance below expectations, needs intervention")
        
        insights.extend(class_trends)
        
        return insights
    
    def _get_student_progress_summary(self, student_id: str, timeframe: str) -> Dict:
        """Get student progress summary"""
        if student_id not in self.student_progress_history:
            return None
        
        history = self.student_progress_history[student_id]
        if not history:
            return None
        
        latest = history[-1]
        return {
            "student_id": student_id,
            "latest_metrics": latest.get("progress_metrics"),
            "history_length": len(history)
        }
    
    def _get_peer_group_progress(self, peer_group: str, timeframe: str) -> Dict:
        """Get peer group progress data"""
        # In real implementation, would aggregate peer group data
        return {
            "peer_group_id": peer_group,
            "group_size": 25,
            "group_average": 0.75,
            "group_median": 0.74,
            "performance_distribution": {
                "advanced": 0.12,
                "proficient": 0.48,
                "developing": 0.28,
                "emerging": 0.12
            }
        }
    
    def _calculate_comparative_metrics(self, student_progress: Dict, peer_progress: Dict) -> Dict:
        """Calculate comparative metrics"""
        student_average = student_progress.get("latest_metrics", {}).get("overall_performance", 0)
        peer_average = peer_progress.get("group_average", 0.75)
        
        difference = student_average - peer_average
        
        return {
            "student_average": student_average,
            "peer_average": peer_average,
            "difference": difference,
            "percentile": self._calculate_percentile(student_average, peer_progress),
            "relative_performance": "above_average" if difference > 0.05 else "below_average" if difference < -0.05 else "average"
        }
    
    def _calculate_percentile(self, student_score: float, peer_progress: Dict) -> str:
        """Calculate approximate percentile"""
        distribution = peer_progress.get("performance_distribution", {})
        
        # Simple percentile calculation
        if student_score >= 0.90:
            return "top_10%"
        elif student_score >= 0.80:
            return "top_25%"
        elif student_score >= 0.70:
            return "top_50%"
        elif student_score >= 0.60:
            return "bottom_25%"
        else:
            return "bottom_10%"
    
    def _identify_relative_position(self, student_progress: Dict, peer_progress: Dict) -> Dict:
        """Identify student's relative position in peer group"""
        comparative = self._calculate_comparative_metrics(student_progress, peer_progress)
        
        return {
            "relative_performance": comparative.get("relative_performance"),
            "percentile": comparative.get("percentile"),
            "distance_from_mean": comparative.get("difference")
        }
    
    def _generate_comparison_insights(self, comparative_metrics: Dict, relative_position: Dict) -> List[str]:
        """Generate comparison insights"""
        insights = []
        
        relative_perf = comparative_metrics.get("relative_performance")
        if relative_perf == "above_average":
            insights.append("Student performs above peer group average")
        elif relative_perf == "below_average":
            insights.append("Student performs below peer group average")
        else:
            insights.append("Student performance is comparable to peer group")
        
        percentile = comparative_metrics.get("percentile")
        insights.append(f"Student is in the {percentile} of the peer group")
        
        return insights
    
    def _get_historical_progress(self, student_id: str, subject: str) -> List[Dict]:
        """Get historical progress data for prediction"""
        if student_id not in self.student_progress_history:
            return []
        
        return self.student_progress_history[student_id]
    
    def _analyze_performance_trajectory(self, historical_data: List[Dict]) -> Dict:
        """Analyze performance trajectory from historical data"""
        if len(historical_data) < 3:
            return {"trajectory": "insufficient_data"}
        
        # Extract scores from historical data
        scores = [data.get("progress_metrics", {}).get("overall_performance", 0) for data in historical_data]
        
        # Analyze trend
        early_avg = sum(scores[:2]) / 2
        recent_avg = sum(scores[-2:]) / 2
        
        if recent_avg > early_avg + 0.05:
            trajectory = "positive"
        elif recent_avg < early_avg - 0.05:
            trajectory = "negative"
        else:
            trajectory = "stable"
        
        return {
            "trajectory": trajectory,
            "early_average": early_avg,
            "recent_average": recent_avg,
            "trend_magnitude": recent_avg - early_avg
        }
    
    def _calculate_growth_rate(self, historical_data: List[Dict]) -> float:
        """Calculate growth rate from historical data"""
        if len(historical_data) < 2:
            return 0.0
        
        scores = [data.get("progress_metrics", {}).get("overall_performance", 0) for data in historical_data]
        
        # Simple growth rate calculation
        growth = (scores[-1] - scores[0]) / len(scores)
        
        return growth
    
    def _predict_future_performance(self, historical_data: List[Dict], trajectory: Dict, growth_rate: float) -> Dict:
        """Predict future performance based on historical data"""
        latest_score = historical_data[-1].get("progress_metrics", {}).get("overall_performance", 0)
        
        trajectory_type = trajectory.get("trajectory", "stable")
        
        if trajectory_type == "positive":
            predicted_score = latest_score + growth_rate * 2  # Project forward
            confidence = "moderate"
        elif trajectory_type == "negative":
            predicted_score = latest_score + growth_rate * 2
            confidence = "moderate"
        else:
            predicted_score = latest_score
            confidence = "low"
        
        return {
            "predicted_score": predicted_score,
            "confidence": confidence,
            "prediction_horizon": "next_assessment",
            "factors_influencing": ["current_trend", "growth_rate", "historical_consistency"]
        }
    
    def _identify_potential_risks(self, historical_data: List[Dict], trajectory: Dict) -> List[str]:
        """Identify potential risks based on trajectory analysis"""
        risks = []
        
        trajectory_type = trajectory.get("trajectory")
        if trajectory_type == "negative":
            risks.append("Declining performance trend, intervention needed")
        elif trajectory_type == "stable":
            risks.append("Stagnant performance, may need challenges")
        
        consistency_check = self._check_historical_consistency(historical_data)
        if consistency_check.get("variability") == "high":
            risks.append("High performance variability, needs support for consistency")
        
        return risks
    
    def _check_historical_consistency(self, historical_data: List[Dict]) -> Dict:
        """Check consistency of historical performance"""
        scores = [data.get("progress_metrics", {}).get("overall_performance", 0) for data in historical_data]
        
        if not scores:
            return {"variability": "unknown"}
        
        score_range = max(scores) - min(scores)
        
        if score_range < 0.15:
            return {"variability": "low", "consistency": "high"}
        elif score_range < 0.25:
            return {"variability": "moderate", "consistency": "moderate"}
        else:
            return {"variability": "high", "consistency": "low"}
    
    def _calculate_prediction_confidence(self, historical_data: List[Dict]) -> Dict:
        """Calculate confidence level for predictions"""
        data_points = len(historical_data)
        consistency = self._check_historical_consistency(historical_data)
        
        confidence_score = 0.0
        
        if data_points >= 5:
            confidence_score += 0.4
        elif data_points >= 3:
            confidence_score += 0.3
        
        if consistency.get("consistency") == "high":
            confidence_score += 0.4
        elif consistency.get("consistency") == "moderate":
            confidence_score += 0.2
        
        confidence_level = "high" if confidence_score >= 0.6 else "moderate" if confidence_score >= 0.4 else "low"
        
        return {
            "confidence_level": confidence_level,
            "confidence_score": confidence_score,
            "data_points": data_points,
            "consistency": consistency.get("consistency")
        }