"""
Region Classifier - Semantic Region Type Classification

Classifies regions into semantic types based on content, position, and formatting.
This enhances the basic layout detection with more granular semantic understanding.

Supports hybrid approach: ML-based classification with rule-based fallback.
"""

import logging
import re
from typing import Optional, Dict, Any, List
from enum import Enum
from pathlib import Path

from app.models.document_models import Region, RegionType, Page

logger = logging.getLogger(__name__)


class SemanticRegionType(str, Enum):
    """
    Enhanced semantic region types beyond basic RegionType.
    These provide more granular classification for educational content.
    """
    # Document structure
    DOCUMENT_TITLE = "document_title"           # Main document title
    CHAPTER_TITLE = "chapter_title"             # Chapter/section title
    SECTION_TITLE = "section_title"             # Section heading
    SUBSECTION_TITLE = "subsection_title"       # Subsection heading
    HEADING = "heading"                         # Generic heading
    
    # Content types
    PARAGRAPH = "paragraph"                     # Standard paragraph text
    INTRODUCTION = "introduction"               # Introduction section
    CONCLUSION = "conclusion"                   # Conclusion section
    SUMMARY = "summary"                        # Summary section
    
    # Educational content
    LEARNING_OBJECTIVE = "learning_objective"   # Learning objectives
    COMPETENCY = "competency"                   # Competency statement
    ASSESSMENT = "assessment"                   # Assessment/question
    EXERCISE = "exercise"                       # Exercise/problem
    EXAMPLE = "example"                         # Example with solution
    
    # Lists and enumerations
    LIST_ITEM = "list_item"                     # List item (bulleted/numbered)
    ENUMERATION = "enumeration"                 # Numbered list
    DEFINITION = "definition"                   # Definition block
    
    # Special content
    FOOTNOTE = "footnote"                       # Footnote
    CAPTION = "caption"                         # Figure/table caption
    QUOTE = "quote"                             # Block quote
    CODE = "code"                               # Code block
    
    # Unknown
    UNKNOWN = "unknown"


