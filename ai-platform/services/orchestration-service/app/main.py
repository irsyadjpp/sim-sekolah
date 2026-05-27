"""
Orchestration Service - Fase 4.3
Governance & Observability - Workflow orchestration and intelligent routing
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50061"))


# Pydantic models
class WorkflowRequest(BaseModel):
    """Workflow orchestration request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    query: str
    context: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    """Workflow orchestration response"""
    request_id: str
    intent: str
    retrieval_strategy: str
    generation_strategy: str
    steps: list
    result: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IntentDetectionRequest(BaseModel):
    """Intent detection request"""
    query: str
    context: Optional[Dict[str, Any]] = None


class IntentDetectionResponse(BaseModel):
    """Intent detection response"""
    intent: str
    confidence: float
    categories: list


# Workflow engine
class WorkflowEngine:
    """Workflow orchestration engine"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.retrieval_router = RetrievalStrategyRouter()
        self.generation_router = GenerationStrategyRouter()
        self.policy_engine = PolicyEngine()
    
    def detect_intent(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Detect user intent"""
        return self.intent_classifier.classify(query, context)
    
    def route_retrieval(self, intent: str, context: Optional[Dict] = None) -> str:
        """Route to appropriate retrieval strategy"""
        return self.retrieval_router.route(intent, context)
    
    def route_generation(self, intent: str, context: Optional[Dict] = None) -> str:
        """Route to appropriate generation strategy"""
        return self.generation_router.route(intent, context)
    
    def execute_workflow(self, request: WorkflowRequest) -> WorkflowResponse:
        """Execute workflow"""
        # Detect intent
        intent_result = self.detect_intent(request.query, request.context)
        
        # Route strategies
        retrieval_strategy = self.route_retrieval(intent_result["intent"], request.context)
        generation_strategy = self.route_generation(intent_result["intent"], request.context)
        
        # Check policies
        policy_result = self.policy_engine.check(request)
        
        # Build workflow steps
        steps = [
            {"step": "intent_detection", "result": intent_result},
            {"step": "retrieval_routing", "strategy": retrieval_strategy},
            {"step": "generation_routing", "strategy": generation_strategy},
            {"step": "policy_check", "result": policy_result}
        ]
        
        return WorkflowResponse(
            request_id=request.request_id,
            intent=intent_result["intent"],
            retrieval_strategy=retrieval_strategy,
            generation_strategy=generation_strategy,
            steps=steps
        )


class IntentClassifier:
    """Intent classification engine"""
    
    def classify(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Classify user intent"""
        query_lower = query.lower()
        
        # Simple rule-based classification
        if any(word in query_lower for word in ["what", "explain", "describe", "define"]):
            return {"intent": "informational", "confidence": 0.8, "categories": ["knowledge"]}
        
        elif any(word in query_lower for word in ["how", "create", "make", "build"]):
            return {"intent": "procedural", "confidence": 0.8, "categories": ["instruction"]}
        
        elif any(word in query_lower for word in ["why", "reason", "cause"]):
            return {"intent": "analytical", "confidence": 0.8, "categories": ["reasoning"]}
        
        elif any(word in query_lower for word in ["compare", "difference", "vs"]):
            return {"intent": "comparative", "confidence": 0.8, "categories": ["comparison"]}
        
        else:
            return {"intent": "general", "confidence": 0.6, "categories": ["general"]}


class RetrievalStrategyRouter:
    """Retrieval strategy router"""
    
    def route(self, intent: str, context: Optional[Dict] = None) -> str:
        """Route to retrieval strategy"""
        strategy_map = {
            "informational": "semantic_search",
            "procedural": "hybrid_search",
            "analytical": "curriculum_aware",
            "comparative": "pedagogy_aware",
            "general": "semantic_search"
        }
        return strategy_map.get(intent, "semantic_search")


class GenerationStrategyRouter:
    """Generation strategy router"""
    
    def route(self, intent: str, context: Optional[Dict] = None) -> str:
        """Route to generation strategy"""
        strategy_map = {
            "informational": "standard_generation",
            "procedural": "step_by_step",
            "analytical": "reasoning_chain",
            "comparative": "structured_comparison",
            "general": "standard_generation"
        }
        return strategy_map.get(intent, "standard_generation")


class PolicyEngine:
    """Policy engine for workflow governance"""
    
    def check(self, request: WorkflowRequest) -> Dict:
        """Check policies for request"""
        # Simple policy checks
        policies_passed = True
        violations = []
        
        # Check query length
        if len(request.query) < 5:
            policies_passed = False
            violations.append("Query too short")
        
        # Check for sensitive content
        sensitive_words = ["password", "secret", "confidential"]
        if any(word in request.query.lower() for word in sensitive_words):
            policies_passed = False
            violations.append("Sensitive content detected")
        
        return {
            "passed": policies_passed,
            "violations": violations
        }


# Initialize workflow engine
workflow_engine = WorkflowEngine()


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
        from .consumer import AsyncOrchestrationServiceConsumer
        consumer = AsyncOrchestrationServiceConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Orchestration Service",
    description="Governance & Observability - Workflow orchestration and intelligent routing",
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
        "service": "orchestration-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Orchestration endpoints
@app.post("/orchestrate")
async def orchestrate_workflow(request: WorkflowRequest):
    """Execute workflow orchestration"""
    response = workflow_engine.execute_workflow(request)
    return response


@app.post("/intent")
async def detect_intent(request: IntentDetectionRequest):
    """Detect user intent"""
    result = workflow_engine.detect_intent(request.query, request.context)
    return IntentDetectionResponse(**result)


@app.get("/orchestration/{request_id}")
async def get_orchestration_result(request_id: str):
    """Get orchestration result by request ID"""
    # In production, this would query a database
    return {"request_id": request_id, "status": "not_implemented"}


@app.get("/strategies")
async def get_available_strategies():
    """Get available strategies"""
    return {
        "retrieval_strategies": [
            "semantic_search",
            "hybrid_search",
            "curriculum_aware",
            "pedagogy_aware",
            "competency_aware"
        ],
        "generation_strategies": [
            "standard_generation",
            "step_by_step",
            "reasoning_chain",
            "structured_comparison",
            "template_based"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
