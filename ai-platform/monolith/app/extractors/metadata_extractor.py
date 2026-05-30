"""
Metadata Extractor untuk Parser Service
Extracts document metadata seperti judul buku, penulis, tahun, kurikulum, dll
Khusus untuk kurikulum dan educational materials
"""
import logging
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import fitz  # PyMuPDF
from pathlib import Path

logger = logging.getLogger(__name__)


class DocumentType(Enum):
    """Tipe dokumen"""
    TEXTBOOK = "textbook"              # Buku teks utama
    WORKBOOK = "workbook"              # Buku latihan
    TEACHER_GUIDE = "teacher_guide"    # Panduan guru
    STUDENT_BOOK = "student_book"      # Buku siswa
    SUPPLEMENTARY = "supplementary"     # Buku penunjang
    ASSESSMENT = "assessment"          # Bahan asesmen
    CURRICULUM_GUIDE = "curriculum_guide"  # Panduan kurikulum
    REFERENCE = "reference"            # Buku referensi
    DIGITAL = "digital"                # Materi digital
    HANDOUT = "handout"                # Lembar kerja
    UNKNOWN = "unknown"


class EducationLevel(Enum):
    """Tingkat pendidikan"""
    TK = "TK"
    SD = "SD"
    SMP = "SMP"
    SMA = "SMA"
    SMK = "SMK"
    PAKET_A = "Paket A"
    PAKET_B = "Paket B"
    PAKET_C = "Paket C"
    OTHER = "other"


class Curriculum(Enum):
    """Kurikulum"""
    MERDEKA = "Kurikulum Merdeka"
    K13 = "Kurikulum 2013"
    KTSP = "KTSP"
    KBK = "KBK"
    LEGACY = "Kurikulum Lama"
    UNKNOWN = "unknown"


@dataclass
class DocumentMetadata:
    """Metadata lengkap untuk dokumen"""
    doc_id: str
    
    # Basic identification
    title: str = ""
    subtitle: str = ""
    authors: List[str] = field(default_factory=list)
    editors: List[str] = field(default_factory=list)
    contributors: List[str] = field(default_factory=list)
    
    # Publication info
    publisher: str = ""
    year: str = ""
    edition: str = ""
    isbn: str = ""
    issn: str = ""
    
    # Educational classification
    document_type: DocumentType = DocumentType.UNKNOWN
    education_level: EducationLevel = EducationLevel.OTHER
    curriculum: Curriculum = Curriculum.UNKNOWN
    grade_level: str = ""  # Kelas 1, Kelas 2, dll
    phase: str = ""         # Fase A, Fase B, dll (Kurikulum Merdeka)
    
    # Subject classification
    subject: str = ""
    subject_code: str = ""
    subjects: List[str] = field(default_factory=list)  # Untuk multiple subjects
    
    # Volume dan edition
    volume: str = ""
    part: str = ""
    chapter: str = ""
    unit: str = ""
    
    # Language dan region
    language: str = "id"
    region: str = ""
    
    # Rights dan licensing
    copyright: str = ""
    license: str = ""
    permissions: str = ""
    
    # Technical metadata
    page_count: int = 0
    word_count: int = 0
    file_size: int = 0
    created_date: str = ""
    modified_date: str = ""
    
    # Educational metadata
    learning_objectives: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    competency_standards: List[str] = field(default_factory=list)
    basic_competencies: List[str] = field(default_factory=list)
    
    # Kurikulum Merdeka specific
    p5_projects: List[str] = field(default_factory=list)
    learning_profiles: List[str] = field(default_factory=list)
    
    # Assessment info
    assessment_type: str = ""
    assessment_level: str = ""
    
    # Additional metadata
    abstract: str = ""
    description: str = ""
    notes: str = ""
    
    # Confidence scores
    extraction_confidence: float = 0.0
    metadata_quality_score: float = 0.0
    
    # Source info
    source: str = ""
    extraction_method: str = ""


@dataclass
class MetadataExtractionResult:
    """Hasil ekstraksi metadata"""
    doc_id: str
    file_path: str
    metadata: DocumentMetadata
    extraction_method: str = "automated"
    confidence: float = 0.0
    errors: List[str] = field(default_factory=list)


