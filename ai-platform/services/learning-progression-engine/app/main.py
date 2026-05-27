"""
Learning Progression Engine - Fase 5.4
Educational Intelligence Layer - Learning progression tracking and gap detection
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ENABLE_GRPC_SERVER = os.getenv("ENABLE_GRPC_SERVER", "false").lower() == "true"
ENABLE_RABBITMQ_CONSUMER = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
GRPC_PORT = int(os.getenv("GRPC_PORT", "50065"))


# Pydantic models
class MasteryTrackingRequest(BaseModel):
    """Mastery tracking request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    competency: str
    performance_data: List[Dict[str, Any]]
    context: Optional[Dict[str, Any]] = None


class MasteryTrackingResult(BaseModel):
    """Mastery tracking result"""
    request_id: str
    user_id: str
    competency: str
    mastery_level: str  # emerging, developing, proficient, advanced
    mastery_score: float
    progression_trend: str  # improving, stable, declining
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class GapDetectionRequest(BaseModel):
    """Prerequisite gap detection request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    target_competency: str
    current_mastery: Dict[str, float]
    prerequisite_map: Dict[str, List[str]]
    context: Optional[Dict[str, Any]] = None


class GapDetectionResult(BaseModel):
    """Prerequisite gap detection result"""
    request_id: str
    user_id: str
    target_competency: str
    has_gaps: bool
    missing_prerequisites: List[str]
    weak_prerequisites: List[str]
    recommended_path: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Learning progression engine
class LearningProgressionEngine:
    """Learning progression and gap detection engine"""
    
    def __init__(self):
        self.mastery_thresholds = {
            "emerging": 0.0,
            "developing": 0.4,
            "proficient": 0.7,
            "advanced": 0.9
        }
        self.progress_history = {}  # Store progress history for analytics
    
    def generate_progress_analytics(self, user_id: str, competency: str, time_range: int = 30) -> Dict:
        """Generate progress analytics for a user and competency"""
        # Get historical data for the user and competency
        history_key = f"{user_id}_{competency}"
        historical_data = self.progress_history.get(history_key, [])
        
        # Filter by time range (simplified)
        recent_data = historical_data[-time_range:] if len(historical_data) > time_range else historical_data
        
        if not recent_data:
            return {
                "user_id": user_id,
                "competency": competency,
                "message": "No historical data available",
                "analytics": {}
            }
        
        # Calculate analytics
        scores = [item.get("score", 0) for item in recent_data]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        max_score = max(scores) if scores else 0.0
        min_score = min(scores) if scores else 0.0
        
        # Calculate trend
        trend = self._calculate_progress_trend(scores)
        
        # Calculate consistency
        consistency = self._calculate_consistency(scores)
        
        # Identify learning velocity
        velocity = self._calculate_learning_velocity(recent_data)
        
        return {
            "user_id": user_id,
            "competency": competency,
            "time_range_days": time_range,
            "analytics": {
                "average_score": avg_score,
                "max_score": max_score,
                "min_score": min_score,
                "trend": trend,
                "consistency": consistency,
                "learning_velocity": velocity,
                "total_data_points": len(recent_data)
            },
            "insights": self._generate_progress_insights(trend, consistency, velocity)
        }
    
    def generate_remediation_recommendations(self, user_id: str, target_competency: str, current_mastery: Dict[str, float], prerequisite_map: Dict[str, List[str]]) -> Dict:
        """Generate detailed remediation recommendations"""
        # Detect gaps
        gap_result = self.detect_gaps(GapDetectionRequest(
            user_id=user_id,
            target_competency=target_competency,
            current_mastery=current_mastery,
            prerequisite_map=prerequisite_map
        ))
        
        # Generate specific remediation strategies
        remediation_plan = []
        
        for missing in gap_result["missing_prerequisites"]:
            remediation_plan.append({
                "competency": missing,
                "priority": "critical",
                "strategy": "intensive_remediation",
                "estimated_duration_hours": 8,
                "resources": self._get_remediation_resources(missing, "critical"),
                "activities": self._get_remediation_activities(missing, "critical")
            })
        
        for weak in gap_result["weak_prerequisites"]:
            remediation_plan.append({
                "competency": weak,
                "priority": "high",
                "strategy": "reinforcement",
                "estimated_duration_hours": 4,
                "resources": self._get_remediation_resources(weak, "high"),
                "activities": self._get_remediation_activities(weak, "high")
            })
        
        # Add target competency preparation
        remediation_plan.append({
            "competency": target_competency,
            "priority": "medium",
            "strategy": "preparation",
            "estimated_duration_hours": 6,
            "resources": self._get_remediation_resources(target_competency, "medium"),
            "activities": self._get_remediation_activities(target_competency, "medium")
        })
        
        # Calculate total estimated duration
        total_duration = sum(item.get("estimated_duration_hours", 0) for item in remediation_plan)
        
        return {
            "user_id": user_id,
            "target_competency": target_competency,
            "remediation_plan": remediation_plan,
            "total_estimated_duration_hours": total_duration,
            "has_gaps": gap_result["has_gaps"],
            "recommended_path": gap_result["recommended_path"]
        }
    
    def record_progress(self, user_id: str, competency: str, score: float, context: Dict = None):
        """Record progress data point"""
        history_key = f"{user_id}_{competency}"
        
        if history_key not in self.progress_history:
            self.progress_history[history_key] = []
        
        self.progress_history[history_key].append({
            "score": score,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        })
    
    def _calculate_progress_trend(self, scores: List[float]) -> str:
        """Calculate progress trend"""
        if len(scores) < 2:
            return "insufficient_data"
        
        # Simple linear regression
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        avg_first = sum(first_half) / len(first_half) if first_half else 0
        avg_second = sum(second_half) / len(second_half) if second_half else 0
        
        difference = avg_second - avg_first
        
        if difference > 0.1:
            return "improving"
        elif difference < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calculate score consistency (inverse of variance)"""
        if len(scores) < 2:
            return 1.0
        
        avg = sum(scores) / len(scores)
        variance = sum((score - avg) ** 2 for score in scores) / len(scores)
        
        # Convert variance to consistency score (0-1)
        consistency = max(0, 1 - variance)
        return consistency
    
    def _calculate_learning_velocity(self, data: List[Dict]) -> float:
        """Calculate learning velocity (score improvement per time unit)"""
        if len(data) < 2:
            return 0.0
        
        first_item = data[0]
        last_item = data[-1]
        
        score_diff = last_item.get("score", 0) - first_item.get("score", 0)
        
        # Calculate time difference (simplified - assumes one day per data point)
        time_diff = len(data) - 1
        
        if time_diff == 0:
            return 0.0
        
        velocity = score_diff / time_diff
        return velocity
    
    def _generate_progress_insights(self, trend: str, consistency: float, velocity: float) -> List[str]:
        """Generate insights from progress analytics"""
        insights = []
        
        if trend == "improving":
            insights.append("Student is showing consistent improvement")
        elif trend == "declining":
            insights.append("Student performance is declining - intervention recommended")
        else:
            insights.append("Student performance is stable")
        
        if consistency > 0.8:
            insights.append("High consistency in performance")
        elif consistency < 0.5:
            insights.append("Low consistency - performance varies significantly")
        
        if velocity > 0.05:
            insights.append("Good learning velocity - student is progressing quickly")
        elif velocity < 0:
            insights.append("Negative learning velocity - student may be struggling")
        
        return insights
    
    def _get_remediation_resources(self, competency: str, priority: str) -> List[str]:
        """Get remediation resources for competency"""
        base_resources = [
            f"Video tutorials for {competency}",
            f"Practice exercises for {competency}",
            f"Study guides for {competency}"
        ]
        
        if priority == "critical":
            return base_resources + [
                f"One-on-one tutoring for {competency}",
                f"Intensive workshop on {competency}",
                f"Interactive simulations for {competency}"
            ]
        elif priority == "high":
            return base_resources + [
                f"Group study sessions for {competency}",
                f"Additional practice problems for {competency}"
            ]
        else:
            return base_resources
    
    def _get_remediation_activities(self, competency: str, priority: str) -> List[str]:
        """Get remediation activities for competency"""
        base_activities = [
            f"Review foundational concepts of {competency}",
            f"Complete practice exercises for {competency}",
            f"Self-assessment on {competency}"
        ]
        
        if priority == "critical":
            return base_activities + [
                f"Daily practice sessions for {competency}",
                f"Peer tutoring for {competency}",
                f"Teacher-guided review of {competency}"
            ]
        elif priority == "high":
            return base_activities + [
                f"Weekly practice sessions for {competency}",
                f"Group problem-solving for {competency}"
            ]
        else:
            return base_activities
    
    def track_mastery(self, request: MasteryTrackingRequest) -> Dict:
        """Track mastery progression"""
        # Calculate mastery score from performance data
        total_score = 0
        total_items = len(request.performance_data)
        
        for item in request.performance_data:
            score = item.get("score", 0)
            weight = item.get("weight", 1.0)
            total_score += score * weight
        
        mastery_score = total_score / total_items if total_items > 0 else 0.0
        
        # Determine mastery level
        mastery_level = self._get_mastery_level(mastery_score)
        
        # Determine progression trend
        progression_trend = self._calculate_trend(request.performance_data)
        
        # Generate recommendations
        recommendations = self._generate_mastery_recommendations(mastery_level, mastery_score)
        
        return {
            "mastery_level": mastery_level,
            "mastery_score": mastery_score,
            "progression_trend": progression_trend,
            "recommendations": recommendations
        }
    
    def detect_gaps(self, request: GapDetectionRequest) -> Dict:
        """Detect prerequisite gaps"""
        missing_prerequisites = []
        weak_prerequisites = []
        
        prerequisites = request.prerequisite_map.get(request.target_competency, [])
        
        for prereq in prerequisites:
            mastery = request.current_mastery.get(prereq, 0.0)
            
            if mastery < 0.4:
                missing_prerequisites.append(prereq)
            elif mastery < 0.7:
                weak_prerequisites.append(prereq)
        
        has_gaps = len(missing_prerequisites) > 0 or len(weak_prerequisites) > 0
        
        # Generate recommended learning path
        recommended_path = self._generate_learning_path(
            request.target_competency,
            missing_prerequisites,
            weak_prerequisites,
            request.prerequisite_map
        )
        
        return {
            "has_gaps": has_gaps,
            "missing_prerequisites": missing_prerequisites,
            "weak_prerequisites": weak_prerequisites,
            "recommended_path": recommended_path
        }
    
    def _get_mastery_level(self, score: float) -> str:
        """Get mastery level from score"""
        if score >= self.mastery_thresholds["advanced"]:
            return "advanced"
        elif score >= self.mastery_thresholds["proficient"]:
            return "proficient"
        elif score >= self.mastery_thresholds["developing"]:
            return "developing"
        else:
            return "emerging"
    
    def _calculate_trend(self, performance_data: List[Dict]) -> str:
        """Calculate progression trend"""
        if len(performance_data) < 2:
            return "stable"
        
        # Get first and last scores
        first_score = performance_data[0].get("score", 0)
        last_score = performance_data[-1].get("score", 0)
        
        if last_score > first_score + 0.1:
            return "improving"
        elif last_score < first_score - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _generate_mastery_recommendations(self, level: str, score: float) -> List[str]:
        """Generate mastery recommendations"""
        recommendations = []
        
        if level == "emerging":
            recommendations.append("Focus on foundational concepts")
            recommendations.append("Practice basic exercises")
            recommendations.append("Seek additional support")
        elif level == "developing":
            recommendations.append("Continue practice with varied problems")
            recommendations.append("Focus on application")
            recommendations.append("Review foundational concepts")
        elif level == "proficient":
            recommendations.append("Challenge with complex problems")
            recommendations.append("Apply to real-world scenarios")
            recommendations.append("Teach others to reinforce learning")
        elif level == "advanced":
            recommendations.append("Explore advanced topics")
            recommendations.append("Create new solutions")
            recommendations.append("Mentor others")
        
        return recommendations
    
    def _generate_learning_path(self, target: str, missing: List[str], weak: List[str], prereq_map: Dict) -> List[str]:
        """Generate recommended learning path"""
        path = []
        
        # Add missing prerequisites first
        for prereq in missing:
            path.append(f"Master {prereq}")
        
        # Add weak prerequisites
        for prereq in weak:
            path.append(f"Strengthen {prereq}")
        
        # Add target competency
        path.append(f"Learn {target}")
        
        return path


