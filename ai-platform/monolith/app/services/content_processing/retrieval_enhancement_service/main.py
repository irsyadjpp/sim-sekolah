"""
Retrieval Enhancement Service - Fase 6.1
Advanced Enhancement - 6 Specialized Retrieval Systems
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50069"))


# Pydantic models
class RetrievalRequest(BaseModel):
    """Base retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    context: Optional[Dict[str, Any]] = None
    top_k: int = Field(default=10, ge=1, le=50)


class CurriculumAwareRetrievalRequest(BaseModel):
    """Curriculum-aware retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    curriculum_phase: str  # A, B, C, D
    grade: str
    subject: str
    top_k: int = Field(default=10, ge=1, le=50)


class PedagogyAwareRetrievalRequest(BaseModel):
    """Pedagogy-aware retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    pedagogy_type: str  # inquiry, differentiated, deep_learning, traditional
    learning_objectives: List[str] = []
    top_k: int = Field(default=10, ge=1, le=50)


class CompetencyAwareRetrievalRequest(BaseModel):
    """Competency-aware retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    target_competency: str
    current_mastery: Dict[str, float] = {}
    top_k: int = Field(default=10, ge=1, le=50)


class AssessmentAwareRetrievalRequest(BaseModel):
    """Assessment-aware retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    assessment_type: str  # formative, summative, diagnostic
    cognitive_level: str  # remember, understand, apply, analyze, evaluate, create
    top_k: int = Field(default=10, ge=1, le=50)


class ContextualRetrievalRequest(BaseModel):
    """Contextual retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    conversation_history: List[Dict] = []
    user_context: Dict[str, Any] = {}
    temporal_context: Optional[str] = None  # morning, afternoon, etc.
    top_k: int = Field(default=10, ge=1, le=50)


class LearningStyleRetrievalRequest(BaseModel):
    """Learning style retrieval request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    learning_style: str  # visual, auditory, kinesthetic, reading
    user_preferences: Dict[str, Any] = {}
    top_k: int = Field(default=10, ge=1, le=50)


