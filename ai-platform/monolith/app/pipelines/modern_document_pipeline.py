"""
Modern Document Understanding Pipeline

Layout-first, page-centric architecture for AI-native document parsing.
Transition from "extract content" to "understand document structure".

This is the NEW pipeline that implements modern document intelligence:
- Layout Detection FIRST
- Region Segmentation
- Reading Order Reconstruction
- Region-Aware Content Extraction
- Table Extraction
- Formula Extraction
- Figure Extraction

Note: Semantic chunking and enrichment are handled by separate services:
- semantic-chunk-service: Curriculum-aware chunking
- semantic-enrichment-service: Advanced semantic tagging

OLD pipeline (document_pipeline.py) is preserved for backward compatibility.
"""
import logging
import time
import asyncio
import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List

from app.models.document_models import Document, Region, RegionType
from app.pipelines.pipeline_context import PipelineContext
from app.pipelines.reading_order_resolver import ReadingOrderResolver
from app.pipelines.region_classifier import RegionClassifier
from app.extractors.enhanced_layout_detector import EnhancedLayoutDetector
from app.extractors.table_extractor import TableExtractor
from app.extractors.formula_extractor import FormulaExtractor
from app.extractors.figure_extractor import FigureExtractor
from app.extractors.ocr_extractor import OCRExtractor

logger = logging.getLogger(__name__)


