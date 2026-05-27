"""
Pedagogy Engine - Fase 5.2
Educational Intelligence Layer - Pedagogy analysis and teaching method classification
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50063"))


# Pydantic models
class PedagogyAnalysisRequest(BaseModel):
    """Pedagogy analysis request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    content_type: str = "text"  # text, lesson_plan, activity
    context: Optional[Dict[str, Any]] = None


class PedagogyAnalysisResult(BaseModel):
    """Pedagogy analysis result"""
    request_id: str
    pedagogy_type: str  # inquiry, differentiated, deep_learning, traditional
    confidence: float
    characteristics: List[str]
    teaching_methods: List[str]
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PedagogyDetectionRequest(BaseModel):
    """Pedagogy detection request"""
    content: str
    context: Optional[Dict[str, Any]] = None


# Pedagogy engine
class PedagogyEngine:
    """Pedagogy analysis and detection engine"""
    
    def __init__(self):
        self.inquiry_keywords = [
            "question", "explore", "investigate", "discover", "inquiry",
            "problem-based", "student-centered", "guided discovery"
        ]
        self.differentiated_keywords = [
            "individual", "group", "level", "ability", "differentiated",
            "adapted", "personalized", "tiered", "flexible"
        ]
        self.deep_learning_keywords = [
            "critical thinking", "analysis", "synthesis", "evaluation",
            "higher-order", "complex", "application", "transfer"
        ]
        self.knowledge_base = {}  # In-memory knowledge base for pedagogy patterns
    
    def analyze_pedagogical_context(self, content: str, context: Optional[Dict] = None) -> Dict:
        """Analyze pedagogical context with deeper analysis"""
        basic_detection = self.detect_pedagogy(content, context)
        
        # Add context analysis
        context_analysis = {
            "grade_level_appropriateness": self._analyze_grade_level(content, context),
            "complexity_level": self._analyze_complexity(content),
            "engagement_potential": self._analyze_engagement_potential(content),
            "differentiation_opportunities": self._identify_differentiation_opportunities(content)
        }
        
        return {
            **basic_detection,
            "context_analysis": context_analysis
        }
    
    def add_to_knowledge_base(self, pattern_type: str, data: Dict[str, Any]) -> str:
        """Add pedagogy pattern to knowledge base"""
        entry_id = f"pedagogy_{pattern_type}_{len(self.knowledge_base)}"
        self.knowledge_base[entry_id] = {
            "pattern_type": pattern_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        return entry_id
    
    def query_knowledge_base(self, pattern_type: str = None) -> List[Dict]:
        """Query pedagogy knowledge base"""
        results = []
        
        for entry_id, entry in self.knowledge_base.items():
            if pattern_type is None or entry["pattern_type"] == pattern_type:
                results.append(entry)
        
        return results
    
    def _analyze_grade_level(self, content: str, context: Optional[Dict] = None) -> str:
        """Analyze grade level appropriateness"""
        grade = context.get("grade", "") if context else ""
        
        # Simple heuristic based on vocabulary complexity
        complex_words = ["analyze", "evaluate", "synthesize", "metacognitive"]
        complex_count = sum(1 for word in complex_words if word in content.lower())
        
        if complex_count >= 3:
            return "upper_grades"
        elif complex_count >= 1:
            return "middle_grades"
        else:
            return "lower_grades"
    
    def _analyze_complexity(self, content: str) -> str:
        """Analyze content complexity"""
        word_count = len(content.split())
        sentence_count = max(1, content.count("."))
        avg_words_per_sentence = word_count / sentence_count
        
        if avg_words_per_sentence > 20:
            return "high"
        elif avg_words_per_sentence > 15:
            return "medium"
        else:
            return "low"
    
    def _analyze_engagement_potential(self, content: str) -> str:
        """Analyze student engagement potential"""
        engagement_indicators = [
            "interactive", "hands-on", "collaborative", "discussion",
            "exploration", "experiment", "project", "game"
        ]
        
        engagement_count = sum(1 for indicator in engagement_indicators if indicator in content.lower())
        
        if engagement_count >= 3:
            return "high"
        elif engagement_count >= 1:
            return "medium"
        else:
            return "low"
    
    def _identify_differentiation_opportunities(self, content: str) -> List[str]:
        """Identify opportunities for differentiation"""
        opportunities = []
        
        if "visual" in content.lower() or "diagram" in content.lower():
            opportunities.append("visual_supports")
        
        if "group" in content.lower() or "collaborative" in content.lower():
            opportunities.append("flexible_grouping")
        
        if "choice" in content.lower() or "option" in content.lower():
            opportunities.append("student_choice")
        
        if "hands-on" in content.lower() or "activity" in content.lower():
            opportunities.append("kinesthetic_activities")
        
        return opportunities if opportunities else ["standard_instruction"]
    
    def detect_pedagogy(self, content: str, context: Optional[Dict] = None) -> Dict:
        """Detect pedagogy type from content"""
        content_lower = content.lower()
        
        scores = {
            "inquiry": self._score_keywords(content_lower, self.inquiry_keywords),
            "differentiated": self._score_keywords(content_lower, self.differentiated_keywords),
            "deep_learning": self._score_keywords(content_lower, self.deep_learning_keywords)
        }
        
        # Determine pedagogy type
        max_score = max(scores.values())
        if max_score == 0:
            pedagogy_type = "traditional"
            confidence = 0.5
        else:
            pedagogy_type = max(scores, key=scores.get)
            confidence = min(max_score / 3.0, 1.0)
        
        # Get characteristics
        characteristics = self._get_characteristics(pedagogy_type)
        
        # Get teaching methods
        teaching_methods = self._get_teaching_methods(pedagogy_type)
        
        # Get recommendations
        recommendations = self._get_recommendations(pedagogy_type)
        
        return {
            "pedagogy_type": pedagogy_type,
            "confidence": confidence,
            "characteristics": characteristics,
            "teaching_methods": teaching_methods,
            "recommendations": recommendations,
            "scores": scores
        }
    
    def _score_keywords(self, content: str, keywords: List[str]) -> float:
        """Score content based on keyword matches"""
        score = 0
        for keyword in keywords:
            if keyword in content:
                score += 1
        return score
    
    def _get_characteristics(self, pedagogy_type: str) -> List[str]:
        """Get characteristics for pedagogy type"""
        characteristics_map = {
            "inquiry": [
                "Student-driven exploration",
                "Open-ended questions",
                "Problem-based learning",
                "Discovery learning"
            ],
            "differentiated": [
                "Tailored to individual needs",
                "Multiple learning pathways",
                "Flexible grouping",
                "Varied assessment methods"
            ],
            "deep_learning": [
                "Critical thinking focus",
                "Higher-order thinking skills",
                "Complex problem solving",
                "Application and transfer"
            ],
            "traditional": [
                "Teacher-centered",
                "Direct instruction",
                "Structured delivery",
                "Standardized approach"
            ]
        }
        return characteristics_map.get(pedagogy_type, [])
    
    def _get_teaching_methods(self, pedagogy_type: str) -> List[str]:
        """Get teaching methods for pedagogy type"""
        methods_map = {
            "inquiry": [
                "Guided inquiry",
                "Open inquiry",
                "Problem-based learning",
                "Project-based learning"
            ],
            "differentiated": [
                "Tiered activities",
                "Learning stations",
                "Flexible grouping",
                "Choice boards"
            ],
            "deep_learning": [
                "Socratic method",
                "Case studies",
                "Concept mapping",
                "Debates and discussions"
            ],
            "traditional": [
                "Lecture",
                "Direct instruction",
                "Drill and practice",
                "Demonstration"
            ]
        }
        return methods_map.get(pedagogy_type, [])
    
    def _get_recommendations(self, pedagogy_type: str) -> List[str]:
        """Get recommendations for pedagogy type"""
        recommendations_map = {
            "inquiry": [
                "Provide scaffolding for complex inquiries",
                "Balance guidance with independence",
                "Use formative assessment to guide learning"
            ],
            "differentiated": [
                "Use pre-assessment to inform grouping",
                "Provide multiple means of representation",
                "Offer choice in assessment methods"
            ],
            "deep_learning": [
                "Design tasks requiring critical analysis",
                "Encourage metacognitive reflection",
                "Connect to real-world applications"
            ],
            "traditional": [
                "Consider incorporating more student engagement",
                "Add interactive elements",
                "Provide opportunities for application"
            ]
        }
        return recommendations_map.get(pedagogy_type, [])


# Initialize pedagogy engine
pedagogy_engine = PedagogyEngine()


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
        from .consumer import AsyncPedagogyEngineConsumer
        consumer = AsyncPedagogyEngineConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Pedagogy Engine",
    description="Educational Intelligence Layer - Pedagogy analysis and teaching method classification",
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
        "service": "pedagogy-engine",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Pedagogy endpoints
@app.post("/pedagogy/analyze")
async def analyze_pedagogy(request: PedagogyAnalysisRequest):
    """Analyze pedagogy from content"""
    result = pedagogy_engine.detect_pedagogy(request.content, request.context)
    return PedagogyAnalysisResult(
        request_id=request.request_id,
        pedagogy_type=result["pedagogy_type"],
        confidence=result["confidence"],
        characteristics=result["characteristics"],
        teaching_methods=result["teaching_methods"],
        recommendations=result["recommendations"]
    )


@app.post("/pedagogy/detect")
async def detect_pedagogy_type(request: PedagogyDetectionRequest):
    """Detect pedagogy type"""
    result = pedagogy_engine.detect_pedagogy(request.content, request.context)
    return result


@app.get("/pedagogy/types")
async def get_pedagogy_types():
    """Get available pedagogy types"""
    return {
        "types": ["inquiry", "differentiated", "deep_learning", "traditional"],
        "descriptions": {
            "inquiry": "Student-centered exploration and discovery",
            "differentiated": "Tailored to individual learning needs",
            "deep_learning": "Focus on higher-order thinking skills",
            "traditional": "Teacher-centered direct instruction"
        }
    }


@app.post("/pedagogy/analyze-context")
async def analyze_pedagogical_context(request: PedagogyAnalysisRequest):
    """Analyze pedagogical context with deeper analysis"""
    result = pedagogy_engine.analyze_pedagogical_context(request.content, request.context)
    return result


# Knowledge base endpoints
@app.post("/pedagogy/knowledge-base/add")
async def add_to_knowledge_base(pattern_type: str, data: Dict[str, Any]):
    """Add pedagogy pattern to knowledge base"""
    entry_id = pedagogy_engine.add_to_knowledge_base(pattern_type, data)
    return {
        "entry_id": entry_id,
        "status": "added"
    }


@app.get("/pedagogy/knowledge-base/query")
async def query_knowledge_base(pattern_type: Optional[str] = None):
    """Query pedagogy knowledge base"""
    results = pedagogy_engine.query_knowledge_base(pattern_type)
    return {
        "results": results,
        "count": len(results)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8014)
