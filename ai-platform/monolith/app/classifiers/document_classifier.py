"""
Document Classifier untuk Parser Service
Routing document ke parser yang sesuai (Marker, Docling, MinerU)
Classification berdasarkan document type, complexity, dan characteristics
"""
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import fitz  # PyMuPDF
import os

logger = logging.getLogger(__name__)


class DocumentComplexity(Enum):
    """Complexity level document"""
    SIMPLE = "simple"           # Text-heavy, basic formatting
    MODERATE = "moderate"       # Some images, tables, basic formatting
    COMPLEX = "complex"         # Many images, complex tables, mixed content
    VERY_COMPLEX = "very_complex"  # Complex layouts, equations, scientific content
    SCIENTIFIC = "scientific"   # Mathematical formulas, scientific diagrams
    MIXED = "mixed"             # Combination of various elements


class DocumentFormat(Enum):
    """Document format classification"""
    TEXT_ONLY = "text_only"
    IMAGE_HEAVY = "image_heavy"
    TABLE_HEAVY = "table_heavy"
    FORMULA_HEAVY = "formula_heavy"
    MIXED_MEDIA = "mixed_media"
    SCANNED = "scanned"
    DIGITAL_NATIVE = "digital_native"


class ParserType(Enum):
    """Parser yang tersedia untuk routing"""
    MARKER = "marker"           # Markdown-based parser, good untuk text-heavy
    DOCLING = "docling"         # Rust-based parser, good untuk complex layouts
    MINERU = "mineru"           # Multi-modal parser, good untuk mixed content
    PYMUPDF = "pymupdf"         # Basic PDF parsing
    PYPDF2 = "pypdf2"           # Simple PDF parsing
    CUSTOM = "custom"           # Custom parser implementation
    VISION = "vision"           # Vision-based parser untuk scanned docs


@dataclass
class DocumentClassification:
    """Classification result untuk document"""
    doc_id: str
    file_path: str
    
    # Complexity dan format
    complexity: DocumentComplexity = DocumentComplexity.MODERATE
    format: DocumentFormat = DocumentFormat.DIGITAL_NATIVE
    content_type: str = ""
    
    # Recommended parser
    recommended_parser: ParserType = ParserType.PYMUPDF
    parser_confidence: float = 0.0
    
    # Alternative parsers
    alternative_parsers: List[ParserType] = None
    alternative_parsers = None  # Initialize as None to avoid mutable default
    
    # Characteristic scores
    text_ratio: float = 0.0           # Ratio of text content
    image_ratio: float = 0.0          # Ratio of image content
    table_ratio: float = 0.0           # Ratio of table content
    formula_ratio: float = 0.0        # Ratio of formula content
    formatting_score: float = 0.0     # Complexity of formatting
    layout_score: float = 0.0          # Complexity of layout
    
    # Specific indicators
    has_math_content: bool = False
    has_scientific_diagrams: bool = False
    has_complex_tables: bool = False
    has_multi_column_layout: bool = False
    is_textbook: bool = False
    is_handwritten: bool = False
    is_scanned: bool = False
    
    # Processing metadata
    page_count: int = 0
    estimated_processing_time: float = 0.0
    memory_requirement: float = 0.0


@dataclass
class ParserRecommendation:
    """Recommendation untuk parser selection"""
    parser_type: ParserType
    confidence: float
    rationale: str
    pros: List[str]
    cons: List[str]
    estimated_quality: str
    estimated_speed: str