class RetrievalResult(BaseModel):
    """Retrieval result"""
    request_id: str
    retrieval_type: str
    results: List[Dict[str, Any]]
    scores: List[float]
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Retrieval Enhancement Engine
class RetrievalEnhancementEngine:
    """Advanced retrieval enhancement with 6 specialized systems"""
    
    def __init__(self):
        # Initialize all specialized retrieval systems
        self.curriculum_aware_reranker = CurriculumAwareReranker()
        self.pedagogy_aware_retrieval = PedagogyAwareRetrieval()
        self.competency_aware_retrieval = CompetencyAwareRetrieval()
        self.assessment_aware_retrieval = AssessmentAwareRetrieval()
        self.contextual_retrieval = ContextualRetrieval()
        self.learning_style_retrieval = LearningStyleRetrieval()
        
        # Performance metrics
        self.performance_metrics = {
            "total_retrievals": 0,
            "avg_retrieval_time_ms": 0,
            "system_usage": {}
        }
    
    def curriculum_aware_rerank(self, request: CurriculumAwareRetrievalRequest) -> Dict:
        """Curriculum-aware reranking"""
        import time
        start_time = time.time()
        
        # Initial retrieval (simulated)
        initial_results = self._simulate_initial_retrieval(request.query, request.top_k)
        
        # Apply curriculum-aware reranking
        reranked_results = self.curriculum_aware_reranker.rerank(
            initial_results,
            request.curriculum_phase,
            request.grade,
            request.subject
        )
        
        # Update performance metrics
        retrieval_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_aware_reranker", retrieval_time)
        
        return {
            "results": reranked_results,
            "scores": [r.get("score", 0.8) for r in reranked_results],
            "metadata": {
                "curriculum_phase": request.curriculum_phase,
                "grade": request.grade,
                "subject": request.subject,
                "reranking_applied": True
            }
        }
    
    def pedagogy_aware_retrieve(self, request: PedagogyAwareRetrievalRequest) -> Dict:
        """Pedagogy-aware retrieval"""
        import time
        start_time = time.time()
        
        # Apply pedagogy-aware retrieval
        results = self.pedagogy_aware_retrieval.retrieve(
            request.query,
            request.pedagogy_type,
            request.learning_objectives,
            request.top_k
        )
        
        # Update performance metrics
        retrieval_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("pedagogy_aware_retrieval", retrieval_time)
        
        return {
            "results": results,
            "scores": [r.get("score", 0.8) for r in results],
            "metadata": {
                "pedagogy_type": request.pedagogy_type,
                "learning_objectives": request.learning_objectives,
                "pedagogy_filters_applied": True
            }
        }
    
    def competency_aware_retrieve(self, request: CompetencyAwareRetrievalRequest) -> Dict:
        """Competency-aware retrieval"""
        import time
        start_time = time.time()
        
        # Apply competency-aware retrieval
        results = self.competency_aware_retrieval.retrieve(
            request.query,
            request.target_competency,
            request.current_mastery,
            request.top_k
        )
        
        # Update performance metrics
        retrieval_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("competency_aware_retrieval", retrieval_time)
        
        return {
            "results": results,
            "scores": [r.get("score", 0.8) for r in results],
            "metadata": {
                "target_competency": request.target_competency,
                "current_mastery": request.current_mastery,
                "competency_filters_applied": True
            }
        }
    
    def assessment_aware_retrieve(self, request: AssessmentAwareRetrievalRequest) -> Dict:
        """Assessment-aware retrieval"""
        import time
        start_time = time.time()
        
        # Apply assessment-aware retrieval
        results = self.assessment_aware_retrieval.retrieve(
            request.query,
            request.assessment_type,
            request.cognitive_level,
            request.top_k
        )
        
        # Update performance metrics
        retrieval_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_aware_retrieval", retrieval_time)
        
        return {
            "results": results,
            "scores": [r.get("score", 0.8) for r in results],
            "metadata": {
                "assessment_type": request.assessment_type,
                "cognitive_level": request.cognitive_level,
                "assessment_filters_applied": True
            }
        }
    
    def contextual_retrieve(self, request: ContextualRetrievalRequest) -> Dict:
        """Contextual retrieval"""
        import time
        start_time = time.time()
        
        # Apply contextual retrieval
        results = self.contextual_retrieval.retrieve(
            request.query,
            request.conversation_history,
            request.user_context,
            request.temporal_context,
            request.top_k
        )
        
        # Update performance metrics
        retrieval_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("contextual_retrieval", retrieval_time)
        
        return {
            "results": results,
            "scores": [r.get("score", 0.8) for r in results],
            "metadata": {
                "conversation_length": len(request.conversation_history),
                "temporal_context": request.temporal_context,
                "context_aware": True
            }
        }
    
    def learning_style_retrieve(self, request: LearningStyleRetrievalRequest) -> Dict:
        """Learning style retrieval"""
        import time
        start_time = time.time()
        
        # Apply learning style retrieval
        results = self.learning_style_retrieval.retrieve(
            request.query,
            request.learning_style,
            request.user_preferences,
            request.top_k
        )
        
        # Update performance metrics
        retrieval_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("learning_style_retrieval", retrieval_time)
        
        return {
            "results": results,
            "scores": [r.get("score", 0.8) for r in results],
            "metadata": {
                "learning_style": request.learning_style,
                "preferences_applied": True,
                "personalized": True
            }
        }
    
    def _simulate_initial_retrieval(self, query: str, top_k: int) -> List[Dict]:
        """Simulate initial retrieval (in production, use actual retrieval service)"""
        results = []
        for i in range(top_k):
            results.append({
                "id": f"doc_{i}",
                "content": f"Sample content for query: {query}",
                "score": 0.8 - (i * 0.05)
            })
        return results
    
    def _update_performance_metrics(self, system_name: str, retrieval_time_ms: float):
        """Update performance metrics"""
        self.performance_metrics["total_retrievals"] += 1
        
        # Update average retrieval time
        total = self.performance_metrics["total_retrievals"]
        current_avg = self.performance_metrics["avg_retrieval_time_ms"]
        new_avg = (current_avg * (total - 1) + retrieval_time_ms) / total
        self.performance_metrics["avg_retrieval_time_ms"] = new_avg
        
        # Update system usage
        if system_name not in self.performance_metrics["system_usage"]:
            self.performance_metrics["system_usage"][system_name] = 0
        self.performance_metrics["system_usage"][system_name] += 1


