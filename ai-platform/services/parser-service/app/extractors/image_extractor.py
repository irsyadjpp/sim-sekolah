import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging
import io

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Extract images from documents using PyMuPDF"""
    
    def __init__(self):
        """Initialize image extractor"""
        self.supported_formats = ['.pdf']
        self.image_min_size = 100  # minimum dimension in pixels
    
    def extract(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Extract images from document
        
        Args:
            file_path: Path to document file
            options: Extraction options
            
        Returns:
            List of extracted images
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension != '.pdf':
                logger.warning(f"Image extraction optimized for PDF, got {file_extension}")
                return []
            
            options = options or {}
            self.image_min_size = options.get('image_min_size', 100)
            
            return self._extract_from_pdf(file_path)
                
        except Exception as e:
            logger.error(f"Error extracting images from {file_path}: {str(e)}")
            return []
    
    def _extract_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract images from PDF using PyMuPDF"""
        try:
            doc = fitz.open(file_path)
            images = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_num, img_info in enumerate(image_list):
                    try:
                        xref = img_info[0]
                        base_image = doc.extract_image(xref)
                        
                        # Check image size
                        if base_image['width'] < self.image_min_size or base_image['height'] < self.image_min_size:
                            logger.debug(f"Skipping small image on page {page_num + 1}")
                            continue
                        
                        # Get image metadata
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # Determine image type (basic classification)
                        image_type = self._classify_image(base_image, page, img_num)
                        
                        # Get image position (if available)
                        bbox = self._get_image_position(page, xref)
                        
                        image_info = {
                            "page_number": page_num + 1,
                            "image_number": img_num + 1,
                            "image_type": image_type,
                            "format": image_ext,
                            "width": base_image['width'],
                            "height": base_image['height'],
                            "size": len(image_bytes),
                            "xref": xref,
                            "bbox": bbox if bbox else None
                        }
                        
                        images.append(image_info)
                        logger.info(f"Extracted image on page {page_num + 1}: {image_type} ({base_image['width']}x{base_image['height']})")
                        
                    except Exception as e:
                        logger.warning(f"Error extracting image {img_num} from page {page_num + 1}: {str(e)}")
                        continue
            
            doc.close()
            logger.info(f"Total images extracted: {len(images)}")
            
            return images
            
        except Exception as e:
            logger.error(f"Error extracting images from PDF: {str(e)}")
            return []
    
    def _classify_image(self, base_image: Dict[str, Any], page, img_num: int) -> str:
        """
        Classify image type (basic classification)
        
        Args:
            base_image: Base image dictionary from PyMuPDF
            page: Page object
            img_num: Image number
            
        Returns:
            Image type string
        """
        # Simple classification based on dimensions and properties
        width = base_image['width']
        height = base_image['height']
        aspect_ratio = width / height if height > 0 else 0
        
        # Basic heuristics
        if aspect_ratio > 3.0 or aspect_ratio < 0.33:
            return "chart"  # Wide or very tall images often charts
        elif width > 1000 or height > 1000:
            return "photo"  # Large images often photos
        elif 0.8 < aspect_ratio < 1.2:
            return "diagram"  # Square-ish images often diagrams
        else:
            return "image"  # Default classification
    
    def _get_image_position(self, page, xref: int) -> Optional[List[int]]:
        """
        Get image bounding box position on page
        
        Args:
            page: Page object
            xref: Image xref
            
        Returns:
            Bounding box [x1, y1, x2, y2] or None
        """
        try:
            # Find image location on page
            for img in page.get_images():
                if img[0] == xref:
                    # Try to get bounding box from page
                    # This is a simplified approach
                    # In production, you'd use more sophisticated methods
                    return [0, 0, 100, 100]  # Placeholder
            return None
        except Exception as e:
            logger.warning(f"Error getting image position: {str(e)}")
            return None
    
    def extract_image_as_base64(self, file_path: str, page_num: int, img_num: int) -> Optional[str]:
        """
        Extract specific image as base64 encoded string
        
        Args:
            file_path: Path to PDF file
            page_num: Page number (1-indexed)
            img_num: Image number on page (1-indexed)
            
        Returns:
            Base64 encoded image string or None
        """
        try:
            doc = fitz.open(file_path)
            page = doc[page_num - 1]
            image_list = page.get_images()
            
            if img_num <= len(image_list):
                xref = image_list[img_num - 1][0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Convert to base64
                import base64
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                
                doc.close()
                return image_b64
            else:
                doc.close()
                return None
                
        except Exception as e:
            logger.error(f"Error extracting image as base64: {str(e)}")
            return None
    
    def count_images(self, file_path: str) -> int:
        """
        Count total images in document
        
        Args:
            file_path: Path to document file
            
        Returns:
            Total number of images
        """
        try:
            images = self.extract(file_path)
            return len(images)
        except Exception as e:
            logger.error(f"Error counting images: {str(e)}")
            return 0