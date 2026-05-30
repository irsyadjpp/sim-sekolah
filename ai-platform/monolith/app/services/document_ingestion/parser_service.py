"""
Parser Service - Monolith Architecture
Document parsing functionality with complete business logic from legacy parser-service
"""
import sys
import logging
import time
import fitz  # PyMuPDF
from typing import Dict, Any, List, Optional
from pathlib import Path
import tempfile
import base64
import uuid

sys.path.append('/app')

# Import actual working components from monolith structure
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.models.multimodal import (
    MultimodalAnalyzer,
    MultimodalNode,
    MediaType,
    MediaContent,
    MediaRole
)
from app.extractors.layout_detector import LayoutDetector
from app.extractors.enhanced_layout_detector import EnhancedLayoutDetector
from app.extractors.formula_extractor import FormulaExtractor
from app.extractors.figure_extractor import FigureExtractor
from app.pipelines.document_pipeline import DocumentPipeline
from app.pipelines.modern_document_pipeline import ModernDocumentPipeline
from app.pipelines.reading_order_resolver import ReadingOrderResolver
from app.pipelines.region_classifier import RegionClassifier
from app.normalizers.content_normalizer import ContentNormalizer

logger = logging.getLogger(__name__)


class ParserService:
    """
    Parser service with complete business logic from legacy parser-service
    Implements modern document understanding pipeline
    """
    
    def __init__(self):
        """Initialize parser service with actual components"""
        self.initialized = False
        
        # Initialize modern pipeline components
        try:
            self.layout_detector = EnhancedLayoutDetector()
            self.reading_order_resolver = ReadingOrderResolver()
            self.region_classifier = RegionClassifier()
            
            # Initialize extractors (region-aware)
            self.ocr_extractor = OCRExtractor()
            self.table_extractor = TableExtractor()
            self.formula_extractor = FormulaExtractor()
            self.figure_extractor = FigureExtractor()
            
            # Initialize multimodal analyzer
            self.multimodal_analyzer = MultimodalAnalyzer()
            
            # Initialize modern pipeline
            self.modern_document_pipeline = ModernDocumentPipeline(
                layout_detector=self.layout_detector,
                reading_order_resolver=self.reading_order_resolver,
                region_classifier=self.region_classifier,
                ocr_extractor=self.ocr_extractor,
                table_extractor=self.table_extractor,
                formula_extractor=self.formula_extractor,
                figure_extractor=self.figure_extractor
            )
            
            # Keep old pipeline for backward compatibility
            self.image_extractor = ImageExtractor()
            self.layout_detector_old = LayoutDetector()
            self.content_normalizer = ContentNormalizer()
            self.document_pipeline = DocumentPipeline(
                table_extractor=self.table_extractor,
                image_extractor=self.image_extractor,
                ocr_extractor=self.ocr_extractor,
                layout_detector=self.layout_detector_old,
                content_normalizer=self.content_normalizer
            )
            
            logger.info("Parser service components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing parser components: {e}")
            # Set components to None for graceful degradation
            self.layout_detector = None
            self.modern_document_pipeline = None
            self.document_pipeline = None
    
    def initialize(self):
        """Initialize parser service"""
        try:
            logger.info("Initializing Parser Service with complete business logic")
            self.initialized = True
            logger.info("Parser Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Parser Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for parser service"""
        components = {}
        if self.layout_detector:
            components["layout_detector"] = "ready"
        if self.modern_document_pipeline:
            components["modern_pipeline"] = "ready"
        if self.document_pipeline:
            components["legacy_pipeline"] = "ready"
        if self.table_extractor:
            components["table_extractor"] = "ready"
        if self.ocr_extractor:
            components["ocr_extractor"] = "ready"
        if self.figure_extractor:
            components["figure_extractor"] = "ready"
        
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "parser_service",
            "architecture": "monolith",
            "components": components,
            "business_logic": "complete" if self.modern_document_pipeline else "partial"
        }
    
    async def parse_document(self, document_data: Any, document_type: str = "pdf", 
                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Parse document using modern pipeline with complete business logic
        
        Args:
            document_data: Document data (bytes or base64)
            document_type: Document type (pdf, docx, etc.)
            metadata: Document metadata
            
        Returns:
            Parsing result with complete document structure
        """
        try:
            logger.info(f"Parsing document of type: {document_type}")
            start_time = time.time()
            
            # Create temp file for processing
            temp_dir = Path(tempfile.gettempdir()) / "monolith_parser"
            temp_dir.mkdir(exist_ok=True)
            
            file_extension = self._get_file_extension(document_type)
            document_id = str(uuid.uuid4())
            temp_file_path = temp_dir / f"{document_id}{file_extension}"
            
            # Write document data
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(document_data, str):
                    decoded_data = base64.b64decode(document_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(document_data)
            
            # Use modern pipeline if available
            if self.modern_document_pipeline and file_extension == '.pdf':
                logger.info("Using modern document pipeline")
                document = self.modern_document_pipeline.process(
                    file_path=str(temp_file_path),
                    document_id=document_id,
                    options=metadata or {}
                )
                
                # Extract structured data from document
                result = self._extract_document_result(document)
            else:
                # Fallback to basic extraction
                logger.info("Using basic document extraction")
                result = await self._basic_parse_document(temp_file_path, metadata or {})
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            result["processing_time"] = time.time() - start_time
            logger.info(f"Document parsed successfully in {result['processing_time']:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing document: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def parse_document_from_path(self, file_path: str, 
                                     metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Parse document from file path
        
        Args:
            file_path: Path to document file
            metadata: Document metadata
            
        Returns:
            Parsing result
        """
        try:
            logger.info(f"Parsing document from path: {file_path}")
            start_time = time.time()
            
            document_id = str(uuid.uuid4())
            file_extension = Path(file_path).suffix.lower()
            
            # Use modern pipeline if available and it's a PDF
            if self.modern_document_pipeline and file_extension == '.pdf':
                logger.info("Using modern document pipeline")
                document = self.modern_document_pipeline.process(
                    file_path=file_path,
                    document_id=document_id,
                    options=metadata or {}
                )
                
                result = self._extract_document_result(document)
                
                # Apply multimodal analysis if available
                if self.multimodal_analyzer and result.get('success'):
                    try:
                        multimodal_nodes = self.multimodal_analyzer.analyze_multimodal_from_parser(document)
                        multimodal_stats = self.multimodal_analyzer.get_multimodal_statistics(multimodal_nodes)
                        
                        # Add multimodal analysis to result
                        result['multimodal_analysis'] = {
                            'nodes': [node.to_dict() for node in multimodal_nodes],
                            'statistics': multimodal_stats,
                            'enabled': True
                        }
                        
                        # Relate multimodal content to text chunks if available
                        if 'chunks' in result:
                            chunk_media_relations = self.multimodal_analyzer.relate_multimodal_to_chunks(
                                multimodal_nodes, result['chunks']
                            )
                            result['multimodal_analysis']['chunk_relations'] = chunk_media_relations
                        
                        logger.info(f"Multimodal analysis completed: {len(multimodal_nodes)} media items analyzed")
                    except Exception as e:
                        logger.warning(f"Multimodal analysis failed: {e}")
                        result['multimodal_analysis'] = {'enabled': False, 'error': str(e)}
            else:
                # Fallback to basic extraction
                logger.info("Using basic document extraction")
                result = await self._basic_parse_document(file_path, metadata or {})
            
            result["processing_time"] = time.time() - start_time
            logger.info(f"Document parsed successfully in {result['processing_time']:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing document from path: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _extract_document_result(self, document) -> Dict[str, Any]:
        """Extract structured result from document object"""
        try:
            # Extract pages and regions
            pages_data = []
            for page in document.pages:
                page_data = {
                    "page_number": page.page_number,
                    "regions": []
                }
                
                for region in page.regions:
                    region_data = {
                        "region_id": region.region_id,
                        "region_type": region.region_type.value if hasattr(region.region_type, 'value') else str(region.region_type),
                        "bbox": region.bbox.to_list() if hasattr(region.bbox, 'to_list') else list(region.bbox),
                        "content": region.content,
                        "confidence": region.confidence if hasattr(region, 'confidence') else 0.8
                    }
                    page_data["regions"].append(region_data)
                
                pages_data.append(page_data)
            
            return {
                "success": True,
                "document_id": document.document_id,
                "page_count": len(document.pages),
                "pages": pages_data,
                "metadata": document.metadata if hasattr(document, 'metadata') else {},
                "pipeline_version": "2.0.0",
                "extraction_method": "modern_pipeline"
            }
        except Exception as e:
            logger.error(f"Error extracting document result: {e}")
            return {
                "success": False,
                "error": str(e),
                "extraction_method": "modern_pipeline"
            }
    
    async def _basic_parse_document(self, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Basic document extraction as fallback"""
        doc = None
        try:
            # Handle encrypted PDFs
            try:
                doc = fitz.open(file_path)
            except Exception as e:
                if "encrypted" in str(e).lower() or "password" in str(e).lower():
                    logger.warning(f"PDF is encrypted: {e}")
                    return {
                        "success": False,
                        "error": "PDF is encrypted and requires password",
                        "error_type": "EncryptedPDF",
                        "extraction_method": "basic_extraction"
                    }
                else:
                    raise
            
            text_content = []
            tables = []
            images = []
            page_count = doc.page_count
            
            for page_num in range(page_count):
                page = doc[page_num]
                
                # Extract text
                page_text = page.get_text()
                text_content.append({
                    "page_number": page_num + 1,
                    "text": page_text,
                    "character_count": len(page_text)
                })
                
                # Extract tables if available
                if self.table_extractor:
                    try:
                        page_tables = page.find_tables()
                        for table in page_tables.tables:
                            tables.append({
                                "page_number": page_num + 1,
                                "bbox": list(table.bbox)
                            })
                    except Exception as e:
                        logger.warning(f"Error extracting tables from page {page_num + 1}: {e}")
                
                # Extract images if available
                if self.image_extractor:
                    try:
                        page_images = page.get_images()
                        for img in page_images:
                            images.append({
                                "page_number": page_num + 1,
                                "xref": img[0]
                            })
                    except Exception as e:
                        logger.warning(f"Error extracting images from page {page_num + 1}: {e}")
            
            # Close document before returning result
            doc.close()
            
            return {
                "success": True,
                "page_count": page_count,
                "text_content": text_content,
                "tables_found": len(tables),
                "images_found": len(images),
                "metadata": metadata,
                "pipeline_version": "1.0.0",
                "extraction_method": "basic_extraction"
            }
            
        except Exception as e:
            logger.error(f"Error in basic parse: {e}")
            if doc:
                doc.close()
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "extraction_method": "basic_extraction"
            }
    
    def _get_file_extension(self, document_type: str) -> str:
        """Get file extension for document type"""
        extensions = {
            "pdf": ".pdf",
            "docx": ".docx",
            "doc": ".doc",
            "txt": ".txt",
            "png": ".png",
            "jpg": ".jpg",
            "jpeg": ".jpeg"
        }
        return extensions.get(document_type.lower(), ".pdf")