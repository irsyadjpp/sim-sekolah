"""
Bloom Semantic Classifier
Advanced Bloom taxonomy classification based on semantic understanding and activity types
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import re
from app.models.chunk_types import BloomLevel


class CognitiveActivity(Enum):
    """Types of cognitive activities for Bloom classification"""
    RECALL = "recall"                   # Simple recall and memorization
    COMPREHENSION = "comprehension"     # Understanding and explaining
    APPLICATION = "application"         # Using knowledge in new situations
    ANALYSIS = "analysis"               # Breaking down and examining
    EVALUATION = "evaluation"           # Judging and assessing
    SYNTHESIS = "synthesis"             # Creating and combining


@dataclass
class BloomIndicators:
    """Bloom level indicators extracted from text"""
    text: str
    level_indicators: Dict[str, int] = field(default_factory=dict)
    activity_type: Optional[str] = None
    cognitive_complexity: str = "basic"
    
    # Specific indicator counts
    recall_indicators: int = 0
    comprehension_indicators: int = 0
    application_indicators: int = 0
    analysis_indicators: int = 0
    evaluation_indicators: int = 0
    synthesis_indicators: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "level_indicators": self.level_indicators,
            "activity_type": self.activity_type,
            "cognitive_complexity": self.cognitive_complexity,
            "recall_indicators": self.recall_indicators,
            "comprehension_indicators": self.comprehension_indicators,
            "application_indicators": self.application_indicators,
            "analysis_indicators": self.analysis_indicators,
            "evaluation_indicators": self.evaluation_indicators,
            "synthesis_indicators": self.synthesis_indicators
        }


class BloomSemanticClassifier:
    """Semantic classifier for Bloom taxonomy with activity-based inference"""
    
    def __init__(self):
        # Indonesian Bloom taxonomy indicators
        self.recall_patterns = [
            r'\b(mengingat|menyebutkan|mendaftar|menyebut\s+namanya|menyebut\s+semua|mengidentifikasi|mengenali)\b',
            r'\b(apa|siapa|di mana|kapan|bagaimana)\s+(namanya|itu|nya)\b',
            r'\b(tuliskan|sebutkan|namun)\s+(semua|semua\s+ini)\b'
        ]
        
        self.comprehension_patterns = [
            r'\b(menjelaskan|menguraikan|menginterpretasikan|memberi contoh|menggambarkan|menggeneralisasi)\b',
            r'\b(memahami|mengerti|mengenal|menghayati)\b',
            r'\b(jelaskan|uraikan|gambarkan|ilustrasikan)\b'
        ]
        
        self.application_patterns = [
            r'\b(menggunakan|menerapkan|mempraktekkan|mendemonstrasikan|mengimplementasikan|mengoperasikan)\b',
            r'\b(perbuat|kerjakan|lakukan|gunakan|terapkan)\b',
            r'\b(eksperimen|praktikum|latihan|penerapan)\b'
        ]
        
        self.analysis_patterns = [
            r'\b(menganalisis|menguraikan|mengelompokkan|mengklasifikasikan|mengidentifikasi|membedakan)\b',
            r'\b(bandingkan|hubungkan|pilih|tetapkan)\b',
            r'\b(analisis|bedakan|pilih|kategorikan)\b'
        ]
        
        self.evaluation_patterns = [
            r'\b(menilai|mengukur|mengevaluasi|menghakimi|mempertimbangkan)\b',
            r'\b(pilih|tentukan|pertimbangkan|berikan\s+pendapat)\b',
            r'\b(mengapa\?|apakah\s+sesuai\?|seberapa\s+baik\?)\b'
        ]
        
        self.synthesis_patterns = [
            r'\b(mencipta|merancang|menyusun|mengkonstruksi|mengembangkan|mengubah)\b',
            r'\b(buat|desain|susun|kembangkan)\b',
            r'\b(proyek|karya\s+tulis|inovasi)\b'
        ]
        
        # Activity-based Bloom inference mapping
        self.activity_bloom_mapping = {
            'experiment': BloomLevel.C3_APPLY,              # Eksperimen → Apply
            'exploration': BloomLevel.C4_ANALYZE,            # Eksplorasi → Analyze
            'discussion': BloomLevel.C4_ANALYZE,             # Diskusi → Analyze
            'reflection': BloomLevel.C5_EVALUATE,            # Refleksi → Evaluate
            'project': BloomLevel.C6_CREATE,                 # Proyek → Create
            'assessment': BloomLevel.C4_ANALYZE,             # Assessment → Analyze
            'evaluation': BloomLevel.C5_EVALUATE,            # Evaluation → Evaluate
            'quiz': BloomLevel.C2_UNDERSTAND,               # Quiz → Understand
            'exercise': BloomLevel.C3_APPLY,                 # Exercise → Apply
            'inquiry': BloomLevel.C4_ANALYZE,                # Inquiry → Analyze
            'collaboration': BloomLevel.C3_APPLY,           # Kolaborasi → Apply
        }
        
        # Content-based Bloom inference
        self.content_bloom_mapping = {
            # Basic content types
            'definition': BloomLevel.C1_REMEMBER,
            'introduction': BloomLevel.C1_REMEMBER,
            'concept': BloomLevel.C2_UNDERSTAND,
            
            # Process content
            'process': BloomLevel.C2_UNDERSTAND,
            'step-by-step': BloomLevel.C3_APPLY,
            'procedure': BloomLevel.C3_APPLY,
            
            # Advanced content
            'analysis': BloomLevel.C4_ANALYZE,
            'comparison': BloomLevel.C4_ANALYZE,
            'evaluation': BloomLevel.C5_EVALUATE,
            'creative': BloomLevel.C6_CREATE
        }
    
    def extract_bloom_indicators(self, text: str, chunk_type: str) -> BloomIndicators:
        """Extract Bloom level indicators from text"""
        text_lower = text.lower()
        
        indicators = BloomIndicators(text=text)
        
        # Count recall indicators (C1)
        for pattern in self.recall_patterns:
            matches = len(re.findall(pattern, text_lower))
            indicators.recall_indicators += matches
        indicators.level_indicators['recall'] = indicators.recall_indicators
        
        # Count comprehension indicators (C2)
        for pattern in self.comprehension_patterns:
            matches = len(re.findall(pattern, text_lower))
            indicators.comprehension_indicators += matches
        indicators.level_indicators['comprehension'] = indicators.comprehension_indicators
        
        # Count application indicators (C3)
        for pattern in self.application_patterns:
            matches = len(re.findall(pattern, text_lower))
            indicators.application_indicators += matches
        indicators.level_indicators['application'] = indicators.application_indicators
        
        # Count analysis indicators (C4)
        for pattern in self.analysis_patterns:
            matches = len(re.findall(pattern, text_lower))
            indicators.analysis_indicators += matches
        indicators.level_indicators['analysis'] = indicators.analysis_indicators
        
        # Count evaluation indicators (C5)
        for pattern in self.evaluation_patterns:
            matches = len(re.findall(pattern, text_lower))
            indicators.evaluation_indicators += matches
        indicators.level_indicators['evaluation'] = indicators.evaluation_indicators
        
        # Count synthesis indicators (C6)
        for pattern in self.synthesis_patterns:
            matches = len(re.findall(pattern, text_lower))
            indicators.synthesis_indicators += matches
        indicators.level_indicators['synthesis'] = indicators.synthesis_indicators
        
        # Determine activity type from chunk type
        indicators.activity_type = self._determine_activity_type(chunk_type, text_lower)
        
        # Determine cognitive complexity
        indicators.cognitive_complexity = self._determine_cognitive_complexity(indicators)
        
        return indicators
    
    def _determine_activity_type(self, chunk_type: str, text_lower: str) -> Optional[str]:
        """Determine activity type from chunk type and text"""
        chunk_type_lower = chunk_type.lower()
        
        # Direct mapping from chunk type to activity
        if 'experiment' in chunk_type_lower or 'eksperimen' in text_lower:
            return 'experiment'
        elif 'exploration' in chunk_type_lower or 'eksplorasi' in text_lower:
            return 'exploration'
        elif 'discussion' in chunk_type_lower or 'diskusi' in text_lower:
            return 'discussion'
        elif 'reflection' in chunk_type_lower or 'refleksi' in text_lower:
            return 'reflection'
        elif 'project' in chunk_type_lower or 'proyek' in text_lower:
            return 'project'
        elif 'assessment' in chunk_type_lower or 'soal' in text_lower:
            return 'assessment'
        elif 'evaluation' in chunk_type_lower or 'evaluasi' in text_lower:
            return 'evaluation'
        elif 'quiz' in chunk_type_lower or 'kuis' in text_lower:
            return 'quiz'
        elif 'exercise' in chunk_type_lower or 'latihan' in text_lower:
            return 'exercise'
        elif 'inquiry' in chunk_type_lower or 'inquiry' in text_lower:
            return 'inquiry'
        elif 'collaboration' in chunk_type_lower or 'kolaborasi' in text_lower:
            return 'collaboration'
        
        return None
    
    def _determine_cognitive_complexity(self, indicators: BloomIndicators) -> str:
        """Determine overall cognitive complexity"""
        # Calculate weighted score
        score = (
            indicators.recall_indicators * 1 +
            indicators.comprehension_indicators * 2 +
            indicators.application_indicators * 3 +
            indicators.analysis_indicators * 4 +
            indicators.evaluation_indicators * 5 +
            indicators.synthesis_indicators * 6
        )
        
        # Determine complexity level
        if score <= 2:
            return "basic"
        elif score <= 4:
            return "intermediate"
        elif score <= 8:
            return "advanced"
        else:
            return "expert"
    
    def classify_bloom_semantic(self, text: str, chunk_type: str, metadata: Dict[str, Any]) -> Tuple[BloomLevel, float, BloomIndicators]:
        """
        Classify Bloom level using semantic analysis with activity-based inference
        
        Args:
            text: Text content to classify
            chunk_type: Type of chunk
            metadata: Document metadata
            
        Returns:
            Tuple of (bloom_level, confidence, indicators)
        """
        indicators = self.extract_bloom_indicators(text, chunk_type)
        
        # Method 1: Activity-based inference (highest priority)
        if indicators.activity_type:
            activity_bloom = self.activity_bloom_mapping.get(indicators.activity_type)
            if activity_bloom:
                return activity_bloom, 0.85, indicators  # High confidence for activity-based
        
        # Method 2: Indicator-based classification
        total_indicators = sum([
            indicators.recall_indicators,
            indicators.comprehension_indicators,
            indicators.application_indicators,
            indicators.analysis_indicators,
            indicators.evaluation_indicators,
            indicators.synthesis_indicators
        ])
        
        if total_indicators == 0:
            # No indicators found, use content-based inference
            content_bloom = self._content_based_inference(chunk_type, text)
            return content_bloom, 0.6, indicators
        
        # Find dominant level
        level_scores = {
            BloomLevel.C1_REMEMBER: indicators.recall_indicators,
            BloomLevel.C2_UNDERSTAND: indicators.comprehension_indicators,
            BloomLevel.C3_APPLY: indicators.application_indicators,
            BloomLevel.C4_ANALYZE: indicators.analysis_indicators,
            BloomLevel.C5_EVALUATE: indicators.evaluation_indicators,
            BloomLevel.C6_CREATE: indicators.synthesis_indicators
        }
        
        dominant_level = max(level_scores.items(), key=lambda x: x[1])
        
        # Calculate confidence based on dominance
        max_score = dominant_level[1]
        confidence = min(max_score / total_indicators + 0.3, 0.9)
        
        return dominant_level[0], confidence, indicators
    
    def _content_based_inference(self, chunk_type: str, text: str) -> BloomLevel:
        """Infer Bloom level based on content type and text patterns"""
        chunk_type_lower = chunk_type.lower()
        text_lower = text.lower()
        
        # Check for definition/introduction content
        if any(word in chunk_type_lower for word in ['definition', 'intro', 'cover']):
            return BloomLevel.C1_REMEMBER
        
        # Check for concept explanation
        if 'concept' in chunk_type_lower:
            # Check if it's basic understanding or deeper
            if any(word in text_lower for word in ['mengapa', 'bagaimana', 'analisis', 'hubungan']):
                return BloomLevel.C4_ANALYZE
            else:
                return BloomLevel.C2_UNDERSTAND
        
        # Check for process explanation
        if 'process' in chunk_type_lower:
            return BloomLevel.C2_UNDERSTAND
        
        # Check for step-by-step instructions
        if re.search(r'^\s*\d+\.', text, re.MULTILINE):
            return BloomLevel.C3_APPLY
        
        # Default to understanding
        return BloomLevel.C2_UNDERSTAND