# Specialized Retrieval Systems
class CurriculumAwareReranker:
    """Curriculum-aware reranking system"""
    
    def __init__(self):
        self.phase_grade_mapping = {
            "A": ["1", "2"],
            "B": ["3", "4"],
            "C": ["5", "6"],
            "D": ["7", "8", "9"]
        }
    
    def rerank(self, results: List[Dict], phase: str, grade: str, subject: str) -> List[Dict]:
        """Rerank results based on curriculum alignment"""
        reranked = []
        
        for result in results:
            base_score = result.get("score", 0.8)
            
            # Apply curriculum alignment boost
            curriculum_score = self._calculate_curriculum_alignment(result, phase, grade, subject)
            
            # Combine scores
            final_score = 0.6 * base_score + 0.4 * curriculum_score
            
            result_copy = result.copy()
            result_copy["score"] = final_score
            result_copy["curriculum_alignment"] = curriculum_score
            reranked.append(result_copy)
        
        # Sort by final score
        reranked.sort(key=lambda x: x["score"], reverse=True)
        return reranked
    
    def _calculate_curriculum_alignment(self, result: Dict, phase: str, grade: str, subject: str) -> float:
        """Calculate curriculum alignment score"""
        # Simplified alignment calculation
        content = result.get("content", "").lower()
        
        score = 0.5  # Base score
        
        # Phase alignment
        if phase.lower() in content:
            score += 0.2
        
        # Grade alignment
        if grade in content:
            score += 0.2
        
        # Subject alignment
        if subject.lower() in content:
            score += 0.1
        
        return min(score, 1.0)


