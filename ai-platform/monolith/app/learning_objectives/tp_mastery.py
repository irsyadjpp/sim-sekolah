"""
TP Mastery Engine

This module handles mastery assessment and tracking for Tujuan Pembelajaran (TP).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class TPMasteryLevel(str, Enum):
    """TP mastery levels"""
    BELUM_MENGUASAI = "belum_menguasai"
    SEDANG_MENGUASAI = "sedang_menguasai"
    MENGUASAI = "menguasai"
    SANGAT_MENGUASAI = "sangat_menguasai"


class TPMasteryEngine:
    """Engine for TP mastery assessment and tracking"""
    
    def __init__(self):
        self.mastery_criteria = self._initialize_mastery_criteria()
        self.mastery_data: Dict[str, Dict] = {}
    
    def assess_mastery(
        self, 
        student_id: str,
        tp_id: str,
        assessment_results: List[Dict],
        evidence: Optional[List[Dict]] = None
    ) -> Dict:
        """Assess mastery level for a specific TP"""
        # Calculate mastery score from assessment results
        mastery_score = self._calculate_mastery_score(assessment_results)
        
        # Determine mastery level
        mastery_level = self._determine_mastery_level(mastery_score)
        
        mastery_record = {
            "mastery_id": f"MAST_{student_id}_{tp_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "student_id": student_id,
            "tp_id": tp_id,
            "mastery_score": mastery_score,
            "mastery_level": mastery_level.value,
            "assessment_results": assessment_results,
            "evidence": evidence or [],
            "assessed_at": datetime.utcnow().isoformat()
        }
        
        # Store mastery record
        key = f"{student_id}_{tp_id}"
        self.mastery_data[key] = mastery_record
        
        return mastery_record
    
    def get_mastery(
        self, 
        student_id: str,
        tp_id: str
    ) -> Optional[Dict]:
        """Get mastery record for a student and TP"""
        key = f"{student_id}_{tp_id}"
        return self.mastery_data.get(key)
    
    def get_student_mastery_summary(
        self, 
        student_id: str,
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Get mastery summary for a student"""
        # Filter mastery records for student
        student_records = [
            record for record in self.mastery_data.values()
            if record["student_id"] == student_id
        ]
        
        if not student_records:
            return {"error": "No mastery records found"}
        
        # Calculate mastery statistics
        total_tps = len(student_records)
        mastered_count = sum(
            1 for record in student_records
            if record["mastery_level"] in [TPMasteryLevel.MENGUASAI.value, TPMasteryLevel.SANGAT_MENGUASAI.value]
        )
        very_mastered_count = sum(
            1 for record in student_records
            if record["mastery_level"] == TPMasteryLevel.SANGAT_MENGUASAI.value
        )
        
        # Calculate average mastery score
        avg_mastery_score = sum(record["mastery_score"] for record in student_records) / total_tps
        
        return {
            "student_id": student_id,
            "fase": fase,
            "mata_pelajaran": mata_pelajaran,
            "total_tps": total_tps,
            "mastered_count": mastered_count,
            "mastery_rate": mastered_count / total_tps if total_tps > 0 else 0,
            "very_mastered_count": very_mastered_count,
            "average_mastery_score": avg_mastery_score,
            "mastery_distribution": self._calculate_mastery_distribution(student_records),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def identify_mastery_gaps(
        self, 
        student_id: str,
        tps: List[Dict]
    ) -> List[Dict]:
        """Identify TPs where student has not achieved mastery"""
        gaps = []
        
        for tp in tps:
            mastery = self.get_mastery(student_id, tp["tp_id"])
            
            if not mastery or mastery["mastery_level"] != TPMasteryLevel.SANGAT_MENGUASAI.value:
                gaps.append({
                    "tp_id": tp["tp_id"],
                    "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
                    "current_mastery": mastery["mastery_level"] if mastery else TPMasteryLevel.BELUM_MENGUASAI.value,
                    "current_score": mastery["mastery_score"] if mastery else 0.0,
                    "target_mastery": TPMasteryLevel.SANGAT_MENGUASAI.value,
                    "gap": 1.0 - (mastery["mastery_score"] if mastery else 0.0)
                })
        
        return sorted(gaps, key=lambda x: x["gap"], reverse=True)
    
    def recommend_mastery_activities(
        self, 
        student_id: str,
        tp_id: str,
        current_mastery: str
    ) -> List[Dict]:
        """Recommend activities to improve mastery"""
        activities = []
        
        if current_mastery == TPMasteryLevel.BELUM_MENGUASAI.value:
            activities = [
                {
                    "activity": "Remedial dasar",
                    "description": "Ulang materi dari awal dengan pendekatan sederhana",
                    "duration": "30 menit",
                    "resources": ["buku teks dasar", "video pembelajaran"]
                },
                {
                    "activity": "Latihan terbimbing",
                    "description": "Latihan soal dengan bimbingan guru",
                    "duration": "20 menit",
                    "resources": ["lembar kerja", "kunci jawaban"]
                }
            ]
        elif current_mastery == TPMasteryLevel.SEDANG_MENGUASAI.value:
            activities = [
                {
                    "activity": "Penguatan konsep",
                    "description": "Fokus pada konsep yang belum dipahami",
                    "duration": "25 menit",
                    "resources": ["buku teks", "contoh soal"]
                },
                {
                    "activity": "Praktik mandiri",
                    "description": "Latihan soal tingkat sedang",
                    "duration": "20 menit",
                    "resources": ["lembar kerja"]
                }
            ]
        elif current_mastery == TPMasteryLevel.MENGUASAI.value:
            activities = [
                {
                    "activity": "Pengayaan",
                    "description": "Soal tingkat lanjut untuk memperdalam pemahaman",
                    "duration": "20 menit",
                    "resources": ["buku pengayaan", "soal tantangan"]
                },
                {
                    "activity": "Peer teaching",
                    "description": "Mengajarkan konsep kepada teman",
                    "duration": "15 menit",
                    "resources": ["materi ajar"]
                }
            ]
        
        return activities
    
    def track_mastery_progression(
        self, 
        student_id: str,
        tp_id: str
    ) -> List[Dict]:
        """Track mastery progression over time"""
        # In a real implementation, this would query historical data
        # For now, return current mastery record
        mastery = self.get_mastery(student_id, tp_id)
        
        if not mastery:
            return []
        
        return [
            {
                "date": mastery["assessed_at"],
                "mastery_level": mastery["mastery_level"],
                "mastery_score": mastery["mastery_score"]
            }
        ]
    
    def _calculate_mastery_score(self, assessment_results: List[Dict]) -> float:
        """Calculate mastery score from assessment results"""
        if not assessment_results:
            return 0.0
        
        total_score = 0
        total_weight = 0
        
        for result in assessment_results:
            score = result.get("score", 0)
            weight = result.get("weight", 1)
            max_score = result.get("max_score", 100)
            
            normalized_score = (score / max_score) if max_score > 0 else 0
            total_score += normalized_score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _determine_mastery_level(self, mastery_score: float) -> TPMasteryLevel:
        """Determine mastery level from score"""
        if mastery_score >= 0.9:
            return TPMasteryLevel.SANGAT_MENGUASAI
        elif mastery_score >= 0.7:
            return TPMasteryLevel.MENGUASAI
        elif mastery_score >= 0.5:
            return TPMasteryLevel.SEDANG_MENGUASAI
        else:
            return TPMasteryLevel.BELUM_MENGUASAI
    
    def _calculate_mastery_distribution(self, records: List[Dict]) -> Dict:
        """Calculate distribution of mastery levels"""
        distribution = {
            TPMasteryLevel.BELUM_MENGUASAI.value: 0,
            TPMasteryLevel.SEDANG_MENGUASAI.value: 0,
            TPMasteryLevel.MENGUASAI.value: 0,
            TPMasteryLevel.SANGAT_MENGUASAI.value: 0
        }
        
        for record in records:
            level = record["mastery_level"]
            distribution[level] += 1
        
        return distribution
    
    def _initialize_mastery_criteria(self) -> Dict:
        """Initialize mastery criteria"""
        return {
            TPMasteryLevel.BELUM_MENGUASAI.value: {"min": 0.0, "max": 0.5},
            TPMasteryLevel.SEDANG_MENGUASAI.value: {"min": 0.5, "max": 0.7},
            TPMasteryLevel.MENGUASAI.value: {"min": 0.7, "max": 0.9},
            TPMasteryLevel.SANGAT_MENGUASAI.value: {"min": 0.9, "max": 1.0}
        }
    
    def generate_mastery_report(
        self, 
        student_id: str,
        tps: List[Dict],
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Generate comprehensive mastery report"""
        summary = self.get_student_mastery_summary(student_id, fase, mata_pelajaran)
        gaps = self.identify_mastery_gaps(student_id, tps)
        
        return {
            "student_id": student_id,
            "fase": fase,
            "mata_pelajaran": mata_pelajaran,
            "mastery_summary": summary,
            "mastery_gaps": gaps,
            "recommendations": [
                self.recommend_mastery_activities(
                    student_id, 
                    gap["tp_id"], 
                    gap["current_mastery"]
                )
                for gap in gaps[:3]
            ],
            "generated_at": datetime.utcnow().isoformat()
        }
