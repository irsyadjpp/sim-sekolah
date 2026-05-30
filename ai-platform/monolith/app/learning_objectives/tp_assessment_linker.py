"""
TP Assessment Linker

This module links Tujuan Pembelajaran (TP) to assessment items and rubrics.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class AssessmentType(str, Enum):
    """Types of assessments"""
    FORMATIF = "formatif"
    SUMATIF = "sumatif"
    DIAGNOSTIK = "diagnostik"
    KINERJA = "kinerja"


class TPAssessmentLinker:
    """Linker for TP to assessment items"""
    
    def __init__(self):
        self.linkage_rules = self._initialize_linkage_rules()
    
    def link_tp_to_assessment(
        self, 
        tp: Dict,
        assessment_type: AssessmentType = AssessmentType.FORMATIF
    ) -> Dict:
        """Link a TP to assessment items"""
        assessment_items = self._generate_assessment_items(tp, assessment_type)
        
        linkage = {
            "linkage_id": f"LINK_{tp['tp_id']}_{assessment_type.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "tp_id": tp["tp_id"],
            "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
            "domain": tp.get("domain", "kognitif"),
            "difficulty": tp.get("difficulty", "sedang"),
            "assessment_type": assessment_type.value,
            "assessment_items": assessment_items,
            "rubric": self._generate_rubric(tp, assessment_type),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return linkage
    
    def link_tp_batch_to_assessment(
        self, 
        tps: List[Dict],
        assessment_type: AssessmentType = AssessmentType.FORMATIF
    ) -> List[Dict]:
        """Link multiple TPs to assessment items"""
        linkages = []
        
        for tp in tps:
            linkage = self.link_tp_to_assessment(tp, assessment_type)
            linkages.append(linkage)
        
        return linkages
    
    def generate_assessment_blueprint(
        self, 
        tps: List[Dict],
        assessment_type: AssessmentType = AssessmentType.SUMATIF,
        jumlah_soal: int = 10
    ) -> Dict:
        """Generate assessment blueprint from TPs"""
        # Distribute questions across TPs
        tp_distribution = self._distribute_questions(tps, jumlah_soal)
        
        blueprint = {
            "blueprint_id": f"BP_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "assessment_type": assessment_type.value,
            "total_questions": jumlah_soal,
            "tp_distribution": tp_distribution,
            "assessment_structure": self._generate_assessment_structure(tp_distribution),
            "rubric_overview": self._generate_rubric_overview(tps),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return blueprint
    
    def align_tp_with_rubric(
        self, 
        tp: Dict,
        rubric: Dict
    ) -> Dict:
        """Align TP with rubric criteria"""
        alignment = {
            "tp_id": tp["tp_id"],
            "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
            "rubric_id": rubric.get("rubric_id", ""),
            "alignment_score": self._calculate_rubric_alignment(tp, rubric),
            "aligned_criteria": self._align_criteria(tp, rubric),
            "alignment_recommendations": self._generate_alignment_recommendations(tp, rubric),
            "aligned_at": datetime.utcnow().isoformat()
        }
        
        return alignment
    
    def _generate_assessment_items(
        self, 
        tp: Dict, 
        assessment_type: AssessmentType
    ) -> List[Dict]:
        """Generate assessment items from TP"""
        items = []
        
        domain = tp.get("domain", "kognitif")
        difficulty = tp.get("difficulty", "sedang")
        
        # Determine item type based on domain and assessment type
        item_type = self._determine_item_type(domain, assessment_type)
        
        # Generate items based on difficulty
        num_items = self._determine_num_items(difficulty, assessment_type)
        
        for i in range(num_items):
            item = {
                "item_id": f"ITEM_{tp['tp_id']}_{i+1}",
                "tp_id": tp["tp_id"],
                "item_type": item_type,
                "difficulty": difficulty,
                "question": self._generate_question(tp, i),
                "expected_answer": self._generate_expected_answer(tp),
                "scoring_guide": self._generate_scoring_guide(tp),
                "max_score": self._determine_max_score(difficulty, item_type)
            }
            items.append(item)
        
        return items
    
    def _generate_rubric(
        self, 
        tp: Dict, 
        assessment_type: AssessmentType
    ) -> Dict:
        """Generate rubric for TP assessment"""
        rubric = {
            "rubric_id": f"RUBRIC_{tp['tp_id']}_{assessment_type.value}",
            "tp_id": tp["tp_id"],
            "assessment_type": assessment_type.value,
            "criteria": self._generate_rubric_criteria(tp),
            "performance_levels": self._generate_performance_levels(),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return rubric
    
    def _distribute_questions(self, tps: List[Dict], total_questions: int) -> Dict:
        """Distribute questions across TPs"""
        distribution = {}
        
        if not tps:
            return distribution
        
        # Simple equal distribution - in production, use more sophisticated logic
        questions_per_tp = total_questions // len(tps)
        remainder = total_questions % len(tps)
        
        for i, tp in enumerate(tps):
            num_questions = questions_per_tp + (1 if i < remainder else 0)
            distribution[tp["tp_id"]] = {
                "tp_id": tp["tp_id"],
                "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
                "num_questions": num_questions,
                "difficulty": tp.get("difficulty", "sedang")
            }
        
        return distribution
    
    def _generate_assessment_structure(self, distribution: Dict) -> List[Dict]:
        """Generate assessment structure from distribution"""
        structure = []
        
        for tp_id, data in distribution.items():
            structure.append({
                "section": f"Bagian {len(structure) + 1}",
                "tp_id": tp_id,
                "num_questions": data["num_questions"],
                "difficulty": data["difficulty"],
                "time_allocation": self._calculate_time_allocation(data["num_questions"], data["difficulty"])
            })
        
        return structure
    
    def _generate_rubric_overview(self, tps: List[Dict]) -> Dict:
        """Generate rubric overview for multiple TPs"""
        return {
            "total_criteria": len(tps),
            "domains": list(set(tp.get("domain", "kognitif") for tp in tps)),
            "difficulty_levels": list(set(tp.get("difficulty", "sedang") for tp in tps))
        }
    
    def _calculate_rubric_alignment(self, tp: Dict, rubric: Dict) -> float:
        """Calculate alignment score between TP and rubric"""
        # Simplified alignment calculation
        tp_text = tp["tujuan_pembelajaran"]
        criteria = rubric.get("criteria", [])
        
        if not criteria:
            return 0.0
        
        aligned_count = 0
        for criterion in criteria:
            criterion_text = criterion.get("description", "")
            if self._text_overlap(tp_text, criterion_text) > 0.3:
                aligned_count += 1
        
        return aligned_count / len(criteria)
    
    def _align_criteria(self, tp: Dict, rubric: Dict) -> List[Dict]:
        """Align TP with rubric criteria"""
        aligned = []
        
        tp_text = tp["tujuan_pembelajaran"]
        criteria = rubric.get("criteria", [])
        
        for criterion in criteria:
            criterion_text = criterion.get("description", "")
            overlap = self._text_overlap(tp_text, criterion_text)
            
            if overlap > 0.3:
                aligned.append({
                    "criterion_id": criterion.get("criterion_id", ""),
                    "description": criterion_text,
                    "alignment_score": overlap
                })
        
        return aligned
    
    def _generate_alignment_recommendations(self, tp: Dict, rubric: Dict) -> List[str]:
        """Generate recommendations for TP-rubric alignment"""
        recommendations = []
        
        alignment_score = self._calculate_rubric_alignment(tp, rubric)
        
        if alignment_score < 0.5:
            recommendations.append("Rubric criteria should be more closely aligned with TP")
        
        if len(rubric.get("criteria", [])) < 3:
            recommendations.append("Rubric should have more detailed criteria")
        
        if not recommendations:
            recommendations.append("TP and rubric are well aligned")
        
        return recommendations
    
    def _determine_item_type(self, domain: str, assessment_type: AssessmentType) -> str:
        """Determine assessment item type"""
        if assessment_type == AssessmentType.KINERJA:
            return "kinerja"
        
        item_types = {
            "kognitif": ["pilihan_ganda", "isian_singkat", "esai"],
            "psikomotorik": ["kinerja", "demonstrasi"],
            "afektif": ["observasi", "skala sikap"]
        }
        
        domain_types = item_types.get(domain, item_types["kognitif"])
        return domain_types[0]
    
    def _determine_num_items(self, difficulty: str, assessment_type: AssessmentType) -> int:
        """Determine number of assessment items"""
        if assessment_type == AssessmentType.SUMATIF:
            return 3
        elif assessment_type == AssessmentType.FORMATIF:
            return 2
        else:
            return 1
    
    def _generate_question(self, tp: Dict, index: int) -> str:
        """Generate assessment question from TP"""
        tp_text = tp["tujuan_pembelajaran"]
        
        # Simple question generation - in production, use AI
        templates = [
            f"Jelaskan bagaimana {tp_text.lower()}!",
            f"Demonstrasikan kemampuan {tp_text.lower()}!",
            f"Bagaimana kamu {tp_text.lower()}?",
            f"Tunjukkan bukti bahwa kamu {tp_text.lower()}!"
        ]
        
        return templates[index % len(templates)]
    
    def _generate_expected_answer(self, tp: Dict) -> str:
        """Generate expected answer from TP"""
        tp_text = tp["tujuan_pembelajaran"]
        return f"Siswa dapat {tp_text.lower()} dengan benar"
    
    def _generate_scoring_guide(self, tp: Dict) -> Dict:
        """Generate scoring guide for TP"""
        return {
            "excellent": f"Sangat baik dalam {tp['tujuan_pembelajaran'][:30]}...",
            "good": f"Cukup baik dalam {tp['tujuan_pembelajaran'][:30]}...",
            "fair": f"Cukup dalam {tp['tujuan_pembelajaran'][:30]}...",
            "poor": f"Kurang dalam {tp['tujuan_pembelajaran'][:30]}..."
        }
    
    def _determine_max_score(self, difficulty: str, item_type: str) -> int:
        """Determine maximum score for item"""
        base_scores = {
            "mudah": 5,
            "sedang": 10,
            "sulit": 15
        }
        
        type_multipliers = {
            "pilihan_ganda": 1,
            "isian_singkat": 1,
            "esai": 2,
            "kinerja": 3,
            "observasi": 2
        }
        
        base_score = base_scores.get(difficulty, 10)
        multiplier = type_multipliers.get(item_type, 1)
        
        return base_score * multiplier
    
    def _generate_rubric_criteria(self, tp: Dict) -> List[Dict]:
        """Generate rubric criteria from TP"""
        tp_text = tp["tujuan_pembelajaran"]
        
        criteria = [
            {
                "criterion_id": f"CRIT_{tp['tp_id']}_1",
                "description": f"Pemahaman {tp_text[:30]}...",
                "weight": 0.4
            },
            {
                "criterion_id": f"CRIT_{tp['tp_id']}_2",
                "description": f"Penerapan {tp_text[:30]}...",
                "weight": 0.3
            },
            {
                "criterion_id": f"CRIT_{tp['tp_id']}_3",
                "description": f"Komunikasi hasil",
                "weight": 0.3
            }
        ]
        
        return criteria
    
    def _generate_performance_levels(self) -> List[Dict]:
        """Generate performance levels for rubric"""
        return [
            {"level": "4", "description": "Sangat baik", "score_range": "90-100"},
            {"level": "3", "description": "Baik", "score_range": "75-89"},
            {"level": "2", "description": "Cukup", "score_range": "60-74"},
            {"level": "1", "description": "Kurang", "score_range": "0-59"}
        ]
    
    def _calculate_time_allocation(self, num_questions: int, difficulty: str) -> str:
        """Calculate time allocation for assessment section"""
        base_time = num_questions * 5  # 5 minutes per question
        
        difficulty_multipliers = {
            "mudah": 1.0,
            "sedang": 1.2,
            "sulit": 1.5
        }
        
        multiplier = difficulty_multipliers.get(difficulty, 1.2)
        total_time = int(base_time * multiplier)
        
        return f"{total_time} menit"
    
    def _text_overlap(self, text1: str, text2: str) -> float:
        """Calculate text overlap (simplified)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _initialize_linkage_rules(self) -> Dict:
        """Initialize linkage rules"""
        return {
            "max_items_per_tp": 5,
            "min_rubric_criteria": 3,
            "max_rubric_criteria": 5
        }