# Initialize learning progression engine
progression_engine = LearningProgressionEngine()


# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Import and start gRPC server if enabled
    if ENABLE_GRPC_SERVER:
        from .grpc_server import serve
        import asyncio
        asyncio.create_task(serve(GRPC_PORT))
    
    # Import and start RabbitMQ consumer if enabled
    if ENABLE_RABBITMQ_CONSUMER:
        from .consumer import AsyncLearningProgressionEngineConsumer
        consumer = AsyncLearningProgressionEngineConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Learning Progression Engine",
    description="Educational Intelligence Layer - Learning progression tracking and gap detection",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "learning-progression-engine",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Progression endpoints
@app.post("/progression/mastery")
async def track_mastery(request: MasteryTrackingRequest):
    """Track mastery progression"""
    result = progression_engine.track_mastery(request)
    return MasteryTrackingResult(
        request_id=request.request_id,
        user_id=request.user_id,
        competency=request.competency,
        mastery_level=result["mastery_level"],
        mastery_score=result["mastery_score"],
        progression_trend=result["progression_trend"],
        recommendations=result["recommendations"]
    )


@app.post("/progression/gaps")
async def detect_gaps(request: GapDetectionRequest):
    """Detect prerequisite gaps"""
    result = progression_engine.detect_gaps(request)
    return GapDetectionResult(
        request_id=request.request_id,
        user_id=request.user_id,
        target_competency=request.target_competency,
        has_gaps=result["has_gaps"],
        missing_prerequisites=result["missing_prerequisites"],
        weak_prerequisites=result["weak_prerequisites"],
        recommended_path=result["recommended_path"]
    )


@app.get("/progression/levels")
async def get_mastery_levels():
    """Get mastery level thresholds"""
    return progression_engine.mastery_thresholds


# Progress analytics endpoints
@app.get("/progression/analytics")
async def get_progress_analytics(user_id: str, competency: str, time_range: int = 30):
    """Generate progress analytics"""
    result = progression_engine.generate_progress_analytics(user_id, competency, time_range)
    return result


@app.post("/progression/record")
async def record_progress(user_id: str, competency: str, score: float, context: Optional[Dict] = None):
    """Record progress data point"""
    progression_engine.record_progress(user_id, competency, score, context)
    return {
        "status": "recorded",
        "user_id": user_id,
        "competency": competency,
        "score": score
    }


# Remediation recommendations endpoints
@app.post("/progression/remediation")
async def get_remediation_recommendations(user_id: str, target_competency: str, current_mastery: Dict[str, float], prerequisite_map: Dict[str, List[str]]):
    """Generate detailed remediation recommendations"""
    result = progression_engine.generate_remediation_recommendations(user_id, target_competency, current_mastery, prerequisite_map)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8016)
