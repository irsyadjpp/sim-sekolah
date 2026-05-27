"""
Educational Ontology Service - Fase 6.3
Advanced Enhancement - 6 Educational Ontologies
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50071"))


# Pydantic models
class OntologyRequest(BaseModel):
    """Base ontology request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str  # query, add, update, delete
    data: Optional[Dict[str, Any]] = None


class OntologyQueryRequest(BaseModel):
    """Ontology query request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ontology_type: str  # curriculum, pedagogy, competency, assessment, learning_objective, concept
    query: str
    filters: Optional[Dict[str, Any]] = None


class OntologyResult(BaseModel):
    """Ontology result"""
    request_id: str
    ontology_type: str
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Educational Ontology Engine
class EducationalOntologyEngine:
    """Advanced educational ontology management with 6 ontologies"""
    
    def __init__(self):
        # Initialize all ontologies
        self.curriculum_ontology = CurriculumOntology()
        self.pedagogy_ontology = PedagogyOntology()
        self.competency_ontology = CompetencyOntology()
        self.assessment_ontology = AssessmentOntology()
        self.learning_objective_ontology = LearningObjectiveOntology()
        self.concept_hierarchy = ConceptHierarchy()
        
        # Ontology management system
        self.ontology_store = {}  # Store ontology data
        self.ontology_metadata = {}  # Store ontology metadata
        
        # Performance metrics
        self.performance_metrics = {
            "total_queries": 0,
            "avg_query_time_ms": 0,
            "ontology_usage": {}
        }
    
    def query_curriculum_ontology(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query curriculum ontology"""
        import time
        start_time = time.time()
        
        result = self.curriculum_ontology.query(query, filters)
        
        query_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("curriculum_ontology", query_time)
        
        return {
            "result": result,
            "metadata": {
                "ontology_type": "curriculum",
                "query_execution_time_ms": query_time,
                "results_count": len(result.get("nodes", []))
            }
        }
    
    def query_pedagogy_ontology(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query pedagogy ontology"""
        import time
        start_time = time.time()
        
        result = self.pedagogy_ontology.query(query, filters)
        
        query_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("pedagogy_ontology", query_time)
        
        return {
            "result": result,
            "metadata": {
                "ontology_type": "pedagogy",
                "query_execution_time_ms": query_time,
                "results_count": len(result.get("nodes", []))
            }
        }
    
    def query_competency_ontology(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query competency ontology"""
        import time
        start_time = time.time()
        
        result = self.competency_ontology.query(query, filters)
        
        query_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("competency_ontology", query_time)
        
        return {
            "result": result,
            "metadata": {
                "ontology_type": "competency",
                "query_execution_time_ms": query_time,
                "results_count": len(result.get("nodes", []))
            }
        }
    
    def query_assessment_ontology(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query assessment ontology"""
        import time
        start_time = time.time()
        
        result = self.assessment_ontology.query(query, filters)
        
        query_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("assessment_ontology", query_time)
        
        return {
            "result": result,
            "metadata": {
                "ontology_type": "assessment",
                "query_execution_time_ms": query_time,
                "results_count": len(result.get("nodes", []))
            }
        }
    
    def query_learning_objective_ontology(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query learning objective ontology"""
        import time
        start_time = time.time()
        
        result = self.learning_objective_ontology.query(query, filters)
        
        query_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("learning_objective_ontology", query_time)
        
        return {
            "result": result,
            "metadata": {
                "ontology_type": "learning_objective",
                "query_execution_time_ms": query_time,
                "results_count": len(result.get("nodes", []))
            }
        }
    
    def query_concept_hierarchy(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query concept hierarchy"""
        import time
        start_time = time.time()
        
        result = self.concept_hierarchy.query(query, filters)
        
        query_time = (time.time() - start_time) * 1000
        self._update_performance_metrics("concept_hierarchy", query_time)
        
        return {
            "result": result,
            "metadata": {
                "ontology_type": "concept",
                "query_execution_time_ms": query_time,
                "results_count": len(result.get("nodes", []))
            }
        }
    
    def _update_performance_metrics(self, ontology_name: str, query_time_ms: float):
        """Update performance metrics"""
        self.performance_metrics["total_queries"] += 1
        
        total = self.performance_metrics["total_queries"]
        current_avg = self.performance_metrics["avg_query_time_ms"]
        new_avg = (current_avg * (total - 1) + query_time_ms) / total
        self.performance_metrics["avg_query_time_ms"] = new_avg
        
        if ontology_name not in self.performance_metrics["ontology_usage"]:
            self.performance_metrics["ontology_usage"][ontology_name] = 0
        self.performance_metrics["ontology_usage"][ontology_name] += 1


# Educational Ontology Classes
class CurriculumOntology:
    """Curriculum ontology management"""
    
    def __init__(self):
        self.nodes = {
            "phase_a": {"type": "phase", "grades": ["1", "2"], "description": "Grades 1-2"},
            "phase_b": {"type": "phase", "grades": ["3", "4"], "description": "Grades 3-4"},
            "phase_c": {"type": "phase", "grades": ["5", "6"], "description": "Grades 5-6"},
            "phase_d": {"type": "phase", "grades": ["7", "8", "9"], "description": "Grades 7-9"},
            "cp": {"type": "curriculum_document", "description": "Capaian Pembelajaran"},
            "atp": {"type": "curriculum_document", "description": "Tujuan Pembelajaran"}
        }
        self.edges = [
            {"source": "phase_a", "target": "phase_b", "relation": "follows"},
            {"source": "phase_b", "target": "phase_c", "relation": "follows"},
            {"source": "phase_c", "target": "phase_d", "relation": "follows"},
            {"source": "cp", "target": "atp", "relation": "informs"}
        ]
    
    def query(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query curriculum ontology"""
        query_lower = query.lower()
        matched_nodes = {}
        
        for node_id, node_data in self.nodes.items():
            # Search in node properties
            node_str = str(node_data).lower()
            if query_lower in node_str or query_lower in node_id.lower():
                matched_nodes[node_id] = node_data
        
        # Apply filters
        if filters:
            matched_nodes = {k: v for k, v in matched_nodes.items() if all(str(v.get(k2)) == str(v2) for k2, v2 in filters.items() if k2 in v)}
        
        return {
            "nodes": matched_nodes,
            "edges": self._filter_edges(matched_nodes.keys()),
            "ontology": "curriculum"
        }
    
    def _filter_edges(self, node_ids: List[str]) -> List[Dict]:
        """Filter edges based on node IDs"""
        return [edge for edge in self.edges if edge["source"] in node_ids and edge["target"] in node_ids]


class PedagogyOntology:
    """Pedagogy ontology management"""
    
    def __init__(self):
        self.nodes = {
            "inquiry": {"type": "pedagogy", "description": "Student-centered inquiry learning"},
            "differentiated": {"type": "pedagogy", "description": "Tailored to individual needs"},
            "collaborative": {"type": "pedagogy", "description": "Group-based learning"},
            "direct": {"type": "pedagogy", "description": "Teacher-centered instruction"},
            "experiential": {"type": "pedagogy", "description": "Hands-on learning experiences"}
        }
        self.edges = [
            {"source": "inquiry", "target": "collaborative", "relation": "complements"},
            {"source": "differentiated", "target": "inquiry", "relation": "supports"},
            {"source": "experiential", "target": "inquiry", "relation": "enhances"}
        ]
    
    def query(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query pedagogy ontology"""
        query_lower = query.lower()
        matched_nodes = {}
        
        for node_id, node_data in self.nodes.items():
            node_str = str(node_data).lower()
            if query_lower in node_str or query_lower in node_id.lower():
                matched_nodes[node_id] = node_data
        
        if filters:
            matched_nodes = {k: v for k, v in matched_nodes.items() if all(str(v.get(k2)) == str(v2) for k2, v2 in filters.items() if k2 in v)}
        
        return {
            "nodes": matched_nodes,
            "edges": [edge for edge in self.edges if edge["source"] in matched_nodes.keys() and edge["target"] in matched_nodes.keys()],
            "ontology": "pedagogy"
        }


class CompetencyOntology:
    """Competency ontology management"""
    
    def __init__(self):
        self.nodes = {
            "core_competencies": {"type": "competency_category", "description": "Fundamental competencies"},
            "basic_competencies": {"type": "competency_category", "description": "Essential skills"},
            "knowledge": {"type": "competency_domain", "description": "Cognitive domain"},
            "skills": {"type": "competency_domain", "description": "Practical abilities"},
            "attitudes": {"type": "competency_domain", "description": "Values and dispositions"}
        }
        self.edges = [
            {"source": "core_competencies", "target": "basic_competencies", "relation": "informs"},
            {"source": "basic_competencies", "target": "knowledge", "relation": "includes"},
            {"source": "basic_competencies", "target": "skills", "relation": "includes"},
            {"source": "basic_competencies", "target": "attitudes", "relation": "includes"}
        ]
    
    def query(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query competency ontology"""
        query_lower = query.lower()
        matched_nodes = {}
        
        for node_id, node_data in self.nodes.items():
            node_str = str(node_data).lower()
            if query_lower in node_str or query_lower in node_id.lower():
                matched_nodes[node_id] = node_data
        
        if filters:
            matched_nodes = {k: v for k, v in matched_nodes.items() if all(str(v.get(k2)) == str(v2) for k2, v2 in filters.items() if k2 in v)}
        
        return {
            "nodes": matched_nodes,
            "edges": [edge for edge in self.edges if edge["source"] in matched_nodes.keys() and edge["target"] in matched_nodes.keys()],
            "ontology": "competency"
        }


class AssessmentOntology:
    """Assessment ontology management"""
    
    def __init__(self):
        self.nodes = {
            "formative": {"type": "assessment", "description": "Ongoing assessment for learning"},
            "summative": {"type": "assessment", "description": "Final evaluation of learning"},
            "diagnostic": {"type": "assessment", "description": "Pre-assessment to identify needs"},
            "performance": {"type": "assessment", "description": "Task-based assessment"},
            "authentic": {"type": "assessment", "description": "Real-world application tasks"}
        }
        self.edges = [
            {"source": "diagnostic", "target": "formative", "relation": "precedes"},
            {"source": "formative", "target": "summative", "relation": "precedes"},
            {"source": "performance", "target": "authentic", "relation": "similar_to"}
        ]
    
    def query(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query assessment ontology"""
        query_lower = query.lower()
        matched_nodes = {}
        
        for node_id, node_data in self.nodes.items():
            node_str = str(node_data).lower()
            if query_lower in node_str or query_lower in node_id.lower():
                matched_nodes[node_id] = node_data
        
        if filters:
            matched_nodes = {k: v for k, v in matched_nodes.items() if all(str(v.get(k2)) == str(v2) for k2, v2 in filters.items() if k2 in v)}
        
        return {
            "nodes": matched_nodes,
            "edges": [edge for edge in self.edges if edge["source"] in matched_nodes.keys() and edge["target"] in matched_nodes.keys()],
            "ontology": "assessment"
        }


class LearningObjectiveOntology:
    """Learning objective ontology management"""
    
    def __init__(self):
        self.nodes = {
            "knowledge_objectives": {"type": "objective_domain", "description": "Knowledge-based objectives"},
            "skill_objectives": {"type": "objective_domain", "description": "Skill-based objectives"},
            "attitude_objectives": {"type": "objective_domain", "description": "Attitude-based objectives"},
            "critical_thinking": {"type": "objective_type", "description": "Higher-order thinking"},
            "problem_solving": {"type": "objective_type", "description": "Solution-oriented objectives"},
            "communication": {"type": "objective_type", "description": "Expression objectives"}
        }
        self.edges = [
            {"source": "knowledge_objectives", "target": "critical_thinking", "relation": "foundational_for"},
            {"source": "skill_objectives", "target": "problem_solving", "relation": "supports"},
            {"source": "attitude_objectives", "target": "communication", "relation": "enables"}
        ]
    
    def query(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query learning objective ontology"""
        query_lower = query.lower()
        matched_nodes = {}
        
        for node_id, node_data in self.nodes.items():
            node_str = str(node_data).lower()
            if query_lower in node_str or query_lower in node_id.lower():
                matched_nodes[node_id] = node_data
        
        if filters:
            matched_nodes = {k: v for k, v in matched_nodes.items() if all(str(v.get(k2)) == str(v2) for k2, v2 in filters.items() if k2 in v)}
        
        return {
            "nodes": matched_nodes,
            "edges": [edge for edge in self.edges if edge["source"] in matched_nodes.keys() and edge["target"] in matched_nodes.keys()],
            "ontology": "learning_objective"
        }


class ConceptHierarchy:
    """Concept hierarchy management"""
    
    def __init__(self):
        self.nodes = {
            "root_concept": {"type": "concept", "level": 0, "description": "Root educational concepts"},
            "domain_concept": {"type": "concept", "level": 1, "description": "Domain-level concepts"},
            "subdomain_concept": {"type": "concept", "level": 2, "description": "Subdomain concepts"},
            "specific_concept": {"type": "concept", "level": 3, "description": "Specific concepts"},
            "atomic_concept": {"type": "concept", "level": 4, "description": "Atomic concepts"}
        }
        self.edges = [
            {"source": "root_concept", "target": "domain_concept", "relation": "has_child"},
            {"source": "domain_concept", "target": "subdomain_concept", "relation": "has_child"},
            {"source": "subdomain_concept", "target": "specific_concept", "relation": "has_child"},
            {"source": "specific_concept", "target": "atomic_concept", "relation": "has_child"}
        ]
    
    def query(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """Query concept hierarchy"""
        query_lower = query.lower()
        matched_nodes = {}
        
        for node_id, node_data in self.nodes.items():
            node_str = str(node_data).lower()
            if query_lower in node_str or query_lower in node_id.lower():
                matched_nodes[node_id] = node_data
        
        if filters:
            matched_nodes = {k: v for k, v in matched_nodes.items() if all(str(v.get(k2)) == str(v2) for k2, v2 in filters.items() if k2 in v)}
        
        return {
            "nodes": matched_nodes,
            "edges": [edge for edge in self.edges if edge["source"] in matched_nodes.keys() and edge["target"] in matched_nodes.keys()],
            "ontology": "concept"
        }


# Initialize educational ontology engine
educational_ontology_engine = EducationalOntologyEngine()


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
        from .consumer import AsyncEducationalOntologyConsumer
        consumer = AsyncEducationalOntologyConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Educational Ontology Service",
    description="Advanced Enhancement - 6 Educational Ontologies",
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
        "service": "educational-ontology-service",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Ontology endpoints
@app.post("/ontology/query")
async def query_ontology(request: OntologyQueryRequest):
    """Query educational ontology"""
    ontology_type = request.ontology_type
    
    if ontology_type == "curriculum":
        result = educational_ontology_engine.query_curriculum_ontology(request.query, request.filters)
    elif ontology_type == "pedagogy":
        result = educational_ontology_engine.query_pedagogy_ontology(request.query, request.filters)
    elif ontology_type == "competency":
        result = educational_ontology_engine.query_competency_ontology(request.query, request.filters)
    elif ontology_type == "assessment":
        result = educational_ontology_engine.query_assessment_ontology(request.query, request.filters)
    elif ontology_type == "learning_objective":
        result = educational_ontology_engine.query_learning_objective_ontology(request.query, request.filters)
    elif ontology_type == "concept":
        result = educational_ontology_engine.query_concept_hierarchy(request.query, request.filters)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown ontology type: {ontology_type}")
    
    return OntologyResult(
        request_id=request.request_id,
        ontology_type=ontology_type,
        result=result["result"],
        metadata=result["metadata"]
    )


# Individual ontology endpoints
@app.post("/ontology/curriculum")
async def query_curriculum_ontology(query: str, filters: Optional[Dict] = None):
    """Query curriculum ontology"""
    result = educational_ontology_engine.query_curriculum_ontology(query, filters)
    return result


@app.post("/ontology/pedagogy")
async def query_pedagogy_ontology(query: str, filters: Optional[Dict] = None):
    """Query pedagogy ontology"""
    result = educational_ontology_engine.query_pedagogy_ontology(query, filters)
    return result


@app.post("/ontology/competency")
async def query_competency_ontology(query: str, filters: Optional[Dict] = None):
    """Query competency ontology"""
    result = educational_ontology_engine.query_competency_ontology(query, filters)
    return result


@app.post("/ontology/assessment")
async def query_assessment_ontology(query: str, filters: Optional[Dict] = None):
    """Query assessment ontology"""
    result = educational_ontology_engine.query_assessment_ontology(query, filters)
    return result


@app.post("/ontology/learning-objective")
async def query_learning_objective_ontology(query: str, filters: Optional[Dict] = None):
    """Query learning objective ontology"""
    result = educational_ontology_engine.query_learning_objective_ontology(query, filters)
    return result


@app.post("/ontology/concept")
async def query_concept_hierarchy(query: str, filters: Optional[Dict] = None):
    """Query concept hierarchy"""
    result = educational_ontology_engine.query_concept_hierarchy(query, filters)
    return result


# Performance monitoring
@app.get("/ontology/performance")
async def get_performance_metrics():
    """Get ontology performance metrics"""
    return educational_ontology_engine.performance_metrics


@app.get("/ontology/available")
async def get_available_ontologies():
    """Get available ontologies"""
    return {
        "ontologies": [
            {
                "name": "curriculum",
                "description": "Curriculum structure and documents ontology",
                "nodes": ["phase_a", "phase_b", "phase_c", "phase_d", "cp", "atp"]
            },
            {
                "name": "pedagogy",
                "description": "Teaching and learning approaches ontology",
                "nodes": ["inquiry", "differentiated", "collaborative", "direct", "experiential"]
            },
            {
                "name": "competency",
                "description": "Competency frameworks and domains ontology",
                "nodes": ["core_competencies", "basic_competencies", "knowledge", "skills", "attitudes"]
            },
            {
                "name": "assessment",
                "description": "Assessment types and methods ontology",
                "nodes": ["formative", "summative", "diagnostic", "performance", "authentic"]
            },
            {
                "name": "learning_objective",
                "description": "Learning objective domains and types ontology",
                "nodes": ["knowledge_objectives", "skill_objectives", "attitude_objectives", "critical_thinking", "problem_solving", "communication"]
            },
            {
                "name": "concept",
                "description": "Educational concept hierarchy ontology",
                "nodes": ["root_concept", "domain_concept", "subdomain_concept", "specific_concept", "atomic_concept"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8022)