class DocumentClassifier:
    """
    Classifier untuk document routing ke appropriate parser
    
    Logic:
    1. Analyze document characteristics (text ratio, images, tables, formulas)
    2. Determine complexity level
    3. Recommend parser based on characteristics
    4. Provide alternative parsers dengan trade-offs
    """
    
    def __init__(self, enable_vision_routing: bool = True):
        """
        Initialize Document Classifier
        
        Args:
            enable_vision_routing: Enable routing ke vision-based parsers
        """
        self.enable_vision_routing = enable_vision_routing
        
        # Thresholds untuk classification
        self.thresholds = {
            'text_heavy': 0.7,
            'image_heavy': 0.3,
            'table_heavy': 0.2,
            'formula_heavy': 0.1,
            'complex_formatting': 0.6,
            'complex_layout': 0.5
        }
        
        logger.info("DocumentClassifier initialized with parser routing capabilities")
    
    def classify(
        self,
        file_path: str,
        doc_id: str,
        sample_pages: int = 5
    ) -> DocumentClassification:
        """
        Classify document dan recommend parser
        
        Args:
            file_path: Path ke document
            doc_id: Document ID
            sample_pages: Number of pages untuk sample analysis
        
        Returns:
            DocumentClassification dengan recommendations
        """
        try:
            doc = fitz.open(file_path)
            
            classification = DocumentClassification(
                doc_id=doc_id,
                file_path=file_path,
                page_count=doc.page_count
            )
            
            # Analyze document characteristics
            self._analyze_document_characteristics(doc, classification, sample_pages)
            
            # Determine complexity dan format
            classification.complexity = self._determine_complexity(classification)
            classification.format = self._determine_format(classification)
            
            # Recommend parser
            recommendation = self._recommend_parser(classification)
            classification.recommended_parser = recommendation.parser_type
            classification.parser_confidence = recommendation.confidence
            classification.alternative_parsers = self._get_alternative_parsers(classification)
            
            # Estimate processing requirements
            classification.estimated_processing_time = self._estimate_processing_time(classification)
            classification.memory_requirement = self._estimate_memory_requirement(classification)
            
            doc.close()
            
            logger.info(
                f"Classified {doc_id} as {classification.complexity.value}, "
                f"format {classification.format.value}, "
                f"recommended parser: {classification.recommended_parser.value}"
            )
            
            return classification
            
        except Exception as e:
            logger.error(f"Error classifying document {doc_id}: {e}")
            # Return default classification
            return DocumentClassification(
                doc_id=doc_id,
                file_path=file_path,
                recommended_parser=ParserType.PYMUPDF,
                parser_confidence=0.0
            )
    
    def _analyze_document_characteristics(
        self,
        doc: fitz.Document,
        classification: DocumentClassification,
        sample_pages: int
    ):
        """Analyze document characteristics"""
        pages_to_analyze = min(sample_pages, doc.page_count)
        
        total_text_length = 0
        total_images = 0
        total_tables = 0
        total_formulas = 0
        total_formatting_score = 0
        total_layout_score = 0
        
        for page_num in range(pages_to_analyze):
            page = doc[page_num]
            
            # Text analysis
            text_content = page.get_text()
            total_text_length += len(text_content)
            
            # Image analysis
            images = page.get_images()
            total_images += len(images)
            
            # Table analysis
            tables = self._detect_tables(page)
            total_tables += len(tables)
            
            # Formula analysis
            formulas = self._detect_formulas(text_content)
            total_formulas += len(formulas)
            
            # Formatting analysis
            formatting_score = self._analyze_formatting(page, text_content)
            total_formatting_score += formatting_score
            
            # Layout analysis
            layout_score = self._analyze_layout(page)
            total_layout_score += layout_score
            
            # Specific indicators
            if total_formulas > 0:
                classification.has_math_content = True
            if self._detect_scientific_diagrams(page):
                classification.has_scientific_diagrams = True
            if self._detect_complex_tables(page):
                classification.has_complex_tables = True
            if self._detect_multi_column_layout(page):
                classification.has_multi_column_layout = True
            if self._is_textbook(text_content):
                classification.is_textbook = True
            if self._is_scanned(page):
                classification.is_scanned = True
        
        # Calculate ratios
        total_content_elements = max(1, total_text_length / 1000 + total_images + total_tables + total_formulas)
        
        classification.text_ratio = total_text_length / 1000 / total_content_elements
        classification.image_ratio = total_images / total_content_elements
        classification.table_ratio = total_tables / total_content_elements
        classification.formula_ratio = total_formulas / total_content_elements
        classification.formatting_score = total_formatting_score / pages_to_analyze
        classification.layout_score = total_layout_score / pages_to_analyze
        
        logger.info(
            f"Document characteristics - Text: {classification.text_ratio:.2f}, "
            f"Images: {classification.image_ratio:.2f}, Tables: {classification.table_ratio:.2f}, "
            f"Formulas: {classification.formula_ratio:.2f}"
        )
    
    def _determine_complexity(self, classification: DocumentClassification) -> DocumentComplexity:
        """Determine document complexity level"""
        if classification.formula_ratio > 0.2 or classification.has_math_content:
            return DocumentComplexity.SCIENTIFIC
        elif classification.formatting_score > 0.7 or classification.layout_score > 0.7:
            return DocumentComplexity.VERY_COMPLEX
        elif classification.table_ratio > 0.3 or classification.formatting_score > 0.5:
            return DocumentComplexity.COMPLEX
        elif classification.image_ratio > 0.2 or classification.table_ratio > 0.1:
            return DocumentComplexity.MODERATE
        elif classification.text_ratio > 0.9:
            return DocumentComplexity.SIMPLE
        else:
            return DocumentComplexity.MIXED
    
    def _determine_format(self, classification: DocumentClassification) -> DocumentFormat:
        """Determine document format"""
        if classification.is_scanned:
            return DocumentFormat.SCANNED
        elif classification.formula_ratio > 0.15:
            return DocumentFormat.FORMULA_HEAVY
        elif classification.table_ratio > 0.25:
            return DocumentFormat.TABLE_HEAVY
        elif classification.image_ratio > 0.35:
            return DocumentFormat.IMAGE_HEAVY
        elif classification.text_ratio > 0.85:
            return DocumentFormat.TEXT_ONLY
        else:
            return DocumentFormat.MIXED_MEDIA
    
    def _recommend_parser(self, classification: DocumentClassification) -> ParserRecommendation:
        """Recommend parser based on classification"""
        complexity = classification.complexity
        format_type = classification.format
        
        # Routing logic
        if complexity == DocumentComplexity.SCIENTIFIC or format_type == DocumentFormat.FORMULA_HEAVY:
            return ParserRecommendation(
                parser_type=ParserType.MINERU,
                confidence=0.85,
                rationale="Scientific content with mathematical formulas benefits from MinerU's multi-modal capabilities",
                pros=["Excellent formula extraction", "Good with mixed content", "Handles scientific diagrams"],
                cons=["Higher memory usage", "Slower processing", "More complex setup"],
                estimated_quality="High",
                estimated_speed="Medium"
            )
        
        elif complexity == DocumentComplexity.VERY_COMPLEX or format_type == DocumentFormat.TABLE_HEAVY:
            return ParserRecommendation(
                parser_type=ParserType.DOCLING,
                confidence=0.80,
                rationale="Complex layouts and table-heavy content benefit from Docling's Rust-based performance",
                pros=["Fast processing", "Good table extraction", "Handles complex layouts"],
                cons=["Less support untuk formulas", "Rust-based setup complexity"],
                estimated_quality="High",
                estimated_speed="Fast"
            )
        
        elif format_type == DocumentFormat.SCANNED:
            if self.enable_vision_routing:
                return ParserRecommendation(
                    parser_type=ParserType.VISION,
                    confidence=0.75,
                    rationale="Scanned documents require vision-based OCR and layout analysis",
                    pros=["Best for scanned content", "Can handle handwritten text"],
                    cons=["Highest resource usage", "Slower processing", "Higher error rate"],
                    estimated_quality="Medium-High",
                    estimated_speed="Slow"
                )
            else:
                return ParserRecommendation(
                    parser_type=ParserType.PYMUPDF,
                    confidence=0.60,
                    rationale="Scanned document without vision routing - using basic PDF parser",
                    pros=["Fast processing", "Low resource usage"],
                    cons=["Poor OCR for scanned content", "Limited layout understanding"],
                    estimated_quality="Low-Medium",
                    estimated_speed="Fast"
                )
        
        elif complexity == DocumentComplexity.SIMPLE or format_type == DocumentFormat.TEXT_ONLY:
            return ParserRecommendation(
                parser_type=ParserType.MARKER,
                confidence=0.90,
                rationale="Simple, text-heavy documents are ideal for Markdown-based parsing",
                pros=["Fastest processing", "Excellent text extraction", "Clean Markdown output"],
                cons=["Limited support for complex layouts", "Struggles with tables/images"],
                estimated_quality="High",
                estimated_speed="Very Fast"
            )
        
        else:  # MODERATE or MIXED
            return ParserRecommendation(
                parser_type=ParserType.MINERU,
                confidence=0.75,
                rationale="Mixed content benefits from MinerU's multi-modal approach",
                pros=["Good balance of features", "Handles various content types"],
                cons=["Higher resource usage than simpler parsers"],
                estimated_quality="High",
                estimated_speed="Medium"
            )
    
    def _get_alternative_parsers(self, classification: DocumentClassification) -> List[ParserType]:
        """Get alternative parsers dengan trade-offs"""
        recommended = classification.recommended_parser
        alternatives = []
        
        if recommended != ParserType.PYMUPDF:
            alternatives.append(ParserType.PYMUPDF)  # Always include basic parser
        
        if recommended != ParserType.DOCLING:
            alternatives.append(ParserType.DOCLING)  # Good for complex layouts
        
        if recommended != ParserType.MINERU and classification.complexity != DocumentComplexity.SIMPLE:
            alternatives.append(ParserType.MINERU)  # Good for mixed content
        
        if classification.format == DocumentFormat.TEXT_ONLY and recommended != ParserType.MARKER:
            alternatives.append(ParserType.MARKER)  # Best for text-heavy
        
        return alternatives
    
    def _detect_tables(self, page: fitz.Page) -> List:
        """Detect tables pada page"""
        # Simple heuristic: look untuk tabular patterns
        text = page.get_text()
        tables = []
        
        # Look untuk repeated delimiters yang indicate tabular structure
        lines = text.split('\n')
        for line in lines:
            # Count spaces/tabs sebagai indicator
            if line.count('   ') > 2 or line.count('\t') > 1:
                tables.append(line)
        
        return tables
    
    def _detect_formulas(self, text: str) -> List[str]:
        """Detect mathematical formulas dalam text"""
        formulas = []
        
        # Look untuk LaTeX patterns
        import re
        latex_patterns = [r'\$[^$]+\$', r'\\\[\\\w+\\\]', r'\\begin\{equation\}']
        for pattern in latex_patterns:
            matches = re.findall(pattern, text)
            formulas.extend(matches)
        
        return formulas
    
    def _analyze_formatting(self, page: fitz.Page, text: str) -> float:
        """Analyze formatting complexity (0.0-1.0)"""
        score = 0.0
        
        # Font variety
        try:
            fonts = page.get_fonts()
            if len(fonts) > 3:
                score += 0.2
            if len(fonts) > 5:
                score += 0.1
        except:
            pass
        
        # Text formatting indicators
        if text.count('**') > 5 or text.count('__') > 5:
            score += 0.3
        
        # Structural elements
        if re.search(r'#+\s+', text):  # Headings
            score += 0.2
        if re.search(r'\d+\.\s+', text):  # Numbered lists
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_layout(self, page: fitz.Page) -> float:
        """Analyze layout complexity (0.0-1.0)"""
        score = 0.0
        
        # Get text blocks untuk layout analysis
        try:
            blocks = page.get_text("blocks")
            if len(blocks) > 10:
                score += 0.3
            if len(blocks) > 20:
                score += 0.2
        except:
            pass
        
        # Check untuk columns
        text = page.get_text()
        if text.count('   ') > 10:  # Multiple spaces indicate columns
            score += 0.2
        
        return min(score, 1.0)
    
    def _detect_scientific_diagrams(self, page: fitz.Page) -> bool:
        """Detect scientific diagrams"""
        # Heuristic: check untuk images dengan specific characteristics
        images = page.get_images()
        if len(images) > 2:
            return True
        return False
    
    def _detect_complex_tables(self, page: fitz.Page) -> bool:
        """Detect complex tables"""
        text = page.get_text()
        # Look untuk complex table patterns
        return text.count('|') > 20 or text.count('+') > 10
    
    def _detect_multi_column_layout(self, page: fitz.Page) -> bool:
        """Detect multi-column layout"""
        try:
            blocks = page.get_text("blocks")
            if len(blocks) > 0:
                # Check jika blocks are arranged secara horizontal
                return True
        except:
            pass
        return False
    
    def _is_textbook(self, text: str) -> bool:
        """Check jika document appears to be a textbook"""
        keywords = ['bab', 'chapter', 'materi', 'pelajaran', 'soal', 'latihan']
        return any(keyword.lower() in text.lower() for keyword in keywords)
    
    def _is_scanned(self, page: fitz.Page) -> bool:
        """Check jika document is scanned"""
        # Heuristic: check untuk low text extraction yang indicates scan
        text = page.get_text()
        return len(text.strip()) < 50
    
    def _estimate_processing_time(self, classification: DocumentClassification) -> float:
        """Estimate processing time in seconds"""
        base_time = classification.page_count * 0.5  # Base time per page
        
        multipliers = {
            DocumentComplexity.SIMPLE: 1.0,
            DocumentComplexity.MODERATE: 1.5,
            DocumentComplexity.COMPLEX: 2.0,
            DocumentComplexity.VERY_COMPLEX: 3.0,
            DocumentComplexity.SCIENTIFIC: 2.5,
            DocumentComplexity.MIXED: 1.8
        }
        
        parser_multipliers = {
            ParserType.MARKER: 0.5,
            ParserType.PYMUPDF: 0.8,
            ParserType.DOCLING: 0.7,
            ParserType.MINERU: 1.2,
            ParserType.VISION: 2.0
        }
        
        complexity_mult = multipliers.get(classification.complexity, 1.5)
        parser_mult = parser_multipliers.get(classification.recommended_parser, 1.0)
        
        return base_time * complexity_mult * parser_mult
    
    def _estimate_memory_requirement(self, classification: DocumentClassification) -> float:
        """Estimate memory requirement in MB"""
        base_memory = classification.page_count * 5  # Base memory per page
        
        complexity_multiplier = {
            DocumentComplexity.SIMPLE: 1.0,
            DocumentComplexity.MODERATE: 1.5,
            DocumentComplexity.COMPLEX: 2.0,
            DocumentComplexity.VERY_COMPLEX: 3.0,
            DocumentComplexity.SCIENTIFIC: 2.5,
            DocumentComplexity.MIXED: 1.8
        }.get(classification.complexity, 1.5)
        
        return base_memory * complexity_multiplier