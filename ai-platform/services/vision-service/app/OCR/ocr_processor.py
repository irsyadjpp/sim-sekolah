import pytesseract
from PIL import Image
import io
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class OCRProcessor:
    """OCR processing using Tesseract"""
    
    def __init__(self):
        """Initialize OCR processor"""
        self.initialized = False
        self.supported_languages = ['ind', 'eng']
        self.default_language = 'ind+eng'
        
        try:
            # Check Tesseract availability
            pytesseract.get_tesseract_version()
            self.initialized = True
            logger.info("Tesseract OCR initialized successfully")
        except Exception as e:
            logger.warning(f"Tesseract OCR not available: {str(e)}")
    
    def process(self, image_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process OCR on image
        
        Args:
            image_path: Path to image file
            options: OCR options (language, dpi, return_regions)
            
        Returns:
            OCR result with text and metadata
        """
        if not self.initialized:
            return {
                "text": "",
                "confidence": 0.0,
                "language": "unknown",
                "error": "Tesseract not available",
                "processing_time": 0.0
            }
        
        try:
            start_time = time.time()
            
            options = options or {}
            language = options.get('language', self.default_language)
            return_regions = options.get('return_regions', False)
            
            # Open image
            image = Image.open(image_path)
            
            if return_regions:
                # Get OCR with region information
                ocr_result = self._ocr_with_regions(image, language)
            else:
                # Simple OCR
                ocr_result = self._ocr_simple(image, language)
            
            processing_time = time.time() - start_time
            ocr_result['processing_time'] = processing_time
            
            logger.info(f"OCR completed in {processing_time:.2f}s, confidence: {ocr_result.get('confidence', 0.0):.2f}")
            
            return ocr_result
            
        except Exception as e:
            logger.error(f"Error processing OCR: {str(e)}")
            return {
                "text": "",
                "confidence": 0.0,
                "language": "unknown",
                "error": str(e),
                "processing_time": 0.0
            }
    
    def _ocr_simple(self, image: Image.Image, language: str) -> Dict[str, Any]:
        """Simple OCR without region information"""
        try:
            # Perform OCR
            text = pytesseract.image_to_string(image, lang=language)
            
            # Get confidence if available
            try:
                ocr_data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
                confidences = [c for c in ocr_data['conf'] if c > 0]
                confidence = sum(confidences) / len(confidences) if confidences else 0.0
            except:
                confidence = 0.0
            
            return {
                "text": text.strip(),
                "confidence": confidence,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Error in simple OCR: {str(e)}")
            raise
    
    def _ocr_with_regions(self, image: Image.Image, language: str) -> Dict[str, Any]:
        """OCR with region information"""
        try:
            # Get detailed OCR data
            ocr_data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
            
            # Extract text
            text_list = []
            for i in range(len(ocr_data['text'])):
                if ocr_data['text'][i].strip():
                    text_list.append(ocr_data['text'][i])
            
            full_text = ' '.join(text_list)
            
            # Calculate confidence
            confidences = [c for c in ocr_data['conf'] if c > 0]
            confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            # Extract regions
            regions = []
            for i in range(len(ocr_data['text'])):
                if ocr_data['text'][i].strip():
                    region = {
                        "text": ocr_data['text'][i],
                        "bbox": [
                            ocr_data['left'][i],
                            ocr_data['top'][i],
                            ocr_data['left'][i] + ocr_data['width'][i],
                            ocr_data['top'][i] + ocr_data['height'][i]
                        ],
                        "confidence": ocr_data['conf'][i] if ocr_data['conf'][i] > 0 else 0
                    }
                    regions.append(region)
            
            return {
                "text": full_text,
                "confidence": confidence,
                "language": language,
                "regions": regions
            }
            
        except Exception as e:
            logger.error(f"Error in OCR with regions: {str(e)}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Resize if too large
            max_size = 3000
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.LANCZOS)
            
            return image
            
        except Exception as e:
            logger.warning(f"Error preprocessing image: {str(e)}")
            return image
    
    def enhance_contrast(self, image: Image.Image) -> Image.Image:
        """Enhance image contrast for better OCR"""
        try:
            from PIL import ImageEnhance
            
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            return image
            
        except Exception as e:
            logger.warning(f"Error enhancing contrast: {str(e)}")
            return image
    
    def is_available(self) -> bool:
        """Check if Tesseract OCR is available"""
        return self.initialized
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.supported_languages