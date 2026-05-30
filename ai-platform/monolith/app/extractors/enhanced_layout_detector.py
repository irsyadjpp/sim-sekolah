"""
Enhanced Layout Detector for Document Understanding

Modern layout detection that returns page-centric regions with semantic classification.
This is the foundation for layout-first document understanding.

Key improvements over basic layout detector:
- Returns Region objects with semantic types
- Page-centric structure
- Standardized bounding boxes
- Region classification (title, paragraph, list, table, etc.)
- Reading order support
"""
import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import logging
import re

from app.models.document_models import (
    Region, RegionType, BoundingBox, Element, ElementType, Page
)
from app.pipelines.pipeline_context import PipelineContext

logger = logging.getLogger(__name__)


class EnhancedLayoutDetector:
    """
    Enhanced layout detector for modern document understanding.
    
    Returns page-centric regions with semantic classification.
    This is the first stage in the layout-first pipeline.
    """
    
    def __init__(self, use_ai_classification: bool = False):
        """
        Initialize enhanced layout detector.
        
        Args:
            use_ai_classification: Whether to use AI/ML for region classification
                                  (requires ML models, currently heuristic-based)
        """
        self.use_ai_classification = use_ai_classification
        
        # Heading patterns for classification
        self.heading_patterns = [
            r'^[A-Z][A-Z\s]{5,}$',  # All caps headings
            r'^\d+\.\s+[A-Z]',  # Numbered sections (1. Introduction)
            r'^[IVX]+\.\s+[A-Z]',  # Roman numeral sections
            r'^BAB\s+[IVX]+',  # Indonesian "BAB I", "BAB II"
            r'^Chapter\s+\d+',  # English chapters
        ]
        
        # List patterns
        self.list_patterns = [
            r'^\s*[\-\•\*]\s+',  # Bullet points
            r'^\s*\d+[.)\]]\s+',  # Numbered lists
            r'^\s*[a-z][.)\]]\s+',  # Lettered lists
        ]
        
        logger.info("EnhancedLayoutDetector initialized with semantic region classification")
    
    def detect(
        self, 
        file_path: str, 
        context: PipelineContext
    ) -> Dict[int, List[Region]]:
        """
        Detect layout structure and return page-centric regions.
        
        This is the FIRST stage in the modern pipeline.
        
        Args:
            file_path: Path to PDF file
            context: Pipeline context for caching and state sharing
            
        Returns:
            Dictionary mapping page_number → List[Region]
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension != '.pdf':
                logger.warning(f"Enhanced layout detection optimized for PDF, got {file_extension}")
                return {}
            
            return self._detect_from_pdf(file_path, context)
                
        except Exception as e:
            logger.error(f"Error in enhanced layout detection: {str(e)}")
            context.add_error(f"Layout detection failed: {str(e)}")
            return {}
    
    def _detect_from_pdf(
        self, 
        file_path: str, 
        context: PipelineContext
    ) -> Dict[int, List[Region]]:
        """Detect layout in PDF document with semantic classification"""
        try:
            doc = fitz.open(file_path)
            all_regions = {}
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_number = page_num + 1
                
                # Get or create page in context
                page_width = page.rect.width
                page_height = page.rect.height
                context.get_or_create_page(page_number, page_width, page_height)
                
                # Detect regions on this page
                page_regions = self._detect_page_regions(page, page_number, context)
                
                # Cache regions in context
                context.set_regions_for_page(page_number, page_regions)
                
                all_regions[page_number] = page_regions
                
                logger.info(f"Detected {len(page_regions)} regions on page {page_number}")
            
            doc.close()
            logger.info(f"Total regions detected across {len(all_regions)} pages")
            
            return all_regions
            
        except Exception as e:
            logger.error(f"Error detecting layout from PDF: {str(e)}")
            context.add_error(f"PDF layout detection failed: {str(e)}")
            return {}
    
    def _detect_page_regions(
        self, 
        page: fitz.Page, 
        page_number: int,
        context: PipelineContext
    ) -> List[Region]:
        """Detect all regions on a single page with semantic classification"""
        regions = []
        
        # 1. Detect structural regions (header, footer, page number)
        regions.extend(self._detect_structural_regions(page, page_number))
        
        # 2. Detect tables
        regions.extend(self._detect_table_regions(page, page_number))
        
        # 3. Detect images/figures
        regions.extend(self._detect_image_regions(page, page_number))
        
        # 4. Detect text blocks and classify them
        text_regions = self._detect_and_classify_text_blocks(page, page_number)
        regions.extend(text_regions)
        
        # 5. Merge overlapping regions (resolve conflicts)
        regions = self._merge_overlapping_regions(regions)
        
        # 6. Assign reading order (preliminary, refined later)
        regions = self._assign_preliminary_reading_order(regions, page.rect.height)
        
        return regions
    
    def _detect_structural_regions(
        self, 
        page: fitz.Page, 
        page_number: int
    ) -> List[Region]:
        """Detect header, footer, and page number regions"""
        regions = []
        page_width = page.rect.width
        page_height = page.rect.height
        
        # Header region (top 10%)
        header_bbox = BoundingBox(0, 0, page_width, page_height * 0.1)
        header_text = page.get_text("text", clip=fitz.Rect(*header_bbox.to_list()))
        
        if header_text.strip():
            region = Region(
                region_id=f"header_p{page_number}",
                region_type=RegionType.HEADER,
                bbox=header_bbox,
                page_number=page_number,
                text_content=header_text.strip(),
                confidence=0.8
            )
            regions.append(region)
        
        # Footer region (bottom 10%)
        footer_y = page_height * 0.9
        footer_bbox = BoundingBox(0, footer_y, page_width, page_height)
        footer_text = page.get_text("text", clip=fitz.Rect(*footer_bbox.to_list()))
        
        if footer_text.strip():
            region = Region(
                region_id=f"footer_p{page_number}",
                region_type=RegionType.FOOTER,
                bbox=footer_bbox,
                page_number=page_number,
                text_content=footer_text.strip(),
                confidence=0.8
            )
            regions.append(region)
        
        # Page number detection (look for numbers in header/footer)
        page_number_pattern = re.search(r'\b\d+\b', header_text + " " + footer_text)
        if page_number_pattern:
            pn_text = page_number_pattern.group()
            # Try to locate the page number more precisely
            # For now, just mark it as detected in metadata
            if regions:
                regions[-1].metadata["contains_page_number"] = True
                regions[-1].metadata["page_number_text"] = pn_text
        
        return regions
    
    def _detect_table_regions(
        self, 
        page: fitz.Page, 
        page_number: int
    ) -> List[Region]:
        """Detect table regions using PyMuPDF's table detection"""
        regions = []
        
        try:
            tables_found = page.find_tables()
            
            for table_num, table in enumerate(tables_found.tables):
                bbox = BoundingBox.from_list(list(table.bbox))
                
                region = Region(
                    region_id=f"table_p{page_number}_t{table_num}",
                    region_type=RegionType.TABLE,
                    bbox=bbox,
                    page_number=page_number,
                    confidence=0.9,
                    metadata={
                        "table_number": table_num + 1,
                        "row_count": len(table.extract()),
                        "bbox_source": "pymupdf_find_tables"
                    }
                )
                regions.append(region)
                
        except Exception as e:
            logger.warning(f"Error detecting tables on page {page_number}: {e}")
        
        return regions
    
    def _detect_image_regions(
        self, 
        page: fitz.Page, 
        page_number: int
    ) -> List[Region]:
        """Detect image/figure regions"""
        regions = []
        
        try:
            image_list = page.get_images(full=True)
            
            for img_num, img_info in enumerate(image_list):
                xref = img_info[0]
                
                # Try to get image position
                # PyMuPDF doesn't directly give image positions, so we need to search
                # This is a simplified approach - production would use more sophisticated methods
                try:
                    # Get image rectangles
                    image_rects = page.get_image_rects(xref)
                    
                    for rect in image_rects:
                        bbox = BoundingBox(rect.x0, rect.y0, rect.x1, rect.y1)
                        
                        # Filter out very small images (likely text artifacts)
                        # Minimum size: 50x50 pixels
                        if bbox.width < 50 or bbox.height < 50:
                            logger.debug(f"Skipping small image artifact: {bbox.width}x{bbox.height}")
                            continue
                        
                        region = Region(
                            region_id=f"image_p{page_number}_i{img_num}",
                            region_type=RegionType.FIGURE,
                            bbox=bbox,
                            page_number=page_number,
                            confidence=0.7,
                            metadata={
                                "image_number": img_num + 1,
                                "xref": xref,
                                "bbox_source": "pymupdf_get_image_rects"
                            }
                        )
                        regions.append(region)
                        
                except Exception as e:
                    logger.debug(f"Could not get position for image {xref}: {e}")
                    # Skip images we can't position
                    continue
                
        except Exception as e:
            logger.warning(f"Error detecting images on page {page_number}: {e}")
        
        return regions
    
    def _detect_and_classify_text_blocks(
        self, 
        page: fitz.Page, 
        page_number: int
    ) -> List[Region]:
        """Detect text blocks and classify them semantically"""
        regions = []
        
        try:
            # Try multiple text extraction methods for better coverage
            # Method 1: get_text("blocks") - good for structured text
            blocks = page.get_text("blocks")
            
            # Method 2: get_text("text") - fallback for unstructured text
            full_text = page.get_text("text")
            
            # Method 3: get_text("words") - for word-level precision
            words = page.get_text("words")
            
            # For mathematical documents like bkb10.pdf, blocks may not work well
            # Force word-based detection if blocks are insufficient
            if not blocks or len(blocks) == 0:
                logger.warning(f"No blocks detected on page {page_number}, using word-based detection")
                return self._detect_from_words(words, page, page_number)
            
            # Try blocks first
            for block_num, block in enumerate(blocks):
                # PyMuPDF blocks are tuples, not dicts
                # block format: (x0, y0, x1, y1, text, block_type, ...)
                if len(block) < 6:
                    continue
                
                block_type = block[5]  # block type (0 = text)
                if block_type != 0:  # Skip non-text blocks
                    continue
                
                bbox = BoundingBox(block[0], block[1], block[2], block[3])
                text = block[4] if len(block) > 4 else ''
                text = text.strip()
                
                if not text:
                    continue
                
                # Classify the text block
                region_type = self._classify_text_block(text, bbox, page)
                
                region = Region(
                    region_id=f"text_p{page_number}_b{block_num}",
                    region_type=region_type,
                    bbox=bbox,
                    page_number=page_number,
                    text_content=text,
                    confidence=self._calculate_classification_confidence(text, region_type),
                    metadata={
                        "block_number": block_num + 1,
                        "bbox_source": "pymupdf_get_text_blocks"
                    }
                )
                
                regions.append(region)
            
            # If blocks don't yield enough content (less than 5 regions), use word-based detection
            # This handles mathematical documents where blocks don't capture content well
            if len(regions) < 5:
                logger.warning(f"Insufficient blocks ({len(regions)}) on page {page_number}, using word-based detection")
                regions = self._detect_from_words(words, page, page_number)
                
        except Exception as e:
            logger.warning(f"Error detecting text blocks on page {page_number}: {e}")
            # Fallback to word-based detection
            try:
                words = page.get_text("words")
                regions = self._detect_from_words(words, page, page_number)
            except Exception as e2:
                logger.error(f"Fallback word detection also failed on page {page_number}: {e2}")
        
        return regions
    
    def _detect_from_words(
        self, 
        words: List, 
        page: fitz.Page, 
        page_number: int
    ) -> List[Region]:
        """Detect text regions from word-level data (fallback method)"""
        regions = []
        
        if not words:
            return regions
        
        try:
            # Group words into lines based on Y position
            lines = {}
            for word in words:
                # word format: (x0, y0, x1, y1, text, block_no, block_type)
                if len(word) < 5:
                    continue
                
                y_pos = word[1]
                # Round Y position to group nearby words
                y_key = round(y_pos, 1)
                
                if y_key not in lines:
                    lines[y_key] = []
                lines[y_key].append(word)
            
            # Convert lines to regions
            for line_num, (y_pos, line_words) in enumerate(sorted(lines.items())):
                if not line_words:
                    continue
                
                # Calculate bounding box for the line
                x0 = min(w[0] for w in line_words)
                y0 = min(w[1] for w in line_words)
                x1 = max(w[2] for w in line_words)
                y1 = max(w[3] for w in line_words)
                
                # Concatenate text
                text = " ".join(w[4] for w in line_words if len(w) > 4)
                text = text.strip()
                
                if not text:
                    continue
                
                bbox = BoundingBox(x0, y0, x1, y1)
                
                # Classify the line
                region_type = self._classify_text_block(text, bbox, page)
                
                region = Region(
                    region_id=f"text_p{page_number}_l{line_num}",
                    region_type=region_type,
                    bbox=bbox,
                    page_number=page_number,
                    text_content=text,
                    confidence=0.6,  # Lower confidence for word-based detection
                    metadata={
                        "line_number": line_num + 1,
                        "bbox_source": "pymupdf_get_text_words"
                    }
                )
                
                regions.append(region)
                
        except Exception as e:
            logger.error(f"Error in word-based detection on page {page_number}: {e}")
        
        return regions
    
    def _classify_text_block(
        self, 
        text: str, 
        bbox: BoundingBox,
        page: fitz.Page
    ) -> RegionType:
        """
        Classify text block into semantic region type.
        
        This is where the magic happens - understanding document structure.
        """
        # Skip very short text blocks (likely noise)
        if len(text.strip()) < 3:
            return RegionType.UNKNOWN
        
        # Check for headings (most important - do this first)
        if self._is_heading(text, bbox, page):
            return self._get_heading_level(text)
        
        # Check for lists
        if self._is_list(text):
            return RegionType.LIST
        
        # Check for captions
        if self._is_caption(text):
            return RegionType.CAPTION
        
        # Check for footnotes
        if self._is_footnote(text, bbox, page):
            return RegionType.FOOTNOTE
        
        # Check if it's mathematical content (formulas, equations)
        if self._is_mathematical_content(text):
            return RegionType.FORMULA
        
        # Check if it's a page number (very short, numeric, at bottom)
        if self._is_page_number(text, bbox, page):
            return RegionType.PAGE_NUMBER
        
        # Default to paragraph for any text content
        # This is the fallback for normal content
        return RegionType.PARAGRAPH
    
    def _is_page_number(self, text: str, bbox: BoundingBox, page: fitz.Page) -> bool:
        """Check if text is a page number"""
        # Page numbers are typically:
        # - Very short (1-3 characters)
        # - Numeric
        # - At bottom of page
        # - Small font size (inferred from bbox height)
        
        text = text.strip()
        
        # Must be numeric
        if not text.isdigit():
            return False
        
        # Must be short
        if len(text) > 3:
            return False
        
        # Must be at bottom of page (last 15%)
        if bbox.y1 < page.rect.height * 0.85:
            return False
        
        # Must be small (height < 20 pixels)
        if bbox.height > 20:
            return False
        
        return True
    
    def _is_mathematical_content(self, text: str) -> bool:
        """Check if text appears to be mathematical content"""
        # Check for mathematical symbols and patterns
        math_indicators = ['=', '+', '-', '×', '÷', '∫', '∑', '√', 'π', '∞', '≤', '≥', '≠']
        math_count = sum(1 for indicator in math_indicators if indicator in text)
        
        # If it has multiple math symbols and numbers, likely mathematical
        if math_count >= 2 and any(c.isdigit() for c in text):
            return True
        
        return False
    
    def _is_heading(self, text: str, bbox: BoundingBox, page: fitz.Page) -> bool:
        """Check if text block is a heading"""
        # Check heading patterns
        for pattern in self.heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Check position (top of page)
        if bbox.y1 < page.rect.height * 0.15:
            return True
        
        # Check if short and possibly bold (heuristic)
        if len(text) < 100 and len(text.split()) < 10:
            return True
        
        return False
    
    def _get_heading_level(self, text: str) -> RegionType:
        """Determine heading level based on text patterns"""
        # Main title (all caps, very short)
        if text.isupper() and len(text.split()) <= 5:
            return RegionType.TITLE
        
        # Subtitle (mixed case, short)
        if len(text.split()) <= 8:
            return RegionType.SUBTITLE
        
        # Numbered heading (1., 2., etc.)
        if re.match(r'^\d+\.', text):
            return RegionType.HEADING
        
        # Lettered heading (a., b., etc.)
        if re.match(r'^[a-z]\.', text):
            return RegionType.SUBHEADING
        
        # Default heading
        return RegionType.HEADING
    
    def _is_list(self, text: str) -> bool:
        """Check if text is a list item"""
        for pattern in self.list_patterns:
            if re.match(pattern, text):
                return True
        return False
    
    def _is_caption(self, text: str) -> bool:
        """Check if text is a caption (Figure 1, Table 1, etc.)"""
        caption_patterns = [
            r'^(Gambar|Figure|Fig\.|Tabel|Table)\s+\d+',
            r'^\d+\.\s+(Gambar|Figure|Tabel|Table)',
        ]
        for pattern in caption_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _is_footnote(self, text: str, bbox: BoundingBox, page: fitz.Page) -> bool:
        """Check if text is a footnote"""
        # Footnotes are typically at the bottom of the page
        if bbox.y1 > page.rect.height * 0.85:
            # Check for footnote markers (superscript numbers)
            if re.match(r'^\d+\s+', text):
                return True
        return False
    
    def _calculate_classification_confidence(self, text: str, region_type: RegionType) -> float:
        """Calculate confidence score for region classification"""
        base_confidence = 0.7
        
        # Higher confidence for clear patterns
        if region_type == RegionType.TITLE and text.isupper():
            return 0.9
        if region_type == RegionType.HEADING and re.match(r'^\d+\.', text):
            return 0.85
        if region_type == RegionType.LIST:
            return 0.8
        if region_type == RegionType.CAPTION:
            return 0.85
        
        return base_confidence
    
    def _estimate_font_size(self, block: Dict[str, Any]) -> float:
        """Estimate font size from block (heuristic)"""
        # PyMuPDF doesn't directly give font size in blocks
        # This is a simplified heuristic
        return 12.0  # Default assumption
    
    def _is_bold(self, block: Dict[str, Any]) -> bool:
        """Check if block is bold (heuristic)"""
        # PyMuPDF doesn't directly give bold info in blocks
        # This would need font analysis in production
        return False
    
    def _extract_words_from_block(self, block: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract individual words from text block"""
        # PyMuPDF blocks don't directly give word positions
        # This is a simplified approach
        text = block.get('text', '')
        bbox = block['bbox']
        
        # Split text into words and approximate positions
        words = text.split()
        if not words:
            return []
        
        # Approximate word positions (linear distribution)
        word_width = (bbox[2] - bbox[0]) / len(words)
        word_data = []
        
        for i, word in enumerate(words):
            word_bbox = [
                bbox[0] + (i * word_width),
                bbox[1],
                bbox[0] + ((i + 1) * word_width),
                bbox[3]
            ]
            word_data.append({
                'text': word,
                'bbox': word_bbox
            })
        
        return word_data
    
    def _merge_overlapping_regions(self, regions: List[Region]) -> List[Region]:
        """Merge overlapping regions to avoid conflicts"""
        # Simplified approach - in production, use more sophisticated merging
        # For now, just return as-is
        return regions
    
    def _assign_preliminary_reading_order(
        self, 
        regions: List[Region], 
        page_height: float
    ) -> List[Region]:
        """
        Assign preliminary reading order based on Y position.
        
        This is a simple top-to-bottom ordering.
        More sophisticated reading order reconstruction happens later.
        """
        # Sort by Y position (top to bottom)
        sorted_regions = sorted(regions, key=lambda r: r.bbox.y1)
        
        # Assign reading order
        for order, region in enumerate(sorted_regions):
            region.reading_order = order
        
        return sorted_regions
