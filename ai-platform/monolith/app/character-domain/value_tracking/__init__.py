"""
Value Tracking

This service tracks student value development over time, monitoring how students
internalize and demonstrate character values in various learning activities and contexts.
"""

from typing import Dict, List, Optional
from datetime import datetime


class ValueTracking:
    """Value tracking service for character development monitoring"""
    
    def __init__(self):
        self.value_database = {}
        self.tracking_history = {}
        self.value_categories = self._initialize_value_categories()
    
    def track(self, student_id: str, activity: Dict) -> Dict:
        """Track student value development from specific activity"""
        tracking_id = f"value_track_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Extract value demonstrations from activity
        value_demonstrations = self._extract_value_demonstrations(activity)
        
        # Assess value internalization level
        internalization_assessment = self._assess_internalization(
            student_id, 
            value_demonstrations
        )
        
        # Update value history
        self._update_value_history(student_id, value_demonstrations)
        
        # Identify value patterns
        value_patterns = self._identify_value_patterns(student_id)
        
        # Calculate value consistency
        consistency_score = self._calculate_value_consistency(student_id)
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "activity": activity,
            "value_demonstrations": value_demonstrations,
            "internalization_assessment": internalization_assessment,
            "value_patterns": value_patterns,
            "consistency_score": consistency_score,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        self.value_database[tracking_id] = tracking_result
        
        return tracking_result
    
    def track_value_development(self, student_id: str, timeframe: str) -> Dict:
        """Track comprehensive value development over specified timeframe"""
        # Get all tracking records for student in timeframe
        student_records = self._get_student_records_in_timeframe(student_id, timeframe)
        
        if not student_records:
            return {
                "student_id": student_id,
                "timeframe": timeframe,
                "error": "No tracking records found for specified timeframe"
            }
        
        # Aggregate value demonstrations
        aggregated_values = self._aggregate_value_demonstrations(student_records)
        
        # Track development trajectory
        development_trajectory = self._track_development_trajectory(student_records)
        
        # Identify value milestones
        value_milestones = self._identify_value_milestones(student_records)
        
        # Predict future development
        predicted_development = self._predict_value_development(aggregated_values, development_trajectory)
        
        return {
            "student_id": student_id,
            "timeframe": timeframe,
            "total_activities_tracked": len(student_records),
            "aggregated_values": aggregated_values,
            "development_trajectory": development_trajectory,
            "value_milestones": value_milestones,
            "predicted_development": predicted_development,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def analyze_value_impact(self, student_id: str, activity_type: str) -> Dict:
        """Analyze the impact of specific activity types on value development"""
        # Get all tracking records for student
        student_records = [
            record for record in self.value_database.values()
            if record.get("student_id") == student_id
        ]
        
        if not student_records:
            return {
                "student_id": student_id,
                "activity_type": activity_type,
                "error": "No tracking records found for student"
            }
        
        # Filter by activity type
        filtered_records = [
            record for record in student_records
            if record.get("activity", {}).get("type") == activity_type
        ]
        
        if not filtered_records:
            return {
                "student_id": student_id,
                "activity_type": activity_type,
                "error": "No tracking records found for this activity type"
            }
        
        # Analyze value impact
        value_impact = self._calculate_value_impact(filtered_records)
        
        # Compare with other activity types
        comparative_analysis = self._compare_activity_types(student_records, activity_type)
        
        return {
            "student_id": student_id,
            "activity_type": activity_type,
            "activities_analyzed": len(filtered_records),
            "value_impact": value_impact,
            "comparative_analysis": comparative_analysis,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def generate_value_report(self, student_id: str) -> Dict:
        """Generate comprehensive value development report"""
        # Get all tracking records for student
        student_records = [
            record for record in self.value_database.values()
            if record.get("student_id") == student_id
        ]
        
        if not student_records:
            return {
                "student_id": student_id,
                "error": "No tracking records found for student"
            }
        
        # Sort by tracking date
        student_records.sort(key=lambda x: x.get("tracked_at", ""))
        
        # Generate report sections
        executive_summary = self._generate_executive_summary(student_records)
        value_development_summary = self._generate_development_summary(student_records)
        activity_impact_analysis = self._generate_activity_impact_analysis(student_records)
        recommendations = self._generate_value_recommendations(student_records)
        
        return {
            "student_id": student_id,
            "report_period": {
                "start": student_records[0].get("tracked_at"),
                "end": student_records[-1].get("tracked_at")
            },
            "executive_summary": executive_summary,
            "value_development_summary": value_development_summary,
            "activity_impact_analysis": activity_impact_analysis,
            "recommendations": recommendations,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _extract_value_demonstrations(self, activity: Dict) -> List[Dict]:
        """Extract value demonstrations from activity data"""
        # In real implementation, this would analyze activity data to identify
        # demonstrated values (e.g., helping others, showing resilience, etc.)
        
        value_demonstrations = []
        
        # Placeholder extraction logic
        if activity.get("activity_type") in ["group_project", "collaboration"]:
            value_demonstrations.append({
                "value_code": "gotong_royong",
                "demonstration_level": "moderate",
                "evidence": "Participated in group work"
            })
        
        if activity.get("activity_type") in ["research", "investigation"]:
            value_demonstrations.append({
                "value_code": "bernah_kritar",
                "demonstration_level": "good",
                "evidence": "Conducted research and analysis"
            })
        
        if activity.get("activity_type") in ["creative_work", "project"]:
            value_demonstrations.append({
                "value_code": "kreatif",
                "demonstration_level": "good",
                "evidence": "Created original work"
            })
        
        return value_demonstrations
    
    def _assess_internalization(self, student_id: str, demonstrations: List[Dict]) -> Dict:
        """Assess value internalization level"""
        if not demonstrations:
            return {
                "internalization_level": "none",
                "internalization_score": 0.0,
                "assessment": "No value demonstrations detected"
            }
        
        # Calculate internalization score based on demonstrations
        internalization_score = self._calculate_internalization_score(demonstrations)
        
        # Determine internalization level
        if internalization_score >= 0.8:
            internalization_level = "internalized"
        elif internalization_score >= 0.6:
            internalization_level = "practicing"
        elif internalization_score >= 0.4:
            internalization_level = "developing"
        else:
            internalization_level = "emerging"
        
        return {
            "internalization_level": internalization_level,
            "internalization_score": internalization_score,
            "demonstrations_count": len(demonstrations),
            "assessment": f"Student is {internalization_level} in value demonstration"
        }
    
    def _update_value_history(self, student_id: str, demonstrations: List[Dict]) -> None:
        """Update student's value history"""
        if student_id not in self.tracking_history:
            self.tracking_history[student_id] = []
        
        timestamp = datetime.utcnow().isoformat()
        
        for demonstration in demonstrations:
            self.tracking_history[student_id].append({
                "timestamp": timestamp,
                "value_code": demonstration.get("value_code"),
                "demonstration_level": demonstration.get("demonstration_level"),
                "evidence": demonstration.get("evidence")
            })
    
    def _identify_value_patterns(self, student_id: str) -> Dict:
        """Identify patterns in value demonstrations"""
        if student_id not in self.tracking_history:
            return {"patterns": [], "insights": []}
        
        history = self.tracking_history[student_id]
        
        # Count demonstrations by value code
        value_counts = {}
        for record in history:
            value_code = record.get("value_code")
            if value_code not in value_counts:
                value_counts[value_code] = 0
            value_counts[value_code] += 1
        
        # Identify most demonstrated values
        sorted_values = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
        
        patterns = []
        for value_code, count in sorted_values[:3]:
            patterns.append({
                "value_code": value_code,
                "demonstration_count": count,
                "pattern": "frequently_demonstrated"
            })
        
        # Identify rarely demonstrated values
        for value_code, count in sorted_values[-3:]:
            patterns.append({
                "value_code": value_code,
                "demonstration_count": count,
                "pattern": "rarely_demonstrated"
            })
        
        return {
            "patterns": patterns,
            "total_demonstrations": len(history)
        }
    
    def _calculate_value_consistency(self, student_id: str) -> float:
        """Calculate consistency of value demonstrations"""
        if student_id not in self.tracking_history:
            return 0.0
        
        history = self.tracking_history[student_id]
        
        if len(history) < 3:
            return 0.5  # Not enough data for consistency assessment
        
        # Simple consistency calculation
        # In real implementation, would use more sophisticated metrics
        unique_values = len(set(record.get("value_code") for record in history))
        total_demonstrations = len(history)
        
        consistency_score = min(1.0, unique_values / 6.0)  # Assuming 6 main values
        
        return consistency_score
    
    def _get_student_records_in_timeframe(self, student_id: str, timeframe: str) -> List[Dict]:
        """Get tracking records for student in specified timeframe"""
        student_records = [
            record for record in self.value_database.values()
            if record.get("student_id") == student_id
        ]
        
        # Filter by timeframe
        # In real implementation, would parse timeframe and filter accordingly
        return student_records
    
    def _aggregate_value_demonstrations(self, records: List[Dict]) -> Dict:
        """Aggregate value demonstrations from multiple records"""
        aggregated = {}
        
        for record in records:
            demonstrations = record.get("value_demonstrations", [])
            
            for demo in demonstrations:
                value_code = demo.get("value_code")
                
                if value_code not in aggregated:
                    aggregated[value_code] = {
                        "value_code": value_code,
                        "demonstration_count": 0,
                        "average_demonstration_level": [],
                        "evidence_examples": []
                    }
                
                aggregated[value_code]["demonstration_count"] += 1
                aggregated[value_code]["average_demonstration_level"].append(
                    self._quantify_demonstration_level(demo.get("demonstration_level"))
                )
                aggregated[value_code]["evidence_examples"].append(
                    demo.get("evidence")
                )
        
        # Calculate average demonstration levels
        for value_code in aggregated:
            levels = aggregated[value_code]["average_demonstration_level"]
            if levels:
                aggregated[value_code]["average_demonstration_level"] = sum(levels) / len(levels)
        
        return aggregated
    
    def _quantify_demonstration_level(self, level: str) -> float:
        """Convert demonstration level to numeric score"""
        level_map = {
            "none": 0.0,
            "low": 0.25,
            "moderate": 0.5,
            "good": 0.75,
            "excellent": 1.0
        }
        
        return level_map.get(level, 0.5)
    
    def _track_development_trajectory(self, records: List[Dict]) -> Dict:
        """Track value development trajectory over time"""
        # Placeholder trajectory analysis
        return {
            "trajectory": "improving",
            "growth_rate": 0.12,
            "stability": "stable",
            "key_development_points": []
        }
    
    def _identify_value_milestones(self, records: List[Dict]) -> List[Dict]:
        """Identify significant value development milestones"""
        # Placeholder milestone identification
        return [
            {
                "milestone_type": "first_demonstration",
                "value_code": "mandiri",
                "timestamp": records[0].get("tracked_at") if records else None
            }
        ]
    
    def _predict_value_development(self, aggregated: Dict, trajectory: Dict) -> Dict:
        """Predict future value development"""
        # Placeholder prediction logic
        return {
            "predicted_trajectory": "continued_improvement",
            "expected_improvement": 0.15,
            "focus_areas": []
        }
    
    def _calculate_value_impact(self, records: List[Dict]) -> Dict:
        """Calculate value impact for specific activity type"""
        impact = {}
        
        for record in records:
            demonstrations = record.get("value_demonstrations", [])
            
            for demo in demonstrations:
                value_code = demo.get("value_code")
                
                if value_code not in impact:
                    impact[value_code] = {
                        "value_code": value_code,
                        "demonstration_count": 0,
                        "average_level": []
                    }
                
                impact[value_code]["demonstration_count"] += 1
                impact[value_code]["average_level"].append(
                    self._quantify_demonstration_level(demo.get("demonstration_level"))
                )
        
        # Calculate averages
        for value_code in impact:
            levels = impact[value_code]["average_level"]
            if levels:
                impact[value_code]["average_level"] = sum(levels) / len(levels)
        
        return impact
    
    def _compare_activity_types(self, all_records: List[Dict], activity_type: str) -> Dict:
        """Compare value impact across different activity types"""
        # Get unique activity types
        activity_types = list(set(
            record.get("activity", {}).get("type") for record in all_records
            if record.get("activity", {}).get("type")
        ))
        
        comparison = {}
        
        for atype in activity_types:
            atype_records = [
                record for record in all_records
                if record.get("activity", {}).get("type") == atype
            ]
            
            impact = self._calculate_value_impact(atype_records)
            comparison[atype] = {
                "activity_count": len(atype_records),
                "value_impact": impact
            }
        
        return comparison
    
    def _calculate_internalization_score(self, demonstrations: List[Dict]) -> float:
        """Calculate internalization score from demonstrations"""
        if not demonstrations:
            return 0.0
        
        total_score = sum(
            self._quantify_demonstration_level(demo.get("demonstration_level"))
            for demo in demonstrations
        )
        
        return total_score / len(demonstrations)
    
    def _generate_executive_summary(self, records: List[Dict]) -> Dict:
        """Generate executive summary for value report"""
        return {
            "total_activities": len(records),
            "key_strengths": [],
            "development_areas": [],
            "overall_trajectory": "improving"
        }
    
    def _generate_development_summary(self, records: List[Dict]) -> Dict:
        """Generate value development summary"""
        return {
            "value_development": {},
            "internalization_progress": {},
            "consistency_analysis": {}
        }
    
    def _generate_activity_impact_analysis(self, records: List[Dict]) -> Dict:
        """Generate activity impact analysis"""
        return {
            "high_impact_activities": [],
            "low_impact_activities": [],
            "activity_recommendations": []
        }
    
    def _generate_value_recommendations(self, records: List[Dict]) -> List[Dict]:
        """Generate value development recommendations"""
        return [
            {
                "type": "continue",
                "recommendation": "Continue current value development activities"
            },
            {
                "type": "focus",
                "recommendation": "Focus on demonstrating values in group activities"
            }
        ]
    
    def _initialize_value_categories(self) -> Dict:
        """Initialize value categories"""
        return {
            "profil_pelajar_pancasila": {
                "code": "ppp",
                "name": "Profil Pelajar Pancasila",
                "values": ["beriman", "berkebinekaan", "gotong_royong", "mandiri", "bernah_kritar", "kreatif"]
            },
            "character_traits": {
                "code": "traits",
                "name": "Character Traits",
                "values": ["resilience", "empathy", "self_control", "gratitude", "curiosity"]
            }
        }