"""
Enhanced Chunk Classifier
Semantic-aware chunk classification to reduce false positives, especially for assessment over-classification
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import re
from app.models.chunk_types import EducationalChunkType, ChunkImportance


class SemanticIntent(Enum):
    """Semantic intent of chunk content"""
    EXPLANATION = "explanation"           # Explaining concepts
    INSTRUCTION = "instruction"           # Giving instructions/steps
    ASSESSMENT = "assessment"            # Testing understanding
    INQUIRY = "inquiry"                  # Exploratory questions
    REFLECTION = "reflection"            # Reflective thinking
    STRUCTURAL = "structural"             # Document structure
    ENRICHMENT = "enrichment"            # Additional material


@dataclass
class ClassificationFeatures:
    """Features extracted for classification"""
    text: str
    length: int
    word_count: int
    sentence_count: int
    
    # Content features
    has_questions: bool = False
    question_count: int = 0
    question_types: List[str] = field(default_factory=list)
    has_numbers: bool = False
    numbered_list: bool = False
    has_bold_keywords: bool = False
    
    # Assessment-specific features
    has_imperative_verbs: bool = False
    has_test_keywords: bool = False
    has_scoring_indicators: bool = False
    has_answer_key: bool = False
    
    # Explanation-specific features
    has_definition_patterns: bool = False
    has_examples: bool = False
    has_explanations: bool = False
    has_descriptions: bool = False
    
    # Structural features
    has_topic_headers: bool = False
    has_section_markers: bool = False
    is_list_content: bool = False


class EnhancedChunkClassifier:
    """Enhanced classifier with semantic awareness to reduce false positives"""
    
    def __init__(self):
        # Assessment indicators - more restrictive now
        self.assessment_indicators = [
            r'^(soal\s+nomor\s+\d+)',  # Soal nomor 1
            r'^(pertanyaan\s+\d+)',    # Pertanyaan 1
            r'^(nomor\s+\d+\.)',       # 1.
            r'^(pilihan\s+ganda)',     # Pilihan ganda
            r'^(isian\s+singkat)',     # Isian singkat
            r'^(uraian)',               # Uraian
            r'^(jawablah)',             # Jawablah
            r'^(tentukan)',             # Tentukan
            r'^(selesaikan)',           # Selesaikan
            r'^(hitunglah)',           # Hitunglah
            r'^(jelaskan\s+suatu)',    # Jelaskan suatu
            r'^(buatlah\s+lahan)',     # Buatlah lahan
        ]
        
        # Concept explanation indicators
        self.concept_indicators = [
            r'^(topik\s+\d+)',         # Topik 1
            r'^(urain\s+materi)',      # Uraian materi
            r'^(pengertian)',           # Pengertian
            r'^(definisi)',             # Definisi
            r'^(apa\s+itu)',           # Apa itu
            r'^(mengapa)',              # Mengapa
            r'^(bagaimana)',            # Bagaimana
            r'^(adalah)',               # adalah
            r'^(merupakan)',             # merupakan
            r'^(yaitu)',                # yaitu
        ]
        
        # Process explanation indicators
        self.process_indicators = [
            r'^(tahap\s+\d+)',         # Tahap 1
            r'^(langkah\s+\d+)',       # Langkah 1
            r'^(proses)',               # Proses
            r'^(cara)',                 # Cara
            r'^(metode)',               # Metode
            r'^(terjadi)',              # terjadi
            r'^(mengalami)',            # mengalami
            r'^(berubah)',              # berubah
        ]
        
        # Inquiry indicators
        self.inquiry_indicators = [
            r'^(ayo\s+mengamati)',      # Ayo Mengamati
            r'^(ayo\s+menyimak)',      # Ayo Menyimak
            r'^(kira-kira)',           # Kira-kira
            r'^(apakah\s+kamu)',       # Apakah kamu
            r'^(coba\s+perhatikan)',   # Coba perhatikan
        ]
        
        # Structural indicators
        self.structural_indicators = [
            r'^(tujuan)',               # Tujuan
            r'^(media\s+pembelajaran)', # Media Pembelajaran
            r'^(metode\s+pembelajaran)',# Metode Pembelajaran
            r'^(halaman)',              # Halaman
            r'^(bab)',                 # Bab
        ]
        
        # False positive patterns - these should NOT trigger assessment
        self.assessment_false_positive_patterns = [
            r'^topik\s+\d+',           # Topic headers
            r'^urian\s+materi',        # Uraian materi
            r'^pengertian',            # Definition sections
            r'^definisi',              # Definition sections
            r'apa\s+itu',              # Definition questions
            r'bagaimana\s+proses',     # Process explanation
            r'mengapa\s+terjadi',      # Explanation questions
        ]
    
    def extract_features(self, text: str) -> ClassificationFeatures:
        """Extract features from text for classification"""
        features = ClassificationFeatures(
            text=text,
            length=len(text),
            word_count=len(text.split()),
            sentence_count=len([s for s in text.split('.') if s.strip()])
        )
        
        # Extract questions
        questions = re.findall(r'[?!.]', text)
        features.has_questions = '?' in text
        features.question_count = text.count('?')
        
        # Detect question types
        if re.search(r'apa|siapa|di mana|kapan|mengapa|bagaimana', text, re.IGNORECASE):
            features.question_types.append('wh_question')
        if re.search(r'apakah|benar|salah', text, re.IGNORECASE):
            features.question_types.append('yes_no')
        
        # Check for numbers
        features.has_numbers = bool(re.search(r'\d+', text))
        features.numbered_list = bool(re.search(r'^\s*\d+\.', text, re.MULTILINE))
        
        # Check for assessment indicators
        for pattern in self.assessment_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                features.has_test_keywords = True
                break
        
        # Check for imperative verbs (assessment)
        imperative_patterns = [r'jawablah', r'tentukan', r'selesaikan', r'hitunglah', r'buatlah']
        features.has_imperative_verbs = any(re.search(pattern, text, re.IGNORECASE) for pattern in imperative_patterns)
        
        # Check for scoring indicators
        features.has_scoring_indicators = bool(re.search(r'skor|nilai|poin|pembahasan', text, re.IGNORECASE))
        
        # Check for concept indicators
        for pattern in self.concept_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                features.has_definition_patterns = True
                break
        
        # Check for process indicators
        for pattern in self.process_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                features.has_descriptions = True
                break
        
        # Check for structural indicators
        features.has_topic_headers = bool(re.search(r'^topik\s+\d+|urian\s+materi', text, re.IGNORECASE))
        features.has_section_markers = any(re.search(pattern, text, re.IGNORECASE) for pattern in self.structural_indicators)
        
        return features
    
    def classify_chunk_semantic(self, text: str, chunk_type: str, metadata: Dict[str, Any]) -> Tuple[EducationalChunkType, SemanticIntent, float]:
        """
        Enhanced semantic classification with false positive reduction
        """
        features = self.extract_features(text)
        
        # First check: False positive prevention
        for false_positive_pattern in self.assessment_false_positive_patterns:
            if re.search(false_positive_pattern, text, re.IGNORECASE):
                # This is NOT assessment, it's explanation
                if re.search(r'^topik', text, re.IGNORECASE):
                    return EducationalChunkType.CONCEPT_INTRO, SemanticIntent.EXPLANATION, 0.9
                elif re.search(r'urian|materi', text, re.IGNORECASE):
                    return EducationalChunkType.PROCESS_EXPLANATION, SemanticIntent.EXPLANATION, 0.85
                elif re.search(r'pengertian|definisi', text, re.IGNORECASE):
                    return EducationalChunkType.DEFINITION, SemanticIntent.EXPLANATION, 0.9
        
        # Second check: Structural content
        if features.has_section_markers or features.has_topic_headers:
            if re.search(r'tujuan', text, re.IGNORECASE):
                return EducationalChunkType.LEARNING_OBJECTIVE, SemanticIntent.INSTRUCTION, 0.85
            else:
                return EducationalChunkType.CONCEPT_INTRO, SemanticIntent.STRUCTURAL, 0.8
        
        # Third check: Inquiry content
        if features.has_questions and features.question_count <= 2:
            for inquiry_pattern in self.inquiry_indicators:
                if re.search(inquiry_pattern, text, re.IGNORECASE):
                    return EducationalChunkType.EXPLORATION, SemanticIntent.INQUIRY, 0.85
        
        # Fourth check: Assessment with higher threshold
        is_assessment = False
        assessment_score = 0
        
        if features.has_test_keywords:
            assessment_score += 0.4
        if features.has_imperative_verbs:
            assessment_score += 0.3
        if features.has_scoring_indicators:
            assessment_score += 0.3
        if features.question_count > 2 and not any(pt in features.question_types for pt in ['wh_question']):
            assessment_score += 0.2
        
        # Only classify as assessment if score is high enough
        if assessment_score >= 0.7:
            is_assessment = True
        
        # Fifth check: Concept explanation
        if features.has_definition_patterns or features.has_descriptions:
            if not is_assessment:
                if re.search(r'proses|tahap|langkah', text, re.IGNORECASE):
                    return EducationalChunkType.PROCESS_EXPLANATION, SemanticIntent.EXPLANATION, 0.8
                else:
                    return EducationalChunkType.CONCEPT_INTRO, SemanticIntent.EXPLANATION, 0.75
        
        # Sixth check: Process content
        if features.has_descriptions:
            return EducationalChunkType.PROCESS_EXPLANATION, SemanticIntent.EXPLANATION, 0.8
        
        # Default fallback with lower confidence
        return EducationalChunkType.CONCEPT_INTRO, SemanticIntent.EXPLANATION, 0.6
    
    def reclassify_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reclassify chunks with enhanced semantic classifier"""
        reclassified = []
        assessment_reductions = 0
        
        for chunk in chunks:
            original_type = chunk.get('chunk_type', '')
            text = chunk.get('text', '')
            metadata = {'subject': chunk.get('subject'), 'grade': chunk.get('grade')}
            
            # Apply enhanced classification
            new_type, semantic_intent, confidence = self.classify_chunk_semantic(text, original_type, metadata)
            
            # Track assessment reductions
            if 'assessment' in original_type.lower() and 'assessment' not in new_type.value.lower():
                assessment_reductions += 1
            
            # Update chunk with new classification
            chunk['chunk_type'] = new_type.value
            chunk['semantic_intent'] = semantic_intent.value
            chunk['classification_confidence'] = confidence
            chunk['original_chunk_type'] = original_type
            
            reclassified.append(chunk)
        
        return reclassified, assessment_reductions