"""
Mastery Tracking

This service provides comprehensive mastery depth tracking capabilities, assessing
student mastery of learning objectives and competencies at different depth levels
(remembering → understanding → applying → analyzing → evaluating → creating).
This is a CORE component for Pembelajaran Mendalam and deep learning intelligence.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class MasteryLevel(Enum):
    """Mastery depth levels based on Bloom's Taxonomy"""
    REMEMBERING = "remembering"  # Surface level
    UNDERSTANDING = "understanding"  # Basic comprehension
    APPLYING = "applying"  # Use in familiar situations
    ANALYZING = "analyzing"  # Break down and connect
    EVALUATING = "evaluating"  # Judge and justify
    CREATING = "creating"  # Generate new ideas/solutions


class MasteryTracking:
    """Mastery depth tracking service for deep learning assessment"""
    
    def __init__(self):
        self.mastery_database = {}
        self.progression_history = {}
        self.mastery_criteria = self._initialize_mastery_criteria()
    
    def track_mastery(self, student_id: str, competency: str, assessment_data: Dict) -> Dict:
        """Track student mastery of specific competency"""
        tracking_id = f"mastery_track_{student_id}_{competency}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Assess current mastery level
        current_mastery = self._assess_mastery_level(competency, assessment_data)
        
        # Compare with previous mastery
        previous_mastery = self._get_previous_mastery(student_id, competency)
        mastery_progression = self._calculate_mastery_progression(previous_mastery, current_mastery)
        
        # Update progression history
        self._update_progression_history(student_id, competency, current_mastery)
        
        # Generate mastery insights
        mastery_insights = self._generate_mastery_insights(
            student_id,
            competency,
            current_mastery,
            mastery_progression
        )
        
        # Determine next learning steps
        next_steps = self._determine_next_steps(competency, current_mastery)
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "competency": competency,
            "current_mastery_level": current_mastery["level"],
            "mastery_score": current_mastery["score"],
            "mastery_progression": mastery_progression,
            "mastery_insights": mastery_insights,
            "next_learning_steps": next_steps,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        self.mastery_database[tracking_id] = tracking_result
        
        return tracking_result
    
    def assess_mastery_depth(self, student_id: str, subject: str, competency_area: str) -> Dict:
        """Comprehensive mastery depth assessment for competency area"""
        assessment_id = f"mastery_depth_{student_id}_{subject}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get all competencies in the area
        competencies = self._get_competencies_in_area(subject, competency_area)
        
        # Assess mastery for each competency
        competency_mastery = {}
        for competency in competencies:
            mastery_data = self._get_latest_mastery(student_id, competency)
            competency_mastery[competency] = mastery_data
        
        # Calculate aggregate mastery depth
        aggregate_mastery = self._calculate_aggregate_mastery(competency_mastery)
        
        # Analyze mastery distribution across depth levels
        depth_distribution = self._analyze_depth_distribution(competency_mastery)
        
        # Identify mastery gaps
        mastery_gaps = self._identify_mastery_gaps(competency_mastery, depth_distribution)
        
        # Generate mastery development plan
        development_plan = self._generate_development_plan(
            student_id,
            subject,
            competency_area,
            competency_mastery,
            mastery_gaps
        )
        
        return {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "subject": subject,
            "competency_area": competency_area,
            "competency_mastery": competency_mastery,
            "aggregate_mastery": aggregate_mastery,
            "depth_distribution": depth_distribution,
            "mastery_gaps": mastery_gaps,
            "development_plan": development_plan,
            "assessed_at": datetime.utcnow().isoformat()
        }
    
    def track_mastery_progression(self, student_id: str, competency: str, timeframe: str = "semester") -> Dict:
        """Track mastery progression over specified timeframe"""
        progression_id = f"mastery_prog_{student_id}_{competency}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get mastery tracking history for timeframe
        history = self._get_mastery_history(student_id, competency, timeframe)
        
        if not history:
            return {
                "progression_id": progression_id,
                "student_id": student_id,
                "competency": competency,
                "error": "No mastery history found for specified timeframe"
            }
        
        # Analyze progression trajectory
        trajectory = self._analyze_progression_trajectory(history)
        
        # Calculate progression rate
        progression_rate = self._calculate_progression_rate(history)
        
        # Identify progression milestones
        milestones = self._identify_progression_milestones(history)
        
        # Predict future mastery
        predicted_mastery = self._predict_future_mastery(history, trajectory)
        
        return {
            "progression_id": progression_id,
            "student_id": student_id,
            "competency": competency,
            "timeframe": timeframe,
            "tracking_history": history,
            "progression_trajectory": trajectory,
            "progression_rate": progression_rate,
            "progression_milestones": milestones,
            "predicted_mastery": predicted_mastery,
            "analyzed_at": datetime.utcnow().isoformat()
        }
    
    def recommend_mastery_activities(self, student_id: str, competency: str, target_level: str) -> Dict:
        """Recommend activities to achieve target mastery level"""
        # Get current mastery
        current_mastery = self._get_latest_mastery(student_id, competency)
        
        if not current_mastery:
            return {
                "student_id": student_id,
                "competency": competency,
                "error": "No mastery data found. Please assess mastery first."
            }
        
        current_level = current_mastery.get("current_mastery_level")
        
        # Determine gap between current and target level
        mastery_gap = self._calculate_mastery_gap(current_level, target_level)
        
        # Generate activities to bridge the gap
        recommended_activities = self._generate_mastery_activities(competency, current_level, target_level)
        
        # Estimate time to target
        time_to_target = self._estimate_time_to_target(mastery_gap, current_mastery)
        
        return {
            "student_id": student_id,
            "competency": competency,
            "current_mastery_level": current_level,
            "target_mastery_level": target_level,
            "mastery_gap": mastery_gap,
            "recommended_activities": recommended_activities,
            "estimated_time_to_target": time_to_target,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _assess_mastery_level(self, competency: str, assessment_data: Dict) -> Dict:
        """Assess mastery level based on assessment data"""
        # In real implementation, this would analyze assessment results
        # to determine mastery level using Bloom's Taxonomy criteria
        
        # Placeholder logic - would use sophisticated analysis
        assessment_score = assessment_data.get("score", 0.70)
        
        # Determine mastery level based on score
        if assessment_score >= 0.90:
            level = MasteryLevel.CREATING.value
            score = assessment_score
        elif assessment_score >= 0.80:
            level = MasteryLevel.EVALUATING.value
            score = assessment_score
        elif assessment_score >= 0.70:
            level = MasteryLevel.ANALYZING.value
            score = assessment_score
        elif assessment_score >= 0.60:
            level = MasteryLevel.APPLYING.value
            score = assessment_score
        elif assessment_score >= 0.50:
            level = MasteryLevel.UNDERSTANDING.value
            score = assessment_score
        else:
            level = MasteryLevel.REMEMBERING.value
            score = assessment_score
        
        return {
            "level": level,
            "score": score,
            "criteria_met": self._get_criteria_for_level(level),
            "evidence": assessment_data.get("evidence", [])
        }
    
    def _get_previous_mastery(self, student_id: str, competency: str) -> Optional[Dict]:
        """Get previous mastery record for student and competency"""
        if student_id not in self.progression_history:
            return None
        
        if competency not in self.progression_history[student_id]:
            return None
        
        history = self.progression_history[student_id][competency]
        
        if len(history) < 2:
            return None
        
        return history[-2]  # Second most recent
    
    def _calculate_mastery_progression(self, previous: Optional[Dict], current: Dict) -> Dict:
        """Calculate mastery progression between assessments"""
        if not previous:
            return {
                "progression": "initial_assessment",
                "level_change": None,
                "score_change": None,
                "trajectory": "baseline"
            }
        
        prev_level = previous.get("level")
        curr_level = current.get("level")
        prev_score = previous.get("score", 0)
        curr_score = current.get("score", 0)
        
        # Determine progression type
        if curr_level == prev_level:
            progression = "stable"
        elif self._is_deeper_level(curr_level, prev_level):
            progression = "improving"
        else:
            progression = "declining"
        
        # Calculate level change
        level_change = self._calculate_level_change(prev_level, curr_level)
        
        # Calculate score change
        score_change = curr_score - prev_score
        
        return {
            "progression": progression,
            "level_change": level_change,
            "score_change": score_change,
            "trajectory": self._determine_trajectory(score_change, progression)
        }
    
    def _update_progression_history(self, student_id: str, competency: str, mastery_data: Dict) -> None:
        """Update progression history for student and competency"""
        if student_id not in self.progression_history:
            self.progression_history[student_id] = {}
        
        if competency not in self.progression_history[student_id]:
            self.progression_history[student_id][competency] = []
        
        self.progression_history[student_id][competency].append({
            "timestamp": datetime.utcnow().isoformat(),
            "level": mastery_data.get("level"),
            "score": mastery_data.get("score")
        })
    
    def _generate_mastery_insights(self, student_id: str, competency: str, current: Dict, progression: Dict) -> Dict:
        """Generate mastery insights and recommendations"""
        level = current.get("level")
        score = current.get("score", 0)
        trajectory = progression.get("trajectory", "stable")
        
        insights = {
            "current_state": f"Student at {level} level with score {score:.2f}",
            "trajectory": trajectory,
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        if score >= 0.8:
            insights["strengths"].append("Strong mastery demonstrated")
        elif score >= 0.6:
            insights["strengths"].append("Good progress in development")
        
        if score < 0.7:
            insights["areas_for_improvement"].append("Need more practice and support")
        
        if trajectory == "improving":
            insights["recommendations"].append("Continue current learning approach")
        elif trajectory == "stable":
            insights["recommendations"].append("Consider challenging activities to advance")
        else:
            insights["recommendations"].append("Review and reinforce foundational concepts")
        
        return insights
    
    def _determine_next_steps(self, competency: str, mastery_data: Dict) -> List[Dict]:
        """Determine next learning steps based on mastery level"""
        level = mastery_data.get("level")
        score = mastery_data.get("score", 0)
        
        next_steps = []
        
        if level == MasteryLevel.REMEMBERING.value:
            next_steps.append({
                "step": "move_to_understanding",
                "activity": "Practice explaining concepts in own words",
                "priority": "high"
            })
        elif level == MasteryLevel.UNDERSTANDING.value:
            next_steps.append({
                "step": "move_to_applying",
                "activity": "Apply concepts in familiar situations",
                "priority": "high"
            })
        elif level == MasteryLevel.APPLYING.value:
            next_steps.append({
                "step": "move_to_analyzing",
                "activity": "Analyze relationships and patterns",
                "priority": "medium"
            })
        elif level == MasteryLevel.ANALYZING.value:
            next_steps.append({
                "step": "move_to_evaluating",
                "activity": "Evaluate and justify reasoning",
                "priority": "medium"
            })
        elif level == MasteryLevel.EVALUATING.value:
            next_steps.append({
                "step": "move_to_creating",
                "activity": "Generate new ideas and solutions",
                "priority": "medium"
            })
        elif level == MasteryLevel.CREATING.value:
            next_steps.append({
                "step": "deepen_mastery",
                "activity": "Apply in complex, novel situations",
                "priority": "low"
            })
        
        return next_steps
    
    def _get_competencies_in_area(self, subject: str, competency_area: str) -> List[str]:
        """Get all competencies in specified area"""
        # Placeholder - would integrate with standards-domain
        return [
            f"{competency_area}_competency_1",
            f"{competency_area}_competency_2",
            f"{competency_area}_competency_3"
        ]
    
    def _get_latest_mastery(self, student_id: str, competency: str) -> Optional[Dict]:
        """Get latest mastery record for student and competency"""
        # Get tracking records
        records = [
            record for record in self.mastery_database.values()
            if record.get("student_id") == student_id and record.get("competency") == competency
        ]
        
        if not records:
            return None
        
        # Sort by tracked_at and return latest
        records.sort(key=lambda x: x.get("tracked_at", ""))
        return records[-1]
    
    def _calculate_aggregate_mastery(self, competency_mastery: Dict) -> Dict:
        """Calculate aggregate mastery across competencies"""
        if not competency_mastery:
            return {"aggregate_score": 0.0, "average_level": "none"}
        
        total_score = sum(
            data.get("mastery_score", 0) 
            for data in competency_mastery.values() 
            if data
        )
        valid_count = sum(1 for data in competency_mastery.values() if data)
        
        average_score = total_score / valid_count if valid_count > 0 else 0.0
        
        # Determine average level
        levels = [data.get("current_mastery_level") for data in competency_mastery.values() if data]
        average_level = self._determine_average_level(levels) if levels else "none"
        
        return {
            "aggregate_score": average_score,
            "average_level": average_level,
            "competencies_assessed": valid_count
        }
    
    def _analyze_depth_distribution(self, competency_mastery: Dict) -> Dict:
        """Analyze distribution of mastery across depth levels"""
        distribution = {}
        
        for data in competency_mastery.values():
            if not data:
                continue
            
            level = data.get("current_mastery_level")
            if level not in distribution:
                distribution[level] = 0
            distribution[level] += 1
        
        return distribution
    
    def _identify_mastery_gaps(self, competency_mastery: Dict, depth_distribution: Dict) -> List[Dict]:
        """Identify mastery gaps and areas needing attention"""
        gaps = []
        
        for competency, data in competency_mastery.items():
            if not data:
                gaps.append({
                    "competency": competency,
                    "gap_type": "no_data",
                    "recommendation": "Assess competency mastery"
                })
                continue
            
            score = data.get("mastery_score", 0)
            level = data.get("current_mastery_level")
            
            if score < 0.6:
                gaps.append({
                    "competency": competency,
                    "gap_type": "low_mastery",
                    "current_score": score,
                    "current_level": level,
                    "target_score": 0.70,
                    "priority": "high"
                })
            elif score < 0.8:
                gaps.append({
                    "competency": competency,
                    "gap_type": "moderate_mastery",
                    "current_score": score,
                    "current_level": level,
                    "target_score": 0.85,
                    "priority": "medium"
                })
        
        return gaps
    
    def _generate_development_plan(self, student_id: str, subject: str, competency_area: str, competency_mastery: Dict, mastery_gaps: List[Dict]) -> Dict:
        """Generate mastery development plan"""
        # Prioritize gaps
        high_priority_gaps = [gap for gap in mastery_gaps if gap.get("priority") == "high"]
        
        # Generate development activities for each gap
        development_activities = []
        for gap in high_priority_gaps[:3]:  # Focus on top 3 priorities
            competency = gap.get("competency")
            current_level = gap.get("current_level")
            activities = self._generate_mastery_activities(competency, current_level, "analyzing")
            development_activities.extend(activities)
        
        return {
            "student_id": student_id,
            "subject": subject,
            "competency_area": competency_area,
            "priority_gaps": len(mastery_gaps),
            "development_activities": development_activities,
            "estimated_duration": self._estimate_development_duration(development_activities),
            "success_criteria": [
                "Achieve 0.75+ mastery score in all competencies",
                "Progress to analyzing level for core competencies"
            ]
        }
    
    def _get_mastery_history(self, student_id: str, competency: str, timeframe: str) -> List[Dict]:
        """Get mastery history for specified timeframe"""
        if student_id not in self.progression_history:
            return []
        
        if competency not in self.progression_history[student_id]:
            return []
        
        return self.progression_history[student_id][competency]
    
    def _analyze_progression_trajectory(self, history: List[Dict]) -> Dict:
        """Analyze progression trajectory over time"""
        if len(history) < 2:
            return {"trajectory": "insufficient_data", "trend": "unknown"}
        
        # Calculate overall trend
        first_score = history[0].get("score", 0)
        last_score = history[-1].get("score", 0)
        score_change = last_score - first_score
        
        if score_change > 0.1:
            trend = "improving"
        elif score_change < -0.1:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trajectory": trend,
            "trend": trend,
            "total_progress": score_change,
            "start_level": history[0].get("level"),
            "current_level": history[-1].get("level")
        }
    
    def _calculate_progression_rate(self, history: List[Dict]) -> Dict:
        """Calculate progression rate (level changes per period)"""
        if len(history) < 2:
            return {"rate": 0.0, "unit": "level_per_period"}
        
        level_changes = 0
        for i in range(1, len(history)):
            if self._is_deeper_level(history[i].get("level"), history[i-1].get("level")):
                level_changes += 1
        
        rate = level_changes / (len(history) - 1)
        
        return {
            "rate": rate,
            "unit": "level_changes_per_period",
            "total_periods": len(history) - 1,
            "total_level_changes": level_changes
        }
    
    def _identify_progression_milestones(self, history: List[Dict]) -> List[Dict]:
        """Identify significant progression milestones"""
        milestones = []
        
        for i, record in enumerate(history):
            level = record.get("level")
            score = record.get("score")
            
            # Identify first time reaching deeper levels
            if level in ["analyzing", "evaluating", "creating"]:
                milestones.append({
                    "milestone": f"achieved_{level}_level",
                    "timestamp": record.get("timestamp"),
                    "score": score
                })
        
        return milestones
    
    def _predict_future_mastery(self, history: List[Dict], trajectory: Dict) -> Dict:
        """Predict future mastery based on trajectory"""
        trend = trajectory.get("trend", "stable")
        current_level = history[-1].get("level") if history else "remembering"
        current_score = history[-1].get("score", 0) if history else 0.5
        
        # Simple prediction logic
        if trend == "improving":
            predicted_level = self._get_next_deeper_level(current_level)
            predicted_score = min(1.0, current_score + 0.15)
        elif trend == "declining":
            predicted_level = self._get_previous_level(current_level)
            predicted_score = max(0.0, current_score - 0.10)
        else:
            predicted_level = current_level
            predicted_score = current_score
        
        return {
            "predicted_level": predicted_level,
            "predicted_score": predicted_score,
            "confidence": "moderate" if len(history) >= 3 else "low",
            "timeframe": "next_period"
        }
    
    def _generate_mastery_activities(self, competency: str, current_level: str, target_level: str) -> List[Dict]:
        """Generate activities to achieve target mastery level"""
        activities = []
        
        # Generate level-specific activities
        level_activities = self._get_level_activities(current_level, target_level)
        
        for i, activity in enumerate(level_activities):
            activities.append({
                "activity_id": f"act_{i}",
                "competency": competency,
                "activity": activity,
                "focus_level": target_level,
                "duration_minutes": 30,
                "type": "individual"
            })
        
        return activities
    
    def _get_level_activities(self, current: str, target: str) -> List[str]:
        """Get activities for specific level progression"""
        activities_map = {
            "understanding": [
                "Explain concepts in own words",
                "Create concept maps",
                "Summarize key ideas"
            ],
            "applying": [
                "Solve practice problems",
                "Apply concepts to familiar scenarios",
                "Complete guided exercises"
            ],
            "analyzing": [
                "Compare and contrast concepts",
                "Analyze relationships between ideas",
                "Break down complex problems"
            ],
            "evaluating": [
                "Critique arguments or solutions",
                "Justify reasoning with evidence",
                "Evaluate alternative approaches"
            ],
            "creating": [
                "Design new solutions",
                "Create original content",
                "Develop innovative approaches"
            ]
        }
        
        return activities_map.get(target, activities_map.get("understanding", []))
    
    def _estimate_time_to_target(self, mastery_gap: int, current_mastery: Dict) -> Dict:
        """Estimate time to reach target mastery level"""
        # Simple estimation: 2-4 weeks per level advancement
        time_map = {
            1: "2-3 weeks",
            2: "3-5 weeks",
            3: "4-6 weeks",
            4: "5-8 weeks",
            5: "6-10 weeks"
        }
        
        estimated_time = time_map.get(mastery_gap, "6-10 weeks")
        
        return {
            "estimated_duration": estimated_time,
            "confidence": "moderate",
            "factors": ["current_mastery", "practice_frequency", "support_level"]
        }
    
    def _estimate_development_duration(self, activities: List[Dict]) -> str:
        """Estimate total duration for development activities"""
        total_minutes = sum(
            activity.get("duration_minutes", 30) 
            for activity in activities
        )
        
        total_hours = total_minutes / 60
        
        return f"{total_hours:.1f} hours"
    
    def _calculate_mastery_gap(self, current: str, target: str) -> int:
        """Calculate gap between current and target mastery levels"""
        level_order = [
            MasteryLevel.REMEMBERING.value,
            MasteryLevel.UNDERSTANDING.value,
            MasteryLevel.APPLYING.value,
            MasteryLevel.ANALYZING.value,
            MasteryLevel.EVALUATING.value,
            MasteryLevel.CREATING.value
        ]
        
        try:
            current_index = level_order.index(current)
            target_index = level_order.index(target)
            return target_index - current_index
        except ValueError:
            return 1  # Default gap
    
    def _is_deeper_level(self, current: str, previous: str) -> bool:
        """Check if current level is deeper than previous"""
        level_order = [
            MasteryLevel.REMEMBERING.value,
            MasteryLevel.UNDERSTANDING.value,
            MasteryLevel.APPLYING.value,
            MasteryLevel.ANALYZING.value,
            MasteryLevel.EVALUATING.value,
            MasteryLevel.CREATING.value
        ]
        
        try:
            current_index = level_order.index(current)
            previous_index = level_order.index(previous)
            return current_index > previous_index
        except ValueError:
            return False
    
    def _calculate_level_change(self, previous: str, current: str) -> int:
        """Calculate number of level changes"""
        if not previous or not current:
            return 0
        
        return self._calculate_mastery_gap(previous, current)
    
    def _determine_trajectory(self, score_change: float, progression: str) -> str:
        """Determine overall trajectory"""
        if progression == "improving":
            return "positive"
        elif progression == "declining":
            return "negative"
        else:
            if score_change > 0.05:
                return "positive"
            elif score_change < -0.05:
                return "negative"
            else:
                return "stable"
    
    def _get_next_deeper_level(self, current: str) -> str:
        """Get next deeper mastery level"""
        level_order = [
            MasteryLevel.REMEMBERING.value,
            MasteryLevel.UNDERSTANDING.value,
            MasteryLevel.APPLYING.value,
            MasteryLevel.ANALYZING.value,
            MasteryLevel.EVALUATING.value,
            MasteryLevel.CREATING.value
        ]
        
        try:
            current_index = level_order.index(current)
            if current_index < len(level_order) - 1:
                return level_order[current_index + 1]
            return current
        except ValueError:
            return MasteryLevel.UNDERSTANDING.value
    
    def _get_previous_level(self, current: str) -> str:
        """Get previous mastery level"""
        level_order = [
            MasteryLevel.REMEMBERING.value,
            MasteryLevel.UNDERSTANDING.value,
            MasteryLevel.APPLYING.value,
            MasteryLevel.ANALYZING.value,
            MasteryLevel.EVALUATING.value,
            MasteryLevel.CREATING.value
        ]
        
        try:
            current_index = level_order.index(current)
            if current_index > 0:
                return level_order[current_index - 1]
            return current
        except ValueError:
            return MasteryLevel.UNDERSTANDING.value
    
    def _determine_average_level(self, levels: List[str]) -> str:
        """Determine average mastery level from list"""
        if not levels:
            return "none"
        
        level_order = [
            MasteryLevel.REMEMBERING.value,
            MasteryLevel.UNDERSTANDING.value,
            MasteryLevel.APPLYING.value,
            MasteryLevel.ANALYZING.value,
            MasteryLevel.EVALUATING.value,
            MasteryLevel.CREATING.value
        ]
        
        # Convert levels to indices and calculate average
        indices = []
        for level in levels:
            try:
                indices.append(level_order.index(level))
            except ValueError:
                continue
        
        if not indices:
            return "none"
        
        average_index = int(sum(indices) / len(indices))
        return level_order[average_index]
    
    def _get_criteria_for_level(self, level: str) -> List[str]:
        """Get mastery criteria for specific level"""
        criteria_map = {
            MasteryLevel.REMEMBERING.value: [
                "Recall facts and basic concepts",
                "Identify key information",
                "Recognize terminology"
            ],
            MasteryLevel.UNDERSTANDING.value: [
                "Explain ideas in own words",
                "Summarize main concepts",
                "Interpret meaning"
            ],
            MasteryLevel.APPLYING.value: [
                "Use concepts in familiar situations",
                "Apply methods to solve problems",
                "Implement learned procedures"
            ],
            MasteryLevel.ANALYZING.value: [
                "Break down complex ideas",
                "Analyze relationships",
                "Identify patterns and connections"
            ],
            MasteryLevel.EVALUATING.value: [
                "Judge and justify reasoning",
                "Critique arguments",
                "Evaluate alternatives"
            ],
            MasteryLevel.CREATING.value: [
                "Generate new ideas",
                "Design original solutions",
                "Create innovative approaches"
            ]
        }
        
        return criteria_map.get(level, [])
    
    def _initialize_mastery_criteria(self) -> Dict:
        """Initialize mastery criteria definitions"""
        return {
            "depth_levels": {
                "remembering": {
                    "description": "Recall and recognize information",
                    "assessment_methods": ["recall", "identification", "matching"]
                },
                "understanding": {
                    "description": "Explain and interpret meaning",
                    "assessment_methods": ["explanation", "summarization", "interpretation"]
                },
                "applying": {
                    "description": "Use information in familiar contexts",
                    "assessment_methods": ["application", "implementation", "execution"]
                },
                "analyzing": {
                    "description": "Break down and examine relationships",
                    "assessment_methods": ["analysis", "comparison", "categorization"]
                },
                "evaluating": {
                    "description": "Judge and justify decisions",
                    "assessment_methods": ["evaluation", "critique", "justification"]
                },
                "creating": {
                    "description": "Generate new ideas and solutions",
                    "assessment_methods": ["creation", "design", "innovation"]
                }
            }
        }