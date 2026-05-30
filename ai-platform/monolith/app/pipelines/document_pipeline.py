"""
LEGACY MODULE - DEPRECATED

This module is maintained for backward compatibility only.
New implementations should use ModernDocumentPipeline from modern_document_pipeline.py

TODO: Migrate all usages to ModernDocumentPipeline and remove this file.
"""

from typing import Optional, Dict, Any, List
import logging
import time

logger = logging.getLogger(__name__)


class DocumentPipeline:
    """Main document processing pipeline that orchestrates all extractors"""
    
    def __init__(
        self,
        text_extractor,
        table_extractor,
        image_extractor,
        ocr_extractor,
        layout_detector,
        content_normalizer
    ):
        """Initialize document pipeline with all extractors"""
        self.text_extractor = text_extractor
        self.table_extractor = table_extractor
        self.image_extractor = image_extractor
        self.ocr_extractor = ocr_extractor
        self.layout_detector = layout_detector
        self.content_normalizer = content_normalizer
    
    def process(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process document through complete pipeline
        
        Args:
            file_path: Path to document file
            options: Processing options
            
        Returns:
            Complete extraction result
        """
        start_time = time.time()
        
        try:
            options = options or {}
            
            logger.info(f"Starting document pipeline for {file_path}")
            
            result = {
                "document_id": options.get("document_id"),
                "file_path": file_path,
                "timestamp": time.time(),
                "stages": {}
            }
            
            # Stage 1: Text Extraction
            if options.get('extract_text', True):
                text_result = self._extract_text(file_path, options)
                result["text_content"] = text_result
                result["stages"]["text_extraction"] = {"status": "completed"}
            else:
                result["stages"]["text_extraction"] = {"status": "skipped"}
            
            # Stage 2: Table Extraction
            if options.get('extract_tables', True):
                tables_result = self._extract_tables(file_path, options)
                result["tables"] = tables_result
                result["stages"]["table_extraction"] = {"status": "completed", "count": len(tables_result)}
            else:
                result["stages"]["table_extraction"] = {"status": "skipped"}
            
            # Stage 3: Image Extraction
            if options.get('extract_images', True):
                images_result = self._extract_images(file_path, options)
                result["images"] = images_result
                result["stages"]["image_extraction"] = {"status": "completed", "count": len(images_result)}
            else:
                result["stages"]["image_extraction"] = {"status": "skipped"}
            
            # Stage 4: Layout Detection
            if options.get('extract_layout', True):
                layout_result = self._detect_layout(file_path, options)
                result["layout"] = layout_result
                result["stages"]["layout_detection"] = {"status": "completed", "count": len(layout_result)}
            else:
                result["stages"]["layout_detection"] = {"status": "skipped"}
            
            # Stage 5: OCR Processing (if requested)
            if options.get('perform_ocr', True):
                ocr_result = self._perform_ocr(file_path, options)
                result["ocr_content"] = ocr_result
                result["stages"]["ocr_processing"] = {"status": "completed"}
            else:
                result["stages"]["ocr_processing"] = {"status": "skipped"}
            
            # Stage 6: Content Normalization
            if options.get('normalize_content', True):
                normalization_result = self._normalize_content(result, options)
                result["normalized_content"] = normalization_result
                result["stages"]["content_normalization"] = {"status": "completed"}
            else:
                result["stages"]["content_normalization"] = {"status": "skipped"}
            
            # Stage 7: Metadata Extraction
            metadata_result = self._extract_metadata(file_path)
            result["metadata"] = metadata_result
            result["stages"]["metadata_extraction"] = {"status": "completed"}
            
            # Stage 8: Statistics Generation
            statistics_result = self._extract_statistics(file_path)
            result["statistics"] = statistics_result
            result["stages"]["statistics_generation"] = {"status": "completed"}
            
            # Calculate processing time
            processing_time = time.time() - start_time
            result["processing_time"] = processing_time
            result["stages"]["total_processing_time"] = processing_time
            
            logger.info(f"Document pipeline completed in {processing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in document pipeline: {str(e)}")
            result["error"] = str(e)
            result["stages"]["pipeline"] = {"status": "failed"}
            result["processing_time"] = time.time() - start_time
            return result
    
    def _extract_text(self, file_path: str, options: Dict[str, Any]) -> str:
        """Extract text from document"""
        try:
            text = self.text_extractor.extract(file_path, options)
            
            if options.get('normalize_content', True):
                text = self.content_normalizer.normalize(text, options)
            
            return text
            
        except Exception as e:
            logger.error(f"Error in text extraction stage: {str(e)}")
            return ""
    
    def _extract_tables(self, file_path: str, options: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tables from document"""
        try:
            tables = self.table_extractor.extract(file_path, options)
            return tables
        except Exception as e:
            logger.error(f"Error in table extraction stage: {str(e)}")
            return []
    
    def _extract_images(self, file_path: str, options: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract images from document"""
        try:
            images = self.image_extractor.extract(file_path, options)
            return images
        except Exception as e:
            logger.error(f"Error in image extraction stage: {str(e)}")
            return []
    
    def _detect_layout(self, file_path: str, options: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect layout in document"""
        try:
            layout = self.layout_detector.detect(file_path, options)
            return layout
        except Exception as e:
            logger.error(f"Error in layout detection stage: {str(e)}")
            return []
    
    def _perform_ocr(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Perform OCR on document"""
        try:
            ocr_options = {
                'ocr_language': options.get('ocr_language', 'ind+eng'),
                'ocr_dpi': options.get('ocr_dpi', 300)
            }
            ocr_result = self.ocr_extractor.extract(file_path, ocr_options)
            return ocr_result
        except Exception as e:
            logger.error(f"Error in OCR stage: {str(e)}")
            return {"text": "", "error": str(e)}
    
    def _normalize_content(self, result: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Normalize content from extraction results"""
        try:
            # Normalize text content
            if "text_content" in result:
                normalized_text = self.content_normalizer.normalize(
                    result["text_content"], 
                    options
                )
                return normalized_text
            
            return ""
        except Exception as e:
            logger.error(f"Error in content normalization stage: {str(e)}")
            return ""
    
    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from document"""
        try:
            metadata = self.content_normalizer.extract_metadata(file_path)
            return metadata
        except Exception as e:
            logger.error(f"Error in metadata extraction stage: {str(e)}")
            return {}
    
    def _extract_statistics(self, file_path: str) -> Dict[str, Any]:
        """Extract statistics from document"""
        try:
            statistics = self.content_normalizer.extract_statistics(file_path)
            return statistics
        except Exception as e:
            logger.error(f"Error in statistics extraction stage: {str(e)}")
            return {}
    
    def process_async(self, file_path: str, options: Optional[Dict[str, Any]] = None):
        """
        Process document asynchronously (for background processing)
        
        Args:
            file_path: Path to document file
            options: Processing options
            
        Returns:
            Async generator that yields results as they become available
        """
        import asyncio
        
        async def async_process():
            try:
                # This is a simplified async version
                # In production, you'd have true async processing for each stage
                
                # Stage 1: Text
                if options.get('extract_text', True):
                    yield {"stage": "text_extraction", "status": "started"}
                    text_result = self._extract_text(file_path, options)
                    yield {"stage": "text_extraction", "status": "completed", "result": text_result}
                
                # Stage 2: Tables
                if options.get('extract_tables', True):
                    yield {"stage": "table_extraction", "status": "started"}
                    tables_result = self._extract_tables(file_path, options)
                    yield {"stage": "table_extraction", "status": "completed", "result": tables_result}
                
                # Continue with other stages...
                
            except Exception as e:
                yield {"stage": "pipeline", "status": "error", "error": str(e)}
        
        return async_process()