"""
TP Progression Engine

This module handles the progression of Tujuan Pembelajaran (TP) across
learning phases and tracks student progress through TP mastery.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class TPProgressionStatus(str, Enum):
    """TP progression status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    MASTERED = "mastered"
    NEEDS_REINFORCEMENT = "needs_reinforcement"


class TPProgressionEngine:
    """Engine for TP progression tracking and management"""
    
    def __init__(self):
        self.progression_rules = self._initialize_progression_rules()
        self.progression_data: Dict[str, Dict] = {}
    
    def create_tp_progression(
        self, 
        student_id: str,
        tps: List[Dict],
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Create TP progression for a student"""
        progression = {
            "student_id": student_id,
            "fase": fase,
            "mata_pelajaran": mata_pelajaran,
            "tp_progression": {},
            "overall_progress": 0.0,
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        for tp in tps:
            progression["tp_progression"][tp["tp_id"]] = {
                "tp_id": tp["tp_id"],
                "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
                "domain": tp.get("domain", "kognitif"),
                "difficulty": tp.get("difficulty", "sedang"),
                "status": TPProgressionStatus.NOT_STARTED.value,
                "progress": 0.0,
                "evidence": [],
                "assessments": [],
                "started_at": None,
                "achieved_at": None,
                "mastered_at": None
            }
        
        progression_id = f"PROG_{student_id}_{fase}_{mata_pelajaran}"
        self.progression_data[progression_id] = progression
        
        return progression
    
    def update_tp_progress(
        self, 
        progression_id: str,
        tp_id: str,
        progress: float,
        evidence: Optional[Dict] = None
    ) -> Dict:
        """Update progress for a specific TP"""
        if progression_id not in self.progression_data:
            return {"error": "Progression not found"}
        
        progression = self.progression_data[progression_id]
        
        if tp_id not in progression["tp_progression"]:
            return {"error": "TP not found in progression"}
        
        tp_progress = progression["tp_progression"][tp_id]
        tp_progress["progress"] = progress
        
        if evidence:
            tp_progress["evidence"].append(evidence)
        
        # Update status based on progress
        if progress >= 0.9:
            tp_progress["status"] = TPProgressionStatus.MASTERED.value
            if not tp_progress["mastered_at"]:
                tp_progress["mastered_at"] = datetime.utcnow().isoformat()
        elif progress >= 0.7:
            tp_progress["status"] = TPProgressionStatus.ACHIEVED.value
            if not tp_progress["achieved_at"]:
                tp_progress["achieved_at"] = datetime.utcnow().isoformat()
        elif progress > 0:
            tp_progress["status"] = TPProgressionStatus.IN_PROGRESS.value
            if not tp_progress["started_at"]:
                tp_progress["started_at"] = datetime.utcnow().isoformat()
        else:
            tp_progress["status"] = TPProgressionStatus.NOT_STARTED.value
        
        # Recalculate overall progress
        progression["overall_progress"] = self._calculate_overall_progress(progression)
        progression["last_updated"] = datetime.utcnow().isoformat()
        
        return {
            "progression_id": progression_id,
            "tp_id": tp_id,
            "new_progress": progress,
            "new_status": tp_progress["status"],
            "overall_progress": progression["overall_progress"]
        }
    
    def get_tp_progression(
        self, 
        student_id: str,
        fase: str,
        mata_pelajaran: str
    ) -> Optional[Dict]:
        """Get TP progression for a student"""
        progression_id = f"PROG_{student_id}_{fase}_{mata_pelajaran}"
        return self.progression_data.get(progression_id)
    
    def get_next_tps(
        self, 
        progression_id: str,
        count: int = 3
    ) -> List[Dict]:
        """Get next TPs to focus on based on progression"""
        if progression_id not in self.progression_data:
            return []
        
        progression = self.progression_data[progression_id]
        
        # Get TPs that are not yet mastered, sorted by progress
        not_mastered = [
            tp for tp in progression["tp_progression"].values()
            if tp["status"] != TPProgressionStatus.MASTERED.value
        ]
        
        not_mastered.sort(key=lambda x: x["progress"])
        
        return not_mastered[:count]
    
    def identify_gaps(
        self, 
        progression_id: str
    ) -> List[Dict]:
        """Identify learning gaps in TP progression"""
        if progression_id not in self.progression_data:
            return []
        
        progression = self.progression_data[progression_id]
        gaps = []
        
        for tp_id, tp_progress in progression["tp_progression"].items():
            if tp_progress["progress"] < 0.5:
                gaps.append({
                    "tp_id": tp_id,
                    "tujuan_pembelajaran": tp_progress["tujuan_pembelajaran"],
                    "current_progress": tp_progress["progress"],
                    "gap": 1.0 - tp_progress["progress"],
                    "priority": "high" if tp_progress["progress"] < 0.3 else "medium"
                })
        
        return sorted(gaps, key=lambda x: x["gap"], reverse=True)
    
    def recommend_reinforcement(
        self, 
        progression_id: str
    ) -> List[Dict]:
        """Recommend reinforcement activities for TPs needing support"""
        gaps = self.identify_gaps(progression_id)
        
        recommendations = []
        for gap in gaps[:5]:  # Top 5 gaps
            recommendation = {
                "tp_id": gap["tp_id"],
                "tujuan_pembelajaran": gap["tujuan_pembelajaran"],
                "reinforcement_type": self._determine_reinforcement_type(gap),
                "suggested_activities": self._suggest_reinforcement_activities(gap),
                "estimated_duration": "15-20 menit"
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def calculate_progression_velocity(
        self, 
        progression_id: str
    ) -> Dict:
        """Calculate progression velocity (speed of learning)"""
        if progression_id not in self.progression_data:
            return {"error": "Progression not found"}
        
        progression = self.progression_data[progression_id]
        
        # Calculate average time to achieve TPs
        achieved_tps = [
            tp for tp in progression["tp_progression"].values()
            if tp["achieved_at"] and tp["started_at"]
        ]
        
        if not achieved_tps:
            return {"velocity": "no_data"}
        
        total_time = 0
        for tp in achieved_tps:
            start = datetime.fromisoformat(tp["started_at"])
            achieved = datetime.fromisoformat(tp["achieved_at"])
            total_time += (achieved - start).total_seconds() / 3600  # hours
        
        avg_time = total_time / len(achieved_tps)
        
        return {
            "average_time_to_achieve": f"{avg_time:.2f} hours",
            "total_tps_achieved": len(achieved_tps),
            "total_tps": len(progression["tp_progression"]),
            "velocity_score": self._calculate_velocity_score(avg_time)
        }
    
    def _calculate_overall_progress(self, progression: Dict) -> float:
        """Calculate overall progress across all TPs"""
        tp_progressions = progression["tp_progression"]
        
        if not tp_progressions:
            return 0.0
        
        total_progress = sum(tp["progress"] for tp in tp_progressions.values())
        return total_progress / len(tp_progressions)
    
    def _determine_reinforcement_type(self, gap: Dict) -> str:
        """Determine type of reinforcement needed"""
        if gap["current_progress"] < 0.2:
            return "remedial"
        elif gap["current_progress"] < 0.4:
            return "intensif"
        else:
            return "penguatan"
    
    def _suggest_reinforcement_activities(self, gap: Dict) -> List[str]:
        """Suggest reinforcement activities"""
        activities = [
            "Ulang materi dengan pendekatan berbeda",
            "Gunakan media pembelajaran visual",
            "Latihan soal bertahap",
            "Diskusi kelompok kecil",
            "Peer teaching"
        ]
        
        return activities[:3]
    
    def _calculate_velocity_score(self, avg_time: float) -> str:
        """Calculate velocity score based on average time"""
        if avg_time < 2:
            return "very_fast"
        elif avg_time < 4:
            return "fast"
        elif avg_time < 6:
            return "normal"
        else:
            return "slow"
    
    def _initialize_progression_rules(self) -> Dict:
        """Initialize progression rules"""
        return {
            "mastery_threshold": 0.9,
            "achievement_threshold": 0.7,
            "progress_threshold": 0.1,
            "reinforcement_threshold": 0.5
        }
    
    def generate_progression_report(
        self, 
        progression_id: str
    ) -> Dict:
        """Generate comprehensive progression report"""
        if progression_id not in self.progression_data:
            return {"error": "Progression not found"}
        
        progression = self.progression_data[progression_id]
        
        return {
            "progression_id": progression_id,
            "student_id": progression["student_id"],
            "fase": progression["fase"],
            "mata_pelajaran": progression["mata_pelajaran"],
            "overall_progress": progression["overall_progress"],
            "tp_count": len(progression["tp_progression"]),
            "mastered_count": sum(
                1 for tp in progression["tp_progression"].values()
                if tp["status"] == TPProgressionStatus.MASTERED.value
            ),
            "achieved_count": sum(
                1 for tp in progression["tp_progression"].values()
                if tp["status"] == TPProgressionStatus.ACHIEVED.value
            ),
            "in_progress_count": sum(
                1 for tp in progression["tp_progression"].values()
                if tp["status"] == TPProgressionStatus.IN_PROGRESS.value
            ),
            "not_started_count": sum(
                1 for tp in progression["tp_progression"].values()
                if tp["status"] == TPProgressionStatus.NOT_STARTED.value
            ),
            "gaps": self.identify_gaps(progression_id),
            "next_focus": self.get_next_tps(progression_id, count=3),
            "reinforcement_recommendations": self.recommend_reinforcement(progression_id),
            "velocity": self.calculate_progression_velocity(progression_id),
            "generated_at": datetime.utcnow().isoformat()
        }
