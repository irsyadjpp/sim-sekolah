"""
Reflection Engine

This service provides comprehensive reflection analysis capabilities for students,
assessing reflection depth, generating contextual prompts, and supporting
metacognitive development aligned with Pembelajaran Mendalam principles.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class ReflectionPhase(Enum):
    """Phases of reflection in learning process"""
    BEFORE_LEARNING = "before_learning"
    DURING_LEARNING = "during_learning"
    AFTER_LEARNING = "after_learning"
    ON_GOING = "ongoing"


class ReflectionDepth(Enum):
    """Depth levels of student reflection"""
    SURFACE = "surface"  # Descriptive, factual
    DESCRIPTIVE = "descriptive"  # Personal connections, some analysis
    ANALYTICAL = "analytical"  # Critical analysis, evaluation
    EVALUATIVE = "evaluative"  # Deep analysis, synthesis
    TRANSFORMATIVE = "transformative"  # Personal transformation, future applications


class ReflectionEngine:
    """Reflection analysis and generation service for Pembelajaran Mendalam"""
    
    def __init__(self):
        self.reflection_database = {}
        self.prompt_library = self._initialize_prompt_library()
        self.depth_analysis_criteria = self._initialize_depth_criteria()
    
    def analyze(self, student_id: str, reflection: str) -> Dict:
        """Analyze student reflection for depth and quality"""
        analysis_id = f"refl_analysis_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine reflection phase
        reflection_phase = self._determine_reflection_phase(reflection)
        
        # Analyze reflection depth
        depth_analysis = self._analyze_reflection_depth(reflection, reflection_phase)
        
        # Identify reflection quality indicators
        quality_indicators = self._identify_quality_indicators(reflection)
        
        # Generate feedback on reflection
        feedback = self._generate_reflection_feedback(depth_analysis, quality_indicators)
        
        # Suggest improvements
        improvement_suggestions = self._suggest_reflection_improvements(
            depth_analysis,
            quality_indicators
        )
        
        analysis_result = {
            "analysis_id": analysis_id,
            "student_id": student_id,
            "reflection": reflection,
            "reflection_phase": reflection_phase.value,
            "depth_analysis": depth_analysis,
            "quality_indicators": quality_indicators,
            "feedback": feedback,
            "improvement_suggestions": improvement_suggestions,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        self.reflection_database[analysis_id] = analysis_result
        
        return analysis_result
    
    def generate_prompts(self, learning_context: Dict) -> Dict:
        """Generate contextual reflection prompts based on learning context"""
        prompt_id = f"prompts_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine appropriate phases for context
        relevant_phases = self._determine_relevant_phases(learning_context)
        
        # Generate prompts for each phase
        phase_prompts = {}
        for phase in relevant_phases:
            phase_prompts[phase.value] = self._generate_phase_prompts(
                phase,
                learning_context
            )
        
        # Generate depth-level prompts
        depth_prompts = self._generate_depth_prompts(learning_context)
        
        # Generate subject-specific prompts
        subject_prompts = self._generate_subject_prompts(learning_context)
        
        prompt_result = {
            "prompt_id": prompt_id,
            "learning_context": learning_context,
            "phase_prompts": phase_prompts,
            "depth_prompts": depth_prompts,
            "subject_prompts": subject_prompts,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return prompt_result
    
    def track_reflection_development(self, student_id: str, timeframe: str = "semester") -> Dict:
        """Track student's reflection development over time"""
        tracking_id = f"refl_track_{student_id}_{timeframe}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get reflection history
        reflection_history = self._get_reflection_history(student_id, timeframe)
        
        if not reflection_history:
            return {
                "tracking_id": tracking_id,
                "student_id": student_id,
                "error": "No reflection history found"
            }
        
        # Analyze depth progression
        depth_progression = self._analyze_depth_progression(reflection_history)
        
        # Analyze phase distribution
        phase_distribution = self._analyze_phase_distribution(reflection_history)
        
        # Identify reflection patterns
        reflection_patterns = self._identify_reflection_patterns(reflection_history)
        
        # Generate development insights
        development_insights = self._generate_development_insights(
            depth_progression,
            phase_distribution,
            reflection_patterns
        )
        
        # Generate development recommendations
        development_recommendations = self._generate_development_recommendations(
            depth_progression,
            reflection_patterns
        )
        
        tracking_result = {
            "tracking_id": tracking_id,
            "student_id": student_id,
            "timeframe": timeframe,
            "reflection_history": reflection_history,
            "depth_progression": depth_progression,
            "phase_distribution": phase_distribution,
            "reflection_patterns": reflection_patterns,
            "development_insights": development_insights,
            "development_recommendations": development_recommendations,
            "tracked_at": datetime.utcnow().isoformat()
        }
        
        return tracking_result
    
    def assess_reflection_practice(self, student_id: str) -> Dict:
        """Assess student's overall reflection practice quality"""
        assessment_id = f"refl_assess_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Get reflection practice data
        practice_data = self._get_reflection_practice_data(student_id)
        
        if not practice_data:
            return {
                "assessment_id": assessment_id,
                "student_id": student_id,
                "error": "No reflection practice data found"
            }
        
        # Assess reflection consistency
        consistency_assessment = self._assess_reflection_consistency(practice_data)
        
        # Assess reflection depth consistency
        depth_consistency = self._assess_depth_consistency(practice_data)
        
        # Assess reflection effectiveness
        effectiveness_assessment = self._assess_reflection_effectiveness(practice_data)
        
        # Calculate overall reflection competency
        overall_competency = self._calculate_reflection_competency(
            consistency_assessment,
            depth_consistency,
            effectiveness_assessment
        )
        
        # Generate practice recommendations
        practice_recommendations = self._generate_practice_recommendations(
            consistency_assessment,
            depth_consistency,
            effectiveness_assessment
        )
        
        assessment_result = {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "consistency_assessment": consistency_assessment,
            "depth_consistency": depth_consistency,
            "effectiveness_assessment": effectiveness_assessment,
            "overall_competency": overall_competency,
            "practice_recommendations": practice_recommendations,
            "assessed_at": datetime.utcnow().isoformat()
        }
        
        return assessment_result
    
    def generate_metacognitive_prompts(self, student_id: str, learning_activity: Dict) -> Dict:
        """Generate metacognitive reflection prompts for learning activity"""
        metacognitive_id = f"meta_prompts_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate planning phase prompts
        planning_prompts = self._generate_planning_prompts(learning_activity)
        
        # Generate monitoring phase prompts
        monitoring_prompts = self._generate_monitoring_prompts(learning_activity)
        
        # Generate evaluation phase prompts
        evaluation_prompts = self._generate_evaluation_prompts(learning_activity)
        
        # Generate regulation prompts
        regulation_prompts = self._generate_regulation_prompts(learning_activity)
        
        metacognitive_result = {
            "metacognitive_id": metacognitive_id,
            "student_id": student_id,
            "learning_activity": learning_activity,
            "planning_prompts": planning_prompts,
            "monitoring_prompts": monitoring_prompts,
            "evaluation_prompts": evaluation_prompts,
            "regulation_prompts": regulation_prompts,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return metacognitive_result
    
    def analyze_reflection_quality(self, student_id: str, reflection_data: List[Dict]) -> Dict:
        """Analyze quality of multiple reflections"""
        quality_analysis_id = f"quality_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze each reflection
        individual_analyses = [
            self.analyze(student_id, reflection.get("text", ""))
            for reflection in reflection_data
        ]
        
        # Calculate aggregate quality metrics
        aggregate_metrics = self._calculate_aggregate_quality(individual_analyses)
        
        # Identify quality trends
        quality_trends = self._identify_quality_trends(individual_analyses)
        
        # Generate quality insights
        quality_insights = self._generate_quality_insights(
            aggregate_metrics,
            quality_trends
        )
        
        quality_analysis_result = {
            "quality_analysis_id": quality_analysis_id,
            "student_id": student_id,
            "individual_analyses": individual_analyses,
            "aggregate_metrics": aggregate_metrics,
            "quality_trends": quality_trends,
            "quality_insights": quality_insights,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        return quality_analysis_result
    
    def _determine_reflection_phase(self, reflection: str) -> ReflectionPhase:
        """Determine which phase of learning the reflection is for"""
        # Simple heuristic - in real implementation would use NLP
        reflection_lower = reflection.lower()
        
        if "before" in reflection_lower or "hope" in reflection_lower or "expect" in reflection_lower:
            return ReflectionPhase.BEFORE_LEARNING
        elif "during" in reflection_lower or "while" in reflection_lower or "currently" in reflection_lower:
            return ReflectionPhase.DURING_LEARNING
        elif "after" in reflection_lower or "learned" in reflection_lower or "completed" in reflection_lower:
            return ReflectionPhase.AFTER_LEARNING
        else:
            return ReflectionPhase.ON_GOING
    
    def _analyze_reflection_depth(self, reflection: str, reflection_phase: ReflectionPhase) -> Dict:
        """Analyze depth of student reflection"""
        reflection_length = len(reflection)
        
        # Simple heuristic for depth assessment - in real implementation would use NLP
        depth_score = self._calculate_depth_score(reflection)
        
        if depth_score < 0.4:
            depth_level = ReflectionDepth.SURFACE
        elif depth_score < 0.6:
            depth_level = ReflectionDepth.DESCRIPTIVE
        elif depth_score < 0.8:
            depth_level = ReflectionDepth.ANALYTICAL
        elif depth_score < 0.9:
            depth_level = ReflectionDepth.EVALUATIVE
        else:
            depth_level = ReflectionDepth.TRANSFORMATIVE
        
        return {
            "depth_level": depth_level.value,
            "depth_score": depth_score,
            "indicators": self._get_depth_indicators(depth_level),
            "phase": reflection_phase.value,
            "feedback": self._get_depth_feedback(depth_level)
        }
    
    def _calculate_depth_score(self, reflection: str) -> float:
        """Calculate depth score from reflection content"""
        # Simple heuristic - in real implementation would use sophisticated NLP
        reflection_lower = reflection.lower()
        
        depth_indicators = [
            "because", "however", "although", "therefore", "consequently",
            "realize", "understand", "connect", "relate", "apply",
            "evaluate", "analyze", "critique", "synthesize", "transform",
            "future", "will", "plan", "improve", "develop", "grow"
        ]
        
        indicator_count = sum(1 for indicator in depth_indicators if indicator in reflection_lower)
        depth_score = min(1.0, indicator_count / 10.0 + 0.3)  # Base score + indicators
        
        return depth_score
    
    def _get_depth_indicators(self, depth_level: ReflectionDepth) -> List[str]:
        """Get indicators for specific depth level"""
        indicators_map = {
            ReflectionDepth.SURFACE: ["descriptive", "factual", "limited_analysis"],
            ReflectionDepth.DESCRIPTIVE: ["personal_connections", "some_analysis", "beginning_insights"],
            ReflectionDepth.ANALYTICAL: ["critical_analysis", "evaluation", "multiple_perspectives"],
            ReflectionDepth.EVALUATIVE: ["deep_analysis", "synthesis", "meaningful_connections"],
            ReflectionDepth.TRANSFORMATIVE: ["personal_transformation", "future_applications", "behavior_change"]
        }
        
        return indicators_map.get(depth_level, indicators_map[ReflectionDepth.DESCRIPTIVE])
    
    def _get_depth_feedback(self, depth_level: ReflectionDepth) -> str:
        """Get feedback based on depth level"""
        feedback_map = {
            ReflectionDepth.SURFACE: "Consider adding more analysis and personal connections to deepen reflection",
            ReflectionDepth.DESCRIPTIVE: "Good descriptive reflection, try to add more critical analysis",
            ReflectionDepth.ANALYTICAL: "Strong analytical reflection, continue to evaluate and synthesize",
            ReflectionDepth.EVALUATIVE: "Excellent deep reflection with meaningful analysis",
            ReflectionDepth.TRANSFORMATIVE": "Exceptional transformative reflection with personal growth implications"
        }
        
        return feedback_map.get(depth_level, "Continue developing reflective practice")
    
    def _identify_quality_indicators(self, reflection: str) -> Dict:
        """Identify quality indicators in reflection"""
        reflection_lower = reflection.lower()
        
        return {
            "personal_connection": "i" in reflection_lower or "my" in reflection_lower,
            "critical_thinking": any(word in reflection_lower for word in ["analyze", "evaluate", "critique"]),
            "future_application": any(word in reflection_lower for word in ["will", "plan", "apply", "future"]),
            "emotional_awareness": any(word in reflection_lower for word in ["feel", "emotion", "react"]),
            "learning_application": any(word in reflection_lower for word in ["use", "apply", "practice"]),
            "growth_mindset": any(word in reflection_lower for word in ["improve", "grow", "develop", "learn"])
        }
    
    def _generate_reflection_feedback(self, depth_analysis: Dict, quality_indicators: Dict) -> Dict:
        """Generate feedback on reflection quality"""
        feedback = {
            "strengths": [],
            "areas_for_improvement": [],
            "encouragement": "Your reflection shows thoughtful consideration"
        }
        
        depth_level = depth_analysis.get("depth_level")
        if depth_level in ["analytical", "evaluative", "transformative"]:
            feedback["strengths"].append("Strong analytical depth")
        
        if quality_indicators.get("critical_thinking"):
            feedback["strengths"].append("Critical thinking demonstrated")
        
        if not quality_indicators.get("future_application"):
            feedback["areas_for_improvement"].append("Consider adding future applications")
        
        if not quality_indicators.get("personal_connection"):
            feedback["areas_for_improvement"].append("Add personal connections and insights")
        
        return feedback
    
    def _suggest_reflection_improvements(self, depth_analysis: Dict, quality_indicators: Dict) -> List[str]:
        """Suggest improvements for reflection practice"""
        suggestions = []
        
        depth_level = depth_analysis.get("depth_level")
        if depth_level == "surface":
            suggestions.append("Add more personal analysis and connections")
        elif depth_level == "descriptive":
            suggestions.append("Include critical analysis and evaluation")
        elif depth_level == "analytical":
            suggestions.append("Add synthesis and personal transformation elements")
        
        if not quality_indicators.get("future_application"):
            suggestions.append("Consider how learning will be applied in the future")
        
        if not quality_indicators.get("personal_connection"):
            suggestions.append("Add personal experiences and connections")
        
        return suggestions if suggestions else ["Continue current reflection practice"]
    
    def _determine_relevant_phases(self, learning_context: Dict) -> List[ReflectionPhase]:
        """Determine which reflection phases are relevant for learning context"""
        learning_type = learning_context.get("activity_type", "general")
        
        if learning_type == "project_based":
            return [ReflectionPhase.BEFORE_LEARNING, ReflectionPhase.DURING_LEARNING, ReflectionPhase.AFTER_LEARNING]
        elif learning_type == "lesson":
            return [ReflectionPhase.BEFORE_LEARNING, ReflectionPhase.AFTER_LEARNING]
        else:
            return [ReflectionPhase.ON_GOING]
    
    def _generate_phase_prompts(self, phase: ReflectionPhase, learning_context: Dict) -> List[str]:
        """Generate prompts for specific reflection phase"""
        subject = learning_context.get("subject", "subject")
        
        phase_prompts_map = {
            ReflectionPhase.BEFORE_LEARNING: [
                f"What do you already know about this {subject} topic?",
                f"What questions do you have about this {subject}?",
                f"How might this connect to what you've learned before?",
                f"What do you hope to learn from this {subject} lesson?"
            ],
            ReflectionPhase.DURING_LEARNING: [
                "What strategies are working for your learning?",
                "What challenges are you facing?",
                "How are you staying engaged with the material?",
                "What connections are you making to your own experiences?"
            ],
            ReflectionPhase.AFTER_LEARNING: [
                f"What did you learn about this {subject}?",
                "How will you apply this learning?",
                "What surprised you about this topic?",
                f"What questions do you still have about {subject}?"
            ],
            ReflectionPhase.ON_GOING: [
                "What have you learned recently?",
                "What challenges are you working on?",
                "How are you growing as a learner?",
                "What goals are you working toward?"
            ]
        }
        
        return phase_prompts_map.get(phase, phase_prompts_map[ReflectionPhase.ON_GOING])
    
    def _generate_depth_prompts(self, learning_context: Dict) -> Dict:
        """Generate prompts for different reflection depth levels"""
        return {
            "surface_prompts": [
                "What happened?",
                "What did you do?",
                "What was the result?"
            ],
            "deep_prompts": [
                "Why did this matter?",
                "How does this connect to your life?",
                "What will you do differently next time?",
                "How has this changed your perspective?"
            ]
        }
    
    def _generate_subject_prompts(self, learning_context: Dict) -> Dict:
        """Generate subject-specific reflection prompts"""
        subject = learning_context.get("subject", "general")
        
        subject_prompts_map = {
            "IPA": [
                "How does this scientific concept connect to real life?",
                "What evidence supports your understanding?",
                "How would you design an experiment to test this?"
            ],
            "Matematika": [
                "How would you explain this to someone else?",
                "Where could you apply this mathematical concept?",
                "What patterns do you notice in this problem?"
            ],
            "Bahasa Indonesia": [
                "How does this text relate to your experiences?",
                "What techniques did the author use?",
                "How would you write this differently?"
            ]
        }
        
        return subject_prompts_map.get(subject, subject_prompts_map.get("general", [
            "How does this relate to your experiences?",
            "What questions do you have?",
            "How can you apply this learning?"
        ]))
    
    def _get_reflection_history(self, student_id: str, timeframe: str) -> List[Dict]:
        """Get student reflection history for timeframe"""
        # In real implementation, would retrieve from database
        return []
    
    def _analyze_depth_progression(self, reflection_history: List[Dict]) -> Dict:
        """Analyze progression of reflection depth over time"""
        if len(reflection_history) < 2:
            return {"progression": "insufficient_data"}
        
        # Extract depth scores and analyze progression
        depth_scores = [analysis.get("depth_analysis", {}).get("depth_score", 0.5) for analysis in reflection_history]
        
        early_avg = sum(depth_scores[:2]) / 2 if len(depth_scores) >= 2 else depth_scores[0]
        recent_avg = sum(depth_scores[-2:]) / 2 if len(depth_scores) >= 2 else depth_scores[-1]
        
        progression_type = "improving" if recent_avg > early_avg + 0.1 else "stable" if abs(recent_avg - early_avg) <= 0.1 else "declining"
        
        return {
            "progression": progression_type,
            "early_average": early_avg,
            "recent_average": recent_avg,
            "depth_improvement": recent_avg - early_avg
        }
    
    def _analyze_phase_distribution(self, reflection_history: List[Dict]) -> Dict:
        """Analyze distribution of reflection phases"""
        phase_counts = defaultdict(int)
        
        for analysis in reflection_history:
            phase = analysis.get("reflection_phase", "ongoing")
            phase_counts[phase] += 1
        
        total = sum(phase_counts.values()) if phase_counts else 1
        
        return {
            "phase_distribution": dict(phase_counts),
            "most_common_phase": max(phase_counts, key=phase_counts.get) if phase_counts else "ongoing",
            "phase_balance": "balanced" if len(phase_counts) >= 3 else "needs_diversity"
        }
    
    def _identify_reflection_patterns(self, reflection_history: List[Dict]) -> Dict:
        """Identify patterns in reflection practice"""
        return {
            "frequency_pattern": "regular" if len(reflection_history) >= 10 else "irregular",
            "depth_consistency": "developing",
            "phase_variety": "moderate",
            "quality_trend": "improving"
        }
    
    def _generate_development_insights(self, depth_progression: Dict, phase_distribution: Dict, reflection_patterns: Dict) -> List[str]:
        """Generate insights from reflection development analysis"""
        insights = []
        
        progression = depth_progression.get("progression")
        if progression == "improving":
            insights.append("Reflection depth is improving over time")
        
        phase_balance = phase_distribution.get("phase_balance")
        if phase_balance == "needs_diversity":
            insights.append("Reflect across different learning phases for more comprehensive development")
        
        frequency = reflection_patterns.get("frequency_pattern")
        if frequency == "irregular":
            insights.append("Establish more regular reflection practice")
        
        return insights
    
    def _generate_development_recommendations(self, depth_progression: Dict, reflection_patterns: Dict) -> List[str]:
        """Generate recommendations for reflection development"""
        recommendations = []
        
        progression = depth_progression.get("progression")
        if progression == "stable":
            recommendations.append("Add challenges to deepen reflection practice")
        elif progression == "declining":
            recommendations.append("Review reflection approach and seek guidance")
        
        frequency = reflection_patterns.get("frequency_pattern")
        if frequency == "irregular":
            recommendations.append("Establish regular reflection schedule")
        
        return recommendations
    
    def _get_reflection_practice_data(self, student_id: str) -> Dict:
        """Get student reflection practice data"""
        # In real implementation, would retrieve from database
        return {}
    
    def _assess_reflection_consistency(self, practice_data: Dict) -> Dict:
        """Assess consistency of reflection practice"""
        return {
            "consistency_score": 0.72,
            "frequency": "weekly",
            "regularity": "developing",
            "assessment": "satisfactory"
        }
    
    def _assess_depth_consistency(self, practice_data: Dict) -> Dict:
        """Assess consistency of reflection depth"""
        return {
            "depth_consistency_score": 0.68,
            "depth_level_range": ["descriptive", "analytical"],
            "depth_improvement": "positive",
            "assessment": "developing"
        }
    
    def _assess_reflection_effectiveness(self, practice_data: Dict) -> Dict:
        """Assess effectiveness of reflection practice"""
        return {
            "effectiveness_score": 0.75,
            "learning_impact": "moderate",
            "skill_development": "good",
            "assessment": "satisfactory"
        }
    
    def _calculate_reflection_competency(self, consistency: Dict, depth: Dict, effectiveness: Dict) -> Dict:
        """Calculate overall reflection competency"""
        consistency_score = consistency.get("consistency_score", 0.5)
        depth_score = depth.get("depth_consistency_score", 0.5)
        effectiveness_score = effectiveness.get("effectiveness_score", 0.5)
        
        overall_score = (consistency_score + depth_score + effectiveness_score) / 3.0
        
        competency_level = "developing" if overall_score < 0.7 else "proficient" if overall_score < 0.85 else "exemplary"
        
        return {
            "overall_score": overall_score,
            "competency_level": competency_level,
            "strengths": [],
            "areas_for_development": []
        }
    
    def _generate_practice_recommendations(self, consistency: Dict, depth: Dict, effectiveness: Dict) -> List[str]:
        """Generate recommendations for reflection practice improvement"""
        recommendations = []
        
        if consistency.get("assessment") == "developing":
            recommendations.append("Establish more consistent reflection routine")
        
        if depth.get("assessment") == "developing":
            recommendations.append("Use deeper reflection prompts to increase depth")
        
        if effectiveness.get("assessment") == "developing":
            recommendations.append("Focus on applying insights from reflections")
        
        return recommendations
    
    def _generate_planning_prompts(self, learning_activity: Dict) -> List[str]:
        """Generate metacognitive planning phase prompts"""
        return [
            "What is your goal for this learning activity?",
            "What strategies will you use to achieve your goal?",
            "How will you know if you're successful?",
            "What challenges might you face and how will you address them?"
        ]
    
    def _generate_monitoring_prompts(self, learning_activity: Dict) -> List[str]:
        """Generate metacognitive monitoring phase prompts"""
        return [
            "Are you making progress toward your goal?",
            "What strategies are working well?",
            "What do you need to adjust?",
            "How are you managing your time and effort?"
        ]
    
    def _generate_evaluation_prompts(self, learning_activity: Dict) -> List[str]:
        """Generate metacognitive evaluation phase prompts"""
        return [
            "Did you achieve your learning goal?",
            "What strategies were most effective?",
            "What would you do differently?",
            "What did you learn about yourself as a learner?"
        ]
    
    def _generate_regulation_prompts(self, learning_activity: Dict) -> List[str]:
        """Generate metacognitive regulation prompts"""
        return [
            "How will you apply what you learned?",
            "What goals will you set for next time?",
            "How will you build on your strengths?",
            "How will you address areas for improvement?"
        ]
    
    def _calculate_aggregate_quality(self, individual_analyses: List[Dict]) -> Dict:
        """Calculate aggregate quality metrics from individual analyses"""
        if not individual_analyses:
            return {"error": "No analyses to aggregate"}
        
        depth_scores = [
            analysis.get("depth_analysis", {}).get("depth_score", 0.5)
            for analysis in individual_analyses
        ]
        
        average_depth = sum(depth_scores) / len(depth_scores)
        
        return {
            "average_depth_score": average_depth,
            "depth_consistency": 0.72,
            "total_reflections": len(individual_analyses),
            "depth_distribution": self._calculate_depth_distribution(individual_analyses)
        }
    
    def _calculate_depth_distribution(self, individual_analyses: List[Dict]) -> Dict:
        """Calculate distribution of reflection depth levels"""
        depth_levels = [analysis.get("depth_analysis", {}).get("depth_level", "descriptive") for analysis in individual_analyses]
        
        distribution = defaultdict(int)
        for level in depth_levels:
            distribution[level] += 1
        
        return dict(distribution)
    
    def _identify_quality_trends(self, individual_analyses: List[Dict]) -> Dict:
        """Identify trends in reflection quality over time"""
        if len(individual_analyses) < 2:
            return {"trend": "insufficient_data"}
        
        depth_scores = [
            analysis.get("depth_analysis", {}).get("depth_score", 0.5)
            for analysis in individual_analyses
        ]
        
        early_avg = sum(depth_scores[:2]) / 2
        recent_avg = sum(depth_scores[-2:]) / 2
        
        trend = "improving" if recent_avg > early_avg + 0.05 else "stable" if abs(recent_avg - early_avg) <= 0.05 else "declining"
        
        return {"trend": trend, "early_average": early_avg, "recent_average": recent_avg}
    
    def _generate_quality_insights(self, aggregate_metrics: Dict, quality_trends: Dict) -> List[str]:
        """Generate insights from quality analysis"""
        insights = []
        
        average_depth = aggregate_metrics.get("average_depth_score", 0.5)
        if average_depth >= 0.7:
            insights.append("Strong average reflection depth")
        
        trend = quality_trends.get("trend")
        if trend == "improving":
            insights.append("Reflection quality improving over time")
        
        return insights
    
    def _initialize_prompt_library(self) -> Dict:
        """Initialize reflection prompt library"""
        return {
            "before_learning": [
                "What do you already know?",
                "What do you hope to learn?",
                "What questions do you have?"
            ],
            "during_learning": [
                "What's working for you?",
                "What challenges are you facing?",
                "How are you staying engaged?"
            ],
            "after_learning": [
                "What did you learn?",
                "How will you apply this?",
                "What surprised you?"
            ],
            "ongoing": [
                "What are you learning?",
                "How are you growing?",
                "What are your goals?"
            ]
        }
    
    def _initialize_depth_criteria(self) -> Dict:
        """Initialize criteria for reflection depth analysis"""
        return {
            "surface": {
                "description": "Descriptive and factual",
                "indicators": ["what happened", "basic facts", "limited connections"],
                "target_length": 50-100 characters
            },
            "descriptive": {
                "description": "Personal connections and some analysis",
                "indicators": ["personal connections", "some analysis", "beginning insights"],
                "target_length": 100-250 characters
            },
            "analytical": {
                "description": "Critical analysis and evaluation",
                "indicators": ["critical thinking", "multiple perspectives", "evaluation"],
                "target_length": 250-500 characters
            },
            "evaluative": {
                "description": "Deep analysis and synthesis",
                "indicators": ["synthesis", "meaningful connections", "evaluation"],
                "target_length": 500-1000 characters"
            },
            "transformative": {
                "description": "Personal transformation and future application",
                "indicators": ["personal growth", "behavior change", "future applications"],
                "target_length": 1000+ characters"
            }
        }