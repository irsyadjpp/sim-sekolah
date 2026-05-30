import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class LayoutDetector:
    """Detect document layout and structure using PyMuPDF"""
    
    def __init__(self):
        """Initialize layout detector"""
        self.supported_formats = ['.pdf']
    
    def detect(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Detect layout structure in document
        
        Args:
            file_path: Path to document file
            options: Detection options
            
        Returns:
            List of layout regions
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension != '.pdf':
                logger.warning(f"Layout detection optimized for PDF, got {file_extension}")
                return []
            
            return self._detect_from_pdf(file_path)
                
        except Exception as e:
            logger.error(f"Error detecting layout in {file_path}: {str(e)}")
            return []
    
    def _detect_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Detect layout in PDF document"""
        try:
            doc = fitz.open(file_path)
            layout_regions = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_width = page.rect.width
                page_height = page.rect.height
                
                # Detect various layout elements
                
                # Headers (top of page)
                header_region = self._detect_header(page, page_width, page_height)
                if header_region:
                    layout_regions.append(header_region)
                
                # Footers (bottom of page)
                footer_region = self._detect_footer(page, page_width, page_height)
                if footer_region:
                    layout_regions.append(footer_region)
                
                # Tables
                table_regions = self._detect_tables(page)
                layout_regions.extend(table_regions)
                
                # Images
                image_regions = self._detect_images(page)
                layout_regions.extend(image_regions)
                
                # Text blocks
                text_regions = self._detect_text_blocks(page)
                layout_regions.extend(text_regions)
                
                logger.info(f"Detected {len(layout_regions)} regions on page {page_num + 1}")
            
            doc.close()
            logger.info(f"Total layout regions detected: {len(layout_regions)}")
            
            return layout_regions
            
        except Exception as e:
            logger.error(f"Error detecting layout from PDF: {str(e)}")
            return []
    
    def _detect_header(self, page, page_width: float, page_height: float) -> Optional[Dict[str, Any]]:
        """Detect header region at top of page"""
        try:
            # Define header region (top 10% of page)
            header_height = page_height * 0.1
            header_rect = fitz.Rect(0, 0, page_width, header_height)
            
            # Check if there's text in header region
            header_text = page.get_text("text", clip=header_rect)
            
            if header_text.strip():
                return {
                    "region_type": "header",
                    "page_number": page.number + 1,
                    "bbox": [0, 0, page_width, header_height],
                    "content": header_text.strip(),
                    "confidence": 0.8
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Error detecting header: {str(e)}")
            return None
    
    def _detect_footer(self, page, page_width: float, page_height: float) -> Optional[Dict[str, Any]]:
        """Detect footer region at bottom of page"""
        try:
            # Define footer region (bottom 10% of page)
            footer_height = page_height * 0.1
            footer_y = page_height - footer_height
            footer_rect = fitz.Rect(0, footer_y, page_width, page_height)
            
            # Check if there's text in footer region
            footer_text = page.get_text("text", clip=footer_rect)
            
            if footer_text.strip():
                return {
                    "region_type": "footer",
                    "page_number": page.number + 1,
                    "bbox": [0, footer_y, page_width, page_height],
                    "content": footer_text.strip(),
                    "confidence": 0.8
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Error detecting footer: {str(e)}")
            return None
    
    def _detect_tables(self, page) -> List[Dict[str, Any]]:
        """Detect table regions on page"""
        try:
            tables_found = page.find_tables()
            table_regions = []
            
            for table_num, table in enumerate(tables_found.tables):
                table_regions.append({
                    "region_type": "table",
                    "page_number": page.number + 1,
                    "table_number": table_num + 1,
                    "bbox": list(table.bbox),
                    "confidence": 0.9
                })
            
            return table_regions
            
        except Exception as e:
            logger.warning(f"Error detecting tables: {str(e)}")
            return []
    
    def _detect_images(self, page) -> List[Dict[str, Any]]:
        """Detect image regions on page"""
        try:
            image_list = page.get_images()
            image_regions = []
            
            for img_num, img_info in enumerate(image_list):
                xref = img_info[0]
                
                # Try to get image position
                # This is simplified - in production you'd use more sophisticated methods
                image_regions.append({
                    "region_type": "image",
                    "page_number": page.number + 1,
                    "image_number": img_num + 1,
                    "xref": xref,
                    "bbox": [0, 0, 100, 100],  # Placeholder
                    "confidence": 0.7
                })
            
            return image_regions
            
        except Exception as e:
            logger.warning(f"Error detecting images: {str(e)}")
            return []
    
    def _detect_text_blocks(self, page) -> List[Dict[str, Any]]:
        """Detect text blocks on page"""
        try:
            # Get text blocks
            blocks = page.get_text("blocks")
            text_regions = []
            
            for block_num, block in enumerate(blocks):
                if block['type'] == 0:  # Text block
                    bbox = block['bbox']
                    
                    # Classify text block type based on position and content
                    block_type = self._classify_text_block(block, page)
                    
                    text_regions.append({
                        "region_type": block_type,
                        "page_number": page.number + 1,
                        "block_number": block_num + 1,
                        "bbox": list(bbox),
                        "content": block['text'] if 'text' in block else '',
                        "confidence": 0.75
                    })
            
            return text_regions
            
        except Exception as e:
            logger.warning(f"Error detecting text blocks: {str(e)}")
            return []
    
    def _classify_text_block(self, block: Dict[str, Any], page) -> str:
        """
        Classify text block type
        
        Args:
            block: Text block dictionary
            page: Page object
            
        Returns:
            Block type string
        """
        try:
            # Get block position
            bbox = block['bbox']
            y_position = bbox[1]
            page_height = page.rect.height
            
            # Top of page might be heading
            if y_position < page_height * 0.15:
                return "heading"
            
            # Check if text looks like a heading (short, possibly bold)
            if 'text' in block:
                text = block['text']
                if len(text) < 100 and len(text.split()) < 10:
                    return "heading"
            
            return "text"
            
        except Exception as e:
            logger.warning(f"Error classifying text block: {str(e)}")
            return "text"
    
    def get_page_structure(self, file_path: str) -> Dict[str, Any]:
        """
        Get overall document structure
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Document structure summary
        """
        try:
            layout = self.detect(file_path)
            
            # Analyze structure
            page_structures = {}
            for region in layout:
                page_num = region['page_number']
                region_type = region['region_type']
                
                if page_num not in page_structures:
                    page_structures[page_num] = {}
                
                if region_type not in page_structures[page_num]:
                    page_structures[page_num][region_type] = 0
                
                page_structures[page_num][region_type] += 1
            
            return {
                "total_pages": len(page_structures),
                "page_structures": page_structures,
                "total_regions": len(layout),
                "region_types": list(set(r['region_type'] for r in layout))
            }
            
        except Exception as e:
            logger.error(f"Error getting page structure: {str(e)}")
            return {}