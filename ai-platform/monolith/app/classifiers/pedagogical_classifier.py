"""
Pedagogical Content Classifier
Advanced classification system for educational content types including assessment, reflection, glossary, rubric, discussion, etc.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import re
from app.models.chunk_types import EducationalChunkType, ChunkImportance, BloomLevel


class PedagogicalIntent(Enum):
    """Pedagogical intent classifications"""
    INSTRUCTION = "instruction"           # Teaching/instructional content
    PRACTICE = "practice"                 # Practice/exercise content
    ASSESSMENT = "assessment"             # Assessment/evaluation content
    REFLECTION = "reflection"             # Metacognitive reflection
    COLLABORATION = "collaboration"      # Group/collaborative work
    RESEARCH = "research"                 # Research/inquiry activities
    CREATIVITY = "creativity"             # Creative production
    ORGANIZATION = "organization"         # Organizational/structural content


@dataclass
class PedagogicalFeatures:
    """Pedagogical features extracted from text content"""
    text_length: int
    sentence_count: int
    paragraph_count: int
    
    # Question features
    has_questions: bool = False
    question_count: int = 0
    question_types: List[str] = field(default_factory=list)
    
    # Instruction features  
    has_instructions: bool = False
    instruction_markers: List[str] = field(default_factory=list)
    
    # Reflection features
    has_reflection_markers: bool = False
    reflection_keywords: List[str] = field(default_factory=list)
    
    # Discussion features
    has_discussion_markers: bool = False
    discussion_keywords: List[str] = field(default_factory=list)
    
    # Summary features
    has_summary_markers: bool = False
    summary_keywords: List[str] = field(default_factory=list)
    
    # Bibliography features
    has_bibliography_markers: bool = False
    reference_count: int = 0
    
    # Glossary features
    has_definition_patterns: bool = False
    has_term_pairs: bool = False
    
    # Rubric features
    has_criteria: bool = False
    has_scoring_levels: bool = False
    
    # Activity features
    has_activity_steps: bool = False
    step_count: int = 0
    
    # Assessment features
    has_assessment_format: bool = False
    assessment_type: Optional[str] = None
    
    # Document structure
    is_cover_page: bool = False
    is_table_of_contents: bool = False
    is_bibliography: bool = False


class PedagogicalClassifier:
    """Advanced classifier for pedagogical content types"""
    
    def __init__(self):
        # Indonesian pedagogical patterns - ENHANCED for Priority 2
        self.reflection_patterns = [
            r'refleksi', r'menilai kembali', r'berpikir kembali', 
            r'apa yang kamu pelajari', r'apa yang kamu rasakan',
            r'kesimpulan dari', r'pengalaman belajar',
            r'bagaimana perasaan kamu', r'apa yang kamu dapatkan',
            r'menyimpulkan', r'merefleksikan', r'introspeksi',
            r'self-reflection', r'refleksi diri', r'pemahaman diri'
        ]
        
        self.glossary_patterns = [
            r'istilah', r'kata kunci', r'kamus', r'glosarium',
            r'definisi', r'artinya', r'berarti', r'yaitu',
            r'pengertian', r'adalah', r'merupakan', r'didefinisikan sebagai',
            r'term:', r'singkatan:', r'kependekan:'
        ]
        
        self.rubric_patterns = [
            r'kriteria', r'penilaian', r'rubrik', r'skor',
            r'nilai', r'penilaian kriteria', r'tingkat pencapaian',
            r'skala penilaian', r'indikator penilaian', r'aspek penilaian',
            r'kriteria keberhasilan', r'rubrik penilaian', r'format penilaian'
        ]
        
        self.bibliography_patterns = [
            r'daftar pustaka', r'referensi', r'sumber',
            r'bibliografi', r'sumber bacaan', r'bahan bacaan',
            r'kutipan', r'pustaka', r'literatur', r'sumber referensi'
        ]
        
        self.summary_patterns = [
            r'rangkuman', r'summary', r'ringkasan',
            r'kesimpulan', r'pokok-pokok', r'intisari',
            r'poin penting', r'saran-saran', r'rekomendasi'
        ]
        
        self.discussion_patterns = [
            r'diskusi', r'berdiskusi', r'kelompok', r'bagikan pendapat',
            r'tukar pendapat', r'perdebatan', r'kolaborasi',
            r'kelompok kerja', r'kerja sama', r'berbagi ide'
        ]
        
        self.assessment_patterns = [
            r'soal', r'pertanyaan', r'latihan', r'evaluasi',
            r'ujian', r'kuis', r'tes'
        ]
        
        self.instruction_patterns = [
            r'langkah', r'tahap', r'prosedur', r'cara',
            r'bagaimana', r'lakukan', r'kerjakan'
        ]
        
        self.curriculum_patterns = [
            r'CP\.', r'TP\.', r'KD\.', r'ATP',
            r'capaian pembelajaran', r'tujuan pembelajaran',
            r'kompetensi dasar', r'kompetensi inti'
        ]
    
    def extract_pedagogical_features(self, text: str) -> PedagogicalFeatures:
        """Extract pedagogical features from text"""
        text_lower = text.lower()
        
        # Basic text statistics
        sentences = re.split(r'[.!?]+', text)
        paragraphs = text.split('\n\n')
        
        features = PedagogicalFeatures(
            text_length=len(text),
            sentence_count=len([s for s in sentences if s.strip()]),
            paragraph_count=len([p for p in paragraphs if p.strip()])
        )
        
        # Extract question features
        questions = re.findall(r'[?]', text)
        features.has_questions = len(questions) > 0
        features.question_count = len(questions)
        
        if features.has_questions:
            question_words = re.findall(r'\b(apa|bagaimana|mengapa|kapan|dimana|siapa)\b', text_lower)
            features.question_types = question_words
        
        # Extract instruction features
        instruction_markers = re.findall(r'\b(langkah|tahap|prosedur|cara|lakukan|kerjakan)\b', text_lower)
        features.has_instructions = len(instruction_markers) > 2
        features.instruction_markers = instruction_markers
        
        # Extract reflection features
        reflection_matches = [pattern for pattern in self.reflection_patterns 
                            if re.search(pattern, text_lower)]
        features.has_reflection_markers = len(reflection_matches) > 0
        features.reflection_keywords = reflection_matches
        
        # Extract discussion features
        discussion_matches = [pattern for pattern in self.discussion_patterns 
                            if re.search(pattern, text_lower)]
        features.has_discussion_markers = len(discussion_matches) > 0
        features.discussion_keywords = discussion_matches
        
        # Extract glossary features
        definition_pattern = re.search(r'\w+\s+(adalah|merupakan|berarti|artinya)', text_lower)
        features.has_definition_patterns = definition_pattern is not None
        
        # Extract rubric features
        rubric_matches = [pattern for pattern in self.rubric_patterns 
                         if re.search(pattern, text_lower)]
        features.has_criteria = len(rubric_matches) > 1
        features.has_scoring_levels = re.search(r'\d+\s*[/.]+\s*\d+', text) is not None
        
        # Extract activity step features
        numbered_steps = re.findall(r'^\s*\d+\.', text, re.MULTILINE)
        features.has_activity_steps = len(numbered_steps) >= 3
        features.step_count = len(numbered_steps)
        
        # Extract assessment features
        assessment_matches = [pattern for pattern in self.assessment_patterns 
                            if re.search(pattern, text_lower)]
        features.has_assessment_format = len(assessment_matches) > 0
        
        if features.has_assessment_format:
            # Determine assessment type
            if re.search(r'\b(pilihan ganda|pilih|a\s*\.\s*b\s*\.\s*c\s*\.\s*d)\b', text_lower):
                features.assessment_type = "multiple_choice"
            elif re.search(r'\b(jelaskan|uraikan|deskripsikan)\b', text_lower):
                features.assessment_type = "essay"
            elif re.search(r'\b(cocokkan|pasangkan)\b', text_lower):
                features.assessment_type = "matching"
        
        # Detect document structure
        features.is_cover_page = self._is_cover_page(text)
        features.is_table_of_contents = self._is_table_of_contents(text)
        features.is_bibliography = self._is_bibliography(text)
        
        return features
    
    def _is_cover_page(self, text: str) -> bool:
        """Detect if text is a cover page"""
        cover_indicators = [
            'cover', 'sampul', 'judul', 'penyusun', 'editor', 'ilustrator',
            'isbn', 'katalog', 'penerbit', 'kota', 'tahun'
        ]
        text_lower = text.lower()
        matches = sum(1 for indicator in cover_indicators if indicator in text_lower)
        return matches >= 3 and len(text) < 500
    
    def _is_table_of_contents(self, text: str) -> bool:
        """Detect if text is table of contents"""
        toc_indicators = [
            'daftar isi', 'table of contents', 'bab', 'halaman',
            'pendahuluan', 'pembahasan', 'penutup'
        ]
        text_lower = text.lower()
        matches = sum(1 for indicator in toc_indicators if indicator in text_lower)
        # Check for typical TOC structure (dots between titles and page numbers)
        has_dots_pattern = re.search(r'\.{3,}\s*\d+', text)
        return matches >= 2 or has_dots_pattern
    
    def _is_bibliography(self, text: str) -> bool:
        """Detect if text is bibliography/references"""
        bib_indicators = [
            'daftar pustaka', 'referensi', 'bibliography', 'sumber',
            'diambil dari', 'diakses', 'journal', 'vol', 'no', 'hal'
        ]
        text_lower = text.lower()
        matches = sum(1 for indicator in bib_indicators if indicator in text_lower)
        return matches >= 2
    
    def classify_pedagogical_type(self, text: str, metadata: Dict[str, Any]) -> Tuple[EducationalChunkType, PedagogicalIntent]:
        """
        Classify text into pedagogical type with intent
        
        Args:
            text: Text content to classify
            metadata: Document metadata
            
        Returns:
            Tuple of (chunk_type, pedagogical_intent)
        """
        features = self.extract_pedagogical_features(text)
        
        # Check document structure types first
        if features.is_cover_page:
            return EducationalChunkType.COVER_PAGE, PedagogicalIntent.ORGANIZATION
        if features.is_table_of_contents:
            return EducationalChunkType.TABLE_OF_CONTENTS, PedagogicalIntent.ORGANIZATION
        if features.is_bibliography:
            return EducationalChunkType.BIBLIOGRAPHY, PedagogicalIntent.ORGANIZATION
        
        # Check curriculum content
        curriculum_matches = [pattern for pattern in self.curriculum_patterns 
                            if re.search(pattern, text.lower())]
        if len(curriculum_matches) >= 2:
            return EducationalChunkType.KURIKULUM_MERDEKA, PedagogicalIntent.ORGANIZATION
        
        # Check for reflection content
        if features.has_reflection_markers and len(features.reflection_keywords) >= 2:
            return EducationalChunkType.REFLECTION, PedagogicalIntent.REFLECTION
        
        # Check for discussion content
        if features.has_discussion_markers and len(features.discussion_keywords) >= 1:
            return EducationalChunkType.DISCUSSION, PedagogicalIntent.COLLABORATION
        
        # Check for glossary content
        if features.has_definition_patterns and len(text) < 300:
            return EducationalChunkType.GLOSSARY, PedagogicalIntent.INSTRUCTION
        
        # Check for rubric content
        if features.has_criteria or features.has_scoring_levels:
            return EducationalChunkType.RUBRIC, PedagogicalIntent.ASSESSMENT
        
        # Check for assessment content
        if features.has_assessment_format:
            if features.assessment_type == "multiple_choice":
                return EducationalChunkType.MULTIPLE_CHOICE, PedagogicalIntent.ASSESSMENT
            elif features.assessment_type == "essay":
                return EducationalChunkType.ESSAY_QUESTION, PedagogicalIntent.ASSESSMENT
            elif features.assessment_type == "matching":
                return EducationalChunkType.MATCHING_QUESTION, PedagogicalIntent.ASSESSMENT
            else:
                return EducationalChunkType.FORMATIVE_ASSESSMENT, PedagogicalIntent.ASSESSMENT
        
        # Check for activity/experiment content
        if features.has_activity_steps and features.step_count >= 3:
            # Check if it's an experiment
            if re.search(r'(eksperimen|percobaan|praktikum)', text.lower()):
                return EducationalChunkType.EXPERIMENT, PedagogicalIntent.PRACTICE
            elif re.search(r'(eksplorasi|penelusuran|investigasi)', text.lower()):
                return EducationalChunkType.EXPLORATION, PedagogicalIntent.RESEARCH
            else:
                return EducationalChunkType.ACTIVITY_GUIDE, PedagogicalIntent.PRACTICE
        
        # Default classification based on existing logic
        if features.has_instructions:
            return EducationalChunkType.INSTRUCTION, PedagogicalIntent.INSTRUCTION
        
        if re.search(r'(tujuan|diharapkan|capaian)', text.lower()):
            return EducationalChunkType.LEARNING_OBJECTIVE, PedagogicalIntent.INSTRUCTION
        
        if re.search(r'(kompetensi|kemampuan)', text.lower()):
            return EducationalChunkType.COMPETENCY, PedagogicalIntent.ORGANIZATION
        
        # Fallback to basic classification
        return EducationalChunkType.CONCEPT_EXPLANATION, PedagogicalIntent.INSTRUCTION