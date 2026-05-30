"""
Recommendation Engine - Fase 5.7
Educational Intelligence Layer - Content recommendation algorithms
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50068"))


# Pydantic models
class RecommendationRequest(BaseModel):
    """Content recommendation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    context: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    strategy: str = "hybrid"  # collaborative, content_based, hybrid


class RecommendationResult(BaseModel):
    """Content recommendation result"""
    request_id: str
    user_id: str
    recommendations: List[Dict[str, Any]]
    strategy_used: str
    confidence_scores: List[float]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Recommendation engine
class RecommendationEngine:
    """Content recommendation engine"""
    
    def __init__(self):
        self.content_database = {}  # In-memory content database
        self.user_profiles = {}  # In-memory user profiles
        self.recommendation_cache = {}  # Cache for recommendations
        self.performance_metrics = {
            "total_recommendations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_response_time_ms": 0
        }
    
    def generate_recommendations_optimized(self, request: RecommendationRequest) -> Dict:
        """Generate optimized content recommendations with caching"""
        import time
        start_time = time.time()
        
        # Check cache
        cache_key = self._generate_cache_key(request)
        if cache_key in self.recommendation_cache:
            self.performance_metrics["cache_hits"] += 1
            cached_result = self.recommendation_cache[cache_key]
            
            # Update performance metrics
            response_time = (time.time() - start_time) * 1000
            self._update_performance_metrics(response_time)
            
            return {
                **cached_result,
                "cached": True,
                "response_time_ms": response_time
            }
        
        self.performance_metrics["cache_misses"] += 1
        
        # Get user profile
        user_profile = self.user_profiles.get(request.user_id, self._create_default_profile(request.user_id))
        
        # Generate recommendations based on strategy with advanced algorithms
        if request.strategy == "collaborative":
            recommendations = self._advanced_collaborative_filtering(user_profile)
        elif request.strategy == "content_based":
            recommendations = self._advanced_content_based_filtering(user_profile)
        elif request.strategy == "matrix_factorization":
            recommendations = self._matrix_factorization_recommendation(user_profile)
        elif request.strategy == "deep_learning":
            recommendations = self._deep_learning_recommendation(user_profile)
        else:  # hybrid
            recommendations = self._advanced_hybrid_filtering(user_profile)
        
        # Calculate confidence scores with advanced scoring
        confidence_scores = self._calculate_advanced_confidence(recommendations, user_profile)
        
        result = {
            "recommendations": recommendations,
            "strategy_used": request.strategy,
            "confidence_scores": confidence_scores
        }
        
        # Cache result (with TTL)
        self.recommendation_cache[cache_key] = {
            **result,
            "cached": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update performance metrics
        response_time = (time.time() - start_time) * 1000
        self._update_performance_metrics(response_time)
        
        self.performance_metrics["total_recommendations"] += 1
        
        return {
            **result,
            "cached": False,
            "response_time_ms": response_time
        }
    
    def _advanced_collaborative_filtering(self, user_profile: Dict) -> List[Dict]:
        """Advanced collaborative filtering with weighted similarity"""
        recommendations = []
        
        # Find similar users with advanced similarity calculation
        similar_users = self._find_similar_users_advanced(user_profile)
        
        # Weight recommendations by similarity and recency
        for similar_user in similar_users[:10]:
            similarity_weight = similar_user["similarity"]
            
            for content_item in similar_user.get("history", []):
                if content_item not in user_profile.get("history", []):
                    # Check if already recommended
                    existing_rec = next((r for r in recommendations if r["content_id"] == content_item), None)
                    
                    if existing_rec:
                        # Update weight
                        existing_rec["confidence"] += 0.1 * similarity_weight
                        existing_rec["similar_users"] += 1
                    else:
                        recommendations.append({
                            "content_id": content_item,
                            "reason": "similar users liked this",
                            "confidence": 0.7 * similarity_weight,
                            "similar_users": 1,
                            "method": "collaborative_filtering"
                        })
        
        # Sort by confidence and apply diversification
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        recommendations = self._diversify_recommendations(recommendations)
        
        return recommendations[:15]
    
    def _advanced_content_based_filtering(self, user_profile: Dict) -> List[Dict]:
        """Advanced content-based filtering with semantic similarity"""
        recommendations = []
        
        # Get user interests with weights
        interests = user_profile.get("interests", [])
        interest_weights = {interest: 1.0 for interest in interests}
        
        # Update weights based on engagement
        for engagement in user_profile.get("engagement_history", []):
            content_interest = engagement.get("interest", "")
            if content_interest in interest_weights:
                interest_weights[content_interest] += engagement.get("score", 0)
        
        # Find similar content with advanced matching
        for interest, weight in interest_weights.items():
            similar_content = self._find_similar_content_advanced(interest, weight)
            
            for content in similar_content:
                if content not in user_profile.get("history", []):
                    existing_rec = next((r for r in recommendations if r["content_id"] == content), None)
                    
                    if existing_rec:
                        existing_rec["confidence"] += 0.1 * weight
                    else:
                        recommendations.append({
                            "content_id": content,
                            "reason": f"matches your interest in {interest}",
                            "confidence": 0.8 * min(weight, 2.0) / 2.0,
                            "interest_match": interest,
                            "method": "content_based_filtering"
                        })
        
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        recommendations = self._diversify_recommendations(recommendations)
        
        return recommendations[:15]
    
    def _matrix_factorization_recommendation(self, user_profile: Dict) -> List[Dict]:
        """Matrix factorization recommendation (simplified)"""
        # In production, use proper matrix factorization algorithms
        # Here we use a simplified approach
        
        user_id = user_profile["user_id"]
        
        # Get user's interaction matrix (simplified)
        user_interactions = user_profile.get("history", [])
        
        # Generate factorized recommendations
        recommendations = []
        
        # Simulate latent factor matching
        for content_id, content in self.content_database.items():
            if content_id not in user_interactions:
                # Calculate latent factor similarity (simplified)
                similarity = self._calculate_latent_similarity(user_profile, content)
                
                if similarity > 0.3:
                    recommendations.append({
                        "content_id": content_id,
                        "reason": "latent factor match",
                        "confidence": similarity,
                        "method": "matrix_factorization"
                    })
        
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        return recommendations[:15]
    
    def _deep_learning_recommendation(self, user_profile: Dict) -> List[Dict]:
        """Deep learning recommendation (simplified)"""
        # In production, use proper neural networks
        # Here we use a simplified approach
        
        recommendations = []
        
        # Get user features
        user_features = self._extract_user_features(user_profile)
        
        # Generate recommendations based on neural features
        for content_id, content in self.content_database.items():
            if content_id not in user_profile.get("history", []):
                # Calculate neural similarity (simplified)
                similarity = self._calculate_neural_similarity(user_features, content)
                
                if similarity > 0.2:
                    recommendations.append({
                        "content_id": content_id,
                        "reason": "neural network prediction",
                        "confidence": similarity,
                        "method": "deep_learning"
                    })
        
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        return recommendations[:15]
    
    def _advanced_hybrid_filtering(self, user_profile: Dict) -> List[Dict]:
        """Advanced hybrid filtering with ensemble methods"""
        # Get recommendations from different methods
        collaborative = self._advanced_collaborative_filtering(user_profile)
        content_based = self._advanced_content_based_filtering(user_profile)
        
        # Ensemble with weighted voting
        ensemble_scores = {}
        
        # Add collaborative scores with weight 0.4
        for rec in collaborative:
            content_id = rec["content_id"]
            ensemble_scores[content_id] = ensemble_scores.get(content_id, 0) + rec["confidence"] * 0.4
        
        # Add content-based scores with weight 0.6
        for rec in content_based:
            content_id = rec["content_id"]
            ensemble_scores[content_id] = ensemble_scores.get(content_id, 0) + rec["confidence"] * 0.6
        
        # Generate final recommendations
        final_recommendations = []
        for content_id, score in ensemble_scores.items():
            final_recommendations.append({
                "content_id": content_id,
                "confidence": min(score, 1.0),
                "method": "hybrid_ensemble",
                "reason": "ensemble of multiple recommendation methods"
            })
        
        final_recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        final_recommendations = self._diversify_recommendations(final_recommendations)
        
        return final_recommendations[:15]
    
    def _find_similar_users_advanced(self, user_profile: Dict) -> List[Dict]:
        """Find similar users with advanced similarity calculation"""
        similar_users = []
        
        for uid, profile in self.user_profiles.items():
            if uid != user_profile["user_id"]:
                # Calculate multi-dimensional similarity
                interest_similarity = self._calculate_jaccard_similarity(
                    set(user_profile.get("interests", [])),
                    set(profile.get("interests", []))
                )
                
                behavior_similarity = self._calculate_behavior_similarity(
                    user_profile.get("history", []),
                    profile.get("history", [])
                )
                
                # Weighted similarity
                similarity = 0.6 * interest_similarity + 0.4 * behavior_similarity
                
                if similarity > 0.2:
                    similar_users.append({
                        **profile,
                        "similarity": similarity
                    })
        
        similar_users.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_users
    
    def _find_similar_content_advanced(self, interest: str, weight: float) -> List[str]:
        """Find similar content with advanced matching"""
        similar_content = []
        
        for content_id, content in self.content_database.items():
            # Multi-dimensional similarity
            text_similarity = self._calculate_text_similarity(interest.lower(), content.get("tags", "").lower())
            category_match = 1.0 if content.get("category") == interest else 0.0
            
            # Weighted similarity
            overall_similarity = 0.7 * text_similarity + 0.3 * category_match
            
            if overall_similarity * weight > 0.3:
                similar_content.append((content_id, overall_similarity))
        
        # Sort by similarity
        similar_content.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in similar_content]
    
    def _diversify_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Diversify recommendations to avoid filter bubble"""
        diversified = []
        seen_categories = set()
        
        for rec in recommendations:
            content = self.content_database.get(rec["content_id"], {})
            category = content.get("category", "unknown")
            
            # Limit recommendations per category
            category_count = sum(1 for r in diversified if self.content_database.get(r["content_id"], {}).get("category") == category)
            
            if category_count < 3 or category not in seen_categories:
                diversified.append(rec)
                seen_categories.add(category)
        
        return diversified
    
    def _calculate_advanced_confidence(self, recommendations: List[Dict], user_profile: Dict) -> List[float]:
        """Calculate advanced confidence scores"""
        confidence_scores = []
        
        for rec in recommendations:
            base_confidence = rec.get("confidence", 0.8)
            
            # Adjust based on user's historical accuracy
            user_accuracy = user_profile.get("recommendation_accuracy", 0.7)
            adjusted_confidence = base_confidence * (0.5 + 0.5 * user_accuracy)
            
            # Apply Bayesian smoothing
            smoothed_confidence = (5 * 0.7 + 10 * adjusted_confidence) / 15
            
            confidence_scores.append(min(smoothed_confidence, 1.0))
        
        return confidence_scores
    
    def _generate_cache_key(self, request: RecommendationRequest) -> str:
        """Generate cache key for request"""
        key_data = f"{request.user_id}_{request.strategy}_{request.preferences}"
        import hashlib
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _update_performance_metrics(self, response_time_ms: float):
        """Update performance metrics"""
        total = self.performance_metrics["total_recommendations"]
        current_avg = self.performance_metrics["avg_response_time_ms"]
        
        # Calculate moving average
        new_avg = (current_avg * total + response_time_ms) / (total + 1)
        self.performance_metrics["avg_response_time_ms"] = new_avg
    
    def _calculate_jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calculate Jaccard similarity"""
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def _calculate_behavior_similarity(self, history1: List, history2: List) -> float:
        """Calculate behavior similarity"""
        set1 = set(history1)
        set2 = set(history2)
        return self._calculate_jaccard_similarity(set1, set2)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simplified)"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        return self._calculate_jaccard_similarity(words1, words2)
    
    def _calculate_latent_similarity(self, user_profile: Dict, content: Dict) -> float:
        """Calculate latent factor similarity (simplified)"""
        # Simplified latent factor calculation
        user_interests = set(user_profile.get("interests", []))
        content_tags = set(content.get("tags", "").split())
        
        return self._calculate_jaccard_similarity(user_interests, content_tags)
    
    def _extract_user_features(self, user_profile: Dict) -> Dict:
        """Extract user features for deep learning (simplified)"""
        return {
            "interests": user_profile.get("interests", []),
            "history_length": len(user_profile.get("history", [])),
            "avg_engagement": user_profile.get("avg_engagement", 0.5)
        }
    
    def _calculate_neural_similarity(self, user_features: Dict, content: Dict) -> float:
        """Calculate neural similarity (simplified)"""
        # Simplified neural similarity calculation
        interest_match = any(interest in content.get("tags", "") for interest in user_features["interests"])
        base_score = 0.5 if interest_match else 0.2
        
        # Adjust by history length (more history = more confident)
        history_factor = min(user_features["history_length"] / 10, 1.0)
        
        return base_score * (0.5 + 0.5 * history_factor)
    
    def get_performance_metrics(self) -> Dict:
        """Get recommendation engine performance metrics"""
        return self.performance_metrics
    
    def clear_cache(self):
        """Clear recommendation cache"""
        self.recommendation_cache.clear()
        return {"status": "cache_cleared"}
    
    def generate_recommendations(self, request: RecommendationRequest) -> Dict:
        """Generate content recommendations"""
        # Get user profile
        user_profile = self.user_profiles.get(request.user_id, self._create_default_profile(request.user_id))
        
        # Generate recommendations based on strategy
        if request.strategy == "collaborative":
            recommendations = self._collaborative_filtering(user_profile)
        elif request.strategy == "content_based":
            recommendations = self._content_based_filtering(user_profile)
        else:  # hybrid
            recommendations = self._hybrid_filtering(user_profile)
        
        # Calculate confidence scores
        confidence_scores = [rec.get("confidence", 0.8) for rec in recommendations]
        
        return {
            "recommendations": recommendations,
            "strategy_used": request.strategy,
            "confidence_scores": confidence_scores
        }
    
    def _create_default_profile(self, user_id: str) -> Dict:
        """Create default user profile"""
        return {
            "user_id": user_id,
            "preferences": {},
            "history": [],
            "interests": []
        }
    
    def _collaborative_filtering(self, user_profile: Dict) -> List[Dict]:
        """Collaborative filtering recommendations"""
        # Simplified collaborative filtering
        recommendations = []
        
        # Find similar users
        similar_users = self._find_similar_users(user_profile)
        
        # Get content liked by similar users
        for similar_user in similar_users[:5]:
            for content in similar_user.get("history", []):
                if content not in user_profile.get("history", []):
                    recommendations.append({
                        "content_id": content,
                        "reason": "similar users liked this",
                        "confidence": 0.75
                    })
        
        return recommendations[:10]
    
    def _content_based_filtering(self, user_profile: Dict) -> List[Dict]:
        """Content-based filtering recommendations"""
        recommendations = []
        
        # Get user interests
        interests = user_profile.get("interests", [])
        
        # Find similar content based on interests
        for interest in interests:
            similar_content = self._find_similar_content(interest)
            
            for content in similar_content:
                if content not in user_profile.get("history", []):
                    recommendations.append({
                        "content_id": content,
                        "reason": f"matches your interest in {interest}",
                        "confidence": 0.85
                    })
        
        return recommendations[:10]
    
    def _hybrid_filtering(self, user_profile: Dict) -> List[Dict]:
        """Hybrid filtering recommendations"""
        # Combine collaborative and content-based
        collaborative = self._collaborative_filtering(user_profile)
        content_based = self._content_based_filtering(user_profile)
        
        # Merge and deduplicate
        seen = set()
        hybrid = []
        
        for rec in collaborative + content_based:
            content_id = rec["content_id"]
            if content_id not in seen:
                seen.add(content_id)
                rec["confidence"] = min(rec.get("confidence", 0.8) + 0.1, 1.0)
                rec["reason"] = f"hybrid: {rec['reason']}"
                hybrid.append(rec)
        
        return hybrid[:10]
    
    def _find_similar_users(self, user_profile: Dict) -> List[Dict]:
        """Find similar users"""
        # Simplified similarity calculation
        similar_users = []
        
        for uid, profile in self.user_profiles.items():
            if uid != user_profile["user_id"]:
                # Calculate similarity based on interests
                user_interests = set(user_profile.get("interests", []))
                profile_interests = set(profile.get("interests", []))
                
                similarity = len(user_interests & profile_interests) / max(len(user_interests | profile_interests), 1)
                
                if similarity > 0.3:
                    similar_users.append({
                        **profile,
                        "similarity": similarity
                    })
        
        # Sort by similarity
        similar_users.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similar_users
    
    def _find_similar_content(self, interest: str) -> List[str]:
        """Find similar content based on interest"""
        # Simplified content similarity
        similar_content = []
        
        for content_id, content in self.content_database.items():
            if interest.lower() in content.get("tags", "").lower():
                similar_content.append(content_id)
        
        return similar_content