class PedagogyAwareRetrieval:
    """Pedagogy-aware retrieval system"""
    
    def __init__(self):
        self.pedagogy_keywords = {
            "inquiry": ["question", "explore", "investigate", "discover", "inquiry"],
            "differentiated": ["individual", "group", "level", "ability", "differentiated"],
            "deep_learning": ["critical thinking", "analysis", "synthesis", "evaluation"],
            "traditional": ["lecture", "instruction", "direct", "structured"]
        }
    
    def retrieve(self, query: str, pedagogy_type: str, learning_objectives: List[str], top_k: int) -> List[Dict]:
        """Retrieve with pedagogy awareness"""
        # Simulate retrieval with pedagogy filtering
        results = []
        keywords = self.pedagogy_keywords.get(pedagogy_type, [])
        
        for i in range(top_k):
            # Calculate pedagogy match score
            query_lower = query.lower()
            keyword_match = sum(1 for kw in keywords if kw in query_lower)
            pedagogy_score = min(keyword_match / max(len(keywords), 1), 1.0)
            
            # Learning objective alignment
            lo_alignment = self._calculate_lo_alignment(query, learning_objectives)
            
            # Combined score
            final_score = 0.6 * pedagogy_score + 0.4 * lo_alignment
            
            results.append({
                "id": f"pedagogy_doc_{i}",
                "content": f"Pedagogy-aware content for: {query}",
                "score": final_score,
                "pedagogy_match": pedagogy_score,
                "lo_alignment": lo_alignment
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def _calculate_lo_alignment(self, query: str, learning_objectives: List[str]) -> float:
        """Calculate learning objective alignment"""
        if not learning_objectives:
            return 0.5
        
        query_lower = query.lower()
        matches = sum(1 for lo in learning_objectives if lo.lower() in query_lower)
        return matches / len(learning_objectives)


class CompetencyAwareRetrieval:
    """Competency-aware retrieval system"""
    
    def __init__(self):
        self.competency_prerequisites = {}  # Store competency relationships
    
    def retrieve(self, query: str, target_competency: str, current_mastery: Dict[str, float], top_k: int) -> List[Dict]:
        """Retrieve with competency awareness"""
        results = []
        
        # Identify prerequisite needs
        prerequisite_needs = self._identify_prerequisite_needs(target_competency, current_mastery)
        
        for i in range(top_k):
            # Calculate competency relevance
            relevance_score = self._calculate_competency_relevance(query, target_competency)
            
            # Adjust based on mastery
            mastery_adjustment = self._adjust_for_mastery(query, current_mastery)
            
            # Prerequisite awareness
            prereq_boost = 0.3 if query in prerequisite_needs else 0.0
            
            final_score = 0.5 * relevance_score + 0.3 * mastery_adjustment + prereq_boost
            
            results.append({
                "id": f"competency_doc_{i}",
                "content": f"Competency-aware content for: {query}",
                "score": final_score,
                "target_competency": target_competency,
                "mastery_considered": True
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def _identify_prerequisite_needs(self, target_competency: str, current_mastery: Dict[str, float]) -> List[str]:
        """Identify prerequisite competencies that need attention"""
        needs = []
        for competency, mastery in current_mastery.items():
            if mastery < 0.7:
                needs.append(competency)
        return needs
    
    def _calculate_competency_relevance(self, query: str, target_competency: str) -> float:
        """Calculate relevance to target competency"""
        query_lower = query.lower()
        competency_lower = target_competency.lower()
        
        if competency_lower in query_lower:
            return 1.0
        
        # Partial match
        competency_words = competency_lower.split()
        matches = sum(1 for word in competency_words if word in query_lower)
        return matches / max(len(competency_words), 1)
    
    def _adjust_for_mastery(self, query: str, current_mastery: Dict[str, float]) -> float:
        """Adjust score based on current mastery levels"""
        # Simplified mastery adjustment
        if not current_mastery:
            return 0.5
        
        avg_mastery = sum(current_mastery.values()) / len(current_mastery)
        
        # Higher mastery = can handle more complex content
        return avg_mastery


class AssessmentAwareRetrieval:
    """Assessment-aware retrieval system"""
    
    def __init__(self):
        self.bloom_level_keywords = {
            "remember": ["define", "list", "identify", "recall"],
            "understand": ["explain", "describe", "summarize", "interpret"],
            "apply": ["apply", "use", "implement", "execute"],
            "analyze": ["analyze", "examine", "compare", "differentiate"],
            "evaluate": ["evaluate", "assess", "judge", "critique"],
            "create": ["create", "design", "develop", "construct"]
        }
    
    def retrieve(self, query: str, assessment_type: str, cognitive_level: str, top_k: int) -> List[Dict]:
        """Retrieve with assessment awareness"""
        results = []
        
        # Get cognitive level keywords
        cognitive_keywords = self.bloom_level_keywords.get(cognitive_level, [])
        
        for i in range(top_k):
            # Calculate assessment type match
            type_score = self._calculate_assessment_type_match(query, assessment_type)
            
            # Calculate cognitive level match
            cognitive_score = self._calculate_cognitive_match(query, cognitive_keywords)
            
            # Difficulty adjustment based on cognitive level
            difficulty_factor = self._get_difficulty_factor(cognitive_level)
            
            final_score = 0.4 * type_score + 0.4 * cognitive_score + 0.2 * difficulty_factor
            
            results.append({
                "id": f"assessment_doc_{i}",
                "content": f"Assessment-aware content for: {query}",
                "score": final_score,
                "assessment_type": assessment_type,
                "cognitive_level": cognitive_level
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def _calculate_assessment_type_match(self, query: str, assessment_type: str) -> float:
        """Calculate assessment type match"""
        query_lower = query.lower()
        type_lower = assessment_type.lower()
        
        if type_lower in query_lower:
            return 1.0
        
        return 0.5
    
    def _calculate_cognitive_match(self, query: str, cognitive_keywords: List[str]) -> float:
        """Calculate cognitive level match"""
        if not cognitive_keywords:
            return 0.5
        
        query_lower = query.lower()
        matches = sum(1 for kw in cognitive_keywords if kw in query_lower)
        return matches / len(cognitive_keywords)
    
    def _get_difficulty_factor(self, cognitive_level: str) -> float:
        """Get difficulty factor based on cognitive level"""
        difficulty_map = {
            "remember": 0.3,
            "understand": 0.5,
            "apply": 0.7,
            "analyze": 0.8,
            "evaluate": 0.9,
            "create": 1.0
        }
        return difficulty_map.get(cognitive_level, 0.6)


class ContextualRetrieval:
    """Contextual retrieval system"""
    
    def __init__(self):
        self.context_window = 5  # Number of recent turns to consider
    
    def retrieve(self, query: str, conversation_history: List[Dict], user_context: Dict, temporal_context: Optional[str], top_k: int) -> List[Dict]:
        """Retrieve with full context awareness"""
        results = []
        
        # Extract context features
        recent_context = conversation_history[-self.context_window:] if conversation_history else []
        context_summary = self._summarize_context(recent_context)
        
        for i in range(top_k):
            # Calculate context relevance
            context_relevance = self._calculate_context_relevance(query, context_summary)
            
            # User personalization
            personalization_score = self._calculate_personalization(query, user_context)
            
            # Temporal adjustment
            temporal_score = self._calculate_temporal_score(query, temporal_context)
            
            # Conversation coherence
            coherence_score = self._calculate_coherence(query, recent_context)
            
            final_score = 0.3 * context_relevance + 0.3 * personalization_score + 0.2 * temporal_score + 0.2 * coherence_score
            
            results.append({
                "id": f"contextual_doc_{i}",
                "content": f"Contextual content for: {query}",
                "score": final_score,
                "context_aware": True,
                "conversation_coherent": coherence_score > 0.5
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def _summarize_context(self, conversation_history: List[Dict]) -> str:
        """Summarize conversation context"""
        if not conversation_history:
            return ""
        
        recent_queries = [turn.get("query", "") for turn in conversation_history]
        return " ".join(recent_queries)
    
    def _calculate_context_relevance(self, query: str, context_summary: str) -> float:
        """Calculate relevance to conversation context"""
        if not context_summary:
            return 0.5
        
        query_lower = query.lower()
        context_lower = context_summary.lower()
        
        # Check for topic continuity
        query_words = set(query_lower.split())
        context_words = set(context_lower.split())
        
        overlap = len(query_words & context_words)
        total = len(query_words | context_words)
        
        return overlap / total if total > 0 else 0.5
    
    def _calculate_personalization(self, query: str, user_context: Dict) -> float:
        """Calculate personalization score based on user context"""
        if not user_context:
            return 0.5
        
        # Simplified personalization
        query_lower = query.lower()
        personalization = 0.5
        
        for key, value in user_context.items():
            if str(value).lower() in query_lower:
                personalization += 0.1
        
        return min(personalization, 1.0)
    
    def _calculate_temporal_score(self, query: str, temporal_context: Optional[str]) -> float:
        """Calculate temporal context score"""
        if not temporal_context:
            return 0.5
        
        # Simplified temporal adjustment
        temporal_boosts = {
            "morning": 0.1,
            "afternoon": 0.05,
            "evening": 0.0
        }
        
        return 0.5 + temporal_boosts.get(temporal_context.lower(), 0.0)
    
    def _calculate_coherence(self, query: str, conversation_history: List[Dict]) -> float:
        """Calculate conversation coherence"""
        if not conversation_history:
            return 0.5
        
        # Simplified coherence calculation
        recent_query = conversation_history[-1].get("query", "") if conversation_history else ""
        
        query_lower = query.lower()
        recent_lower = recent_query.lower()
        
        # Check for follow-up questions
        follow_up_indicators = ["what about", "also", "another", "more", "additionally"]
        is_follow_up = any(indicator in query_lower for indicator in follow_up_indicators)
        
        if is_follow_up:
            return 0.9
        
        # Topic similarity
        query_words = set(query_lower.split())
        recent_words = set(recent_lower.split())
        
        overlap = len(query_words & recent_words)
        return 0.5 + (0.4 if overlap > 0 else 0.0)


class LearningStyleRetrieval:
    """Learning style retrieval system"""
    
    def __init__(self):
        self.style_content_mapping = {
            "visual": ["diagrams", "charts", "videos", "images", "graphs"],
            "auditory": ["audio", "podcasts", "lectures", "discussions", "explanations"],
            "kinesthetic": ["hands-on", "activities", "experiments", "simulations", "projects"],
            "reading": ["text", "articles", "books", "documents", "written"]
        }
    
    def retrieve(self, query: str, learning_style: str, user_preferences: Dict, top_k: int) -> List[Dict]:
        """Retrieve with learning style awareness"""
        results = []
        
        # Get content types for learning style
        content_types = self.style_content_mapping.get(learning_style, [])
        
        for i in range(top_k):
            # Calculate style match
            style_score = self._calculate_style_match(query, learning_style, content_types)
            
            # Preference alignment
            preference_score = self._calculate_preference_alignment(query, user_preferences)
            
            # Personalization boost
            personalization = 0.2 if user_preferences else 0.0
            
            final_score = 0.5 * style_score + 0.3 * preference_score + personalization
            
            results.append({
                "id": f"style_doc_{i}",
                "content": f"Learning style adapted content for: {query}",
                "score": final_score,
                "learning_style": learning_style,
                "content_types": content_types[:3]
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def _calculate_style_match(self, query: str, learning_style: str, content_types: List[str]) -> float:
        """Calculate learning style match"""
        query_lower = query.lower()
        
        # Check for content type mentions
        type_matches = sum(1 for content_type in content_types if content_type in query_lower)
        
        if type_matches > 0:
            return 1.0
        
        # Check for learning style keywords
        style_keywords = {
            "visual": ["see", "look", "watch", "diagram", "chart"],
            "auditory": ["hear", "listen", "sound", "audio", "speak"],
            "kinesthetic": ["do", "make", "build", "hands-on", "activity"],
            "reading": ["read", "text", "write", "document", "article"]
        }
        
        keywords = style_keywords.get(learning_style, [])
        keyword_matches = sum(1 for kw in keywords if kw in query_lower)
        
        return 0.5 + (0.3 if keyword_matches > 0 else 0.0)
    
    def _calculate_preference_alignment(self, query: str, user_preferences: Dict) -> float:
        """Calculate alignment with user preferences"""
        if not user_preferences:
            return 0.5
        
        query_lower = query.lower()
        alignment_score = 0.5
        
        for pref_key, pref_value in user_preferences.items():
            if str(pref_value).lower() in query_lower:
                alignment_score += 0.1
        
        return min(alignment_score, 1.0)


# Initialize retrieval enhancement engine
retrieval_enhancement_engine = RetrievalEnhancementEngine()


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
        from .consumer import AsyncRetrievalEnhancementConsumer
        consumer = AsyncRetrievalEnhancementConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Retrieval Enhancement Service",
    description="Advanced Enhancement - 6 Specialized Retrieval Systems",
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
        "service": "retrieval-enhancement-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Retrieval Enhancement endpoints
@app.post("/retrieval/curriculum-aware")
async def curriculum_aware_retrieval(request: CurriculumAwareRetrievalRequest):
    """Curriculum-aware reranking"""
    result = retrieval_enhancement_engine.curriculum_aware_rerank(request)
    return RetrievalResult(
        request_id=request.request_id,
        retrieval_type="curriculum_aware_reranker",
        results=result["results"],
        scores=result["scores"],
        metadata=result["metadata"]
    )


@app.post("/retrieval/pedagogy-aware")
async def pedagogy_aware_retrieval(request: PedagogyAwareRetrievalRequest):
    """Pedagogy-aware retrieval"""
    result = retrieval_enhancement_engine.pedagogy_aware_retrieve(request)
    return RetrievalResult(
        request_id=request.request_id,
        retrieval_type="pedagogy_aware_retrieval",
        results=result["results"],
        scores=result["scores"],
        metadata=result["metadata"]
    )


@app.post("/retrieval/competency-aware")
async def competency_aware_retrieval(request: CompetencyAwareRetrievalRequest):
    """Competency-aware retrieval"""
    result = retrieval_enhancement_engine.competency_aware_retrieve(request)
    return RetrievalResult(
        request_id=request.request_id,
        retrieval_type="competency_aware_retrieval",
        results=result["results"],
        scores=result["scores"],
        metadata=result["metadata"]
    )


@app.post("/retrieval/assessment-aware")
async def assessment_aware_retrieval(request: AssessmentAwareRetrievalRequest):
    """Assessment-aware retrieval"""
    result = retrieval_enhancement_engine.assessment_aware_retrieve(request)
    return RetrievalResult(
        request_id=request.request_id,
        retrieval_type="assessment_aware_retrieval",
        results=result["results"],
        scores=result["scores"],
        metadata=result["metadata"]
    )


@app.post("/retrieval/contextual")
async def contextual_retrieval(request: ContextualRetrievalRequest):
    """Contextual retrieval"""
    result = retrieval_enhancement_engine.contextual_retrieve(request)
    return RetrievalResult(
        request_id=request.request_id,
        retrieval_type="contextual_retrieval",
        results=result["results"],
        scores=result["scores"],
        metadata=result["metadata"]
    )


@app.post("/retrieval/learning-style")
async def learning_style_retrieval(request: LearningStyleRetrievalRequest):
    """Learning style retrieval"""
    result = retrieval_enhancement_engine.learning_style_retrieve(request)
    return RetrievalResult(
        request_id=request.request_id,
        retrieval_type="learning_style_retrieval",
        results=result["results"],
        scores=result["scores"],
        metadata=result["metadata"]
    )


# Performance monitoring
@app.get("/retrieval/performance")
async def get_performance_metrics():
    """Get retrieval performance metrics"""
    return retrieval_enhancement_engine.performance_metrics


@app.get("/retrieval/systems")
async def get_available_systems():
    """Get available retrieval systems"""
    return {
        "systems": [
            {
                "name": "curriculum_aware_reranker",
                "description": "Reranks results based on curriculum alignment",
                "parameters": ["curriculum_phase", "grade", "subject"]
            },
            {
                "name": "pedagogy_aware_retrieval",
                "description": "Retrieves content based on pedagogy type",
                "parameters": ["pedagogy_type", "learning_objectives"]
            },
            {
                "name": "competency_aware_retrieval",
                "description": "Retrieves content based on competency needs",
                "parameters": ["target_competency", "current_mastery"]
            },
            {
                "name": "assessment_aware_retrieval",
                "description": "Retrieves content for specific assessment types",
                "parameters": ["assessment_type", "cognitive_level"]
            },
            {
                "name": "contextual_retrieval",
                "description": "Retrieves content with full context awareness",
                "parameters": ["conversation_history", "user_context", "temporal_context"]
            },
            {
                "name": "learning_style_retrieval",
                "description": "Retrieves content adapted to learning style",
                "parameters": ["learning_style", "user_preferences"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)