class MetadataExtractor:
    """
    Extractor untuk document metadata dari PDF documents
    
    Mendukung ekstraksi:
    - Judul, penulis, penerbit
    - Tahun publikasi, edition
    - ISBN/ISSN
    - Kurikulum, tingkat pendidikan, mata pelajaran
    - Informasi Kurikulum Merdeka
    - Metadata pendidikan lainnya
    """
    
    def __init__(self, extract_all: bool = True, min_confidence: float = 0.5):
        """
        Initialize Metadata Extractor
        
        Args:
            extract_all: Extract semua metadata fields
            min_confidence: Minimum confidence score untuk extraction
        """
        self.extract_all = extract_all
        self.min_confidence = min_confidence
        
        # Initialize patterns
        self._init_extraction_patterns()
        
        logger.info("MetadataExtractor initialized for educational document metadata")
    
    def _init_extraction_patterns(self):
        """Initialize regex patterns untuk metadata extraction"""
        # Title patterns
        self.title_patterns = [
            re.compile(r'(?i)^[Bb]uku\s+(.+)$', re.MULTILINE),
            re.compile(r'(?i)^[Pp]anduan\s+(.+)$', re.MULTILINE),
            re.compile(r'(?i)^[Ll]atihan\s+(.+)$', re.MULTILINE),
            re.compile(r'(?i)^[Mm]odul\s+(.+)$', re.MULTILINE),
            re.compile(r'(?i)^[Bb]ahan\s+(.+)$', re.MULTILINE),
        ]
        
        # Author patterns
        self.author_patterns = [
            re.compile(r'(?i)(?:[Pp]enulis|Author|Penyusun|Ditulis)\s*[:：]\s*(.+)'),
            re.compile(r'(?i)(?:[Oo]leh|By)\s*(.+)'),
            re.compile(r'(?i)(?:[Dd]isusun\s+[Oo]leh|Compiled\s+[Bb]y)\s*(.+)'),
        ]
        
        # Publisher patterns
        self.publisher_patterns = [
            re.compile(r'(?i)(?:[Pp]enerbit|Publisher|Diterbitkan)\s*[:：]\s*(.+)'),
            re.compile(r'(?i)(?:[Cc]v\.|CV)\s*(.+)'),
        ]
        
        # Year patterns
        self.year_patterns = [
            re.compile(r'\b(19|20)\d{2}\b'),
            re.compile(r'(?i)(?:[Tt]ahun|Year)\s*[:：]?\s*(19|20)\d{2}'),
        ]
        
        # ISBN patterns
        self.isbn_pattern = re.compile(
            r'(?i)(?:ISBN[-–]?(?:1[03])?[:\s])?([0-9X\-]{10,17})'
        )
        
        # Education level patterns
        self.education_level_patterns = [
            (re.compile(r'(?i)\b[Tt][Kk]\b'), EducationLevel.TK),
            (re.compile(r'(?i)\b[Ss][Dd]\b'), EducationLevel.SD),
            (re.compile(r'(?i)\b[Ss][Mm][Pp]\b'), EducationLevel.SMP),
            (re.compile(r'(?i)\b[Ss][Mm][Aa]\b'), EducationLevel.SMA),
            (re.compile(r'(?i)\b[Ss][Mm][Kk]\b'), EducationLevel.SMK),
            (re.compile(r'(?i)[Pp]aket\s+[Aa]'), EducationLevel.PAKET_A),
            (re.compile(r'(?i)[Pp]aket\s+[Bb]'), EducationLevel.PAKET_B),
            (re.compile(r'(?i)[Pp]aket\s+[Cc]'), EducationLevel.PAKET_C),
        ]
        
        # Curriculum patterns
        self.curriculum_patterns = [
            (re.compile(r'(?i)[Kk]urikulum\s+[Mm]erdeka'), Curriculum.MERDEKA),
            (re.compile(r'(?i)[Kk]urikulum\s+2013'), Curriculum.K13),
            (re.compile(r'(?i)[Kk]13'), Curriculum.K13),
            (re.compile(r'(?i)[Kk][Tt][Ss][Pp]'), Curriculum.KTSP),
            (re.compile(r'(?i)[Kk][Bb][Kk]'), Curriculum.KBK),
        ]
        
        # Grade level patterns
        self.grade_patterns = [
            re.compile(r'(?i)[Kk]elas\s+([1-9]|1[0-2])'),
            re.compile(r'(?i)[Gg]rade\s+([1-9]|1[0-2])'),
            re.compile(r'(?i)\b([IVX]+)\b'),
        ]
        
        # Phase patterns (Kurikulum Merdeka)
        self.phase_patterns = [
            re.compile(r'(?i)[Ff]ase\s+([A-D])'),
            re.compile(r'(?i)[Pp]hase\s+([1-4])'),
        ]
        
        # Subject patterns
        self.subject_patterns = [
            re.compile(r'(?i)(?:[Mm]atematika|[Mm]ath)'),
            re.compile(r'(?i)(?:[Bb]ahasa\s+[Ii]ndonesia|[Ii]ndonesian)'),
            re.compile(r'(?i)(?:[Bb]ahasa\s+[Ii]nggris|[Ee]nglish)'),
            re.compile(r'(?i)(?:[Ii][Pp][Aa]|[Ss]ains)'),
            re.compile(r'(?i)(?:[Ii][Pp][Ss]|[Ss]ocial)'),
            re.compile(r'(?i)(?:[Pp][Jj][Oo][Kk]|[Pp][Ee]|[Ss]ports)'),
            re.compile(r'(?i)(?:[Ss]eni\s+[Bb]udaya|[Aa]rts)'),
            re.compile(r'(?i)(?:[Pp][Pp][Kk][Nn]|[Cc]ivics)'),
            re.compile(r'(?i)(?:[Aa]gama|[Rr]eligion)'),
        ]
    
    def extract(
        self,
        file_path: str,
        doc_id: str,
        extraction_method: str = "automated"
    ) -> MetadataExtractionResult:
        """
        Extract metadata dari PDF document
        
        Args:
            file_path: Path ke PDF file
            doc_id: Document ID
            extraction_method: Method untuk extraction (automated, manual, hybrid)
        
        Returns:
            MetadataExtractionResult dengan extracted metadata
        """
        result = MetadataExtractionResult(
            doc_id=doc_id,
            file_path=file_path,
            metadata=DocumentMetadata(doc_id=doc_id),
            extraction_method=extraction_method
        )
        
        try:
            doc = fitz.open(file_path)
            
            # Extract dari first few pages (biasanya metadata ada di halaman awal)
            max_metadata_pages = min(5, doc.page_count)
            metadata_text = ""
            for page_num in range(max_metadata_pages):
                page = doc[page_num]
                metadata_text += page.get_text() + "\n"
            
            # Extract metadata components
            self._extract_basic_metadata(metadata_text, result.metadata)
            self._extract_publication_metadata(metadata_text, result.metadata)
            self._extract_educational_metadata(metadata_text, result.metadata)
            self._extract_curriculum_metadata(metadata_text, result.metadata)
            self._extract_document_stats(doc, result.metadata)
            
            # Calculate confidence
            result.confidence = self._calculate_confidence(result.metadata)
            result.metadata.extraction_confidence = result.confidence
            result.metadata.extraction_method = extraction_method
            result.metadata.source = file_path
            
            doc.close()
            
            logger.info(f"Extracted metadata from {file_path} with confidence {result.confidence}")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            result.errors.append(str(e))
            return result
    
    def _extract_basic_metadata(self, text: str, metadata: DocumentMetadata):
        """Extract basic metadata (title, authors)"""
        # Extract title
        for pattern in self.title_patterns:
            matches = pattern.findall(text)
            if matches:
                metadata.title = matches[0].strip()
                break
        
        # If no title pattern matches, try first significant line
        if not metadata.title:
            lines = text.strip().split('\n')
            for line in lines[:10]:  # Check first 10 lines
                line = line.strip()
                if len(line) > 10 and len(line) < 200:
                    metadata.title = line
                    break
        
        # Extract authors
        for pattern in self.author_patterns:
            matches = pattern.findall(text)
            if matches:
                author_text = matches[0] if isinstance(matches[0], str) else matches[0][1]
                # Split multiple authors
                authors = re.split(r'[,&]', author_text)
                metadata.authors = [a.strip() for a in authors if a.strip()]
                break
    
    def _extract_publication_metadata(self, text: str, metadata: DocumentMetadata):
        """Extract publication metadata (publisher, year, ISBN)"""
        # Extract publisher
        for pattern in self.publisher_patterns:
            matches = pattern.findall(text)
            if matches:
                metadata.publisher = matches[0].strip()
                break
        
        # Extract year
        years = self.year_patterns[0].findall(text)  # Use basic year pattern
        if years:
            # Use most recent year (last occurrence)
            metadata.year = years[-1]
        
        # Extract ISBN
        isbn_match = self.isbn_pattern.search(text)
        if isbn_match:
            metadata.isbn = isbn_match.group(1).strip()
    
    def _extract_educational_metadata(self, text: str, metadata: DocumentMetadata):
        """Extract educational metadata (level, subject, grade)"""
        # Extract education level
        for pattern, level in self.education_level_patterns:
            if pattern.search(text):
                metadata.education_level = level
                break
        
        # Extract subject
        for pattern in self.subject_patterns:
            match = pattern.search(text)
            if match:
                subject = match.group(1).strip() if isinstance(match, re.Match) else pattern.pattern
                metadata.subject = subject
                metadata.subjects.append(subject)
                break
        
        # Extract grade level
        grade_match = self.grade_patterns[0].search(text)  # Kelas pattern
        if grade_match:
            metadata.grade_level = f"Kelas {grade_match.group(1)}"
        
        # Extract phase
        phase_match = self.phase_patterns[0].search(text)
        if phase_match:
            metadata.phase = f"Fase {phase_match.group(1)}"
    
    def _extract_curriculum_metadata(self, text: str, metadata: DocumentMetadata):
        """Extract curriculum-specific metadata"""
        # Extract curriculum
        for pattern, curriculum in self.curriculum_patterns:
            if pattern.search(text):
                metadata.curriculum = curriculum
                break
        
        # Extract P5 projects (Kurikulum Merdeka)
        p5_pattern = re.compile(r'(?i)(?:[Pp]5|[Pp]rojek\s+[Pp]enguatan\s+[Pp]rofile\s+[Pp]elajar)', re.MULTILINE)
        p5_matches = p5_pattern.finditer(text)
        for match in p5_matches:
            # Extract context around P5 mention
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 100)
            context = text[start:end].strip()
            metadata.p5_projects.append(context)
        
        # Extract competency standards
        competency_pattern = re.compile(r'(?i)(?:[Ss]tandar\s+[Kk]ompetensi|SK)\s*[:：]?\s*(.+)', re.MULTILINE)
        competency_matches = competency_pattern.findall(text)
        for match in competency_matches:
            competency = match if isinstance(match, str) else match[0]
            metadata.competency_standards.append(competency.strip())
    
    def _extract_document_stats(self, doc: fitz.Document, metadata: DocumentMetadata):
        """Extract document statistics"""
        metadata.page_count = doc.page_count
        
        # Estimate word count
        total_words = 0
        for page in doc:
            text = page.get_text()
            total_words += len(text.split())
        metadata.word_count = total_words
        
        # File size
        try:
            from pathlib import Path
            metadata.file_size = Path(doc.name).stat().st_size
        except:
            pass
    
    def _calculate_confidence(self, metadata: DocumentMetadata) -> float:
        """Calculate confidence score untuk extracted metadata"""
        confidence = 0.0
        total_checks = 0
        
        # Check basic metadata
        if metadata.title:
            confidence += 0.2
        total_checks += 1
        
        if metadata.authors:
            confidence += 0.15
        total_checks += 1
        
        # Check publication metadata
        if metadata.publisher:
            confidence += 0.1
        total_checks += 1
        
        if metadata.year:
            confidence += 0.1
        total_checks += 1
        
        # Check educational metadata
        if metadata.subject:
            confidence += 0.15
        total_checks += 1
        
        if metadata.education_level != EducationLevel.OTHER:
            confidence += 0.15
        total_checks += 1
        
        if metadata.curriculum != Curriculum.UNKNOWN:
            confidence += 0.15
        total_checks += 1
        
        if metadata.grade_level:
            confidence += 0.1
        total_checks += 1
        
        return min(confidence / total_checks if total_checks > 0 else 0.0, 1.0)
    
    def enrich_with_manual_metadata(
        self,
        base_result: MetadataExtractionResult,
        manual_metadata: Dict[str, Any]
    ) -> MetadataExtractionResult:
        """
        Enrich automated extraction dengan manual metadata
        
        Args:
            base_result: Base automated extraction result
            manual_metadata: Manual metadata sebagai dictionary
        
        Returns:
            Enriched metadata extraction result
        """
        for key, value in manual_metadata.items():
            if hasattr(base_result.metadata, key) and value:
                setattr(base_result.metadata, key, value)
        
        # Update confidence untuk manually provided fields
        base_result.confidence = min(base_result.confidence + 0.2, 1.0)
        base_result.metadata.extraction_method = "hybrid"
        
        return base_result