# Initialize recommendation engine
recommendation_engine = RecommendationEngine()


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
        from .consumer import AsyncRecommendationEngineConsumer
        consumer = AsyncRecommendationEngineConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Recommendation Engine",
    description="Educational Intelligence Layer - Content recommendation algorithms",
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
        "service": "recommendation-engine",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Recommendation endpoints
@app.post("/recommendation/generate")
async def generate_recommendations(request: RecommendationRequest):
    """Generate content recommendations"""
    result = recommendation_engine.generate_recommendations(request)
    return RecommendationResult(
        request_id=request.request_id,
        user_id=request.user_id,
        recommendations=result["recommendations"],
        strategy_used=result["strategy_used"],
        confidence_scores=result["confidence_scores"]
    )


@app.get("/recommendation/strategies")
async def get_recommendation_strategies():
    """Get available recommendation strategies"""
    return {
        "strategies": ["collaborative", "content_based", "hybrid", "matrix_factorization", "deep_learning"],
        "descriptions": {
            "collaborative": "Based on similar users' preferences",
            "content_based": "Based on content similarity to user interests",
            "hybrid": "Combines collaborative and content-based approaches",
            "matrix_factorization": "Uses matrix factorization for latent feature discovery",
            "deep_learning": "Uses neural networks for recommendation prediction"
        }
    }


# Advanced recommendation endpoints
@app.post("/recommendation/generate-optimized")
async def generate_recommendations_optimized(request: RecommendationRequest):
    """Generate optimized content recommendations with caching"""
    result = recommendation_engine.generate_recommendations_optimized(request)
    return result


# Performance monitoring endpoints
@app.get("/recommendation/performance")
async def get_performance_metrics():
    """Get recommendation engine performance metrics"""
    return recommendation_engine.get_performance_metrics()


@app.post("/recommendation/cache/clear")
async def clear_cache():
    """Clear recommendation cache"""
    return recommendation_engine.clear_cache()


# Content database management endpoints
@app.post("/recommendation/content/add")
async def add_content(content_id: str, content_data: Dict[str, Any]):
    """Add content to database"""
    recommendation_engine.content_database[content_id] = content_data
    return {"status": "added", "content_id": content_id}


@app.get("/recommendation/content/{content_id}")
async def get_content(content_id: str):
    """Get content by ID"""
    content = recommendation_engine.content_database.get(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8019)
