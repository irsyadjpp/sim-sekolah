"""
Regulation Repository

This module manages the repository for education regulations and standards.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class RegulationType(str, Enum):
    """Types of education regulations"""
    KURIKULUM_MERDEKA = "kurikulum_merdeka"
    PEMBELAJARAN_MENDALAM = "pembelajaran_mendalam"
    PROFIL_PELAJAR_PANCASILA = "profil_pelajar_pancasila"
    STANDAR_NASIONAL = "standar_nasional"
    PERATURAN_MENTERI = "peraturan_menteri"
    PERATURAN_DAERAH = "peraturan_daerah"


class RegulationRepository:
    """Repository for education regulations"""
    
    def __init__(self):
        self.regulation_data: Dict[str, Dict] = {}
        self.regulation_index: Dict[str, List[str]] = {}  # Index by type, year
    
    def save_regulation(self, regulation: Dict) -> Dict:
        """Save a regulation to the repository"""
        reg_id = regulation.get("regulation_id", f"REG_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}")
        
        # Add metadata
        regulation["regulation_id"] = reg_id
        regulation["created_at"] = regulation.get("created_at", datetime.utcnow().isoformat())
        regulation["updated_at"] = datetime.utcnow().isoformat()
        
        self.regulation_data[reg_id] = regulation
        
        # Update index
        reg_type = regulation.get("type", "")
        year = regulation.get("year", "")
        index_key = f"{reg_type}_{year}"
        
        if index_key not in self.regulation_index:
            self.regulation_index[index_key] = []
        
        if reg_id not in self.regulation_index[index_key]:
            self.regulation_index[index_key].append(reg_id)
        
        return {"status": "saved", "regulation_id": reg_id}
    
    def get_regulation(self, regulation_id: str) -> Optional[Dict]:
        """Get a regulation by ID"""
        return self.regulation_data.get(regulation_id)
    
    def get_regulations_by_type(self, regulation_type: RegulationType) -> List[Dict]:
        """Get all regulations of a specific type"""
        results = []
        
        for regulation in self.regulation_data.values():
            if regulation.get("type") == regulation_type.value:
                results.append(regulation)
        
        return results
    
    def get_regulations_by_year(self, year: str) -> List[Dict]:
        """Get all regulations from a specific year"""
        results = []
        
        for regulation in self.regulation_data.values():
            if regulation.get("year") == year:
                results.append(regulation)
        
        return results
    
    def search_regulations(self, criteria: Dict) -> List[Dict]:
        """Search regulations by criteria"""
        results = []
        
        for regulation in self.regulation_data.values():
            match = True
            
            for key, value in criteria.items():
                if key not in regulation or regulation[key] != value:
                    match = False
                    break
            
            if match:
                results.append(regulation)
        
        return results
    
    def update_regulation(self, regulation_id: str, updates: Dict) -> Dict:
        """Update a regulation"""
        if regulation_id not in self.regulation_data:
            return {"error": "Regulation not found"}
        
        self.regulation_data[regulation_id].update(updates)
        self.regulation_data[regulation_id]["updated_at"] = datetime.utcnow().isoformat()
        
        return {"status": "updated", "regulation_id": regulation_id}
    
    def delete_regulation(self, regulation_id: str) -> Dict:
        """Delete a regulation"""
        if regulation_id not in self.regulation_data:
            return {"error": "Regulation not found"}
        
        regulation = self.regulation_data[regulation_id]
        reg_type = regulation.get("type", "")
        year = regulation.get("year", "")
        index_key = f"{reg_type}_{year}"
        
        # Remove from index
        if index_key in self.regulation_index and regulation_id in self.regulation_index[index_key]:
            self.regulation_index[index_key].remove(regulation_id)
        
        # Remove from data
        del self.regulation_data[regulation_id]
        
        return {"status": "deleted", "regulation_id": regulation_id}
    
    def get_all_regulations(self) -> List[Dict]:
        """Get all regulations"""
        return list(self.regulation_data.values())
    
    def count_regulations(self) -> int:
        """Count total regulations in repository"""
        return len(self.regulation_data)
    
    def initialize_default_regulations(self) -> Dict:
        """Initialize default Kurikulum Merdeka regulations"""
        default_regulations = [
            {
                "type": RegulationType.KURIKULUM_MERDEKA.value,
                "title": "Kurikulum Merdeka",
                "description": "Kurikulum Merdeka adalah kurikulum berbasis kompetensi dan karakter",
                "year": "2022",
                "version": "1.0",
                "status": "active"
            },
            {
                "type": RegulationType.PEMBELAJARAN_MENDALAM.value,
                "title": "Pembelajaran Mendalam",
                "description": "Pembelajaran Mendalam menekankan pemahaman, aplikasi, dan refleksi",
                "year": "2022",
                "version": "1.0",
                "status": "active"
            },
            {
                "type": RegulationType.PROFIL_PELAJAR_PANCASILA.value,
                "title": "Profil Pelajar Pancasila",
                "description": "Profil Pelajar Pancasila mencakup 6 dimensi karakter",
                "year": "2022",
                "version": "1.0",
                "status": "active"
            }
        ]
        
        for reg in default_regulations:
            self.save_regulation(reg)
        
        return {"status": "initialized", "count": len(default_regulations)}
