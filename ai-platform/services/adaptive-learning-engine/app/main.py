"""
Adaptive Learning Engine - Fase 5.6
Educational Intelligence Layer - Personalized learning path generation
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50067"))


# Pydantic models
class PersonalizedPathRequest(BaseModel):
    """Personalized learning path request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    target_competency: str
    current_mastery: Dict[str, float]
    learning_style: Optional[str] = None  # visual, auditory, kinesthetic, reading
    preferences: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None


class PersonalizedPathResult(BaseModel):
    """Personalized learning path result"""
    request_id: str
    user_id: str
    target_competency: str
    learning_path: List[Dict[str, Any]]
    estimated_duration: int
    adaptation_notes: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ContentSelectionRequest(BaseModel):
    """Adaptive content selection request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    competency: str
    current_level: str
    learning_style: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ContentSelectionResult(BaseModel):
    """Adaptive content selection result"""
    request_id: str
    user_id: str
    competency: str
    recommended_content: List[Dict[str, Any]]
    adaptation_reason: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Adaptive learning engine
class AdaptiveLearningEngine:
    """Personalized learning and content adaptation engine"""
    
    def __init__(self):
        self.learning_style_map = {
            "visual": ["videos", "diagrams", "infographics", "charts"],
            "auditory": ["podcasts", "audio lectures", "discussions", "explanations"],
            "kinesthetic": ["hands-on activities", "experiments", "simulations", "projects"],
            "reading": ["textbooks", "articles", "notes", "written exercises"]
        }
        self.ml_models = {}  # Store trained ML models
        self.ab_tests = {}  # Store A/B test configurations and results
        self.user_model_versions = {}  # Track which model version each user is assigned
    
    def train_adaptive_model(self, training_data: List[Dict], model_type: str = "path_recommendation") -> Dict:
        """Train ML model for adaptive learning"""
        model_id = f"{model_type}_{len(self.ml_models)}"
        
        # Simplified ML training (in production, use proper ML libraries)
        if model_type == "path_recommendation":
            model = self._train_path_model(training_data)
        elif model_type == "content_adaptation":
            model = self._train_content_model(training_data)
        elif model_type == "difficulty_adjustment":
            model = self._train_difficulty_model(training_data)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Store model
        self.ml_models[model_id] = {
            "id": model_id,
            "type": model_type,
            "model": model,
            "training_data_size": len(training_data),
            "created_at": datetime.utcnow().isoformat(),
            "performance": self._evaluate_model(model, training_data)
        }
        
        return {
            "model_id": model_id,
            "model_type": model_type,
            "training_data_size": len(training_data),
            "performance": self.ml_models[model_id]["performance"]
        }
    
    def _train_path_model(self, training_data: List[Dict]) -> Dict:
        """Train path recommendation model (simplified)"""
        # In production, use proper ML algorithms like random forests, neural networks
        # Here we use a simplified heuristic-based model
        
        # Extract patterns from training data
        success_patterns = {}
        
        for data_point in training_data:
            mastery = data_point.get("current_mastery", {})
            target = data_point.get("target_competency", "")
            success = data_point.get("success", False)
            
            pattern_key = tuple(sorted(mastery.items()))
            
            if pattern_key not in success_patterns:
                success_patterns[pattern_key] = {"success": 0, "total": 0}
            
            success_patterns[pattern_key]["total"] += 1
            if success:
                success_patterns[pattern_key]["success"] += 1
        
        # Calculate success rates
        for pattern in success_patterns.values():
            pattern["success_rate"] = pattern["success"] / pattern["total"] if pattern["total"] > 0 else 0
        
        return {
            "type": "path_recommendation",
            "patterns": success_patterns,
            "version": "1.0"
        }
    
    def _train_content_model(self, training_data: List[Dict]) -> Dict:
        """Train content adaptation model (simplified)"""
        # Extract learning style effectiveness patterns
        style_effectiveness = {}
        
        for data_point in training_data:
            learning_style = data_point.get("learning_style", "")
            content_type = data_point.get("content_type", "")
            engagement = data_point.get("engagement", 0)
            
            key = f"{learning_style}_{content_type}"
            
            if key not in style_effectiveness:
                style_effectiveness[key] = {"total_engagement": 0, "count": 0}
            
            style_effectiveness[key]["total_engagement"] += engagement
            style_effectiveness[key]["count"] += 1
        
        # Calculate average engagement
        for style in style_effectiveness.values():
            style["avg_engagement"] = style["total_engagement"] / style["count"] if style["count"] > 0 else 0
        
        return {
            "type": "content_adaptation",
            "style_effectiveness": style_effectiveness,
            "version": "1.0"
        }
    
    def _train_difficulty_model(self, training_data: List[Dict]) -> Dict:
        """Train difficulty adjustment model (simplified)"""
        # Extract difficulty-performance patterns
        difficulty_patterns = {}
        
        for data_point in training_data:
            difficulty = data_point.get("difficulty", "")
            performance = data_point.get("performance", 0)
            mastery_level = data_point.get("mastery_level", "")
            
            key = f"{mastery_level}_{difficulty}"
            
            if key not in difficulty_patterns:
                difficulty_patterns[key] = {"total_performance": 0, "count": 0}
            
            difficulty_patterns[key]["total_performance"] += performance
            difficulty_patterns[key]["count"] += 1
        
        # Calculate optimal difficulty
        for pattern in difficulty_patterns.values():
            pattern["avg_performance"] = pattern["total_performance"] / pattern["count"] if pattern["count"] > 0 else 0
        
        return {
            "type": "difficulty_adjustment",
            "difficulty_patterns": difficulty_patterns,
            "version": "1.0"
        }
    
    def _evaluate_model(self, model: Dict, test_data: List[Dict]) -> Dict:
        """Evaluate model performance (simplified)"""
        # In production, use proper evaluation metrics
        # Here we use simplified accuracy calculation
        
        if model["type"] == "path_recommendation":
            # Calculate path prediction accuracy
            correct_predictions = 0
            total_predictions = len(test_data)
            
            for data_point in test_data:
                mastery = data_point.get("current_mastery", {})
                pattern_key = tuple(sorted(mastery.items()))
                
                if pattern_key in model["patterns"]:
                    success_rate = model["patterns"][pattern_key]["success_rate"]
                    predicted_success = success_rate > 0.5
                    actual_success = data_point.get("success", False)
                    
                    if predicted_success == actual_success:
                        correct_predictions += 1
            
            accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
            return {"accuracy": accuracy, "total_predictions": total_predictions}
        
        else:
            return {"accuracy": 0.75, "note": "Simplified evaluation"}
    
    def create_ab_test(self, test_config: Dict) -> Dict:
        """Create A/B test for comparing adaptive learning strategies"""
        test_id = f"ab_test_{len(self.ab_tests)}"
        
        # Validate test configuration
        required_fields = ["name", "description", "variant_a", "variant_b", "success_metric"]
        for field in required_fields:
            if field not in test_config:
                raise ValueError(f"Missing required field: {field}")
        
        # Create test configuration
        self.ab_tests[test_id] = {
            "id": test_id,
            "name": test_config["name"],
            "description": test_config["description"],
            "variant_a": test_config["variant_a"],
            "variant_b": test_config["variant_b"],
            "success_metric": test_config["success_metric"],
            "traffic_split": test_config.get("traffic_split", 0.5),  # 50/50 split by default
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "results": {
                "variant_a": {"participants": 0, "successes": 0},
                "variant_b": {"participants": 0, "successes": 0}
            }
        }
        
        return {
            "test_id": test_id,
            "status": "created",
            "configuration": self.ab_tests[test_id]
        }
    
    def assign_user_to_variant(self, user_id: str, test_id: str) -> Dict:
        """Assign user to A/B test variant"""
        if test_id not in self.ab_tests:
            raise HTTPException(status_code=404, detail="Test not found")
        
        test = self.ab_tests[test_id]
        
        # Check if user already assigned
        if user_id in self.user_model_versions:
            existing_assignment = self.user_model_versions[user_id].get(test_id)
            if existing_assignment:
                return {"user_id": user_id, "variant": existing_assignment, "status": "already_assigned"}
        
        # Assign based on traffic split
        import random
        import hashlib
        
        # Consistent hash-based assignment
        hash_value = int(hashlib.md5(f"{user_id}_{test_id}".encode()).hexdigest(), 16)
        assigned_variant = "variant_a" if (hash_value % 100) < (test["traffic_split"] * 100) else "variant_b"
        
        # Record assignment
        if user_id not in self.user_model_versions:
            self.user_model_versions[user_id] = {}
        
        self.user_model_versions[user_id][test_id] = assigned_variant
        test["results"][assigned_variant]["participants"] += 1
        
        return {
            "user_id": user_id,
            "test_id": test_id,
            "variant": assigned_variant,
            "status": "assigned"
        }
    
    def record_ab_test_result(self, user_id: str, test_id: str, success: bool) -> Dict:
        """Record A/B test result"""
        if test_id not in self.ab_tests:
            raise HTTPException(status_code=404, detail="Test not found")
        
        test = self.ab_tests[test_id]
        
        # Get user's assigned variant
        if user_id not in self.user_model_versions or test_id not in self.user_model_versions[user_id]:
            raise HTTPException(status_code=400, detail="User not assigned to test")
        
        variant = self.user_model_versions[user_id][test_id]
        
        # Record result
        if success:
            test["results"][variant]["successes"] += 1
        
        # Calculate current results
        results = self._calculate_ab_test_results(test)
        
        return {
            "test_id": test_id,
            "user_id": user_id,
            "variant": variant,
            "success": success,
            "current_results": results
        }
    
    def _calculate_ab_test_results(self, test: Dict) -> Dict:
        """Calculate A/B test results"""
        variant_a = test["results"]["variant_a"]
        variant_b = test["results"]["variant_b"]
        
        # Calculate success rates
        success_rate_a = variant_a["successes"] / variant_a["participants"] if variant_a["participants"] > 0 else 0
        success_rate_b = variant_b["successes"] / variant_b["participants"] if variant_b["participants"] > 0 else 0
        
        # Calculate statistical significance (simplified)
        from math import sqrt
        def calculate_significance(p1, n1, p2, n2):
            if n1 == 0 or n2 == 0:
                return 0
            pooled_p = (p1 * n1 + p2 * n2) / (n1 + n2)
            se = sqrt(pooled_p * (1 - pooled_p) * (1/n1 + 1/n2))
            if se == 0:
                return 0
            z = (p1 - p2) / se
            return z
        
        z_score = calculate_significance(success_rate_a, variant_a["participants"], success_rate_b, variant_b["participants"])
        
        return {
            "variant_a": {
                "success_rate": success_rate_a,
                "participants": variant_a["participants"]
            },
            "variant_b": {
                "success_rate": success_rate_b,
                "participants": variant_b["participants"]
            },
            "statistical": {
                "z_score": z_score,
                "significant": abs(z_score) > 1.96  # 95% confidence level
            }
        }
    
    def get_ab_test_results(self, test_id: str) -> Dict:
        """Get A/B test results"""
        if test_id not in self.ab_tests:
            raise HTTPException(status_code=404, detail="Test not found")
        
        test = self.ab_tests[test_id]
        results = self._calculate_ab_test_results(test)
        
        return {
            "test_id": test_id,
            "test_name": test["name"],
            "status": test["status"],
            "results": results,
            "created_at": test["created_at"]
        }
    
    def generate_personalized_path(self, request: PersonalizedPathRequest) -> Dict:
        """Generate personalized learning path"""
        # Identify gaps
        gaps = self._identify_gaps(request.target_competency, request.current_mastery)
        
        # Build learning path
        learning_path = []
        
        # Add prerequisite learning
        for gap in gaps["missing"]:
            learning_path.append({
                "step": f"Learn {gap}",
                "type": "prerequisite",
                "priority": "high",
                "estimated_hours": 5
            })
        
        # Add weak areas
        for gap in gaps["weak"]:
            learning_path.append({
                "step": f"Strengthen {gap}",
                "type": "reinforcement",
                "priority": "medium",
                "estimated_hours": 3
            })
        
        # Add target competency
        learning_path.append({
            "step": f"Master {request.target_competency}",
            "type": "target",
            "priority": "high",
            "estimated_hours": 10
        })
        
        # Adapt based on learning style
        if request.learning_style:
            learning_path = self._adapt_for_learning_style(learning_path, request.learning_style)
        
        # Calculate estimated duration
        estimated_duration = sum(step.get("estimated_hours", 0) for step in learning_path)
        
        # Generate adaptation notes
        adaptation_notes = self._generate_adaptation_notes(request)
        
        return {
            "learning_path": learning_path,
            "estimated_duration": estimated_duration,
            "adaptation_notes": adaptation_notes
        }
    
    def select_content(self, request: ContentSelectionRequest) -> Dict:
        """Select adaptive content based on user profile"""
        # Get content types based on learning style
        content_types = self.learning_style_map.get(request.learning_style, ["mixed"])
        
        # Generate recommended content
        recommended_content = []
        
        for content_type in content_types[:3]:
            recommended_content.append({
                "type": content_type,
                "competency": request.competency,
                "level": request.current_level,
                "adaptation": f"Adapted for {request.learning_style} learning style"
            })
        
        # Add general content
        recommended_content.append({
            "type": "practice_exercises",
            "competency": request.competency,
            "level": request.current_level,
            "adaptation": "Adaptive difficulty based on performance"
        })
        
        # Generate adaptation reason
        adaptation_reason = f"Content selected based on {request.learning_style} learning style and current {request.current_level} level"
        
        return {
            "recommended_content": recommended_content,
            "adaptation_reason": adaptation_reason
        }
    
    def _identify_gaps(self, target: str, mastery: Dict[str, float]) -> Dict:
        """Identify learning gaps"""
        missing = []
        weak = []
        
        for competency, score in mastery.items():
            if score < 0.4:
                missing.append(competency)
            elif score < 0.7:
                weak.append(competency)
        
        return {
            "missing": missing,
            "weak": weak
        }
    
    def _adapt_for_learning_style(self, path: List[Dict], learning_style: str) -> List[Dict]:
        """Adapt learning path for learning style"""
        adapted_path = []
        
        for step in path:
            adapted_step = step.copy()
            
            # Add learning style specific resources
            resources = self.learning_style_map.get(learning_style, [])
            adapted_step["recommended_resources"] = resources
            
            adapted_path.append(adapted_step)
        
        return adapted_path
    
    def _generate_adaptation_notes(self, request: PersonalizedPathRequest) -> List[str]:
        """Generate adaptation notes"""
        notes = []
        
        if request.learning_style:
            notes.append(f"Path adapted for {request.learning_style} learning style")
        
        if request.preferences:
            notes.append("Path customized based on user preferences")
        
        if len(request.current_mastery) > 0:
            notes.append("Path optimized based on current mastery levels")
        
        return notes


# Initialize adaptive learning engine
adaptive_engine = AdaptiveLearningEngine()


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
        from .consumer import AsyncAdaptiveLearningEngineConsumer
        consumer = AsyncAdaptiveLearningEngineConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Adaptive Learning Engine",
    description="Educational Intelligence Layer - Personalized learning path generation",
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
        "service": "adaptive-learning-engine",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Adaptive learning endpoints
@app.post("/adaptive/path")
async def generate_personalized_path(request: PersonalizedPathRequest):
    """Generate personalized learning path"""
    result = adaptive_engine.generate_personalized_path(request)
    return PersonalizedPathResult(
        request_id=request.request_id,
        user_id=request.user_id,
        target_competency=request.target_competency,
        learning_path=result["learning_path"],
        estimated_duration=result["estimated_duration"],
        adaptation_notes=result["adaptation_notes"]
    )


@app.post("/adaptive/content")
async def select_adaptive_content(request: ContentSelectionRequest):
    """Select adaptive content"""
    result = adaptive_engine.select_content(request)
    return ContentSelectionResult(
        request_id=request.request_id,
        user_id=request.user_id,
        competency=request.competency,
        recommended_content=result["recommended_content"],
        adaptation_reason=result["adaptation_reason"]
    )


@app.get("/adaptive/learning-styles")
async def get_learning_styles():
    """Get available learning styles"""
    return adaptive_engine.learning_style_map


# ML model training endpoints
@app.post("/adaptive/train-model")
async def train_adaptive_model(training_data: List[Dict], model_type: str = "path_recommendation"):
    """Train ML model for adaptive learning"""
    result = adaptive_engine.train_adaptive_model(training_data, model_type)
    return result


@app.get("/adaptive/models")
async def list_models():
    """List trained ML models"""
    return {
        "models": [
            {
                "id": model_id,
                "type": model["type"],
                "created_at": model["created_at"],
                "performance": model["performance"]
            }
            for model_id, model in adaptive_engine.ml_models.items()
        ],
        "count": len(adaptive_engine.ml_models)
    }


# A/B testing endpoints
@app.post("/adaptive/ab-test")
async def create_ab_test(test_config: Dict[str, Any]):
    """Create A/B test for comparing adaptive learning strategies"""
    result = adaptive_engine.create_ab_test(test_config)
    return result


@app.post("/adaptive/ab-test/assign")
async def assign_user_to_variant(user_id: str, test_id: str):
    """Assign user to A/B test variant"""
    result = adaptive_engine.assign_user_to_variant(user_id, test_id)
    return result


@app.post("/adaptive/ab-test/result")
async def record_ab_test_result(user_id: str, test_id: str, success: bool):
    """Record A/B test result"""
    result = adaptive_engine.record_ab_test_result(user_id, test_id, success)
    return result


@app.get("/adaptive/ab-test/{test_id}/results")
async def get_ab_test_results(test_id: str):
    """Get A/B test results"""
    result = adaptive_engine.get_ab_test_results(test_id)
    return result


@app.get("/adaptive/ab-tests")
async def list_ab_tests():
    """List all A/B tests"""
    return {
        "tests": [
            {
                "id": test_id,
                "name": test["name"],
                "status": test["status"],
                "created_at": test["created_at"]
            }
            for test_id, test in adaptive_engine.ab_tests.items()
        ],
        "count": len(adaptive_engine.ab_tests)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8018)
