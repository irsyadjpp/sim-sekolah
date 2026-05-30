"""
TP Alignment

This module handles alignment of Tujuan Pembelajaran (TP) with CP, ATP,
and Kurikulum Merdeka standards.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class AlignmentType(str, Enum):
    """Types of alignment"""
    CP_ALIGNMENT = "cp_alignment"
    ATP_ALIGNMENT = "atp_alignment"
    STANDARDS_ALIGNMENT = "standards_alignment"
    DEEP_LEARNING_ALIGNMENT = "deep_learning_alignment"


class AlignmentLevel(str, Enum):
    """Alignment levels"""
    NOT_ALIGNED = "not_aligned"
    PARTIALLY_ALIGNED = "partially_aligned"
    ALIGNED = "aligned"
    STRONGLY_ALIGNED = "strongly_aligned"


class TPAlignment:
    """Alignment checker for Tujuan Pembelajaran"""
    
    def __init__(self):
        self.alignment_rules = self._initialize_alignment_rules()
        self.standards_data = self._load_standards_data()
    
    def check_cp_alignment(
        self, 
        tp: Dict,
        cp_data: Dict
    ) -> Dict:
        """Check alignment of TP with CP"""
        tp_text = tp["tujuan_pembelajaran"]
        cp_elements = cp_data.get("elements", [])
        
        alignment_scores = []
        for element in cp_elements:
            score = self._calculate_text_similarity(
                tp_text, 
                element.get("elemen", "")
            )
            alignment_scores.append({
                "cp_id": element.get("cp_id"),
                "elemen": element.get("elemen"),
                "alignment_score": score
            })
        
        # Find best match
        best_match = max(alignment_scores, key=lambda x: x["alignment_score"])
        
        alignment_level = self._determine_alignment_level(best_match["alignment_score"])
        
        return {
            "tp_id": tp["tp_id"],
            "alignment_type": AlignmentType.CP_ALIGNMENT.value,
            "best_match_cp": best_match["cp_id"],
            "alignment_score": best_match["alignment_score"],
            "alignment_level": alignment_level.value,
            "all_alignments": alignment_scores,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    def check_atp_alignment(
        self, 
        tp: Dict,
        atp_data: List[Dict]
    ) -> Dict:
        """Check alignment of TP with ATP"""
        tp_text = tp["tujuan_pembelajaran"]
        
        alignment_scores = []
        for atp in atp_data:
            atp_tps = atp.get("tujuan_pembelajaran", [])
            for atp_tp in atp_tps:
                score = self._calculate_text_similarity(tp_text, atp_tp)
                alignment_scores.append({
                    "atp_id": atp["atp_id"],
                    "periode": atp["periode"],
                    "alignment_score": score
                })
        
        if not alignment_scores:
            return {
                "tp_id": tp["tp_id"],
                "alignment_type": AlignmentType.ATP_ALIGNMENT.value,
                "alignment_level": AlignmentLevel.NOT_ALIGNED.value,
                "message": "No ATP data available"
            }
        
        best_match = max(alignment_scores, key=lambda x: x["alignment_score"])
        alignment_level = self._determine_alignment_level(best_match["alignment_score"])
        
        return {
            "tp_id": tp["tp_id"],
            "alignment_type": AlignmentType.ATP_ALIGNMENT.value,
            "best_match_atp": best_match["atp_id"],
            "best_match_period": best_match["periode"],
            "alignment_score": best_match["alignment_score"],
            "alignment_level": alignment_level.value,
            "all_alignments": alignment_scores,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    def check_standards_alignment(
        self, 
        tp: Dict,
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Check alignment with Kurikulum Merdeka standards"""
        tp_text = tp["tujuan_pembelajaran"]
        domain = tp.get("domain", "kognitif")
        
        # Get relevant standards
        relevant_standards = self._get_relevant_standards(
            fase, 
            mata_pelajaran, 
            domain
        )
        
        alignment_scores = []
        for standard in relevant_standards:
            score = self._calculate_text_similarity(
                tp_text, 
                standard.get("description", "")
            )
            alignment_scores.append({
                "standard_id": standard.get("standard_id"),
                "description": standard.get("description"),
                "alignment_score": score
            })
        
        if not alignment_scores:
            return {
                "tp_id": tp["tp_id"],
                "alignment_type": AlignmentType.STANDARDS_ALIGNMENT.value,
                "alignment_level": AlignmentLevel.NOT_ALIGNED.value,
                "message": "No relevant standards found"
            }
        
        best_match = max(alignment_scores, key=lambda x: x["alignment_score"])
        alignment_level = self._determine_alignment_level(best_match["alignment_score"])
        
        return {
            "tp_id": tp["tp_id"],
            "alignment_type": AlignmentType.STANDARDS_ALIGNMENT.value,
            "best_match_standard": best_match["standard_id"],
            "alignment_score": best_match["alignment_score"],
            "alignment_level": alignment_level.value,
            "all_alignments": alignment_scores,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    def check_deep_learning_alignment(
        self, 
        tp: Dict
    ) -> Dict:
        """Check alignment with Pembelajaran Mendalam principles"""
        tp_text = tp["tujuan_pembelajaran"]
        
        deep_learning_principles = [
            "memahami",
            "mengaplikasi",
            "merefleksi",
            "bermakna",
            "kontekstual",
            "inquiry"
        ]
        
        alignment_scores = {}
        for principle in deep_learning_principles:
            score = self._calculate_text_similarity(tp_text, principle)
            alignment_scores[principle] = score
        
        # Calculate overall alignment
        avg_alignment = sum(alignment_scores.values()) / len(alignment_scores)
        alignment_level = self._determine_alignment_level(avg_alignment)
        
        return {
            "tp_id": tp["tp_id"],
            "alignment_type": AlignmentType.DEEP_LEARNING_ALIGNMENT.value,
            "alignment_score": avg_alignment,
            "alignment_level": alignment_level.value,
            "principle_alignments": alignment_scores,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    def check_comprehensive_alignment(
        self, 
        tp: Dict,
        cp_data: Dict,
        atp_data: List[Dict],
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Check all alignment types for a TP"""
        cp_alignment = self.check_cp_alignment(tp, cp_data)
        atp_alignment = self.check_atp_alignment(tp, atp_data)
        standards_alignment = self.check_standards_alignment(
            tp, fase, mata_pelajaran
        )
        deep_learning_alignment = self.check_deep_learning_alignment(tp)
        
        # Calculate overall alignment score
        scores = [
            cp_alignment.get("alignment_score", 0),
            atp_alignment.get("alignment_score", 0),
            standards_alignment.get("alignment_score", 0),
            deep_learning_alignment.get("alignment_score", 0)
        ]
        
        overall_score = sum(scores) / len(scores)
        overall_level = self._determine_alignment_level(overall_score)
        
        return {
            "tp_id": tp["tp_id"],
            "overall_alignment_score": overall_score,
            "overall_alignment_level": overall_level.value,
            "cp_alignment": cp_alignment,
            "atp_alignment": atp_alignment,
            "standards_alignment": standards_alignment,
            "deep_learning_alignment": deep_learning_alignment,
            "recommendations": self._generate_alignment_recommendations(
                cp_alignment,
                atp_alignment,
                standards_alignment,
                deep_learning_alignment
            ),
            "checked_at": datetime.utcnow().isoformat()
        }
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (simplified)"""
        # In production, use proper NLP similarity metrics
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _determine_alignment_level(self, score: float) -> AlignmentLevel:
        """Determine alignment level from score"""
        if score >= 0.8:
            return AlignmentLevel.STRONGLY_ALIGNED
        elif score >= 0.6:
            return AlignmentLevel.ALIGNED
        elif score >= 0.4:
            return AlignmentLevel.PARTIALLY_ALIGNED
        else:
            return AlignmentLevel.NOT_ALIGNED
    
    def _get_relevant_standards(
        self, 
        fase: str, 
        mata_pelajaran: str, 
        domain: str
    ) -> List[Dict]:
        """Get relevant Kurikulum Merdeka standards"""
        # In production, this would query the standards repository
        # For now, return placeholder data
        return [
            {
                "standard_id": f"STD_{fase}_{mata_pelajaran}_{domain}",
                "description": f"Standar untuk {domain} di fase {fase}"
            }
        ]
    
    def _generate_alignment_recommendations(
        self, 
        cp_alignment: Dict,
        atp_alignment: Dict,
        standards_alignment: Dict,
        deep_learning_alignment: Dict
    ) -> List[str]:
        """Generate recommendations based on alignment results"""
        recommendations = []
        
        if cp_alignment.get("alignment_score", 0) < 0.6:
            recommendations.append("TP perlu diselaraskan lebih baik dengan CP")
        
        if atp_alignment.get("alignment_score", 0) < 0.6:
            recommendations.append("TP perlu dipasangkan ke ATP yang sesuai")
        
        if standards_alignment.get("alignment_score", 0) < 0.6:
            recommendations.append("TP perlu disesuaikan dengan standar Kurikulum Merdeka")
        
        if deep_learning_alignment.get("alignment_score", 0) < 0.6:
            recommendations.append("TP perlu mencakup prinsip Pembelajaran Mendalam")
        
        if not recommendations:
            recommendations.append("TP sudah selaras dengan seluruh standar")
        
        return recommendations
    
    def _initialize_alignment_rules(self) -> Dict:
        """Initialize alignment rules"""
        return {
            "cp_alignment_threshold": 0.6,
            "atp_alignment_threshold": 0.6,
            "standards_alignment_threshold": 0.6,
            "deep_learning_alignment_threshold": 0.6
        }
    
    def _load_standards_data(self) -> Dict:
        """Load Kurikulum Merdeka standards data"""
        # In production, load from standards repository
        return {}