class ModernDocumentPipeline:
    """
    Modern document understanding pipeline with layout-first architecture.
    
    Stage Order (CORRECT):
    1. Layout Detection
    2. Region Segmentation
    3. Reading Order Reconstruction
    4. Region-Aware OCR
    5. Content Extraction per Region
    6. Table Extraction
    7. Formula Extraction
    8. Figure Extraction
    
    Key improvements over old pipeline:
    - Layout-first (not text-first)
    - Page-centric structure (not flat)
    - Region-aware processing (not document-wide)
    - Reading order reconstruction (not object order)
    - Shared context (not independent stages)
    
    Note: Semantic chunking and enrichment are handled by separate services:
    - semantic-chunk-service: Curriculum-aware chunking
    - semantic-enrichment-service: Advanced semantic tagging
    """
    
    def __init__(
        self,
        layout_detector: Optional[EnhancedLayoutDetector] = None,
        reading_order_resolver: Optional[ReadingOrderResolver] = None,
        region_classifier: Optional[RegionClassifier] = None,
        # Region-aware extractors
        table_extractor: Optional[TableExtractor] = None,
        formula_extractor: Optional[FormulaExtractor] = None,
        figure_extractor: Optional[FigureExtractor] = None,
        ocr_extractor: Optional[OCRExtractor] = None,
        # Legacy (deprecated)
        content_normalizer=None
    ):
        """
        Initialize modern document pipeline.
        
        Args:
            layout_detector: Enhanced layout detector with semantic classification
            reading_order_resolver: Reading order reconstruction
            region_classifier: Semantic region type classifier
            table_extractor: Region-aware table extractor
            formula_extractor: Region-aware formula extractor
            figure_extractor: Region-aware figure extractor
            ocr_extractor: Region-aware OCR extractor
            content_normalizer: Content normalizer (deprecated)
        """
        self.layout_detector = layout_detector or EnhancedLayoutDetector()
        self.reading_order_resolver = reading_order_resolver or ReadingOrderResolver()
        self.region_classifier = region_classifier or RegionClassifier()
        
        # Region-aware extractors
        self.table_extractor = table_extractor or TableExtractor()
        self.formula_extractor = formula_extractor or FormulaExtractor()
        self.figure_extractor = figure_extractor or FigureExtractor()
        self.ocr_extractor = ocr_extractor or OCRExtractor()
        
        # Legacy (deprecated)
        self.content_normalizer = content_normalizer
        
        logger.info("ModernDocumentPipeline initialized with layout-first architecture, region-aware extractors, and semantic region classification")
    
    def process(
        self, 
        file_path: str, 
        document_id: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Process document through modern understanding pipeline.
        
        Args:
            file_path: Path to document file
            document_id: Unique document identifier
            options: Processing options
            
        Returns:
            Document with page-centric structure and semantic understanding
        """
        start_time = time.time()
        
        try:
            options = options or {}
            
            # Create pipeline context for state sharing
            context = PipelineContext(
                document_id=document_id,
                file_path=file_path,
                options=options
            )
            
            logger.info(f"Starting modern document pipeline for {file_path}")
            
            # ========================================
            # STAGE 1: Layout Detection (FIRST!)
            # ========================================
            if options.get('detect_layout', True):
                stage_start = time.time()
                
                logger.info("Stage 1: Layout Detection")
                regions_by_page = self.layout_detector.detect(file_path, context)
                
                context.set_stage_result("layout_detection", regions_by_page)
                context.set_stage_timing("layout_detection", time.time() - stage_start)
                context.stages_completed.append("layout_detection")
            
            # ========================================
            # STAGE 2: Build Document Model
            # ========================================
            logger.info("Stage 2: Building Document Model")
            document = context.ensure_document()
            document.stages_completed.append("document_model")
            
            # ========================================
            # STAGE 3: Semantic Region Classification
            # ========================================
            if options.get('classify_regions', True):
                stage_start = time.time()
                
                logger.info("Stage 3: Semantic Region Classification")
                
                # Classify regions into semantic types
                self._classify_regions(document, context, options)
                
                context.set_stage_timing("region_classification", time.time() - stage_start)
                context.stages_completed.append("region_classification")
            
            # ========================================
            # STAGE 4: Reading Order Reconstruction
            # ========================================
            if options.get('resolve_reading_order', True):
                stage_start = time.time()
                
                logger.info("Stage 4: Reading Order Reconstruction")
                
                for page_number, regions in context.regions_by_page.items():
                    page = document.get_page(page_number)
                    if page:
                        ordered_regions = self.reading_order_resolver.resolve_reading_order(
                            page, regions
                        )
                        page.regions = ordered_regions
                
                context.set_stage_timing("reading_order", time.time() - stage_start)
                context.stages_completed.append("reading_order")
            
            # ========================================
            # STAGE 5: Region-Aware Content Extraction
            # ========================================
            if options.get('extract_content', True):
                stage_start = time.time()
                
                logger.info("Stage 5: Region-Aware Content Extraction")
                
                # Extract content for each region using region-aware extractors
                self._extract_region_content(document, context, options)
                
                context.set_stage_timing("content_extraction", time.time() - stage_start)
                context.stages_completed.append("content_extraction")
            
            # ========================================
            # STAGE 6: Finalize Document
            # ========================================
            document.processing_time = time.time() - start_time
            document.processed_at = context.completed_at
            document.metadata.update(context.get_stage_timings_summary())
            document.metadata["cache_stats"] = context.get_cache_stats()
            
            context.mark_completed()
            context.merge_regions_to_document()
            
            logger.info(f"Modern document pipeline completed in {document.processing_time:.2f}s")
            logger.info(f"Document statistics: {document.get_statistics()}")
            
            return document
            
        except Exception as e:
            logger.error(f"Error in modern document pipeline: {str(e)}")
            if 'context' in locals():
                context.add_error(f"Pipeline failed: {str(e)}")
                context.mark_completed()
            
            # Return minimal document with error info
            document = Document(document_id=document_id, file_path=file_path)
            document.metadata["error"] = str(e)
            document.processing_time = time.time() - start_time
            
            return document
    
    def _extract_region_content(
        self, 
        document: Document, 
        context: PipelineContext,
        options: Dict[str, Any]
    ) -> None:
        """
        Extract content for each region using region-aware extractors (NEW).
        
        This method now uses the refactored extractors that work at region level.
        """
        try:
            doc = fitz.open(document.file_path)
            
            for page in document.pages:
                fitz_page = doc[page.page_number - 1]
                
                for region in page.regions:
                    # Skip structural regions
                    if region.region_type in [RegionType.HEADER, RegionType.FOOTER, RegionType.PAGE_NUMBER]:
                        continue
                    
                    # Extract content based on region type using region-aware extractors
                    if region.region_type == RegionType.TABLE:
                        if self.table_extractor and options.get('extract_tables', True):
                            table_data = self.table_extractor.extract_from_region(region, fitz_page, options)
                            if table_data:
                                region.metadata['table_data'] = table_data
                                logger.info(f"Extracted table from region {region.region_id}")
                    
                    elif region.region_type == RegionType.FORMULA:
                        if self.formula_extractor and options.get('extract_formulas', True):
                            formula_data = self.formula_extractor.extract_from_region(region, fitz_page, options)
                            if formula_data:
                                region.metadata['formula_data'] = formula_data
                                logger.info(f"Extracted formula from region {region.region_id}")
                    
                    elif region.region_type == RegionType.FIGURE:
                        if self.figure_extractor and options.get('extract_figures', True):
                            figure_data = self.figure_extractor.extract_from_region(region, fitz_page, options)
                            if figure_data:
                                region.metadata['figure_data'] = figure_data
                                logger.info(f"Extracted figure from region {region.region_id}")
                    
                    # OCR for regions that need it (e.g., scanned regions)
                    elif options.get('apply_ocr', False) and self.ocr_extractor:
                        ocr_data = self.ocr_extractor.extract_from_region(region, fitz_page, options)
                        if ocr_data:
                            region.metadata['ocr_data'] = ocr_data
                            # Update text content with OCR result if available
                            if ocr_data.get('text') and not region.text_content:
                                region.text_content = ocr_data['text']
                            logger.info(f"Applied OCR to region {region.region_id}")
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error in region-aware content extraction: {e}")
            context.add_error(f"Region-aware extraction failed: {e}")
    
    def _classify_regions(
        self, 
        document: Document, 
        context: PipelineContext,
        options: Dict[str, Any]
    ) -> None:
        """
        Classify regions into semantic types using RegionClassifier.
        
        This method enhances the basic layout detection with semantic understanding.
        """
        try:
            doc = fitz.open(document.file_path)
            
            for page in document.pages:
                fitz_page = doc[page.page_number - 1]
                
                # Classify all regions on this page
                classifications = self.region_classifier.classify_regions(
                    regions=page.regions,
                    page_number=page.page_number,
                    page_width=page.width,
                    page_height=page.height,
                    context={"document_type": document.document_type}
                )
                
                logger.info(f"Classified {len(classifications)} regions on page {page.page_number}")
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error in region classification: {e}")
            context.add_error(f"Region classification failed: {e}")
    
    async def process_async(
        self, 
        file_path: str, 
        document_id: str,
        options: Optional[Dict[str, Any]] = None
    ):
        """
        Process document asynchronously with parallel stage execution.
        
        This implementation uses asyncio.gather for parallel processing:
        - Layout detection can run in parallel for multiple pages
        - Region classification can run in parallel for multiple pages
        - Content extraction can run in parallel for multiple regions
        
        Args:
            file_path: Path to document file
            document_id: Unique document identifier
            options: Processing options
            
        Returns:
            Processed document
        """
        options = options or {}
        start_time = time.time()
        
        logger.info(f"Starting async document processing: {file_path}")
        
        # Initialize context
        context = PipelineContext(file_path, document_id)
        
        # ========================================
        # STAGE 1: Layout Detection (Async - Parallel per page)
        # ========================================
        if options.get('detect_layout', True):
            stage_start = time.time()
            
            logger.info("Stage 1 (Async): Layout Detection")
            
            # Open document once
            doc = fitz.open(file_path)
            
            # Create async tasks for each page
            layout_tasks = []
            for page_num in range(doc.page_count):
                task = self._detect_layout_async(doc, page_num, context, options)
                layout_tasks.append(task)
            
            # Run all layout detection tasks in parallel
            await asyncio.gather(*layout_tasks)
            
            doc.close()
            
            context.set_stage_timing("layout_detection", time.time() - stage_start)
            context.stages_completed.append("layout_detection")
        
        # ========================================
        # STAGE 2: Build Document Model
        # ========================================
        logger.info("Stage 2: Building Document Model")
        document = context.ensure_document()
        document.stages_completed.append("document_model")
        
        # ========================================
        # STAGE 3: Semantic Region Classification (Async - Parallel per page)
        # ========================================
        if options.get('classify_regions', True):
            stage_start = time.time()
            
            logger.info("Stage 3 (Async): Semantic Region Classification")
            
            # Create async tasks for each page
            classification_tasks = []
            for page in document.pages:
                task = self._classify_regions_async(page, context, options)
                classification_tasks.append(task)
            
            # Run all classification tasks in parallel
            await asyncio.gather(*classification_tasks)
            
            context.set_stage_timing("region_classification", time.time() - stage_start)
            context.stages_completed.append("region_classification")
        
        # ========================================
        # STAGE 4: Reading Order Reconstruction (Async - Parallel per page)
        # ========================================
        if options.get('resolve_reading_order', True):
            stage_start = time.time()
            
            logger.info("Stage 4 (Async): Reading Order Reconstruction")
            
            # Create async tasks for each page
            reading_order_tasks = []
            for page in document.pages:
                task = self._resolve_reading_order_async(page, context, options)
                reading_order_tasks.append(task)
            
            # Run all reading order tasks in parallel
            await asyncio.gather(*reading_order_tasks)
            
            context.set_stage_timing("reading_order", time.time() - stage_start)
            context.stages_completed.append("reading_order")
        
        # ========================================
        # STAGE 5: Region-Aware Content Extraction (Async - Parallel per region)
        # ========================================
        if options.get('extract_content', True):
            stage_start = time.time()
            
            logger.info("Stage 5 (Async): Region-Aware Content Extraction")
            
            # Create async tasks for each region
            extraction_tasks = []
            doc = fitz.open(file_path)
            
            for page in document.pages:
                fitz_page = doc[page.page_number - 1]
                for region in page.regions:
                    # Skip structural regions
                    if region.region_type in [RegionType.HEADER, RegionType.FOOTER, RegionType.PAGE_NUMBER]:
                        continue
                    
                    task = self._extract_region_content_async(region, fitz_page, context, options)
                    extraction_tasks.append(task)
            
            # Run all extraction tasks in parallel
            await asyncio.gather(*extraction_tasks)
            
            doc.close()
            
            context.set_stage_timing("content_extraction", time.time() - stage_start)
            context.stages_completed.append("content_extraction")
        
        # ========================================
        # STAGE 6: Semantic Services Integration (Sequential)
        # ========================================
        if options.get('use_semantic_services', False):
            stage_start = time.time()
            
            logger.info("Stage 6: Semantic Services Integration")
            
            # This stage is sequential (external service call)
            document = self.semantic_services_integration.process_with_semantic_services(
                document, options
            )
            
            context.set_stage_timing("semantic_services_integration", time.time() - stage_start)
            context.stages_completed.append("semantic_services_integration")
        else:
            # ========================================
            # STAGE 6: Semantic Chunking (Sequential)
            # ========================================
            if options.get('chunk_content', True):
                stage_start = time.time()
                
                logger.info("Stage 6: Semantic Chunking (built-in)")
                
                chunks = self.semantic_chunker.chunk_document(document)
                
                context.set_stage_result("semantic_chunking", chunks)
                context.set_stage_timing("semantic_chunking", time.time() - stage_start)
                context.stages_completed.append("semantic_chunking")
        
        # ========================================
        # Finalize Document
        # ========================================
        document.processing_time = time.time() - start_time
        document.metadata = {
            "stages_completed": context.stages_completed,
            "stage_timings": context.stage_timings,
            "errors": context.errors
        }
        
        logger.info(f"Async document pipeline completed in {document.processing_time:.2f}s")
        
        return document
    
    async def _detect_layout_async(
        self, 
        doc: fitz.Document, 
        page_num: int, 
        context: PipelineContext,
        options: Dict[str, Any]
    ) -> None:
        """Async wrapper for layout detection on a single page."""
        page = doc[page_num]
        regions = self.layout_detector.detect_layout(page, page_num + 1)
        context.add_regions(regions)
    
    async def _classify_regions_async(
        self, 
        page, 
        context: PipelineContext,
        options: Dict[str, Any]
    ) -> None:
        """Async wrapper for region classification on a single page."""
        classifications = self.region_classifier.classify_regions(
            regions=page.regions,
            page_number=page.page_number,
            page_width=page.width,
            page_height=page.height,
            context={"document_type": context.document_type}
        )
    
    async def _resolve_reading_order_async(
        self, 
        page, 
        context: PipelineContext,
        options: Dict[str, Any]
    ) -> None:
        """Async wrapper for reading order resolution on a single page."""
        ordered_regions = self.reading_order_resolver.resolve_reading_order(
            page, page.regions
        )
        page.regions = ordered_regions
    
    async def _extract_region_content_async(
        self, 
        region: Region, 
        fitz_page: fitz.Page,
        context: PipelineContext,
        options: Dict[str, Any]
    ) -> None:
        """Async wrapper for region content extraction on a single region."""
        # Extract content based on region type using region-aware extractors
        if region.region_type == RegionType.TABLE:
            if self.table_extractor and options.get('extract_tables', True):
                table_data = self.table_extractor.extract_from_region(region, fitz_page, options)
                if table_data:
                    region.metadata['table_data'] = table_data
        
        elif region.region_type == RegionType.FORMULA:
            if self.formula_extractor and options.get('extract_formulas', True):
                formula_data = self.formula_extractor.extract_from_region(region, fitz_page, options)
                if formula_data:
                    region.metadata['formula_data'] = formula_data
        
        elif region.region_type == RegionType.FIGURE:
            if self.figure_extractor and options.get('extract_figures', True):
                figure_data = self.figure_extractor.extract_from_region(region, fitz_page, options)
                if figure_data:
                    region.metadata['figure_data'] = figure_data
        
        # OCR for regions that need it
        elif options.get('apply_ocr', False) and self.ocr_extractor:
            ocr_data = self.ocr_extractor.extract_from_region(region, fitz_page, options)
            if ocr_data:
                region.metadata['ocr_data'] = ocr_data
                if ocr_data.get('text') and not region.text_content:
                    region.text_content = ocr_data['text']
