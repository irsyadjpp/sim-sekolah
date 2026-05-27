import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging
import io

logger = logging.getLogger(__name__)


class OCRExtractor:
    """OCR processing for documents using Tesseract"""
    
    def __init__(self):
        """Initialize OCR extractor"""
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        self.tesseract_available = self._check_tesseract()
        self.default_language = 'ind+eng'  # Indonesian + English
    
    def _check_tesseract(self) -> bool:
        """Check if Tesseract OCR is available"""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR is available")
            return True
        except Exception as e:
            logger.warning(f"Tesseract OCR not available: {str(e)}")
            return False
    
    def extract(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform OCR on document
        
        Args:
            file_path: Path to document file
            options: OCR options
            
        Returns:
            OCR result with text and metadata
        """
        try:
            if not self.tesseract_available:
                logger.warning("Tesseract OCR not available, skipping OCR")
                return {
                    "text": "",
                    "confidence": 0.0,
                    "language": "unknown",
                    "error": "Tesseract not available"
                }
            
            options = options or {}
            language = options.get('ocr_language', self.default_language)
            dpi = options.get('ocr_dpi', 300)
            
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.pdf':
                return self._ocr_pdf(file_path, language, dpi)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                return self._ocr_image(file_path, language)
            else:
                logger.warning(f"OCR not optimized for {file_extension}")
                return {
                    "text": "",
                    "confidence": 0.0,
                    "language": "unknown"
                }
                
        except Exception as e:
            logger.error(f"Error performing OCR on {file_path}: {str(e)}")
            raise
    
    def _ocr_pdf(self, file_path: str, language: str, dpi: int) -> Dict[str, Any]:
        """Perform OCR on PDF document"""
        try:
            import pytesseract
            
            doc = fitz.open(file_path)
            ocr_text = []
            total_confidence = 0.0
            pages_processed = 0
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # Render page to image at specified DPI
                mat = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to bytes
                img_bytes = pix.tobytes("png")
                
                # Perform OCR
                ocr_result = pytesseract.image_to_data(
                    io.BytesIO(img_bytes),
                    lang=language,
                    output_type=pytesseract.Output.DICT
                )
                
                # Extract text and calculate confidence
                page_text = []
                page_confidence = 0.0
                words_counted = 0
                
                for i, text in enumerate(ocr_result['text']):
                    if text.strip():
                        page_text.append(text)
                        if 'conf' in ocr_result:
                            conf = ocr_result['conf'][i]
                            if conf > 0:  # -1 indicates invalid
                                page_confidence += conf
                                words_counted += 1
                
                page_full_text = ' '.join(page_text)
                ocr_text.append(page_full_text)
                
                avg_page_confidence = page_confidence / words_counted if words_counted > 0 else 0
                total_confidence += avg_page_confidence
                pages_processed += 1
                
                logger.info(f"OCR processed page {page_num + 1}, confidence: {avg_page_confidence:.2f}")
            
            doc.close()
            
            full_text = "\n\n".join(ocr_text)
            avg_confidence = total_confidence / pages_processed if pages_processed > 0 else 0.0
            
            logger.info(f"PDF OCR completed, {len(full_text)} characters, avg confidence: {avg_confidence:.2f}")
            
            return {
                "text": full_text,
                "confidence": avg_confidence,
                "language": language,
                "pages_processed": pages_processed,
                "total_words": len(full_text.split())
            }
            
        except Exception as e:
            logger.error(f"Error performing OCR on PDF: {str(e)}")
            raise
    
    def _ocr_image(self, file_path: str, language: str) -> Dict[str, Any]:
        """Perform OCR on image file"""
        try:
            import pytesseract
            from PIL import Image
            
            # Open image
            image = Image.open(file_path)
            
            # Perform OCR
            ocr_result = pytesseract.image_to_data(
                image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate confidence
            text_list = []
            total_confidence = 0.0
            words_counted = 0
            
            for i, text in enumerate(ocr_result['text']):
                if text.strip():
                    text_list.append(text)
                    if 'conf' in ocr_result:
                        conf = ocr_result['conf'][i]
                        if conf > 0:
                            total_confidence += conf
                            words_counted += 1
            
            full_text = ' '.join(text_list)
            avg_confidence = total_confidence / words_counted if words_counted > 0 else 0.0
            
            logger.info(f"Image OCR completed, {len(full_text)} characters, confidence: {avg_confidence:.2f}")
            
            return {
                "text": full_text,
                "confidence": avg_confidence,
                "language": language,
                "total_words": len(full_text.split())
            }
            
        except Exception as e:
            logger.error(f"Error performing OCR on image: {str(e)}")
            raise
    
    def extract_with_regions(self, file_path: str, language: str = None) -> Dict[str, Any]:
        """
        Perform OCR and return text with region information
        
        Args:
            file_path: Path to document file
            language: OCR language
            
        Returns:
            OCR result with region information
        """
        try:
            if not self.tesseract_available:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "language": "unknown",
                    "regions": [],
                    "error": "Tesseract not available"
                }
            
            import pytesseract
            from PIL import Image
            
            language = language or self.default_language
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.pdf':
                # For PDF, process first page for simplicity
                doc = fitz.open(file_path)
                page = doc[0]
                mat = fitz.Matrix(300 / 72, 300 / 72)
                pix = page.get_pixmap(matrix=mat)
                img_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_bytes))
                doc.close()
            else:
                image = Image.open(file_path)
            
            # Perform OCR with hOCR output for regions
            hocr = pytesseract.image_to_pdf_or_hocr(
                image,
                lang=language,
                extension='hocr'
            )
            
            # Also get standard output
            ocr_result = pytesseract.image_to_data(
                image,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text
            text = ' '.join([t for t in ocr_result['text'] if t.strip()])
            
            # Calculate confidence
            confidence = 0.0
            if 'conf' in ocr_result:
                confidences = [c for c in ocr_result['conf'] if c > 0]
                confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            # Extract basic region information
            regions = []
            for i in range(len(ocr_result['text'])):
                if ocr_result['text'][i].strip():
                    regions.append({
                        "text": ocr_result['text'][i],
                        "bbox": [
                            ocr_result['left'][i],
                            ocr_result['top'][i],
                            ocr_result['left'][i] + ocr_result['width'][i],
                            ocr_result['top'][i] + ocr_result['height'][i]
                        ],
                        "confidence": ocr_result['conf'][i] if 'conf' in ocr_result else 0
                    })
            
            return {
                "text": text,
                "confidence": confidence,
                "language": language,
                "regions": regions,
                "hocr": hocr
            }
            
        except Exception as e:
            logger.error(f"Error performing OCR with regions: {str(e)}")
            raise