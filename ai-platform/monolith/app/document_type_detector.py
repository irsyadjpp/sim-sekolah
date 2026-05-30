"""
Document Type Detector

Automatically detects document type to route to appropriate processing strategies.
"""
import re
import logging
from typing import Dict, Any, Optional
from enum import Enum

from app.models.document_models import Document

logger = logging.getLogger(__name__)


class DocumentType(Enum):
    """Document types for educational content"""
    TEXTBOOK = "textbook"
    LESSON_PLAN = "lesson_plan"
    ASSESSMENT = "assessment"
    ACTIVITY = "activity"
    INQUIRY = "inquiry"
    COMPETENCY_DOCUMENT = "competency_document"
    GENERAL = "general"
    # Indonesian Government/Ministry Document Types
    REGULATION = "regulation"  # Peraturan/Regulasi
    GUIDE = "guide"  # Panduan
    ACADEMIC_PAPER = "academic_paper"  # Kajian/Naskah Akademik
    CIRCULAR = "circular"  # Surat Edaran
    PRESENTATION = "presentation"  # Paparan


class DocumentTypeDetector:
    """
    Detects document type based on content patterns and structure.
    
    Routes documents to appropriate semantic processing strategies.
    """
    
    def __init__(self):
        """Initialize document type detector"""
        # Textbook patterns
        self.textbook_patterns = [
            r'chapter\s+\d+',
            r'bab\s+[ivx\d]+',
            r'section\s+\d+',
            r'unit\s+\d+',
            r'\d+\.\d+\s+',  # Decimal numbering like 10.1, 10.2
            r'exercises?',
            r'example',
            r'problem',
        ]
        
        # Lesson plan patterns
        self.lesson_plan_patterns = [
            r'lesson\s+plan',
            r'rencana\s+pelaksanaan\s+pembelajaran',
            r'rpp',
            r'learning\s+objectives?',
            r'tujuan\s+pembelajaran',
            r'kompetensi\s+(dasar|intisari)',
            r'materi\s+pembelajaran',
            r'kegiatan\s+pembelajaran',
            r'penilaian',
        ]
        
        # Assessment patterns
        self.assessment_patterns = [
            r'assessment',
            r'evaluasi',
            r'test',
            r'quiz',
            r'exam',
            r'ujian',
            r'soal',
            r'pertanyaan',
            r'pilihan\s+ganda',
            r'essay',
        ]
        
        # Activity patterns
        self.activity_patterns = [
            r'activity',
            r'kegiatan',
            r'experiment',
            r'praktikum',
            r'project',
            r'tugas',
            r'work\s+sheet',
        ]
        
        # Inquiry patterns
        self.inquiry_patterns = [
            r'inquiry',
            r'penemuan',
            r'investigation',
            r'research',
            r'exploration',
            r'eksplorasi',
        ]
        
        # Competency document patterns
        self.competency_patterns = [
            r'kompetensi\s+intim',
            r'kompetensi\s+dasar',
            r'capaian\s+pembelajaran',
            r'indikator\s+pencapaian',
            r'tujuan\s+pembelajaran',
            r'standar\s+kompetensi',
        ]
        
        # Regulation patterns (Indonesian government documents)
        self.regulation_patterns = [
            r'peraturan',
            r'regulasi',
            r'undang-undang',
            r'uu\s+no\.?\s*\d+',
            r'pp\s+no\.?\s*\d+',  # Peraturan Pemerintah
            r'perpres',  # Peraturan Presiden
            r'permendikbud',  # Peraturan Menteri Pendidikan
            r'permen',  # Peraturan Menteri
            r'standar\s+nasional',
            r'snp',  # Standar Nasional Pendidikan
            r'nomor\s+\d+',
            r'tahun\s+\d{4}',
        ]
        
        # Guide patterns (Panduan)
        self.guide_patterns = [
            r'panduan',
            r'guide',
            r'petunjuk',
            r'manual',
            r'buku\s+panduan',
            r'pedoman',
            r'panduan\s+mata\s+pelajaran',
            r'panduan\s+pembelajaran',
            r'panduan\s+implementasi',
        ]
        
        # Academic paper patterns (Kajian/Naskah Akademik)
        self.academic_paper_patterns = [
            r'kajian',
            r'naskah\s+akademik',
            r'akademik',
            r'research',
            r'studi',
            r'penelitian',
            r'jurnal',
            r'paper',
            r'analisis',
            r'review',
            r'literature',
        ]
        
        # Circular patterns (Surat Edaran)
        self.circular_patterns = [
            r'surat\s+edaran',
            r'edaran',
            r'se',
            r'surat\s+keputusan',
            r'sk',
            r'memo',
            r'pengumuman',
            r'notifikasi',
        ]
        
        # Presentation patterns (Paparan)
        self.presentation_patterns = [
            r'paparan',
            r'presentasi',
            r'slide',
            r'ppt',
            r'powerpoint',
            r'presentasi',
            r'materi\s+presentasi',
        ]
        
        logger.info("DocumentTypeDetector initialized")
    
    def detect(self, document: Document) -> DocumentType:
        """
        Detect document type based on content analysis.
        
        Args:
            document: Document model with pages and regions
            
        Returns:
            Detected document type
        """
        try:
            # Extract full text from document
            full_text = self._extract_full_text(document)
            
            if not full_text or len(full_text.strip()) < 10:
                logger.warning("Insufficient text for document type detection")
                return DocumentType.GENERAL
            
            # Score each document type
            scores = {
                DocumentType.TEXTBOOK: self._score_textbook(full_text, document),
                DocumentType.LESSON_PLAN: self._score_lesson_plan(full_text, document),
                DocumentType.ASSESSMENT: self._score_assessment(full_text, document),
                DocumentType.ACTIVITY: self._score_activity(full_text, document),
                DocumentType.INQUIRY: self._score_inquiry(full_text, document),
                DocumentType.COMPETENCY_DOCUMENT: self._score_competency(full_text, document),
                # Indonesian government document types
                DocumentType.REGULATION: self._score_regulation(full_text, document),
                DocumentType.GUIDE: self._score_guide(full_text, document),
                DocumentType.ACADEMIC_PAPER: self._score_academic_paper(full_text, document),
                DocumentType.CIRCULAR: self._score_circular(full_text, document),
                DocumentType.PRESENTATION: self._score_presentation(full_text, document),
            }
            
            # Find highest score
            detected_type = max(scores.items(), key=lambda x: x[1])[0]
            confidence = scores[detected_type]
            
            logger.info(f"Document type detected: {detected_type.value if hasattr(detected_type, 'value') else detected_type} (confidence: {confidence:.2f})")
            
            # If confidence is too low, return general
            if confidence < 0.3:
                logger.warning(f"Low confidence ({confidence:.2f}), defaulting to GENERAL")
                return DocumentType.GENERAL
            
            return detected_type
            
        except Exception as e:
            logger.error(f"Error detecting document type: {e}")
            return DocumentType.GENERAL
    
    def _extract_full_text(self, document: Document) -> str:
        """Extract full text from document"""
        text_parts = []
        
        for page in document.pages:
            for region in page.regions:
                if region.text_content:
                    text_parts.append(region.text_content)
        
        return " ".join(text_parts)
    
    def _score_textbook(self, text: str, document: Document) -> float:
        """Score document as textbook"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.textbook_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.1
        
        # Structure analysis
        # Textbooks typically have hierarchical structure with many headings
        heading_count = sum(1 for page in document.pages 
                          for region in page.regions 
                          if region.region_type in ['heading', 'title', 'subtitle'])
        
        if heading_count > 10:
            score += 0.3
        elif heading_count > 5:
            score += 0.2
        
        # Textbooks have many pages
        if len(document.pages) > 20:
            score += 0.2
        elif len(document.pages) > 10:
            score += 0.1
        
        # Mathematical content (like equations)
        if '=' in text and any(op in text for op in ['+', '-', '×', '÷']):
            score += 0.2
        
        return min(score, 1.0)
    
    def _score_lesson_plan(self, text: str, document: Document) -> float:
        """Score document as lesson plan"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.lesson_plan_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.15
        
        # Lesson plans are typically shorter
        if len(document.pages) <= 5:
            score += 0.2
        
        # Check for competency indicators
        competency_indicators = ['kompetensi', 'tujuan', 'capaian', 'indikator']
        for indicator in competency_indicators:
            if indicator in text.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def _score_assessment(self, text: str, document: Document) -> float:
        """Score document as assessment"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.assessment_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.15
        
        # Check for question patterns
        question_patterns = [r'\d+\.', r'\?', r'pilih', r'jawab']
        for pattern in question_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.05
        
        return min(score, 1.0)
    
    def _score_activity(self, text: str, document: Document) -> float:
        """Score document as activity"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.activity_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.2
        
        return min(score, 1.0)
    
    def _score_inquiry(self, text: str, document: Document) -> float:
        """Score document as inquiry"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.inquiry_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.2
        
        return min(score, 1.0)
    
    def _score_competency(self, text: str, document: Document) -> float:
        """Score document as competency document"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.competency_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.15
        
        # Check for Indonesian competency verbs
        competency_verbs = [
            'memahami', 'menerangkan', 'menjelaskan', 'mengidentifikasi',
            'menganalisis', 'menerapkan', 'menilai', 'membuat'
        ]
        
        for verb in competency_verbs:
            if verb in text.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def _score_regulation(self, text: str, document: Document) -> float:
        """Score document as regulation (Peraturan/Regulasi)"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.regulation_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.15
        
        # Regulations typically have formal structure
        formal_indicators = [
            r'bab\s+[ivx\d]+',
            r'pasal\s+\d+',
            r'ayat\s+\d+',
            r'butir\s+\d+',
        ]
        
        for indicator in formal_indicators:
            matches = len(re.findall(indicator, text, re.IGNORECASE))
            score += matches * 0.1
        
        # Check for government ministry references
        ministry_keywords = [
            'kementerian', 'kemendikbud', 'kemendikdasmen', 'pemerintah',
            'menteri', 'presiden', 'republik', 'indonesia'
        ]
        
        for keyword in ministry_keywords:
            if keyword in text.lower():
                score += 0.1
        
        # Regulations often have numbering like "Nomor X Tahun XXXX"
        if re.search(r'nomor\s+\d+\s+tahun\s+\d{4}', text, re.IGNORECASE):
            score += 0.3
        
        return min(score, 1.0)
    
    def _score_guide(self, text: str, document: Document) -> float:
        """Score document as guide (Panduan)"""
        score = 0.0
        
        # Pattern matching - higher weight for "panduan" keyword
        for pattern in self.guide_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            # Give higher weight for "panduan" specifically
            if 'panduan' in pattern.lower():
                score += matches * 0.3
            else:
                score += matches * 0.1
        
        # Guides often have step-by-step instructions
        step_patterns = [
            r'langkah\s+\d+',
            r'step\s+\d+',
            r'tahap\s+\d+',
            r'cara\s+melakukan',
            r'prosedur',
        ]
        
        for pattern in step_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.05  # Lower weight since lesson_plan also has these
        
        # Guides for educators - but penalize if it looks like a lesson plan
        educator_keywords = [
            'pendidik', 'guru', 'pengajar', 'fasilitator',
            'pembelajaran', 'mengajar', 'kelas'
        ]
        
        educator_count = sum(1 for keyword in educator_keywords if keyword in text.lower())
        if educator_count > 0:
            # If it has lesson plan keywords, reduce score
            lesson_plan_keywords = ['rencana pelaksanaan', 'rpp', 'tujuan pembelajaran', 'kompetensi dasar']
            lesson_plan_count = sum(1 for keyword in lesson_plan_keywords if keyword in text.lower())
            if lesson_plan_count > 0:
                score -= 0.3  # Penalize if it looks more like a lesson plan
            else:
                score += 0.05  # Small boost if it's for educators but not a lesson plan
        
        return max(score, 0.0)
    
    def _score_academic_paper(self, text: str, document: Document) -> float:
        """Score document as academic paper (Kajian/Naskah Akademik)"""
        score = 0.0
        
        # Pattern matching - higher weight for specific academic keywords
        for pattern in self.academic_paper_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            # Give higher weight for "kajian" and "naskah akademik"
            if 'kajian' in pattern.lower() or 'akademik' in pattern.lower():
                score += matches * 0.3
            else:
                score += matches * 0.1
        
        # Academic papers have citations/references - strong indicator
        citation_patterns = [
            r'\[\d+\]',  # [1], [2], etc.
            r'\(\d{4}\)',  # (2024), (2023), etc.
            r'referensi',
            r'daftar\s+pusaka',
            r'bibliografi',
        ]
        
        for pattern in citation_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.15  # Higher weight for citations
        
        # Academic structure - strong indicator
        academic_structure = [
            r'abstrak',
            r'pendahuluan',
            r'metodologi',
            r'hasil',
            r'pembahasan',
            r'kesimpulan',
            r'rekomendasi',
        ]
        
        structure_count = sum(1 for section in academic_structure if section in text.lower())
        if structure_count >= 4:
            score += 0.4  # Strong boost if it has academic structure
        elif structure_count >= 2:
            score += 0.2
        
        # Penalize if it looks like a guide
        if 'panduan' in text.lower() and 'kajian' not in text.lower():
            score -= 0.3
        
        return max(score, 0.0)
    
    def _score_circular(self, text: str, document: Document) -> float:
        """Score document as circular (Surat Edaran)"""
        score = 0.0
        
        # Pattern matching
        for pattern in self.circular_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.2
        
        # Circulars are typically short
        if len(document.pages) <= 3:
            score += 0.2
        
        # Circulars have date and reference numbers
        if re.search(r'\d{1,2}\s+[a-z]+\s+\d{4}', text, re.IGNORECASE):
            score += 0.1  # Date pattern
        
        if re.search(r'nomor\s*:\s*\d+', text, re.IGNORECASE):
            score += 0.15  # Reference number
        
        # Circulars often address recipients
        recipient_patterns = [
            r'kepada',
            r'yth',
            r'dengan\s+hormat',
            r'salam\s+hormat',
        ]
        
        for pattern in recipient_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.1
        
        return min(score, 1.0)
    
    def _score_presentation(self, text: str, document: Document) -> float:
        """Score document as presentation (Paparan)"""
        score = 0.0
        
        # Pattern matching - higher weight for "paparan" specifically
        for pattern in self.presentation_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            # Give higher weight for "paparan" specifically
            if 'paparan' in pattern.lower():
                score += matches * 0.4
            else:
                score += matches * 0.1
        
        # Presentations have slide-like structure
        slide_indicators = [
            r'slide\s+\d+',
            r'halaman\s+\d+',
            r'page\s+\d+',
        ]
        
        for indicator in slide_indicators:
            matches = len(re.findall(indicator, text, re.IGNORECASE))
            score += matches * 0.15
        
        # Presentations often have bullet points - strong indicator
        bullet_count = text.count('•') + text.count('-') + text.count('*')
        if bullet_count > 10:
            score += 0.3
        elif bullet_count > 5:
            score += 0.15
        
        # Presentations are typically concise
        avg_words_per_page = len(text.split()) / max(len(document.pages), 1)
        if avg_words_per_page < 100:
            score += 0.2
        
        # Penalize if it looks like a lesson plan (has "langkah" but no "paparan")
        if 'langkah' in text.lower() and 'paparan' not in text.lower():
            score -= 0.3
        
        return max(score, 0.0)
