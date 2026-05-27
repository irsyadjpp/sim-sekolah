"""
Curriculum Engine - Fase 5.1
Educational Intelligence Layer - Curriculum validation and CP/ATP alignment
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
GRPC_PORT = int(os.getenv("GRPC_PORT", "50062"))


# Pydantic models
class CPStructure(BaseModel):
    """Curriculum Program structure"""
    id: str
    name: str
    phase: str  # A, B, C, D
    grade: str
    subjects: List[str]
    competencies: List[Dict[str, Any]]
    learning_objectives: List[str]


class ATPStructure(BaseModel):
    """Annual Teaching Plan structure"""
    id: str
    cp_id: str
    phase: str
    grade: str
    semester: str
    topics: List[Dict[str, Any]]
    time_allocation: Dict[str, int]


class CurriculumValidationRequest(BaseModel):
    """Curriculum validation request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cp_structure: Optional[CPStructure] = None
    atp_structure: Optional[ATPStructure] = None
    validation_type: str  # cp, atp, alignment


class CurriculumValidationResult(BaseModel):
    """Curriculum validation result"""
    request_id: str
    is_valid: bool
    validation_type: str
    errors: List[str]
    warnings: List[str]
    alignment_score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AlignmentCheckRequest(BaseModel):
    """CP/ATP alignment check request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cp_id: str
    atp_id: str
    cp_structure: CPStructure
    atp_structure: ATPStructure


class AlignmentCheckResult(BaseModel):
    """CP/ATP alignment check result"""
    request_id: str
    cp_id: str
    atp_id: str
    is_aligned: bool
    alignment_score: float
    missing_competencies: List[str]
    extra_topics: List[str]
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CPStructureParser:
    """Parser for Curriculum Program structure"""
    
    def parse(self, raw_data: Dict[str, Any]) -> CPStructure:
        """Parse raw data into CP structure"""
        return CPStructure(
            id=raw_data.get("id", str(uuid.uuid4())),
            name=raw_data.get("name", ""),
            phase=raw_data.get("phase", ""),
            grade=raw_data.get("grade", ""),
            subjects=raw_data.get("subjects", []),
            competencies=raw_data.get("competencies", []),
            learning_objectives=raw_data.get("learning_objectives", [])
        )


class ATPStructureParser:
    """Parser for Annual Teaching Plan structure"""
    
    def parse(self, raw_data: Dict[str, Any]) -> ATPStructure:
        """Parse raw data into ATP structure"""
        return ATPStructure(
            id=raw_data.get("id", str(uuid.uuid4())),
            cp_id=raw_data.get("cp_id", ""),
            phase=raw_data.get("phase", ""),
            grade=raw_data.get("grade", ""),
            semester=raw_data.get("semester", ""),
            topics=raw_data.get("topics", []),
            time_allocation=raw_data.get("time_allocation", {})
        )


# Curriculum engine
class CurriculumEngine:
    """Curriculum validation and alignment engine"""
    
    def __init__(self):
        self.phase_map = {
            "A": ["1", "2"],
            "B": ["3", "4"],
            "C": ["5", "6"],
            "D": ["7", "8", "9"]
        }
        self.knowledge_base = {}  # In-memory knowledge base
        self.cp_parser = CPStructureParser()
        self.atp_parser = ATPStructureParser()
    
    def parse_cp_structure(self, raw_data: Dict[str, Any]) -> CPStructure:
        """Parse CP structure from raw data"""
        return self.cp_parser.parse(raw_data)
    
    def parse_atp_structure(self, raw_data: Dict[str, Any]) -> ATPStructure:
        """Parse ATP structure from raw data"""
        return self.atp_parser.parse(raw_data)
    
    def add_to_knowledge_base(self, entry_type: str, data: Dict[str, Any]) -> str:
        """Add entry to knowledge base"""
        entry_id = f"{entry_type}_{len(self.knowledge_base)}"
        self.knowledge_base[entry_id] = {
            "type": entry_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        return entry_id
    
    def query_knowledge_base(self, entry_type: str, filters: Dict[str, Any] = None) -> List[Dict]:
        """Query knowledge base"""
        results = []
        
        for entry_id, entry in self.knowledge_base.items():
            if entry["type"] == entry_type:
                if filters:
                    match = True
                    for key, value in filters.items():
                        if entry["data"].get(key) != value:
                            match = False
                            break
                    if match:
                        results.append(entry)
                else:
                    results.append(entry)
        
        return results
    
    def validate_cp(self, cp: CPStructure) -> Dict:
        """Validate Curriculum Program structure"""
        errors = []
        warnings = []
        
        # Check phase-grade alignment
        if cp.phase not in self.phase_map:
            errors.append(f"Invalid phase: {cp.phase}")
        elif cp.grade not in self.phase_map[cp.phase]:
            errors.append(f"Grade {cp.grade} not in phase {cp.phase}")
        
        # Check for required fields
        if not cp.subjects:
            errors.append("No subjects defined")
        
        if not cp.competencies:
            warnings.append("No competencies defined")
        
        if not cp.learning_objectives:
            warnings.append("No learning objectives defined")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def validate_atp(self, atp: ATPStructure) -> Dict:
        """Validate Annual Teaching Plan structure"""
        errors = []
        warnings = []
        
        # Check phase-grade alignment
        if atp.phase not in self.phase_map:
            errors.append(f"Invalid phase: {atp.phase}")
        elif atp.grade not in self.phase_map[atp.phase]:
            errors.append(f"Grade {atp.grade} not in phase {atp.phase}")
        
        # Check for required fields
        if not atp.topics:
            errors.append("No topics defined")
        
        if not atp.time_allocation:
            warnings.append("No time allocation defined")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def check_alignment(self, cp: CPStructure, atp: ATPStructure) -> Dict:
        """Check CP/ATP alignment"""
        missing_competencies = []
        extra_topics = []
        recommendations = []
        
        # Check phase/grade alignment
        if cp.phase != atp.phase:
            missing_competencies.append(f"Phase mismatch: CP {cp.phase} vs ATP {atp.phase}")
        
        if cp.grade != atp.grade:
            missing_competencies.append(f"Grade mismatch: CP {cp.grade} vs ATP {atp.grade}")
        
        # Check competency coverage
        cp_competencies = set(comp.get("code", "") for comp in cp.competencies)
        atp_topics = set(topic.get("competency", "") for topic in atp.topics)
        
        missing = cp_competencies - atp_topics
        if missing:
            missing_competencies.extend([f"Missing competency: {c}" for c in missing])
            recommendations.append("Add missing competencies to ATP")
        
        # Check for extra topics
        atp_competencies = set(topic.get("competency", "") for topic in atp.topics)
        extra = atp_competencies - cp_competencies
        if extra:
            extra_topics.extend([f"Extra topic: {t}" for t in extra])
            recommendations.append("Review extra topics in ATP")
        
        # Calculate alignment score
        total_cp = len(cp_competencies)
        covered = len(cp_competencies - missing)
        alignment_score = (covered / total_cp) if total_cp > 0 else 0.0
        
        return {
            "is_aligned": len(missing_competencies) == 0,
            "alignment_score": alignment_score,
            "missing_competencies": missing_competencies,
            "extra_topics": extra_topics,
            "recommendations": recommendations
        }


# Initialize curriculum engine
curriculum_engine = CurriculumEngine()


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
        from .consumer import AsyncCurriculumEngineConsumer
        consumer = AsyncCurriculumEngineConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Curriculum Engine",
    description="Educational Intelligence Layer - Curriculum validation and CP/ATP alignment",
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
        "service": "curriculum-engine",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Curriculum endpoints
@app.post("/curriculum/validate")
async def validate_curriculum(request: CurriculumValidationRequest):
    """Validate curriculum structure"""
    if request.validation_type == "cp" and request.cp_structure:
        result = curriculum_engine.validate_cp(request.cp_structure)
        return CurriculumValidationResult(
            request_id=request.request_id,
            is_valid=result["is_valid"],
            validation_type="cp",
            errors=result["errors"],
            warnings=result["warnings"]
        )
    elif request.validation_type == "atp" and request.atp_structure:
        result = curriculum_engine.validate_atp(request.atp_structure)
        return CurriculumValidationResult(
            request_id=request.request_id,
            is_valid=result["is_valid"],
            validation_type="atp",
            errors=result["errors"],
            warnings=result["warnings"]
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid validation request")


@app.post("/curriculum/alignment")
async def check_cp_atp_alignment(request: AlignmentCheckRequest):
    """Check CP/ATP alignment"""
    result = curriculum_engine.check_alignment(request.cp_structure, request.atp_structure)
    return AlignmentCheckResult(
        request_id=request.request_id,
        cp_id=request.cp_id,
        atp_id=request.atp_id,
        is_aligned=result["is_aligned"],
        alignment_score=result["alignment_score"],
        missing_competencies=result["missing_competencies"],
        extra_topics=result["extra_topics"],
        recommendations=result["recommendations"]
    )


@app.get("/curriculum/phase-info")
async def get_phase_info():
    """Get phase information"""
    return curriculum_engine.phase_map


# Parsing endpoints
@app.post("/curriculum/parse-cp")
async def parse_cp(raw_data: Dict[str, Any]):
    """Parse CP structure from raw data"""
    cp_structure = curriculum_engine.parse_cp_structure(raw_data)
    return {
        "cp_structure": cp_structure,
        "status": "parsed"
    }


@app.post("/curriculum/parse-atp")
async def parse_atp(raw_data: Dict[str, Any]):
    """Parse ATP structure from raw data"""
    atp_structure = curriculum_engine.parse_atp_structure(raw_data)
    return {
        "atp_structure": atp_structure,
        "status": "parsed"
    }


# Knowledge base endpoints
@app.post("/curriculum/knowledge-base/add")
async def add_to_knowledge_base(entry_type: str, data: Dict[str, Any]):
    """Add entry to knowledge base"""
    entry_id = curriculum_engine.add_to_knowledge_base(entry_type, data)
    return {
        "entry_id": entry_id,
        "status": "added"
    }


@app.get("/curriculum/knowledge-base/query")
async def query_knowledge_base(entry_type: str, filters: Optional[str] = None):
    """Query knowledge base"""
    filter_dict = eval(filters) if filters else None
    results = curriculum_engine.query_knowledge_base(entry_type, filter_dict)
    return {
        "results": results,
        "count": len(results)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8013)