class RegionClassifier:
    """
    Classifies regions into semantic types based on content analysis.
    
    This classifier uses multiple heuristics:
    - Text patterns (headings, lists, etc.)
    - Position on page (top, bottom, margins)
    - Formatting hints (font size, bold, etc.)
    - Content keywords (objectives, assessment, etc.)
    """
    
    # Heading patterns
    HEADING_PATTERNS = [
        r'^[A-Z\s]+$',  # All caps
        r'^\d+\.\s+[A-Z]',  # Numbered heading (1. Title)
        r'^[IVXLCDM]+\.\s+[A-Z]',  # Roman numeral heading
        r'^[A-Z][a-z]+\s+\d+$',  # Chapter X
        r'^BAB\s+\d+',  # Indonesian: BAB X
        r'^SUB\s+BAB\s+\d+',  # Indonesian: SUB BAB X
    ]
    
    # Educational content keywords
    LEARNING_OBJECTIVE_KEYWORDS = [
        'tujuan pembelajaran', 'learning objective', 'learning outcomes',
        'kompetensi dasar', 'kompetensi inti', 'indikator pencapaian'
    ]
    
    ASSESSMENT_KEYWORDS = [
        'latihan', 'soal', 'tes', 'ujian', 'assessment', 'exercise',
        'evaluasi', 'tes formatif', 'tes sumatif'
    ]
    
    EXAMPLE_KEYWORDS = [
        'contoh', 'example', 'for example', 'misalnya', 'sebagai contoh'
    ]
    
    DEFINITION_KEYWORDS = [
        'definisi', 'definition', 'adalah', 'yaitu', 'merupakan',
        'didefinisikan sebagai', 'dapat diartikan'
    ]
    
    # List patterns
    LIST_PATTERNS = [
        r'^\d+\.',  # 1. 2. 3.
        r'^[a-z]\.',  # a. b. c.
        r'^[A-Z]\.',  # A. B. C.
        r'^[ivxlcdm]+\.',  # i. ii. iii.
        r'^[-•●○]',  # Bullet points
    ]
    
    def __init__(self, enable_enhanced_classification: bool = True, use_ml: bool = False, ml_model_path: Optional[str] = None):
        """
        Initialize region classifier.
        
        Args:
            enable_enhanced_classification: Enable enhanced semantic classification
            use_ml: Enable ML-based classification (requires scikit-learn)
            ml_model_path: Path to saved ML model file
        """
        self.enable_enhanced_classification = enable_enhanced_classification
        self.use_ml = use_ml
        self.ml_classifier = None
        
        if use_ml:
            try:
                from app.pipelines.ml_region_classifier import MLRegionClassifier
                self.ml_classifier = MLRegionClassifier(model_path=ml_model_path)
                if self.ml_classifier.use_ml:
                    logger.info("ML-based region classification enabled")
                else:
                    logger.info("ML model not available, using rule-based classification")
            except ImportError:
                logger.warning("ML region classifier not available, using rule-based only")
                self.use_ml = False
        
        logger.info("RegionClassifier initialized")
    
    def classify_region(
        self, 
        region: Region, 
        page: Optional[Page] = None,
        page_number: int = 1,
        page_width: float = 595,
        page_height: float = 842,
        context: Optional[Dict[str, Any]] = None
    ) -> SemanticRegionType:
        """
        Classify a region into a semantic type.
        
        Args:
            region: Region to classify
            page: Page object (required for ML classification)
            page_number: Page number (1-indexed)
            page_width: Page width in points
            page_height: Page height in points
            context: Additional context (document type, etc.)
            
        Returns:
            SemanticRegionType classification
        """
        # Try ML classification first if enabled
        if self.use_ml and self.ml_classifier and page:
            try:
                ml_region_type, confidence = self.ml_classifier.predict(region, page)
                # Map RegionType to SemanticRegionType
                semantic_type = self._map_region_to_semantic(ml_region_type)
                if confidence > 0.6:
                    region.metadata = region.metadata or {}
                    region.metadata['ml_confidence'] = confidence
                    region.metadata['classification_method'] = 'ml'
                    return semantic_type
            except Exception as e:
                logger.warning(f"ML classification failed: {e}, falling back to rule-based")
        
        # Fall back to rule-based classification
        if not self.enable_enhanced_classification:
            return self._basic_classification(region)
        
        text = region.text_content or ""
        
        # Check for specific semantic types
        semantic_type = self._check_learning_objective(text)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_assessment(text)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_example(text)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_definition(text)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_list_item(text)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_heading(text, region, page_number)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_caption(text, region.region_type)
        if semantic_type:
            return semantic_type
        
        semantic_type = self._check_footnote(text, region, page_height)
        if semantic_type:
            return semantic_type
        
        # Default to paragraph for text content
        if text.strip():
            return SemanticRegionType.PARAGRAPH
        
        return SemanticRegionType.UNKNOWN
    
    def _map_region_to_semantic(self, region_type: RegionType) -> SemanticRegionType:
        """Map RegionType to SemanticRegionType"""
        mapping = {
            RegionType.TITLE: SemanticRegionType.DOCUMENT_TITLE,
            RegionType.HEADING: SemanticRegionType.HEADING,
            RegionType.SUBHEADING: SemanticRegionType.SUBSECTION_TITLE,
            RegionType.PARAGRAPH: SemanticRegionType.PARAGRAPH,
            RegionType.LIST: SemanticRegionType.LIST_ITEM,
            RegionType.LIST_ITEM: SemanticRegionType.LIST_ITEM,
            RegionType.TABLE: SemanticRegionType.UNKNOWN,
            RegionType.FIGURE: SemanticRegionType.UNKNOWN,
            RegionType.FORMULA: SemanticRegionType.UNKNOWN,
            RegionType.FOOTER: SemanticRegionType.FOOTNOTE,
            RegionType.HEADER: SemanticRegionType.UNKNOWN,
            RegionType.PAGE_NUMBER: SemanticRegionType.UNKNOWN,
        }
        return mapping.get(region_type, SemanticRegionType.PARAGRAPH)
    
    def _basic_classification(self, region: Region) -> SemanticRegionType:
        """
        Basic classification using only RegionType.
        
        Maps basic RegionType to SemanticRegionType.
        """
        mapping = {
            RegionType.TITLE: SemanticRegionType.DOCUMENT_TITLE,
            RegionType.HEADING: SemanticRegionType.HEADING,
            RegionType.SUBHEADING: SemanticRegionType.SUBSECTION_TITLE,
            RegionType.PARAGRAPH: SemanticRegionType.PARAGRAPH,
            RegionType.LIST: SemanticRegionType.LIST_ITEM,
            RegionType.TABLE: SemanticRegionType.UNKNOWN,  # Tables are handled separately
            RegionType.FIGURE: SemanticRegionType.UNKNOWN,  # Figures are handled separately
            RegionType.FORMULA: SemanticRegionType.UNKNOWN,  # Formulas are handled separately
            RegionType.FOOTER: SemanticRegionType.FOOTNOTE,
            RegionType.HEADER: SemanticRegionType.UNKNOWN,
            RegionType.PAGE_NUMBER: SemanticRegionType.UNKNOWN,
        }
        
        return mapping.get(region.region_type, SemanticRegionType.UNKNOWN)
    
    def _check_learning_objective(self, text: str) -> Optional[SemanticRegionType]:
        """Check if text is a learning objective."""
        text_lower = text.lower().strip()
        
        for keyword in self.LEARNING_OBJECTIVE_KEYWORDS:
            if keyword in text_lower:
                return SemanticRegionType.LEARNING_OBJECTIVE
        
        return None
    
    def _check_assessment(self, text: str) -> Optional[SemanticRegionType]:
        """Check if text is an assessment/exercise."""
        text_lower = text.lower().strip()
        
        for keyword in self.ASSESSMENT_KEYWORDS:
            if keyword in text_lower:
                return SemanticRegionType.ASSESSMENT
        
        return None
    
    def _check_example(self, text: str) -> Optional[SemanticRegionType]:
        """Check if text is an example."""
        text_lower = text.lower().strip()
        
        for keyword in self.EXAMPLE_KEYWORDS:
            if keyword in text_lower:
                return SemanticRegionType.EXAMPLE
        
        return None
    
    def _check_definition(self, text: str) -> Optional[SemanticRegionType]:
        """Check if text is a definition."""
        text_lower = text.lower().strip()
        
        for keyword in self.DEFINITION_KEYWORDS:
            if keyword in text_lower:
                return SemanticRegionType.DEFINITION
        
        return None
    
    def _check_list_item(self, text: str) -> Optional[SemanticRegionType]:
        """Check if text is a list item."""
        for pattern in self.LIST_PATTERNS:
            if re.match(pattern, text.strip()):
                return SemanticRegionType.LIST_ITEM
        
        return None
    
    def _check_heading(
        self, 
        text: str, 
        region: Region, 
        page_number: int
    ) -> Optional[SemanticRegionType]:
        """Check if text is a heading."""
        text_stripped = text.strip()
        
        # Check heading patterns
        for pattern in self.HEADING_PATTERNS:
            if re.match(pattern, text_stripped):
                # Determine heading level based on position and content
                if page_number == 1 and region.bbox.y1 < 100:
                    return SemanticRegionType.DOCUMENT_TITLE
                elif 'BAB' in text_stripped or 'CHAPTER' in text_stripped.upper():
                    return SemanticRegionType.CHAPTER_TITLE
                else:
                    return SemanticRegionType.SECTION_TITLE
        
        # Check if it's short and at the top of the page
        if len(text_stripped) < 100 and region.bbox.y1 < 150:
            if text_stripped.isupper() or text_stripped.istitle():
                return SemanticRegionType.HEADING
        
        return None
    
    def _check_caption(
        self, 
        text: str, 
        region_type: RegionType
    ) -> Optional[SemanticRegionType]:
        """Check if text is a caption."""
        text_lower = text.lower().strip()
        
        # Caption prefixes
        caption_prefixes = ['gambar', 'tabel', 'figure', 'fig.', 'table', 'ilustrasi']
        
        for prefix in caption_prefixes:
            if text_lower.startswith(prefix):
                return SemanticRegionType.CAPTION
        
        return None
    
    def _check_footnote(
        self, 
        text: str, 
        region: Region, 
        page_height: float
    ) -> Optional[SemanticRegionType]:
        """Check if text is a footnote."""
        # Footnotes are typically at the bottom of the page
        if region.bbox.y2 > page_height - 100:
            # Check for footnote markers (superscript numbers)
            if re.match(r'^\d+\s+', text.strip()):
                return SemanticRegionType.FOOTNOTE
        
        return None
    
    def classify_regions(
        self, 
        regions: List[Region], 
        page: Optional[Page] = None,
        page_number: int = 1,
        page_width: float = 595,
        page_height: float = 842,
        context: Optional[Dict[str, Any]] = None
    ) -> List[SemanticRegionType]:
        """
        Classify multiple regions.
        
        Args:
            regions: List of regions to classify
            page: Page object (required for ML classification)
            page_number: Page number (1-indexed)
            page_width: Page width in points
            page_height: Page height in points
            context: Additional context
            
        Returns:
            List of semantic types corresponding to regions
        """
        classifications = []
        
        for region in regions:
            semantic_type = self.classify_region(
                region, page, page_number, page_width, page_height, context
            )
            classifications.append(semantic_type)
            
            # Store classification in region metadata
            region.metadata = region.metadata or {}
            region.metadata['semantic_type'] = semantic_type.value
        
        logger.info(f"Classified {len(regions)} regions on page {page_number}")
        
        return classifications
