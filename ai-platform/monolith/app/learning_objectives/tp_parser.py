"""
TP Parser

This module parses Tujuan Pembelajaran (TP) from various sources including
CP (Capaian Pembelajaran), curriculum documents, and teacher input.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import re


class TPSource(str, Enum):
    """Sources for TP data"""
    CP_DERIVED = "cp_derived"
    MANUAL_INPUT = "manual_input"
    CURRICULUM_DOCUMENT = "curriculum_document"
    AI_GENERATED = "ai_generated"


class TPDifficulty(str, Enum):
    """TP difficulty levels"""
    MUDAH = "mudah"
    SEDANG = "sedang"
    SULIT = "sulit"


class TPDomain(str, Enum):
    """TP domains according to Kurikulum Merdeka"""
    KOGNITIF = "kognitif"
    PSIKOMOTORIK = "psikomotorik"
    AFECTIF = "afektif"


class TPParser:
    """Parser for Tujuan Pembelajaran (Learning Objectives)"""
    
    def __init__(self):
        self.tp_patterns = self._initialize_tp_patterns()
        self.verb_taxonomy = self._initialize_verb_taxonomy()
    
    def parse_from_cp(
        self, 
        cp_data: Dict,
        fase: str,
        mata_pelajaran: str
    ) -> List[Dict]:
        """Parse TP from CP (Capaian Pembelajaran)"""
        cp_elements = cp_data.get("elements", [])
        
        tps = []
        for i, element in enumerate(cp_elements):
            tp = {
                "tp_id": f"TP_{fase}_{mata_pelajaran}_{i+1}",
                "fase": fase,
                "mata_pelajaran": mata_pelajaran,
                "cp_id": element.get("cp_id", ""),
                "elemen_cp": element.get("elemen", ""),
                "tujuan_pembelajaran": self._derive_tp_from_element(element),
                "domain": self._determine_domain(element),
                "difficulty": self._determine_difficulty(element),
                "source": TPSource.CP_DERIVED.value,
                "created_at": datetime.utcnow().isoformat()
            }
            tps.append(tp)
        
        return tps
    
    def parse_from_text(
        self, 
        text: str,
        fase: str,
        mata_pelajaran: str
    ) -> List[Dict]:
        """Parse TP from free text input"""
        sentences = self._split_into_sentences(text)
        
        tps = []
        for i, sentence in enumerate(sentences):
            if self._is_valid_tp(sentence):
                tp = {
                    "tp_id": f"TP_{fase}_{mata_pelajaran}_{i+1}",
                    "fase": fase,
                    "mata_pelajaran": mata_pelajaran,
                    "tujuan_pembelajaran": sentence,
                    "domain": self._determine_domain_from_text(sentence),
                    "difficulty": self._determine_difficulty_from_text(sentence),
                    "source": TPSource.MANUAL_INPUT.value,
                    "created_at": datetime.utcnow().isoformat()
                }
                tps.append(tp)
        
        return tps
    
    def parse_from_curriculum_document(
        self, 
        document_content: str,
        fase: str,
        mata_pelajaran: str
    ) -> List[Dict]:
        """Parse TP from curriculum document"""
        tp_patterns = self.tp_patterns["curriculum_document"]
        
        tps = []
        matches = re.finditer(tp_patterns, document_content, re.MULTILINE | re.IGNORECASE)
        
        for i, match in enumerate(matches):
            tp_text = match.group(1).strip()
            tp = {
                "tp_id": f"TP_{fase}_{mata_pelajaran}_{i+1}",
                "fase": fase,
                "mata_pelajaran": mata_pelajaran,
                "tujuan_pembelajaran": tp_text,
                "domain": self._determine_domain_from_text(tp_text),
                "difficulty": self._determine_difficulty_from_text(tp_text),
                "source": TPSource.CURRICULUM_DOCUMENT.value,
                "created_at": datetime.utcnow().isoformat()
            }
            tps.append(tp)
        
        return tps
    
    def generate_tp_from_cp_ai(
        self, 
        cp_data: Dict,
        fase: str,
        mata_pelajaran: str,
        jumlah_tp: int = 5
    ) -> List[Dict]:
        """Generate TP from CP using AI (placeholder for AI integration)"""
        cp_elements = cp_data.get("elements", [])
        
        tps = []
        for i in range(min(jumlah_tp, len(cp_elements))):
            element = cp_elements[i]
            tp = {
                "tp_id": f"TP_{fase}_{mata_pelajaran}_{i+1}",
                "fase": fase,
                "mata_pelajaran": mata_pelajaran,
                "cp_id": element.get("cp_id", ""),
                "elemen_cp": element.get("elemen", ""),
                "tujuan_pembelajaran": self._ai_generate_tp_from_element(element),
                "domain": self._determine_domain(element),
                "difficulty": self._determine_difficulty(element),
                "source": TPSource.AI_GENERATED.value,
                "created_at": datetime.utcnow().isoformat(),
                "ai_generated": True
            }
            tps.append(tp)
        
        return tps
    
    def _derive_tp_from_element(self, element: Dict) -> str:
        """Derive TP from CP element"""
        elemen_cp = element.get("elemen", "")
        
        # Convert CP element to TP by making it more specific and actionable
        # This is a simplified version - in production, this would use AI
        tp_templates = [
            f"Siswa mampu {elemen_cp.lower()}",
            f"Siswa dapat {elemen_cp.lower()}",
            f"Peserta didik mampu {elemen_cp.lower()}",
            f"Peserta didik dapat {elemen_cp.lower()}"
        ]
        
        # Select appropriate template based on element characteristics
        return tp_templates[0]  # Simplified selection
    
    def _ai_generate_tp_from_element(self, element: Dict) -> str:
        """Generate TP from CP element using AI (placeholder)"""
        elemen_cp = element.get("elemen", "")
        
        # Placeholder for AI generation
        # In production, this would call an LLM to generate specific TPs
        return f"Siswa mampu {elemen_cp.lower()} dengan bimbingan minimal"
    
    def _determine_domain(self, element: Dict) -> str:
        """Determine domain (kognitif, psikomotorik, afektif) from element"""
        elemen_cp = element.get("elemen", "").lower()
        
        kognitif_keywords = ["memahami", "menganalisis", "mengevaluasi", "mengerti", "mengenal"]
        psikomotorik_keywords = ["melakukan", "menerapkan", "menyusun", "membuat", "mengoperasikan"]
        afektif_keywords = ["menghargai", "menyukai", "menghormati", "peduli", "berperilaku"]
        
        for keyword in kognitif_keywords:
            if keyword in elemen_cp:
                return TPDomain.KOGNITIF.value
        
        for keyword in psikomotorik_keywords:
            if keyword in elemen_cp:
                return TPDomain.PSIKOMOTORIK.value
        
        for keyword in afektif_keywords:
            if keyword in elemen_cp:
                return TPDomain.AFECTIF.value
        
        return TPDomain.KOGNITIF.value  # Default
    
    def _determine_domain_from_text(self, text: str) -> str:
        """Determine domain from text"""
        return self._determine_domain({"elemen": text})
    
    def _determine_difficulty(self, element: Dict) -> str:
        """Determine difficulty level from element"""
        elemen_cp = element.get("elemen", "").lower()
        
        # Simple heuristic based on complexity indicators
        complexity_indicators = {
            "mudah": ["mengenal", "mengingat", "menyebutkan"],
            "sedang": ["memahami", "menjelaskan", "mengidentifikasi"],
            "sulit": ["menganalisis", "mengevaluasi", "mengkreasi", "merancang"]
        }
        
        for level, keywords in complexity_indicators.items():
            for keyword in keywords:
                if keyword in elemen_cp:
                    return level
        
        return TPDifficulty.SEDANG.value  # Default
    
    def _determine_difficulty_from_text(self, text: str) -> str:
        """Determine difficulty from text"""
        return self._determine_difficulty({"elemen": text})
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting - in production, use NLP library
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _is_valid_tp(self, sentence: str) -> bool:
        """Check if sentence is a valid TP"""
        # Valid TP should start with a verb and be actionable
        verb_patterns = [
            r'^(mampu|dapat|harus|akan)',
            r'^(siswa|peserta didik|murid)',
            r'^(men|meng|mem|me)'
        ]
        
        for pattern in verb_patterns:
            if re.match(pattern, sentence, re.IGNORECASE):
                return True
        
        return len(sentence.split()) >= 3  # Minimum length check
    
    def _initialize_tp_patterns(self) -> Dict:
        """Initialize regex patterns for TP parsing"""
        return {
            "curriculum_document": r'(?:tujuan pembelajaran|tp|learning objective)[:\s]+(.+?)(?:\n|$)',
            "numbered_list": r'^\d+\.\s+(.+)$',
            "bullet_point": r'^[-*•]\s+(.+)$'
        }
    
    def _initialize_verb_taxonomy(self) -> Dict:
        """Initialize verb taxonomy for TP classification"""
        return {
            "kognitif": {
                "low": ["mengingat", "mengidentifikasi", "menyebutkan", "mengenali"],
                "medium": ["memahami", "menjelaskan", "menginterpretasi", "menggambarkan"],
                "high": ["menganalisis", "mengevaluasi", "mengkreasi", "merancang"]
            },
            "psikomotorik": {
                "low": ["meniru", "mengamati", "menirukan"],
                "medium": ["melakukan", "menerapkan", "menyusun", "mengoperasikan"],
                "high": ["menginovasi", "mengembangkan", "merancang", "mengkreasi"]
            },
            "afektif": {
                "low": ["menerima", "menyadari", "menghargai"],
                "medium": ["menyukai", "menghormati", "peduli", "berpartisipasi"],
                "high": ["menginternalisasi", "mengamalkan", "mempraktikkan", "mempromosikan"]
            }
        }
    
    def classify_tp_verb(self, tp_text: str) -> Dict:
        """Classify the verb in TP according to Bloom's taxonomy"""
        tp_lower = tp_text.lower()
        
        for domain, levels in self.verb_taxonomy.items():
            for level, verbs in levels.items():
                for verb in verbs:
                    if verb in tp_lower:
                        return {
                            "domain": domain,
                            "level": level,
                            "verb": verb
                        }
        
        return {
            "domain": "kognitif",
            "level": "medium",
            "verb": "memahami"  # Default
        }
    
    def validate_tp_structure(self, tp: Dict) -> Dict:
        """Validate TP structure according to Kurikulum Merdeka standards"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        required_fields = ["tp_id", "fase", "mata_pelajaran", "tujuan_pembelajaran", "domain"]
        for field in required_fields:
            if field not in tp or not tp[field]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Missing required field: {field}")
        
        # Check TP text quality
        tp_text = tp.get("tujuan_pembelajaran", "")
        if len(tp_text) < 10:
            validation_result["valid"] = False
            validation_result["errors"].append("TP text too short")
        
        if len(tp_text) > 200:
            validation_result["warnings"].append("TP text too long, consider splitting")
        
        # Check domain validity
        valid_domains = [d.value for d in TPDomain]
        if tp.get("domain") not in valid_domains:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Invalid domain: {tp.get('domain')}")
        
        return validation_result
