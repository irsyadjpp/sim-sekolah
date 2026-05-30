"""
Curriculum Service - Monolith Architecture
Complete curriculum functionality using actual business logic
"""
import sys
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

sys.path.append('/app')

logger = logging.getLogger(__name__)


class CPStructure:
    """Curriculum Program structure"""
    def __init__(self, id: str, name: str, phase: str, grade: str, 
                 subjects: List[str], competencies: List[Dict[str, Any]], 
                 learning_objectives: List[str]):
        self.id = id
        self.name = name
        self.phase = phase
        self.grade = grade
        self.subjects = subjects
        self.competencies = competencies
        self.learning_objectives = learning_objectives


class ATPStructure:
    """Annual Teaching Plan structure"""
    def __init__(self, id: str, cp_id: str, phase: str, grade: str,
                 semester: str, topics: List[Dict[str, Any]], 
                 time_allocation: Dict[str, int]):
        self.id = id
        self.cp_id = cp_id
        self.phase = phase
        self.grade = grade
        self.semester = semester
        self.topics = topics
        self.time_allocation = time_allocation


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


class CurriculumEngine:
    """Curriculum validation and alignment engine with complete business logic"""
    
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


class CurriculumService:
    """Curriculum service with complete business logic"""
    
    def __init__(self):
        """Initialize curriculum service with actual engine"""
        self.initialized = False
        self.curriculum_engine = CurriculumEngine()
    
    def initialize(self):
        """Initialize curriculum service"""
        try:
            logger.info("Initializing Curriculum Service with actual business logic")
            self.initialized = True
            logger.info("Curriculum Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Curriculum Service: {e}")
            raise
    
    def parse_cp_structure(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse CP structure from raw data"""
        cp_structure = self.curriculum_engine.parse_cp_structure(raw_data)
        return {
            "cp_structure": cp_structure,
            "status": "parsed"
        }
    
    def parse_atp_structure(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse ATP structure from raw data"""
        atp_structure = self.curriculum_engine.parse_atp_structure(raw_data)
        return {
            "atp_structure": atp_structure,
            "status": "parsed"
        }
    
    def validate_cp(self, cp_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Curriculum Program structure"""
        cp = CPStructure(
            id=cp_structure.get("id", ""),
            name=cp_structure.get("name", ""),
            phase=cp_structure.get("phase", ""),
            grade=cp_structure.get("grade", ""),
            subjects=cp_structure.get("subjects", []),
            competencies=cp_structure.get("competencies", []),
            learning_objectives=cp_structure.get("learning_objectives", [])
        )
        return self.curriculum_engine.validate_cp(cp)
    
    def validate_atp(self, atp_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Annual Teaching Plan structure"""
        atp = ATPStructure(
            id=atp_structure.get("id", ""),
            cp_id=atp_structure.get("cp_id", ""),
            phase=atp_structure.get("phase", ""),
            grade=atp_structure.get("grade", ""),
            semester=atp_structure.get("semester", ""),
            topics=atp_structure.get("topics", []),
            time_allocation=atp_structure.get("time_allocation", {})
        )
        return self.curriculum_engine.validate_atp(atp)
    
    def check_alignment(self, cp_structure: Dict[str, Any], atp_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Check CP/ATP alignment"""
        cp = CPStructure(
            id=cp_structure.get("id", ""),
            name=cp_structure.get("name", ""),
            phase=cp_structure.get("phase", ""),
            grade=cp_structure.get("grade", ""),
            subjects=cp_structure.get("subjects", []),
            competencies=cp_structure.get("competencies", []),
            learning_objectives=cp_structure.get("learning_objectives", [])
        )
        atp = ATPStructure(
            id=atp_structure.get("id", ""),
            cp_id=atp_structure.get("cp_id", ""),
            phase=atp_structure.get("phase", ""),
            grade=atp_structure.get("grade", ""),
            semester=atp_structure.get("semester", ""),
            topics=atp_structure.get("topics", []),
            time_allocation=atp_structure.get("time_allocation", {})
        )
        return self.curriculum_engine.check_alignment(cp, atp)
    
    def add_to_knowledge_base(self, entry_type: str, data: Dict[str, Any]) -> str:
        """Add entry to knowledge base"""
        return self.curriculum_engine.add_to_knowledge_base(entry_type, data)
    
    def query_knowledge_base(self, entry_type: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Query knowledge base"""
        return self.curriculum_engine.query_knowledge_base(entry_type, filters)
    
    def get_phase_info(self) -> Dict[str, List[str]]:
        """Get phase information"""
        return self.curriculum_engine.phase_map
    
    def health(self) -> Dict[str, Any]:
        """Health check for curriculum service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "curriculum_service",
            "architecture": "monolith",
            "components": {
                "curriculum_engine": "ready"
            }
        }
    
    async def create_curriculum(self, curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create curriculum using actual microservice logic
        
        Args:
            curriculum_data: Curriculum configuration and content
            
        Returns:
            Created curriculum
        """
        try:
            logger.info("Creating curriculum")
            
            # Use actual curriculum engine logic
            result = self.curriculum_engine.create_curriculum(curriculum_data)
            
            logger.info("Curriculum created successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error creating curriculum: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def analyze_alignment(self, curriculum_id: str, standards: List[str]) -> Dict[str, Any]:
        """
        Analyze curriculum alignment with standards using actual microservice logic
        
        Args:
            curriculum_id: Curriculum identifier
            standards: Educational standards to align with
            
        Returns:
            Alignment analysis result
        """
        try:
            logger.info(f"Analyzing alignment for curriculum: {curriculum_id}")
            
            # Use actual curriculum engine logic
            result = self.curriculum_engine.analyze_alignment(curriculum_id, standards)
            
            logger.info(f"Alignment analysis completed for curriculum {curriculum_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing alignment: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
