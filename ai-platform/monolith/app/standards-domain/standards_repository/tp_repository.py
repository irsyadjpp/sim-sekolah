"""
TP Repository

This module manages the repository for Tujuan Pembelajaran (TP) data.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class TPRepository:
    """Repository for Tujuan Pembelajaran data"""
    
    def __init__(self):
        self.tp_data: Dict[str, Dict] = {}
        self.tp_index: Dict[str, List[str]] = {}  # Index by fase, mata_pelajaran
    
    def save_tp(self, tp: Dict) -> Dict:
        """Save a TP to the repository"""
        tp_id = tp["tp_id"]
        
        # Add metadata
        tp["created_at"] = tp.get("created_at", datetime.utcnow().isoformat())
        tp["updated_at"] = datetime.utcnow().isoformat()
        
        self.tp_data[tp_id] = tp
        
        # Update index
        fase = tp.get("fase", "")
        mata_pelajaran = tp.get("mata_pelajaran", "")
        index_key = f"{fase}_{mata_pelajaran}"
        
        if index_key not in self.tp_index:
            self.tp_index[index_key] = []
        
        if tp_id not in self.tp_index[index_key]:
            self.tp_index[index_key].append(tp_id)
        
        return {"status": "saved", "tp_id": tp_id}
    
    def get_tp(self, tp_id: str) -> Optional[Dict]:
        """Get a TP by ID"""
        return self.tp_data.get(tp_id)
    
    def get_tps_by_fase_mata_pelajaran(
        self, 
        fase: str, 
        mata_pelajaran: str
    ) -> List[Dict]:
        """Get all TPs for a specific fase and mata pelajaran"""
        index_key = f"{fase}_{mata_pelajaran}"
        tp_ids = self.tp_index.get(index_key, [])
        
        return [self.tp_data[tp_id] for tp_id in tp_ids if tp_id in self.tp_data]
    
    def update_tp(self, tp_id: str, updates: Dict) -> Dict:
        """Update a TP"""
        if tp_id not in self.tp_data:
            return {"error": "TP not found"}
        
        self.tp_data[tp_id].update(updates)
        self.tp_data[tp_id]["updated_at"] = datetime.utcnow().isoformat()
        
        return {"status": "updated", "tp_id": tp_id}
    
    def delete_tp(self, tp_id: str) -> Dict:
        """Delete a TP"""
        if tp_id not in self.tp_data:
            return {"error": "TP not found"}
        
        tp = self.tp_data[tp_id]
        fase = tp.get("fase", "")
        mata_pelajaran = tp.get("mata_pelajaran", "")
        index_key = f"{fase}_{mata_pelajaran}"
        
        # Remove from index
        if index_key in self.tp_index and tp_id in self.tp_index[index_key]:
            self.tp_index[index_key].remove(tp_id)
        
        # Remove from data
        del self.tp_data[tp_id]
        
        return {"status": "deleted", "tp_id": tp_id}
    
    def search_tps(self, criteria: Dict) -> List[Dict]:
        """Search TPs by criteria"""
        results = []
        
        for tp in self.tp_data.values():
            match = True
            
            for key, value in criteria.items():
                if key not in tp or tp[key] != value:
                    match = False
                    break
            
            if match:
                results.append(tp)
        
        return results
    
    def get_all_tps(self) -> List[Dict]:
        """Get all TPs"""
        return list(self.tp_data.values())
    
    def count_tps(self) -> int:
        """Count total TPs in repository"""
        return len(self.tp_data)
