"""
Standards Database Module

Provides database schema and access methods for storing and retrieving
all curriculum standards.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class StandardRecord:
    """Standard record structure for database"""
    id: str
    standard_type: str  # CP, ATP, ModulAjar, Assessment, Rubric, ProfilPancasila
    standard_code: str
    name: str
    description: str
    phase: Optional[str] = None
    grade: Optional[str] = None
    subject: Optional[str] = None
    content: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class StandardsDatabase:
    """In-memory database for standards (can be extended to real database)"""
    
    def __init__(self):
        self.standards: Dict[str, StandardRecord] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample Kurikulum Merdeka standards"""
        # Sample CP standards
        self._add_sample_cp("A", "IPA")
        self._add_sample_cp("B", "IPA")
        self._add_sample_cp("C", "IPA")
        self._add_sample_cp("D", "IPA")
        
        # Sample ATP standards
        self._add_sample_atp("1", "ganjil", "IPA")
        self._add_sample_atp("2", "ganjil", "IPA")
        self._add_sample_atp("7", "ganjil", "IPA")
        
        # Sample Profil Pelajar Pancasila
        self._add_sample_profil_pancasila()
    
    def _add_sample_cp(self, phase: str, subject: str):
        """Add sample CP standard"""
        cp_id = f"CP_{subject}_{phase}"
        self.standards[cp_id] = StandardRecord(
            id=cp_id,
            standard_type="CP",
            standard_code=f"CP-{subject}-{phase}",
            name=f"CP {subject} Fase {phase}",
            description=f"Curriculum Program for {subject} in Phase {phase}",
            phase=phase,
            subject=subject,
            content={
                "learning_objectives": [
                    f"Memahami konsep dasar {subject}",
                    f"Mengaplikasikan {subject} dalam konteks nyata",
                    f"Mengembangkan kemampuan berpikir kritis dalam {subject}"
                ],
                "competencies": {
                    "KI": ["KI-1", "KI-2", "KI-3", "KI-4"],
                    "KD": ["KD-1", "KD-2", "KD-3", "KD-4"]
                }
            },
            metadata={"version": "1.0", "year": "2026"}
        )
    
    def _add_sample_atp(self, grade: str, semester: str, subject: str):
        """Add sample ATP standard"""
        atp_id = f"ATP_{subject}_{grade}_{semester}"
        self.standards[atp_id] = StandardRecord(
            id=atp_id,
            standard_type="ATP",
            standard_code=f"ATP-{subject}-{grade}-{semester}",
            name=f"ATP {subject} Kelas {grade} {semester}",
            description=f"Annual Teaching Plan for {subject} Grade {grade} {semester}",
            grade=grade,
            subject=subject,
            content={
                "semester": semester,
                "topics": [
                    {"topic": f"Introduction {subject}", "weeks": 2},
                    {"topic": f"Core {subject}", "weeks": 3},
                    {"topic": f"Application {subject}", "weeks": 2},
                    {"topic": f"Project {subject}", "weeks": 2},
                    {"topic": f"Review {subject}", "weeks": 1}
                ],
                "time_allocation": {
                    "weekly_hours": 5,
                    "semester_hours": 100
                }
            },
            metadata={"version": "1.0", "year": "2026"}
        )
    
    def _add_sample_profil_pancasila(self):
        """Add sample Profil Pelajar Pancasila standard"""
        dimensions = [
            "Beriman, bertakwa kepada Tuhan YME, dan berakhlak mulia",
            "Berkebinekaan global",
            "Gotong royong",
            "Mandiri",
            "Bernalar kritis",
            "Kreatif"
        ]
        
        for i, dimension in enumerate(dimensions):
            dim_id = f"PP_{i+1}"
            self.standards[dim_id] = StandardRecord(
                id=dim_id,
                standard_type="ProfilPancasila",
                standard_code=f"PP-{i+1}",
                name=f"Dimensi {i+1}: {dimension}",
                description=f"Profil Pelajar Pancasila Dimension {i+1}",
                content={
                    "dimension": dimension,
                    "indicators": [
                        f"Indikator 1 untuk {dimension}",
                        f"Indikator 2 untuk {dimension}",
                        f"Indikator 3 untuk {dimension}"
                    ],
                    "assessment_criteria": [
                        f"Kriteria asesmen 1",
                        f"Kriteria asesmen 2"
                    ]
                },
                metadata={"dimension_index": i+1, "version": "1.0"}
            )
    
    def get_standard(self, standard_type: str, standard_id: str) -> Optional[Dict]:
        """Get specific standard by type and ID"""
        for record in self.standards.values():
            if record.standard_type == standard_type and record.id == standard_id:
                return {
                    "id": record.id,
                    "type": record.standard_type,
                    "code": record.standard_code,
                    "name": record.name,
                    "description": record.description,
                    "content": record.content,
                    "metadata": record.metadata
                }
        return None
    
    def get_standards_by_type(self, standard_type: str) -> List[Dict]:
        """Get all standards of a specific type"""
        results = []
        for record in self.standards.values():
            if record.standard_type == standard_type:
                results.append({
                    "id": record.id,
                    "type": record.standard_type,
                    "code": record.standard_code,
                    "name": record.name,
                    "description": record.description,
                    "content": record.content,
                    "metadata": record.metadata
                })
        return results
    
    def save_standard(self, standard_data: Dict) -> Dict:
        """Save new standard to database"""
        standard_id = standard_data.get("id", str(uuid.uuid4()))
        
        new_record = StandardRecord(
            id=standard_id,
            standard_type=standard_data.get("type", "Unknown"),
            standard_code=standard_data.get("code", ""),
            name=standard_data.get("name", ""),
            description=standard_data.get("description", ""),
            phase=standard_data.get("phase"),
            grade=standard_data.get("grade"),
            subject=standard_data.get("subject"),
            content=standard_data.get("content", {}),
            metadata=standard_data.get("metadata", {})
        )
        
        self.standards[standard_id] = new_record
        return {"success": True, "id": standard_id}
    
    def update_standard(self, standard_id: str, update_data: Dict) -> Dict:
        """Update existing standard"""
        if standard_id not in self.standards:
            return {"success": False, "error": "Standard not found"}
        
        record = self.standards[standard_id]
        
        # Update fields
        if "name" in update_data:
            record.name = update_data["name"]
        if "description" in update_data:
            record.description = update_data["description"]
        if "content" in update_data:
            record.content.update(update_data["content"])
        if "metadata" in update_data:
            record.metadata.update(update_data["metadata"])
        
        record.updated_at = datetime.utcnow().isoformat()
        
        return {"success": True, "id": standard_id}
    
    def delete_standard(self, standard_id: str) -> Dict:
        """Delete standard from database"""
        if standard_id not in self.standards:
            return {"success": False, "error": "Standard not found"}
        
        del self.standards[standard_id]
        return {"success": True}
    
    def search_standards(self, query: str) -> List[Dict]:
        """Search standards by query"""
        results = []
        query_lower = query.lower()
        
        for record in self.standards.values():
            if (query_lower in record.name.lower() or 
                query_lower in record.description.lower() or
                query_lower in str(record.content).lower()):
                results.append({
                    "id": record.id,
                    "type": record.standard_type,
                    "code": record.standard_code,
                    "name": record.name,
                    "description": record.description
                })
        
        return results